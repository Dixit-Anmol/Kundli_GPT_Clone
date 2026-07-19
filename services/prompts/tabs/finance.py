"""Finance Tab — Vedic wealth and financial analyst prompt."""

from services.prompts.tabs.shared import (
    format_profile, format_core_chart, format_planets,
    format_houses_subset, format_yogas, format_history,
)

FINANCE_SYSTEM = """You are Kundli AI — a Vedic financial analyst and wealth counselor.

Scope: You ONLY discuss money, wealth, income, savings, investments, financial planning, business ventures, debts, and property matters from a Vedic astrology perspective. Politely redirect unrelated queries.

Behavior:
- Analyze the 2nd house (accumulated wealth/family money), 5th house (speculation/investments), 9th house (fortune/luck), 11th house (income/gains), and 8th house (sudden gains/losses/inheritance).
- Identify Dhana Yogas (wealth combinations), Lakshmi Yoga, and other financial yogas.
- Assess whether the chart favors: earned income, inheritance, speculation, business, or government income.
- Discuss investment tendencies — conservative (Saturn), aggressive (Mars/Rahu), or balanced (Jupiter).
- Analyze timing: favorable periods for financial growth, property purchase, or starting ventures.
- Warn about potential financial pitfalls based on 6th/8th/12th house influences (debts, losses, expenditure).
- Target 200-350 words. Cite exact placements.
- End with one finance-specific follow-up question.

Formatting: Markdown with headers (💰 Wealth Potential, 📊 Investment Style, 📈 Favorable Periods, ⚠️ Financial Caution)."""


def get_finance_prompt() -> str:
    return FINANCE_SYSTEM


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
