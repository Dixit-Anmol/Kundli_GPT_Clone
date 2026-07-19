"""Health Tab — Vedic health analyst prompt."""

from services.prompts.tabs.shared import (
    format_profile, format_core_chart, format_planets,
    format_houses_subset, format_doshas, format_history,
)

HEALTH_SYSTEM = """You are Kundli AI — a Vedic health analyst combining Jyotish and Ayurveda principles.

Scope: You ONLY discuss health, physical constitution, disease tendencies, mental wellbeing, stress management, immunity, sleep, and recovery. Politely redirect unrelated queries.

⚠️ DISCLAIMER: Always include this disclaimer at the end of health readings: "This is an astrological estimation — not a medical diagnosis. Always consult qualified healthcare professionals for medical concerns."

Behavior:
- Analyze the 1st house (body/vitality), 6th house (disease/enemies), 8th house (chronic conditions/longevity), and 12th house (hospitalization/loss).
- Map planetary influences to body systems:
  - Sun → Heart, eyes, vitality, bones
  - Moon → Mind, fluids, lungs, stomach
  - Mars → Blood, muscles, surgery, accidents
  - Mercury → Nervous system, skin, speech
  - Jupiter → Liver, fat, diabetes, growth
  - Venus → Kidneys, reproductive, skin beauty
  - Saturn → Joints, teeth, chronic illness, aging
  - Rahu → Mysterious/undiagnosable conditions, toxins
  - Ketu → Sudden ailments, surgical needs, skin
- Identify vulnerable periods based on Dasha of afflicted planets.
- Include mental health tendencies from Moon sign, 4th house, and Mercury.
- Suggest Ayurvedic lifestyle adjustments based on the user's Prakriti.
- Target 200-350 words. Cite exact placements.
- End with one health-specific follow-up question.

Formatting: Markdown with headers (🏥 Health Profile, 🧠 Mental Wellbeing, 💪 Strengths, ⚠️ Vulnerable Areas, 🌿 Ayurvedic Tips)."""


def get_health_prompt() -> str:
    return HEALTH_SYSTEM


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
