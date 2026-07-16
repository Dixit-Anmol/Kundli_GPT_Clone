NAKSHATRAS = [
    {"name": "Ashwini", "lord": "ketu", "deity": "Ashwini Kumaras"},
    {"name": "Bharani", "lord": "venus", "deity": "Yama"},
    {"name": "Krittika", "lord": "sun", "deity": "Agni"},
    {"name": "Rohini", "lord": "moon", "deity": "Brahma"},
    {"name": "Mrigashira", "lord": "mars", "deity": "Soma"},
    {"name": "Ardra", "lord": "rahu", "deity": "Rudra"},
    {"name": "Punarvasu", "lord": "jupiter", "deity": "Aditi"},
    {"name": "Pushya", "lord": "saturn", "deity": "Brihaspati"},
    {"name": "Ashlesha", "lord": "mercury", "deity": "Sarpas"},
    {"name": "Magha", "lord": "ketu", "deity": "Pitris"},
    {"name": "Purva Phalguni", "lord": "venus", "deity": "Bhaga"},
    {"name": "Uttara Phalguni", "lord": "sun", "deity": "Aryaman"},
    {"name": "Hasta", "lord": "moon", "deity": "Savitr"},
    {"name": "Chitra", "lord": "mars", "deity": "Vishwakarma"},
    {"name": "Swati", "lord": "rahu", "deity": "Vayu"},
    {"name": "Vishakha", "lord": "jupiter", "deity": "Indra-Agni"},
    {"name": "Anuradha", "lord": "saturn", "deity": "Mitra"},
    {"name": "Jyeshtha", "lord": "mercury", "deity": "Indra"},
    {"name": "Mula", "lord": "ketu", "deity": "Nirriti"},
    {"name": "Purva Ashadha", "lord": "venus", "deity": "Apah"},
    {"name": "Uttara Ashadha", "lord": "sun", "deity": "Vishvadevas"},
    {"name": "Shravana", "lord": "moon", "deity": "Vishnu"},
    {"name": "Dhanishta", "lord": "mars", "deity": "Vasus"},
    {"name": "Shatabhisha", "lord": "rahu", "deity": "Varuna"},
    {"name": "Purva Bhadrapada", "lord": "jupiter", "deity": "Aja Ekapada"},
    {"name": "Uttara Bhadrapada", "lord": "saturn", "deity": "Ahirbudhnya"},
    {"name": "Revati", "lord": "mercury", "deity": "Pushan"}
]

def calculate_nakshatra(longitude: float) -> dict:
    """Find Nakshatra name, ruling lord, deity, and pada (1-4) for a given sidereal longitude."""
    # Each nakshatra is exactly 13.333333 degrees wide (13 deg 20 min)
    nak_width = 360.0 / 27.0
    nak_idx = int(longitude // nak_width)
    
    # Remainder longitude within the current nakshatra
    rem_long = longitude % nak_width
    # Each pada is exactly 3.333333 degrees wide (3 deg 20 min)
    pada_width = nak_width / 4.0
    pada = int(rem_long // pada_width) + 1
    
    nak = NAKSHATRAS[nak_idx]
    
    return {
        "name": nak["name"],
        "lord": nak["lord"],
        "deity": nak["deity"],
        "pada": pada,
        "longitude": longitude
    }

def get_all_planet_nakshatras(planet_positions: dict) -> dict:
    results = {}
    for planet, long in planet_positions.items():
        results[planet] = calculate_nakshatra(long)
    return results
