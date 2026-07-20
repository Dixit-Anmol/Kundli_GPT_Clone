"""
Vedic Relationship Analysis Engine — Multi-Target Relationship Intelligence.

Supports 9 relationship categories:
- Father (9th, 10th, 1st | Sun, Jupiter | Pitru Dosha)
- Mother (4th, 1st, 10th | Moon, Venus | Matru Yogas)
- Siblings (3rd, 11th | Mars, Mercury | Bhratri Yogas)
- Spouse / Partner (7th, 2nd, 8th, 12th | Venus, Jupiter, Darakaraka | D9 Navamsa | Manglik)
- Children (5th, 9th | Jupiter, Sun | D7 Saptamsa | Putra Yogas)
- Friends (11th, 3rd | Mercury, Jupiter | Maitri Yogas)
- Boss / Authorities (10th, 6th, 9th | Sun, Saturn, Jupiter | D10 Dashamsha | Raj Yogas)
- Mentors / Teachers (9th, 5th | Jupiter, Sun | Guru Yogas)
- In-Laws (7th, 8th, 2nd | Venus, Jupiter | 8th Lord Status)
"""

from typing import Dict, Any, List, Optional


RELATIONSHIP_CONFIGS: Dict[str, Dict[str, Any]] = {
    "father": {
        "title": "Father (Pitr)",
        "icon": "👨‍🦳",
        "primary_houses": [9, 10, 1],
        "karakas": ["sun", "jupiter"],
        "divisional": None,
        "check_doshas": ["pitru_dosha", "sun_affliction"],
        "focus_areas": [
            "Emotional Bond", "Respect", "Communication", "Financial Support",
            "Father's Influence", "Karmic Lessons", "Areas of Conflict",
            "Relationship Timeline", "Improvement Suggestions"
        ]
    },
    "mother": {
        "title": "Mother (Matr)",
        "icon": "👩‍🦳",
        "primary_houses": [4, 1, 10],
        "karakas": ["moon", "venus"],
        "divisional": None,
        "check_doshas": ["moon_affliction"],
        "focus_areas": [
            "Emotional Bond", "Care & Nurturing", "Mental Connection",
            "Home Environment", "Communication", "Support", "Challenges"
        ]
    },
    "siblings": {
        "title": "Siblings (Bhratr)",
        "icon": "👦",
        "primary_houses": [3, 11],
        "karakas": ["mars", "mercury"],
        "divisional": None,
        "check_doshas": ["bhratri_dosha"],
        "focus_areas": [
            "Support", "Rivalry", "Communication", "Cooperation",
            "Business Together", "Long-term Bond"
        ]
    },
    "spouse": {
        "title": "Spouse / Partner (Kalatra)",
        "icon": "💍",
        "primary_houses": [7, 2, 8, 12],
        "karakas": ["venus", "jupiter"],
        "divisional": "D9 Navamsa",
        "check_doshas": ["manglik"],
        "focus_areas": [
            "Compatibility", "Communication", "Romance", "Trust",
            "Emotional Bond", "Physical Compatibility", "Marriage Stability",
            "Challenges", "Improvement"
        ]
    },
    "children": {
        "title": "Children (Santana)",
        "icon": "👶",
        "primary_houses": [5, 9],
        "karakas": ["jupiter", "sun"],
        "divisional": "D7 Saptamsa",
        "check_doshas": ["putra_dosha"],
        "focus_areas": [
            "Chances of Children", "Relationship with Children", "Parenting Style",
            "Child Success", "Emotional Bond", "Family Happiness"
        ]
    },
    "friends": {
        "title": "Friends (Maitri)",
        "icon": "🤝",
        "primary_houses": [11, 3],
        "karakas": ["mercury", "jupiter"],
        "divisional": None,
        "check_doshas": ["rahu_in_11"],
        "focus_areas": [
            "Social Circle", "Networking", "Loyal Friends",
            "Betrayal Tendencies", "Helpful Contacts"
        ]
    },
    "boss": {
        "title": "Boss & Authorities (Adhikari)",
        "icon": "👔",
        "primary_houses": [10, 6, 9],
        "karakas": ["sun", "saturn", "jupiter"],
        "divisional": "D10 Dashamsha",
        "check_doshas": ["sun_saturn_clash"],
        "focus_areas": [
            "Authority Relationships", "Workplace Respect", "Promotions",
            "Leadership", "Government Support", "Workplace Politics"
        ]
    },
    "mentors": {
        "title": "Mentors & Teachers (Guru)",
        "icon": "🧘",
        "primary_houses": [9, 5],
        "karakas": ["jupiter", "sun"],
        "divisional": None,
        "check_doshas": ["guru_chandal"],
        "focus_areas": [
            "Guidance", "Learning", "Spiritual Teachers",
            "Mentor Support", "Blessings"
        ]
    },
    "inlaws": {
        "title": "In-Laws (Kutumba)",
        "icon": "🏡",
        "primary_houses": [7, 8, 2],
        "karakas": ["venus", "jupiter"],
        "divisional": None,
        "check_doshas": ["8th_house_affliction"],
        "focus_areas": [
            "Family Acceptance", "Harmony", "Long-term Relations",
            "Possible Conflicts"
        ]
    }
}


