"""
Ayurvedic Prakriti (Constitution) Estimator from Vedic Astrological Indicators.

Maps planetary sign placements, ascendant, and nakshatra elements to Vata/Pitta/Kapha
dosha tendencies. The estimation is astrological — not a clinical diagnosis.
"""

# Sign → Element mapping
SIGN_ELEMENTS = {
    "Aries": "Fire", "Leo": "Fire", "Sagittarius": "Fire",
    "Taurus": "Earth", "Virgo": "Earth", "Capricorn": "Earth",
    "Gemini": "Air", "Libra": "Air", "Aquarius": "Air",
    "Cancer": "Water", "Scorpio": "Water", "Pisces": "Water",
}

# Element → Dosha contribution
ELEMENT_DOSHA = {
    "Fire":  {"vata": 0.1, "pitta": 0.7, "kapha": 0.2},
    "Earth": {"vata": 0.1, "pitta": 0.2, "kapha": 0.7},
    "Air":   {"vata": 0.7, "pitta": 0.2, "kapha": 0.1},
    "Water": {"vata": 0.2, "pitta": 0.3, "kapha": 0.5},
}

# Planet significance weights
PLANET_WEIGHTS = {
    "sun": 2.0,
    "moon": 2.5,
    "mars": 1.5,
    "mercury": 1.2,
    "jupiter": 1.5,
    "venus": 1.2,
    "saturn": 1.5,
    "rahu": 0.8,
    "ketu": 0.8,
}

# Nakshatra → rough dosha tendency (simplified mapping)
NAKSHATRA_DOSHA = {
    "Ashwini": "pitta", "Bharani": "pitta", "Krittika": "pitta",
    "Rohini": "kapha", "Mrigashira": "vata", "Ardra": "vata",
    "Punarvasu": "vata", "Pushya": "kapha", "Ashlesha": "kapha",
    "Magha": "pitta", "Purva Phalguni": "pitta", "Uttara Phalguni": "pitta",
    "Hasta": "vata", "Chitra": "pitta", "Swati": "vata",
    "Vishakha": "pitta", "Anuradha": "kapha", "Jyeshtha": "pitta",
    "Moola": "vata", "Purva Ashadha": "pitta", "Uttara Ashadha": "kapha",
    "Shravana": "kapha", "Dhanishta": "vata", "Shatabhisha": "vata",
    "Purva Bhadrapada": "vata", "Uttara Bhadrapada": "kapha", "Revati": "kapha",
}


def estimate_prakriti(chart_data: dict) -> dict:
    """
    Estimate Ayurvedic Prakriti from birth chart data.
    
    Returns:
        {
            "vata": float (percentage),
            "pitta": float (percentage),
            "kapha": float (percentage),
            "dominant_dosha": str,
            "dominant_element": str,
            "element_distribution": {"Fire": %, "Earth": %, "Air": %, "Water": %},
        }
    """
    meta = chart_data.get("metadata") if isinstance(chart_data.get("metadata"), dict) and chart_data.get("metadata") else chart_data
    planets = chart_data.get("raw_positions") or chart_data.get("planets", {})

    vata_score = 0.0
    pitta_score = 0.0
    kapha_score = 0.0
    total_weight = 0.0

    element_scores = {"Fire": 0.0, "Earth": 0.0, "Air": 0.0, "Water": 0.0}

    # 1. Ascendant sign contribution (weight 3.0)
    asc_sign = meta.get("ascendant_sign") or chart_data.get("ascendant_sign") or "Aries"

    asc_element = SIGN_ELEMENTS.get(asc_sign, "Fire")
    asc_dosha = ELEMENT_DOSHA.get(asc_element, ELEMENT_DOSHA["Fire"])
    asc_weight = 3.0
    vata_score += asc_dosha["vata"] * asc_weight
    pitta_score += asc_dosha["pitta"] * asc_weight
    kapha_score += asc_dosha["kapha"] * asc_weight
    element_scores[asc_element] += asc_weight
    total_weight += asc_weight
    
    # 2. Planetary sign contributions (weighted by planet significance)
    for p_name, p_data in planets.items():
        sign = p_data.get("sign", "Aries")
        element = SIGN_ELEMENTS.get(sign, "Fire")
        dosha = ELEMENT_DOSHA.get(element, ELEMENT_DOSHA["Fire"])
        weight = PLANET_WEIGHTS.get(p_name.lower(), 1.0)
        
        # Lagna lord gets extra weight
        if p_name.lower() == _get_lagna_lord(asc_sign):
            weight *= 1.5
        
        vata_score += dosha["vata"] * weight
        pitta_score += dosha["pitta"] * weight
        kapha_score += dosha["kapha"] * weight
        element_scores[element] += weight
        total_weight += weight
    
    # 3. Moon nakshatra contribution (weight 1.5)
    moon_nak = meta.get("nakshatra") or chart_data.get("nakshatra") or ""

    nak_dosha = NAKSHATRA_DOSHA.get(moon_nak, "vata")
    nak_weight = 1.5
    if nak_dosha == "vata":
        vata_score += nak_weight
    elif nak_dosha == "pitta":
        pitta_score += nak_weight
    else:
        kapha_score += nak_weight
    total_weight += nak_weight
    
    # Normalize to percentages
    dosha_total = vata_score + pitta_score + kapha_score
    if dosha_total == 0:
        dosha_total = 1.0
    
    vata_pct = round((vata_score / dosha_total) * 100, 1)
    pitta_pct = round((pitta_score / dosha_total) * 100, 1)
    kapha_pct = round(100 - vata_pct - pitta_pct, 1)  # Ensure sums to 100
    
    # Dominant dosha
    doshas = {"Vata": vata_pct, "Pitta": pitta_pct, "Kapha": kapha_pct}
    dominant_dosha = max(doshas, key=doshas.get)
    
    # Element distribution
    elem_total = sum(element_scores.values()) or 1.0
    element_dist = {k: round((v / elem_total) * 100, 1) for k, v in element_scores.items()}
    dominant_element = max(element_dist, key=element_dist.get)
    
    return {
        "vata": vata_pct,
        "pitta": pitta_pct,
        "kapha": kapha_pct,
        "dominant_dosha": dominant_dosha,
        "dominant_element": dominant_element,
        "element_distribution": element_dist,
    }


def _get_lagna_lord(sign: str) -> str:
    """Return the ruling planet name for a zodiac sign."""
    lords = {
        "Aries": "mars", "Taurus": "venus", "Gemini": "mercury",
        "Cancer": "moon", "Leo": "sun", "Virgo": "mercury",
        "Libra": "venus", "Scorpio": "mars", "Sagittarius": "jupiter",
        "Capricorn": "saturn", "Aquarius": "saturn", "Pisces": "jupiter",
    }
    return lords.get(sign, "sun")
