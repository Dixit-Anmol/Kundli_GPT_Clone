"""
Strongly-typed dataclass definitions for the Vedic Astrology Engine.

Every chart, planet position, house cusp, dasha period, and global
calculation is represented as a typed dictionary (TypedDict) so the
entire FullChartBundle is JSON-serialisable out of the box.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
import datetime


# ---------------------------------------------------------------------------
# Birth Details
# ---------------------------------------------------------------------------
@dataclass
class BirthDetails:
    name: str
    date_of_birth: str          # "YYYY-MM-DD"
    time_of_birth: str          # "HH:MM:SS"
    latitude: float
    longitude: float
    timezone_offset: float      # UTC offset in hours (e.g. 5.5 for IST)


# ---------------------------------------------------------------------------
# Nakshatra
# ---------------------------------------------------------------------------
@dataclass
class NakshatraInfo:
    name: str
    lord: str
    deity: str
    pada: int
    longitude: float


# ---------------------------------------------------------------------------
# Planet Position (per-chart, per-planet)
# ---------------------------------------------------------------------------
@dataclass
class PlanetPosition:
    name: str                   # e.g. "sun"
    name_sanskrit: str          # e.g. "Surya"
    longitude: float            # sidereal longitude in that chart
    sign: str                   # e.g. "Leo"
    sign_index: int             # 0-11
    degree: float               # degree within sign (0-30)
    house: int                  # 1-12
    nakshatra: NakshatraInfo
    dignity: str                # "Exalted", "Own Sign", "Debilitated", "Neutral", etc.
    is_retrograde: bool
    is_combust: bool
    speed: float                # degrees per day (negative = retrograde)


# ---------------------------------------------------------------------------
# House Cusp
# ---------------------------------------------------------------------------
@dataclass
class HouseCusp:
    house_number: int           # 1-12
    sign: str
    sign_index: int
    lord: str                   # planet that rules this sign
    signification: str


# ---------------------------------------------------------------------------
# Single Divisional Chart
# ---------------------------------------------------------------------------
@dataclass
class ChartData:
    chart_name: str                             # "D1", "D9", etc.
    planet_positions: Dict[str, PlanetPosition] = field(default_factory=dict)
    house_cusps: List[HouseCusp] = field(default_factory=list)
    house_lords: Dict[int, str] = field(default_factory=dict)          # {1: "mars", 2: "venus", ...}
    planet_house_mapping: Dict[str, int] = field(default_factory=dict)  # {"sun": 5, ...}
    planet_sign_mapping: Dict[str, str] = field(default_factory=dict)   # {"sun": "Leo", ...}
    planet_strength: Dict[str, str] = field(default_factory=dict)       # {"sun": "Strong", ...}
    benefic_planets: List[str] = field(default_factory=list)
    malefic_planets: List[str] = field(default_factory=list)
    aspects: List[str] = field(default_factory=list)
    conjunctions: List[str] = field(default_factory=list)
    exaltations: List[str] = field(default_factory=list)
    debilitations: List[str] = field(default_factory=list)
    retrograde_planets: List[str] = field(default_factory=list)
    combust_planets: List[str] = field(default_factory=list)
    yogas: List[Dict[str, str]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Dasha
# ---------------------------------------------------------------------------
@dataclass
class DashaPeriod:
    planet: str
    start: str                  # ISO date
    end: str                    # ISO date
    duration_years: float
    sub_periods: List[DashaPeriod] = field(default_factory=list)


@dataclass
class DashaData:
    mahadasha_timeline: List[DashaPeriod] = field(default_factory=list)
    current_mahadasha: Optional[DashaPeriod] = None
    current_antardasha: Optional[DashaPeriod] = None
    current_pratyantar: Optional[DashaPeriod] = None


# ---------------------------------------------------------------------------
# Gochar (Transits)
# ---------------------------------------------------------------------------
@dataclass
class GocharData:
    transit_date: str           # ISO date
    transit_positions: Dict[str, float] = field(default_factory=dict)       # {"sun": 123.45, ...}
    transit_signs: Dict[str, str] = field(default_factory=dict)             # {"sun": "Leo", ...}
    transit_houses: Dict[str, int] = field(default_factory=dict)            # {"sun": 5, ...} (natal house)
    transit_aspects: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Shadbala
# ---------------------------------------------------------------------------
@dataclass
class ShadbalaEntry:
    planet: str
    sthana_bala: float          # Positional strength
    dig_bala: float             # Directional strength
    kala_bala: float            # Temporal strength
    chesta_bala: float          # Motional strength
    naisargika_bala: float      # Natural strength
    drik_bala: float            # Aspectual strength
    total: float


# ---------------------------------------------------------------------------
# Ashtakavarga
# ---------------------------------------------------------------------------
@dataclass
class AshtakavargaEntry:
    planet: str
    bindu_per_house: List[int] = field(default_factory=list)  # 12 values (houses 1-12)
    total_bindu: int = 0


@dataclass
class AshtakavargaData:
    planet_entries: List[AshtakavargaEntry] = field(default_factory=list)
    sarvashtakavarga: List[int] = field(default_factory=list)  # 12 values (sum across all planets)


# ---------------------------------------------------------------------------
# Karakas
# ---------------------------------------------------------------------------
@dataclass
class KarakaData:
    atmakaraka: str = ""        # Highest degree planet
    amatyakaraka: str = ""      # Second highest
    bhratrikaraka: str = ""     # Third
    matrikaraka: str = ""       # Fourth
    putrakaraka: str = ""       # Fifth
    gnatikaraka: str = ""       # Sixth
    darakaraka: str = ""        # Seventh (lowest degree)


# ---------------------------------------------------------------------------
# Planetary Friendships
# ---------------------------------------------------------------------------
@dataclass
class FriendshipData:
    natural: Dict[str, Dict[str, str]] = field(default_factory=dict)
    # e.g. {"sun": {"moon": "friend", "mars": "friend", "saturn": "enemy", ...}}
    temporal: Dict[str, Dict[str, str]] = field(default_factory=dict)
    compound: Dict[str, Dict[str, str]] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Master Container
# ---------------------------------------------------------------------------
@dataclass
class FullChartBundle:
    birth_details: BirthDetails
    D1: ChartData = field(default_factory=lambda: ChartData(chart_name="D1"))
    D2: ChartData = field(default_factory=lambda: ChartData(chart_name="D2"))
    D4: ChartData = field(default_factory=lambda: ChartData(chart_name="D4"))
    D7: ChartData = field(default_factory=lambda: ChartData(chart_name="D7"))
    D9: ChartData = field(default_factory=lambda: ChartData(chart_name="D9"))
    D10: ChartData = field(default_factory=lambda: ChartData(chart_name="D10"))
    D12: ChartData = field(default_factory=lambda: ChartData(chart_name="D12"))
    D16: ChartData = field(default_factory=lambda: ChartData(chart_name="D16"))
    D20: ChartData = field(default_factory=lambda: ChartData(chart_name="D20"))
    D24: ChartData = field(default_factory=lambda: ChartData(chart_name="D24"))
    D27: ChartData = field(default_factory=lambda: ChartData(chart_name="D27"))
    D30: ChartData = field(default_factory=lambda: ChartData(chart_name="D30"))
    D40: ChartData = field(default_factory=lambda: ChartData(chart_name="D40"))
    D45: ChartData = field(default_factory=lambda: ChartData(chart_name="D45"))
    D60: ChartData = field(default_factory=lambda: ChartData(chart_name="D60"))
    dasha: DashaData = field(default_factory=DashaData)
    gochar: GocharData = field(default_factory=lambda: GocharData(transit_date=""))
    nakshatra: Dict[str, NakshatraInfo] = field(default_factory=dict)
    shadbala: List[ShadbalaEntry] = field(default_factory=list)
    ashtakavarga: AshtakavargaData = field(default_factory=AshtakavargaData)
    friendships: FriendshipData = field(default_factory=FriendshipData)
    dignity: Dict[str, str] = field(default_factory=dict)
    lagna: str = ""
    moon_sign: str = ""
    sun_sign: str = ""
    karakas: KarakaData = field(default_factory=KarakaData)
    generated_at: str = ""

    def to_dict(self) -> dict:
        """Recursively convert the entire bundle to a JSON-serialisable dict."""
        return asdict(self)
