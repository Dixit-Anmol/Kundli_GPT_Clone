def detect_yogas(planet_details: dict, planet_houses: dict) -> list:
    """Detect prominent Vedic Yogas (planetary combinations) present in the birth chart."""
    active_yogas = []
    
    # 1. Gajakesari Yoga
    # Jupiter in a quadrant (1, 4, 7, 10) from the Moon.
    moon_house = planet_houses.get("moon", 1)
    jupiter_house = planet_houses.get("jupiter", 1)
    relative_house = ((jupiter_house - moon_house) % 12) + 1
    if relative_house in [1, 4, 7, 10]:
        active_yogas.append({
            "name": "Gaja Kesari Yoga",
            "meaning": "Jupiter in a quadrant from the Moon. Brings intelligence, wisdom, prosperity, reputation, and virtuous qualities.",
            "type": "Auspicious"
        })
        
    # 2. Budhaditya Yoga
    # Sun and Mercury in the same sign (conjunction)
    sun_sign = planet_details.get("sun", {}).get("sign")
    mercury_sign = planet_details.get("mercury", {}).get("sign")
    if sun_sign and mercury_sign and sun_sign == mercury_sign:
        active_yogas.append({
            "name": "Budhaditya Yoga",
            "meaning": "Sun and Mercury conjunction. Gives intelligence, learning ability, professional success, and mental agility.",
            "type": "Intellectual"
        })
        
    # 3. Chandra Mangala Yoga
    # Moon and Mars conjunct (same sign)
    moon_sign = planet_details.get("moon", {}).get("sign")
    mars_sign = planet_details.get("mars", {}).get("sign")
    if moon_sign and mars_sign and moon_sign == mars_sign:
        active_yogas.append({
            "name": "Chandra Mangala Yoga",
            "meaning": "Conjunction of Moon and Mars. Promotes earnings through self-efforts, real estate gains, and emotional vigor.",
            "type": "Wealth"
        })
        
    # 4. Pancha Mahapurusha Yogas
    # Non-luminary planet (Mars, Mercury, Jupiter, Venus, Saturn) in its exaltation/own sign, and placed in a Kendra (1st, 4th, 7th, 10th house).
    kendras = [1, 4, 7, 10]
    mahapurusha_yogas = {
        "mars": ("Ruchaka Yoga", "Strength, energy, leadership, courage, wealth through land or metals."),
        "mercury": ("Bhadra Yoga", "High intellect, excellent communication, logical capacity, long life."),
        "jupiter": ("Hamsa Yoga", "Wisdom, spiritual alignment, high virtues, happiness, respected in society."),
        "venus": ("Malavya Yoga", "Luxury, beauty, fine arts, family happiness, magnetic personality."),
        "saturn": ("Sasa Yoga", "Commanding power, authority, loyalty, long-lasting assets, hard-working mindset.")
    }
    
    for planet, (yoga_name, yoga_meaning) in mahapurusha_yogas.items():
        details = planet_details.get(planet, {})
        dignity = details.get("dignity", "")
        house = planet_houses.get(planet, 1)
        
        if (dignity in ["Exalted", "Exalted Sign", "Own Sign"]) and (house in kendras):
            active_yogas.append({
                "name": yoga_name,
                "meaning": f"{planet.capitalize()} is strong in a Kendra house. {yoga_meaning}",
                "type": "Mahapurusha"
            })
            
    return active_yogas
