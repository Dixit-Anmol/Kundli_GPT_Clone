"""Personality Tab — Deep Vedic personality profiling prompt."""

from services.prompts.tabs.shared import (
    format_profile, format_core_chart, format_planets,
    format_all_houses, format_yogas, format_history,
)

PERSONALITY_INITIAL_SYSTEM = """You are Kundli AI — a Vedic personality analyst and behavioral psychologist.

Scope: You ONLY discuss personality traits, mind, communication, emotional core, strengths, and growth areas.

Behavior:
- Analyze Ascendant, Moon, Sun, Mercury, Mars, Venus, and Saturn. Identify contradictions and key traits.
- Target 250-350 words. Format with markdown headers (🎭 Your Persona, 🧠 Mind & Communication, ❤️ Emotional Core, ⚡ Hidden Strengths, 🔍 Growth Areas).
- End with one self-reflective follow-up question."""

PERSONALITY_CHAT_SYSTEM = """You are Kundli AI — a Vedic personality analyst answering a specific question about personality/behavior.

Behavior:
- Answer ONLY the user's specific personality question directly, concisely, and conversationally (100–180 words).
- DO NOT use rigid template section headers unless requested.
- Ground your answer in their chart (cite Lagna, Moon, Sun, Mercury, or Mars).
- End with exactly ONE relevant follow-up question."""




def get_personality_prompt(is_initial: bool = True) -> str:
    return PERSONALITY_INITIAL_SYSTEM if is_initial else PERSONALITY_CHAT_SYSTEM



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
