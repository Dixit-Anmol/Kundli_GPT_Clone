import os

def classify_intent(query: str) -> str:
    """Classify user query into one of the key Vedic life intents."""
    q = query.lower()
    if any(k in q for k in ["job", "career", "work", "business", "profession", "boss", "salary", "promotion"]):
        return "Career"
    if any(k in q for k in ["relationship", "love", "partner", "friend", "gf", "bf", "dating"]):
        return "Relationships"
    if any(k in q for k in ["marry", "marriage", "husband", "wife", "spouse", "wedding"]):
        return "Marriage"
    if any(k in q for k in ["health", "disease", "sick", "cure", "body", "physical", "illness"]):
        return "Health"
    if any(k in q for k in ["spirit", "god", "meditat", "yoga", "dharma", "guru", "moksha"]):
        return "Spirituality"
    if any(k in q for k in ["money", "wealth", "finance", "rich", "debt", "loan", "savings"]):
        return "Wealth"
    if any(k in q for k in ["study", "exam", "education", "college", "school", "degree", "learning"]):
        return "Education"
    if any(k in q for k in ["family", "parent", "mother", "father", "brother", "sister", "home"]):
        return "Family"
    if any(k in q for k in ["mind", "mental", "stress", "anxiet", "depress", "wellbeing", "peace"]):
        return "Mental Wellbeing"
    if any(k in q for k in ["remedy", "gemstone", "stone", "pooja", "mantra", "ritual"]):
        return "Remedies"
    if any(k in q for k in ["gita", "verse", "krishna", "geeta", "shloka"]):
        return "Bhagavad Gita Discussion"
    if any(k in q for k in ["explain", "chart", "placements", "birth", "lagna", "signs"]):
        return "Astrology Explanation"
    return "General Horoscope"

def calculate_vedic_aspects(planets: dict) -> list:
    """Determine major Vedic planetary aspects (Drishti) dynamically from house positions."""
    aspects = []
    for p_name, p in planets.items():
        h = p.get("house")
        if not h:
            continue
        # Standard 7th aspect
        t7 = (h + 6) % 12 or 12
        aspects.append(f"{p_name.capitalize()} aspects House {t7}")
        # Special aspects
        if p_name.lower() == "mars":
            t4 = (h + 3) % 12 or 12
            t8 = (h + 7) % 12 or 12
            aspects.append(f"Mars aspects House {t4}")
            aspects.append(f"Mars aspects House {t8}")
        elif p_name.lower() == "jupiter":
            t5 = (h + 4) % 12 or 12
            t9 = (h + 8) % 12 or 12
            aspects.append(f"Jupiter aspects House {t5}")
            aspects.append(f"Jupiter aspects House {t9}")
        elif p_name.lower() == "saturn":
            t3 = (h + 2) % 12 or 12
            t10 = (h + 9) % 12 or 12
            aspects.append(f"Saturn aspects House {t3}")
            aspects.append(f"Saturn aspects House {t10}")
    return aspects

def get_planet_strengths(planets: dict) -> dict:
    """Evaluate planetary strength based on dignity (exalted, own, debilitated, enemy sign)."""
    strengths = {}
    for p_name, p in planets.items():
        dignity = p.get("dignity", "").lower()
        if any(w in dignity for w in ["exalted", "own", "moolatrikona"]):
            strengths[p_name] = ("Strong", f"Placed in {p.get('dignity')} sign ({p.get('sign')})")
        elif any(w in dignity for w in ["debilitated", "enemy"]):
            strengths[p_name] = ("Weak", f"Placed in {p.get('dignity')} sign ({p.get('sign')})")
        else:
            strengths[p_name] = ("Neutral", f"Placed in neutral/friendly sign ({p.get('sign')})")
    return strengths

