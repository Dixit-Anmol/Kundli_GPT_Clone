import { useState, useEffect } from 'react'

interface TransitItem {
  planet: string
  hindiName: string
  sign: string
  status: string
  badgeStyle: string
  degree: string
  effect: string
}

const TRANSIT_LIST: TransitItem[] = [
  {
    planet: 'Sun',
    hindiName: 'सूर्य',
    sign: 'Sun in Aries (Mesha)',
    status: 'Exalted • High Vitality',
    badgeStyle: 'bg-amber-500/10 text-amber-800 border-amber-500/30',
    degree: '14° 22\'',
    effect: 'Leadership & Solar Energy Peak',
  },
  {
    planet: 'Moon',
    hindiName: 'चन्द्र',
    sign: 'Moon in Taurus (Vrishabha)',
    status: 'Exalted • Emotional Bliss',
    badgeStyle: 'bg-emerald-500/10 text-emerald-800 border-emerald-500/30',
    degree: '08° 45\'',
    effect: 'Deep Mental Peace & Intuition',
  },
  {
    planet: 'Jupiter',
    hindiName: 'गुरु',
    sign: 'Jupiter in Taurus (Vrishabha)',
    status: 'Benefic • Financial Expansion',
    badgeStyle: 'bg-yellow-500/10 text-yellow-900 border-yellow-500/30',
    degree: '21° 10\'',
    effect: 'Abundance, Wisdom & Luck',
  },
  {
    planet: 'Saturn',
    hindiName: 'शनि',
    sign: 'Saturn in Aquarius (Kumbha)',
    status: 'Own Sign • Karmic Discipline',
    badgeStyle: 'bg-blue-500/10 text-blue-900 border-blue-500/30',
    degree: '18° 50\'',
    effect: 'Long-term Growth & Mastery',
  },
  {
    planet: 'Mars',
    hindiName: 'मंगल',
    sign: 'Mars in Capricorn (Makara)',
    status: 'Exalted • Courage & Action',
    badgeStyle: 'bg-rose-500/10 text-rose-900 border-rose-500/30',
    degree: '28° 04\'',
    effect: 'Unstoppable Drive & Victory',
  },
  {
    planet: 'Venus',
    hindiName: 'शुक्र',
    sign: 'Venus in Pisces (Meena)',
    status: 'Exalted • Creative Harmony',
    badgeStyle: 'bg-purple-500/10 text-purple-900 border-purple-500/30',
    degree: '12° 30\'',
    effect: 'Artistic Genius & Harmony',
  },
  {
    planet: 'Mercury',
    hindiName: 'बुध',
    sign: 'Mercury in Gemini (Mithuna)',
    status: 'Own Sign • Intellect & Speech',
    badgeStyle: 'bg-teal-500/10 text-teal-900 border-teal-500/30',
    degree: '05° 15\'',
    effect: 'Sharp Analysis & Communication',
  },
  {
    planet: 'Rahu',
    hindiName: 'राहु',
    sign: 'Rahu in Pisces (Meena)',
    status: 'Karmic Axis Shift',
    badgeStyle: 'bg-indigo-500/10 text-indigo-900 border-indigo-500/30',
    degree: '15° 00\'',
    effect: 'Innovation & Ambition',
  },
  {
    planet: 'Ketu',
    hindiName: 'केतु',
    sign: 'Ketu in Virgo (Kanya)',
    status: 'Spiritual Liberation',
    badgeStyle: 'bg-orange-500/10 text-orange-900 border-orange-500/30',
    degree: '15° 00\'',
    effect: 'Detachment & Higher Consciousness',
  },
]

