HOUSE_SIGNIFICATORS = {
    1: "Self, personality, physical body, appearance, health, beginning of life.",
    2: "Wealth, family, speech, primary education, food, assets, face.",
    3: "Courage, short travels, siblings, communication, writing, efforts, hands.",
    4: "Mother, home, happiness, vehicle, lands, emotions, heart, inner peace.",
    5: "Intellect, children, creativity, past life merits (Purvapunya), romance, speculation.",
    6: "Debts, enemies, diseases, service, daily routine, competition, obstacles.",
    7: "Spouse, partnership, business partners, relationship, travel, public life.",
    8: "Longevity, secrets, inheritance, sudden transformations, occult, mysteries.",
    9: "Dharma, fortune (Bhagya), father, higher education, long journeys, philosophy, religion.",
    10: "Career, status, reputation, public life, authority, karma, actions in society.",
    11: "Gains, desires fulfillment, friends, elder siblings, cash flow, achievements.",
    12: "Losses, liberation (Moksha), foreign travels, isolation, dreams, bedroom pleasures."
}

def calculate_planet_houses(planet_positions: dict, ascendant: float) -> dict:
    """Calculate the house number (1-12) for each planet using the Whole Sign system."""
    asc_sign_idx = int(ascendant // 30)
    planet_houses = {}
    
    for planet, long in planet_positions.items():
        planet_sign_idx = int(long // 30)
        # Calculate house index (1-indexed)
        house = ((planet_sign_idx - asc_sign_idx) % 12) + 1
        planet_houses[planet] = house
        
    return planet_houses

def get_house_lordships(ascendant: float) -> dict:
    """Map each house number (1-12) to its ruling sign and planet lord."""
    from services.astrology.planets import ZODIAC_SIGNS, SIGN_LORDS
    
    asc_sign_idx = int(ascendant // 30)
    lords = {}
    
    for house_num in range(1, 13):
        sign_idx = (asc_sign_idx + house_num - 1) % 12
        sign_name = ZODIAC_SIGNS[sign_idx]
        lord_planet = SIGN_LORDS[sign_name]
        lords[house_num] = {
            "sign": sign_name,
            "lord": lord_planet,
            "signification": HOUSE_SIGNIFICATORS[house_num]
        }
        
    return lords
