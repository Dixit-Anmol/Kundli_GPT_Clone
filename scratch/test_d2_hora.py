def calculate_d2_hora(planets: dict, ascendant_degree: float = 0.0) -> dict:
    """
    Calculate D2 Hora divisional chart placements for financial analysis.
    Odd Signs (Aries, Gemini, Leo, Libra, Sagittarius, Aquarius):
        0-15 deg = Sun Hora (Leo)
        15-30 deg = Moon Hora (Cancer)
    Even Signs (Taurus, Cancer, Virgo, Scorpio, Capricorn, Pisces):
        0-15 deg = Moon Hora (Cancer)
        15-30 deg = Sun Hora (Leo)
    """
    sign_names = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                  "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    
    sun_hora_planets = []
    moon_hora_planets = []
    hora_details = {}

    for p_name, p in planets.items():
        deg = float(p.get("degree", 0.0))
        sign_str = p.get("sign", "Aries")
        
        # If degree is 0-30 relative to sign vs 0-360 absolute
        sign_idx = sign_names.index(sign_str) if sign_str in sign_names else 0
        deg_in_sign = deg % 30.0 if deg > 30 else deg
        
        # Odd sign (1st, 3rd, 5th sign i.e. 0, 2, 4, 6, 8, 10 index)
        is_odd = (sign_idx % 2 == 0)
        
        if is_odd:
            hora = "Sun Hora (Leo)" if deg_in_sign < 15.0 else "Moon Hora (Cancer)"
        else:
            hora = "Moon Hora (Cancer)" if deg_in_sign < 15.0 else "Sun Hora (Leo)"
            
        hora_details[p_name] = hora
        if "Sun" in hora:
            sun_hora_planets.append(p_name.capitalize())
        else:
            moon_hora_planets.append(p_name.capitalize())

    return {
        "sun_hora_planets": sun_hora_planets,
        "moon_hora_planets": moon_hora_planets,
        "hora_details": hora_details,
        "dominant_hora": "Sun Hora (Active Earning & Enterprise)" if len(sun_hora_planets) > len(moon_hora_planets) else "Moon Hora (Accumulated Savings & Assets)"
    }

# Quick test with sample planets
sample_planets = {
    "sun": {"sign": "Scorpio", "degree": 23.18},
    "moon": {"sign": "Leo", "degree": 25.34},
    "jupiter": {"sign": "Cancer", "degree": 12.50},
    "venus": {"sign": "Libra", "degree": 18.20},
    "mars": {"sign": "Taurus", "degree": 5.10},
    "saturn": {"sign": "Capricorn", "degree": 14.80},
    "mercury": {"sign": "Scorpio", "degree": 10.30},
}
print(calculate_d2_hora(sample_planets))
