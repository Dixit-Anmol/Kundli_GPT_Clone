import { useState, useRef, useEffect } from 'react'
import type { UserProfile } from '../../types/profile'
import { getCurrentTier } from '../../utils/subscriptionManager'
import { TIER_CONFIG } from '../../config/subscriptionConfig'
import { getMaxProfilesForTier } from '../../config/subscriptionConfig'

interface NavbarProps {
  profiles?: UserProfile[]
  activeProfileId?: string
  onSelectProfile?: (profileId: string) => void
  onAddNewProfile?: () => void
  onDeleteProfile?: (profileId: string) => void
  onOpenPricing?: () => void
}

export default function Navbar({
  profiles = [],
  activeProfileId,
  onSelectProfile,
  onAddNewProfile,
  onDeleteProfile,
  onOpenPricing,
}: NavbarProps) {
  const [dropdownOpen, setDropdownOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  const currentTier = getCurrentTier()
  const tierConfig = TIER_CONFIG[currentTier]
  const maxProfiles = getMaxProfilesForTier(currentTier)

  const activeProfile = profiles.find((p) => p.id === activeProfileId) || profiles[0]

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setDropdownOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  return (
    <nav className="glass border-b border-outline-variant/50 h-[72px] sticky top-0 z-50 flex items-center justify-between px-4 md:px-10">
      {/* Logo */}
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center text-on-primary shadow-xs">
          <span className="material-symbols-outlined text-2xl" style={{ fontVariationSettings: "'FILL' 1" }}>
            auto_awesome
          </span>
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="font-display text-[24px] sm:text-[28px] leading-tight font-semibold text-primary">
              AstroSutra AI
            </h1>
            {/* Subscription Tier Badge */}
            <button
              onClick={onOpenPricing}
              title="Click to view subscription plans"
              className="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded-full text-white shadow-xs transition-all hover:scale-105 cursor-pointer"
              style={{ backgroundColor: tierConfig.color }}
            >
              {tierConfig.label}
            </button>
          </div>
          <p className="text-[12px] leading-4 font-semibold text-on-surface-variant">
            Modular AI Astrology Platform
          </p>
        </div>
      </div>

      {/* Navigation & Multi-Profile Switcher & Upgrade Button */}
      <div className="flex items-center gap-2.5 sm:gap-3 relative" ref={dropdownRef}>
        {/* Upgrade / Pricing Button */}
        <button
          onClick={onOpenPricing}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-2xl bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white font-bold text-xs shadow-md shadow-orange-500/20 transition-all hover:scale-105 cursor-pointer"
        >
          <span className="material-symbols-outlined text-base" style={{ fontVariationSettings: "'FILL' 1" }}>
            workspace_premium
          </span>
          <span className="hidden sm:inline">Pricing & Plans</span>
          <span className="sm:hidden">Plans</span>
        </button>

        {/* Dynamic Active Profile Trigger Button */}
        {activeProfile ? (
          <button
            onClick={() => setDropdownOpen((prev) => !prev)}
            className="flex items-center gap-2 bg-surface border border-outline-variant hover:border-primary/50 px-3 py-1.5 rounded-2xl shadow-xs transition-all cursor-pointer hover:bg-surface-variant/30"
          >
            <div className="w-7 h-7 bg-primary-fixed rounded-full flex items-center justify-center text-primary text-xs font-bold">
              {activeProfile.name.charAt(0).toUpperCase()}
            </div>
            <div className="text-left hidden sm:block">
              <p className="text-xs font-bold text-on-surface leading-tight">
                {activeProfile.name}
              </p>
              <p className="text-[10px] text-primary font-semibold leading-none">
                {activeProfile.relationship || 'Self'}
              </p>
            </div>
            <span className="material-symbols-outlined text-sm text-on-surface-variant ml-1">
              {dropdownOpen ? 'expand_less' : 'expand_more'}
            </span>
          </button>
        ) : null}

        {/* Profile Switcher Dropdown Menu */}
        {dropdownOpen && (
          <div className="absolute right-0 top-12 w-72 bg-surface border border-outline-variant/80 rounded-2xl shadow-xl py-2 z-50 animate-fade-in-up">
            <div className="px-4 py-2 border-b border-outline-variant/40 flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-on-surface-variant">
                Switch Chart Profile
              </span>
              <span className="text-[10px] font-semibold text-primary bg-primary-fixed px-2 py-0.5 rounded-full">
                {profiles.length}/{maxProfiles} Profiles
              </span>
            </div>

            {/* Profile List */}
            <div className="max-h-60 overflow-y-auto custom-scrollbar py-1">
              {profiles.map((profile) => {
                const isActive = profile.id === activeProfileId
                return (
                  <div
                    key={profile.id}
                    className={`flex items-center justify-between px-3 py-2 hover:bg-surface-variant/40 transition-colors ${
                      isActive ? 'bg-primary-fixed/40' : ''
                    }`}
                  >
                    <button
                      onClick={() => {
                        if (onSelectProfile) onSelectProfile(profile.id)
                        setDropdownOpen(false)
                      }}
                      className="flex-1 flex items-center gap-2.5 text-left cursor-pointer"
                    >
                      <div className="w-8 h-8 rounded-full bg-primary text-white flex items-center justify-center text-xs font-bold shrink-0">
                        {profile.name.charAt(0).toUpperCase()}
                      </div>
                      <div className="min-w-0">
                        <p className="text-xs font-bold text-on-surface truncate">
                          {profile.name} {isActive && <span className="text-primary ml-1">✓</span>}
                        </p>
                        <p className="text-[10px] text-on-surface-variant">
                          {profile.relationship || 'Self'} · {profile.chartData?.metadata?.ascendant_sign || 'Chart Ready'}
                        </p>
                      </div>
                    </button>

                    {/* Delete profile button */}
                    {profiles.length > 1 && onDeleteProfile && (
                      <button
                        onClick={(e) => {
                          e.stopPropagation()
                          if (confirm(`Remove profile for ${profile.name}?`)) {
                            onDeleteProfile(profile.id)
                          }
                        }}
                        title="Remove profile"
                        className="text-on-surface-variant/60 hover:text-red-500 p-1 rounded-lg transition-colors cursor-pointer ml-1"
                      >
                        <span className="material-symbols-outlined text-base">close</span>
                      </button>
                    )}
                  </div>
                )
              })}
            </div>

            {/* Add New Profile CTA */}
            <div className="px-3 pt-2 border-t border-outline-variant/40">
              <button
                onClick={() => {
                  setDropdownOpen(false)
                  if (onAddNewProfile) onAddNewProfile()
                }}
                disabled={profiles.length >= maxProfiles}
                className="w-full flex items-center justify-center gap-2 py-2 px-3 bg-primary text-white rounded-xl text-xs font-bold hover:bg-primary-container disabled:opacity-50 transition-all cursor-pointer shadow-xs"
              >
                <span className="material-symbols-outlined text-base">add</span>
                {profiles.length >= maxProfiles ? `Profile Limit Reached (${maxProfiles})` : 'Add Profile (Family/Friend)'}
              </button>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}
