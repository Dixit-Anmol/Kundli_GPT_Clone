"""
Planetary Strength computations for Vedic Astrology.

Implements:
- Shadbala (6-fold strength: Sthana, Dig, Kala, Chesta, Naisargika, Drik)
- Ashtakavarga (Bindu contribution tables)
- Planetary friendships (Natural + Temporal → Compound)
- Combustion detection
- Retrograde detection
"""

import swisseph as swe

from services.astrology.planets import (
    ZODIAC_SIGNS, SIGN_LORDS, EXALTATION_DEBILITATION, get_sign_name
)


# ---------------------------------------------------------------------------
# Natural Friendship Table (Parashari)
# ---------------------------------------------------------------------------
# "friend", "neutral", "enemy"
NATURAL_FRIENDS = {
    "sun":     {"friend": ["moon", "mars", "jupiter"],      "enemy": ["venus", "saturn"],               "neutral": ["mercury"]},
    "moon":    {"friend": ["sun", "mercury"],                "enemy": [],                                 "neutral": ["mars", "jupiter", "venus", "saturn"]},
    "mars":    {"friend": ["sun", "moon", "jupiter"],        "enemy": ["mercury"],                        "neutral": ["venus", "saturn"]},
    "mercury": {"friend": ["sun", "venus"],                  "enemy": ["moon"],                           "neutral": ["mars", "jupiter", "saturn"]},
    "jupiter": {"friend": ["sun", "moon", "mars"],           "enemy": ["mercury", "venus"],               "neutral": ["saturn"]},
    "venus":   {"friend": ["mercury", "saturn"],             "enemy": ["sun", "moon"],                    "neutral": ["mars", "jupiter"]},
    "saturn":  {"friend": ["mercury", "venus"],              "enemy": ["sun", "moon", "mars"],            "neutral": ["jupiter"]},
    "rahu":    {"friend": ["mercury", "venus", "saturn"],    "enemy": ["sun", "moon", "mars"],            "neutral": ["jupiter"]},
    "ketu":    {"friend": ["mars", "jupiter"],               "enemy": ["mercury", "venus"],               "neutral": ["sun", "moon", "saturn"]},
}


# ---------------------------------------------------------------------------
# Combustion orbs (in degrees from Sun)
# ---------------------------------------------------------------------------
COMBUSTION_ORBS = {
    "moon": 12.0,
    "mars": 17.0,
    "mercury": 14.0,    # 12° when retrograde, but we simplify to 14°
    "jupiter": 11.0,
    "venus": 10.0,      # 8° when retrograde
    "saturn": 15.0,
}


# ---------------------------------------------------------------------------
# Naisargika Bala (innate natural strength, fixed values in Shashtiamsas)
# ---------------------------------------------------------------------------
NAISARGIKA_BALA = {
    "sun": 60.0,
    "moon": 51.43,
    "mars": 17.14,
    "mercury": 25.71,
    "jupiter": 34.29,
    "venus": 42.86,
    "saturn": 8.57,
}


# ---------------------------------------------------------------------------
# Dig Bala ideal houses (where each planet gets directional strength)
# ---------------------------------------------------------------------------
DIG_BALA_HOUSES = {
    "sun": 10,      # 10th house
    "moon": 4,      # 4th house
    "mars": 10,     # 10th house
    "mercury": 1,   # 1st house
    "jupiter": 1,   # 1st house
    "venus": 4,     # 4th house
    "saturn": 7,    # 7th house
}