export default function GocharaOrbits() {
  const [activeIndex, setActiveIndex] = useState(0)

  // Auto-shift the active transit card every 3.5 seconds
  useEffect(() => {
    const timer = setInterval(() => {
      setActiveIndex((prev) => (prev + 1) % TRANSIT_LIST.length)
    }, 3500)
    return () => clearInterval(timer)
  }, [])

  const currentActiveHindi = TRANSIT_LIST[activeIndex]?.hindiName

  return (
    <div className="w-full grid grid-cols-1 md:grid-cols-12 gap-8 md:gap-12 items-center">
      {/* ── Left Side: Auto-shifting Navagraha Transit Cards (No Emojis) ── */}
      <div className="md:col-span-6 flex flex-col justify-center">
        <h2 className="font-display text-2xl sm:text-3xl md:text-[42px] text-on-background mb-3 uppercase tracking-[0.1em] italic font-semibold leading-tight">
          The Heavens in Motion
        </h2>
        <p className="text-base sm:text-lg text-on-surface-variant mb-6 font-light leading-relaxed italic">
          Our engine constantly tracks the movement of the Navagrahas to provide real-time Gochara insights that evolve as the cosmos shifts.
        </p>

        {/* Dynamic Auto-shifting Transit Cards Box */}
        <div className="relative min-h-[200px] flex flex-col gap-3">
          {TRANSIT_LIST.map((item, idx) => {
            const isActive = idx === activeIndex
            const isNext = idx === (activeIndex + 1) % TRANSIT_LIST.length

            if (!isActive && !isNext) return null

            return (
              <div
                key={item.planet}
                className={`p-4 sm:p-5 bg-white border border-outline-variant transition-all duration-700 rounded-xl sm:rounded-2xl ${
                  isActive
                    ? 'opacity-100 scale-100 shadow-md border-primary/50 z-10 translate-y-0'
                    : 'opacity-40 scale-95 shadow-none border-outline-variant/40 -z-0 translate-y-1'
                }`}
                style={{ boxShadow: isActive ? '0 8px 30px -8px rgba(230, 126, 34, 0.2)' : 'none' }}
              >
                <div className="flex items-center justify-between gap-3">
                  <div className="flex items-center gap-3 min-w-0">
                    {/* Hindi Planet Badge Pill */}
                    <div className="w-10 h-10 sm:w-11 sm:h-11 rounded-xl bg-primary-fixed/40 border border-primary/30 flex items-center justify-center font-display font-bold text-primary text-sm sm:text-base shrink-0 shadow-xs">
                      {item.hindiName}
                    </div>

                    <div className="min-w-0">
                      <h4 className="text-xs sm:text-sm tracking-[0.1em] uppercase font-bold text-on-background truncate">
                        {item.sign}
                      </h4>
                      <p className="text-[11px] sm:text-xs text-on-surface-variant font-medium mt-0.5">
                        Deg: <span className="font-mono text-primary font-bold">{item.degree}</span> · {item.effect}
                      </p>
                    </div>
                  </div>

                  <span
                    className={`text-[10px] sm:text-[11px] tracking-[0.08em] uppercase px-2.5 py-1 font-extrabold rounded-full border shrink-0 ${item.badgeStyle}`}
                  >
                    {item.status}
                  </span>
                </div>
              </div>
            )
          })}
        </div>

        {/* Dots indicator */}
        <div className="flex items-center gap-2 mt-4 justify-center md:justify-start">
          {TRANSIT_LIST.map((item, i) => (
            <button
              key={i}
              onClick={() => setActiveIndex(i)}
              className={`h-2 rounded-full transition-all cursor-pointer ${
                i === activeIndex ? 'w-6 bg-primary' : 'w-2 bg-outline-variant/60 hover:bg-primary/50'
              }`}
              title={`View ${item.hindiName} (${item.planet})`}
            />
          ))}
        </div>
      </div>

      {/* ── Right Side: Multi-Ring Concentric Orbiting Circles with Hindi Graha Badges ── */}
      <div className="md:col-span-6 relative flex justify-center items-center py-4 select-none">
        <div className="relative w-64 h-64 sm:w-80 sm:h-80 md:w-96 md:h-96 flex items-center justify-center">
          
          {/* Outer Ring 3 — Saturn (शनि), Rahu (राहु) & Ketu (केतु) (Slow 90s Counter-Clockwise Rotation) */}
          <div
            className="absolute inset-0 rounded-full border border-primary/30 border-dashed"
            style={{ animation: 'spinCounter 90s linear infinite' }}
          >
            {/* Shani (शनि) */}
            <div className="absolute -top-3.5 left-1/2 -translate-x-1/2">
              <div
                className={`px-2.5 py-1 rounded-full border text-xs font-display font-extrabold shadow-sm transition-all ${
                  currentActiveHindi === 'शनि'
                    ? 'bg-primary text-white border-primary scale-110 ring-2 ring-primary/30'
                    : 'bg-white text-primary border-primary/40'
                }`}
                style={{ animation: 'spinClockwise 90s linear infinite' }}
              >
                शनि
              </div>
            </div>

            {/* Rahu (राहु) */}
            <div className="absolute -bottom-3.5 left-1/4 -translate-x-1/2">
              <div
                className={`px-2.5 py-1 rounded-full border text-xs font-display font-extrabold shadow-sm transition-all ${
                  currentActiveHindi === 'राहु'
                    ? 'bg-primary text-white border-primary scale-110 ring-2 ring-primary/30'
                    : 'bg-white text-amber-900 border-amber-800/40'
                }`}
                style={{ animation: 'spinClockwise 90s linear infinite' }}
              >
                राहु
              </div>
            </div>

            {/* Ketu (केतु) */}
            <div className="absolute -bottom-3.5 right-1/4 translate-x-1/2">
              <div
                className={`px-2.5 py-1 rounded-full border text-xs font-display font-extrabold shadow-sm transition-all ${
                  currentActiveHindi === 'केतु'
                    ? 'bg-primary text-white border-primary scale-110 ring-2 ring-primary/30'
                    : 'bg-white text-orange-900 border-orange-800/40'
                }`}
                style={{ animation: 'spinClockwise 90s linear infinite' }}
              >
                केतु
              </div>
            </div>
          </div>

          {/* Middle Ring 2 — Guru (गुरु), Mangal (मंगल) & Budh (बुध) (60s Clockwise Rotation) */}
          <div
            className="absolute inset-7 sm:inset-9 rounded-full border-2 border-primary/35"
            style={{ animation: 'spinClockwise 60s linear infinite' }}
          >
            {/* Guru (गुरु) */}
            <div className="absolute top-1/2 -left-4 -translate-y-1/2">
              <div
                className={`px-2.5 py-1 rounded-full border text-xs font-display font-extrabold shadow-sm transition-all ${
                  currentActiveHindi === 'गुरु'
                    ? 'bg-primary text-white border-primary scale-110 ring-2 ring-primary/30'
                    : 'bg-white text-primary border-primary/40'
                }`}
                style={{ animation: 'spinCounter 60s linear infinite' }}
              >
                गुरु
              </div>
            </div>

            {/* Mangal (मंगल) */}
            <div className="absolute top-1/2 -right-4 -translate-y-1/2">
              <div
                className={`px-2.5 py-1 rounded-full border text-xs font-display font-extrabold shadow-sm transition-all ${
                  currentActiveHindi === 'मंगल'
                    ? 'bg-primary text-white border-primary scale-110 ring-2 ring-primary/30'
                    : 'bg-white text-rose-800 border-rose-700/40'
                }`}
                style={{ animation: 'spinCounter 60s linear infinite' }}
              >
                मंगल
              </div>
            </div>

            {/* Budh (बुध) */}
            <div className="absolute -top-3.5 left-1/2 -translate-x-1/2">
              <div
                className={`px-2.5 py-1 rounded-full border text-xs font-display font-extrabold shadow-sm transition-all ${
                  currentActiveHindi === 'बुध'
                    ? 'bg-primary text-white border-primary scale-110 ring-2 ring-primary/30'
                    : 'bg-white text-teal-800 border-teal-700/40'
                }`}
                style={{ animation: 'spinCounter 60s linear infinite' }}
              >
                बुध
              </div>
            </div>
          </div>

          {/* Inner Ring 1 — Surya (सूर्य), Chandra (चन्द्र) & Shukra (शुक्र) (30s Counter-Clockwise Rotation) */}
          <div
            className="absolute inset-15 sm:inset-18 rounded-full border border-primary/45 border-dotted"
            style={{ animation: 'spinCounter 30s linear infinite' }}
          >
            {/* Surya (सूर्य) */}
            <div className="absolute -top-3.5 left-1/2 -translate-x-1/2">
              <div
                className={`px-2.5 py-0.5 rounded-full border text-xs font-display font-extrabold shadow-sm transition-all ${
                  currentActiveHindi === 'सूर्य'
                    ? 'bg-amber-600 text-white border-amber-600 scale-110 ring-2 ring-amber-500/40'
                    : 'bg-amber-500 text-white border-amber-600'
                }`}
                style={{ animation: 'spinClockwise 30s linear infinite' }}
              >
                सूर्य
              </div>
            </div>

            {/* Chandra (चन्द्र) */}
            <div className="absolute -bottom-3.5 left-1/2 -translate-x-1/2">
              <div
                className={`px-2.5 py-0.5 rounded-full border text-xs font-display font-extrabold shadow-sm transition-all ${
                  currentActiveHindi === 'चन्द्र'
                    ? 'bg-primary text-white border-primary scale-110 ring-2 ring-primary/30'
                    : 'bg-white text-primary border-primary/40'
                }`}
                style={{ animation: 'spinClockwise 30s linear infinite' }}
              >
                चन्द्र
              </div>
            </div>

            {/* Shukra (शुक्र) */}
            <div className="absolute top-1/2 -right-3.5 -translate-y-1/2">
              <div
                className={`px-2.5 py-0.5 rounded-full border text-xs font-display font-extrabold shadow-sm transition-all ${
                  currentActiveHindi === 'शुक्र'
                    ? 'bg-purple-700 text-white border-purple-700 scale-110 ring-2 ring-purple-500/40'
                    : 'bg-purple-50 text-purple-900 border-purple-300'
                }`}
                style={{ animation: 'spinClockwise 30s linear infinite' }}
              >
                शुक्र
              </div>
            </div>
          </div>

          {/* Center Hub — Gochara Core */}
          <div className="w-24 h-24 sm:w-28 sm:h-28 rounded-full bg-gradient-to-br from-primary-fixed to-white border-2 border-primary/60 flex flex-col items-center justify-center p-2 shadow-md z-10 text-center animate-pulse">
            <span className="font-display text-sm sm:text-base font-bold text-primary">
              गोचर
            </span>
            <span className="text-[10px] font-sans font-semibold text-on-surface-variant opacity-80">
              Gochara
            </span>
            <span className="text-[9px] font-mono font-bold text-amber-800 bg-amber-100 px-2 py-0.5 rounded-full mt-0.5">
              नवग्रह
            </span>
          </div>

        </div>
      </div>

      {/* Keyframes for Orbit Rotation & Counter-Rotation so Hindi Graha text stays upright */}
      <style>{`
        @keyframes spinClockwise {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        @keyframes spinCounter {
          from { transform: rotate(0deg); }
          to { transform: rotate(-360deg); }
        }
      `}</style>
    </div>
  )
}
