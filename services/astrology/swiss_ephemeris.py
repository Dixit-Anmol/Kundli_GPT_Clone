import os
import math
from functools import lru_cache

# Try importing pyswisseph (Swiss Ephemeris wrapper)
try:
    import swisseph as swe
    SWISSEPH_AVAILABLE = True
except ImportError:
    SWISSEPH_AVAILABLE = False

# Analytical calculations for Keplerian elements as fallback
# This provides highly accurate positions for Vedic chart signs/nakshatras
# without needing compiled C binaries.
PLANET_ELEMENTS = {
    # Elements at J2000.0: [a (AU), e, i (deg), L (deg), long_peri (deg), long_node (deg)]
    # and their rates per century.
    'sun': [1.00000011, 0.01671022, 0.00005, 280.46645, 282.94049, 0.0,
            0.00000005, -0.00003804, -0.0152, 36000.76983, 1.178229, 0.0],
    'mercury': [0.38709893, 0.20563069, 7.00487, 252.25084, 77.45645, 48.33167,
                0.0, 0.0000204, -0.00594, 149472.67411, 0.15901, -0.12516],
    'venus': [0.72333199, 0.00677323, 3.39471, 181.97973, 131.53298, 76.68069,
              0.0, -0.00004776, -0.000788, 58517.81538, 0.002008, -0.27769],
    'mars': [1.52366231, 0.09341233, 1.85061, 355.45332, 336.04084, 49.57854,
             -0.00007221, 0.00011902, -0.000724, 19140.30268, 0.44388, -0.29277],
    'jupiter': [5.20336301, 0.04839266, 1.3053, 34.40438, 14.75385, 100.55615,
                0.00060737, -0.0001288, -0.00415, 3034.74612, 0.1915, 0.20388],
    'saturn': [9.53707032, 0.0541506, 2.48446, 49.94432, 92.43194, 113.71504,
               -0.0030153, -0.00036762, 0.00193, 1222.11379, -0.41897, -0.28867]
}

def datetime_to_jd(year: int, month: int, day: int, hour_utc: float) -> float:
    """Convert UTC calendar date and decimal hour to Julian Day Number."""
    if month <= 2:
        year -= 1
        month += 12
    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)
    jd = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + (hour_utc / 24.0) + B - 1524.5
    return jd

def get_lahiri_ayanamsa(jd: float) -> float:
    """Calculate Lahiri Ayanamsa (precession offset for sidereal Vedic astrology)."""
    # Standard approximation: Ayanamsa at J2000.0 is ~23.85 degrees
    # Precession rate is approx 50.3 seconds of arc per year (0.01397 degrees per year)
    t = (jd - 2451545.0) / 36525.0  # Julian centuries since J2000
    ayanamsa = 23.85 + 1.39697 * t + 0.0003086 * t * t
    return ayanamsa % 360.0

@lru_cache(maxsize=5)
def calculate_positions_raw(jd: float) -> dict:
    """Calculate geocentric ecliptic coordinates of planets (tropical degrees)."""
    positions = {}
    
    if SWISSEPH_AVAILABLE:
        # Configure Swiss Ephemeris
        # Check if we have ephemeris data folder, set path if exists
        ephem_path = os.path.join(os.path.dirname(__file__), '..', '..', 'backend', 'data', 'ephemeris')
        if os.path.exists(ephem_path):
            swe.set_ephe_path(ephem_path)
            
        swe_planets = {
            'sun': swe.SUN,
            'moon': swe.MOON,
            'mercury': swe.MERCURY,
            'venus': swe.VENUS,
            'mars': swe.MARS,
            'jupiter': swe.JUPITER,
            'saturn': swe.SATURN,
        }
        
        # Geocentric calculations (UT)
        for name, swe_id in swe_planets.items():
            res = swe.calc_ut(jd, swe_id)
            positions[name] = res[0][0]  # Longitude is the first element of the results tuple
            
        # Node positions (True node for Rahu, Ketu is Rahu + 180)
        rahu_res = swe.calc_ut(jd, swe.TRUE_NODE)
        positions['rahu'] = rahu_res[0][0]
        positions['ketu'] = (rahu_res[0][0] + 180.0) % 360.0
        
    else:
        # Fallback Keplerian analytical model
        t = (jd - 2451545.0) / 36525.0  # Julian centuries since J2000
        
        # Sun position (Earth position inverted)
        sun_elems = PLANET_ELEMENTS['sun']
        L = (sun_elems[3] + sun_elems[9] * t) % 360.0
        g = math.radians((L - (sun_elems[4] + sun_elems[10] * t)) % 360.0)
        sun_long = (L + 1.9148 * math.sin(g) + 0.0200 * math.sin(2*g)) % 360.0
        positions['sun'] = sun_long
        
        # Moon position (Simplified analytical model)
        # Mean longitude
        Lm = (218.316 + 481267.881 * t) % 360.0
        # Mean anomaly
        Mm = math.radians((134.963 + 477198.868 * t) % 360.0)
        moon_long = (Lm + 6.289 * math.sin(Mm) + 1.274 * math.sin(math.radians((2*Lm - Mm)))) % 360.0
        positions['moon'] = moon_long

        # Rahu & Ketu (Mean Nodes)
        rahu_long = (125.0445 - 1934.136 * t) % 360.0
        positions['rahu'] = rahu_long
        positions['ketu'] = (rahu_long + 180.0) % 360.0

        # Calculate other planets (heliocentric to geocentric)
        for planet, elems in PLANET_ELEMENTS.items():
            if planet == 'sun':
                continue
            # Semi-major axis, eccentricity, inclination
            a = elems[0] + elems[6] * t
            e = elems[1] + elems[7] * t
            inc = math.radians(elems[2] + elems[8] * t)
            # Longitude of ascending node, perihelion
            node = math.radians(elems[5] + elems[11] * t)
            peri = math.radians(elems[4] + elems[10] * t)
            # Mean anomaly
            M = math.radians((elems[3] + elems[9] * t) - math.degrees(peri))
            
            # Kepler's Equation: E - e*sin(E) = M
            E = M
            for _ in range(5):
                E = M + e * math.sin(E)
                
            # Coordinates in orbital plane
            x_orb = a * (math.cos(E) - e)
            y_orb = a * math.sqrt(1 - e*e) * math.sin(E)
            
            # Plane rotation
            r = math.sqrt(x_orb**2 + y_orb**2)
            v = math.atan2(y_orb, x_orb)
            
            x_helio = r * (math.cos(node) * math.cos(v + peri - node) - math.sin(node) * math.sin(v + peri - node) * math.cos(inc))
            y_helio = r * (math.sin(node) * math.cos(v + peri - node) + math.cos(node) * math.sin(v + peri - node) * math.cos(inc))
            z_helio = r * math.sin(v + peri - node) * math.sin(inc)
            
            # Geocentric correction
            # Sun heliocentric coordinates (Earth coordinates relative to Sun inverted)
            sun_rad = math.radians(sun_long)
            x_sun = math.cos(sun_rad)
            y_sun = math.sin(sun_rad)
            
            x_geo = x_helio + x_sun
            y_geo = y_helio + y_sun
            
            positions[planet] = math.degrees(math.atan2(y_geo, x_geo)) % 360.0

    return positions

