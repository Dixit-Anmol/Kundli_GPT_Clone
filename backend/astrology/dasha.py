"""
Vimshottari Dasha computation with 3-level depth.

Computes Mahadasha → Antardasha → Pratyantar Dasha timelines from
Moon's sidereal longitude and birth date.
"""

import datetime
from typing import List, Optional
from backend.astrology.types import DashaPeriod, DashaData


# ---------------------------------------------------------------------------
# Vimshottari constants
# ---------------------------------------------------------------------------

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
    "mercury": 17,
}

TOTAL_CYCLE_YEARS = 120  # Sum of all Mahadasha years


# ---------------------------------------------------------------------------
# Core computation
# ---------------------------------------------------------------------------

def _add_days(base: datetime.date, days: float) -> datetime.date:
    """Add fractional days to a date."""
    return base + datetime.timedelta(days=int(days))


def _compute_sub_periods(
    parent_planet: str,
    parent_start: datetime.date,
    parent_duration_years: float,
    depth: int,   # 1 = Antardasha, 2 = Pratyantar
    max_depth: int = 2,
) -> List[DashaPeriod]:
    """
    Recursively compute sub-periods within a Mahadasha or Antardasha.

    Sub-period duration = (parent_duration × sub_lord_years) / 120
    Sub-periods follow the same DASHA_ORDER starting from the parent planet.
    """
    if depth > max_depth:
        return []

    # Find starting index in the cycle
    start_idx = DASHA_ORDER.index(parent_planet)
    current_date = parent_start
    sub_periods = []

    for i in range(9):
        sub_lord = DASHA_ORDER[(start_idx + i) % 9]
        sub_lord_years = DASHA_YEARS[sub_lord]

        # Duration of this sub-period
        sub_duration_years = (parent_duration_years * sub_lord_years) / TOTAL_CYCLE_YEARS
        sub_days = sub_duration_years * 365.25

        end_date = _add_days(current_date, sub_days)

        # Recursively compute deeper sub-periods
        deeper = _compute_sub_periods(
            sub_lord, current_date, sub_duration_years,
            depth + 1, max_depth
        )

        sub_periods.append(DashaPeriod(
            planet=sub_lord,
            start=current_date.isoformat(),
            end=end_date.isoformat(),
            duration_years=round(sub_duration_years, 4),
            sub_periods=deeper,
        ))

        current_date = end_date

    return sub_periods


def calculate_full_vimshottari(
    moon_longitude: float,
    birth_date: datetime.date,
    depth: int = 2,   # 2 = Maha → Antar → Pratyantar
) -> List[DashaPeriod]:
    """
    Calculate the complete Vimshottari Dasha timeline from birth,
    with sub-periods down to the specified depth.

    Args:
        moon_longitude: Sidereal longitude of the Moon (0-360).
        birth_date: Date of birth.
        depth: How many sub-levels (1=Antar only, 2=Antar+Pratyantar).

    Returns:
        List of DashaPeriod objects representing the full Mahadasha timeline.
    """
    # Determine starting Nakshatra and progress
    nak_width = 360.0 / 27.0
    nak_idx = int(moon_longitude // nak_width)
    start_long = nak_idx * nak_width
    progress = (moon_longitude - start_long) / nak_width  # 0.0 to 1.0

    # Starting Dasha lord = Nakshatra lord
    start_lord_idx = nak_idx % 9
    start_lord = DASHA_ORDER[start_lord_idx]
    start_years = DASHA_YEARS[start_lord]

    # Remaining portion of the first Mahadasha at birth
    remaining_years = start_years * (1.0 - progress)

    current_date = birth_date
    timeline = []

    # First (partial) Mahadasha
    first_days = remaining_years * 365.25
    first_end = _add_days(current_date, first_days)

    sub_periods = _compute_sub_periods(
        start_lord, current_date, remaining_years, 1, depth
    )

    timeline.append(DashaPeriod(
        planet=start_lord,
        start=current_date.isoformat(),
        end=first_end.isoformat(),
        duration_years=round(remaining_years, 4),
        sub_periods=sub_periods,
    ))
    current_date = first_end

    # Subsequent full Mahadashas (complete the 120-year cycle)
    for i in range(1, 10):
        lord = DASHA_ORDER[(start_lord_idx + i) % 9]
        years = DASHA_YEARS[lord]
        days = years * 365.25
        end_date = _add_days(current_date, days)

        sub_periods = _compute_sub_periods(
            lord, current_date, years, 1, depth
        )

        timeline.append(DashaPeriod(
            planet=lord,
            start=current_date.isoformat(),
            end=end_date.isoformat(),
            duration_years=years,
            sub_periods=sub_periods,
        ))
        current_date = end_date

    return timeline


# ---------------------------------------------------------------------------
# Current period lookup
# ---------------------------------------------------------------------------

def _find_active_period(periods: List[DashaPeriod], query_iso: str) -> Optional[DashaPeriod]:
    """Find the active period from a list for a given ISO date."""
    for period in periods:
        if period.start <= query_iso <= period.end:
            return period
    return periods[-1] if periods else None


def get_current_periods(
    timeline: List[DashaPeriod],
    query_date: datetime.date,
) -> DashaData:
    """
    Given a full Mahadasha timeline, find the active Maha/Antar/Pratyantar
    periods for the query date.

    Returns a DashaData object with all three levels populated.
    """
    query_iso = query_date.isoformat()

    maha = _find_active_period(timeline, query_iso)
    antar = None
    pratyantar = None

    if maha and maha.sub_periods:
        antar = _find_active_period(maha.sub_periods, query_iso)
        if antar and antar.sub_periods:
            pratyantar = _find_active_period(antar.sub_periods, query_iso)

    return DashaData(
        mahadasha_timeline=timeline,
        current_mahadasha=maha,
        current_antardasha=antar,
        current_pratyantar=pratyantar,
    )
