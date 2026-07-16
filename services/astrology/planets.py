# Vedic Astrology Planets Database & Placement Rules
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

PLANET_NAMES_SANSKRIT = {
    "sun": "Surya",
    "moon": "Chandra",
    "mars": "Mangal",
    "mercury": "Budh",
    "jupiter": "Guru",
    "venus": "Shukra",
    "saturn": "Shani",
    "rahu": "Rahu",
    "ketu": "Ketu"
}

SIGN_LORDS = {
    "Aries": "mars",
    "Taurus": "venus",
    "Gemini": "mercury",
    "Cancer": "moon",
    "Leo": "sun",
    "Virgo": "mercury",
    "Libra": "venus",
    "Scorpio": "mars",
    "Sagittarius": "jupiter",
    "Capricorn": "saturn",
    "Aquarius": "saturn",
    "Pisces": "jupiter"
}

EXALTATION_DEBILITATION = {
    # Planet: [Exaltation Sign, Exaltation Degree, Debilitation Sign, Debilitation Degree]
    "sun": ["Aries", 10.0, "Libra", 10.0],
    "moon": ["Taurus", 3.0, "Scorpio", 3.0],
    "mars": ["Capricorn", 28.0, "Cancer", 28.0],
    "mercury": ["Virgo", 15.0, "Pisces", 15.0],
    "jupiter": ["Cancer", 5.0, "Capricorn", 5.0],
    "venus": ["Pisces", 27.0, "Virgo", 27.0],
    "saturn": ["Libra", 20.0, "Aries", 20.0]
}

def get_sign_name(longitude: float) -> str:
    idx = int(longitude // 30)
    return ZODIAC_SIGNS[idx]

def get_planet_dignity(planet: str, longitude: float) -> str:
    """Determine if a planet is Exalted, Debilitated, or in Own Sign, Friend's Sign, Neutral, or Enemy."""
    if planet not in EXALTATION_DEBILITATION:
        return "Neutral"
        
    sign = get_sign_name(longitude)
    deg = longitude % 30.0
    
    ex_sign, ex_deg, de_sign, de_deg = EXALTATION_DEBILITATION[planet]
    
    if sign == ex_sign:
        # Close enough to exact degree is highly exalted, otherwise exalted sign
        return "Exalted" if abs(deg - ex_deg) < 5.0 else "Exalted Sign"
    if sign == de_sign:
        return "Debilitated" if abs(deg - de_deg) < 5.0 else "Debilitated Sign"
        
    # Check Own Sign
    if SIGN_LORDS[sign] == planet:
        return "Own Sign"
        
    return "Neutral"

def get_planet_details(positions: dict) -> dict:
    details = {}
    for name, long in positions.items():
        sign_idx = int(long // 30)
        sign_name = ZODIAC_SIGNS[sign_idx]
        deg = long % 30.0
        
        details[name] = {
            "name_sanskrit": PLANET_NAMES_SANSKRIT.get(name, name.capitalize()),
            "longitude": long,
            "sign": sign_name,
            "degree": deg,
            "dignity": get_planet_dignity(name, long)
        }
    return details
