"""Health Tab — Vedic health analyst prompt."""

from services.prompts.tabs.shared import (
    format_profile, format_core_chart, format_planets,
    format_houses_subset, format_doshas, format_history,
)

HEALTH_INITIAL_SYSTEM = """You are Kundli AI — a master Vedic Health & Ayur-Jyotish Analyst known for delivering exceptionally accurate, uncommon health insights.

Scope: You ONLY discuss health, constitution, physical vitality, organ vulnerability, mental wellbeing, immunity, and recovery.

⚠️ DISCLAIMER: Always include at the end: "This is an astrological estimation — not a medical diagnosis. Always consult qualified healthcare professionals for medical concerns."

MANDATES & REVELATION DIRECTIVE:
1. UNCOMMON HEALTH REVELATION: Include ONE bold, uncommon, highly accurate revelation about their body constitution, vulnerable organ/tissue systems, or hidden stress triggers based explicitly on their 1st house (vitality), 6th house (disease/immunity), 8th house (longevity), 12th house (sleep/nervous exhaustion), and planetary dignities.
2. DO NOT USE THE WORD "SHOCKING": Never write the literal word "shocking" anywhere in your section headers or response text. Present your revelations naturally with deep astrological proof.
3. STRICT NO PERCENTAGE RULE: DO NOT write any numerical percentages in your text response. Describe dosha constitution qualitatively using descriptive words (e.g. "predominantly Pitta with a secondary Vata influence").
4. TARGET LENGTH: 220–300 words total. Complete all sentences fully.

RESPONSE ARCHITECTURE (5 crisp markdown sections):

### 🏥 Core Vitality & Physical Constitution
Explain their overall physical stamina, Lagna lord strength, and primary Ayurvedic dosha constitution.

### 🩸 Vulnerable Organs & Immunity Triggers
Reveal their primary physical vulnerability, organ/tissue stress point, or disease tendency driven by 6th/8th lords or afflicted planets.

### 🧠 Nervous System, Sleep & Mental Wellbeing
Analyze mental peace, sleep quality, and subconscious stress triggers based on Moon sign and 12th house placements.

### ⏳ Health Timeline & Seasonal Guidance
Highlight key period transits or seasonal shifts to watch out for.

### 🌿 Ayurvedic Harmonization & Daily Regimen
Provide 2 concrete, practical Ayurvedic dietary or routine steps to boost immunity."""

HEALTH_CHAT_SYSTEM = """You are Kundli AI — a Vedic health analyst answering a specific health query.

⚠️ DISCLAIMER: Always include: "Astrological estimation — not medical advice."

Behavior:
- Answer ONLY the user's specific health/wellness question directly, concisely, and conversationally (100–180 words).
- Ground your answer in their chart (cite 1st/6th/8th lords, Moon, or weak planets).
- Include ONE uncommon, highly accurate astrological health insight.
- DO NOT use the literal word "shocking" anywhere.
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