# ---------------------------------------------------------------------------
# Ashtakavarga contribution table (simplified Parashari rules)
# Key: contributing_planet → list of houses from its own position where it
# gives a bindu (benefic point) to the target planet's Ashtakavarga.
# ---------------------------------------------------------------------------
ASHTAKAVARGA_TABLE = {
    "sun": {
        "sun":     [1, 2, 4, 7, 8, 9, 10, 11],
        "moon":    [3, 6, 10, 11],
        "mars":    [1, 2, 4, 7, 8, 9, 10, 11],
        "mercury": [3, 5, 6, 9, 10, 11, 12],
        "jupiter": [5, 6, 9, 11],
        "venus":   [6, 7, 12],
        "saturn":  [1, 2, 4, 7, 8, 9, 10, 11],
        "asc":     [3, 4, 6, 10, 11, 12],
    },
    "moon": {
        "sun":     [3, 6, 7, 8, 10, 11],
        "moon":    [1, 3, 6, 7, 10, 11],
        "mars":    [2, 3, 5, 6, 9, 10, 11],
        "mercury": [1, 3, 4, 5, 7, 8, 10, 11],
        "jupiter": [1, 4, 7, 8, 10, 11, 12],
        "venus":   [3, 4, 5, 7, 9, 10, 11],
        "saturn":  [3, 5, 6, 11],
        "asc":     [3, 6, 10, 11],
    },
    "mars": {
        "sun":     [3, 5, 6, 10, 11],
        "moon":    [3, 6, 11],
        "mars":    [1, 2, 4, 7, 8, 10, 11],
        "mercury": [3, 5, 6, 11],
        "jupiter": [6, 10, 11, 12],
        "venus":   [6, 8, 11, 12],
        "saturn":  [1, 4, 7, 8, 9, 10, 11],
        "asc":     [1, 3, 6, 10, 11],
    },
    "mercury": {
        "sun":     [5, 6, 9, 11, 12],
        "moon":    [2, 4, 6, 8, 10, 11],
        "mars":    [1, 2, 4, 7, 8, 9, 10, 11],
        "mercury": [1, 3, 5, 6, 9, 10, 11, 12],
        "jupiter": [6, 8, 11, 12],
        "venus":   [1, 2, 3, 4, 5, 8, 9, 11],
        "saturn":  [1, 2, 4, 7, 8, 9, 10, 11],
        "asc":     [1, 2, 4, 6, 8, 10, 11],
    },
    "jupiter": {
        "sun":     [1, 2, 3, 4, 7, 8, 9, 10, 11],
        "moon":    [2, 5, 7, 9, 11],
        "mars":    [1, 2, 4, 7, 8, 10, 11],
        "mercury": [1, 2, 4, 5, 6, 9, 10, 11],
        "jupiter": [1, 2, 3, 4, 7, 8, 10, 11],
        "venus":   [2, 5, 6, 9, 10, 11],
        "saturn":  [3, 5, 6, 12],
        "asc":     [1, 2, 4, 5, 6, 7, 9, 10, 11],
    },
    "venus": {
        "sun":     [8, 11, 12],
        "moon":    [1, 2, 3, 4, 5, 8, 9, 11, 12],
        "mars":    [3, 4, 6, 8, 9, 11, 12],
        "mercury": [3, 5, 6, 9, 11],
        "jupiter": [5, 8, 9, 10, 11],
        "venus":   [1, 2, 3, 4, 5, 8, 9, 10, 11],
        "saturn":  [3, 4, 5, 8, 9, 10, 11],
        "asc":     [1, 2, 3, 4, 5, 8, 9, 11],
    },
    "saturn": {
        "sun":     [1, 2, 4, 7, 8, 9, 10, 11],
        "moon":    [3, 6, 11],
        "mars":    [3, 5, 6, 10, 11, 12],
        "mercury": [6, 8, 9, 10, 11, 12],
        "jupiter": [5, 6, 11, 12],
        "venus":   [6, 11, 12],
        "saturn":  [3, 5, 6, 11],
        "asc":     [1, 3, 4, 6, 10, 11],
    },
}

SEVEN_PLANETS = ["sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn"]


# ===================================================================
# Combustion
# ===================================================================

def is_combust(planet: str, sun_longitude: float, planet_longitude: float) -> bool:
    """Check if a planet is combust (too close to the Sun)."""
    if planet in ("sun", "rahu", "ketu"):
        return False

    orb = COMBUSTION_ORBS.get(planet, 15.0)
    diff = abs(planet_longitude - sun_longitude)
    if diff > 180:
        diff = 360 - diff
    return diff <= orb


# ===================================================================
# Retrograde
# ===================================================================

def is_retrograde(jd: float, swe_planet_id: int) -> bool:
    """Check if a planet is retrograde at the given Julian Day (negative speed)."""
    # FLG_SPEED is included by default; index 3 of result is daily speed
    res = swe.calc_ut(jd, swe_planet_id, swe.FLG_SIDEREAL | swe.FLG_SPEED)
    return res[0][3] < 0


def get_planet_speed(jd: float, swe_planet_id: int) -> float:
    """Get the daily speed in longitude for a planet."""
    res = swe.calc_ut(jd, swe_planet_id, swe.FLG_SIDEREAL | swe.FLG_SPEED)
    return res[0][3]


