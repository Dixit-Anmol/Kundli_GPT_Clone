"""
Element Distribution Calculator.

Calculates the distribution of Fire, Earth, Air, Water, and Ether elements
from planetary sign placements in the birth chart.
"""

SIGN_ELEMENTS = {
    "Aries": "Fire", "Leo": "Fire", "Sagittarius": "Fire",
    "Taurus": "Earth", "Virgo": "Earth", "Capricorn": "Earth",
    "Gemini": "Air", "Libra": "Air", "Aquarius": "Air",
    "Cancer": "Water", "Scorpio": "Water", "Pisces": "Water",
}

# Planet weights for element calculation
PLANET_WEIGHTS = {
    "sun": 2.0, "moon": 2.5, "mars": 1.5, "mercury": 1.2,
    "jupiter": 1.5, "venus": 1.2, "saturn": 1.5, "rahu": 0.8, "ketu": 0.8,
}


def calculate_element_distribution(chart_data: dict) -> dict:
    """
    Calculate element distribution from planetary placements.
    
    Returns:
        {
            "Fire": float (%),
            "Earth": float (%),
            "Air": float (%),
            "Water": float (%),
            "Ether": float (%),
            "dominant": str,
        }
    """
    meta = chart_data.get("metadata", {})
    planets = chart_data.get("planets", {})
    
    scores = {"Fire": 0.0, "Earth": 0.0, "Air": 0.0, "Water": 0.0, "Ether": 0.0}
    
    # Ascendant contribution
    asc_sign = meta.get("ascendant_sign", "Aries")
    asc_elem = SIGN_ELEMENTS.get(asc_sign, "Fire")
    scores[asc_elem] += 3.0
    
    # Planetary contributions
    for p_name, p_data in planets.items():
        sign = p_data.get("sign", "Aries")
        elem = SIGN_ELEMENTS.get(sign, "Fire")
        weight = PLANET_WEIGHTS.get(p_name.lower(), 1.0)
        scores[elem] += weight
        
    # Ether is derived as a balance indicator — spiritual planets (Jupiter, Ketu) contribute
    jupiter_data = planets.get("jupiter", {})
    ketu_data = planets.get("ketu", {})
    if jupiter_data.get("house") in [5, 9, 12]:
        scores["Ether"] += 1.5
    if ketu_data.get("house") in [5, 9, 12]:
        scores["Ether"] += 1.0
    
    # Normalize
    total = sum(scores.values()) or 1.0
    distribution = {k: round((v / total) * 100, 1) for k, v in scores.items()}
    dominant = max(distribution, key=distribution.get)
    
    return {**distribution, "dominant": dominant}
