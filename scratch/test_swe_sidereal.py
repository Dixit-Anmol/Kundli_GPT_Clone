import swisseph as swe

swe.set_sid_mode(swe.SIDM_LAHIRI)

jd = swe.julday(1990, 12, 9, 6.416666666666667)
lat = 28.6139
lon = 77.2090

ay = swe.get_ayanamsa_ut(jd)
cusps_sid, ascmc_sid = swe.houses_ex(jd, lat, lon, b'W', swe.FLG_SIDEREAL)
cusps_trop, ascmc_trop = swe.houses_ex(jd, lat, lon, b'W', 0)

print("Ayanamsha:", ay)
print("Tropical ascmc[0]:", ascmc_trop[0])
print("Sidereal ascmc[0] (FLG_SIDEREAL):", ascmc_sid[0])
print("Difference (ascmc_trop[0] - ascmc_sid[0]):", (ascmc_trop[0] - ascmc_sid[0]) % 360)

print("\n--- Cusps comparison ---")
print("Tropical Cusps:", cusps_trop)
print("Sidereal Cusps (FLG_SIDEREAL):", cusps_sid)
