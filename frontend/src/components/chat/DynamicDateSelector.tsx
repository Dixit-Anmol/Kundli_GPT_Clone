import { useState, useEffect } from 'react'

interface DynamicDateSelectorProps {
  value: string // YYYY-MM-DD
  onChange: (dateStr: string) => void
  label?: string
  required?: boolean
}

const MONTHS = [
  { value: '01', label: 'Jan (01)' },
  { value: '02', label: 'Feb (02)' },
  { value: '03', label: 'Mar (03)' },
  { value: '04', label: 'Apr (04)' },
  { value: '05', label: 'May (05)' },
  { value: '06', label: 'Jun (06)' },
  { value: '07', label: 'Jul (07)' },
  { value: '08', label: 'Aug (08)' },
  { value: '09', label: 'Sep (09)' },
  { value: '10', label: 'Oct (10)' },
  { value: '11', label: 'Nov (11)' },
  { value: '12', label: 'Dec (12)' },
]

export default function DynamicDateSelector({
  value,
  onChange,
  label = '📅 Date of Birth',
  required = false,
}: DynamicDateSelectorProps) {
  // Parse initial YYYY-MM-DD
  const parts = (value || '').split('-')
  const initialYear = parts[0] || '1995'
  const initialMonth = parts[1] || '01'
  const initialDay = parts[2] || '01'

  const [year, setYear] = useState(initialYear)
  const [month, setMonth] = useState(initialMonth)
  const [day, setDay] = useState(initialDay)

  // Generate Year options from current year down to 1940
  const currentYear = new Date().getFullYear()
  const years: string[] = []
  for (let y = currentYear; y >= 1940; y--) {
    years.push(y.toString())
  }

  // Calculate max days in selected month & year
  const getMaxDays = (yStr: string, mStr: string) => {
    const y = parseInt(yStr, 10) || 1995
    const m = parseInt(mStr, 10) || 1
    return new Date(y, m, 0).getDate()
  }

  const maxDays = getMaxDays(year, month)
  const days: string[] = []
  for (let d = 1; d <= maxDays; d++) {
    days.push(d < 10 ? `0${d}` : d.toString())
  }

  // Handle updates
  useEffect(() => {
    // If current day exceeds max days for new month, adjust day
    let validDay = day
    if (parseInt(day, 10) > maxDays) {
      validDay = maxDays < 10 ? `0${maxDays}` : maxDays.toString()
      setDay(validDay)
    }

    if (year && month && validDay) {
      const formatted = `${year}-${month}-${validDay}`
      if (formatted !== value) {
        onChange(formatted)
      }
    }
  }, [year, month, day, maxDays])

  return (
    <div className="space-y-2">
      {label && (
        <label className="text-xs font-bold text-primary block">
          {label} {required && '*'}
        </label>
      )}

      {/* 3 Themed Dropdown Selectors Grid */}
      <div className="grid grid-cols-3 gap-2 sm:gap-3">
        {/* Day Selector */}
        <div>
          <span className="text-[10px] font-bold uppercase tracking-wider text-on-surface-variant block mb-1">
            Day
          </span>
          <select
            value={day}
            onChange={(e) => setDay(e.target.value)}
            className="w-full bg-surface border border-outline-variant/60 rounded-2xl px-3 py-3 text-xs sm:text-sm text-primary font-bold focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary cursor-pointer shadow-xs hover:border-primary/50 transition-all"
          >
            {days.map((d) => (
              <option key={d} value={d}>
                {d}
              </option>
            ))}
          </select>
        </div>

        {/* Month Selector */}
        <div>
          <span className="text-[10px] font-bold uppercase tracking-wider text-on-surface-variant block mb-1">
            Month
          </span>
          <select
            value={month}
            onChange={(e) => setMonth(e.target.value)}
            className="w-full bg-surface border border-outline-variant/60 rounded-2xl px-3 py-3 text-xs sm:text-sm text-primary font-bold focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary cursor-pointer shadow-xs hover:border-primary/50 transition-all"
          >
            {MONTHS.map((m) => (
              <option key={m.value} value={m.value}>
                {m.label}
              </option>
            ))}
          </select>
        </div>

        {/* Year Selector */}
        <div>
          <span className="text-[10px] font-bold uppercase tracking-wider text-on-surface-variant block mb-1">
            Year
          </span>
          <select
            value={year}
            onChange={(e) => setYear(e.target.value)}
            className="w-full bg-surface border border-outline-variant/60 rounded-2xl px-3 py-3 text-xs sm:text-sm text-primary font-bold focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary cursor-pointer shadow-xs hover:border-primary/50 transition-all"
          >
            {years.map((y) => (
              <option key={y} value={y}>
                {y}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Formatted Date Pill Preview */}
      <div className="flex items-center justify-between px-3 py-1.5 bg-surface-variant/30 rounded-xl border border-outline-variant/40 text-[11px] font-semibold text-on-surface-variant">
        <span>Selected Birth Date:</span>
        <span className="font-bold text-primary font-mono bg-surface px-2 py-0.5 rounded-md border border-outline-variant/40">
          {year}-{month}-{day}
        </span>
      </div>
    </div>
  )
}
