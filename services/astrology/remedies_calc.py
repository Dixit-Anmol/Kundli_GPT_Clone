"""
Remedy Data Generator.

Identifies weak/afflicted planets and generates structured remedy data:
mantras, gemstones, charity, fasting days, color therapy, deity suggestions.
"""

PLANET_MANTRAS = {
    "sun": {"beej": "Om Hraam Hreem Hraum Sah Suryaya Namaha", "vedic": "Om Adityaya Vidmahe Divakaraya Dhimahi Tanno Suryah Prachodayat", "count": 7000},
    "moon": {"beej": "Om Shraam Shreem Shraum Sah Chandraya Namaha", "vedic": "Om Kshirputraya Vidmahe Amrittatvaya Dhimahi Tanno Chandrah Prachodayat", "count": 11000},
    "mars": {"beej": "Om Kraam Kreem Kraum Sah Bhaumaya Namaha", "vedic": "Om Angarakaya Vidmahe Bhoomiputraya Dhimahi Tanno Kujah Prachodayat", "count": 10000},
    "mercury": {"beej": "Om Braam Breem Braum Sah Budhaya Namaha", "vedic": "Om Budhaya Vidmahe Priyangu Kalikanaya Dhimahi Tanno Budhah Prachodayat", "count": 9000},
    "jupiter": {"beej": "Om Graam Greem Graum Sah Gurave Namaha", "vedic": "Om Brihaspataye Vidmahe Surashreshthaya Dhimahi Tanno Guruh Prachodayat", "count": 19000},
    "venus": {"beej": "Om Draam Dreem Draum Sah Shukraya Namaha", "vedic": "Om Rajadabikaraya Vidmahe Brigusuthaya Dhimahi Tanno Shukrah Prachodayat", "count": 16000},
    "saturn": {"beej": "Om Praam Preem Praum Sah Shanaischaraya Namaha", "vedic": "Om Shanaischaraya Vidmahe Shanaidevaya Dhimahi Tanno Mandah Prachodayat", "count": 23000},
    "rahu": {"beej": "Om Bhraam Bhreem Bhraum Sah Rahave Namaha", "vedic": "Om Sookdantaya Vidmahe Ugraroopaya Dhimahi Tanno Rahuh Prachodayat", "count": 18000},
    "ketu": {"beej": "Om Sraam Sreem Sraum Sah Ketave Namaha", "vedic": "Om Chitravarnaya Vidmahe Sarparoopaya Dhimahi Tanno Ketuh Prachodayat", "count": 17000},
}

PLANET_GEMSTONES = {
    "sun": {"primary": "Ruby (Manik)", "alternative": "Garnet, Spinel", "metal": "Gold", "finger": "Ring finger", "day": "Sunday"},
    "moon": {"primary": "Pearl (Moti)", "alternative": "Moonstone", "metal": "Silver", "finger": "Little finger", "day": "Monday"},
    "mars": {"primary": "Red Coral (Moonga)", "alternative": "Carnelian", "metal": "Gold/Copper", "finger": "Ring finger", "day": "Tuesday"},
    "mercury": {"primary": "Emerald (Panna)", "alternative": "Green Tourmaline, Peridot", "metal": "Gold", "finger": "Little finger", "day": "Wednesday"},
    "jupiter": {"primary": "Yellow Sapphire (Pukhraj)", "alternative": "Citrine, Yellow Topaz", "metal": "Gold", "finger": "Index finger", "day": "Thursday"},
    "venus": {"primary": "Diamond (Heera)", "alternative": "White Sapphire, Zircon", "metal": "Platinum/Silver", "finger": "Middle finger", "day": "Friday"},
    "saturn": {"primary": "Blue Sapphire (Neelam)", "alternative": "Amethyst, Blue Spinel", "metal": "Silver/Iron", "finger": "Middle finger", "day": "Saturday"},
    "rahu": {"primary": "Hessonite (Gomed)", "alternative": "Zircon", "metal": "Silver", "finger": "Middle finger", "day": "Saturday"},
    "ketu": {"primary": "Cat's Eye (Lehsunia)", "alternative": "Tiger's Eye", "metal": "Silver", "finger": "Little finger", "day": "Tuesday"},
}

