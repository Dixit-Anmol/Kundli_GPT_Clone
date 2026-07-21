"""
Shared context formatting helpers used by all tab prompt builders.
"""
from services.prompts.geeta import get_planet_strengths, calculate_vedic_aspects


SIGN_HINDI_MAP = {
    "Aries": "Mesh", "Taurus": "Vrishabha", "Gemini": "Mithun",
    "Cancer": "Kark", "Leo": "Simha", "Virgo": "Kanya",
    "Libra": "Tula", "Scorpio": "Vrishchik", "Sagittarius": "Dhanu",
    "Capricorn": "Makar", "Aquarius": "Kumbh", "Pisces": "Meen",
}

def format_sign_hindi(sign: str) -> str:
    hindi = SIGN_HINDI_MAP.get(sign)
    return f"{sign} ({hindi})" if hindi else str(sign)


def format_profile(profile: dict) -> str:
    """Format user profile block."""
    if not profile:
        return "Name: Seeker"
    name = profile.get("name", "Seeker")
    dob = profile.get("date_of_birth", "N/A")
    tob = profile.get("time_of_birth", "N/A")
    return f"Name: {name}\nDate of Birth: {dob}\nTime of Birth: {tob}"


def format_dasha_info(chart_data: dict) -> str:
    """Format active Vimshottari Mahadasha planet, start/end dates, and timeline."""
    curr = chart_data.get("current_dasha")
    timeline = chart_data.get("dasha_timeline", [])

    if not curr and timeline:
        import datetime
        from services.astrology.dasha import get_current_dasha
        try:
            curr = get_current_dasha(timeline, datetime.date.today())
        except Exception:
            curr = timeline[0] if timeline else None

    if curr:
        planet = curr.get("planet", "Unknown").capitalize()
        start = curr.get("start", "N/A")
        end = curr.get("end", "N/A")
        duration = curr.get("duration_years", "N/A")

        dasha_str = f"ACTIVE MAHADASHA: {planet} Mahadasha (Start: {start} | End: {end} | Duration: {duration} years)"

        # Add next dasha preview if available
        next_dasha = ""
        for i, p in enumerate(timeline):
            if p.get("start") == curr.get("start") and p.get("planet") == curr.get("planet") and i + 1 < len(timeline):
                nxt = timeline[i + 1]
                next_dasha = f"\nNEXT MAHADASHA PREVIEW: {nxt.get('planet', '').capitalize()} Mahadasha (Start: {nxt.get('start')} | End: {nxt.get('end')})"
                break
        return dasha_str + next_dasha

    return "ACTIVE MAHADASHA: Calculation pending."


def format_core_chart(chart_data: dict) -> str:
    """Format the core ascendant/moon/nakshatra and active Dasha timeline context block."""
    meta = chart_data.get("metadata") if isinstance(chart_data.get("metadata"), dict) and chart_data.get("metadata") else chart_data
    asc = meta.get("ascendant_sign") or chart_data.get("ascendant_sign") or "Aries"
    moon = meta.get("moon_sign") or chart_data.get("moon_sign") or "Cancer"
    nak = meta.get("nakshatra") or chart_data.get("nakshatra") or "Pushya"
    pada = meta.get("pada") or chart_data.get("pada") or 1
    asc_deg = meta.get("ascendant_longitude", 0.0)

    dasha_block = format_dasha_info(chart_data)

    return (
        f"Ascendant (Lagna): {asc} at {asc_deg:.2f}°\n"
        f"Moon Sign (Rashi): {moon}\n"
        f"Nakshatra: {nak} (Pada {pada})\n"
        f"{dasha_block}"
    )






def format_planets(planets: dict) -> str:
    """Format planetary positions with strengths."""
    strengths = get_planet_strengths(planets)
    lines = []
    for p_name, p in planets.items():
        state = "Retrograde" if p.get("retrograde") else "Direct"
        combust = "Combust" if p.get("combust") else ""
        str_val, str_desc = strengths.get(p_name, ("Neutral", ""))
        status_parts = [s for s in [state, combust] if s]
        lines.append(
            f"- {p.get('name_sanskrit', p_name.capitalize())} ({p_name.capitalize()}): "
            f"{p.get('sign', '?')} | {p.get('degree', 0):.1f}° | House {p.get('house', '?')} | "
            f"Nak: {p.get('nakshatra', {}).get('name', '?')} | {', '.join(status_parts)} | {str_val}"
        )
    return "\n".join(lines)


def format_houses_subset(houses: dict, planets: dict, house_numbers: list) -> str:
    """Format only the specified house numbers."""
    lines = []
    for h_num in house_numbers:
        h_key = str(h_num)
        h = houses.get(h_key, {})
        if not h:
            continue
        occupants = [p_name.capitalize() for p_name, p in planets.items() if str(p.get("house")) == h_key]
        occ_str = ", ".join(occupants) if occupants else "Empty"
        lines.append(
            f"- House {h_num} ({h.get('sign', '?')}): Lord: {h.get('lord', '?').capitalize()} | "
            f"Occupants: {occ_str} | {h.get('signification', '')}"
        )
    return "\n".join(lines)


def format_all_houses(houses: dict, planets: dict) -> str:
    """Format all 12 houses."""
    return format_houses_subset(houses, planets, list(range(1, 13)))


def format_yogas(yogas: list) -> str:
    """Format yoga list."""
    if not yogas:
        return "None active."
    lines = []
    for y in yogas:
        lines.append(f"- {y.get('name', '?')} ({y.get('type', '?')}): {y.get('meaning', '')}")
    return "\n".join(lines)


def format_doshas(doshas: dict) -> str:
    """Format dosha status."""
    lines = []
    for d_name, d_val in doshas.items():
        active = "Active" if d_val.get("is_present") else "Not Active"
        lines.append(f"- {d_name.capitalize()}: {active} — {d_val.get('description', 'No affliction')}")
    return "\n".join(lines) or "None detected."


def format_history(history: list, last_n: int = 4) -> str:
    """Format recent conversation history."""
    if not history:
        return "No previous conversation."
    turns = []
    for h in history[-last_n:]:
        turns.append(f"{h['role'].capitalize()}: {h['content'][:200]}")
    return "\n".join(turns)
