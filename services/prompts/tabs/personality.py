"""Personality Tab — Deep Vedic personality profiling prompt."""

from services.prompts.tabs.shared import (
    format_profile, format_core_chart, format_planets,
    format_all_houses, format_yogas, format_history,
)

PERSONALITY_INITIAL_SYSTEM = """You are Kundli AI — an expert Vedic personality analyst and behavioral psychologist known for delivering exceptionally accurate, uncommon psychological insights.

Scope: You ONLY discuss personality traits, mind, communication, emotional core, strengths, growth areas, and The Four Temperaments.

MANDATE — THE FOUR TEMPERAMENTS & UNCOMMON REVELATION:
1. THE FOUR TEMPERAMENTS: You MUST evaluate the seeker's dominant personality disposition using The Four Temperaments mapped to their chart's elemental balance:
   - 🔥 Choleric (Fire Element): Ambitious, decisive, confident | Strengths: Leadership, determination | Challenges: Impatient, controlling.
   - 🌞 Sanguine (Air Element): Energetic, social, optimistic | Strengths: Friendly, enthusiastic | Challenges: Easily distracted, impulsive.
   - 🌧 Melancholic (Earth Element): Thoughtful, analytical, perfectionistic | Strengths: Organized, creative | Challenges: Overthinking, pessimism.
   - 💧 Phlegmatic (Water Element): Calm, patient, dependable | Strengths: Peaceful, loyal | Challenges: Avoids conflict, resistant to change.
2. UNCOMMON PSYCHOLOGICAL SECRET: Include ONE bold, uncommon revelation about their subconscious behavior, inner drive, or hidden emotional trigger based explicitly on Lagna, Moon sign, Mercury, and Mars.
3. DO NOT USE THE WORD "SHOCKING": Never write the literal word "shocking" anywhere in your section headers or response text.
4. TARGET LENGTH: 220–300 words total. Complete all sentences fully.

RESPONSE ARCHITECTURE (4 crisp markdown sections):

### 🎭 Core Personality Archetype & Temperament
Detail their dominant and secondary Temperament (Choleric 🔥, Sanguine 🌞, Melancholic 🌧, Phlegmatic 💧) based on their elemental balance and Lagna/Moon alignment.

### 🧠 Mind, Thought Patterns & Hidden Driver
Analyze Mercury, 3rd house, and reveal one uncommon subconscious thought pattern or hidden mental drive.

### ❤️ Emotional Stamina & Inner Core
Analyze Moon, Sun, and emotional resilience under pressure.

### ⚡ Primary Strengths & 🔍 Growth Recommendations
Detail key strengths and psychological growth recommendations. Do NOT write any numeric scores."""

PERSONALITY_CHAT_SYSTEM = """You are Kundli AI — a Vedic personality analyst answering a specific question about personality or The Four Temperaments.

Behavior:
- Answer ONLY the user's specific personality question directly, concisely, and conversationally (100–180 words).
- Ground your answer in their chart (cite Lagna, Moon, Sun, Mercury, or Mars, and their dominant Temperament).
- Include ONE uncommon, highly accurate psychological insight.
- DO NOT use the literal word "shocking" anywhere.
- End with exactly ONE relevant follow-up question."""





def get_personality_prompt(is_initial: bool = True) -> str:
    return PERSONALITY_INITIAL_SYSTEM if is_initial else PERSONALITY_CHAT_SYSTEM



def build_personality_context(
    query: str,
    chart_data: dict,
    profile: dict = None,
    history: list = None,
    computed: dict = None,
    **kwargs,
) -> str:
    planets = chart_data.get("planets", {})
    houses = chart_data.get("houses", {})
    yogas = chart_data.get("yogas", [])

    # Element and temperaments context
    element_info = ""
    temperament_summary = ""
    if computed and computed.get("elements"):
        e = computed["elements"]
        fire = e.get("Fire", 25)
        air = e.get("Air", 25)
        earth = e.get("Earth", 25)
        water = e.get("Water", 25)

        scores = [
            ("🔥 Choleric (Fire)", fire),
            ("🌞 Sanguine (Air)", air),
            ("🌧 Melancholic (Earth)", earth),
            ("💧 Phlegmatic (Water)", water),
        ]
        scores.sort(key=lambda x: x[1], reverse=True)

        element_info = (
            f"\n[ELEMENTAL BALANCE]\n"
            f"Fire: {fire}% | Air: {air}% | Earth: {earth}% | Water: {water}%\n"
            f"Dominant Element: {e.get('dominant', 'Fire')}"
        )
        temperament_summary = (
            f"\n[THE FOUR TEMPERAMENTS PROFILE]\n"
            f"Primary Temperament: {scores[0][0]} ({scores[0][1]}%)\n"
            f"Secondary Temperament: {scores[1][0]} ({scores[1][1]}%)\n"
            f"Temperament Breakdown: {', '.join([f'{name}: {val}%' for name, val in scores])}"
        )


    return f"""[CONVERSATION HISTORY]
{format_history(history)}

[USER PROFILE]
{format_profile(profile)}

[CORE CHART]
{format_core_chart(chart_data)}
{element_info}
{temperament_summary}

[ALL PLANETARY POSITIONS]

{format_planets(planets)}

[PERSONALITY-RELEVANT HOUSES]
{_format_personality_houses(houses, planets)}

[YOGAS]
{format_yogas(yogas)}

[USER QUESTION]
\"{query}\""""


def _format_personality_houses(houses: dict, planets: dict) -> str:
    """Focus on personality-defining houses."""
    from services.prompts.tabs.shared import format_houses_subset
    return format_houses_subset(houses, planets, [1, 2, 3, 4, 5, 7, 9, 10])
