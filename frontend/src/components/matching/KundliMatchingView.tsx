import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import type { UserProfile } from '../../types/profile'

interface KundliMatchingViewProps {
  profiles: UserProfile[]
  apiBaseUrl: string
  sessionId: string
}

interface PersonFormState {
  mode: 'profile' | 'manual'
  profileId: string
  fullName: string
  dateOfBirth: string
  timeOfBirth: string
  placeName: string
  latitude: number
  longitude: number
}

export default function KundliMatchingView({
  profiles = [],
  apiBaseUrl,
  sessionId,
}: KundliMatchingViewProps) {
  // Person A state (defaults to first profile if available)
  const [personA, setPersonA] = useState<PersonFormState>({
    mode: profiles.length > 0 ? 'profile' : 'manual',
    profileId: profiles.length > 0 ? profiles[0].id : '',
    fullName: profiles.length > 0 ? profiles[0].name : 'Partner A',
    dateOfBirth: '1998-05-15',
    timeOfBirth: '10:30',
    placeName: 'New Delhi, India',
    latitude: 28.6139,
    longitude: 77.209,
  })

  // Person B state (defaults to second profile if available)
  const [personB, setPersonB] = useState<PersonFormState>({
    mode: profiles.length > 1 ? 'profile' : 'manual',
    profileId: profiles.length > 1 ? profiles[1].id : '',
    fullName: profiles.length > 1 ? profiles[1].name : 'Partner B',
    dateOfBirth: '2000-08-20',
    timeOfBirth: '14:15',
    placeName: 'Mumbai, India',
    latitude: 19.076,
    longitude: 72.8777,
  })

  const [loading, setLoading] = useState(false)
  const [matchResult, setMatchResult] = useState<any>(null)
  const [aiReport, setAiReport] = useState<string>('')

  const handleMatch = async () => {
    setLoading(true)
    try {
      const payload = {
        session_id: sessionId,
        person_a: {
          profile_id: personA.mode === 'profile' ? personA.profileId : null,
          name: personA.fullName || 'Partner A',
          date_str: personA.dateOfBirth,
          time_str: personA.timeOfBirth,
          latitude: personA.latitude,
          longitude: personA.longitude,
        },
        person_b: {
          profile_id: personB.mode === 'profile' ? personB.profileId : null,
          name: personB.fullName || 'Partner B',
          date_str: personB.dateOfBirth,
          time_str: personB.timeOfBirth,
          latitude: personB.latitude,
          longitude: personB.longitude,
        },
      }

      const res = await fetch(`${apiBaseUrl}/api/match-kundli`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })

      if (res.ok) {
        const data = await res.json()
        setMatchResult(data.matching)
        setAiReport(data.ai_report)
      } else {
        alert('Failed to compute Kundli Matching. Please check your backend connection.')
      }
    } catch (err) {
      console.error('Kundli matching failed:', err)
      alert('Error connecting to Kundli Matching server.')
    } finally {
      setLoading(false)
    }
  }

  const factors = matchResult?.ashtakoota?.factors || {}
  const totalScore = matchResult?.ashtakoota?.total_score || 0

  return (
    <div className="space-y-6 animate-fade-in-up">
      {/* Header Banner */}
      <div className="celestial-card p-6 rounded-3xl bg-surface border border-outline-variant/60 shadow-xs">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 bg-primary-fixed rounded-2xl flex items-center justify-center text-primary font-bold shadow-xs shrink-0">
            <span className="material-symbols-outlined text-3xl" style={{ fontVariationSettings: "'FILL' 1" }}>
              diversity_2
            </span>
          </div>
          <div>
            <h2 className="font-display text-3xl font-bold text-primary">
              Vedic Kundli Matching (Gun Milan)
            </h2>
            <p className="text-xs text-on-surface-variant font-medium mt-0.5">
              Ashtakoota 36 Guna Milan · Manglik Alignment · Nadi/Bhakoot/Rajju Doshas · Yoni Compatibility & AI Synthesis
            </p>
          </div>
        </div>
      </div>

      {/* Dual Partner Selection Form */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Person A Selector Card */}
        <div className="bg-surface p-6 rounded-3xl border border-outline-variant/60 shadow-xs">
          <div className="flex items-center justify-between mb-4 border-b border-outline-variant/40 pb-3">
            <div className="flex items-center gap-2">
              <span className="material-symbols-outlined text-primary text-xl">person</span>
              <h3 className="font-display text-xl font-bold text-primary">Partner A (Boy / Primary)</h3>
            </div>
            {profiles.length > 0 && (
              <div className="flex bg-surface-variant/40 p-1 rounded-xl text-xs font-semibold">
                <button
                  onClick={() => setPersonA((prev) => ({ ...prev, mode: 'profile' }))}
                  className={`px-3 py-1 rounded-lg transition-all cursor-pointer ${
                    personA.mode === 'profile' ? 'bg-primary text-white shadow-xs' : 'text-on-surface-variant'
                  }`}
                >
                  Saved Profile
                </button>
                <button
                  onClick={() => setPersonA((prev) => ({ ...prev, mode: 'manual' }))}
                  className={`px-3 py-1 rounded-lg transition-all cursor-pointer ${
                    personA.mode === 'manual' ? 'bg-primary text-white shadow-xs' : 'text-on-surface-variant'
                  }`}
                >
                  Enter Details
                </button>
              </div>
            )}
          </div>

          {personA.mode === 'profile' && profiles.length > 0 ? (
            <div>
              <label className="text-xs font-bold text-on-surface-variant block mb-1.5">Select Profile</label>
              <select
                value={personA.profileId}
                onChange={(e) => {
                  const id = e.target.value
                  const p = profiles.find((item) => item.id === id)
                  setPersonA((prev) => ({
                    ...prev,
                    profileId: id,
                    fullName: p ? p.name : prev.fullName,
                  }))
                }}
                className="w-full bg-background border border-outline-variant/80 rounded-2xl px-4 py-2.5 text-sm font-medium text-on-surface focus:outline-none focus:border-primary"
              >
                {profiles.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.name} ({p.relationship || 'Self'})
                  </option>
                ))}
              </select>
            </div>
          ) : (
            <div className="space-y-3">
              <div>
                <label className="text-[11px] font-bold text-on-surface-variant block mb-1">Full Name</label>
                <input
                  type="text"
                  value={personA.fullName}
                  onChange={(e) => setPersonA((prev) => ({ ...prev, fullName: e.target.value }))}
                  className="w-full bg-background border border-outline-variant/80 rounded-xl px-3 py-2 text-xs text-on-surface focus:outline-none focus:border-primary"
                  placeholder="Enter full name"
                />
              </div>
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="text-[11px] font-bold text-on-surface-variant block mb-1">Date of Birth</label>
                  <input
                    type="date"
                    value={personA.dateOfBirth}
                    onChange={(e) => setPersonA((prev) => ({ ...prev, dateOfBirth: e.target.value }))}
                    className="w-full bg-background border border-outline-variant/80 rounded-xl px-3 py-2 text-xs text-on-surface focus:outline-none focus:border-primary"
                  />
                </div>
                <div>
                  <label className="text-[11px] font-bold text-on-surface-variant block mb-1">Time of Birth</label>
                  <input
                    type="time"
                    value={personA.timeOfBirth}
                    onChange={(e) => setPersonA((prev) => ({ ...prev, timeOfBirth: e.target.value }))}
                    className="w-full bg-background border border-outline-variant/80 rounded-xl px-3 py-2 text-xs text-on-surface focus:outline-none focus:border-primary"
                  />
                </div>
              </div>
              <div>
                <label className="text-[11px] font-bold text-on-surface-variant block mb-1">Birth Place</label>
                <input
                  type="text"
                  value={personA.placeName}
                  onChange={(e) => setPersonA((prev) => ({ ...prev, placeName: e.target.value }))}
                  className="w-full bg-background border border-outline-variant/80 rounded-xl px-3 py-2 text-xs text-on-surface focus:outline-none focus:border-primary"
                  placeholder="e.g. New Delhi, India"
                />
              </div>
            </div>
          )}
        </div>

        {/* Person B Selector Card */}
        <div className="bg-surface p-6 rounded-3xl border border-outline-variant/60 shadow-xs">
          <div className="flex items-center justify-between mb-4 border-b border-outline-variant/40 pb-3">
            <div className="flex items-center gap-2">
              <span className="material-symbols-outlined text-primary text-xl">person_3</span>
              <h3 className="font-display text-xl font-bold text-primary">Partner B (Girl / Secondary)</h3>
            </div>
            {profiles.length > 0 && (
              <div className="flex bg-surface-variant/40 p-1 rounded-xl text-xs font-semibold">
                <button
                  onClick={() => setPersonB((prev) => ({ ...prev, mode: 'profile' }))}
                  className={`px-3 py-1 rounded-lg transition-all cursor-pointer ${
                    personB.mode === 'profile' ? 'bg-primary text-white shadow-xs' : 'text-on-surface-variant'
                  }`}
                >
                  Saved Profile
                </button>
                <button
                  onClick={() => setPersonB((prev) => ({ ...prev, mode: 'manual' }))}
                  className={`px-3 py-1 rounded-lg transition-all cursor-pointer ${
                    personB.mode === 'manual' ? 'bg-primary text-white shadow-xs' : 'text-on-surface-variant'
                  }`}
                >
                  Enter Details
                </button>
              </div>
            )}
          </div>

          {personB.mode === 'profile' && profiles.length > 0 ? (
            <div>
              <label className="text-xs font-bold text-on-surface-variant block mb-1.5">Select Profile</label>
              <select
                value={personB.profileId}
                onChange={(e) => {
                  const id = e.target.value
                  const p = profiles.find((item) => item.id === id)
                  setPersonB((prev) => ({
                    ...prev,
                    profileId: id,
                    fullName: p ? p.name : prev.fullName,
                  }))
                }}
                className="w-full bg-background border border-outline-variant/80 rounded-2xl px-4 py-2.5 text-sm font-medium text-on-surface focus:outline-none focus:border-primary"
              >
                {profiles.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.name} ({p.relationship || 'Self'})
                  </option>
                ))}
              </select>
            </div>
          ) : (
            <div className="space-y-3">
              <div>
                <label className="text-[11px] font-bold text-on-surface-variant block mb-1">Full Name</label>
                <input
                  type="text"
                  value={personB.fullName}
                  onChange={(e) => setPersonB((prev) => ({ ...prev, fullName: e.target.value }))}
                  className="w-full bg-background border border-outline-variant/80 rounded-xl px-3 py-2 text-xs text-on-surface focus:outline-none focus:border-primary"
                  placeholder="Enter full name"
                />
              </div>
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="text-[11px] font-bold text-on-surface-variant block mb-1">Date of Birth</label>
                  <input
                    type="date"
                    value={personB.dateOfBirth}
                    onChange={(e) => setPersonB((prev) => ({ ...prev, dateOfBirth: e.target.value }))}
                    className="w-full bg-background border border-outline-variant/80 rounded-xl px-3 py-2 text-xs text-on-surface focus:outline-none focus:border-primary"
                  />
                </div>
                <div>
                  <label className="text-[11px] font-bold text-on-surface-variant block mb-1">Time of Birth</label>
                  <input
                    type="time"
                    value={personB.timeOfBirth}
                    onChange={(e) => setPersonB((prev) => ({ ...prev, timeOfBirth: e.target.value }))}
                    className="w-full bg-background border border-outline-variant/80 rounded-xl px-3 py-2 text-xs text-on-surface focus:outline-none focus:border-primary"
                  />
                </div>
              </div>
              <div>
                <label className="text-[11px] font-bold text-on-surface-variant block mb-1">Birth Place</label>
                <input
                  type="text"
                  value={personB.placeName}
                  onChange={(e) => setPersonB((prev) => ({ ...prev, placeName: e.target.value }))}
                  className="w-full bg-background border border-outline-variant/80 rounded-xl px-3 py-2 text-xs text-on-surface focus:outline-none focus:border-primary"
                  placeholder="e.g. Mumbai, India"
                />
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Match Button */}
      <div className="text-center">
        <button
          onClick={handleMatch}
          disabled={loading}
          className="px-8 py-3.5 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white rounded-2xl text-base font-bold shadow-lg shadow-orange-500/25 transition-all hover:scale-105 disabled:opacity-50 cursor-pointer inline-flex items-center gap-2"
        >
          <span className="material-symbols-outlined text-xl" style={{ fontVariationSettings: "'FILL' 1" }}>
            favorite
          </span>
          {loading ? 'Calculating Ashtakoota Gunas…' : 'Match Kundli (Gun Milan)'}
        </button>
      </div>

      {/* Loading Spinner */}
      {loading && (
        <div className="py-12 text-center space-y-4">
          <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-xs text-on-surface-variant font-medium animate-pulse">
            Calculating Ashtakoota 36 Gunas, Manglik Alignment & Synthesizing AI Compatibility Report…
          </p>
        </div>
      )}

      {/* Results Section */}
      {matchResult && !loading && (
        <div className="space-y-6 animate-fade-in-up">
          {/* Ashtakoota Score Gauge Card */}
          <div className="celestial-card p-6 sm:p-8 rounded-3xl bg-surface border border-outline-variant/60 shadow-xs flex flex-wrap items-center justify-between gap-6">
            <div className="flex items-center gap-6">
              {/* Score Donut / Badge */}
              <div className="w-24 h-24 rounded-full bg-gradient-to-br from-amber-500 to-orange-500 text-white flex flex-col items-center justify-center shadow-lg shrink-0">
                <span className="text-3xl font-bold font-display leading-none">{totalScore}</span>
                <span className="text-[11px] font-medium opacity-90">/ 36 Gunas</span>
              </div>
              <div>
                <span className="text-xs font-extrabold uppercase tracking-wider px-3 py-1 rounded-full bg-primary-fixed text-primary border border-primary/20">
                  {matchResult.ashtakoota?.verdict}
                </span>
                <h3 className="font-display text-2xl font-bold text-primary mt-2">
                  {matchResult.person_a_name} & {matchResult.person_b_name}
                </h3>
                <p className="text-xs text-on-surface-variant mt-1 max-w-md">
                  {matchResult.ashtakoota?.recommendation}
                </p>
              </div>
            </div>

            {/* Yoni Symbol Compatibility Display */}
            <div className="bg-primary-fixed/40 p-4 rounded-2xl border border-primary/20 text-center shrink-0">
              <span className="text-xs font-bold text-primary block mb-1 uppercase tracking-wider">Yoni Animal Pairing</span>
              <span className="text-xl font-bold text-on-background block">
                {matchResult.yoni_pairing?.display}
              </span>
              <span className="text-[11px] font-semibold text-on-surface-variant">
                {matchResult.yoni_pairing?.relation}
              </span>
            </div>
          </div>

          {/* 8 Ashtakoota Factors Grid */}
          <div className="bg-surface p-6 rounded-3xl border border-outline-variant/60 shadow-xs">
            <h4 className="font-display text-xl font-bold text-primary mb-4 flex items-center gap-2">
              <span className="material-symbols-outlined text-primary text-xl">fact_check</span>
              Ashtakoota 8 Compatibility Factors (36 Points)
            </h4>

            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
              <FactorCard title="1. Varna (Spiritual)" pts={factors.varna?.obtained} max={1} desc={`${factors.varna?.boy_varna} & ${factors.varna?.girl_varna}`} />
              <FactorCard title="2. Vashya (Attraction)" pts={factors.vashya?.obtained} max={2} desc={`${factors.vashya?.boy_vashya} & ${factors.vashya?.girl_vashya}`} />
              <FactorCard title="3. Tara (Destiny)" pts={factors.tara?.obtained} max={3} desc="Nakshatra Distance" />
              <FactorCard title="4. Yoni (Physical)" pts={factors.yoni?.obtained} max={4} desc={matchResult.yoni_pairing?.relation} />
              <FactorCard title="5. Graha Maitri (Mental)" pts={factors.graha_maitri?.obtained} max={5} desc={factors.graha_maitri?.relation} />
              <FactorCard title="6. Gana (Temperament)" pts={factors.gana?.obtained} max={6} desc={factors.gana?.relation} />
              <FactorCard title="7. Bhakoot (Prosperity)" pts={factors.bhakoot?.obtained} max={7} desc={factors.bhakoot?.status} />
              <FactorCard title="8. Nadi (Progeny/Health)" pts={factors.nadi?.obtained} max={8} desc={factors.nadi?.status} />
            </div>
          </div>

          {/* Doshas & Marriage Timing Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Dosha Analysis Card */}
            <div className="bg-surface p-6 rounded-3xl border border-outline-variant/60 shadow-xs">
              <h4 className="font-display text-xl font-bold text-primary mb-3 flex items-center gap-2">
                <span className="material-symbols-outlined text-primary text-xl">shield</span>
                Vedic Dosha & Longevity Checks
              </h4>
              <ul className="space-y-2.5 text-xs text-on-surface font-medium">
                <li className="flex items-center justify-between p-2.5 rounded-xl bg-background border border-outline-variant/40">
                  <span>🔥 Manglik Compatibility:</span>
                  <span className="font-bold text-primary">{matchResult.dosha_analysis?.manglik_summary}</span>
                </li>
                <li className="flex items-center justify-between p-2.5 rounded-xl bg-background border border-outline-variant/40">
                  <span>🧬 Nadi Dosha:</span>
                  <span className="font-bold text-primary">{matchResult.dosha_analysis?.nadi_dosha?.status}</span>
                </li>
                <li className="flex items-center justify-between p-2.5 rounded-xl bg-background border border-outline-variant/40">
                  <span>💰 Bhakoot Dosha:</span>
                  <span className="font-bold text-primary">{matchResult.dosha_analysis?.bhakoot_dosha?.status}</span>
                </li>
                <li className="flex items-center justify-between p-2.5 rounded-xl bg-background border border-outline-variant/40">
                  <span>👑 Rajju Dosha (Longevity):</span>
                  <span className="font-bold text-primary">{matchResult.dosha_analysis?.rajju_dosha?.status}</span>
                </li>
              </ul>
            </div>

            {/* Marriage Timing Card */}
            <div className="bg-surface p-6 rounded-3xl border border-outline-variant/60 shadow-xs">
              <h4 className="font-display text-xl font-bold text-primary mb-3 flex items-center gap-2">
                <span className="material-symbols-outlined text-primary text-xl">event_available</span>
                Marriage Timing Estimate
              </h4>
              <div className="bg-primary-fixed/40 p-4 rounded-2xl border border-primary/20 text-xs leading-relaxed text-on-background font-medium">
                {matchResult.marriage_timing}
              </div>
            </div>
          </div>

          {/* AI Compatibility Report */}
          {aiReport && (
            <div className="celestial-card p-6 sm:p-8 rounded-3xl bg-surface border border-outline-variant/60 shadow-xs">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 bg-primary-fixed rounded-2xl flex items-center justify-center text-primary font-bold shadow-xs">
                  <span className="material-symbols-outlined text-2xl" style={{ fontVariationSettings: "'FILL' 1" }}>
                    auto_awesome
                  </span>
                </div>
                <div>
                  <h3 className="font-display text-2xl font-bold text-primary">
                    AI Master Compatibility Report
                  </h3>
                  <p className="text-xs text-on-surface-variant">Empathetic Synthesis & Remedial Guidance</p>
                </div>
              </div>

              <div className="markdown-container text-sm leading-relaxed text-on-background">
                <ReactMarkdown>{aiReport}</ReactMarkdown>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

function FactorCard({ title, pts, max, desc }: { title: string; pts: number; max: number; desc: string }) {
  const percent = Math.min(100, Math.max(0, (pts / max) * 100))
  return (
    <div className="bg-background p-3.5 rounded-2xl border border-outline-variant/50">
      <div className="flex items-center justify-between text-xs font-bold text-on-surface mb-1">
        <span>{title}</span>
        <span className="text-primary">{pts} / {max}</span>
      </div>
      <div className="w-full h-1.5 bg-surface-variant rounded-full overflow-hidden mb-2">
        <div
          className="h-full bg-gradient-to-r from-amber-500 to-orange-500 rounded-full transition-all"
          style={{ width: `${percent}%` }}
        />
      </div>
      <p className="text-[10px] text-on-surface-variant truncate font-medium">{desc}</p>
    </div>
  )
}
