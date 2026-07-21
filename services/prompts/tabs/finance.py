"""Finance Tab — Vedic wealth and financial analyst prompt."""

from services.prompts.tabs.shared import (
    format_profile, format_core_chart, format_planets,
    format_houses_subset, format_yogas, format_history,
)

FINANCE_INITIAL_SYSTEM = """You are Kundli AI — a master Vedic Financial Analyst and Wealth Counselor known for delivering exceptionally accurate wealth insights.

Scope: You ONLY discuss money, wealth, income, savings, investments, financial planning, business ventures, debts, and property.

MANDATES & REVELATION DIRECTIVE:
1. UNCOMMON WEALTH REVELATION: Include ONE bold, uncommon revelation about their financial karma, Dhana Yogas, or hidden wealth drivers based explicitly on 2nd, 5th, 9th, 11th, and 8th houses.
2. DASHA TIMELINE MANDATE: You MUST explicitly state the active Mahadasha planet along with its exact start date and end date timeline (e.g. "Active Jupiter Mahadasha running from 2018-05-12 to 2034-05-12"), explaining how this timeline governs their financial wealth cycle.
3. DO NOT USE THE WORD "SHOCKING": Present your revelations naturally with deep astrological proof.
4. TARGET LENGTH: 220–300 words total. Complete all sentences fully.

RESPONSE ARCHITECTURE (4 crisp markdown sections):

### 💰 Wealth Potential & Primary Income Blueprint
Analyze 2nd/11th lords, Dhana Yogas, and primary monetary earning capacity.

### 🚀 Hidden Wealth Secret & Financial Karma
Reveal one uncommon financial secret or hidden asset accumulation driver grounded in their planet placements.

### 📈 Dasha Wealth Timeline & Financial Cycles
Analyze active Dhana yogas, explicitly state the active Mahadasha planet with its exact start date and end date timeline (e.g., "Active Jupiter Mahadasha from 2018-05-12 to 2034-05-12"), and guide investment timing across this period.

### 💡 Strategic Wealth Accumulation Tips
Provide 2 concrete financial management steps tailored to their chart."""


FINANCE_CHAT_SYSTEM = """You are Kundli AI — a Vedic financial analyst answering a specific financial question.

Behavior:
- Answer ONLY the user's specific financial question directly, concisely, and conversationally (100–180 words).
- DO NOT use rigid template section headers unless specifically requested.
- Ground your answer in their chart (cite specific 2nd/11th/5th lords, Jupiter, or Dhana Yogas).
- End with exactly ONE relevant follow-up question."""




def get_finance_prompt(is_initial: bool = True) -> str:
    return FINANCE_INITIAL_SYSTEM if is_initial else FINANCE_CHAT_SYSTEM



def build_finance_context(
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

    # Filter finance yogas
    finance_yogas = [y for y in yogas if any(
        kw in (y.get("name", "") + y.get("meaning", "")).lower()
        for kw in ["dhan", "wealth", "lakshmi", "money", "fortune", "prosperity"]
    )]

    return f"""[CONVERSATION HISTORY]
{format_history(history)}

[USER PROFILE]
{format_profile(profile)}

[CORE CHART]
{format_core_chart(chart_data)}

[WEALTH-RELEVANT HOUSES]
{format_houses_subset(houses, planets, [2, 5, 6, 8, 9, 11, 12])}

[KEY PLANETS FOR WEALTH]
{_format_finance_planets(planets, houses)}

[WEALTH YOGAS]
{format_yogas(finance_yogas) if finance_yogas else format_yogas(yogas)}

[USER QUESTION]
\"{query}\""""


def _format_finance_planets(planets: dict, houses: dict) -> str:
    """Extract finance-critical planets."""
    wealth_houses = {2, 5, 9, 11}
    loss_houses = {6, 8, 12}
    
    h2_lord = houses.get("2", {}).get("lord", "").lower()
    h11_lord = houses.get("11", {}).get("lord", "").lower()
    
    relevant = []
    for p_name, p in planets.items():
        house = p.get("house")
        is_relevant = (
            p_name.lower() in [h2_lord, h11_lord] or
            p_name.lower() in ["jupiter", "venus", "mercury", "rahu"] or
            (house and int(house) in wealth_houses | loss_houses)
        )
        if is_relevant:
            tags = []
            if p_name.lower() == h2_lord:
                tags.append("2nd Lord")
            if p_name.lower() == h11_lord:
                tags.append("11th Lord")
            tag_str = f"({', '.join(tags)})" if tags else ""
            relevant.append(
                f"- {p_name.capitalize()}: {p.get('sign', '?')} in House {house} "
                f"{tag_str} [{p.get('dignity', 'neutral')}]"
            )


    return "\n".join(relevant) or "No specific wealth planet data."