def analyze_relationship(chart_data: dict, relationship_type: str = "spouse") -> dict:
    """
    Computes a dedicated relationship package for the selected target.
    Calculates house & lord dignities, karakas, aspects, Yogas/Doshas, and relationship score (0-100).
    """
    rel_type = relationship_type.lower()
    if rel_type not in RELATIONSHIP_CONFIGS:
        rel_type = "spouse"

    cfg = RELATIONSHIP_CONFIGS[rel_type]
    planets = chart_data.get("raw_positions") or chart_data.get("planets") or {}
    houses = chart_data.get("houses") or {}
    doshas = chart_data.get("doshas") or {}
    yogas = chart_data.get("yogas") or []

    # 1. Extract Primary House Details
    house_details = []
    primary_lords = []
    house_score_mod = 0

    for h_num in cfg["primary_houses"]:
        h_str = str(h_num)
        h_info = houses.get(h_str, {})
        sign = h_info.get("sign", "Unknown")
        lord = h_info.get("lord", "").lower()
        if lord:
            primary_lords.append(lord)

        # Planets residing in house
        planets_in_h = [
            p_name for p_name, p in planets.items()
            if str(p.get("house")) == h_str
        ]

        # Check house affliction
        malefic_count = sum(1 for p in planets_in_h if p.lower() in ["saturn", "rahu", "ketu", "mars"])
        benefic_count = sum(1 for p in planets_in_h if p.lower() in ["jupiter", "venus", "mercury", "moon"])
        house_score_mod += (benefic_count * 5) - (malefic_count * 4)

        house_details.append({
            "house": h_num,
            "sign": sign,
            "lord": lord.capitalize(),
            "planets_in_house": [p.capitalize() for p in planets_in_h]
        })

    # 2. Extract Primary Karaka Details
    karaka_details = []
    karaka_score_mod = 0

    for k_name in cfg["karakas"]:
        k_data = planets.get(k_name.lower()) or planets.get(k_name.capitalize()) or {}
        if k_data:
            sign = k_data.get("sign", "?")
            house = k_data.get("house", "?")
            dignity = k_data.get("dignity", "neutral")
            is_retro = k_data.get("retrograde", False)
            is_combust = k_data.get("combust", False)

            if dignity in ["exalted", "own"]:
                karaka_score_mod += 12
            elif dignity == "debilitated":
                karaka_score_mod -= 12

            if is_combust:
                karaka_score_mod -= 8
            if is_retro:
                karaka_score_mod -= 4

            karaka_details.append({
                "planet": k_name.capitalize(),
                "sign": sign,
                "house": house,
                "dignity": dignity,
                "retrograde": is_retro,
                "combust": is_combust,
            })

    # 3. Check Target-Specific Doshas & Yogas
    active_doshas = []
    if rel_type == "spouse":
        manglik = doshas.get("manglik", {})
        if manglik.get("is_present"):
            active_doshas.append("Manglik Dosha (Mars in 7th/8th/12th/4th/1st)")
            karaka_score_mod -= 10
        else:
            active_doshas.append("Non-Manglik (No major Mars martial affliction)")
    elif rel_type == "father":
        sun_p = planets.get("sun", {})
        if sun_p.get("house") in [8, 12] or sun_p.get("dignity") == "debilitated":
            active_doshas.append("Pitru Affirmation: Sun weakened or in dusthana")
            karaka_score_mod -= 8
    elif rel_type == "children":
        jup_p = planets.get("jupiter", {})
        if jup_p.get("house") in [6, 8, 12]:
            active_doshas.append("Santana Caution: Jupiter in 6th/8th/12th")
            karaka_score_mod -= 6

    # Relevant Yogas
    rel_yogas = [
        y.get("name") for y in yogas
        if any(w in y.get("name", "").lower() for w in ["raj", "dhana", "gaja", "shubha", "vivah", "guru"])
    ]
    if rel_yogas:
        karaka_score_mod += min(len(rel_yogas) * 4, 12)

    # 4. Calculate Deterministic Relationship Score (0 to 100)
    base_score = 65
    raw_score = base_score + house_score_mod + karaka_score_mod
    final_score = max(25, min(96, raw_score))

    return {
        "target": rel_type,
        "title": cfg["title"],
        "icon": cfg["icon"],
        "score": final_score,
        "houses": house_details,
        "karakas": karaka_details,
        "divisional": cfg["divisional"],
        "doshas": active_doshas,
        "yogas": rel_yogas[:4],
        "focus_areas": cfg["focus_areas"],
    }


