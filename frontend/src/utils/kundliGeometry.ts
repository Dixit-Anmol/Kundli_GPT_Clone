/**
 * North Indian Kundli Chart Geometry and House Coordinates
 */

export interface HousePos {
  signX: number
  signY: number
  planetX: number
  planetY: number
  name: string
  hindiName: string
}

export const SIGN_NUMBER_MAP: Record<string, number> = {
  Aries: 1,
  Taurus: 2,
  Gemini: 3,
  Cancer: 4,
  Leo: 5,
  Virgo: 6,
  Libra: 7,
  Scorpio: 8,
  Sagittarius: 9,
  Capricorn: 10,
  Aquarius: 11,
  Pisces: 12,
}

export const PLANET_INFO_MAP: Record<
  string,
  { short: string; hindi: string; icon: string; color: string }
> = {
  sun: { short: 'Su', hindi: 'Surya', icon: '☀️', color: '#E67E22' },
  moon: { short: 'Mo', hindi: 'Chandra', icon: '🌙', color: '#3498DB' },
  mars: { short: 'Ma', hindi: 'Mangal', icon: '♂️', color: '#E74C3C' },
  mercury: { short: 'Me', hindi: 'Budh', icon: '☿', color: '#2ECC71' },
  jupiter: { short: 'Ju', hindi: 'Guru', icon: '♃', color: '#F1C40F' },
  venus: { short: 'Ve', hindi: 'Shukra', icon: '♀', color: '#9B59B6' },
  saturn: { short: 'Sa', hindi: 'Shani', icon: '♄', color: '#34495E' },
  rahu: { short: 'Ra', hindi: 'Rahu', icon: '☊', color: '#7F8C8D' },
  ketu: { short: 'Ke', hindi: 'Ketu', icon: '☋', color: '#95A5A6' },
}

/** 12 North Indian House Coordinates on a 400x400 SVG Canvas */
export const NORTH_INDIAN_HOUSES: Record<number, HousePos> = {
  1: { signX: 200, signY: 35, planetX: 200, planetY: 130, name: '1st House (Lagna)', hindiName: 'Tanu Bhava' },
  2: { signX: 75, signY: 25, planetX: 100, planetY: 55, name: '2nd House (Wealth)', hindiName: 'Dhana Bhava' },
  3: { signX: 25, signY: 75, planetX: 55, planetY: 100, name: '3rd House (Siblings)', hindiName: 'Sahaja Bhava' },
  4: { signX: 30, signY: 200, planetX: 110, planetY: 200, name: '4th House (Mother & Comfort)', hindiName: 'Sukha Bhava' },
  5: { signX: 25, signY: 325, planetX: 55, planetY: 300, name: '5th House (Intelligence & Children)', hindiName: 'Putra Bhava' },
  6: { signX: 75, signY: 375, planetX: 100, planetY: 345, name: '6th House (Enemies & Health)', hindiName: 'Ari Bhava' },
  7: { signX: 200, signY: 365, planetX: 200, planetY: 275, name: '7th House (Marriage)', hindiName: 'Kalatra Bhava' },
  8: { signX: 325, signY: 375, planetX: 300, planetY: 345, name: '8th House (Longevity)', hindiName: 'Randhra Bhava' },
  9: { signX: 375, signY: 325, planetX: 345, planetY: 300, name: '9th House (Dharma & Fortune)', hindiName: 'Bhagya Bhava' },
  10: { signX: 370, signY: 200, planetX: 290, planetY: 200, name: '10th House (Career & Status)', hindiName: 'Karma Bhava' },
  11: { signX: 375, signY: 75, planetX: 345, planetY: 100, name: '11th House (Gains)', hindiName: 'Labha Bhava' },
  12: { signX: 325, signY: 25, planetX: 300, planetY: 55, name: '12th House (Moksha & Loss)', hindiName: 'Vyaya Bhava' },
}


/** Calculate sign number (1 to 12) for a given house index (1 to 12) based on ascendant sign */
export function getHouseSignNumber(houseNum: number, ascendantSign: string): number {
  const ascNum = SIGN_NUMBER_MAP[ascendantSign] || 1
  const signNum = ((ascNum - 1 + (houseNum - 1)) % 12) + 1
  return signNum
}
