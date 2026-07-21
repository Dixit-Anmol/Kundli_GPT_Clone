"""Overview Tab — Concise overall personality and chart summary prompt."""

from services.prompts.tabs.shared import (
    format_profile, format_core_chart, format_planets,
    format_all_houses, format_yogas, format_doshas, format_history,
)

OVERVIEW_INITIAL_SYSTEM = """You are AstroSutra AI — a seasoned Vedic astrologer providing a concise, structured overall birth chart overview.

Scope: You ONLY discuss the user's overall chart summary, key placements, personality snapshot, and current Dasha effects.

Behavior:
- Open with the single most defining feature of this chart — something genuinely uncommon.
- Cover: Ascendant personality, Moon mind, Sun core identity, strongest/weakest planets, active yogas, doshas, current Dasha influence.
- Keep it structured with markdown headers (✨, 🌙, ☀️, 🪐). Target 200-350 words.
- NO generic greetings. Every claim must cite specific placements.
- End with one insightful follow-up question."""

OVERVIEW_CHAT_SYSTEM = """You are AstroSutra AI — a seasoned Vedic astrologer answering a specific question about the user's chart.

Behavior:
- Answer ONLY the specific user question directly, concisely, and conversationally (100–180 words).
- DO NOT use rigid multi-section template headers unless explicitly requested by the user.
- Ground your answer directly in their birth chart (cite specific planets, houses, or yogas relevant to their question).
- Maintain a warm, clear, and insightful tone.
- End with exactly ONE relevant follow-up question."""




def get_overview_prompt(is_initial: bool = True) -> str:
    return OVERVIEW_INITIAL_SYSTEM if is_initial else OVERVIEW_CHAT_SYSTEM



def build_overview_context(
    query: str,
    chart_data: dict,
    profile: dict = None,
    history: list = None,
    computed: dict = None,
    **kwargs,
) -> str:
    meta = chart_data.get("metadata", {})
    planets = chart_data.get("planets", {})
    houses = chart_data.get("houses", {})
    yogas = chart_data.get("yogas", [])
    doshas = chart_data.get("doshas", {})

    # Include lucky attributes and element data if pre-computed
    lucky = ""
    elements = ""
    rankings = ""
    if computed:
        if computed.get("lucky"):
            l = computed["lucky"]
            lucky = (
                f"\n[LUCKY ATTRIBUTES]\n"
                f"Colors: {', '.join(l.get('lucky_colors', []))}\n"
                f"Numbers: {', '.join(str(n) for n in l.get('lucky_numbers', []))}\n"
                f"Day: {l.get('lucky_day', 'N/A')}\n"
                f"Direction: {l.get('lucky_direction', 'N/A')}"
            )
        if computed.get("elements"):
            e = computed["elements"]
            elements = (
                f"\n[ELEMENT DISTRIBUTION]\n"
                f"Fire: {e.get('Fire', 0)}% | Earth: {e.get('Earth', 0)}% | "
                f"Air: {e.get('Air', 0)}% | Water: {e.get('Water', 0)}% | "
                f"Dominant: {e.get('dominant', 'N/A')}"
            )
        if computed.get("planet_rankings"):
            top3 = computed["planet_rankings"][:3]
            bot2 = computed["planet_rankings"][-2:]
            rankings = "\n[PLANET STRENGTH RANKING]\nStrongest: " + ", ".join(
                f"{r['planet'].capitalize()} ({r['status']})" for r in top3
            ) + "\nWeakest: " + ", ".join(
                f"{r['planet'].capitalize()} ({r['status']})" for r in bot2
            )

    return f"""[CONVERSATION HISTORY]
{format_history(history)}

[USER PROFILE]
{format_profile(profile)}

[CORE CHART]
{format_core_chart(chart_data)}
{lucky}
{elements}
{rankings}

[PLANETARY POSITIONS]
{format_planets(planets)}

[ALL HOUSES]
{format_all_houses(houses, planets)}

[YOGAS]
{format_yogas(yogas)}

[DOSHAS]
{format_doshas(doshas)}

[USER QUESTION]
\"{query}\""""
