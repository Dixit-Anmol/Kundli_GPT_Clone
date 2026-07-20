import { useState } from 'react'

interface PersonalityDashboardProps {
  chartData: any
  computed?: any
}

interface TemperamentDefinition {
  id: string
  name: string
  devanagari: string
  element: string
  icon: string
  color: string
  badgeBg: string
  coreTraits: string
  strengths: string
  challenges: string
  astrologicalBasis: string
  recommendations: string
}

const TEMPERAMENTS: TemperamentDefinition[] = [
  {
    id: 'choleric',
    name: 'Choleric',
    devanagari: 'तेजस्वी (Agni)',
    element: 'Fire (Agni)',
    icon: 'local_fire_department',
    color: 'text-rose-600 border-rose-500/40 bg-rose-500/10',
    badgeBg: 'bg-rose-600 text-white',
    coreTraits: 'Ambitious, decisive, confident',
    strengths: 'Leadership, determination, visionary drive',
    challenges: 'Impatient, controlling, prone to burnout',
    astrologicalBasis: 'Driven by Sun, Mars & Fire signs (Aries, Leo, Sagittarius). High energy and competitive instinct.',
    recommendations: 'Practice patience, delegate responsibilities, and use evening breathwork to cool fiery intensity.'
  },
  {
    id: 'sanguine',
    name: 'Sanguine',
    devanagari: 'उत्सही (Vayu)',
    element: 'Air (Vayu)',
    icon: 'wb_sunny',
    color: 'text-amber-600 border-amber-500/40 bg-amber-500/10',
    badgeBg: 'bg-amber-600 text-white',
    coreTraits: 'Energetic, social, optimistic',
    strengths: 'Friendly, enthusiastic, quick communicator',
    challenges: 'Easily distracted, impulsive, superficial focus',
    astrologicalBasis: 'Driven by Mercury, Venus & Air signs (Gemini, Libra, Aquarius). Rapid intellectual curiosity.',
    recommendations: 'Structure daily priorities into single-task deep work blocks to channel creative enthusiasm.'
  },
  {
    id: 'melancholic',
    name: 'Melancholic',
    devanagari: 'विचारशील (Prithvi)',
    element: 'Earth (Prithvi)',
    icon: 'thunderstorm',
    color: 'text-emerald-700 border-emerald-500/40 bg-emerald-500/10',
    badgeBg: 'bg-emerald-700 text-white',
    coreTraits: 'Thoughtful, analytical, perfectionistic',
    strengths: 'Organized, creative, deep attention to detail',
    challenges: 'Overthinking, pessimism, self-criticism',
    astrologicalBasis: 'Driven by Saturn, Mercury & Earth signs (Taurus, Virgo, Capricorn). Methodical and grounded.',
    recommendations: 'Set time limits on planning, practice self-compassion, and avoid perfectionism traps.'
  },
  {
    id: 'phlegmatic',
    name: 'Phlegmatic',
    devanagari: 'शान्त (Jala)',
    element: 'Water (Jala)',
    icon: 'water_drop',
    color: 'text-blue-600 border-blue-500/40 bg-blue-500/10',
    badgeBg: 'bg-blue-600 text-white',
    coreTraits: 'Calm, patient, dependable',
    strengths: 'Peaceful, loyal, empathetic listening',
    challenges: 'Avoids conflict, resistant to change, passive',
    astrologicalBasis: 'Driven by Moon, Venus & Water signs (Cancer, Scorpio, Pisces). Emotional depth and stability.',
    recommendations: 'Embrace healthy confrontation, take proactive initiative, and engage in daily physical exercise.'
  }
]

