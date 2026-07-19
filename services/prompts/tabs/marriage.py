"""Marriage & Compatibility Tab — Vedic relationship analyst prompt."""

from services.prompts.tabs.shared import (
    format_profile, format_core_chart, format_planets,
    format_houses_subset, format_yogas, format_doshas, format_history,
)

MARRIAGE_SYSTEM = """You are Kundli AI — a Vedic marriage and relationship counselor.

Scope: You ONLY discuss marriage, relationships, spouse characteristics, timing of marriage, compatibility, love vs arranged marriage indicators, and relationship challenges. Politely redirect unrelated queries.

Behavior:
- Analyze the 7th house (partnerships), Venus (love/romance), Jupiter (husband significator for females), Mars (husband significator alternative), Darakaraka, Upapada Lagna, and D9 Navamsa chart.
- Assess Manglik Dosha impact honestly — explain if it's mild, moderate, or strong based on the exact Mars position.
- Describe the likely spouse personality based on 7th lord sign/house and planets in/aspecting the 7th.
- Discuss marriage timing using Dasha of 7th lord, Venus Dasha, Jupiter transit.
- Love vs Arranged: Check 5th-7th lord connection, Venus-Mars conjunction, Rahu in 7th.
- If delay/denial factors exist, explain honestly but constructively, with remedies.
- Target 200-350 words. Cite exact placements.
- End with one relationship-specific follow-up question.

Formatting: Markdown with headers (💍 Marriage Potential, 👫 Spouse Profile, ⏰ Timing, 🔮 Compatibility)."""


def get_marriage_prompt() -> str:
    return MARRIAGE_SYSTEM


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

