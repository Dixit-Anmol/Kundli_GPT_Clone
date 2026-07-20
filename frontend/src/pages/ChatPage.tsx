import { useState, useEffect } from 'react'
import Navbar from '../components/layout/Navbar'
import BirthDetailsForm, { type BirthData } from '../components/chat/BirthDetailsForm'
import BirthplaceMap from '../components/chat/BirthplaceMap'
import ComputingCard from '../components/chat/ComputingCard'
import AssistantMessage from '../components/chat/AssistantMessage'
import DashboardPage from './DashboardPage'

import type { UserProfile } from '../types/profile'
import {
  getSavedProfiles,
  getActiveProfileId,
  setActiveProfileId,
  saveProfile,
  deleteProfile,
  MAX_PROFILES,
} from '../utils/profileManager'

type ChatStep = 'loading' | 'welcome' | 'birthplace' | 'computing' | 'ready'

const API_BASE_URL =
  window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000'
    : 'https://kundli-gpt-clone-back.onrender.com'

export default function ChatPage() {
  const [sessionId] = useState(() => Math.random().toString(36).substring(7))
  const [step, setStep] = useState<ChatStep>('loading')

  // Multi-profile state
  const [profiles, setProfiles] = useState<UserProfile[]>([])
  const [activeId, setActiveId] = useState<string | null>(null)

  // Current active profile's chart and birth data
  const [birthData, setBirthData] = useState<BirthData | null>(null)
  const [chartData, setChartData] = useState<any>(null)

  // -----------------------------------------------------------------------
  // On Mount — Load saved profiles from localStorage
  // -----------------------------------------------------------------------
  useEffect(() => {
    const saved = getSavedProfiles()
    const savedActiveId = getActiveProfileId()

    setProfiles(saved)

    if (saved.length > 0) {
      const active = saved.find((p) => p.id === savedActiveId) || saved[0]
      setActiveId(active.id)
      setActiveProfileId(active.id)
      setBirthData(active.birthData)
      setChartData(active.chartData)
      setStep('ready')
    } else {
      setStep('welcome')
    }
  }, [])

  // -----------------------------------------------------------------------
  // Birth details form submission
  // -----------------------------------------------------------------------
  const handleBirthSubmit = (data: BirthData) => {
    setBirthData(data)
    setStep('birthplace')
  }

  // -----------------------------------------------------------------------
  // Birthplace confirmation → chart computation + multi-profile persistence
  // -----------------------------------------------------------------------
  const handleBirthplaceConfirm = async (_placeName: string, lat: number, lon: number) => {
    if (!birthData) return
    setStep('computing')

    const newProfileId = crypto.randomUUID()

    try {
      const timeStr = birthData.timeOfBirth
        ? birthData.timeOfBirth.length === 5
          ? `${birthData.timeOfBirth}:00`
          : birthData.timeOfBirth
        : '12:00:00'

      // 1. Fetch real chart data from FastAPI backend
      const response = await fetch(`${API_BASE_URL}/api/chart`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: birthData.fullName || 'Seeker',
          date_str: birthData.dateOfBirth || new Date().toISOString().split('T')[0],
          time_str: timeStr,
          latitude: lat,
          longitude: lon,
          session_id: sessionId,
          user_id: newProfileId,
          mode: birthData.mode || 'exact',
          time_slot: birthData.timeSlot || 'unknown',
          question: birthData.question,
          category: birthData.category,
        }),
      })


      if (response.ok) {
        const data = await response.json()

        const newProfile: UserProfile = {
          id: newProfileId,
          name: birthData.fullName,
          relationship: birthData.relationship || 'Self',
          birthData: {
            ...birthData,
            placeName: _placeName,
            latitude: lat,
            longitude: lon,
          },
          chartData: data,
          computed: data.computed,
          createdAt: new Date().toISOString(),
        }

        const updatedProfiles = saveProfile(newProfile)
        setProfiles(updatedProfiles)
        setActiveId(newProfileId)
        setChartData(data)
        setStep('ready')
      }
    } catch (err) {
      console.error('Failed to calculate horoscope chart:', err)
      // Fallback offline profile creation
      const mockChart = {
        name: birthData.fullName,
        ascendant_sign: 'Scorpio',
        moon_sign: 'Aries',
        nakshatra: 'Ashwini',
        pada: 2,
        yogas: [{ name: 'Budhaditya Yoga', meaning: 'Sun-Mercury conjunction in 10th house' }],
        doshas: { manglik: { is_present: true, description: 'Mars in 4th house' } },
        planets: {},
        houses: {},
      }

      const fallbackProfile: UserProfile = {
        id: newProfileId,
        name: birthData.fullName,
        relationship: birthData.relationship || 'Self',
        birthData: {
          ...birthData,
          placeName: _placeName,
          latitude: lat,
          longitude: lon,
        },
        chartData: mockChart,
        createdAt: new Date().toISOString(),
      }

      const updatedProfiles = saveProfile(fallbackProfile)
      setProfiles(updatedProfiles)
      setActiveId(newProfileId)
      setChartData(mockChart)
      setStep('ready')
    }
  }

  // -----------------------------------------------------------------------
  // Switch Active Profile (from Navbar Dropdown)
  // -----------------------------------------------------------------------
  const handleSelectProfile = (profileId: string) => {
    const target = profiles.find((p) => p.id === profileId)
    if (!target) return
    setActiveId(profileId)
    setActiveProfileId(profileId)
    setBirthData(target.birthData)
    setChartData(target.chartData)
    setStep('ready')
  }

  // -----------------------------------------------------------------------
  // Add New Profile (from Navbar Dropdown)
  // -----------------------------------------------------------------------
  const handleAddNewProfile = () => {
    if (profiles.length >= MAX_PROFILES) {
      alert(`You have reached the maximum profile limit (${MAX_PROFILES}). Remove an existing profile to add a new one.`)
      return
    }
    setBirthData(null)
    setChartData(null)
    setStep('welcome')
  }

  // -----------------------------------------------------------------------
  // Delete Profile (from Navbar Dropdown)
  // -----------------------------------------------------------------------
  const handleDeleteProfile = async (profileId: string) => {
    try {
      await fetch(`${API_BASE_URL}/api/profile/${profileId}`, { method: 'DELETE' })
    } catch {
      // Ignore network errors
    }

    const updated = deleteProfile(profileId)
    setProfiles(updated)

    if (updated.length > 0) {
      const active = updated.find((p) => p.id === getActiveProfileId()) || updated[0]
      setActiveId(active.id)
      setActiveProfileId(active.id)
      setBirthData(active.birthData)
      setChartData(active.chartData)
      setStep('ready')
    } else {
      setActiveId(null)
      setBirthData(null)
      setChartData(null)
      setStep('welcome')
    }
  }

  // -----------------------------------------------------------------------
  // Render Dashboard Page if Chart Ready
  // -----------------------------------------------------------------------
  if (step === 'ready' && chartData && activeId) {
    return (
      <DashboardPage
        chartData={chartData}
        computed={chartData.computed}
        birthData={birthData}
        sessionId={sessionId}
        userId={activeId}
        apiBaseUrl={API_BASE_URL}
        profiles={profiles}
        activeProfileId={activeId}
        onSelectProfile={handleSelectProfile}
        onAddNewProfile={handleAddNewProfile}
        onDeleteProfile={handleDeleteProfile}
        onResetProfile={() => setStep('welcome')}
      />
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar
        profiles={profiles}
        activeProfileId={activeId || undefined}
        onSelectProfile={handleSelectProfile}
        onAddNewProfile={handleAddNewProfile}
        onDeleteProfile={handleDeleteProfile}
      />

      <main className="relative z-10 max-w-[800px] mx-auto px-4 pt-12 pb-[180px]">
        <div className="space-y-6">
          {/* Loading State */}
          {step === 'loading' && (
            <AssistantMessage icon="hourglass_top">
              <div className="flex items-center gap-3">
                <div className="w-2 h-2 bg-primary rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-primary rounded-full animate-bounce delay-100" />
                <div className="w-2 h-2 bg-primary rounded-full animate-bounce delay-200" />
                <span className="text-on-surface-variant ml-2">Checking saved horoscope profiles…</span>
              </div>
            </AssistantMessage>
          )}

          {/* Welcome Message */}
          {step !== 'loading' && (
            <AssistantMessage icon="star">
              {profiles.length > 0
                ? '🙏 Namaste! Add a new profile for a family member or friend to analyze their Vedic birth chart.'
                : '🙏 Namaste! Welcome to Kundli AI. I will calculate your personalized Vedic birth chart and store up to 5 profiles for you and your loved ones.'}
            </AssistantMessage>
          )}

          {/* Birth Details Form */}
          {step === 'welcome' && <BirthDetailsForm onSubmit={handleBirthSubmit} />}

          {/* Birthplace Selection */}
          {(step === 'birthplace' || step === 'computing') && (
            <>
              <AssistantMessage icon="location_on">
                Great{birthData ? `, ${birthData.fullName}` : ''}! Now I need the birthplace location.
                Please search the city or drop a pin on the map.
              </AssistantMessage>
              {step === 'birthplace' && <BirthplaceMap onConfirm={handleBirthplaceConfirm} />}
            </>
          )}

          {/* Computing State */}
          {step === 'computing' && (
            <ComputingCard
              steps={[
                { label: 'Finding Sidereal Planetary Positions', status: 'active', progress: 45 },
                { label: 'Calculating Houses & Lagna', status: 'waiting' },
                { label: 'Computing Nakshatras & Yogas', status: 'waiting' },
              ]}
            />
          )}
        </div>
      </main>
    </div>
  )
}
