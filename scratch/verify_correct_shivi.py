import swisseph as swe
import datetime

# Shivi Details: 1990-12-09 11:55 AM IST Delhi
tz_offset = 5.5
lat = 28.6139
lon = 77.2090

dt = datetime.datetime(1990, 12, 9, 11, 55, 0)
dt_utc = dt - datetime.timedelta(hours=tz_offset)
hour_utc = dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0

jd = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, hour_utc)
swe.set_sid_mode(swe.SIDM_LAHIRI)

# Correct Sidereal Ascendant (FLG_SIDEREAL already handles Ayanamsha!)
cusps_sid, ascmc_sid = swe.houses_ex(jd, lat, lon, b'W', swe.FLG_SIDEREAL)
asc_sidereal = ascmc_sid[0] % 360.0

signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
asc_sign_idx = int(asc_sidereal // 30)

print(f"Correct Sidereal Ascendant: {asc_sidereal:.4f}° ({signs[asc_sign_idx]} {asc_sidereal % 30:.2f}°)")

# Calculate planets sidereal
swe_planets = {
    'sun': swe.SUN,
    'moon': swe.MOON,
    'mercury': swe.MERCURY,
    'venus': swe.VENUS,
    'mars': swe.MARS,
    'jupiter': swe.JUPITER,
    'saturn': swe.SATURN,
    'rahu': swe.TRUE_NODE,
}

positions = {}
for name, swe_id in swe_planets.items():
    res = swe.calc_ut(jd, swe_id, swe.FLG_SIDEREAL)
    positions[name] = res[0][0]
positions['ketu'] = (positions['rahu'] + 180.0) % 360.0

print("\n--- Correct Whole Sign Houses for Shivi (Aquarius Lagna) ---")
for p_name, long in positions.items():
    p_sign_idx = int(long // 30)
    house = ((p_sign_idx - asc_sign_idx) % 12) + 1
    deg = long % 30
    print(f"{p_name.capitalize()}: Longitude {long:.2f}° | {signs[p_sign_idx]} {deg:.2f}° | House {house}")
