"""
Main Astrology Engine Orchestrator.

Generates ALL 15 divisional charts, global calculations (Dasha, Gochar,
Shadbala, Ashtakavarga, Karakas, friendships), and packages them into
a single FullChartBundle.

This is called ONCE when the user submits birth details. The result
is cached and reused across all future LLM prompts.
"""

import datetime
from dataclasses import asdict

from services.astrology.swiss_ephemeris import (
    datetime_to_jd,
    get_sidereal_positions,
    get_house_cusps,
    get_lahiri_ayanamsa,
)
from services.astrology.planets import (
    ZODIAC_SIGNS,
    SIGN_LORDS,
    PLANET_NAMES_SANSKRIT,
    EXALTATION_DEBILITATION,
    get_sign_name,
    get_planet_dignity,
)
from services.astrology.nakshatra import calculate_nakshatra
from services.astrology.houses import HOUSE_SIGNIFICATORS
from services.astrology.yogas import detect_yogas
from services.astrology.houses import calculate_planet_houses

from backend.astrology.types import (
    BirthDetails,
    NakshatraInfo,
    PlanetPosition,
    HouseCusp,
    ChartData,
    DashaData,
    KarakaData,
    FullChartBundle,
)
from backend.astrology.divisional import (
    compute_varga_position,
    ALL_VARGA_NAMES,
)
from backend.astrology.strength import (
    is_combust,
    is_retrograde,
    get_planet_speed,
    SWE_PLANET_IDS,
    SEVEN_PLANETS,
    compute_shadbala,
    compute_ashtakavarga,
    compute_natural_friendships,
    compute_temporal_friendships,
    compute_compound_friendships,
    classify_benefic_malefic,
)
from backend.astrology.dasha import (
    calculate_full_vimshottari,
    get_current_periods,
)
from backend.astrology.gochar import build_gochar_data


ALL_PLANETS = ["sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn", "rahu", "ketu"]


# ===================================================================
# Vedic Aspects
# ===================================================================

def _compute_aspects(planet_houses: dict) -> list:
    """Compute Vedic Drishti (aspects) for all planets."""
    aspects = []
    for p_name, house in planet_houses.items():
        # Standard 7th aspect (all planets)
        t7 = ((house + 6) % 12) + 1 if ((house + 6) % 12) != 0 else 12
        # Recalculate properly: target_house = (house - 1 + offset) % 12 + 1
        t7 = ((house - 1 + 6) % 12) + 1
        aspects.append(f"{p_name.capitalize()} aspects House {t7}")

        if p_name == "mars":
            t4 = ((house - 1 + 3) % 12) + 1
            t8 = ((house - 1 + 7) % 12) + 1
            aspects.append(f"Mars aspects House {t4}")
            aspects.append(f"Mars aspects House {t8}")
        elif p_name == "jupiter":
            t5 = ((house - 1 + 4) % 12) + 1
            t9 = ((house - 1 + 8) % 12) + 1
            aspects.append(f"Jupiter aspects House {t5}")
            aspects.append(f"Jupiter aspects House {t9}")
        elif p_name == "saturn":
            t3 = ((house - 1 + 2) % 12) + 1
            t10 = ((house - 1 + 9) % 12) + 1
            aspects.append(f"Saturn aspects House {t3}")
            aspects.append(f"Saturn aspects House {t10}")
    return aspects


# ===================================================================
# Conjunctions
# ===================================================================

def _compute_conjunctions(planet_houses: dict) -> list:
    """Find planets sharing the same house (conjunction)."""
    house_to_planets = {}
    for p_name, house in planet_houses.items():
        house_to_planets.setdefault(house, []).append(p_name)

    conjunctions = []
    for house, planets in house_to_planets.items():
        if len(planets) > 1:
            names = " & ".join(p.capitalize() for p in sorted(planets))
            conjunctions.append(f"{names} conjunct in House {house}")
    return conjunctions


# ===================================================================
# Chara Karakas
# ===================================================================

