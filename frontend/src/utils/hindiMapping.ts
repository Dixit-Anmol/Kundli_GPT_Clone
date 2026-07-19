/**
 * Hindi / Vedic Astrology Terminology Mappings.
 * Provides traditional Hindi / Sanskrit names for Signs (Rashi), Planets (Graha), and Houses (Bhavas).
 */

export const SIGN_HINDI_MAP: Record<string, { hindi: string; devanagari: string }> = {
  Aries: { hindi: 'Mesh', devanagari: 'मेष' },
  Taurus: { hindi: 'Vrishabha', devanagari: 'वृषभ' },
  Gemini: { hindi: 'Mithun', devanagari: 'मिथुन' },
  Cancer: { hindi: 'Kark', devanagari: 'कर्क' },
  Leo: { hindi: 'Simha', devanagari: 'सिंह' },
  Virgo: { hindi: 'Kanya', devanagari: 'कन्या' },
  Libra: { hindi: 'Tula', devanagari: 'तुला' },
  Scorpio: { hindi: 'Vrishchik', devanagari: 'वृश्चिक' },
  Sagittarius: { hindi: 'Dhanu', devanagari: 'धनु' },
  Capricorn: { hindi: 'Makar', devanagari: 'मकर' },
  Aquarius: { hindi: 'Kumbh', devanagari: 'कुंभ' },
  Pisces: { hindi: 'Meen', devanagari: 'मीन' },
}

export const PLANET_HINDI_MAP: Record<string, { hindi: string; devanagari: string }> = {
  Sun: { hindi: 'Surya', devanagari: 'सूर्य' },
  Moon: { hindi: 'Chandra', devanagari: 'चंद्र' },
  Mars: { hindi: 'Mangal', devanagari: 'मंगल' },
  Mercury: { hindi: 'Budh', devanagari: 'बुध' },
  Jupiter: { hindi: 'Guru', devanagari: 'गुरु' },
  Venus: { hindi: 'Shukra', devanagari: 'शुक्र' },
  Saturn: { hindi: 'Shani', devanagari: 'शनि' },
  Rahu: { hindi: 'Rahu', devanagari: 'राहु' },
  Ketu: { hindi: 'Ketu', devanagari: 'केतु' },
}

/** Formats a zodiac sign name with its Hindi translation, e.g. "Aries (Mesh)" */
export function formatSignWithHindi(signName?: string): string {
  if (!signName) return 'N/A'
  const match = SIGN_HINDI_MAP[signName]
  if (match) {
    return `${signName} (${match.devanagari})`
  }
  return signName
}

/** Formats a planet name with its Hindi translation, e.g. "Sun (Surya)" */
export function formatPlanetWithHindi(planetName?: string): string {
  if (!planetName) return 'N/A'
  const capitalized = planetName.charAt(0).toUpperCase() + planetName.slice(1).toLowerCase()
  const match = PLANET_HINDI_MAP[capitalized]
  if (match) {
    return `${capitalized} (${match.devanagari})`
  }
  return capitalized
}
