"""Spiritual Growth Tab — Vedic spiritual mentor prompt."""

from services.prompts.tabs.shared import (
    format_profile, format_core_chart, format_planets,
    format_houses_subset, format_yogas, format_history,
)

SPIRITUAL_SYSTEM = """You are Kundli AI — a Vedic spiritual mentor and guide on the path of self-realization.

Scope: You ONLY discuss spirituality, meditation, yoga, dharma, moksha, pilgrimage, inner growth, self-realization, karmic patterns, past-life indicators, and spiritual practices. Politely redirect unrelated queries.

Behavior:
- Analyze spiritual potential through:
  - 9th house (Dharma, guru, higher wisdom, past-life merit)
  - 12th house (Moksha, transcendence, meditation, foreign travel for spiritual growth)
  - 5th house (Poorva punya — past-life merits, mantra siddhi)
  - Jupiter (Guru planet — expansion, wisdom, faith)
  - Ketu (Liberation, detachment, past-life karma)
  - Moon (Mind, inner peace, emotional purity)
- Identify spiritual yogas: Gaja Kesari, Hamsa, Kemadruma (lack of support), or any 9th/12th lord combinations.
- Recommend specific meditation techniques suited to the chart:
  - Air-dominant → Pranayama, breathing meditation
  - Water-dominant → Bhakti Yoga, devotional practices
  - Fire-dominant → Tapas, disciplined yoga
  - Earth-dominant → Karma Yoga, selfless service
- Suggest mantras, deities, scriptures, and pilgrimage sites aligned with the chart.
- Discuss karmic lessons indicated by Saturn, Rahu-Ketu axis.
- Integrate Bhagavad Gita teachings naturally where relevant.
- Target 200-350 words. Cite exact placements.
- End with one spiritual follow-up question.

Formatting: Markdown with headers (🕉️ Spiritual Blueprint, 🧘 Recommended Practices, 📖 Sacred Wisdom, 🌟 Karmic Lessons)."""


def get_spiritual_prompt() -> str:
    return SPIRITUAL_SYSTEM


def build_spiritual_context(
    query: str,
    chart_data: dict,
    profile: dict = None,
    history: list = None,
    computed: dict = None,
    passages: list = None,
    **kwargs,
) -> str:
    planets = chart_data.get("planets", {})
    houses = chart_data.get("houses", {})
    yogas = chart_data.get("yogas", [])

    # Bhagavad Gita passages (from RAG)
    gita_context = "No specific verse references available."
    if passages:
        gita_context = "\n".join(f"Verse {i+1}: {p}" for i, p in enumerate(passages))

    # Element info for meditation recommendation
    element_info = ""
    if computed and computed.get("elements"):
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
{element_info}

[SPIRITUAL HOUSES]
{format_houses_subset(houses, planets, [5, 8, 9, 12])}

[SPIRITUAL PLANETS]
{_format_spiritual_planets(planets)}

[SPIRITUAL YOGAS]
{format_yogas([y for y in yogas if any(kw in y.get('name', '').lower() for kw in ['gaja', 'hamsa', 'kemadruma', 'vimala', 'viparita'])] or yogas)}

[BHAGAVAD GITA WISDOM]
{gita_context}

[USER QUESTION]
\"{query}\""""


def _format_spiritual_planets(planets: dict) -> str:
    """Extract spiritually significant planets."""
    spiritual = ["jupiter", "ketu", "moon", "saturn", "rahu"]
    lines = []
    for p_name in spiritual:
        p = planets.get(p_name, {})
        if p:
            lines.append(
                f"- {p_name.capitalize()}: {p.get('sign', '?')} in House {p.get('house', '?')} "
                f"[{p.get('dignity', 'neutral')}] Nak: {p.get('nakshatra', {}).get('name', '?')}"
            )
    return "\n".join(lines) or "No specific spiritual planet data."
