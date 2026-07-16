import datetime

DASHA_ORDER = ["ketu", "venus", "sun", "moon", "mars", "rahu", "jupiter", "saturn", "mercury"]

DASHA_YEARS = {
    "ketu": 7,
    "venus": 20,
    "sun": 6,
    "moon": 10,
    "mars": 7,
    "rahu": 18,
    "jupiter": 16,
    "saturn": 19,
    "mercury": 17
}

def calculate_vimshottari_dasha(moon_longitude: float, birth_date: datetime.date) -> list:
    """Calculate the Vimshottari Dasha periods starting from birth date based on Moon's longitude."""
    nak_width = 360.0 / 27.0
    nak_idx = int(moon_longitude // nak_width)
    
    # Starting nakshatra details
    start_long = nak_idx * nak_width
    progress = (moon_longitude - start_long) / nak_width # Progress fraction through current Nakshatra
    
    # The starting planet in the dasha cycle is the lord of the Moon's Nakshatra
    # The Nakshatra array starts with Ashwini (ruled by Ketu)
    # The order of nakshatras matches the DASHA_ORDER (cycle repeating 3 times: 27 total)
    start_lord_idx = nak_idx % 9
    start_lord = DASHA_ORDER[start_lord_idx]
    
    # Remaining years in the first Mahadasha at birth
    start_lord_years = DASHA_YEARS[start_lord]
    years_remaining = start_lord_years * (1.0 - progress)
    
    # Build dasha timeline starting from birth date
    current_date = birth_date
    timeline = []
    
    # Add first dasha (partially completed)
    days_remaining = int(years_remaining * 365.25)
    end_date = current_date + datetime.timedelta(days=days_remaining)
    timeline.append({
        "planet": start_lord,
        "start": current_date.isoformat(),
        "end": end_date.isoformat(),
        "duration_years": round(years_remaining, 2)
    })
    current_date = end_date
    
    # Calculate subsequent dashas for the rest of a 120-year cycle
    curr_lord_idx = (start_lord_idx + 1) % 9
    for _ in range(9):
        lord = DASHA_ORDER[curr_lord_idx]
        years = DASHA_YEARS[lord]
        days = int(years * 365.25)
        end_date = current_date + datetime.timedelta(days=days)
        timeline.append({
            "planet": lord,
            "start": current_date.isoformat(),
            "end": end_date.isoformat(),
            "duration_years": years
        })
        current_date = end_date
        curr_lord_idx = (curr_lord_idx + 1) % 9
        
    return timeline

def get_current_dasha(timeline: list, query_date: datetime.date) -> dict:
    """Find the active Mahadasha planet on a given query date."""
    query_iso = query_date.isoformat()
    for period in timeline:
        if period["start"] <= query_iso <= period["end"]:
            return period
    return timeline[-1] # Fallback to last if beyond 120 years
