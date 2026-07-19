"""Marriage & Compatibility Tab — Vedic relationship analyst prompt."""

from services.prompts.tabs.shared import (
    format_profile, format_core_chart, format_planets,
    format_houses_subset, format_yogas, format_doshas, format_history,
)

MARRIAGE_INITIAL_SYSTEM = """You are Kundli AI — a Vedic marriage and relationship counselor.

Scope: You ONLY discuss marriage, relationships, spouse characteristics, timing of marriage, compatibility, love vs arranged indicators, and relationship dynamics.

Behavior:
- Analyze the 7th house, Venus, Jupiter, Mars, Darakaraka, Upapada Lagna, and D9 Navamsa.
- Assess Manglik Dosha impact, spouse personality traits, timing, and love vs arranged indicators.
- Target 200-350 words. Format with markdown headers (💍 Marriage Potential, 👫 Spouse Profile, ⏰ Timing, 🔮 Compatibility).
- End with one relationship-specific follow-up question."""

MARRIAGE_CHAT_SYSTEM = """You are Kundli AI — a Vedic marriage counselor answering a specific relationship question.

Behavior:
- Answer ONLY the user's specific relationship question directly, concisely, and conversationally (100–180 words).
- DO NOT use rigid template section headers unless specifically requested.
- Ground your response directly in their birth chart (cite specific 7th lord, Venus, Jupiter, or 5th house placements).
- End with exactly ONE relevant follow-up question."""




def get_marriage_prompt(is_initial: bool = True) -> str:
    return MARRIAGE_INITIAL_SYSTEM if is_initial else MARRIAGE_CHAT_SYSTEM



def build_marriage_context(
    query: str,
    chart_data: dict,
    profile: dict = None,
    history: list = None,
    computed: dict = None,
    **kwargs,
) -> str:
    planets = chart_data.get("planets", {})
    houses = chart_data.get("houses", {})
    yogas = chart_data.get("yogas", [])
    doshas = chart_data.get("doshas", {})

    # Manglik status
    manglik = doshas.get("manglik", {})
    manglik_info = (
        f"Manglik Status: {'Active — ' + manglik.get('description', '') if manglik.get('is_present') else 'Not Manglik'}"
    )

    return f"""[CONVERSATION HISTORY]
{format_history(history)}

[USER PROFILE]
{format_profile(profile)}

[CORE CHART]
{format_core_chart(chart_data)}

[MARRIAGE-RELEVANT HOUSES]
{format_houses_subset(houses, planets, [1, 2, 4, 5, 7, 8, 12])}

[KEY PLANETS FOR MARRIAGE]
{_format_marriage_planets(planets, houses)}

[MANGLIK ANALYSIS]
{manglik_info}

[MARRIAGE-RELATED YOGAS]
{format_yogas([y for y in yogas if any(kw in y.get('name', '').lower() for kw in ['vivah', 'marriage', 'venus', 'relationship'])] or yogas[:5])}

[USER QUESTION]
\"{query}\""""


def _format_marriage_planets(planets: dict, houses: dict) -> str:
    """Extract marriage-critical planets."""
    h7 = houses.get("7", {})
    lord_7 = h7.get("lord", "").lower()
    
    relevant = []
    for p_name, p in planets.items():
        is_relevant = (
            p_name.lower() == lord_7 or
            p_name.lower() in ["venus", "jupiter", "mars", "rahu"] or
            p.get("house") in [5, 7, 8, 12]
        )
        if is_relevant:
            tag = "7th Lord" if p_name.lower() == lord_7 else ""
            tag_str = f"({tag})" if tag else ""
            relevant.append(
                f"- {p_name.capitalize()}: {p.get('sign', '?')} in House {p.get('house', '?')} "
                f"{tag_str} [{p.get('dignity', 'neutral')}]"
            )
    return "\n".join(relevant) or "No specific marriage planet data."

