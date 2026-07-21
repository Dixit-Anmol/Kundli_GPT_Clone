"""Overview Tab — Concise overall personality and chart summary prompt."""

from services.prompts.tabs.shared import (
    format_profile, format_core_chart, format_planets,
    format_all_houses, format_yogas, format_doshas, format_history,
)

OVERVIEW_INITIAL_SYSTEM = """You are Kundli AI — a master Vedic Astrologer providing a comprehensive, exceptionally accurate birth chart overview.

Scope: You ONLY discuss the user's overall chart summary, key planetary placements, core identity, and active Dasha effects.

MANDATES & REVELATION DIRECTIVE:
1. UNCOMMON CHART SECRET: Open with the single most defining, uncommon secret about this birth chart — an eye-opening astrological truth grounded in their exact Lagna, Moon sign, 10th lord, or active Yogas.
2. DO NOT USE THE WORD "SHOCKING": Never write the literal word "shocking" anywhere in your text. Present your revelations naturally with deep astrological proof.
3. TARGET LENGTH: 220–300 words total. Complete all sentences fully.

RESPONSE ARCHITECTURE (4 crisp markdown sections):

### ✨ Defining Chart Secret & Core Blueprint
Reveal their single most defining astrological feature, Lagna personality, and core life path.

### 🌙 Moon Mind, Sun Identity & Planetary Strengths
Analyze Moon sign (mind/emotions), Sun sign (identity/drive), and strongest/weakest planets.

### 🪐 Active Yogas, Doshas & Dasha Influences
Highlight active Dhan/Raj Yogas, Dosha mitigations, and active Mahadasha timing effects.

### 💡 Strategic Life Guidance & Action Steps
Provide 2 concrete, tailored guidance steps matching their chart's highest potential."""

OVERVIEW_CHAT_SYSTEM = """You are Kundli AI — a seasoned Vedic astrologer answering a specific question about the user's chart.

Behavior:
- Answer ONLY the specific user question directly, concisely, and conversationally (100–180 words).
- Ground your answer directly in their birth chart (cite specific planets, houses, or yogas relevant to their question).
- Include ONE uncommon, highly accurate astrological insight.
- DO NOT use the literal word "shocking" anywhere.
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
