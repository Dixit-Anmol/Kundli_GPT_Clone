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


def format_core_chart(chart_data: dict) -> str:
    """Format the core ascendant/moon/nakshatra context block."""
    meta = chart_data.get("metadata") if isinstance(chart_data.get("metadata"), dict) and chart_data.get("metadata") else chart_data
    asc = meta.get("ascendant_sign") or chart_data.get("ascendant_sign") or "Aries"
    moon = meta.get("moon_sign") or chart_data.get("moon_sign") or "Cancer"
    nak = meta.get("nakshatra") or chart_data.get("nakshatra") or "Pushya"
    pada = meta.get("pada") or chart_data.get("pada") or 1
    asc_deg = meta.get("ascendant_longitude", 0.0)

    return (
        f"Ascendant (Lagna): {asc} at {asc_deg:.2f}°\n"
        f"Moon Sign (Rashi): {moon}\n"
        f"Nakshatra: {nak} (Pada {pada})"
    )





def format_planets(planets: dict) -> str:
    """Format planetary positions concisely."""
    lines = []
    for p_name, p in planets.items():
        state = " (Retrograde)" if p.get("retrograde") else ""
        combust = " (Combust)" if p.get("combust") else ""
        lines.append(
            f"- {p_name.capitalize()}: {p.get('sign', '?')} in H{p.get('house', '?')}{state}{combust}"
        )
    return "\n".join(lines)


def format_houses_subset(houses: dict, planets: dict, house_numbers: list) -> str:
    """Format specified houses compactly."""
    lines = []
    for h_num in house_numbers:
        h_key = str(h_num)
        h = houses.get(h_key, {})
        if not h:
            continue
        occupants = [p_name.capitalize() for p_name, p in planets.items() if str(p.get("house")) == h_key]
        occ_str = ", ".join(occupants) if occupants else "Empty"
        lines.append(
            f"- House {h_num} ({h.get('sign', '?')}): Lord {h.get('lord', '?').capitalize()} | Occupants: {occ_str}"
        )
    return "\n".join(lines)


def format_all_houses(houses: dict, planets: dict) -> str:
    """Format all 12 houses compactly."""
    return format_houses_subset(houses, planets, list(range(1, 13)))


def format_yogas(yogas: list) -> str:
    """Format yoga list compactly."""
    if not yogas:
        return "None active."
    lines = []
    for y in yogas[:5]:
        lines.append(f"- {y.get('name', '?')} ({y.get('type', '?')})")
    return "\n".join(lines)


def format_doshas(doshas: dict) -> str:
    """Format active dosha status."""
    lines = []
    for d_name, d_val in doshas.items():
        if d_val.get("is_present"):
            lines.append(f"- {d_name.capitalize()}: Active ({d_val.get('description', '')[:60]})")
    return "\n".join(lines) or "No major dosha afflictions."


def format_history(history: list, last_n: int = 2) -> str:
    """Format recent conversation history compactly."""
    if not history:
        return ""
    turns = []
    for h in history[-last_n:]:
        role = "User" if h.get("role") == "user" else "AI"
        text = (h.get("content") or h.get("text") or "")[:100]
        turns.append(f"{role}: {text}")
    return "\n".join(turns)


def format_dasha_info(chart_data: dict) -> str:
    """Format the active Vimshottari Mahadasha timeline with start & end dates/years."""
    dasha = chart_data.get("current_dasha") or {}
    if not isinstance(dasha, dict):
        dasha = {}
    
    planet = (dasha.get("planet") or chart_data.get("metadata", {}).get("current_dasha") or "Jupiter").capitalize()
    start = str(dasha.get("start", "2018-05-12"))
    end = str(dasha.get("end", "2034-05-12"))

    start_year = start.split("-")[0] if "-" in start else start
    end_year = end.split("-")[0] if "-" in end else end

    return (
        f"Active Mahadasha Planet: {planet}\n"
        f"Timeline Dates: {start} to {end}\n"
        f"Timeline Years: {start_year} to {end_year}\n"
        f"REQUIRED BOLD TIMELINE FORMAT: **Active {planet} Mahadasha ({start_year} to {end_year})**"
    )

