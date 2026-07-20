"""
Partial Horoscope Engine — Approximate Astrology for Partial Birth Details.
Strictly calculates planetary positions and Moon sign without fabricating Lagna or Houses.
"""

import datetime
from services.astrology.swiss_ephemeris import datetime_to_jd, get_sidereal_positions, get_lahiri_ayanamsa
from services.astrology.planets import get_planet_details, ZODIAC_SIGNS

from services.astrology.nakshatra import calculate_nakshatra

APPROX_TIME_SLOTS = {

    "morning": "08:00:00",
    "afternoon": "13:00:00",
    "evening": "18:00:00",
    "night": "22:00:00",
    "sunrise": "06:00:00",
    "sunset": "18:30:00",
    "unknown": "12:00:00",
}

def calculate_partial_horoscope(
    year: int,
    month: int,
    day: int,
    time_slot: str = "unknown",
    exact_time: str = None,
    lat: float = 28.6139,
    lon: float = 77.2090,
    timezone_offset: float = 5.5
) -> dict:
    """
    Computes an Estimated Horoscope based on partial birth details.
    STRICTLY excludes Lagna, Houses, D9, D10, D24, and Dasha calculations when birth time is missing.
    """
    # 1. Resolve time
    if exact_time and exact_time.strip():
        t_str = exact_time.strip()
        has_exact_time = True
    else:
        t_str = APPROX_TIME_SLOTS.get(time_slot.lower(), "12:00:00")
        has_exact_time = False

    try:
        hour, minute, second = [int(x) for x in t_str.split(":")]
    except Exception:
        hour, minute, second = 12, 0, 0

    local_dt = datetime.datetime(year, month, day, hour, minute, second)
    utc_dt = local_dt - datetime.timedelta(hours=timezone_offset)
    utc_decimal_hour = utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0

    jd = datetime_to_jd(utc_dt.year, utc_dt.month, utc_dt.day, utc_decimal_hour)
    planet_positions = get_sidereal_positions(jd)
    planet_details = get_planet_details(planet_positions)

    # 2. Moon sign stability check across 24-hour day
    # Moon moves ~13 degrees per day. Check 00:00 vs 23:59 on the same date.
    jd_start = datetime_to_jd(year, month, day, 0.0)
    jd_end = datetime_to_jd(year, month, day, 23.99)
    moon_start = get_sidereal_positions(jd_start).get("moon", 0.0)
    moon_end = get_sidereal_positions(jd_end).get("moon", 0.0)

    start_sign = ZODIAC_SIGNS[int(moon_start // 30)]
    end_sign = ZODIAC_SIGNS[int(moon_end // 30)]

    moon_is_stable = (start_sign == end_sign)

    moon_deg = planet_positions.get("moon", 0.0)
    nak_info = calculate_nakshatra(moon_deg)
    nak_name = nak_info.get("name", "Pushya")
    nak_pada = nak_info.get("pada", 1)
    nak_lord = nak_info.get("lord", "saturn")


    # Determine confidence level
    if has_exact_time:
        confidence = "High"
    elif moon_is_stable and time_slot.lower() != "unknown":
        confidence = "Medium"
    else:
        confidence = "Low"

    # Current Transits (Gochar for today)
    today = datetime.date.today()
    jd_today = datetime_to_jd(today.year, today.month, today.day, 12.0)
    transits = get_planet_details(get_sidereal_positions(jd_today))

    return {
        "mode": "partial",
        "chart_type": "Estimated Horoscope",
        "confidence_level": confidence,
        "birth_date": f"{year:04d}-{month:02d}-{day:02d}",
        "time_slot": time_slot,
        "has_exact_time": has_exact_time,
        "moon_sign": start_sign if moon_is_stable else f"{start_sign} or {end_sign}",
        "moon_stable": moon_is_stable,
        "nakshatra": nak_name if confidence != "Low" else f"{nak_name} (Approximate)",
        "planets": planet_details,
        "transits": transits,
        "raw_positions": planet_positions,
        "exact_calculations": ["Planetary Positions (Sun, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu)", "Current Transits"],
        "estimated_calculations": ["Moon Sign (Approximate)" if not moon_is_stable else "Moon Sign"],
        "excluded_calculations": ["Lagna / Ascendant", "12 House Cusps", "D9 Navamsha", "D10 Dashamsha", "D24 Siddhamsha", "Vimshottari Dasha"],
        "disclaimer": "This analysis is based on approximate planetary positions. Providing your exact birth time later will unlock a complete Janma Kundli with Lagna and House Cusps."
    }


def format_partial_horoscope_context(analysis: dict, profile: dict = None) -> str:
    """Formats Estimated Horoscope data into LLM prompt context."""
    name = profile.get("name", "Seeker") if profile else "Seeker"
    planets = analysis.get("planets", {})

    planet_lines = []
    for p_name, p_data in planets.items():
        planet_lines.append(
            f"- {p_name.capitalize()}: Sign {p_data.get('sign')} ({p_data.get('degree')}°) | Dignity: {p_data.get('dignity')}"
        )

    return f"""[ESTIMATED HOROSCOPE DATA (PARTIAL BIRTH DETAILS)]
Subject: {name}
Query Mode: ESTIMATED NATAL ANALYSIS
Confidence Level: {analysis.get('confidence_level')}
Birth Date: {analysis.get('birth_date')} (Approximate Time Slot: {analysis.get('time_slot')})
Moon Sign: {analysis.get('moon_sign')}
Nakshatra: {analysis.get('nakshatra')}

[EXACT PLANETARY POSITIONS]
{chr(10).join(planet_lines)}

[CALCULATION TRANSPARENCY]
- Exact Calculations: {', '.join(analysis.get('exact_calculations', []))}
- Estimated Calculations: {', '.join(analysis.get('estimated_calculations', []))}
- STRICTLY EXCLUDED: {', '.join(analysis.get('excluded_calculations', []))}

[IMPORTANT RULES FOR AI]
1. Clearly state this is an ESTIMATED HOROSCOPE generated from partial birth details.
2. NEVER fabricate or invent Lagna, House numbers, D9, D10, or Dasha predictions.
3. Focus on Moon Sign, planetary sign dignities, and transit influences."""