# Map planet names to Swiss Ephemeris IDs
SWE_PLANET_IDS = {
    "sun": swe.SUN,
    "moon": swe.MOON,
    "mars": swe.MARS,
    "mercury": swe.MERCURY,
    "jupiter": swe.JUPITER,
    "venus": swe.VENUS,
    "saturn": swe.SATURN,
    "rahu": swe.TRUE_NODE,
}


# ===================================================================
# Natural Friendships
# ===================================================================

def compute_natural_friendships() -> dict:
    """Return the full natural friendship matrix."""
    result = {}
    for planet in SEVEN_PLANETS + ["rahu", "ketu"]:
        data = NATURAL_FRIENDS.get(planet, {})
        friends_map = {}
        for friend in data.get("friend", []):
            friends_map[friend] = "friend"
        for enemy in data.get("enemy", []):
            friends_map[enemy] = "enemy"
        for neutral in data.get("neutral", []):
            friends_map[neutral] = "neutral"
        result[planet] = friends_map
    return result


# ===================================================================
# Temporal Friendships
# ===================================================================

def compute_temporal_friendships(planet_houses: dict) -> dict:
    """
    Two planets are temporal friends if they are in houses 2, 3, 4, 10, 11, 12
    from each other (i.e. within 5 houses on either side).
    """
    planets = list(planet_houses.keys())
    result = {}
    for p1 in planets:
        result[p1] = {}
        h1 = planet_houses[p1]
        for p2 in planets:
            if p1 == p2:
                continue
            h2 = planet_houses[p2]
            diff = ((h2 - h1) % 12) + 1  # 1-indexed difference
            if diff in [2, 3, 4, 10, 11, 12]:
                result[p1][p2] = "friend"
            else:
                result[p1][p2] = "enemy"
    return result


# ===================================================================
# Compound Friendships (Natural + Temporal)
# ===================================================================

def compute_compound_friendships(natural: dict, temporal: dict) -> dict:
    """
    Combine natural and temporal friendships:
    friend + friend = best_friend
    friend + enemy = neutral
    enemy + friend = neutral
    enemy + enemy = bitter_enemy
    neutral + friend = friend
    neutral + enemy = enemy
    """
    combine_table = {
        ("friend", "friend"): "best_friend",
        ("friend", "enemy"): "neutral",
        ("enemy", "friend"): "neutral",
        ("enemy", "enemy"): "bitter_enemy",
        ("neutral", "friend"): "friend",
        ("neutral", "enemy"): "enemy",
        ("friend", "neutral"): "friend",
        ("enemy", "neutral"): "enemy",
        ("neutral", "neutral"): "neutral",
    }

    result = {}
    for p1 in natural:
        result[p1] = {}
        for p2 in natural.get(p1, {}):
            nat = natural.get(p1, {}).get(p2, "neutral")
            temp = temporal.get(p1, {}).get(p2, "neutral")
            result[p1][p2] = combine_table.get((nat, temp), "neutral")
    return result


# ===================================================================
# Shadbala (simplified)
# ===================================================================

def compute_shadbala(
    jd: float,
    lat: float,
    lon: float,
    positions: dict,
    planet_houses: dict,
) -> list:
    """
    Compute a simplified Shadbala for the 7 traditional planets.

    Returns a list of dicts with planet name and 6 bala components + total.
    """
    from backend.astrology.types import ShadbalaEntry

    results = []
    for planet in SEVEN_PLANETS:
        pos = positions.get(planet, 0.0)
        house = planet_houses.get(planet, 1)

        # 1. Sthana Bala (positional) — based on dignity
        sign = get_sign_name(pos)
        exalt_data = EXALTATION_DEBILITATION.get(planet)
        sthana = 30.0  # default neutral
        if exalt_data:
            if sign == exalt_data[0]:
                sthana = 60.0
            elif sign == exalt_data[2]:
                sthana = 5.0
            elif SIGN_LORDS.get(sign) == planet:
                sthana = 50.0

        # 2. Dig Bala (directional) — max when in ideal house
        ideal_house = DIG_BALA_HOUSES.get(planet, 1)
        house_diff = abs(house - ideal_house)
        if house_diff > 6:
            house_diff = 12 - house_diff
        dig = max(0.0, 60.0 - (house_diff * 10.0))

        # 3. Kala Bala (temporal) — day/night born affects luminaries
        # Simplified: Sun strong by day, Moon by night, others moderate
        kala = 30.0
        if planet == "sun":
            kala = 45.0
        elif planet == "moon":
            kala = 45.0

        # 4. Chesta Bala (motional) — retrograde planets get higher chesta
        swe_id = SWE_PLANET_IDS.get(planet)
        chesta = 30.0
        if swe_id and planet not in ("sun", "moon"):
            speed = get_planet_speed(jd, swe_id)
            if speed < 0:   # retrograde
                chesta = 60.0
            elif speed > 1.0:
                chesta = 15.0

        # 5. Naisargika Bala (natural, fixed)
        naisargika = NAISARGIKA_BALA.get(planet, 30.0)

        # 6. Drik Bala (aspectual) — simplified: benefic aspects add, malefic subtract
        drik = 30.0

        total = sthana + dig + kala + chesta + naisargika + drik

        results.append(ShadbalaEntry(
            planet=planet,
            sthana_bala=round(sthana, 2),
            dig_bala=round(dig, 2),
            kala_bala=round(kala, 2),
            chesta_bala=round(chesta, 2),
            naisargika_bala=round(naisargika, 2),
            drik_bala=round(drik, 2),
            total=round(total, 2),
        ))

    return results