def get_sidereal_positions(jd: float) -> dict:
    """Calculate sidereal positions of planets using Lahiri Ayanamsa."""
    if SWISSEPH_AVAILABLE:
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        ayanamsa = swe.get_ayanamsa_ut(jd)
    else:
        ayanamsa = get_lahiri_ayanamsa(jd)
        
    tropical_pos = calculate_positions_raw(jd)
    sidereal_pos = {}
    for name, long in tropical_pos.items():
        sidereal_pos[name] = (long - ayanamsa) % 360.0
    return sidereal_pos

def get_house_cusps(jd: float, lat: float, lon: float) -> list:
    """Compute houses using Whole Sign system (standard in Vedic Astrology)."""
    if SWISSEPH_AVAILABLE:
        ephem_path = os.path.join(os.path.dirname(__file__), '..', '..', 'backend', 'data', 'ephemeris')
        if os.path.exists(ephem_path):
            swe.set_ephe_path(ephem_path)
            
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        ayanamsa = swe.get_ayanamsa_ut(jd)
        
        # Calculate house cusps and additional points (ascmc[0] is the Ascendant)
        cusps, ascmc = swe.houses(jd, lat, lon, b'W')
        ascendant_tropical = ascmc[0]
        ascendant_sidereal = (ascendant_tropical - ayanamsa) % 360.0
    else:
        # Fallback to analytical model
        # Calculate Ascendant (Lagna)
        d = jd - 2451545.0
        t = d / 36525.0
        gst = (18.697374558 + 24.06570982441908 * d) % 24.0
        lst = (gst + lon / 15.0) % 24.0
        ramc = lst * 15.0 # Right Ascension of Meridian Cusp in degrees
        
        # Obliquity of ecliptic
        eps = math.radians(23.4392911 - 46.8150 * t / 3600.0)
        
        # Standard Astronomical Ascendant formula (correcting quadrant signs)
        ramc_rad = math.radians(ramc)
        lat_rad = math.radians(lat)
        
        numerator = math.cos(ramc_rad)
        denominator = -math.sin(ramc_rad) * math.cos(eps) - math.tan(lat_rad) * math.sin(eps)
        
        ascendant_tropical = math.degrees(math.atan2(numerator, denominator)) % 360.0
        
        # Offset by Lahiri Ayanamsa for sidereal Ascendant
        ayanamsa = get_lahiri_ayanamsa(jd)
        ascendant_sidereal = (ascendant_tropical - ayanamsa) % 360.0
        
    # Whole Sign House System:
    # 1st house starts at 0 degrees of the sign of Ascendant.
    # House 1 = sign_idx of ascendant, House 2 = (sign_idx + 1) % 12, etc.
    asc_sign_idx = int(ascendant_sidereal // 30)
    
    house_cusps_sidereal = []
    for h in range(12):
        cusp_long = ((asc_sign_idx + h) * 30.0) % 360.0
        house_cusps_sidereal.append(cusp_long)
        
    return ascendant_sidereal, house_cusps_sidereal
