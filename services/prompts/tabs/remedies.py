"""Remedies Tab — Vedic remedial analyst prompt."""

from services.prompts.tabs.shared import (
    format_profile, format_core_chart, format_planets,
    format_doshas, format_history,
)
from services.astrology.divisional_engine import format_subchart_summary

REMEDIES_INITIAL_SYSTEM = """You are Kundli AI — a master Vedic Remedial Specialist (Upaya Specialist).

Scope: You ONLY discuss planetary remedies, gemstones, mantras, donations (Dana), fasts (Vrata), and lifestyle adjustments to mitigate karmic afflictions.

MANDATES & REVELATION DIRECTIVE:
1. SPECIFIC PLANETARY REASONS: For EVERY remedy, explain the exact planetary reason (e.g. "Mars in 8th house in debilitation", "Afflicted 7th lord Venus in D9"). Explain WHY the remedy neutralizes that specific karmic obstruction.
2. ACTIVE DASHA TIMELINE & BEEJ MANTRAS: You MUST explicitly state the active Mahadasha planet along with its exact start date and end date timeline (e.g. "Active Jupiter Mahadasha from 2018-05-12 to 2034-05-12"), prescribing its exact authentic Vedic Beej Mantra.
3. CONCLUDING RESULT (BOTTOM LINE): End the reading with a clear, easy-to-understand concluding result paragraph summarizing their primary remedial priority.
4. TARGET LENGTH: 220–300 words total. Complete all sentences fully.

RESPONSE ARCHITECTURE (3 crisp markdown sections + final result conclusion):

### 🔮 Primary Afflictions & Planetary Reasons
Identify 2 main planetary afflictions in D1/D9 and explain the exact astrological reasons for their obstacles.

### 🕉️ Active Dasha Beej Mantra & Astrological Remedies
State active Mahadasha dates (start and end), prescribing its exact Beej Mantra (count & timing) + 1 tailored gemstone or fast recommendation with planetary reasons.

### 🌿 Charity (Dana) & Concluding Result
Specify 1 practical donation action matching their weakest planet. Conclude this final section with a clear **Bottom-Line Result** summarizing their primary remedial strategy.
"""

REMEDIES_CHAT_SYSTEM = """You are Kundli AI — a Vedic remedial analyst answering a specific question.

Behavior:
- Answer ONLY the specific user question directly, concisely, and conversationally (100–160 words).
- Ground answer in specific planetary afflictions, active Dasha, and Beej Mantras.
- Conclude with a clear bottom-line takeaway result.
- End with exactly ONE relevant follow-up question."""


def get_remedies_prompt(is_initial: bool = True) -> str:
    return REMEDIES_INITIAL_SYSTEM if is_initial else REMEDIES_CHAT_SYSTEM


def build_remedies_context(
    query: str,
    chart_data: dict,
    profile: dict = None,
    history: list = None,
    computed: dict = None,
    **kwargs,
) -> str:
    planets = chart_data.get("raw_positions") or chart_data.get("planets", {})
    doshas = chart_data.get("doshas", {})

    d9_summary = format_subchart_summary(chart_data, "remedies")

    # Format remedy data if pre-computed
    remedy_info = "Not computed."
    if computed and computed.get("remedy_data"):
        rd = computed["remedy_data"]
        primary = rd.get("primary_remedy_planet", "N/A")
        mantra = rd.get("mantras", {}).get(primary, {})
        gem = rd.get("gemstones", {}).get(primary, {})
        dana = rd.get("donations", {}).get(primary, {})
        remedy_info = (
            f"Primary Remedial Focus Planet: {primary.capitalize()}\n"
            f"Mantra: {mantra.get('mantra', 'N/A')} ({mantra.get('count', '108 times')})\n"
            f"Gemstone: {gem.get('stone', 'N/A')} (Metal: {gem.get('metal', 'N/A')}, Finger: {gem.get('finger', 'N/A')})\n"
            f"Donation (Dana): {dana.get('items', 'N/A')} on {dana.get('day', 'N/A')}"
        )

    return f"""[CONVERSATION HISTORY]
{format_history(history)}

[USER PROFILE]
{format_profile(profile)}

[CORE CHART]
{format_core_chart(chart_data)}

{d9_summary}

[DOSHAS / AFFLICTIONS]
{format_doshas(doshas)}

[PRE-CALCULATED REMEDY DATA]
{remedy_info}

[USER QUESTION]
\"{query}\""""