PLANET_CHARITY = {
    "sun": {"items": ["Wheat", "Jaggery (Gur)", "Red flowers"], "day": "Sunday", "recipient": "Father figures, elderly"},
    "moon": {"items": ["Rice", "White cloth", "Milk", "Silver"], "day": "Monday", "recipient": "Mothers, women"},
    "mars": {"items": ["Red lentils (Masoor dal)", "Red cloth", "Copper"], "day": "Tuesday", "recipient": "Soldiers, brothers"},
    "mercury": {"items": ["Green moong dal", "Green cloth", "Books"], "day": "Wednesday", "recipient": "Students, scholars"},
    "jupiter": {"items": ["Yellow cloth", "Turmeric", "Chana dal", "Bananas"], "day": "Thursday", "recipient": "Teachers, Brahmins, elderly"},
    "venus": {"items": ["White rice", "Ghee", "White clothes", "Perfume"], "day": "Friday", "recipient": "Women, artists"},
    "saturn": {"items": ["Black sesame (Til)", "Mustard oil", "Iron", "Black cloth"], "day": "Saturday", "recipient": "Workers, elderly, disabled"},
    "rahu": {"items": ["Coconut", "Blue/black cloth", "Electrical items"], "day": "Saturday", "recipient": "Sweepers, outcasts"},
    "ketu": {"items": ["Blanket", "Dog food", "Sesame seeds"], "day": "Tuesday", "recipient": "Dogs, spiritual seekers"},
}

PLANET_FASTING = {
    "sun": "Sunday", "moon": "Monday", "mars": "Tuesday",
    "mercury": "Wednesday", "jupiter": "Thursday", "venus": "Friday",
    "saturn": "Saturday", "rahu": "Saturday", "ketu": "Tuesday",
}

PLANET_COLORS = {
    "sun": "Orange, Saffron, Gold",
    "moon": "White, Silver",
    "mars": "Red, Coral",
    "mercury": "Green",
    "jupiter": "Yellow, Gold",
    "venus": "White, Cream, Light Pink",
    "saturn": "Black, Dark Blue, Navy",
    "rahu": "Smoke Grey",
    "ketu": "Grey, Brown",
}

PLANET_DEITIES = {
    "sun": {"deity": "Lord Surya", "temple": "Surya temple / Konark", "practice": "Surya Namaskar at sunrise"},
    "moon": {"deity": "Lord Shiva / Chandra", "temple": "Somnath / Shiva temples", "practice": "Chandra Darshan on Purnima"},
    "mars": {"deity": "Lord Hanuman / Kartikeya", "temple": "Hanuman temple", "practice": "Hanuman Chalisa on Tuesdays"},
    "mercury": {"deity": "Lord Vishnu / Budh", "temple": "Vishnu temple", "practice": "Vishnu Sahasranamam"},
    "jupiter": {"deity": "Lord Brihaspati / Dakshinamurthy", "temple": "Brihaspati temple", "practice": "Guru Vandana on Thursdays"},
    "venus": {"deity": "Goddess Lakshmi / Shukra", "temple": "Lakshmi temple", "practice": "Lakshmi puja on Fridays"},
    "saturn": {"deity": "Lord Shani Dev", "temple": "Shani temple / Shingnapur", "practice": "Shani Stotra on Saturdays"},
    "rahu": {"deity": "Goddess Durga", "temple": "Durga temple", "practice": "Durga mantra, Rahu Kaal awareness"},
    "ketu": {"deity": "Lord Ganesha", "temple": "Ganesha temple", "practice": "Ganesha puja, silent meditation"},
}

DUSTHANA_HOUSES = {6, 8, 12}


