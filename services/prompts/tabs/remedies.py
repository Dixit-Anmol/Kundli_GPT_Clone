"""Remedies Tab — Personalized Vedic remedies prompt."""

from services.prompts.tabs.shared import (
    format_profile, format_core_chart, format_doshas, format_history,
)

REMEDIES_INITIAL_SYSTEM = """You are Kundli AI — a Vedic remedy specialist and spiritual advisor.

Scope: You ONLY discuss remedies: mantras, gemstones, charity, fasting, color therapy, deity worship, and daily spiritual practices.

Behavior:
- Identify weak planets and prescribe complete remedy kits (Beej mantra, gemstone caveat, charity, fasting, colors, deity).
- Address active Doshas (Manglik, Kaal Sarp, Sade Sati).
- Target 250-350 words. Format with markdown headers (🪐 Weak Planets, 📿 Mantras, 💎 Gemstones, 🙏 Daily Practices, 🕉️ Dosha Remedies).
- End with one remedy-specific follow-up question."""

REMEDIES_CHAT_SYSTEM = """You are Kundli AI — a Vedic remedy specialist answering a specific remedy question.

Behavior:
- Answer ONLY the user's specific remedy question directly, concisely, and conversationally (100–180 words).
- DO NOT use rigid template section headers unless requested.
- Include gemstone caution ("Consult a Jyotish expert before wearing gemstones") if gemstones are mentioned.
- Ground advice directly in their weak planets or chart afflictions.
- End with exactly ONE relevant follow-up question."""




def get_remedies_prompt(is_initial: bool = True) -> str:
    return REMEDIES_INITIAL_SYSTEM if is_initial else REMEDIES_CHAT_SYSTEM



def build_remedies_context(
    query: str,
    chart_data: dict,
    profile: dict = None,
    history: list = None,
    computed: dict = None,
    **kwargs,
) -> str:
    doshas = chart_data.get("doshas", {})

    # Remedy data from pre-computation
    remedy_info = "Not pre-computed. Identify weak planets from the planetary positions below."
    if computed and computed.get("remedy_data"):
        rd = computed["remedy_data"]
        weak = rd.get("weak_planets", [])
        if weak:
            lines = []
            for w in weak:
                p = w["planet"]
                r = w.get("remedies", {})
                mantra = r.get("mantra", {})
                gem = r.get("gemstone", {})
                charity = r.get("charity", {})
                deity = r.get("deity", {})
                lines.append(
                    f"\n--- {p.capitalize()} ({w['status']}) ---\n"
                    f"Beej Mantra: {mantra.get('beej', 'N/A')}\n"
                    f"Jaap Count: {mantra.get('count', 'N/A')}\n"
                    f"Gemstone: {gem.get('primary', 'N/A')} (Alt: {gem.get('alternative', 'N/A')})\n"
                    f"Metal: {gem.get('metal', 'N/A')} | Finger: {gem.get('finger', 'N/A')}\n"
                    f"Charity: {', '.join(charity.get('items', []))} on {charity.get('day', 'N/A')}\n"
                    f"Fasting: {r.get('fasting_day', 'N/A')}\n"
                    f"Colors: {r.get('colors', 'N/A')}\n"
                    f"Deity: {deity.get('deity', 'N/A')} — {deity.get('practice', 'N/A')}"
                )
            remedy_info = "\n".join(lines)
        
        general = rd.get("general_remedies", [])
        if general:
            remedy_info += "\n\n--- Dosha-Specific Remedies ---"
            for g in general:
                remedy_info += f"\n{g['dosha']}: {g['remedy']}"

    # Planet rankings for weakness context
    rankings_info = ""
    if computed and computed.get("planet_rankings"):
        rankings = computed["planet_rankings"]
        weak_list = [r for r in rankings if r["status"] in ("Weak", "Very Weak")]
        if weak_list:
            rankings_info = "\n[PLANET WEAKNESS SUMMARY]\n" + "\n".join(
                f"- {r['planet'].capitalize()}: Score {r['score']} ({r['status']}) — {'; '.join(r.get('reasons', []))}"
                for r in weak_list
            )

    return f"""[CONVERSATION HISTORY]
{format_history(history)}

[USER PROFILE]
{format_profile(profile)}

[CORE CHART]
{format_core_chart(chart_data)}

[DOSHAS]
{format_doshas(doshas)}

[PRE-COMPUTED REMEDY DATA]
{remedy_info}
{rankings_info}

[USER QUESTION]
\"{query}\""""
