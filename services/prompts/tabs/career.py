"""Career Tab — Vedic career counselor and Kala & Vidya prompt module."""

from services.prompts.tabs.shared import (
    format_profile, format_core_chart,
    format_houses_subset, format_yogas, format_history,
)
from services.astrology.kala_vidya_engine import analyze_kala_vidya, format_kala_vidya_subset_context

CAREER_INITIAL_SYSTEM = """You are Kundli AI — a Vedic career counselor and professional strategist.

Scope: Discuss career, profession, business, education, and professional growth.
Behavior:
- Analyze 10th, 6th, 2nd, 11th houses and D10 Dashamsha.
- Suggest 2-3 specific career fields matching the chart.
- Target 180-250 words total. Format with headers: 💼 Career Path, 📈 Timing & Yogas, 🎯 Recommendations.
- End with one follow-up question."""

CAREER_CHAT_SYSTEM = """You are Kundli AI — a Vedic career counselor answering a specific career question.

Behavior:
- Answer directly and concisely (100–150 words).
- Ground response in birth chart (cite specific 10th/6th/2nd lords, planets, or yogas).
- End with one follow-up question."""

KALA_VIDYA_INITIAL_SYSTEM = """You are Kundli AI — an expert Vedic Astrologer specializing in the 64 Classical Kalas (चतुःषष्टि कला).

MANDATES & CONSTRAINTS:
1. STRICT TRUTHFULNESS: READ AND USE ONLY THE SPECIFIC KALAS PROVIDED IN THE USER's ASTROLOGICAL SUBSET DATA BELOW. DO NOT INVENT OR PREDICT ANY UNLISTED KALAS.
2. RESPONSE LENGTH: MUST BE CONCISE, STRICTLY BETWEEN 180 AND 250 WORDS TOTAL. COMPLETE ALL SENTENCES FULLY.
3. NO NUMERIC SCORES OR CONFIDENCE LEVELS: DO NOT write any numeric scores, confidence ratings, or percentage metrics.
4. DEVANAGARI SCRIPT FORMAT: In Section 2, EVERY item MUST start with the Devanagari script name FIRST as provided in the subset data, followed by Romanized Sanskrit name and English meaning.

RESPONSE ARCHITECTURE (Keep total under 250 words):

### 1. 🎓 Core Archetype
1-2 sentences summarizing the user's dominant talent archetype.

### 2. 🌟 Top Classical Kalas (Devanagari)
List the top Kalas from the provided astrological subset. Format each line strictly as:
[Number]. **[Devanagari Name] / [Romanized Name]** ([English Meaning]) - 1 short sentence astrological reason.

### 3. 🎯 Career Alignment & Key Skills
List 3 matching modern career roles and 3 core practical skills.

### 4. 🚀 Growth Advice
1 practical growth tip based on the horoscope."""



def get_career_prompt(is_initial: bool = True, sub_tab: str = "overview") -> str:
    if sub_tab == "kala_vidya":
        return KALA_VIDYA_INITIAL_SYSTEM if is_initial else CAREER_CHAT_SYSTEM
    return CAREER_INITIAL_SYSTEM if is_initial else CAREER_CHAT_SYSTEM


def build_career_context(
    query: str,
    chart_data: dict,
    profile: dict = None,
    history: list = None,
    computed: dict = None,
    sub_tab: str = "overview",
    **kwargs,
) -> str:
    st = kwargs.get("sub_tab") or sub_tab or "overview"

    hist_str = format_history(history)
    hist_part = f"[CONVERSATION HISTORY]\n{hist_str}\n\n" if hist_str and hist_str != "No previous conversation." else ""

    if st == "kala_vidya":
        kv_analysis = analyze_kala_vidya(chart_data)
        subset_text = format_kala_vidya_subset_context(kv_analysis, profile=profile)
        
        return f"""{hist_part}[USER PROFILE]
{format_profile(profile)}

{subset_text}

[USER QUERY]
"{query}" """

    # Default Career Overview
    planets = chart_data.get("planets", {})
    houses = chart_data.get("houses", {})
    yogas = chart_data.get("yogas", [])

    career_yogas = [y for y in yogas if any(
        kw in (y.get("name", "") + y.get("type", "")).lower()
        for kw in ["raj", "dharma", "karma", "wealth", "dhan", "profession"]
    )]

    return f"""{hist_part}[USER PROFILE]
{format_profile(profile)}

[CORE CHART]
{format_core_chart(chart_data)}

[CAREER HOUSES]
{format_houses_subset(houses, planets, [2, 6, 10, 11])}

[KEY PLANETS]
{_format_career_planets(planets, houses)}

[YOGAS]
{format_yogas(career_yogas[:3]) if career_yogas else format_yogas(yogas[:3])}

[QUERY]
"{query}" """


def _format_career_planets(planets: dict, houses: dict) -> str:
    """Extract career-critical planet placements efficiently."""
    career_planets = []
    h10 = houses.get("10", {})
    lord_10 = h10.get("lord", "").lower()
    
    for p_name, p in planets.items():
        is_relevant = (
            p_name.lower() == lord_10 or
            p.get("house") in [2, 6, 10, 11] or
            p_name.lower() in ["sun", "saturn", "jupiter", "mercury"]
        )
        if is_relevant:
            career_planets.append(
                f"- {p_name.capitalize()}: {p.get('sign', '?')} in H{p.get('house', '?')} "
                f"({'[10th Lord]' if p_name.lower() == lord_10 else ''}) "
                f"[{p.get('dignity', 'neutral')}]"
            )
    return "\n".join(career_planets[:5]) or "No specific planet data."