# ===================================================================
# Ashtakavarga
# ===================================================================

def compute_ashtakavarga(positions: dict, ascendant: float) -> dict:
    """
    Compute Ashtakavarga bindu scores for each planet.

    Returns:
        {
            "planet_entries": [{planet, bindu_per_house, total_bindu}, ...],
            "sarvashtakavarga": [sum_h1, sum_h2, ..., sum_h12]
        }
    """
    from backend.astrology.types import AshtakavargaEntry, AshtakavargaData

    asc_sign_idx = int(ascendant // 30)

    # House index (0-based) for each planet relative to Ascendant
    def planet_house_0(planet_name):
        if planet_name == "asc":
            return 0
        lon = positions.get(planet_name, 0.0)
        sign_idx = int(lon // 30)
        return (sign_idx - asc_sign_idx) % 12

    entries = []
    sarva = [0] * 12

    for target_planet in SEVEN_PLANETS:
        bindu = [0] * 12
        table = ASHTAKAVARGA_TABLE.get(target_planet, {})

        for contributor in list(SEVEN_PLANETS) + ["asc"]:
            contrib_house = planet_house_0(contributor)
            houses_giving_bindu = table.get(contributor, [])

            for h_offset in houses_giving_bindu:
                benefited_house = (contrib_house + h_offset - 1) % 12
                bindu[benefited_house] += 1

        total = sum(bindu)
        entries.append(AshtakavargaEntry(
            planet=target_planet,
            bindu_per_house=bindu,
            total_bindu=total,
        ))
        for i in range(12):
            sarva[i] += bindu[i]

    return AshtakavargaData(planet_entries=entries, sarvashtakavarga=sarva)


# ===================================================================
# Benefic / Malefic classification
# ===================================================================

# Natural benefics and malefics
NATURAL_BENEFICS = {"jupiter", "venus", "mercury", "moon"}
NATURAL_MALEFICS = {"sun", "mars", "saturn", "rahu", "ketu"}

def classify_benefic_malefic(positions: dict) -> tuple:
    """
    Classify planets into benefic and malefic lists.
    Mercury is benefic unless conjunct a malefic.
    Moon is benefic when waxing (longitude > Sun's longitude in a 180° range).
    """
    sun_lon = positions.get("sun", 0.0)
    moon_lon = positions.get("moon", 0.0)

    # Moon phase: waxing if Moon is 0-180° ahead of Sun
    moon_sun_diff = (moon_lon - sun_lon) % 360
    moon_benefic = moon_sun_diff <= 180

    benefics = ["jupiter", "venus"]
    malefics = ["mars", "saturn", "rahu", "ketu", "sun"]

    if moon_benefic:
        benefics.append("moon")
    else:
        malefics.append("moon")

    # Mercury: check if conjunct (same sign) with any malefic
    merc_sign = int(positions.get("mercury", 0.0) // 30)
    merc_with_malefic = any(
        int(positions.get(m, 0.0) // 30) == merc_sign
        for m in ["mars", "saturn", "rahu", "ketu"]
    )
    if merc_with_malefic:
        malefics.append("mercury")
    else:
        benefics.append("mercury")

    return benefics, malefics
