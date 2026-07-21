"""
Vedic Financial Engine & D2 Hora Sub-Chart Specialist.

Calculates:
- D2 Hora Divisional Chart (Surya Hora vs Chandra Hora placements)
- D4 Chaturthamsha (Property & Fixed Assets)
- Indu Lagna (Special Vedic Wealth Point)
- Key Financial Lords (2nd, 11th, 5th, 9th, 8th, 12th)
- Dhana & Lakshmi Yogas
"""

SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# Planetary Kala/Ray values for Indu Lagna calculation
PLANET_RAYS = {
    "sun": 30,
    "moon": 16,
    "mars": 6,
    "mercury": 8,
    "jupiter": 10,
    "venus": 12,
    "saturn": 1,
}

SIGN_LORDS = {
    "Aries": "mars", "Taurus": "venus", "Gemini": "mercury", "Cancer": "moon",
    "Leo": "sun", "Virgo": "mercury", "Libra": "venus", "Scorpio": "mars",
    "Sagittarius": "jupiter", "Capricorn": "saturn", "Aquarius": "saturn", "Pisces": "jupiter"
}


def calculate_d2_hora(planets: dict) -> dict:
    """
    Calculate D2 Hora divisional chart placements.
    Odd Signs (Aries, Gemini, Leo, Libra, Sagittarius, Aquarius):
        0-15° = Sun Hora (Leo) -> Active Earning & Enterprise
        15-30° = Moon Hora (Cancer) -> Accumulated Wealth & Assets
    Even Signs (Taurus, Cancer, Virgo, Scorpio, Capricorn, Pisces):
        0-15° = Moon Hora (Cancer) -> Accumulated Wealth & Assets
        15-30° = Sun Hora (Leo) -> Active Earning & Enterprise
    """
    sun_hora_planets = []
    moon_hora_planets = []
    hora_details = {}

    for p_name, p in planets.items():
        deg = float(p.get("degree", 0.0))
        sign_str = p.get("sign", "Aries")

        sign_idx = SIGN_NAMES.index(sign_str) if sign_str in SIGN_NAMES else 0
        deg_in_sign = deg % 30.0 if deg > 30 else deg

        # Odd sign index (0, 2, 4, 6, 8, 10 for Aries, Gemini, Leo, etc.)
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

    dominant = (
        "Sun Hora Dominant 🔥 (Strong Drive for Active Earning, Business & Enterprise)"
        if len(sun_hora_planets) > len(moon_hora_planets)
        else "Moon Hora Dominant 💧 (Strong Focus on Liquid Savings, Assets & Asset Preservation)"
    )

    return {
        "sun_hora_planets": sun_hora_planets,
        "moon_hora_planets": moon_hora_planets,
        "hora_details": hora_details,
        "dominant_hora": dominant,
    }


def calculate_indu_lagna(chart_data: dict) -> dict:
    """
    Calculate Indu Lagna (Special Vedic Wealth Point).
    Formula: Sum of 9th lord's rays from Lagna + 9th lord's rays from Moon Sign.
    Divide sum by 12, remainder from Moon sign gives Indu Lagna.
    """
    houses = chart_data.get("houses", {})
    planets = chart_data.get("raw_positions") or chart_data.get("planets", {})

    meta = chart_data.get("metadata", {})
    moon_sign = meta.get("moon_sign") or chart_data.get("moon_sign") or "Cancer"

    # 9th Lord from Lagna
    h9 = houses.get("9", {})
    lord_9_lagna = (h9.get("lord") or "jupiter").lower()
    rays_lagna = PLANET_RAYS.get(lord_9_lagna, 10)

    # 9th Lord from Moon Sign
    moon_idx = SIGN_NAMES.index(moon_sign) if moon_sign in SIGN_NAMES else 3
    sign_9_moon = SIGN_NAMES[(moon_idx + 8) % 12]
    lord_9_moon = SIGN_LORDS.get(sign_9_moon, "jupiter").lower()
    rays_moon = PLANET_RAYS.get(lord_9_moon, 10)

    total_rays = rays_lagna + rays_moon
    rem = total_rays % 12
    if rem == 0:
        rem = 12

    indu_sign_idx = (moon_idx + (rem - 1)) % 12
    indu_sign = SIGN_NAMES[indu_sign_idx]

    # Find planets occupying or aspecting Indu Lagna
    occupants = [
        p_name.capitalize()
        for p_name, p in planets.items()
        if p.get("sign") == indu_sign
    ]
    occ_str = ", ".join(occupants) if occupants else "Unoccupied"

    return {
        "indu_lagna_sign": indu_sign,
        "rays_sum": total_rays,
        "occupants": occ_str,
        "description": f"Indu Lagna in {indu_sign} (Total Wealth Rays: {total_rays}). Occupants: {occ_str}.",
    }