def generate_remedy_data(chart_data: dict, planet_rankings: list = None) -> dict:
    """
    Identify weak/afflicted planets and generate structured remedy data.
    
    Returns:
        {
            "weak_planets": [{"planet": str, "status": str, "remedies": {...}}],
            "afflicted_houses": [...],
            "general_remedies": [...]
        }
    """
    planets = chart_data.get("raw_positions") or chart_data.get("planets") or {}

    doshas = chart_data.get("doshas", {})
    
    # Identify weak planets from rankings (if provided) or from dignity
    weak_planets = []
    
    if planet_rankings:
        for r in planet_rankings:
            if r["status"] in ("Weak", "Very Weak"):
                p_name = r["planet"]
                weak_planets.append({
                    "planet": p_name,
                    "display_name": r.get("display_name", p_name.capitalize()),
                    "status": r["status"],
                    "score": r["score"],
                    "reasons": r.get("reasons", []),
                    "remedies": _build_remedies(p_name),
                })
    else:
        # Fallback: check dignity directly
        for p_name, p_data in planets.items():
            dignity = (p_data.get("dignity") or "").lower()
            is_weak = any(w in dignity for w in ["debilitated", "enemy"])
            is_combust = p_data.get("combust", False)
            house = p_data.get("house")
            in_dusthana = house and int(house) in DUSTHANA_HOUSES
            
            if is_weak or is_combust or in_dusthana:
                status = "Debilitated" if "debilitated" in dignity else "Afflicted"
                weak_planets.append({
                    "planet": p_name,
                    "display_name": p_data.get("name_sanskrit", p_name.capitalize()),
                    "status": status,
                    "score": None,
                    "reasons": [
                        f"{'Debilitated' if is_weak else 'Neutral'} dignity",
                        f"{'Combust' if is_combust else 'Non-combust'}",
                        f"House {house}" + (" (Dusthana)" if in_dusthana else ""),
                    ],
                    "remedies": _build_remedies(p_name),
                })
    
    # Identify afflicted houses
    afflicted = []
    for p_name, p_data in planets.items():
        house = p_data.get("house")
        if house and int(house) in DUSTHANA_HOUSES:
            afflicted.append({
                "house": int(house),
                "occupant": p_name.capitalize(),
                "sign": p_data.get("sign", "?"),
            })
    
    # General remedies based on doshas
    general = []
    if doshas.get("manglik", {}).get("is_present"):
        general.append({
            "dosha": "Manglik Dosha",
            "remedy": "Perform Kumbh Vivah before marriage. Recite Hanuman Chalisa daily. Offer red flowers at Hanuman temple on Tuesdays.",
        })
    if doshas.get("kaal_sarp", {}).get("is_present"):
        general.append({
            "dosha": "Kaal Sarp Dosha",
            "remedy": "Perform Kaal Sarp Dosh Nivaran Puja at Trimbakeshwar. Offer milk to Shiva Lingam on Mondays. Keep a silver snake idol at home.",
        })
    if doshas.get("sade_sati", {}).get("is_present"):
        general.append({
            "dosha": "Sade Sati (Saturn Transit)",
            "remedy": "Recite Shani Stotra or Hanuman Chalisa on Saturdays. Donate black sesame and mustard oil. Wear dark blue or black on Saturdays.",
        })
    
    return {
        "weak_planets": weak_planets,
        "afflicted_houses": afflicted,
        "general_remedies": general,
    }


def _build_remedies(planet_name: str) -> dict:
    """Build the full remedy kit for a single planet."""
    p = planet_name.lower()
    return {
        "mantra": PLANET_MANTRAS.get(p, {}),
        "gemstone": PLANET_GEMSTONES.get(p, {}),
        "charity": PLANET_CHARITY.get(p, {}),
        "fasting_day": PLANET_FASTING.get(p, ""),
        "colors": PLANET_COLORS.get(p, ""),
        "deity": PLANET_DEITIES.get(p, {}),
    }
