interface HoroscopeDetail {
  label: string
  value: string
}

interface HoroscopeSummaryProps {
  details: HoroscopeDetail[]
  todaysEnergy: string
  onViewComplete: () => void
}

const defaultDetails: HoroscopeDetail[] = [
  { label: 'Ascendant (Lagna)', value: 'Libra' },
  { label: 'Moon Sign (Rashi)', value: 'Cancer' },
  { label: 'Current Dasha', value: 'Jupiter' },
  { label: 'Nakshatra', value: 'Pushya' },
]

const defaultEnergy =
  '"A harmonious day for financial ventures. Mars in your 11th house brings unexpected support from mentors. Focus on clear communication today."'

export default function HoroscopeSummary({
  details = defaultDetails,
  todaysEnergy = defaultEnergy,
  onViewComplete,
}: HoroscopeSummaryProps) {
  return (
    <div className="ml-12 celestial-card rounded-3xl p-6 border-2 border-primary/20 animate-fade-in-up delay-500">
      {/* Header */}
      <div className="flex items-start justify-between mb-6">
        <div>
          <span className="px-3 py-1 bg-tertiary-fixed text-on-tertiary-fixed rounded-full text-[10px] font-bold uppercase tracking-widest mb-2 inline-block">
            Analysis Complete
          </span>
          <h2 className="font-display text-[40px] leading-[48px] tracking-tight font-bold text-primary">
            ✨ Horoscope Ready
          </h2>
        </div>
        <div className="w-16 h-16 bg-primary-fixed rounded-2xl flex items-center justify-center border border-primary/10">
          <span
            className="material-symbols-outlined text-4xl text-primary"
            style={{ fontVariationSettings: "'FILL' 1" }}
          >
            balance
          </span>
        </div>
      </div>

      {/* Detail Grid */}
      <div className="grid grid-cols-2 gap-4 mb-12">
        {details.map((detail, i) => (
          <div key={i} className="p-4 bg-background rounded-2xl border border-outline-variant/60">
            <p className="text-[12px] leading-4 font-semibold text-on-surface-variant">
              {detail.label}
            </p>
            <p className="font-display text-[28px] leading-9 font-semibold text-primary">
              {detail.value}
            </p>
          </div>
        ))}
      </div>

      {/* Today's Energy */}
      <div className="bg-primary-fixed/50 p-4 rounded-2xl border border-primary/10 mb-12">
        <p className="text-[12px] leading-4 font-semibold text-primary mb-1 uppercase tracking-wider">
          Today's Energy
        </p>
        <p className="text-[16px] leading-6 text-on-surface-variant italic">{todaysEnergy}</p>
      </div>

      {/* CTA */}
      <button
        onClick={onViewComplete}
        className="w-full py-4 bg-inverse-surface text-white rounded-2xl font-display text-[28px] leading-9 font-semibold hover:bg-black transition-all shadow-md"
      >
        View Complete Horoscope
      </button>
    </div>
  )
}
