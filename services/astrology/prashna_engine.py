"""
Prashna Engine — Horary Astrology Engine for Unknown Birth Details.
Calculates Prashna Kundli based on the exact moment and location of the query.
"""

import datetime
from services.astrology.swiss_ephemeris import (
    datetime_to_jd, get_sidereal_positions, get_house_cusps, get_lahiri_ayanamsa
)
from services.astrology.planets import get_planet_details, ZODIAC_SIGNS, SIGN_LORDS

from services.astrology.nakshatra import calculate_nakshatra

NAKSHATRA_NAMES = [

    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

TITHE_NAMES = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shasthi",
    "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dwadashi",
    "Trayodashi", "Chaturdashi", "Purnima", "Amavasya"
]

PLANET_ORDER_HORA = ["sun", "venus", "mercury", "moon", "saturn", "jupiter", "mars"]

def get_hora(dt: datetime.datetime) -> str:
    """Calculates the ruling planet (Hora lord) of the current hour."""
    weekday_index = dt.weekday() # 0 = Monday, 6 = Sunday
    # Sunday lord = Sun (0), Monday lord = Moon (3), Tuesday = Mars (6), Wednesday = Mercury (2), Thursday = Jupiter (5), Friday = Venus (1), Saturday = Saturn (4)
    weekday_hora_starts = {0: 3, 1: 6, 2: 2, 3: 5, 4: 1, 5: 4, 6: 0} # map weekday to PLANET_ORDER_HORA index
    start_lord_idx = weekday_hora_starts[weekday_index]
    hour_of_day = dt.hour
    hora_idx = (start_lord_idx + hour_of_day) % 7
    return PLANET_ORDER_HORA[hora_idx].capitalize()


def calculate_prashna_chart(
    question: str,
    category: str,
    lat: float,
    lon: float,
    timezone_offset: float = 5.5,
    dt: datetime.datetime = None
) -> dict:
    """
    Computes a dedicated Prashna (Horary) Kundli for the user's question at the current moment and place.
    """
    if dt is None:
        dt = datetime.datetime.now()

    # Convert to UTC
    utc_dt = dt - datetime.timedelta(hours=timezone_offset)
    utc_decimal_hour = utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0
    jd = datetime_to_jd(utc_dt.year, utc_dt.month, utc_dt.day, utc_decimal_hour)
    ayanamsa = get_lahiri_ayanamsa(jd)

    # Sidereal planet positions & Prashna Lagna
    planet_positions = get_sidereal_positions(jd)
    ascendant, house_cusps = get_house_cusps(jd, lat, lon)

    # Ascendant sign & degree
    asc_sign_index = int(ascendant // 30)
    asc_sign_name = ZODIAC_SIGNS[asc_sign_index]

    asc_degree = ascendant % 30
    asc_lord = SIGN_LORDS.get(asc_sign_name.lower(), "Jupiter")

    # Planet details
    planet_details = get_planet_details(planet_positions)

    # Calculate Prashna Whole-Sign houses relative to Prashna Lagna
    for p_name, p_data in planet_details.items():
        p_deg = p_data.get("degree", 0.0)
        p_sign_index = int(p_deg // 30)
        house_num = ((p_sign_index - asc_sign_index) % 12) + 1
        p_data["house"] = house_num

    # Moon data & Panchanga
    moon_deg = planet_positions.get("moon", 0.0)
    sun_deg = planet_positions.get("sun", 0.0)

    # Tithi: (Moon - Sun) / 12 degrees
    diff = (moon_deg - sun_deg) % 360
    tithi_index = int(diff // 12)
    tithi_name = TITHE_NAMES[tithi_index % 16]

    # Moon Nakshatra
    nak_info = calculate_nakshatra(moon_deg)
    nak_name = nak_info.get("name", "Pushya")
    nak_pada = nak_info.get("pada", 1)
    nak_lord = nak_info.get("lord", "saturn")


    # Yoga: (Sun + Moon) / 13°20'
    yoga_num = int(((sun_deg + moon_deg) % 360) // (13.333333)) + 1

    # Hora
    hora_lord = get_hora(dt)

    return {
        "mode": "prashna",
        "chart_type": "Prashna Horoscope (Horary)",
        "question": question,
        "category": category,
        "location": {"latitude": lat, "longitude": lon},
        "prashna_time": dt.strftime("%Y-%m-%d %H:%M:%S"),
        "prashna_lagna": {
            "sign": asc_sign_name,
            "degree": round(asc_degree, 2),
            "lord": asc_lord.capitalize()
        },
        "panchanga": {
            "tithi": tithi_name,
            "nakshatra": nak_name,
            "pada": nak_pada,
            "nakshatra_lord": nak_lord.capitalize(),
            "hora": hora_lord,
            "yoga_index": yoga_num
        },
        "planets": planet_details,
        "raw_positions": planet_positions,
        "disclaimer": "This guidance uses Prashna Astrology (Horary) based on the exact time and location of your question. Providing your exact birth details later will unlock a complete Janma Kundli."
    }


def format_prashna_context(analysis: dict, profile: dict = None) -> str:
    """Formats Prashna Kundli data into LLM prompt context."""
    name = profile.get("name", "Seeker") if profile else "Seeker"
    question = analysis.get("question", "General Guidance")
    cat = analysis.get("category", "General")
    lagna = analysis.get("prashna_lagna", {})
    panch = analysis.get("panchanga", {})
    planets = analysis.get("planets", {})

    planet_lines = []
    for p_name, p_data in planets.items():
        planet_lines.append(
            f"- {p_name.capitalize()}: Sign {p_data.get('sign')} | House {p_data.get('house')} | Dignity: {p_data.get('dignity')}"
        )

    return f"""[PRASHNA KUNDLI HORARY DATA (QUESTION-BASED GUIDANCE)]
Subject: {name}
Query Mode: PRASHNA HOROSCOPE (No Birth Details Available)
Question Category: {cat.upper()}
User Question: "{question}"
Prashna Moment: {analysis.get('prashna_time')}

[PRASHNA LAGNA & ASCENDANT]
- Prashna Lagna Sign: {lagna.get('sign')} ({lagna.get('degree')}°)
- Prashna Lagna Lord: {lagna.get('lord')}

[PANCHANGA OF THE MOMENT]
- Hora Lord: {panch.get('hora')}
- Nakshatra: {panch.get('nakshatra')} (Pada {panch.get('pada')}, Lord: {panch.get('nakshatra_lord')})
- Tithi: {panch.get('tithi')}

[PLANETARY PLACEMENTS IN PRASHNA CHART]
{chr(10).join(planet_lines)}

[IMPORTANT PRASHNA RULES FOR AI]
1. Clearly state this is a PRASHNA HOROSCOPE generated for the exact moment of the user's question.
2. Focus directly on answering the user's specific question using Prashna Lagna ({lagna.get('sign')}) and Moon alignment.
3. NEVER claim this is their natal birth chart."""
