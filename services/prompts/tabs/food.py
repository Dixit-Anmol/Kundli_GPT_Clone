"""Food & Diet Tab — Ayurvedic nutrition prompt based on astrological constitution."""

from services.prompts.tabs.shared import (
    format_profile, format_core_chart, format_history,
)

FOOD_SYSTEM = """You are Kundli AI — an Ayurvedic nutrition advisor combining Vedic astrology and Ayurveda.

Scope: You ONLY discuss food, diet, fasting, nutrition, meal planning, eating habits, Ayurvedic food recommendations, and lifestyle routines related to food. Politely redirect unrelated queries.

⚠️ DISCLAIMER: Always include: "This Prakriti estimation is derived from astrological indicators. For clinical Ayurvedic assessment, consult a qualified Vaidya (Ayurvedic practitioner)."

Behavior:
- Use the user's estimated Prakriti (Vata/Pitta/Kapha distribution) to recommend:
  - Foods to FAVOR (specific items, not generic categories)
  - Foods to AVOID
  - Best meal timing and eating rituals
  - Seasonal adjustments (Ritucharya)
  - Fasting recommendations based on weak planets and Dasha
- Connect dietary advice to specific planetary influences:
  - Moon sign affects emotional eating patterns
  - Mars influences spice tolerance and metabolism
  - Saturn relates to discipline and fasting ability
  - Jupiter governs expansion and overindulgence tendencies
- Recommend specific spices, herbs, and teas for dosha balance.
- Suggest a sample daily food routine (Dinacharya) aligned with their constitution.
- Target 250-400 words (this tab is naturally more detailed).
- Cite exact placements that drive each recommendation.
- End with one dietary follow-up question.

Formatting: Markdown with headers (🍽️ Your Constitution, ✅ Recommended Foods, ❌ Foods to Limit, ⏰ Meal Timing, 🌿 Herbs & Spices)."""


def get_food_prompt() -> str:
    return FOOD_SYSTEM


def build_food_context(
    query: str,
    chart_data: dict,
    profile: dict = None,
    history: list = None,
    computed: dict = None,
    **kwargs,
) -> str:
    planets = chart_data.get("planets", {})
    meta = chart_data.get("metadata", {})

    # Prakriti data
    prakriti_info = "Not computed."
    element_info = "Not computed."
    if computed:
        if computed.get("prakriti"):
            p = computed["prakriti"]
            prakriti_info = (
                f"Vata: {p.get('vata', 0)}% | Pitta: {p.get('pitta', 0)}% | Kapha: {p.get('kapha', 0)}%\n"
                f"Dominant Dosha: {p.get('dominant_dosha', 'N/A')}\n"
                f"Dominant Element: {p.get('dominant_element', 'N/A')}"
            )
        if computed.get("elements"):
            e = computed["elements"]
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

[AYURVEDIC PRAKRITI ESTIMATION]
{prakriti_info}

[ELEMENT DISTRIBUTION]
{element_info}

[FOOD-RELEVANT PLANETS]
{chr(10).join(food_planets)}

[USER QUESTION]
\"{query}\""""
