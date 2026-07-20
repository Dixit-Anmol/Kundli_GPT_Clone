import { useState } from 'react'
import type { RelationshipType } from '../../types/profile'
import PrashnaQuestionSelector from './PrashnaQuestionSelector'

export type OnboardingMode = 'exact' | 'partial' | 'prashna'

export interface BirthData {
  fullName: string
  gender: 'male' | 'female' | 'other'
  dateOfBirth?: string
  timeOfBirth?: string
  relationship?: RelationshipType
  mode?: OnboardingMode
  timeSlot?: string
  question?: string
  category?: string
}

interface BirthDetailsFormProps {
  onSubmit: (data: BirthData) => void
}

export default function BirthDetailsForm({ onSubmit }: BirthDetailsFormProps) {
  const [mode, setMode] = useState<OnboardingMode>('exact')

  // Form State
  const [name, setName] = useState('')
  const [gender, setGender] = useState<'male' | 'female' | 'other'>('male')
  const [relationship, setRelationship] = useState<RelationshipType>('Self')
  const [dob, setDob] = useState('')
  const [tob, setTob] = useState('')

  // Option 2 Partial State
  const [timeSlot, setTimeSlot] = useState<string>('unknown')

  // Submit Handler
  const handleFormSubmit = () => {
    if (!name.trim()) return

    if (mode === 'exact') {
      if (dob && tob) {
        onSubmit({
          fullName: name.trim(),
          gender,
          dateOfBirth: dob,
          timeOfBirth: tob,
          relationship,
          mode: 'exact',
        })
      }
    } else if (mode === 'partial') {
      if (dob) {
        onSubmit({
          fullName: name.trim(),
          gender,
          dateOfBirth: dob,
          timeOfBirth: tob || undefined,
          relationship,
          mode: 'partial',
          timeSlot,
        })
      }
    }
  }

  const handlePrashnaSelect = (question: string, category: string) => {
    onSubmit({
      fullName: name.trim() || 'Seeker',
      gender,
      relationship,
      mode: 'prashna',
      question,
      category,
    })
  }

  const genderOptions: Array<{ value: 'male' | 'female' | 'other'; label: string; icon: string }> = [
    { value: 'male', label: 'Male', icon: 'male' },
    { value: 'female', label: 'Female', icon: 'female' },
    { value: 'other', label: 'Other', icon: 'person' },
  ]

  const timeSlotOptions = [
    { value: 'unknown', label: '❓ Unknown Time (Approximate Planetary Calculation)' },
    { value: 'morning', label: '🌅 Morning (6:00 AM – 12:00 PM)' },
    { value: 'afternoon', label: '☀️ Afternoon (12:00 PM – 5:00 PM)' },
    { value: 'evening', label: '🌇 Evening (5:00 PM – 8:00 PM)' },
    { value: 'night', label: '🌙 Night (8:00 PM – 4:00 AM)' },
    { value: 'sunrise', label: '🌅 Around Sunrise' },
    { value: 'sunset', label: '🌇 Around Sunset' },
  ]

  return (
    <div className="mx-auto celestial-card rounded-3xl p-8 sm:p-10 shadow-xl border border-outline-variant/60 animate-fade-in-up space-y-8 max-w-4xl bg-surface/95 backdrop-blur-md">
      {/* Header Banner */}
      <div className="border-b border-outline-variant/40 pb-6">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-600 shrink-0">
            <span className="material-symbols-outlined text-2xl">auto_awesome</span>
          </div>
          <div>
            <h2 className="font-display text-3xl sm:text-4xl font-extrabold text-primary leading-tight">
              ✨ Your Vedic Birth Essence
            </h2>
            <p className="text-sm sm:text-base text-on-surface-variant font-medium mt-1">
              Select your birth information status below to calculate your Janma Kundli, Estimated Horoscope, or Horary Prashna Guidance.
            </p>
          </div>
        </div>
      </div>

      {/* 3 Prominent Hero Onboarding Cards */}
      <div className="space-y-3">
        <label className="text-xs font-bold uppercase tracking-wider text-primary block">
          Step 1: Choose Your Birth Details Availability
        </label>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Card 1: Exact Details */}
          <div
            onClick={() => setMode('exact')}
            className={`p-5 rounded-2xl border-2 transition-all cursor-pointer flex flex-col justify-between space-y-3 ${
              mode === 'exact'
                ? 'bg-primary/5 border-primary ring-4 ring-primary/10 shadow-md scale-[1.02]'
                : 'bg-surface-variant/30 border-outline-variant/50 hover:border-primary/40 hover:bg-surface-variant/50'
            }`}
          >
            <div className="flex items-center justify-between">
              <span className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-700">
                <span className="material-symbols-outlined text-xl">verified</span>
              </span>
              <span className={`text-[11px] font-extrabold px-2.5 py-0.5 rounded-full ${
                mode === 'exact' ? 'bg-primary text-white' : 'bg-surface-variant text-on-surface-variant'
              }`}>
                Full Chart
              </span>
            </div>
            <div>
              <h4 className="font-display text-lg font-bold text-primary">
                ✅ Known Birth Details
              </h4>
              <p className="text-xs text-on-surface-variant font-medium mt-1 leading-relaxed">
                Generate complete D1 Janma Kundli with exact Lagna, Houses, D9, D10 & Dashas.
              </p>
            </div>
          </div>

          {/* Card 2: Partial Details */}
          <div
            onClick={() => setMode('partial')}
            className={`p-5 rounded-2xl border-2 transition-all cursor-pointer flex flex-col justify-between space-y-3 ${
              mode === 'partial'
                ? 'bg-primary/5 border-primary ring-4 ring-primary/10 shadow-md scale-[1.02]'
                : 'bg-surface-variant/30 border-outline-variant/50 hover:border-primary/40 hover:bg-surface-variant/50'
            }`}
          >
            <div className="flex items-center justify-between">
              <span className="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-700">
                <span className="material-symbols-outlined text-xl">help</span>
              </span>
              <span className={`text-[11px] font-extrabold px-2.5 py-0.5 rounded-full ${
                mode === 'partial' ? 'bg-primary text-white' : 'bg-surface-variant text-on-surface-variant'
              }`}>
                Approximate
              </span>
            </div>
            <div>
              <h4 className="font-display text-lg font-bold text-primary">
                ❓ Partial Birth Details
              </h4>
              <p className="text-xs text-on-surface-variant font-medium mt-1 leading-relaxed">
                Calculate Moon Sign & planetary positions without fabricating Lagna or Houses.
              </p>
            </div>
          </div>

          {/* Card 3: Prashna / Unknown Details */}
          <div
            onClick={() => setMode('prashna')}
            className={`p-5 rounded-2xl border-2 transition-all cursor-pointer flex flex-col justify-between space-y-3 ${
              mode === 'prashna'
                ? 'bg-primary/5 border-primary ring-4 ring-primary/10 shadow-md scale-[1.02]'
                : 'bg-surface-variant/30 border-outline-variant/50 hover:border-primary/40 hover:bg-surface-variant/50'
            }`}
          >
            <div className="flex items-center justify-between">
              <span className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-700">
                <span className="material-symbols-outlined text-xl">psychology</span>
              </span>
              <span className={`text-[11px] font-extrabold px-2.5 py-0.5 rounded-full ${
                mode === 'prashna' ? 'bg-primary text-white' : 'bg-surface-variant text-on-surface-variant'
              }`}>
                Prashna Horary
              </span>
            </div>
            <div>
              <h4 className="font-display text-lg font-bold text-primary">
                🙏 Unknown Birth Details
              </h4>
              <p className="text-xs text-on-surface-variant font-medium mt-1 leading-relaxed">
                No birth details required. Receives direct guidance using Horary Prashna Kundli.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Step 2 Inputs Container */}
      <div className="space-y-6 pt-2">
        <label className="text-xs font-bold uppercase tracking-wider text-primary block">
          Step 2: Enter Profile Information
        </label>

        {/* Common Name, Gender & Relationship Fields */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          <div>
            <label className="text-xs font-bold text-primary block mb-2">
              Full Name *
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Anmol Dixit"
              className="w-full bg-surface-variant/40 border border-outline-variant/60 rounded-2xl px-4 py-3.5 text-sm sm:text-base text-primary focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary transition-all font-medium"
            />
          </div>

          <div>
            <label className="text-xs font-bold text-primary block mb-2">Gender</label>
            <div className="grid grid-cols-3 gap-2">
              {genderOptions.map((opt) => (
                <button
                  key={opt.value}
                  type="button"
                  onClick={() => setGender(opt.value)}
                  className={`py-3 px-2 text-xs sm:text-sm font-bold rounded-2xl border transition-all cursor-pointer flex items-center justify-center gap-1 ${
                    gender === opt.value
                      ? 'bg-primary text-white border-primary shadow-xs'
                      : 'bg-surface-variant/30 border-outline-variant/50 text-on-surface-variant hover:bg-surface-variant/60'
                  }`}
                >
                  <span className="material-symbols-outlined text-base">{opt.icon}</span>
                  <span>{opt.label}</span>
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="text-xs font-bold text-primary block mb-2">Profile Target</label>
            <select
              value={relationship}
              onChange={(e) => setRelationship(e.target.value as RelationshipType)}
              className="w-full bg-surface-variant/40 border border-outline-variant/60 rounded-2xl px-4 py-3.5 text-sm sm:text-base text-primary focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary cursor-pointer font-medium"
            >
              {['Self', 'Spouse', 'Child', 'Parent', 'Friend', 'Other'].map((rel) => (
                <option key={rel} value={rel}>
                  {rel}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Mode 1: Exact Birth Details Inputs */}
        {mode === 'exact' && (
          <div className="space-y-6 animate-fade-in-up bg-surface-variant/20 p-6 rounded-3xl border border-outline-variant/50">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div>
                <label className="text-xs font-bold text-primary block mb-2">
                  📅 Date of Birth *
                </label>
                <input
                  type="date"
                  value={dob}
                  onChange={(e) => setDob(e.target.value)}
                  className="w-full bg-surface border border-outline-variant/60 rounded-2xl px-4 py-3.5 text-sm sm:text-base text-primary focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary font-medium"
                />
              </div>

              <div>
                <label className="text-xs font-bold text-primary block mb-2">
                  ⏰ Time of Birth *
                </label>
                <input
                  type="time"
                  value={tob}
                  onChange={(e) => setTob(e.target.value)}
                  className="w-full bg-surface border border-outline-variant/60 rounded-2xl px-4 py-3.5 text-sm sm:text-base text-primary focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary font-medium"
                />
              </div>
            </div>

            <button
              type="button"
              onClick={handleFormSubmit}
              disabled={!name.trim() || !dob || !tob}
              className="w-full bg-primary text-white font-bold py-4 rounded-2xl text-sm sm:text-base shadow-lg shadow-primary/25 hover:scale-[1.01] transition-all disabled:opacity-50 cursor-pointer flex items-center justify-center gap-2"
            >
              <span>Proceed to Select Birthplace & Generate Janma Kundli</span>
              <span className="material-symbols-outlined text-lg">arrow_forward</span>
            </button>
          </div>
        )}

        {/* Mode 2: Partial Details Inputs */}
        {mode === 'partial' && (
          <div className="space-y-6 animate-fade-in-up bg-amber-500/5 p-6 rounded-3xl border border-amber-500/30">
            <div className="bg-amber-500/10 border border-amber-500/30 p-4 rounded-2xl text-xs sm:text-sm text-amber-950 font-medium leading-relaxed">
              ℹ️ <strong>Estimated Horoscope Mode Active</strong>: Enter whatever birth date details you know. Lagna and House Cusps are strictly excluded until exact birth time is provided.
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div>
                <label className="text-xs font-bold text-primary block mb-2">
                  📅 Birth Date / Year *
                </label>
                <input
                  type="date"
                  value={dob}
                  onChange={(e) => setDob(e.target.value)}
                  className="w-full bg-surface border border-outline-variant/60 rounded-2xl px-4 py-3.5 text-sm sm:text-base text-primary focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary font-medium"
                />
              </div>

              <div>
                <label className="text-xs font-bold text-primary block mb-2">
                  🌅 Approximate Time Slot
                </label>
                <select
                  value={timeSlot}
                  onChange={(e) => setTimeSlot(e.target.value)}
                  className="w-full bg-surface border border-outline-variant/60 rounded-2xl px-4 py-3.5 text-sm sm:text-base text-primary focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary cursor-pointer font-medium"
                >
                  {timeSlotOptions.map((opt) => (
                    <option key={opt.value} value={opt.value}>
                      {opt.label}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className="text-xs font-bold text-primary block mb-2">
                ⏱️ Exact Time of Birth (Optional)
              </label>
              <input
                type="time"
                value={tob}
                onChange={(e) => setTob(e.target.value)}
                placeholder="Optional"
                className="w-full bg-surface border border-outline-variant/60 rounded-2xl px-4 py-3.5 text-sm sm:text-base text-primary focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary font-medium"
              />
            </div>

            <button
              type="button"
              onClick={handleFormSubmit}
              disabled={!name.trim() || !dob}
              className="w-full bg-primary text-white font-bold py-4 rounded-2xl text-sm sm:text-base shadow-lg shadow-primary/25 hover:scale-[1.01] transition-all disabled:opacity-50 cursor-pointer flex items-center justify-center gap-2"
            >
              <span>Proceed to Select Location & Generate Estimated Horoscope</span>
              <span className="material-symbols-outlined text-lg">arrow_forward</span>
            </button>
          </div>
        )}

        {/* Mode 3: Unknown Birth Details (Prashna Horary) Inputs */}
        {mode === 'prashna' && (
          <div className="space-y-6 animate-fade-in-up bg-purple-500/5 p-6 rounded-3xl border border-purple-500/30">
            <div className="bg-purple-500/10 border border-purple-500/30 p-4 rounded-2xl text-xs sm:text-sm text-purple-950 font-medium leading-relaxed">
              🔮 <strong>Prashna Horary Mode Active</strong>: Zero birth details required! Your chart will be calculated using the exact moment and location of your question right now.
            </div>

            <PrashnaQuestionSelector onSelectQuestion={handlePrashnaSelect} />
          </div>
        )}
      </div>
    </div>
  )
}
