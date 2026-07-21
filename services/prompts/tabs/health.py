"""Health Tab — Vedic health analyst prompt."""

from services.prompts.tabs.shared import (
    format_profile, format_core_chart, format_planets,
    format_houses_subset, format_doshas, format_history,
)

HEALTH_INITIAL_SYSTEM = """You are Kundli AI — a Vedic health analyst combining Jyotish and Ayurveda.

Scope: You ONLY discuss health, constitution, disease tendencies, mental wellbeing, immunity, and recovery.

⚠️ DISCLAIMER: Always include at the end: "This is an astrological estimation — not a medical diagnosis. Always consult qualified healthcare professionals for medical concerns."

Behavior:
- STRICT NO PERCENTAGE RULE: DO NOT write any numerical percentages in your text response. Describe dosha constitution qualitatively using descriptive words only (e.g. "predominantly Pitta").
- Analyze 1st, 6th, 8th, and 12th houses, Moon sign, and planetary body mappings.
- Target 200-350 words. Format with markdown headers (🏥 Health Profile, 🧠 Mental Wellbeing, 💪 Strengths, ⚠️ Vulnerable Areas, 🌿 Ayurvedic Tips).
- End with one health-specific follow-up question."""

HEALTH_CHAT_SYSTEM = """You are Kundli AI — a Vedic health analyst answering a specific health query.

⚠️ DISCLAIMER: Always include: "Astrological estimation — not medical advice."

Behavior:
- Answer ONLY the user's specific health/wellness question directly, concisely, and conversationally (100–180 words).
- DO NOT use rigid template section headers unless requested.
- STRICT NO PERCENTAGE RULE: DO NOT write any numerical percentages in your response text.
- Ground your answer in their chart (cite 1st/6th/8th lords, Moon, or weak planets).
- End with exactly ONE relevant follow-up question."""





def get_health_prompt(is_initial: bool = True) -> str:
    return HEALTH_INITIAL_SYSTEM if is_initial else HEALTH_CHAT_SYSTEM



def build_health_context(
    query: str,
    chart_data: dict,
    profile: dict = None,
    history: list = None,
    computed: dict = None,
    **kwargs,
) -> str:
    planets = chart_data.get("planets", {})
    houses = chart_data.get("houses", {})
    doshas = chart_data.get("doshas", {})

    # Include Prakriti data if available
    prakriti_info = "Not computed."
    if computed and computed.get("prakriti"):
        p = computed["prakriti"]
        prakriti_info = (
            f"Vata: {p.get('vata', 0)}% | Pitta: {p.get('pitta', 0)}% | Kapha: {p.get('kapha', 0)}%\n"
            f"Dominant Dosha: {p.get('dominant_dosha', 'N/A')}\n"
            f"Dominant Element: {p.get('dominant_element', 'N/A')}"
        )

    return f"""[CONVERSATION HISTORY]
{format_history(history)}

[USER PROFILE]
{format_profile(profile)}

[CORE CHART]
{format_core_chart(chart_data)}

[HEALTH-RELEVANT HOUSES]
{format_houses_subset(houses, planets, [1, 6, 8, 12, 4])}

[HEALTH-CRITICAL PLANETS]
{_format_health_planets(planets, houses)}

[AYURVEDIC PRAKRITI ESTIMATION]
{prakriti_info}

[DOSHAS]
{format_doshas(doshas)}

[USER QUESTION]
\"{query}\""""


def _format_health_planets(planets: dict, houses: dict) -> str:
    """Extract health-critical planets."""
    health_houses = {1, 4, 6, 8, 12}
    relevant = []
    for p_name, p in planets.items():
        house = p.get("house")
        if house and int(house) in health_houses:
            relevant.append(
                f"- {p_name.capitalize()}: {p.get('sign', '?')} in House {house} "
                f"[{p.get('dignity', 'neutral')}] — "
                f"{'Retrograde' if p.get('retrograde') else 'Direct'}"
            )
    # Always include Sun and Moon
    for key_planet in ["sun", "moon"]:
        if key_planet in planets and not any(key_planet in r for r in relevant):
            p = planets[key_planet]
            relevant.append(
                f"- {key_planet.capitalize()}: {p.get('sign', '?')} in House {p.get('house', '?')} "
                f"[{p.get('dignity', 'neutral')}]"
            )
    return "\n".join(relevant) or "No specific health planet data."
