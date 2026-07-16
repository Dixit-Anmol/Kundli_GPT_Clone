import datetime
from services.astrology.swiss_ephemeris import datetime_to_jd, get_sidereal_positions, get_house_cusps
from services.astrology.planets import get_planet_details
from services.astrology.houses import calculate_planet_houses, get_house_lordships
from services.astrology.nakshatra import get_all_planet_nakshatras
from services.astrology.yogas import detect_yogas
from services.astrology.doshas import check_manglik, check_kaal_sarp, check_sade_sati

def calculate_horoscope_data(
    year: int, month: int, day: int,
    hour: int, minute: int, second: int,
    lat: float, lon: float, timezone_offset: float
) -> dict:
    """Orchestrate the calculation of the full sidereal birth chart and horoscope details (Step 2)."""
    
    # 1. Convert local time to UTC decimal hour
    # Local Time = UTC + Offset -> UTC = Local Time - Offset
    local_decimal_hour = hour + minute / 60.0 + second / 3600.0
    utc_decimal_hour = (local_decimal_hour - timezone_offset) % 24.0
    
    # Handle day shift if timezone boundary is crossed
    day_shift = int((local_decimal_hour - timezone_offset) // 24.0)
    birth_date = datetime.date(year, month, day)
    if day_shift != 0:
        birth_date = birth_date + datetime.timedelta(days=day_shift)
        
    # 2. Calculate Julian Day
    jd = datetime_to_jd(birth_date.year, birth_date.month, birth_date.day, utc_decimal_hour)
    
    # 3. Calculate sidereal positions of all planets
    planet_positions = get_sidereal_positions(jd)
    
    # 4. Calculate Ascendant and House Cusps
    ascendant, house_cusps = get_house_cusps(jd, lat, lon)
    
    # 5. Extract planet properties (Sanskrit name, sign, degree, dignity)
    planet_details = get_planet_details(planet_positions)
    
    # 6. Calculate planet houses (Whole Sign)
    planet_houses = calculate_planet_houses(planet_positions, ascendant)
    
    # 7. Calculate planet nakshatras
    planet_nakshatras = get_all_planet_nakshatras(planet_positions)
    
    # Merge house and nakshatra data into planet details
    for p_name in planet_details.keys():
        planet_details[p_name]["house"] = planet_houses[p_name]
        planet_details[p_name]["nakshatra"] = planet_nakshatras[p_name]
        
    # 8. Calculate house details (lordship, ruling sign, significance)
    house_details = get_house_lordships(ascendant)
    
    # 9. Detect Yogas (combinations)
    yogas = detect_yogas(planet_details, planet_houses)
    
    # 10. Check Doshas (afflictions)
    manglik = check_manglik(planet_houses)
    kaal_sarp = check_kaal_sarp(planet_details)
    
    # Sade Sati - requires current transit of Saturn
    # Use Saturn's coordinate on current date (or fallback J2000.0 / approximate)
    today = datetime.date.today()
    jd_today = datetime_to_jd(today.year, today.month, today.day, 12.0)
    transit_positions = get_sidereal_positions(jd_today)
    saturn_transit = transit_positions.get("saturn", 0.0)
    sade_sati = check_sade_sati(planet_positions["moon"], saturn_transit)
    
    # Combine everything into the structured context block
    chart_context = {
        "metadata": {
            "julian_day": jd,
            "ascendant_longitude": ascendant,
            "ascendant_sign": house_details[1]["sign"],
            "moon_sign": planet_details["moon"]["sign"],
            "nakshatra": planet_details["moon"]["nakshatra"]["name"],
            "pada": planet_details["moon"]["nakshatra"]["pada"],
            "ayanamsa": (planet_positions["sun"] - planet_positions["sun"]) % 360.0 # Placeholder/0 relative
        },
        "planets": planet_details,
        "houses": {str(k): v for k, v in house_details.items()},
        "yogas": yogas,
        "doshas": {
            "manglik": manglik,
            "kaal_sarp": kaal_sarp,
            "sade_sati": sade_sati
        }
    }
    
    return chart_context
