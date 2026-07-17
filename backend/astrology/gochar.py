"""
Gochar (Transit) computation for Vedic Astrology.

Calculates current planetary transits and their relationship to
the natal chart (transit houses, transit-to-natal aspects).
"""

import datetime

from services.astrology.swiss_ephemeris import (
    datetime_to_jd,
    get_sidereal_positions,
)
from services.astrology.planets import ZODIAC_SIGNS, get_sign_name
from backend.astrology.types import GocharData


# Vedic aspect offsets by planet (house number offsets for aspects)
# All planets have 7th aspect; Mars has 4th & 8th; Jupiter 5th & 9th; Saturn 3rd & 10th.
SPECIAL_ASPECTS = {
    "mars":    [4, 7, 8],
    "jupiter": [5, 7, 9],
    "saturn":  [3, 7, 10],
}
DEFAULT_ASPECTS = [7]


def compute_current_transits(
    transit_date: datetime.date = None,
) -> dict:
    """
    Get sidereal positions of all planets at the given date (noon UTC).

    Returns:
        {"sun": 123.45, "moon": 234.56, ...}
    """
    if transit_date is None:
        transit_date = datetime.date.today()

    jd = datetime_to_jd(transit_date.year, transit_date.month, transit_date.day, 12.0)
    return get_sidereal_positions(jd)


def compute_transit_houses(
    transit_positions: dict,
    natal_ascendant: float,
) -> dict:
    """
    Determine which natal house each transiting planet occupies.

    Uses Whole Sign system: the natal Ascendant sign is House 1.
    """
    asc_sign_idx = int(natal_ascendant // 30)
    transit_houses = {}

    for planet, lon in transit_positions.items():
        planet_sign_idx = int(lon // 30)
        house = ((planet_sign_idx - asc_sign_idx) % 12) + 1
        transit_houses[planet] = house

    return transit_houses


def compute_transit_signs(transit_positions: dict) -> dict:
    """Get the zodiac sign name for each transiting planet."""
    return {planet: get_sign_name(lon) for planet, lon in transit_positions.items()}


def compute_transit_aspects(
    transit_positions: dict,
    natal_positions: dict,
    natal_ascendant: float,
) -> list:
    """
    Compute transit-to-natal aspects.

    For each transiting planet, determine which natal houses it aspects
    and which natal planets occupy those houses.
    """
    asc_sign_idx = int(natal_ascendant // 30)

    # Build natal planet → house map
    natal_houses = {}
    for planet, lon in natal_positions.items():
        planet_sign_idx = int(lon // 30)
        house = ((planet_sign_idx - asc_sign_idx) % 12) + 1
        natal_houses[planet] = house

    # Build house → natal planets map
    house_to_planets = {}
    for planet, house in natal_houses.items():
        house_to_planets.setdefault(house, []).append(planet)

    aspects = []

    for t_planet, t_lon in transit_positions.items():
        t_sign_idx = int(t_lon // 30)
        t_house = ((t_sign_idx - asc_sign_idx) % 12) + 1

        # Get aspect offsets for this planet
        aspect_offsets = SPECIAL_ASPECTS.get(t_planet, DEFAULT_ASPECTS)

        for offset in aspect_offsets:
            aspected_house = ((t_house + offset - 1) % 12) + 1
            natal_in_house = house_to_planets.get(aspected_house, [])

            if natal_in_house:
                for n_planet in natal_in_house:
                    aspects.append(
                        f"Transit {t_planet.capitalize()} (House {t_house}) "
                        f"aspects natal {n_planet.capitalize()} (House {aspected_house})"
                    )
            else:
                aspects.append(
                    f"Transit {t_planet.capitalize()} (House {t_house}) "
                    f"aspects House {aspected_house}"
                )

    return aspects


def build_gochar_data(
    natal_positions: dict,
    natal_ascendant: float,
    transit_date: datetime.date = None,
) -> GocharData:
    """
    Build a complete GocharData object for the given transit date.
    """
    if transit_date is None:
        transit_date = datetime.date.today()

    t_positions = compute_current_transits(transit_date)
    t_signs = compute_transit_signs(t_positions)
    t_houses = compute_transit_houses(t_positions, natal_ascendant)
    t_aspects = compute_transit_aspects(t_positions, natal_positions, natal_ascendant)

    return GocharData(
        transit_date=transit_date.isoformat(),
        transit_positions=t_positions,
        transit_signs=t_signs,
        transit_houses=t_houses,
        transit_aspects=t_aspects,
    )
