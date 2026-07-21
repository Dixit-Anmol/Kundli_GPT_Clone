"""
Planet Strength Ranking Module.

Ranks all 9 planets by overall functional strength using:
- Dignity (exalted/own/debilitated/enemy)
- House placement quality (Kendra/Trikona = strong, Dusthana = weak)
- Yoga participation count
- Retrograde/combustion status
"""

# House quality categories
KENDRA_HOUSES = {1, 4, 7, 10}     # Strongest angular houses
TRIKONA_HOUSES = {1, 5, 9}         # Trinal houses (dharma)
UPACHAYA_HOUSES = {3, 6, 10, 11}   # Growth houses
DUSTHANA_HOUSES = {6, 8, 12}       # Difficult houses
MARAKA_HOUSES = {2, 7}             # Death-inflicting houses

# Dignity scores
DIGNITY_SCORES = {
    "exalted": 5.0,
    "own sign": 4.0,
    "own": 4.0,
    "moolatrikona": 4.5,
    "friend": 3.0,
    "friendly": 3.0,
    "neutral": 2.0,
    "enemy": 1.0,
    "debilitated": 0.5,
}


def rank_planets(chart_data: dict) -> list:
    """
    Rank all planets by composite functional strength.
    
    Returns a sorted list of dicts:
    [
        {"planet": "jupiter", "score": 8.5, "rank": 1, "status": "Strong", "reason": "..."},
        ...
    ]
    """
    planets = chart_data.get("raw_positions") or chart_data.get("planets") or {}

    yogas = chart_data.get("yogas", [])
    
    # Count yoga participation per planet
    yoga_participation = {}
    for yoga in yogas:
        involved = yoga.get("involved_planets", [])
        if isinstance(involved, list):
            for p in involved:
                yoga_participation[p.lower()] = yoga_participation.get(p.lower(), 0) + 1
    
    rankings = []
    
    for p_name, p_data in planets.items():
        score = 0.0
        reasons = []
        
        # 1. Dignity score (0.5 - 5.0)
        dignity = (p_data.get("dignity") or "neutral").lower()
        dig_score = 2.0  # default neutral
        for key, val in DIGNITY_SCORES.items():
            if key in dignity:
                dig_score = val
                break
        score += dig_score
        if dig_score >= 4.0:
            reasons.append(f"{dignity.title()} dignity in {p_data.get('sign', '?')}")
        elif dig_score <= 1.0:
            reasons.append(f"{dignity.title()} in {p_data.get('sign', '?')}")
        
        # 2. House placement quality (0 - 3.0)
        house = p_data.get("house")
        if house:
            h = int(house)
            if h in KENDRA_HOUSES:
                score += 3.0
                reasons.append(f"Kendra placement (House {h})")
            elif h in TRIKONA_HOUSES:
                score += 2.5
                reasons.append(f"Trikona placement (House {h})")
            elif h in UPACHAYA_HOUSES:
                score += 1.5
                reasons.append(f"Upachaya placement (House {h})")
            elif h in DUSTHANA_HOUSES:
                score -= 1.0
                reasons.append(f"Dusthana placement (House {h})")
            else:
                score += 1.0
        
        # 3. Yoga participation bonus (+0.5 per yoga)
        y_count = yoga_participation.get(p_name.lower(), 0)
        if y_count > 0:
            score += y_count * 0.5
            reasons.append(f"Participates in {y_count} yoga(s)")
        
        # 4. Retrograde penalty (-0.5) or bonus for malefics (+0.3)
        if p_data.get("retrograde"):
            if p_name.lower() in ["saturn", "mars", "rahu", "ketu"]:
                score += 0.3
                reasons.append("Retrograde (malefic — adds intensity)")
            else:
                score -= 0.5
                reasons.append("Retrograde (weakened)")
        
        # 5. Combustion penalty (-1.0)
        if p_data.get("combust"):
            score -= 1.0
            reasons.append("Combust (too close to Sun)")
        
        # Determine status label
        if score >= 6.0:
            status = "Very Strong"
        elif score >= 4.0:
            status = "Strong"
        elif score >= 2.5:
            status = "Moderate"
        elif score >= 1.0:
            status = "Weak"
        else:
            status = "Very Weak"
        
        rankings.append({
            "planet": p_name,
            "display_name": p_data.get("name_sanskrit", p_name.capitalize()),
            "score": round(score, 1),
            "status": status,
            "sign": p_data.get("sign", "?"),
            "house": house,
            "reasons": reasons,
        })
    
    # Sort by score descending
    rankings.sort(key=lambda x: x["score"], reverse=True)
    
    # Assign rank
    for i, r in enumerate(rankings):
        r["rank"] = i + 1
    
    return rankings