def analyze_financial_profile(chart_data: dict) -> dict:
    """
    Generate comprehensive Vedic financial profile with D2 Hora sub-chart data.
    """
    planets = chart_data.get("raw_positions") or chart_data.get("planets", {})
    houses = chart_data.get("houses", {})
    yogas = chart_data.get("yogas", [])

    # 1. D2 Hora Sub-Chart Placements
    d2 = calculate_d2_hora(planets)

    # 2. Indu Lagna Wealth Point
    indu = calculate_indu_lagna(chart_data)

    # 3. Key Financial Lords & House Details
    h2 = houses.get("2", {})
    h11 = houses.get("11", {})
    h5 = houses.get("5", {})
    h9 = houses.get("9", {})
    h8 = houses.get("8", {})
    h12 = houses.get("12", {})

    l2 = h2.get("lord", "?").capitalize()
    l11 = h11.get("lord", "?").capitalize()
    l5 = h5.get("lord", "?").capitalize()
    l9 = h9.get("lord", "?").capitalize()
    l8 = h8.get("lord", "?").capitalize()
    l12 = h12.get("lord", "?").capitalize()

    # D2 Hora placement of key Dhana Lords (2nd & 11th)
    l2_p = planets.get(h2.get("lord", "").lower(), {})
    l11_p = planets.get(h11.get("lord", "").lower(), {})
    l2_hora = d2["hora_details"].get(h2.get("lord", "").lower(), "N/A")
    l11_hora = d2["hora_details"].get(h11.get("lord", "").lower(), "N/A")

    # 4. Wealth Yogas
    wealth_yogas = [
        y.get("name")
        for y in yogas
        if any(
            kw in (y.get("name", "") + y.get("meaning", "")).lower()
            for kw in ["dhan", "wealth", "lakshmi", "money", "fortune", "gaja", "hamsa"]
        )
    ]

    return {
        "d2_hora": d2,
        "indu_lagna": indu,
        "d1_financial_houses": {
            "h2_wealth_accumulation": f"House 2 ({h2.get('sign', '?')}) | Lord: {l2} (in {l2_p.get('sign', '?')} H{l2_p.get('house', '?')} | D2 Hora: {l2_hora})",
            "h11_gains_income": f"House 11 ({h11.get('sign', '?')}) | Lord: {l11} (in {l11_p.get('sign', '?')} H{l11_p.get('house', '?')} | D2 Hora: {l11_hora})",
            "h5_speculation_investments": f"House 5 ({h5.get('sign', '?')}) | Lord: {l5}",
            "h9_fortune_luck": f"House 9 ({h9.get('sign', '?')}) | Lord: {l9}",
            "h8_unearned_wealth": f"House 8 ({h8.get('sign', '?')}) | Lord: {l8}",
            "h12_expenditure_outflow": f"House 12 ({h12.get('sign', '?')}) | Lord: {l12}",
        },
        "wealth_yogas": wealth_yogas or ["Standard Dhan Yoga Combinations"],
    }


def format_finance_context_subset(analysis: dict) -> str:
    """Format structured financial subset context string for LLM prompt."""
    d2 = analysis.get("d2_hora", {})
    indu = analysis.get("indu_lagna", {})
    fh = analysis.get("d1_financial_houses", {})
    yogas = analysis.get("wealth_yogas", [])

    sun_p = ", ".join(d2.get("sun_hora_planets", [])) or "None"
    moon_p = ", ".join(d2.get("moon_hora_planets", [])) or "None"

    return f"""[D2 HORA DIVISIONAL CHART & WEALTH SUB-CHART INDICATORS]
• D2 Hora Disposition: {d2.get('dominant_hora', 'N/A')}
  - Sun Hora Planets (Active Earning & Enterprise): {sun_p}
  - Moon Hora Planets (Liquid Savings & Asset Preservation): {moon_p}

[INDU LAGNA — SPECIAL VEDIC WEALTH ASCENDANT]
• Indu Lagna Point: {indu.get('indu_lagna_sign', 'N/A')} (Rays Sum: {indu.get('rays_sum', 0)})
• Indu Lagna Occupants: {indu.get('occupants', 'None')}

[D1 FINANCIAL HOUSE LORDS & D2 HORA PLACEMENTS]
• 2nd House (Dhana / Accumulated Wealth): {fh.get('h2_wealth_accumulation', 'N/A')}
• 11th House (Labha / Income & Gains): {fh.get('h11_gains_income', 'N/A')}
• 5th House (Speculative Gains & Stocks): {fh.get('h5_speculation_investments', 'N/A')}
• 9th House (Bhagya / Financial Fortune): {fh.get('h9_fortune_luck', 'N/A')}
• 8th House (Unearned Wealth & Joint Assets): {fh.get('h8_unearned_wealth', 'N/A')}
• 12th House (Vyaya / Outflow & Investments): {fh.get('h12_expenditure_outflow', 'N/A')}

[ACTIVE DHANA & LAKSHMI YOGAS]
{chr(10).join(f"- {y}" for y in yogas)}"""
