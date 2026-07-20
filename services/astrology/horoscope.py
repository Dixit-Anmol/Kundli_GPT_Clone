import datetime
from services.astrology.swiss_ephemeris import datetime_to_jd, get_sidereal_positions, get_house_cusps, get_lahiri_ayanamsa
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
    """Orchestrate the calculation of the full sidereal birth chart and horoscope details."""
    
    # 1. Convert local datetime to UTC using timedelta
    local_dt = datetime.datetime(year, month, day, hour, minute, second)
    utc_dt = local_dt - datetime.timedelta(hours=timezone_offset)
    
    utc_decimal_hour = utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0 + utc_dt.microsecond / 3600000000.0
    
    # 2. Calculate Julian Day Number
    jd = datetime_to_jd(utc_dt.year, utc_dt.month, utc_dt.day, utc_decimal_hour)
    ayanamsa = get_lahiri_ayanamsa(jd)
    
    # 3. Calculate sidereal positions of all planets
    planet_positions = get_sidereal_positions(jd)
    
    # 4. Calculate true Sidereal Ascendant and House Cusps
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
            "ayanamsa": ayanamsa
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