def _compute_karakas(positions: dict) -> KarakaData:
    """
    Compute Jaimini Chara Karakas.
    The planet with the highest degree (within its sign) is Atmakaraka,
    the next is Amatyakaraka, and so on (7 Karakas using 7 planets, Rahu excluded).
    """
    degrees = {}
    for planet in SEVEN_PLANETS:
        lon = positions.get(planet, 0.0)
        degrees[planet] = lon % 30.0

    # Sort by degree descending
    sorted_planets = sorted(degrees.keys(), key=lambda p: degrees[p], reverse=True)

    karaka_names = [
        "atmakaraka",
        "amatyakaraka",
        "bhratrikaraka",
        "matrikaraka",
        "putrakaraka",
        "gnatikaraka",
        "darakaraka",
    ]

    karaka_dict = {}
    for i, k_name in enumerate(karaka_names):
        if i < len(sorted_planets):
            karaka_dict[k_name] = sorted_planets[i]
        else:
            karaka_dict[k_name] = ""

    return KarakaData(**karaka_dict)


# ===================================================================
# Build a single ChartData for any Varga
# ===================================================================

def _build_chart_data(
    varga_name: str,
    d1_positions: dict,
    d1_ascendant: float,
    jd: float,
    sun_longitude: float,
) -> ChartData:
    """
    Build a complete ChartData for the given Varga division.

    For D1, positions are the natal sidereal positions.
    For other vargas, each planet's position is projected into its Varga sign.
    """
    # Compute Varga sign for each planet
    varga_longitudes = {}
    for planet, lon in d1_positions.items():
        varga_sign_idx = compute_varga_position(lon, varga_name)
        # Use the sign midpoint as representative longitude in this varga
        varga_longitudes[planet] = varga_sign_idx * 30.0 + (lon % 30.0) * (30.0 / 30.0)
        # Actually, in Varga charts we keep the degree within sign from D1
        # but place it in the new sign
        degree_in_sign = lon % 30.0
        varga_longitudes[planet] = varga_sign_idx * 30.0 + degree_in_sign

    # Compute Ascendant for this Varga
    asc_varga_sign_idx = compute_varga_position(d1_ascendant, varga_name)
    asc_degree = d1_ascendant % 30.0
    varga_ascendant = asc_varga_sign_idx * 30.0 + asc_degree

    # House mapping (Whole Sign: Asc sign = House 1)
    planet_house_map = {}
    for planet, lon in varga_longitudes.items():
        p_sign = int(lon // 30) % 12
        house = ((p_sign - asc_varga_sign_idx) % 12) + 1
        planet_house_map[planet] = house

    # Planet sign mapping
    planet_sign_map = {planet: ZODIAC_SIGNS[int(lon // 30) % 12] for planet, lon in varga_longitudes.items()}

    # House lords
    house_lords = {}
    for h in range(1, 13):
        sign_idx = (asc_varga_sign_idx + h - 1) % 12
        sign_name = ZODIAC_SIGNS[sign_idx]
        house_lords[h] = SIGN_LORDS[sign_name]

    # House cusps
    house_cusps = []
    for h in range(1, 13):
        sign_idx = (asc_varga_sign_idx + h - 1) % 12
        sign_name = ZODIAC_SIGNS[sign_idx]
        house_cusps.append(HouseCusp(
            house_number=h,
            sign=sign_name,
            sign_index=sign_idx,
            lord=SIGN_LORDS[sign_name],
            signification=HOUSE_SIGNIFICATORS.get(h, ""),
        ))

    # Planet positions with nakshatra, dignity, retrograde, combust
    planet_positions = {}
    for planet in ALL_PLANETS:
        lon = varga_longitudes.get(planet, 0.0)
        sign_idx = int(lon // 30) % 12
        sign_name = ZODIAC_SIGNS[sign_idx]
        degree = lon % 30.0
        house = planet_house_map.get(planet, 1)

        nak_info = calculate_nakshatra(d1_positions.get(planet, 0.0))
        nakshatra = NakshatraInfo(
            name=nak_info["name"],
            lord=nak_info["lord"],
            deity=nak_info["deity"],
            pada=nak_info["pada"],
            longitude=d1_positions.get(planet, 0.0),
        )

        # Retrograde and speed (use D1 values — retrograde is physical, not chart-dependent)
        swe_id = SWE_PLANET_IDS.get(planet)
        retro = False
        speed = 0.0
        if swe_id is not None:
            retro = is_retrograde(jd, swe_id)
            speed = get_planet_speed(jd, swe_id)

        combust = is_combust(planet, sun_longitude, d1_positions.get(planet, 0.0))
        dignity = get_planet_dignity(planet, lon)

        planet_positions[planet] = PlanetPosition(
            name=planet,
            name_sanskrit=PLANET_NAMES_SANSKRIT.get(planet, planet.capitalize()),
            longitude=lon,
            sign=sign_name,
            sign_index=sign_idx,
            degree=round(degree, 4),
            house=house,
            nakshatra=nakshatra,
            dignity=dignity,
            is_retrograde=retro,
            is_combust=combust,
            speed=round(speed, 4),
        )

    # Strength classification
    planet_strength = {}
    for planet, pp in planet_positions.items():
        d = pp.dignity.lower()
        if any(w in d for w in ["exalted", "own"]):
            planet_strength[planet] = "Strong"
        elif any(w in d for w in ["debilitated"]):
            planet_strength[planet] = "Weak"
        else:
            planet_strength[planet] = "Neutral"

    # Benefic / Malefic
    benefics, malefics = classify_benefic_malefic(d1_positions)

    # Aspects
    aspects = _compute_aspects(planet_house_map)

    # Conjunctions
    conjunctions = _compute_conjunctions(planet_house_map)

    # Exaltations / Debilitations / Retrogrades / Combusts
    exaltations = [p for p, pp in planet_positions.items() if "exalted" in pp.dignity.lower()]
    debilitations = [p for p, pp in planet_positions.items() if "debilitated" in pp.dignity.lower()]
    retrogrades = [p for p, pp in planet_positions.items() if pp.is_retrograde]
    combusts = [p for p, pp in planet_positions.items() if pp.is_combust]

    # Yogas (only meaningful for D1 and D9)
    yogas = []
    if varga_name in ("D1", "D9"):
        # Reuse existing yoga detection
        # Build planet_details compatible format for detect_yogas
        planet_details_compat = {}
        for pname, pp in planet_positions.items():
            planet_details_compat[pname] = {
                "name_sanskrit": pp.name_sanskrit,
                "longitude": pp.longitude,
                "sign": pp.sign,
                "degree": pp.degree,
                "dignity": pp.dignity,
            }
        yogas = detect_yogas(planet_details_compat, planet_house_map)

    return ChartData(
        chart_name=varga_name,
        planet_positions=planet_positions,
        house_cusps=house_cusps,
        house_lords=house_lords,
        planet_house_mapping=planet_house_map,
        planet_sign_mapping=planet_sign_map,
        planet_strength=planet_strength,
        benefic_planets=benefics,
        malefic_planets=malefics,
        aspects=aspects,
        conjunctions=conjunctions,
        exaltations=exaltations,
        debilitations=debilitations,
        retrograde_planets=retrogrades,
        combust_planets=combusts,
        yogas=yogas,
    )


# ===================================================================
# Main entry point
# ===================================================================

def generate_all_charts(birth: BirthDetails) -> FullChartBundle:
    """
    Generate ALL 15 divisional charts and global calculations from
    the user's birth details.

    This is the single entry point for the entire astrology engine.
    Call this once at birth-detail submission time and cache the result.
    """
    # 1. Parse birth details
    dt = datetime.datetime.strptime(birth.date_of_birth, "%Y-%m-%d")
    tm = datetime.datetime.strptime(birth.time_of_birth, "%H:%M:%S")
    birth_date = dt.date()

    # Convert local time to UTC
    local_decimal_hour = tm.hour + tm.minute / 60.0 + tm.second / 3600.0
    utc_decimal_hour = (local_decimal_hour - birth.timezone_offset) % 24.0

    day_shift = int((local_decimal_hour - birth.timezone_offset) // 24.0)
    adjusted_date = birth_date
    if day_shift != 0:
        adjusted_date = birth_date + datetime.timedelta(days=day_shift)

    # 2. Julian Day
    jd = datetime_to_jd(adjusted_date.year, adjusted_date.month, adjusted_date.day, utc_decimal_hour)

    # 3. D1 sidereal positions (source of truth for all vargas)
    d1_positions = get_sidereal_positions(jd)
    sun_lon = d1_positions.get("sun", 0.0)

    # 4. D1 Ascendant and house cusps
    d1_ascendant, _ = get_house_cusps(jd, birth.latitude, birth.longitude)

    # 5. Build all 15 divisional charts
    charts = {}
    for varga in ALL_VARGA_NAMES:
        charts[varga] = _build_chart_data(varga, d1_positions, d1_ascendant, jd, sun_lon)

    # 6. Nakshatra data for all planets
    nakshatra_data = {}
    for planet, lon in d1_positions.items():
        nak = calculate_nakshatra(lon)
        nakshatra_data[planet] = NakshatraInfo(
            name=nak["name"],
            lord=nak["lord"],
            deity=nak["deity"],
            pada=nak["pada"],
            longitude=lon,
        )

    # 7. Vimshottari Dasha (3-level)
    moon_lon = d1_positions.get("moon", 0.0)
    dasha_timeline = calculate_full_vimshottari(moon_lon, birth_date, depth=2)
    today = datetime.date.today()
    dasha_data = get_current_periods(dasha_timeline, today)

    # 8. Gochar (current transits)
    gochar_data = build_gochar_data(d1_positions, d1_ascendant, today)

    # 9. Shadbala
    d1_planet_houses = charts["D1"].planet_house_mapping
    shadbala_list = compute_shadbala(jd, birth.latitude, birth.longitude, d1_positions, d1_planet_houses)

    # 10. Ashtakavarga
    ashtakavarga_data = compute_ashtakavarga(d1_positions, d1_ascendant)

    # 11. Friendships
    natural = compute_natural_friendships()
    temporal = compute_temporal_friendships(d1_planet_houses)
    compound = compute_compound_friendships(natural, temporal)

    from backend.astrology.types import FriendshipData
    friendships = FriendshipData(natural=natural, temporal=temporal, compound=compound)

    # 12. Dignities (D1)
    dignity_map = {p: get_planet_dignity(p, lon) for p, lon in d1_positions.items()}

    # 13. Karakas
    karakas = _compute_karakas(d1_positions)

    # 14. Key sign data
    lagna_sign = ZODIAC_SIGNS[int(d1_ascendant // 30) % 12]
    moon_sign = get_sign_name(d1_positions.get("moon", 0.0))
    sun_sign = get_sign_name(d1_positions.get("sun", 0.0))

    # 15. Assemble FullChartBundle
    bundle = FullChartBundle(
        birth_details=birth,
        D1=charts["D1"],
        D2=charts["D2"],
        D4=charts["D4"],
        D7=charts["D7"],
        D9=charts["D9"],
        D10=charts["D10"],
        D12=charts["D12"],
        D16=charts["D16"],
        D20=charts["D20"],
        D24=charts["D24"],
        D27=charts["D27"],
        D30=charts["D30"],
        D40=charts["D40"],
        D45=charts["D45"],
        D60=charts["D60"],
        dasha=dasha_data,
        gochar=gochar_data,
        nakshatra=nakshatra_data,
        shadbala=shadbala_list,
        ashtakavarga=ashtakavarga_data,
        friendships=friendships,
        dignity=dignity_map,
        lagna=lagna_sign,
        moon_sign=moon_sign,
        sun_sign=sun_sign,
        karakas=karakas,
        generated_at=datetime.datetime.utcnow().isoformat(),
    )

    return bundle