export default function PersonalityDashboard({ chartData, computed }: PersonalityDashboardProps) {
  const [selectedTempId, setSelectedTempId] = useState<string>('choleric')

  // Calculate elemental scores from computed or chartData fallback
  const elements = computed?.elements || {}
  const rawPlanets = chartData?.planets || {}
  
  let fireScore = elements.Fire
  let airScore = elements.Air
  let earthScore = elements.Earth
  let waterScore = elements.Water

  if (fireScore === undefined) {
    // Basic sign-based fallback
    let f = 0, a = 0, e = 0, w = 0
    const fireSigns = ['Aries', 'Leo', 'Sagittarius']
    const airSigns = ['Gemini', 'Libra', 'Aquarius']
    const earthSigns = ['Taurus', 'Virgo', 'Capricorn']
    const waterSigns = ['Cancer', 'Scorpio', 'Pisces']

    Object.values(rawPlanets).forEach((p: any) => {
      const s = p?.sign
      if (fireSigns.includes(s)) f += 1
      else if (airSigns.includes(s)) a += 1
      else if (earthSigns.includes(s)) e += 1
      else if (waterSigns.includes(s)) w += 1
    })
    const total = Math.max(1, f + a + e + w)
    fireScore = Math.round((f / total) * 100)
    airScore = Math.round((a / total) * 100)
    earthScore = Math.round((e / total) * 100)
    waterScore = Math.round((w / total) * 100)
  }


  const scoresMap: Record<string, number> = {
    choleric: fireScore,
    sanguine: airScore,
    melancholic: earthScore,
    phlegmatic: waterScore
  }

  // Find dominant temperament
  const sortedTemps = [...TEMPERAMENTS].sort((a, b) => (scoresMap[b.id] || 0) - (scoresMap[a.id] || 0))
  const dominantTemp = sortedTemps[0]
  const secondaryTemp = sortedTemps[1]

  const activeTemp = TEMPERAMENTS.find(t => t.id === selectedTempId) || dominantTemp

  return (
    <div className="space-y-6 animate-fade-in-up">
      {/* Banner Card */}
      <div className="celestial-card p-6 rounded-3xl bg-surface border border-outline-variant/60 shadow-xs space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-outline-variant/40 pb-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-primary/10 border border-primary/20 flex items-center justify-center text-primary shrink-0">
              <span className="material-symbols-outlined text-2xl">psychology</span>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-display text-2xl font-bold text-primary">
                  The Four Temperaments & Psychological Archetype
                </h3>
                <span className="text-[11px] font-extrabold bg-primary-fixed text-primary px-2.5 py-0.5 rounded-full">
                  Vedic Psychology
                </span>
              </div>
              <p className="text-xs text-on-surface-variant font-medium mt-0.5">
                Classical Four Temperaments analysis derived from your birth chart's elemental distribution and planetary dignities.
              </p>
            </div>
          </div>

          {/* Dominant Badge */}
          <div className="flex flex-wrap items-center gap-2">
            <div className="bg-primary/10 border border-primary/30 px-3.5 py-1.5 rounded-2xl text-xs flex items-center gap-2">
              <span className="text-on-surface-variant font-medium">Primary:</span>
              <strong className="text-primary font-bold">{dominantTemp.name} ({scoresMap[dominantTemp.id]}%)</strong>
            </div>
            <div className="bg-surface-variant/40 border border-outline-variant/50 px-3.5 py-1.5 rounded-2xl text-xs flex items-center gap-2">
              <span className="text-on-surface-variant font-medium">Secondary:</span>
              <strong className="text-on-surface font-bold">{secondaryTemp.name} ({scoresMap[secondaryTemp.id]}%)</strong>
            </div>
          </div>
        </div>

        {/* 4 Temperaments Table Grid Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 pt-2">
          {TEMPERAMENTS.map((t) => {
            const isSelected = selectedTempId === t.id
            const isDominant = dominantTemp.id === t.id
            const score = scoresMap[t.id] || 25

            return (
              <div
                key={t.id}
                onClick={() => setSelectedTempId(t.id)}
                className={`p-4 rounded-2xl border transition-all cursor-pointer flex flex-col justify-between space-y-3 ${
                  isSelected
                    ? `${t.color} ring-2 ring-primary/20 shadow-md scale-[1.02]`
                    : 'bg-surface-variant/30 border-outline-variant/50 hover:border-primary/40 hover:bg-surface-variant/50'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="material-symbols-outlined text-xl">{t.icon}</span>
                    <h5 className="font-display text-lg font-bold text-primary">
                      {t.name}
                    </h5>
                  </div>
                  {isDominant && (
                    <span className="text-[10px] font-extrabold bg-primary text-white px-2 py-0.5 rounded-full">
                      Dominant
                    </span>
                  )}
                </div>

                <div className="space-y-1 text-xs">
                  <div className="flex justify-between items-center text-[11px] font-semibold text-on-surface-variant">
                    <span>{t.element}</span>
                    <strong className="text-primary">{score}%</strong>
                  </div>
                  <div className="w-full bg-surface-variant/60 rounded-full h-1.5 overflow-hidden">
                    <div
                      className="bg-primary h-full rounded-full transition-all duration-500"
                      style={{ width: `${score}%` }}
                    />
                  </div>
                </div>

                <div className="space-y-1 pt-1 border-t border-outline-variant/30 text-[11px]">
                  <p className="font-semibold text-primary">
                    Traits: <span className="font-normal text-on-surface-variant">{t.coreTraits}</span>
                  </p>
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Selected Temperament Detailed Breakdown Card */}
      {activeTemp && (
        <div className="celestial-card p-6 rounded-3xl bg-surface border border-outline-variant/60 shadow-xs space-y-4 animate-fade-in-up">
          <div className="flex flex-wrap items-center justify-between gap-3 border-b border-outline-variant/40 pb-3">
            <div>
              <span className="text-[10px] font-extrabold text-primary uppercase tracking-wider bg-primary-fixed px-2.5 py-0.5 rounded-full">
                Detailed Temperament Analysis
              </span>
              <h4 className="font-display text-2xl font-bold text-primary mt-1 flex items-center gap-2">
                <span className="material-symbols-outlined text-2xl">{activeTemp.icon}</span>
                {activeTemp.name} ({activeTemp.devanagari}) — {activeTemp.element}
              </h4>
            </div>

            <span className="text-xs font-bold text-primary bg-surface-variant border border-outline-variant/60 px-3 py-1 rounded-full">
              Elemental Alignment: {scoresMap[activeTemp.id]}%
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Core Traits & Strengths */}
            <div className="bg-surface-variant/30 p-4 rounded-2xl border border-outline-variant/40 space-y-2">
              <div className="flex items-center gap-2 font-bold text-sm text-emerald-900">
                <span className="material-symbols-outlined text-emerald-600 text-lg">stars</span>
                <h6>Core Strengths & Virtues</h6>
              </div>
              <p className="text-xs text-on-surface leading-relaxed font-semibold">
                {activeTemp.strengths}
              </p>
              <p className="text-xs text-on-surface-variant leading-relaxed">
                {activeTemp.coreTraits}
              </p>
            </div>

            {/* Challenges */}
            <div className="bg-surface-variant/30 p-4 rounded-2xl border border-outline-variant/40 space-y-2">
              <div className="flex items-center gap-2 font-bold text-sm text-amber-950">
                <span className="material-symbols-outlined text-amber-600 text-lg">warning</span>
                <h6>Potential Challenges & Pitfalls</h6>
              </div>
              <p className="text-xs text-on-surface leading-relaxed font-semibold text-amber-950">
                {activeTemp.challenges}
              </p>
              <p className="text-xs text-on-surface-variant leading-relaxed">
                {activeTemp.astrologicalBasis}
              </p>
            </div>

            {/* Recommendations */}
            <div className="bg-primary/5 p-4 rounded-2xl border border-primary/30 space-y-2">
              <div className="flex items-center gap-2 font-bold text-sm text-primary">
                <span className="material-symbols-outlined text-primary text-lg">auto_awesome</span>
                <h6>Vedic Growth Recommendations</h6>
              </div>
              <p className="text-xs text-on-surface font-medium leading-relaxed">
                {activeTemp.recommendations}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
