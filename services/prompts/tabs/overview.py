"""Overview Tab — Concise overall personality and chart summary prompt."""

from services.prompts.tabs.shared import (
    format_profile, format_core_chart, format_planets,
    format_all_houses, format_yogas, format_doshas, format_history,
)
from services.astrology.divisional_engine import format_subchart_summary

OVERVIEW_INITIAL_SYSTEM = """You are Kundli AI — a master Vedic Astrologer providing a comprehensive birth chart overview combining D1 Lagna and D9 Navamsha sub-chart analysis.

Scope: You ONLY discuss overall chart summary, key planetary placements, core identity, active Dasha, and life trajectory.

MANDATES & REVELATION DIRECTIVE:
1. SUB-CHART & PLANETARY REASONS: Cite D1 & D9 Navamsha placements for Lagna Lord, Moon Sign, Sun Sign, and active Mahadasha planet. Explain WHY each placement shapes their life path.
2. ACTIVE DASHA TIMELINE: Explicitly state the active Mahadasha planet with its exact start date and end date timeline (e.g., "Active Jupiter Mahadasha running from 2018-05-12 to 2034-05-12").
3. CONCLUDING RESULT (BOTTOM LINE): End the reading with a clear, easy-to-understand concluding result paragraph summarizing the user's overall chart destiny and primary takeaway.
4. TARGET LENGTH: 220–300 words total. Complete all sentences fully.

RESPONSE ARCHITECTURE (3 crisp markdown sections + final result conclusion):

### ✨ Defining Chart Secret & D9 Navamsha Blueprint
Reveal their single most defining astrological feature, Lagna lord strength, D9 Navamsha disposition, and core life path.

### 🌙 Moon Mind, Sun Identity & Dasha Timeline
Analyze Moon sign (emotions), Sun sign (core identity), and active Mahadasha planet with its exact start and end dates.

### 🪐 Active Yogas, Strategic Guidance & Concluding Result
Highlight active Dhan/Raj Yogas, Dosha mitigations, and 2 concrete life guidance steps. Conclude this final section with a clear **Bottom-Line Result** summarizing their overarching life trajectory.
"""

OVERVIEW_CHAT_SYSTEM = """You are Kundli AI — a seasoned Vedic astrologer answering a specific question about the user's chart.

Behavior:
- Answer ONLY the specific user question directly, concisely, and conversationally (100–180 words).
- Ground answer directly in D1 & D9 chart placements and active Dasha.
- Conclude with a clear bottom-line takeaway result.
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
    planets = chart_data.get("raw_positions") or chart_data.get("planets", {})
    houses = chart_data.get("houses", {})
    yogas = chart_data.get("yogas", [])
    doshas = chart_data.get("doshas", {})

    d9_summary = format_subchart_summary(chart_data, "overview")

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

{d9_summary}

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
