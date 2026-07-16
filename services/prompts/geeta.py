GEETA_PROMPT_TEMPLATE = """You are counseling {name} who is seeking spiritual guidance based on the Bhagavad Gita and their Vedic Horoscope.

[User's Spiritual Seeking]
"{query}"

[User's Birth Chart Summary]
- Ascendant: {asc_sign}
- Moon Sign: {moon_sign}
- Nakshatra: {nakshatra}
- Active Yogas: {yogas}
- Active Doshas: {doshas}

[Relevant Bhagavad Gita Teachings & Verses]
{gita_passages}

Please reply to the user using the structured, conversational guidelines defined in your system instructions. Do NOT repeat their full horoscope coordinates. Answer their query directly, refer briefly to their placements or the Gita if relevant, provide practical recommendations in bullet points, and end with one short follow-up question.
"""

def build_geeta_prompt(name: str, query: str, chart_data: dict, passages: list) -> str:
    """Build prompt combining RAG passages, user query, and horoscope context (Step 3)."""
    meta = chart_data.get("metadata", {})
    yogas = ", ".join([y["name"] for y in chart_data.get("yogas", [])]) or "None"
    
    doshas_active = []
    for d_name, d_val in chart_data.get("doshas", {}).items():
        if d_val.get("is_present"):
            doshas_active.append(d_name.capitalize())
    doshas_formatted = ", ".join(doshas_active) or "None"
    
    gita_passages = ""
    for idx, passg in enumerate(passages):
        gita_passages += f"Verse Reference {idx+1}:\n{passg}\n\n"
        
    if not gita_passages:
        gita_passages = "No specific verse references available. Use general teachings of Karma Yoga and Self-Realization."
        
    prompt = GEETA_PROMPT_TEMPLATE.format(
        name=name,
        query=query,
        asc_sign=meta.get("ascendant_sign", "Aries"),
        moon_sign=meta.get("moon_sign", "Cancer"),
        nakshatra=meta.get("nakshatra", "Pushya"),
        yogas=yogas,
        doshas=doshas_formatted,
        gita_passages=gita_passages
    )
    
    return prompt
