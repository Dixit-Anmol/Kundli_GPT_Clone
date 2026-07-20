export type RelationshipType =
  | 'Self'
  | 'Spouse'
  | 'Child'
  | 'Parent'
  | 'Friend'
  | 'Other'

export interface UserProfile {
  id: string // Unique UUID per profile
  name: string
  relationship: RelationshipType
  birthData: {
    fullName: string
    gender: 'male' | 'female' | 'other'
    dateOfBirth?: string
    timeOfBirth?: string
    placeName?: string
    latitude?: number
    longitude?: number
    relationship?: RelationshipType
    mode?: 'exact' | 'partial' | 'prashna'
    timeSlot?: string
    question?: string
    category?: string
  }

  chartData: any // Calculated horoscope data
  computed?: any // Prakriti, elements, lucky, rankings, remedies
  createdAt: string
}

