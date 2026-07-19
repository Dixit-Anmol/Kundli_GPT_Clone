"""
Lucky Attributes Calculator.

Derives lucky colors, numbers, day, and direction from the Lagna lord,
Moon sign ruler, and dominant planetary influences.
"""

PLANET_COLORS = {
    "sun": ["Gold", "Orange", "Saffron"],
    "moon": ["White", "Silver", "Pearl"],
    "mars": ["Red", "Coral", "Scarlet"],
    "mercury": ["Green", "Emerald"],
    "jupiter": ["Yellow", "Turmeric", "Golden"],
    "venus": ["White", "Cream", "Pastel Pink"],
    "saturn": ["Black", "Dark Blue", "Navy"],
    "rahu": ["Smoke Grey", "Hessonite Brown"],
    "ketu": ["Grey", "Earthy Brown"],
}

PLANET_NUMBERS = {
    "sun": [1, 10, 19],
    "moon": [2, 11, 20],
    "mars": [9, 18, 27],
    "mercury": [5, 14, 23],
    "jupiter": [3, 12, 21],
    "venus": [6, 15, 24],
    "saturn": [8, 17, 26],
    "rahu": [4, 13, 22],
    "ketu": [7, 16, 25],
}

PLANET_DAYS = {
    "sun": "Sunday",
    "moon": "Monday",
    "mars": "Tuesday",
    "mercury": "Wednesday",
    "jupiter": "Thursday",
    "venus": "Friday",
    "saturn": "Saturday",
    "rahu": "Saturday",
    "ketu": "Tuesday",
}

PLANET_DIRECTIONS = {
    "sun": "East",
    "moon": "North-West",
    "mars": "South",
    "mercury": "North",
    "jupiter": "North-East",
    "venus": "South-East",
    "saturn": "West",
    "rahu": "South-West",
    "ketu": "North-West",
}

SIGN_LORDS = {
    "Aries": "mars", "Taurus": "venus", "Gemini": "mercury",
    "Cancer": "moon", "Leo": "sun", "Virgo": "mercury",
    "Libra": "venus", "Scorpio": "mars", "Sagittarius": "jupiter",
    "Capricorn": "saturn", "Aquarius": "saturn", "Pisces": "jupiter",
}


def calculate_lucky_attributes(chart_data: dict) -> dict:
    """
    Calculate lucky colors, numbers, day, and direction from birth chart.
    
    Returns:
        {
            "lucky_colors": [str],
            "lucky_numbers": [int],
            "lucky_day": str,
            "lucky_direction": str,
        }
    """
    meta = chart_data.get("metadata", {})
    
    asc_sign = meta.get("ascendant_sign", "Aries")
    moon_sign = meta.get("moon_sign", "Cancer")
    
    lagna_lord = SIGN_LORDS.get(asc_sign, "sun")
    moon_lord = SIGN_LORDS.get(moon_sign, "moon")
    
    # Lucky colors: primary from lagna lord, secondary from moon lord
    colors = list(PLANET_COLORS.get(lagna_lord, ["Gold"]))
    moon_colors = PLANET_COLORS.get(moon_lord, [])
    for c in moon_colors:
        if c not in colors:
            colors.append(c)
    
    # Lucky numbers: from lagna lord
    numbers = list(PLANET_NUMBERS.get(lagna_lord, [1]))
    
    # Lucky day: from lagna lord
    day = PLANET_DAYS.get(lagna_lord, "Sunday")
    
    # Lucky direction: from lagna lord
    direction = PLANET_DIRECTIONS.get(lagna_lord, "East")
    
    return {
        "lucky_colors": colors[:4],
        "lucky_numbers": numbers,
        "lucky_day": day,
        "lucky_direction": direction,
    }
