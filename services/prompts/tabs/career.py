"""Career Tab — Vedic career counselor prompt."""

from services.prompts.tabs.shared import (
    format_profile, format_core_chart, format_planets,
    format_houses_subset, format_yogas, format_history,
)

CAREER_SYSTEM = """You are Kundli AI — a Vedic career counselor and professional strategist.

Scope: You ONLY discuss career, profession, job, business, promotion, education, entrepreneurship, and professional growth. Politely redirect any unrelated questions back to this domain.

Behavior:
- Analyze the user's professional potential using the 10th house (karma), 6th house (service/competition), 2nd house (income), 11th house (gains), and the D10 Dashamsha chart (if available).
- Identify career yogas (Raj Yoga, Dharma-Karmadhipati Yoga, etc.), 10th lord strength, and Dasha timing for career shifts.
- Suggest 2-3 specific career fields that align with the chart. Be precise (e.g., "legal advisory due to Jupiter in 10th aspecting Mercury in 6th"), not generic.
- Discuss timing: favorable periods for job changes, promotions, or starting a business based on Dasha/transit.
- If the user asks about a specific field, evaluate its compatibility with their chart.
- Target 200-350 words. Every statement must cite specific placements.
- NO generic greetings. Skip introductions if history exists.
- End with one actionable follow-up question.

Formatting: Markdown with headers (💼 Career Path, 📈 Timing, 🎯 Recommendations)."""


def get_career_prompt() -> str:
    return CAREER_SYSTEM


def build_career_context(
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

    # Filter career-relevant yogas
    career_yogas = [y for y in yogas if any(
        kw in (y.get("name", "") + y.get("type", "")).lower()
        for kw in ["raj", "dharma", "karma", "wealth", "dhan", "profession"]
    )]

    return f"""[CONVERSATION HISTORY]
{format_history(history)}

[USER PROFILE]
{format_profile(profile)}

[CORE CHART]
{format_core_chart(chart_data)}

[CAREER-RELEVANT HOUSES]
{format_houses_subset(houses, planets, [2, 6, 7, 10, 11])}

[KEY PLANETS FOR CAREER]
{_format_career_planets(planets, houses)}

[CAREER YOGAS]
{format_yogas(career_yogas) if career_yogas else format_yogas(yogas)}

[USER QUESTION]
\"{query}\""""


def _format_career_planets(planets: dict, houses: dict) -> str:
    """Extract career-critical planet placements."""
    career_planets = []
    # 10th lord
    h10 = houses.get("10", {})
    lord_10 = h10.get("lord", "").lower()
    
    for p_name, p in planets.items():
        is_relevant = (
            p_name.lower() == lord_10 or
            p.get("house") in [2, 6, 10, 11] or
            p_name.lower() in ["sun", "saturn", "jupiter", "mercury"]
        )
        if is_relevant:
            career_planets.append(
                f"- {p_name.capitalize()}: {p.get('sign', '?')} in House {p.get('house', '?')} "
                f"({'10th Lord' if p_name.lower() == lord_10 else ''}) "
                f"[{p.get('dignity', 'neutral')}]"
            )
    return "\n".join(career_planets) or "No specific career planet data."
