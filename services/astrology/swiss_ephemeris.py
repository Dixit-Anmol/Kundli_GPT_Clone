"""
Vedic Astrology calculations using Swiss Ephemeris C-bindings.

This module delegates 100% of Julian Day, Ayanamsha, planet positions,
and house/ascendant computations to the compiled Swiss Ephemeris library,
eliminating manual math approximations.
"""

import os
import swisseph as swe

# Resolve ephemeris files directory path
_BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_EPHEM_PATH = os.path.abspath(os.path.join(
    os.path.dirname(_BACKEND_DIR),  # project root from services/
    "backend", "data", "ephemeris"
))

if os.path.exists(_EPHEM_PATH):
    swe.set_ephe_path(_EPHEM_PATH)

# Set global sidereal mode to Lahiri
swe.set_sid_mode(swe.SIDM_LAHIRI)


def datetime_to_jd(year: int, month: int, day: int, hour_utc: float) -> float:
    """Convert UTC calendar date and decimal hour to Julian Day Number using Swiss Ephemeris."""
    return swe.julday(year, month, day, hour_utc)


def get_lahiri_ayanamsa(jd: float) -> float:
    """Get the true Lahiri Ayanamsha from Swiss Ephemeris."""
    return swe.get_ayanamsa_ut(jd)


def get_sidereal_positions(jd: float) -> dict:
    """Calculate geocentric sidereal positions of all planets using Swiss Ephemeris."""
    swe_planets = {
        'sun': swe.SUN,
        'moon': swe.MOON,
        'mercury': swe.MERCURY,
        'venus': swe.VENUS,
        'mars': swe.MARS,
        'jupiter': swe.JUPITER,
        'saturn': swe.SATURN,
    }
    
    positions = {}
    
    # Calculate geocentric positions directly in sidereal mode
    for name, swe_id in swe_planets.items():
        res = swe.calc_ut(jd, swe_id, swe.FLG_SIDEREAL)
        positions[name] = res[0][0]
        
    # True node for Rahu, Ketu is Rahu + 180
    rahu_res = swe.calc_ut(jd, swe.TRUE_NODE, swe.FLG_SIDEREAL)
    positions['rahu'] = rahu_res[0][0]
    positions['ketu'] = (rahu_res[0][0] + 180.0) % 360.0
    
    return positions


def get_house_cusps(jd: float, lat: float, lon: float) -> tuple:
    """Compute Whole Sign house positions and true Sidereal Ascendant using Swiss Ephemeris."""
    # houses_ex returns (cusps, ascmc) in sidereal mode when FLG_SIDEREAL is passed
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'W', swe.FLG_SIDEREAL)
    
    # ascmc[0] with FLG_SIDEREAL is already the true sidereal Ascendant
    ascendant_sidereal = ascmc[0] % 360.0
    
    # Calculate Whole Sign house boundaries based on sidereal Ascendant sign
    asc_sign_idx = int(ascendant_sidereal // 30)
    house_cusps_sidereal = [(asc_sign_idx * 30.0 + i * 30.0) % 360.0 for i in range(12)]
    
    return ascendant_sidereal, house_cusps_sidereal