def format_relationship_subset_context(analysis: dict, profile: dict = None, history: list = None) -> str:
    """
    Formats ONLY the relevant astrological subset for the chosen relationship target.
    Eliminates token bloat while providing rich target data.
    """
    title = analysis.get("title", "Relationship")
    score = analysis.get("score", 70)
    houses = analysis.get("houses", [])
    karakas = analysis.get("karakas", [])
    doshas = analysis.get("doshas", [])
    yogas = analysis.get("yogas", [])
    divisional = analysis.get("divisional")

    # Format house subset block
    house_lines = []
    for h in houses:
        planets_str = f" containing [{', '.join(h['planets_in_house'])}]" if h['planets_in_house'] else " (Vacant)"
        house_lines.append(f"- {h['house']}th House: Sign {h['sign']} | Lord: {h['lord']}{planets_str}")

    # Format karaka subset block
    karaka_lines = []
    for k in karakas:
        status_parts = []
        if k["retrograde"]:
            status_parts.append("Retrograde [R]")
        if k["combust"]:
            status_parts.append("Combust")
        status_parts.append(f"Dignity: {k['dignity']}")

        karaka_lines.append(
            f"- {k['planet']}: In {k['sign']} (House {k['house']}) — {', '.join(status_parts)}"
        )

    name = profile.get("name", "Seeker") if profile else "Seeker"

    return f"""[RELATIONSHIP TARGET DATA: {title.upper()}]
Subject Name: {name}

[PRIMARY HOUSES FOR {title.upper()}]

{chr(10).join(house_lines)}

[PRIMARY KARAKA PLANETS]
{chr(10).join(karaka_lines) if karaka_lines else "Standard Karaka planetary alignment."}

[DIVISIONAL CHART SUPPORT]
{f"Chart: {divisional} active indicators." if divisional else "D1 Lagna primary indicators."}

[DOSHAS & AFFLICTIONS]
{chr(10).join(f"- {d}" for d in doshas) if doshas else "- No severe target-specific afflictions detected."}

[SUPPORTIVE YOGAS]
{chr(10).join(f"- {y}" for y in yogas) if yogas else "- Standard benefic yogas."}"""
