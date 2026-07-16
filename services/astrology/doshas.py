def check_manglik(planet_houses: dict) -> dict:
    """Check if Manglik Dosha (Mars placement) is present in the chart."""
    # Classic Manglik houses: 1, 2, 4, 7, 8, 12
    mars_house = planet_houses.get("mars", 1)
    is_manglik = mars_house in [1, 2, 4, 7, 8, 12]
    
    meanings = {
        1: "Mars in 1st house can lead to hot-headedness and conflict in partnerships.",
        2: "Mars in 2nd house can cause harsh speech and friction in family life.",
        4: "Mars in 4th house affects domestic peace and can cause domestic disputes.",
        7: "Mars in 7th house directly impacts marriage, causing relationship friction.",
        8: "Mars in 8th house can lead to issues with in-laws or sudden health changes.",
        12: "Mars in 12th house can cause sleep disturbances or excessive expenditures."
    }
    
    return {
        "is_present": is_manglik,
        "house": mars_house,
        "description": meanings.get(mars_house, "Mars is not in any of the critical Manglik houses.") if is_manglik else "No Manglik Dosha found."
    }

def check_kaal_sarp(planet_details: dict) -> dict:
    """Check if Kaal Sarp Dosha (all traditional planets hemmed between Rahu and Ketu) is present."""
    # Find longitudes of Rahu and Ketu
    rahu_long = planet_details.get("rahu", {}).get("longitude", 0.0)
    ketu_long = planet_details.get("ketu", {}).get("longitude", 0.0)
    
    # Standardize Rahu as lower bound (or upper bound depending on axis)
    min_axis = min(rahu_long, ketu_long)
    max_axis = max(rahu_long, ketu_long)
    
    traditional_planets = ["sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn"]
    
    # Check if all traditional planets are inside [min_axis, max_axis]
    inside_count = 0
    outside_count = 0
    for planet in traditional_planets:
        long = planet_details.get(planet, {}).get("longitude", 0.0)
        if min_axis <= long <= max_axis:
            inside_count += 1
        else:
            outside_count += 1
            
    # Hemmed on either side of the Rahu-Ketu axis
    is_kaal_sarp = (inside_count == 7) or (outside_count == 7)
    
    return {
        "is_present": is_kaal_sarp,
        "description": "All planets are hemmed between the Rahu-Ketu axis, indicating Kaal Sarp Dosha, which can bring struggle and sudden changes." if is_kaal_sarp else "No Kaal Sarp Dosha found."
    }

def check_sade_sati(moon_long: float, transiting_saturn_long: float) -> dict:
    """Check if Sade Sati (Saturn transit over natal Moon) is active."""
    # Sade Sati occurs when transiting Saturn is in:
    # 1. The sign before natal Moon (12th from Moon)
    # 2. The sign of natal Moon (1st from Moon)
    # 3. The sign after natal Moon (2nd from Moon)
    moon_sign_idx = int(moon_long // 30)
    saturn_sign_idx = int(transiting_saturn_long // 30)
    
    diff = (saturn_sign_idx - moon_sign_idx) % 12
    # Adjust for negative values or distance: 12th from Moon is 11, 2nd from Moon is 1
    is_active = diff in [11, 0, 1]
    
    phase = "Not Active"
    description = "Sade Sati is not active for this Moon sign right now."
    
    if is_active:
        if diff == 11:
            phase = "First Phase (12th from Moon)"
            description = "Saturn is in the sign before your natal Moon. Focus on managing expenses and mental peace."
        elif diff == 0:
            phase = "Second Phase / Peak (Conjunction)"
            description = "Saturn is transiting directly over your natal Moon sign. Peak impact: demands patience, discipline, and hard work."
        elif diff == 1:
            phase = "Third Phase (2nd from Moon)"
            description = "Saturn is in the sign after your natal Moon. Focus on domestic stability, speech, and financial consolidation."
            
    return {
        "is_present": is_active,
        "phase": phase,
        "description": description
    }
