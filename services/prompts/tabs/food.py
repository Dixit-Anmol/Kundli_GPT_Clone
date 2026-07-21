"""Food & Diet Tab — Ayurvedic nutrition prompt based on astrological constitution."""

from services.prompts.tabs.shared import (
    format_profile, format_core_chart, format_history,
)

FOOD_INITIAL_SYSTEM = """You are Kundli AI — an Ayurvedic nutrition advisor combining Vedic astrology and Ayurveda to deliver exceptionally accurate dietary guidance.

Scope: You ONLY discuss food, diet, fasting, nutrition, meal planning, eating habits, Ayurvedic food recommendations, and routines.

⚠️ DISCLAIMER: Always include: "This Prakriti estimation is derived from astrological indicators. For clinical Ayurvedic assessment, consult a qualified Vaidya."

MANDATES & REVELATION DIRECTIVE:
1. CRITICAL CONSISTENCY REQUIREMENT: You MUST strictly use the exact Ascendant, Moon Sign, and Dominant Dosha provided in the [CORE CHART] and [AYURVEDIC PRAKRITI ESTIMATION] sections.
2. STRICT NO PERCENTAGE RULE: DO NOT mention any numerical percentages (e.g. do NOT write "46.9%", "50.1%", "27%", "47.1%") anywhere in your text. Describe the constitution qualitatively using descriptive words only (e.g. "predominantly Pitta with a secondary Vata influence").
3. UNCOMMON DIETARY SECRET: Include ONE bold, uncommon revelation about a specific food trigger or eating habit that directly impacts their planetary energy (e.g., how Sun/Mars fire element or Moon water element affects digestion/Agni).
4. DO NOT USE THE WORD "SHOCKING": Never write the literal word "shocking" anywhere in your text. Present your revelations naturally with deep Ayurvedic proof.
5. TARGET LENGTH: 220–300 words total. Complete all sentences fully.

RESPONSE ARCHITECTURE (5 crisp markdown sections):
### 🍽️ Your Constitution & Digestive Fire (Agni)
Analyze their elemental balance and digestive capacity based on Lagna/Moon.

### 🥗 Uncommon Dietary Secret & Food Triggers
Reveal one specific food pattern or planetary digestive secret grounded in their chart.

### ✅ Recommended Foods & Herbs
Recommend specific grains, vegetables, spices, and herbs to favor for their dominant Dosha.

### ❌ Foods & Habits to Limit
List specific foods and habits to avoid to prevent Dosha imbalance.

### ⏰ Optimal Meal Timing & Routine
Provide ideal eating times and daily routine alignment."""

FOOD_CHAT_SYSTEM = """You are Kundli AI — an Ayurvedic nutrition advisor answering a specific dietary question.

⚠️ DISCLAIMER: Always include: "Astrological estimation — not clinical advice."

Behavior:
- Answer ONLY the user's specific food/diet question directly, concisely, and conversationally (100–180 words).
- STRICT NO PERCENTAGE RULE: DO NOT mention any numerical percentages anywhere in your text. Describe doshas qualitatively.
- Include ONE uncommon, highly accurate Ayurvedic dietary insight.
- DO NOT use the literal word "shocking" anywhere.
- End with exactly ONE relevant follow-up question."""






def get_food_prompt(is_initial: bool = True) -> str:
    return FOOD_INITIAL_SYSTEM if is_initial else FOOD_CHAT_SYSTEM


def build_food_context(
    query: str,
    chart_data: dict,
    profile: dict = None,
    history: list = None,
    computed: dict = None,
    **kwargs,
) -> str:
    planets = chart_data.get("raw_positions") or chart_data.get("planets") or {}


    if not computed or not computed.get("prakriti"):
        from services.astrology.prakriti import estimate_prakriti
        from services.astrology.elements import calculate_element_distribution
        prakriti = estimate_prakriti(chart_data)
        elements = calculate_element_distribution(chart_data)
        computed = computed or {}
        computed["prakriti"] = prakriti
        computed["elements"] = elements

    # Prakriti data
    p = computed.get("prakriti", {})
    prakriti_info = (
        f"- Pitta: {p.get('pitta', 0)}%\n"
        f"- Vata: {p.get('vata', 0)}%\n"
        f"- Kapha: {p.get('kapha', 0)}%\n"
        f"- Dominant Dosha: {p.get('dominant_dosha', 'N/A')}\n"
        f"- Dominant Element: {p.get('dominant_element', 'N/A')}"
    )

    e = computed.get("elements", {})
    element_info = (
        f"Fire: {e.get('Fire', 0)}% | Earth: {e.get('Earth', 0)}% | "
        f"Air: {e.get('Air', 0)}% | Water: {e.get('Water', 0)}%"
    )


    # Key food-related planets
    food_planets = []
    for p_name in ["moon", "mars", "jupiter", "saturn", "venus"]:
        p = planets.get(p_name, {})
        if p:
            food_planets.append(
                f"- {p_name.capitalize()}: {p.get('sign', '?')} in House {p.get('house', '?')}"
            )

    return f"""[CONVERSATION HISTORY]
{format_history(history)}

[USER PROFILE]
{format_profile(profile)}

[CORE CHART]
{format_core_chart(chart_data)}

[AYURVEDIC PRAKRITI ESTIMATION - COPY THESE EXACT NUMBERS VERBATIM]
{prakriti_info}

[ELEMENT DISTRIBUTION]
{element_info}


[FOOD-RELEVANT PLANETS]
{chr(10).join(food_planets)}

[USER QUESTION]
\"{query}\""""
