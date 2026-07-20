import { useState } from 'react'
import BirthTimeRectificationWizard from './BirthTimeRectificationWizard'

interface PrashnaDashboardViewProps {
  chartData: any
  onApplyRectifiedTime?: (rectifiedTime: string) => void
}

export default function PrashnaDashboardView({
  chartData,
  onApplyRectifiedTime,
}: PrashnaDashboardViewProps) {
  const [showWizard, setShowWizard] = useState(false)

  const mode = chartData?.mode || 'prashna'
  const isPrashna = mode === 'prashna'
  const isPartial = mode === 'partial'

  const prashnaLagna = chartData?.prashna_lagna || {}
  const panchanga = chartData?.panchanga || {}
  const planets = chartData?.planets || {}
  const transits = chartData?.transits || planets

  const moonData = planets.moon || {}
  const moonSign = isPartial ? chartData?.moon_sign : moonData.sign || 'Active Sign'
  const nakshatra = isPartial ? chartData?.nakshatra : panchanga.nakshatra || 'Active Nakshatra'

  const handleEstimateConfirmed = (timeStr: string) => {
    setShowWizard(false)
    if (onApplyRectifiedTime) {
      onApplyRectifiedTime(timeStr)
    }
  }

  return (
    <div className="space-y-6 animate-fade-in-up">
      {/* Disclaimer Banner */}
      <div className="bg-amber-500/10 border border-amber-500/30 p-4 rounded-3xl flex items-start gap-3 text-amber-950">
        <span className="material-symbols-outlined text-amber-600 text-2xl shrink-0 mt-0.5">
          info
        </span>
        <div className="space-y-1 text-xs">
          <p className="font-bold text-amber-900 text-sm">
            {isPrashna
              ? '🔮 Prashna Horary Guidance Active'
              : '🪐 Estimated Horoscope Mode Active'}
          </p>
          <p className="text-amber-900/90 leading-relaxed font-medium">
            {isPrashna
              ? 'This analysis is calculated using Prashna Astrology (Horary) based on the exact moment and location of your question. Since birth details are unavailable, Lagna and natal house cusps are excluded.'
              : 'This analysis is based on approximate planetary positions from your partial birth details. Providing your birth time later will unlock a complete Janma Kundli with exact Lagna and House Cusps.'}
          </p>
          <div className="pt-1 flex flex-wrap items-center gap-3">
            <span className="text-[11px] font-bold text-amber-800">
              {isPartial ? `Confidence Level: ${chartData?.confidence_level || 'Medium'}` : 'Exact Question Moment Active'}
            </span>
            <button
              onClick={() => setShowWizard(true)}
              className="text-[11px] font-extrabold text-primary bg-surface border border-outline-variant/60 px-3 py-1 rounded-full shadow-xs hover:bg-surface-variant cursor-pointer flex items-center gap-1"
            >
              <span className="material-symbols-outlined text-xs">auto_fix_high</span>
              Estimate My Birth Time
            </button>
          </div>
        </div>
      </div>

      {/* Main Guidance Card */}
      <div className="celestial-card p-6 rounded-3xl bg-surface border border-outline-variant/60 shadow-xs space-y-4">
        <div className="flex items-center justify-between border-b border-outline-variant/40 pb-3">
          <h4 className="font-display text-xl font-bold text-primary flex items-center gap-2">
            <span className="material-symbols-outlined text-primary text-2xl">
              {isPrashna ? 'psychology' : 'explore'}
            </span>
            {isPrashna ? '🔮 Prashna Horary Guidance' : '🪐 Estimated Horoscope Overview'}
          </h4>
          <span className="text-xs font-bold text-primary bg-primary-fixed px-3 py-1 rounded-full">
            {isPrashna ? `Lagna: ${prashnaLagna.sign || 'Horary'}` : `Moon: ${moonSign}`}
          </span>
        </div>

        {isPrashna ? (
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3.5">
            <div className="bg-surface-variant/30 p-3.5 rounded-2xl border border-outline-variant/40 space-y-1">
              <span className="text-[10px] font-semibold text-on-surface-variant block">Prashna Lagna</span>
              <strong className="text-primary text-sm block font-bold">{prashnaLagna.sign} ({prashnaLagna.degree}°)</strong>
              <span className="text-[11px] text-on-surface-variant">Lord: {prashnaLagna.lord}</span>
            </div>

            <div className="bg-surface-variant/30 p-3.5 rounded-2xl border border-outline-variant/40 space-y-1">
              <span className="text-[10px] font-semibold text-on-surface-variant block">Moment Panchanga</span>
              <strong className="text-primary text-sm block font-bold">Hora: {panchanga.hora}</strong>
              <span className="text-[11px] text-on-surface-variant">Tithi: {panchanga.tithi}</span>
            </div>

            <div className="bg-surface-variant/30 p-3.5 rounded-2xl border border-outline-variant/40 space-y-1">
              <span className="text-[10px] font-semibold text-on-surface-variant block">Horary Moon</span>
              <strong className="text-primary text-sm block font-bold">{moonData.sign}</strong>
              <span className="text-[11px] text-on-surface-variant">Nakshatra: {nakshatra}</span>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3.5">
            <div className="bg-surface-variant/30 p-3.5 rounded-2xl border border-outline-variant/40 space-y-1">
              <span className="text-[10px] font-semibold text-on-surface-variant block">Estimated Moon Sign</span>
              <strong className="text-primary text-sm block font-bold">{moonSign}</strong>
              <span className="text-[11px] text-on-surface-variant">Stability: {chartData?.moon_stable ? 'Stable' : 'Approximate'}</span>
            </div>

            <div className="bg-surface-variant/30 p-3.5 rounded-2xl border border-outline-variant/40 space-y-1">
              <span className="text-[10px] font-semibold text-on-surface-variant block">Nakshatra</span>
              <strong className="text-primary text-sm block font-bold">{nakshatra}</strong>
              <span className="text-[11px] text-on-surface-variant">Confidence: {chartData?.confidence_level}</span>
            </div>

            <div className="bg-surface-variant/30 p-3.5 rounded-2xl border border-outline-variant/40 space-y-1">
              <span className="text-[10px] font-semibold text-on-surface-variant block">Calculations Status</span>
              <strong className="text-primary text-xs block font-bold">Planetary Signs Exact</strong>
              <span className="text-[11px] text-on-surface-variant">Lagna/Houses Excluded</span>
            </div>
          </div>
        )}
      </div>

      {/* Grid of UI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* 🌙 Current Moon Influence Card */}
        <div className="celestial-card p-5 rounded-3xl bg-surface border border-outline-variant/60 shadow-xs space-y-2">
          <div className="flex items-center gap-2 text-primary font-bold text-sm">
            <span className="material-symbols-outlined text-amber-500 text-xl">dark_mode</span>
            <h5>🌙 Current Moon Influence</h5>
          </div>
          <p className="text-xs text-on-surface-variant leading-relaxed">
            The Moon is currently transiting <strong>{moonSign}</strong> in <strong>{nakshatra}</strong>. This positioning governs your intuitive clarity, emotional stamina, and mental absorption for active queries.
          </p>
        </div>

        {/* 🚀 Current Planetary Transits (Gochar) Card */}
        <div className="celestial-card p-5 rounded-3xl bg-surface border border-outline-variant/60 shadow-xs space-y-2">
          <div className="flex items-center gap-2 text-primary font-bold text-sm">
            <span className="material-symbols-outlined text-emerald-600 text-xl">rocket_launch</span>
            <h5>🚀 Active Planetary Transits (Gochar)</h5>
          </div>
          <p className="text-xs text-on-surface-variant leading-relaxed">
            Jupiter in <strong>{transits.jupiter?.sign || 'Aptitude'}</strong> and Saturn in <strong>{transits.saturn?.sign || 'Focus'}</strong> provide key transit support. Major movements favor methodical execution over impulsive shifts.
          </p>
        </div>

        {/* ⚡ Today's Opportunities Card */}
        <div className="celestial-card p-5 rounded-3xl bg-surface border border-outline-variant/60 shadow-xs space-y-2">
          <div className="flex items-center gap-2 text-emerald-900 font-bold text-sm">
            <span className="material-symbols-outlined text-emerald-600 text-xl">bolt</span>
            <h5>⚡ Active Opportunities</h5>
          </div>
          <ul className="text-xs text-on-surface-variant space-y-1">
            <li className="flex items-center gap-2">
              <span className="material-symbols-outlined text-emerald-600 text-sm">check_circle</span>
              Focus on strategic planning and first-principles analysis
            </li>
            <li className="flex items-center gap-2">
              <span className="material-symbols-outlined text-emerald-600 text-sm">check_circle</span>
              Seek direct mentor guidance and dialogic consultation
            </li>
          </ul>
        </div>

        {/* ⚠ Things to Avoid Card */}
        <div className="celestial-card p-5 rounded-3xl bg-surface border border-outline-variant/60 shadow-xs space-y-2">
          <div className="flex items-center gap-2 text-amber-950 font-bold text-sm">
            <span className="material-symbols-outlined text-amber-600 text-xl">warning</span>
            <h5>⚠ Things to Avoid Right Now</h5>
          </div>
          <ul className="text-xs text-on-surface-variant space-y-1">
            <li className="flex items-center gap-2">
              <span className="material-symbols-outlined text-amber-600 text-sm">error</span>
              Avoid rush decisions without verifying foundational facts
            </li>
            <li className="flex items-center gap-2">
              <span className="material-symbols-outlined text-amber-600 text-sm">error</span>
              Do not rely on unverified rumors or emotional impulses
            </li>
          </ul>
        </div>
      </div>

      {/* 🕉 Suggested Remedies Card */}
      <div className="celestial-card p-6 rounded-3xl bg-surface border border-outline-variant/60 shadow-xs space-y-3">
        <div className="flex items-center gap-2 text-primary font-bold text-base">
          <span className="material-symbols-outlined text-primary text-xl">self_improvement</span>
          <h5>🕉 Suggested Remedial Practices</h5>
        </div>
        <p className="text-xs text-on-surface-variant leading-relaxed">
          Simple mindfulness practice: Engage in 5 minutes of Pranayama breath control every morning. Recite <i>Om Namah Shivaya</i> or your preferred mantra to ground mental composure during planetary transits.
        </p>
      </div>

      {/* Wizard Modal */}
      {showWizard && (
        <BirthTimeRectificationWizard
          onClose={() => setShowWizard(false)}
          onEstimateConfirmed={handleEstimateConfirmed}
        />
      )}
    </div>
  )
}
