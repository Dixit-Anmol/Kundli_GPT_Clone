"""Health Tab — Vedic health analyst prompt."""

from services.prompts.tabs.shared import (
    format_profile, format_core_chart, format_planets,
    format_houses_subset, format_doshas, format_history, format_dasha_info,
)

HEALTH_INITIAL_SYSTEM = """You are Kundli AI — a Vedic health analyst combining Jyotish and Ayurveda.

Scope: You ONLY discuss health, constitution, disease tendencies, physical vitality, organ vulnerability, mental wellbeing, immunity, and recovery.

⚠️ DISCLAIMER: Always include at the end: "This is an astrological estimation — not a medical diagnosis. Always consult qualified healthcare professionals for medical concerns."

MANDATES & REVELATION DIRECTIVE (DO NOT CHANGE PROMPT STRUCTURE):
1. HIGHLY SPECIFIC ORGAN VULNERABILITY PREDICTIONS: Ground every health claim in specific planetary body mappings, Lagna lord strength, 6th lord (immunity/disease), and 8th lord (chronic stress). Predict SPECIFIC organ/system sensitivities (e.g. digestive inflammation/acid reflux via Mars/Pitta, joint stiffness/bone weakness via Saturn/Vata, cardiac/eye sensitivity via Sun, nervous system/sleep imbalance via Moon/12th house).
2. HIGHLY SPECIFIC DASHA TIMELINE VULNERABILITIES: You MUST cite the active Mahadasha planet with its exact start date and end date timeline (e.g. "Active Saturn Mahadasha running from 2020-03-15 to 2039-03-15"), explaining WHICH specific periods within this timeline require heightened immunity care.
3. STRICT NO PERCENTAGE RULE: DO NOT write any numerical percentages in your text response. Describe doshas qualitatively using descriptive words only (e.g. "predominantly Pitta with Vata influence").
4. TARGET LENGTH: 220–320 words total. Format with the exact 5 markdown headers.

RESPONSE ARCHITECTURE (Preserve exact 5 markdown sections):

### 🏥 Health Profile
Explain overall physical stamina, Lagna lord strength, active Mahadasha timeline dates (start and end), and primary Ayurvedic dosha constitution.

### 🧠 Mental Wellbeing
Analyze mental peace, sleep quality, nervous system sensitivity, and subconscious stress triggers based on Moon sign and 12th house placements.

### 💪 Strengths
Highlight their top 2 astrological physical strengths, strong organ resilience, and natural immunity buffers.

### ⚠️ Vulnerable Areas
Detail primary physical vulnerability, specific organ stress points, and planetary reasons driven by 6th/8th lords or afflicted planets.

### 🌿 Ayurvedic Tips
Provide 2 highly specific daily Ayurvedic routine steps, dietary habits, and herbs tailored to their planetary constitution and active Dasha."""

HEALTH_CHAT_SYSTEM = """You are Kundli AI — a Vedic health analyst answering a specific health query.

⚠️ DISCLAIMER: Always include: "Astrological estimation — not medical advice."

Behavior:
- Answer ONLY the user's specific health/wellness question directly, concisely, and conversationally (100–180 words).
- Ground answer in specific organ vulnerabilities (e.g. digestion, joints, nervous system), 1st/6th/8th lords, active Dasha dates, and planets.
- STRICT NO PERCENTAGE RULE: DO NOT write any numerical percentages in your response text.
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

    dasha_timeline = format_dasha_info(chart_data)

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

[ACTIVE HEALTH DASHA TIMELINE]
{dasha_timeline}

[HEALTH-RELEVANT HOUSES]
{format_houses_subset(houses, planets, [1, 6, 8, 12, 4])}

[HEALTH-CRITICAL PLANETS & ORGAN MAPPINGS]
{_format_health_planets(planets, houses)}

[AYURVEDIC PRAKRITI ESTIMATION]
{prakriti_info}

[DOSHAS]
{format_doshas(doshas)}

[USER QUESTION]
\"{query}\""""


def _format_health_planets(planets: dict, houses: dict) -> str:
    """Extract health-critical planets with specific organ body mappings."""
    organ_mappings = {
        "sun": "Heart, Sight/Eyes, Bones, Vital Power, Head",
        "moon": "Mind, Blood Circulation, Sleep Rhythm, Lungs, Fluids",
        "mars": "Blood Vessels, Muscles, Liver, Digestive Fire/Agni, Inflammatory Triggers",
        "mercury": "Nervous System, Respiratory Tract, Skin, Intestines, Speech",
        "jupiter": "Liver, Gallbladder, Pancreas, Thighs, Fat Metabolism",
        "venus": "Kidneys, Reproductive System, Hormonal Balance, Throat/Skin",
        "saturn": "Joints, Knees, Bones, Teeth, Chronic Weakness, Digestion Slowdown",
        "rahu": "Mysterious Ailments, Allergies, Nervous Anxieties, Toxic Outflows",
        "ketu": "Nerve Receptors, Diagnostic Ambiguity, Skin Sensitivities, Spasms"
    }

    health_houses = {1, 4, 6, 8, 12}
    relevant = []
    for p_name, p in planets.items():
        house = p.get("house")
        if house and int(house) in health_houses:
            mapping = organ_mappings.get(p_name.lower(), "Physical System")
            relevant.append(
                f"- {p_name.capitalize()}: {p.get('sign', '?')} in House {house} "
                f"[{p.get('dignity', 'neutral')}] — Body System: {mapping}"
            )
    # Always include Sun and Moon
    for key_planet in ["sun", "moon"]:
        if key_planet in planets and not any(key_planet in r for r in relevant):
            p = planets[key_planet]
            mapping = organ_mappings.get(key_planet.lower(), "Core Vitality")
            relevant.append(
                f"- {key_planet.capitalize()}: {p.get('sign', '?')} in House {p.get('house', '?')} "
                f"[{p.get('dignity', 'neutral')}] — Body System: {mapping}"
            )
    return "\n".join(relevant) or "No specific health planet data."