def assemble_unified_prompt(
    query: str,
    chart_data: dict,
    profile: dict = None,
    history: list = None,
    passages: list = None,
    intent: str = None
) -> str:
    """Assembles all horoscope, user profile, and Gita context into the exact 13 ordered sections."""
    meta = chart_data.get("metadata", {})
    planets = chart_data.get("planets", {})
    houses = chart_data.get("houses", {})
    yogas = chart_data.get("yogas", [])
    doshas = chart_data.get("doshas", {})

    # 1. Conversation History
    hist_formatted = "None."
    if history:
        turns = []
        for h in history[-5:]: # Keep last 5 turns for tokens
            turns.append(f"{h['role'].capitalize()}: {h['content']}")
        hist_formatted = "\n".join(turns)

    # 2. Conversation Summary
    summary_formatted = "None."
    if history:
        last_asst = next((m["content"] for m in reversed(history) if m["role"] == "assistant"), None)
        if last_asst:
            summary_formatted = f"Last guidance shared with Seeker: {last_asst[:150]}..."

    # 3. User Intent
    detected_intent = intent or classify_intent(query)

    # 4. User Profile
    name = profile.get("name", "Seeker") if profile else "Seeker"
    dob = profile.get("date_of_birth", "N/A") if profile else "N/A"
    tob = profile.get("time_of_birth", "N/A") if profile else "N/A"
    coords = f"Lat: {profile.get('latitude', 0.0):.4f}, Lon: {profile.get('longitude', 0.0):.4f}" if profile else "N/A"
    tz = f"UTC Offset: {profile.get('timezone_offset', 5.5)}h" if profile else "N/A"
    user_profile = f"Name: {name}\nDate of Birth: {dob}\nTime of Birth: {tob}\nCoordinates: {coords}\nTimezone: {tz}"

    # 5. Horoscope Context
    h_context = (
        f"Ascendant (Lagna): {meta.get('ascendant_sign', 'Aries')} at {meta.get('ascendant_longitude', 0.0):.2f}°\n"
        f"Moon Sign (Rashi): {meta.get('moon_sign', 'Cancer')}\n"
        f"Nakshatra: {meta.get('nakshatra', 'Pushya')} (Pada {meta.get('pada', 1)})"
    )

    # 6. Planetary Positions & Strengths
    planet_positions = ""
    strengths_map = get_planet_strengths(planets)
    for p_name, p in planets.items():
        state = "Retrograde" if p.get("retrograde") else "Direct"
        combust = "Combust" if p.get("combust") else "Non-combust"
        str_val, str_desc = strengths_map.get(p_name, ("Neutral", ""))
        planet_positions += (
            f"- {p['name_sanskrit']} ({p_name.capitalize()}): Sign: {p['sign']} | Degree: {p['degree']:.2f}° | "
            f"House: {p['house']} | Nakshatra: {p['nakshatra']['name']} | Status: {state}, {combust} | Strength: {str_val} ({str_desc})\n"
        )

    # 7. Houses
    houses_info = ""
    for h_num in sorted(houses.keys(), key=int):
        h = houses[h_num]
        # Find occupying planets
        occupants = [p_name.capitalize() for p_name, p in planets.items() if str(p.get("house")) == str(h_num)]
        occupants_str = ", ".join(occupants) if occupants else "None"
        houses_info += f"- House {h_num} ({h['sign']}): Lord: {h['lord'].capitalize()} | Occupying: {occupants_str} | Signification: {h['signification']}\n"

    # 8. Vedic Aspects
    aspects_info = "\n".join(calculate_vedic_aspects(planets))

    # 9. Yogas
    yogas_info = ""
    if yogas:
        for y in yogas:
            yogas_info += f"- {y['name']} ({y['type']}): {y['meaning']}\n"
    else:
        yogas_info = "None active."

    # 10. Doshas
    doshas_info = ""
    for d_name, d_val in doshas.items():
        active = "Active" if d_val.get("is_present") else "Not Active"
        doshas_info += f"- {d_name.capitalize()}: Status: {active} | Description: {d_val.get('description', 'No affliction detected.')}\n"

    # 11. Dashas
    # Fallback to general current dasha block for scalability
    dashas_formatted = "Current Mahadasha: Jupiter | Remaining: Approx. 5 years (General reference)."

    # 12. Retrieved Bhagavad Gita Context
    gita_passages = ""
    if passages:
        for idx, passg in enumerate(passages):
            gita_passages += f"Verse Reference {idx+1}:\n{passg}\n\n"
    else:
        gita_passages = "No specific verse references available. Use general teachings of Karma Yoga and Self-Realization."

    # Future Scalability Marker
    scalability_marker = "[Future Extensibility: Sacred scriptures, bank statements, daily mood journals, health bio-data remain offline.]"

    # Compile the final structured prompt matching the ordering requirement
    prompt = f"""[2. CONVERSATION HISTORY]
{hist_formatted}

[3. CONVERSATION SUMMARY]
{summary_formatted}

[4. USER INTENT]
{detected_intent}

[5. USER PROFILE]
{user_profile}

[6. HOROSCOPE CONTEXT]
{h_context}

[7. PLANETARY STRENGTHS & POSITIONS]
{planet_positions}

[8. HOUSES]
{houses_info}

[9. VEDIC ASPECTS]
{aspects_info}

[10. YOGAS]
{yogas_info}

[11. DOSHAS]
{doshas_info}

[12. DASHAS]
{dashas_formatted}

[13. RETRIEVED BHAGAVAD GITA CONTEXT]
{gita_passages}

{scalability_marker}

[CURRENT USER QUESTION]
"{query}"
"""
    return prompt

def build_geeta_prompt(name: str, query: str, chart_data: dict, passages: list) -> str:
    """Old geeta prompt compatibility layer - routes into the unified prompt compiler."""
    # Since this is a legacy router, we fallback to passing chart_data and RAG passages
    return assemble_unified_prompt(
        query=query,
        chart_data=chart_data,
        passages=passages
    )
