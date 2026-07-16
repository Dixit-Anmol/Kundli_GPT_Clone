from services.prompts.geeta import assemble_unified_prompt

def build_horoscope_prompt(name: str, chart_data: dict, profile: dict = None) -> str:
    """Build the raw prompt to interpret the birth chart context (Step 3)."""
    prof = profile or {
        "name": name,
        "date_of_birth": "N/A",
        "time_of_birth": "N/A",
        "latitude": 0.0,
        "longitude": 0.0,
        "timezone_offset": 5.5
    }
    
    # We pass the default query for chart analysis
    return assemble_unified_prompt(
        query="Analyze my birth chart and explain my placements.",
        chart_data=chart_data,
        profile=prof,
        history=[],
        passages=[],
        intent="Astrology Explanation"
    )
