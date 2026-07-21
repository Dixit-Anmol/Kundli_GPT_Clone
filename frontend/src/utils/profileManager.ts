import type { UserProfile } from '../types/profile'

const PROFILES_STORAGE_KEY = 'kundli_saved_profiles'
const ACTIVE_PROFILE_KEY = 'kundli_active_profile_id'
export const MAX_PROFILES = 5

export function getSavedProfiles(): UserProfile[] {
  try {
    const data = localStorage.getItem(PROFILES_STORAGE_KEY)
    if (!data) return []
    const parsed = JSON.parse(data)
    return Array.isArray(parsed) ? parsed : []
  } catch (err) {
    console.error('Failed to parse saved profiles from localStorage:', err)
    return []
  }
}

export function getActiveProfileId(): string | null {
  return localStorage.getItem(ACTIVE_PROFILE_KEY)
}

export function setActiveProfileId(id: string): void {
  localStorage.setItem(ACTIVE_PROFILE_KEY, id)
}

export function saveProfile(profile: UserProfile): UserProfile[] {
  const current = getSavedProfiles()
  const existingIndex = current.findIndex((p) => p.id === profile.id)

  let updated: UserProfile[]
  if (existingIndex >= 0) {
    // Update existing profile
    updated = [...current]
    updated[existingIndex] = profile
  } else {
    // Add new profile (if max limit reached, displace oldest)
    if (current.length >= MAX_PROFILES) {
      updated = [profile, ...current.slice(0, MAX_PROFILES - 1)]
    } else {
      updated = [profile, ...current]
    }
  }

  try {
    localStorage.setItem(PROFILES_STORAGE_KEY, JSON.stringify(updated))
    setActiveProfileId(profile.id)
  } catch (err) {
    console.error('Failed to save profile to localStorage:', err)
  }
  return updated
}


export function deleteProfile(id: string): UserProfile[] {
  const current = getSavedProfiles()
  const updated = current.filter((p) => p.id !== id)
  localStorage.setItem(PROFILES_STORAGE_KEY, JSON.stringify(updated))

  // If deleted profile was active, switch active profile to first remaining
  if (getActiveProfileId() === id) {
    if (updated.length > 0) {
      setActiveProfileId(updated[0].id)
    } else {
      localStorage.removeItem(ACTIVE_PROFILE_KEY)
    }
  }

  return updated
}
