import json

HOROSCOPE_PROMPT_TEMPLATE = """You are analyzing the Vedic Birth Chart (Kundli) of {name}.
Here are the astronomical details of their chart:

[Ascendant (Lagna)]
Sign: {asc_sign}
Longitude: {asc_long:.2f}°

[Planetary Positions]
{planets_formatted}

[Whole Sign House Meanings & Lords]
{houses_formatted}

[Active Vedic Yogas]
{yogas_formatted}

[Afflictions (Doshas)]
- Manglik Dosha: {manglik_status} ({manglik_desc})
- Kaal Sarp Dosha: {kaalsarp_status} ({kaalsarp_desc})
- Sade Sati: {sadesati_status} ({sadesati_desc})

Please write a concise, conversational, and encouraging initial Vedic birth chart analysis.
Focus on identifying the top 3 dominant characteristics of their chart (e.g. based on Ascendant, Moon Sign, or Yogas), list them in clean bullet points with brief explanations, and summarize any active Doshas or remedies briefly.

Do NOT write a long essay. Keep the entire response under 350 words.
Greet them warmly on this first message (e.g., "Namaste {name}! 🙏 Let's explore your horoscope together.").
At the end, ask a single follow-up question about whether they want to dive into their career, relationships, or spiritual path.
"""

def build_horoscope_prompt(name: str, chart_data: dict) -> str:
    """Build the raw prompt to interpret the birth chart context (Step 3)."""
    meta = chart_data.get("metadata", {})
    planets = chart_data.get("planets", {})
    houses = chart_data.get("houses", {})
    yogas = chart_data.get("yogas", [])
    doshas = chart_data.get("doshas", {})
    
    # Format planets
    planets_formatted = ""
    for name_key, p in planets.items():
        planets_formatted += (
            f"- {p['name_sanskrit']} ({name_key.capitalize()}): placed in {p['sign']} "
            + f"({p['degree']:.2f}°) in House {p['house']} [Dignity: {p['dignity']}]\n"
        )
        
    # Format houses
    houses_formatted = ""
    for h_num, h in houses.items():
        houses_formatted += f"- House {h_num} ({h['sign']}, ruled by {h['lord'].capitalize()}): {h['signification']}\n"
        
    # Format Yogas
    if yogas:
        yogas_formatted = "\n".join([f"- {y['name']} ({y['type']}): {y['meaning']}" for y in yogas])
    else:
        yogas_formatted = "None detected."
        
    # Format Doshas
    manglik = doshas.get("manglik", {})
    kaalsarp = doshas.get("kaal_sarp", {})
    sadesati = doshas.get("sade_sati", {})
    
    prompt = HOROSCOPE_PROMPT_TEMPLATE.format(
        name=name,
        asc_sign=meta.get("ascendant_sign", "Aries"),
        asc_long=meta.get("ascendant_longitude", 0.0),
        planets_formatted=planets_formatted,
        houses_formatted=houses_formatted,
        yogas_formatted=yogas_formatted,
        manglik_status="Active" if manglik.get("is_present") else "Not Present",
        manglik_desc=manglik.get("description", ""),
        kaalsarp_status="Active" if kaalsarp.get("is_present") else "Not Present",
        kaalsarp_desc=kaalsarp.get("description", ""),
        sadesati_status="Active" if sadesati.get("is_present") else "Not Present",
        sadesati_desc=sadesati.get("description", "")
    )
    
    return prompt
