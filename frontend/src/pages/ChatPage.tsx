import { useState, useEffect } from 'react'
import Navbar from '../components/layout/Navbar'
import BirthDetailsForm, { type BirthData } from '../components/chat/BirthDetailsForm'
import ComputingCard from '../components/chat/ComputingCard'

import AssistantMessage from '../components/chat/AssistantMessage'
import DashboardPage from './DashboardPage'
import PricingPage from './PricingPage'

import type { UserProfile } from '../types/profile'
import {
  getSavedProfiles,
  getActiveProfileId,
  setActiveProfileId,
  saveProfile,
  deleteProfile,
} from '../utils/profileManager'

type ChatStep = 'loading' | 'welcome' | 'birthplace' | 'computing' | 'ready'

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000'
    : 'https://kundli-gpt-clone-back.onrender.com')


export default function ChatPage() {
  const [sessionId] = useState(() => Math.random().toString(36).substring(7))
  const [step, setStep] = useState<ChatStep>('loading')
  const [showPricing, setShowPricing] = useState(false)

  // Multi-profile state
  const [profiles, setProfiles] = useState<UserProfile[]>([])
  const [activeId, setActiveId] = useState<string | null>(null)

  // Current active profile's chart and birth data
  const [birthData, setBirthData] = useState<BirthData | null>(null)
  const [chartData, setChartData] = useState<any>(null)

  // -----------------------------------------------------------------------
  // On Mount — Load saved profiles from localStorage & hydrate from backend if needed
  // -----------------------------------------------------------------------
  useEffect(() => {
    const saved = getSavedProfiles()
    const savedActiveId = getActiveProfileId()

    setProfiles(saved)

    if (saved.length > 0) {
      const active = saved.find((p) => p.id === savedActiveId) || saved[0]
      setActiveId(active.id)
      setActiveProfileId(active.id)
      setBirthData(active.birthData || null)

      if (active.chartData && active.chartData.ascendant_sign) {
        setChartData(active.chartData)
        setStep('ready')
      } else if (active.id) {
        // Attempt to load from backend profile store
        fetch(`${API_BASE_URL}/api/profile/${active.id}`)
          .then((res) => (res.ok ? res.json() : null))
          .then((data) => {
            if (data && data.exists && data.chart_summary) {
              setChartData(data.chart_summary)
              setStep('ready')
            } else if (active.birthData) {
              // Re-trigger chart calculation from saved birth details
              handleBirthSubmit(active.birthData, active.id)
            } else {
              setStep('ready')
            }
          })
          .catch(() => setStep('ready'))
      } else {
        setStep('ready')
      }
    } else {
      setStep('welcome')
    }
  }, [])

  // -----------------------------------------------------------------------
  // Switch active profile
  // -----------------------------------------------------------------------
  const handleSelectProfile = (profileId: string) => {
    const selected = profiles.find((p) => p.id === profileId)
    if (!selected) return

    setActiveId(selected.id)
    setActiveProfileId(selected.id)
    setBirthData(selected.birthData || null)

    if (selected.chartData && selected.chartData.ascendant_sign) {
      setChartData(selected.chartData)
      setStep('ready')
    } else {
      // Re-calculate if missing chart data
      if (selected.birthData) handleBirthSubmit(selected.birthData, selected.id)
    }
  }

  // -----------------------------------------------------------------------
  // Add new profile (triggers welcome form)
  // -----------------------------------------------------------------------
  const handleAddNewProfile = () => {
    setActiveId(null)
    setBirthData(null)
    setChartData(null)
    setStep('welcome')
  }

  // -----------------------------------------------------------------------
  // Delete profile
  // -----------------------------------------------------------------------
  const handleDeleteProfile = (profileId: string) => {
    const updated = deleteProfile(profileId)
    setProfiles(updated)

    if (updated.length === 0) {
      setActiveId(null)
      setBirthData(null)
      setChartData(null)
      setStep('welcome')
    } else if (activeId === profileId) {
      handleSelectProfile(updated[0].id)
    }
  }

  // -----------------------------------------------------------------------
  // Form submission -> Calculate Kundli chart
  // -----------------------------------------------------------------------
  const handleBirthSubmit = async (data: BirthData, targetProfileId?: string) => {
    setBirthData(data)
    setStep('computing')

    const newProfileId = targetProfileId || `prof_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`

    try {
      const payload: any = {
        name: data.fullName || 'Seeker',
        latitude: data.latitude || 28.6139,
        longitude: data.longitude || 77.209,
        session_id: sessionId,
        user_id: newProfileId,
        mode: data.mode || 'exact',
        time_slot: data.timeSlot || 'unknown',
        question: data.question || null,
        category: data.category || 'general',
      }

      if (data.dateOfBirth) payload.date_str = data.dateOfBirth
      if (data.timeOfBirth) payload.time_str = data.timeOfBirth

      const response = await fetch(`${API_BASE_URL}/api/chart`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })

      if (!response.ok) {
        throw new Error('Failed to calculate birth chart')
      }

      const resData = await response.json()
      const chart = resData.natal || resData

      setBirthData(data)
      setChartData(chart)

      // Save to multi-profile storage
      const newProfile: UserProfile = {
        id: newProfileId,
        name: data.fullName || 'Seeker',
        relationship: data.relationship || 'Self',
        birthData: data,
        chartData: chart,
        computed: resData.computed || chart.computed,
        createdAt: new Date().toISOString(),
      }

      const updatedProfiles = saveProfile(newProfile)
      setProfiles(updatedProfiles)
      setActiveId(newProfileId)
      setActiveProfileId(newProfileId)
      setStep('ready')
    } catch (error) {
      console.error('Error submitting birth details:', error)
      alert('Failed to compute birth chart. Please check your internet connection and backend status.')
      setStep('welcome')
    }
  }

  // -----------------------------------------------------------------------
  // Render Pricing Page if user clicked Pricing
  // -----------------------------------------------------------------------
  if (showPricing) {
    return <PricingPage onNavigateBack={() => setShowPricing(false)} />
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
        onOpenPricing={() => setShowPricing(true)}
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
        onOpenPricing={() => setShowPricing(true)}
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
                : '🙏 Namaste! Welcome to AstroSutra AI. I will calculate your personalized Vedic birth chart and store up to 5 profiles for you and your loved ones.'}
            </AssistantMessage>
          )}

          {/* Birth Details & Location Form (Single Page) */}
          {step === 'welcome' && <BirthDetailsForm onSubmit={handleBirthSubmit} />}

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
