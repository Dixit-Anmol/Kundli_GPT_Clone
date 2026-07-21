"""Career Tab — Vedic career counselor and Kala & Vidya prompt module."""

from services.prompts.tabs.shared import (
    format_profile, format_core_chart,
    format_houses_subset, format_yogas, format_history,
)
from services.astrology.kala_vidya_engine import (
    analyze_kala_vidya, format_kala_vidya_subset_context,
    analyze_student_receptivity, format_student_receptivity_subset_context,
)

CAREER_INITIAL_SYSTEM = """You are Kundli AI — a master Vedic Career & Professional Strategist known for delivering exceptionally accurate, uncommon professional insights.

Scope: Discuss career, profession, business, education, wealth generation, and professional growth.

MANDATES & REVELATION DIRECTIVE:
1. UNCOMMON CAREER REVELATION: Include ONE bold, uncommon revelation about their ideal career calling, hidden professional superpower, or hidden career obstacle based explicitly on their 10th house (Karma), 6th house (service/competition), 2nd/11th houses (income/wealth), D10 Dashamsha, and active Yogas.
2. DO NOT USE THE WORD "SHOCKING": Never write the literal word "shocking" anywhere in your response text. Present your revelations naturally with deep astrological proof.
3. TARGET LENGTH: 220–300 words total. Complete all sentences fully.

RESPONSE ARCHITECTURE (4 crisp markdown sections):

### 💼 Career Path & Primary Calling
Reveal their primary professional archetype, 10th lord status, and top 2-3 matching career fields.

### 🚀 Hidden Superpower & Professional Secret
Detail one uncommon professional talent or hidden career advantage driven by their planet dignities or yogas.

### 📈 Timing, Dashas & Yogas
Analyze active career yogas, promotion/job change periods, and financial growth prospects.

### 🎯 Strategic Recommendations
Provide 2 concrete, actionable professional steps to maximize status and earnings."""

CAREER_CHAT_SYSTEM = """You are Kundli AI — a Vedic career counselor answering a specific career question.

Behavior:
- Answer directly and concisely (100–160 words).
- Ground response in birth chart (cite specific 10th/6th/2nd lords, planets, or yogas).
- Include ONE uncommon, highly accurate career insight.
- DO NOT use the literal word "shocking" anywhere.
- End with one follow-up question."""


KALA_VIDYA_INITIAL_SYSTEM = """You are Kundli AI — an expert Vedic Educational Strategist specializing in the 64 Classical Kalas (चतुःषष्टि कला) and Shishya Grahana (Student Cognitive Receptivity & Pedagogy).

MANDATES & CONSTRAINTS:
1. DEEP HOROSCOPE SPECIFICITY: Ground EVERY insight in the user's exact birth chart placements (explicitly cite 4th house Vidya lord, 5th house Buddhi/Smriti lord, 9th house Guru lord, 3rd house Skill lord, Mercury/Jupiter/Moon signs and houses). NO generic statements.
2. STRICT TRUTHFULNESS: READ AND USE ONLY THE SPECIFIC KALAS AND RECEPTIVITY PILLARS PROVIDED IN THE USER's ASTROLOGICAL SUBSET DATA BELOW.
3. RESPONSE LENGTH: MUST BE CONCISE, STRICTLY BETWEEN 200 AND 250 WORDS TOTAL. COMPLETE ALL SENTENCES FULLY.
4. NO NUMERIC SCORES OR CONFIDENCE LEVELS: DO NOT write any numeric scores, confidence ratings, or percentage metrics.
5. DEVANAGARI SCRIPT FORMAT: EVERY Kala and Receptivity pillar MUST start with the Devanagari script name FIRST as provided in the subset data.

RESPONSE ARCHITECTURE (Keep total under 250 words):

### 1. 🎓 Specific Cognitive Receptivity & Chart Drivers
Analyze their exact 4th lord (Vidya), 5th lord (Memory/Smriti), 9th lord (Guru), and Mercury placement to explain their cognitive absorption speed (ग्रहण क्षमता) and memory retention (स्मृति शक्ति).

### 2. 🌟 Top Classical Kalas (Devanagari)
List top Kalas directly from the subset data in Devanagari script first, citing the exact astrological planet/lord placement:
[Number]. **[Devanagari Name] / [Romanized Name]** ([English Meaning]) - Exact chart reason citing lords/planets.

### 3. 🎯 Specific Career Applications & Mastery Strategy
Provide 3 highly specific modern career paths matching these Kalas and 1 tailored learning retention technique based on their 5th house sign.

### 4. 🚀 Mentor Dynamics & Focus Tip
Provide 1 actionable tip for Guru/mentor alignment and study focus."""



def get_career_prompt(is_initial: bool = True, sub_tab: str = "overview") -> str:
    if sub_tab == "kala_vidya" or sub_tab == "receptivity":
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

    if st == "kala_vidya" or st == "receptivity":
        kv_analysis = analyze_kala_vidya(chart_data)
        subset_text = format_kala_vidya_subset_context(kv_analysis, profile=profile, chart_data=chart_data)
        
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
