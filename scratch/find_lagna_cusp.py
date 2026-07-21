import swisseph as swe
import datetime

# Shivi Details
# 1990-12-09 11:55 AM IST at Delhi (28.6139 N, 77.2090 E)

tz_offset = 5.5
lat = 28.6139
lon = 77.2090

dt = datetime.datetime(1990, 12, 9, 11, 55, 0)
dt_utc = dt - datetime.timedelta(hours=tz_offset)
hour_utc = dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0

jd = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, hour_utc)

# Set Lahiri Ayanamsha
swe.set_sid_mode(swe.SIDM_LAHIRI)
ayanamsa = swe.get_ayanamsa_ut(jd)

# Swiss ephemeris houses_ex with tropical vs sidereal
cusps_w, ascmc_w = swe.houses_ex(jd, lat, lon, b'W', swe.FLG_SIDEREAL)
cusps_p, ascmc_p = swe.houses_ex(jd, lat, lon, b'P', swe.FLG_SIDEREAL)
cusps_p_trop, ascmc_p_trop = swe.houses_ex(jd, lat, lon, b'P', 0)

print(f"Ayanamsha (Lahiri): {ayanamsa:.6f}°")
print(f"ascmc_w[0] (Tropical Ascendant from houses_ex): {ascmc_w[0]:.6f}°")
print(f"Sidereal Ascendant (ascmc_w[0] - ayanamsa): {(ascmc_w[0] - ayanamsa) % 360:.6f}°")

asc_trop = ascmc_w[0]
asc_sid = (ascmc_w[0] - ayanamsa) % 360

print(f"\nTropical Ascendant Sign: {int(asc_trop // 30)} ({asc_trop % 30:.2f}°)")
print(f"Sidereal Ascendant Sign: {int(asc_sid // 30)} ({asc_sid % 30:.2f}°)")

signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
print(f"Tropical Ascendant: {signs[int(asc_trop // 30)]} ({asc_trop % 30:.2f}°)")
print(f"Sidereal Ascendant: {signs[int(asc_sid // 30)]} ({asc_sid % 30:.2f}°)")

# Let's check around 11:55 AM (e.g. 11:45, 11:50, 11:55, 12:00)
print("\n--- Testing Ascendant around 11:55 AM IST ---")
for m in [40, 45, 50, 52, 53, 54, 55, 56, 60]:
    dt_m = datetime.datetime(1990, 12, 9, 11, m, 0)
    dt_m_utc = dt_m - datetime.timedelta(hours=tz_offset)
    h_utc = dt_m_utc.hour + dt_m_utc.minute / 60.0 + dt_m_utc.second / 3600.0
    jd_m = swe.julday(dt_m_utc.year, dt_m_utc.month, dt_m_utc.day, h_utc)
    ay_m = swe.get_ayanamsa_ut(jd_m)
    c_m, a_m = swe.houses_ex(jd_m, lat, lon, b'W', swe.FLG_SIDEREAL)
    sid_asc = (a_m[0] - ay_m) % 360
    sign_name = signs[int(sid_asc // 30)]
    print(f"Time {11}:{m:02d} AM IST -> Sidereal Ascendant: {sid_asc:.4f}° ({sign_name} {sid_asc % 30:.2f}°)")
