import { useState } from 'react'

import Navbar from '../components/layout/Navbar'
import TabNavigation, { type TabType } from '../components/dashboard/TabNavigation'
import TabPanel, { type TabCacheItem } from '../components/dashboard/TabPanel'
import type { UserProfile } from '../types/profile'

interface DashboardPageProps {
  chartData: any
  computed?: any
  birthData: any
  sessionId: string
  userId: string
  apiBaseUrl: string
  profiles?: UserProfile[]
  activeProfileId?: string
  onSelectProfile?: (profileId: string) => void
  onAddNewProfile?: () => void
  onDeleteProfile?: (profileId: string) => void
  onResetProfile: () => void
}

export default function DashboardPage({
  chartData,
  computed,
  birthData,
  sessionId,
  userId,
  apiBaseUrl,
  profiles = [],
  activeProfileId,
  onSelectProfile,
  onAddNewProfile,
  onDeleteProfile,
  onResetProfile,
}: DashboardPageProps) {
  const [activeTab, setActiveTab] = useState<TabType>('overview')

  // Persistent cache for tab readings and chat messages across tab switches
  const [tabCache, setTabCache] = useState<Partial<Record<TabType, TabCacheItem>>>({})

  const handleUpdateCache = (tab: TabType, item: TabCacheItem) => {
    setTabCache((prev) => ({ ...prev, [tab]: item }))
  }

  const meta = {
    ascendant_sign: chartData?.metadata?.ascendant_sign || chartData?.ascendant_sign || 'Aries',
    moon_sign: chartData?.metadata?.moon_sign || chartData?.moon_sign || 'Cancer',
    nakshatra: chartData?.metadata?.nakshatra || chartData?.nakshatra || 'Pushya',
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Top Navbar with Dynamic Profile Switcher */}
      <Navbar
        profiles={profiles}
        activeProfileId={activeProfileId}
        onSelectProfile={onSelectProfile}
        onAddNewProfile={onAddNewProfile}
        onDeleteProfile={onDeleteProfile}
      />

      {/* Tab Navigation Sticky Bar */}
      <TabNavigation activeTab={activeTab} onTabChange={setActiveTab} />

      {/* Main Container */}
      <main className="max-w-[1200px] mx-auto px-4 py-8">
        {/* User Greeting Banner */}
        <div className="mb-6 flex flex-wrap items-center justify-between gap-4 bg-surface p-5 rounded-3xl border border-outline-variant/60 shadow-xs">
          <div>
            <div className="flex items-center gap-2">
              <h1 className="font-display text-3xl font-bold text-primary">
                🙏 Welcome, {birthData?.fullName || 'Seeker'}!
              </h1>
              {birthData?.relationship && (
                <span className="text-xs font-semibold text-primary bg-primary-fixed px-2.5 py-0.5 rounded-full border border-primary/20">
                  {birthData.relationship}
                </span>
              )}
            </div>
            <p className="text-xs text-on-surface-variant mt-1 font-medium">
              Ascendant: <strong className="text-primary">{meta.ascendant_sign}</strong> · Moon Sign: <strong className="text-primary">{meta.moon_sign}</strong> · Nakshatra: <strong className="text-primary">{meta.nakshatra}</strong>
            </p>
          </div>

          <button
            onClick={onResetProfile}
            className="text-xs text-on-surface-variant hover:text-primary transition-colors underline underline-offset-4 decoration-outline-variant hover:decoration-primary cursor-pointer"
          >
            Edit Chart Details
          </button>
        </div>

        {/* Tab Panel View */}
        <TabPanel
          key={`${activeProfileId}-${activeTab}`}
          tab={activeTab}
          chartData={chartData}
          computed={computed || chartData?.computed}
          sessionId={sessionId}
          userId={userId}
          apiBaseUrl={apiBaseUrl}
          cachedData={tabCache[activeTab]}
          onUpdateCache={(data) => handleUpdateCache(activeTab, data)}
        />
      </main>
    </div>
  )
}
