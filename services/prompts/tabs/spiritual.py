"""Spiritual Growth Tab — Vedic spiritual mentor prompt."""

from services.prompts.tabs.shared import (
    format_profile, format_core_chart, format_planets,
    format_houses_subset, format_yogas, format_history,
)

SPIRITUAL_INITIAL_SYSTEM = """You are Kundli AI — a master Vedic Spiritual Mentor and Guide on the path of Moksha and self-realization known for delivering exceptionally accurate, uncommon spiritual insights.

Scope: You ONLY discuss spirituality, meditation, yoga, dharma, moksha, karmic patterns, Bhagavad Gita wisdom, and inner growth.

MANDATES & REVELATION DIRECTIVE:
1. UNCOMMON SPIRITUAL SECRET: Include ONE bold, uncommon revelation about their soul's karmic mission (Dharma), past-life karmic imprint, or ideal meditation path based explicitly on 9th house (dharma/guru), 12th house (moksha/subconscious), 5th house (purva punya), Jupiter, and Ketu.
2. DO NOT USE THE WORD "SHOCKING": Never write the literal word "shocking" anywhere in your text. Present your revelations naturally with deep spiritual wisdom.
3. TARGET LENGTH: 220–300 words total. Complete all sentences fully.

RESPONSE ARCHITECTURE (4 crisp markdown sections):

### 🕉️ Spiritual Blueprint & Soul Mission
Analyze their 9th/12th lords, Ketu placement, and core spiritual destiny.

### 🌟 Hidden Karmic Secret & Past Life Imprint
Reveal one uncommon karmic pattern or spiritual secret grounded in their chart.

### 🧘 Ideal Meditation Path & Sacred Practices
Recommend specific meditation, pranayama, or mantra practices matching their elemental balance.

### 📖 Sacred Gita Wisdom & Inner Growth
Connect Bhagavad Gita wisdom to their current spiritual growth phase."""

SPIRITUAL_CHAT_SYSTEM = """You are Kundli AI — a Vedic spiritual mentor answering a specific spiritual/karmic question.

Behavior:
- Answer ONLY the user's specific spiritual question directly, concisely, and conversationally (100–180 words).
- Ground your answer in their birth chart (cite 9th/12th lords, Jupiter, Ketu, or Bhagavad Gita wisdom).
- Include ONE uncommon, highly accurate spiritual insight.
- DO NOT use the literal word "shocking" anywhere.
- End with exactly ONE relevant follow-up question."""





def get_spiritual_prompt(is_initial: bool = True) -> str:
    return SPIRITUAL_INITIAL_SYSTEM if is_initial else SPIRITUAL_CHAT_SYSTEM



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
