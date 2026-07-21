"""
Shodashvarga & Sub-Chart Engine for Deep Vedic Analysis across all Tabs.

Calculates:
- D9 Navamsha (Marriage, Soul Destiny, Core Strength)
- D10 Dashamsha (Career, Status, Karma)
- D6 Shashtamsha / D7 Saptamsha (Health, Immunity, Relationships)
- D20 Vimshamsha (Spiritual Evolution, Moksha)
"""

SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

MOVABLE_SIGNS = {"Aries", "Cancer", "Libra", "Capricorn"}
FIXED_SIGNS = {"Taurus", "Leo", "Scorpio", "Aquarius"}
DUAL_SIGNS = {"Gemini", "Virgo", "Sagittarius", "Pisces"}


def calculate_d9_navamsha(planets: dict) -> dict:
    """Calculate D9 Navamsha sign for all 9 planets (3°20' per division)."""
    d9_positions = {}
    for p_name, p in planets.items():
        deg = float(p.get("degree", 0.0))
        sign_str = p.get("sign", "Aries")
        sign_idx = SIGN_NAMES.index(sign_str) if sign_str in SIGN_NAMES else 0
        deg_in_sign = deg % 30.0 if deg > 30 else deg

        nav_part = int(deg_in_sign // (30.0 / 9.0))  # 0 to 8

        if sign_str in MOVABLE_SIGNS:
            start_sign_idx = sign_idx
        elif sign_str in FIXED_SIGNS:
            start_sign_idx = (sign_idx + 8) % 12
        else:  # Dual
            start_sign_idx = (sign_idx + 4) % 12

        d9_sign_idx = (start_sign_idx + nav_part) % 12
        d9_positions[p_name] = SIGN_NAMES[d9_sign_idx]

    return d9_positions


def calculate_d10_dashamsha(planets: dict) -> dict:
    """Calculate D10 Dashamsha sign for all 9 planets (3°00' per division)."""
    d10_positions = {}
    for p_name, p in planets.items():
        deg = float(p.get("degree", 0.0))
        sign_str = p.get("sign", "Aries")
        sign_idx = SIGN_NAMES.index(sign_str) if sign_str in SIGN_NAMES else 0
        deg_in_sign = deg % 30.0 if deg > 30 else deg

        d10_part = int(deg_in_sign // 3.0)  # 0 to 9

        is_odd = (sign_idx % 2 == 0)
        start_sign_idx = sign_idx if is_odd else (sign_idx + 8) % 12

        d10_sign_idx = (start_sign_idx + d10_part) % 12
        d10_positions[p_name] = SIGN_NAMES[d10_sign_idx]

    return d10_positions


def calculate_d7_saptamsha(planets: dict) -> dict:
    """Calculate D7 Saptamsha sign for relationships & progeny (4°17' per division)."""
    d7_positions = {}
    for p_name, p in planets.items():
        deg = float(p.get("degree", 0.0))
        sign_str = p.get("sign", "Aries")
        sign_idx = SIGN_NAMES.index(sign_str) if sign_str in SIGN_NAMES else 0
        deg_in_sign = deg % 30.0 if deg > 30 else deg

        d7_part = int(deg_in_sign // (30.0 / 7.0))  # 0 to 6

        is_odd = (sign_idx % 2 == 0)
        start_sign_idx = sign_idx if is_odd else (sign_idx + 6) % 12

        d7_sign_idx = (start_sign_idx + d7_part) % 12
        d7_positions[p_name] = SIGN_NAMES[d7_sign_idx]

    return d7_positions


def format_subchart_summary(chart_data: dict, tab: str) -> str:
    """
    Format sub-chart divisional positions, planetary reasons, active Dasha, and impact for a tab.
    """
    planets = chart_data.get("raw_positions") or chart_data.get("planets", {})

    d9 = calculate_d9_navamsha(planets)
    d10 = calculate_d10_dashamsha(planets)
    d7 = calculate_d7_saptamsha(planets)

    curr_dasha = chart_data.get("current_dasha") or {}
    dasha_planet = curr_dasha.get("planet", "Jupiter").capitalize()
    dasha_start = curr_dasha.get("start", "N/A")
    dasha_end = curr_dasha.get("end", "N/A")

    if tab in ["career", "profession"]:
        lines = [
            "[D10 DASHAMSHA (CAREER & STATUS SUB-CHART)]",
            f"• Active Mahadasha Planet: {dasha_planet} (Running: {dasha_start} to {dasha_end})",
        ]
        for p_name in ["sun", "saturn", "jupiter", "mercury", "mars"]:
            if p_name in planets:
                p = planets[p_name]
                lines.append(
                    f"- {p_name.capitalize()}: D1 Sign: {p.get('sign', '?')} H{p.get('house', '?')} | "
                    f"D10 Dashamsha Sign: {d10.get(p_name, '?')} [{p.get('dignity', 'neutral')}] — "
                    f"Impact: Dictates professional status & leadership drive."
                )
        return "\n".join(lines)

    elif tab in ["marriage", "relationships", "relationship"]:
        lines = [
            "[D9 NAVAMSHA (SPOUSE & RELATIONSHIP SUB-CHART)]",
            f"• Active Mahadasha Planet: {dasha_planet} (Running: {dasha_start} to {dasha_end})",
        ]
        for p_name in ["venus", "jupiter", "mars", "moon", "sun"]:
            if p_name in planets:
                p = planets[p_name]
                lines.append(
                    f"- {p_name.capitalize()}: D1 Sign: {p.get('sign', '?')} H{p.get('house', '?')} | "
                    f"D9 Navamsha Sign: {d9.get(p_name, '?')} | D7 Sign: {d7.get(p_name, '?')} — "
                    f"Impact: Dictates soulmate connection & emotional harmony."
                )
        return "\n".join(lines)

    elif tab in ["health", "food"]:
        lines = [
            "[HEALTH & PHYSICAL VITALITY SUB-CHART INDICATORS]",
            f"• Active Mahadasha Planet: {dasha_planet} (Running: {dasha_start} to {dasha_end})",
        ]
        for p_name in ["sun", "moon", "mars", "saturn", "rahu", "ketu"]:
            if p_name in planets:
                p = planets[p_name]
                lines.append(
                    f"- {p_name.capitalize()}: D1 Sign: {p.get('sign', '?')} H{p.get('house', '?')} | "
                    f"D9 Sign: {d9.get(p_name, '?')} [{p.get('dignity', 'neutral')}] — "
                    f"Impact: Influences physical stamina, organ stress & immunity."
                )
        return "\n".join(lines)

    elif tab in ["spiritual", "remedies", "personality", "overview"]:
        lines = [
            "[D9 NAVAMSHA & SPIRITUAL SUB-CHART INDICATORS]",
            f"• Active Mahadasha Planet: {dasha_planet} (Running: {dasha_start} to {dasha_end})",
        ]
        for p_name in ["jupiter", "ketu", "saturn", "sun", "moon"]:
            if p_name in planets:
                p = planets[p_name]
                lines.append(
                    f"- {p_name.capitalize()}: D1 Sign: {p.get('sign', '?')} H{p.get('house', '?')} | "
                    f"D9 Navamsha Sign: {d9.get(p_name, '?')} — "
                    f"Impact: Governs inner wisdom, karmic lessons & soul evolution."
                )
        return "\n".join(lines)

    return ""
