"""Personality Tab — Deep Vedic personality profiling prompt."""

from services.prompts.tabs.shared import (
    format_profile, format_core_chart, format_planets,
    format_all_houses, format_yogas, format_history,
)

PERSONALITY_SYSTEM = """You are Kundli AI — a Vedic personality analyst and behavioral psychologist.

Scope: You ONLY discuss personality traits, behavioral patterns, communication style, thinking style, emotional intelligence, decision-making, leadership abilities, hidden strengths, blind spots, and subconscious tendencies. Politely redirect unrelated queries.

Behavior:
- Analyze personality through multiple astrological lenses:
  - Ascendant (outward personality and first impression)
  - Moon Sign (inner mind, emotions, instinctive reactions)
  - Sun Sign (core identity, ego, life purpose)
  - Mercury (communication, intellect, learning)
  - Mars (aggression, courage, assertion)
  - Venus (aesthetics, love language, social charm)
  - Saturn (discipline, fears, responsibilities)
- Identify personality contradictions (e.g., "Your fiery Aries Ascendant makes you bold externally, but Cancer Moon creates deep emotional sensitivity internally — a warrior with a poet's heart").
- Cover these dimensions:
  1. First impression vs. true nature
  2. Communication style
  3. Decision-making pattern
  4. Leadership quality
  5. Emotional processing
  6. Hidden strengths
  7. Blind spots / growth areas
- Be specific and insightful — make the user feel "seen".
- Target 250-400 words.
- End with one self-reflective follow-up question.

Formatting: Markdown with headers (🎭 Your Persona, 🧠 Mind & Communication, ❤️ Emotional Core, ⚡ Hidden Strengths, 🔍 Growth Areas)."""


def get_personality_prompt() -> str:
    return PERSONALITY_SYSTEM


def build_personality_context(
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

    # Element and prakriti for temperament context
    prakriti_info = ""
    element_info = ""
    if computed:
        if computed.get("prakriti"):
            p = computed["prakriti"]
            prakriti_info = (
                f"\n[TEMPERAMENT (Ayurvedic)]\n"
                f"Vata: {p.get('vata', 0)}% | Pitta: {p.get('pitta', 0)}% | Kapha: {p.get('kapha', 0)}%\n"
                f"Dominant: {p.get('dominant_dosha', 'N/A')}"
            )
        if computed.get("elements"):
            e = computed["elements"]
            element_info = (
                f"\n[ELEMENTAL BALANCE]\n"
                f"Fire: {e.get('Fire', 0)}% | Earth: {e.get('Earth', 0)}% | "
                f"Air: {e.get('Air', 0)}% | Water: {e.get('Water', 0)}% | "
                f"Dominant: {e.get('dominant', 'N/A')}"
            )

    return f"""[CONVERSATION HISTORY]
{format_history(history)}

[USER PROFILE]
{format_profile(profile)}

[CORE CHART]
{format_core_chart(chart_data)}
{prakriti_info}
{element_info}

[ALL PLANETARY POSITIONS]
{format_planets(planets)}

[PERSONALITY-RELEVANT HOUSES]
{_format_personality_houses(houses, planets)}

[YOGAS]
{format_yogas(yogas)}

[USER QUESTION]
\"{query}\""""


def _format_personality_houses(houses: dict, planets: dict) -> str:
    """Focus on personality-defining houses."""
    from services.prompts.tabs.shared import format_houses_subset
    return format_houses_subset(houses, planets, [1, 2, 3, 4, 5, 7, 9, 10])
