import { useState } from 'react'
import {
  NORTH_INDIAN_HOUSES,
  getHouseSignNumber,
  PLANET_INFO_MAP,
} from '../../utils/kundliGeometry'
import { formatSignWithHindi } from '../../utils/hindiMapping'

interface AnimatedKundliChartProps {
  chartData: any
}

export default function AnimatedKundliChart({ chartData }: AnimatedKundliChartProps) {
  const [animKey, setAnimKey] = useState(0)
  const [hoveredHouse, setHoveredHouse] = useState<number | null>(null)
  const [hoveredPlanet, setHoveredPlanet] = useState<any | null>(null)

  const meta = {
    ascendant_sign: chartData?.metadata?.ascendant_sign || chartData?.ascendant_sign || 'Scorpio',
    moon_sign: chartData?.metadata?.moon_sign || chartData?.moon_sign || 'Aries',
    nakshatra: chartData?.metadata?.nakshatra || chartData?.nakshatra || 'Ashwini',
  }

  const planets = chartData?.raw_positions || chartData?.planets || {}

  // Group planets by house (1 to 12)
  const housePlanets: Record<number, Array<{ key: string; data: any }>> = {}
  for (let h = 1; h <= 12; h++) {
    housePlanets[h] = []
  }

  Object.entries(planets).forEach(([pName, pData]: [string, any]) => {
    const houseNum = Number(pData?.house) || 1
    if (housePlanets[houseNum]) {
      housePlanets[houseNum].push({ key: pName.toLowerCase(), data: pData })
    }
  })

  const handleReplayAnimation = () => {
    setAnimKey((prev) => prev + 1)
  }

  // SVG grid line paths for North Indian Kundli chart (Canvas 400x400)
  const lines = [
    // Outer square border lines
    { x1: 0, y1: 0, x2: 400, y2: 0, delay: '0ms' },
    { x1: 400, y1: 0, x2: 400, y2: 400, delay: '150ms' },
    { x1: 400, y1: 400, x2: 0, y2: 400, delay: '300ms' },
    { x1: 0, y1: 400, x2: 0, y2: 0, delay: '450ms' },

    // Main Diagonals
    { x1: 0, y1: 0, x2: 400, y2: 400, delay: '600ms' },
    { x1: 0, y1: 400, x2: 400, y2: 0, delay: '750ms' },

    // Inner Diamond
    { x1: 200, y1: 0, x2: 400, y2: 200, delay: '900ms' },
    { x1: 400, y1: 200, x2: 200, y2: 400, delay: '1050ms' },
    { x1: 200, y1: 400, x2: 0, y2: 200, delay: '1200ms' },
    { x1: 0, y1: 200, x2: 200, y2: 0, delay: '1350ms' },
  ]

  return (
    <div className="celestial-card p-6 rounded-3xl bg-surface border border-outline-variant/60 shadow-md mb-8 animate-fade-in-up">
      {/* Header Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 mb-4 border-b border-outline-variant/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-primary text-2xl">grid_view</span>
            <h3 className="font-display text-2xl font-bold text-primary">
              D1 Janam Kundli (Lagna Birth Chart)
            </h3>
          </div>
          <p className="text-xs text-on-surface-variant font-medium mt-0.5">
            Ascendant: <strong className="text-primary">{formatSignWithHindi(meta.ascendant_sign)}</strong> · <span className="font-bold text-primary">H1–H12</span> House Numbers · <span className="font-bold text-amber-700">1–12</span> Zodiac Sign Numbers
          </p>

        </div>

        <button
          onClick={handleReplayAnimation}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-primary-fixed hover:bg-primary-fixed/80 text-primary border border-primary/20 text-xs font-bold rounded-xl transition-all cursor-pointer shadow-xs"
          title="Replay drawing animation"
        >
          <span className="material-symbols-outlined text-base">replay</span>
          Re-Draw Chart
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
        {/* Animated Kundli SVG Canvas */}
        <div className="lg:col-span-7 flex justify-center relative">
          <div className="w-full max-w-[420px] aspect-square relative p-2 bg-surface-variant/20 rounded-3xl border border-outline-variant/50 shadow-inner">
            <svg
              key={animKey}
              viewBox="0 0 400 400"
              className="w-full h-full drop-shadow-sm select-none"
            >
              {/* Outer Glow Defs */}
              <defs>
                <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                  <feGaussianBlur stdDeviation="3" result="blur" />
                  <feComposite in="SourceGraphic" in2="blur" operator="over" />
                </filter>
              </defs>

              {/* Animated Chart Grid Lines */}
              {lines.map((line, idx) => (
                <line
                  key={`${animKey}-line-${idx}`}
                  x1={line.x1}
                  y1={line.y1}
                  x2={line.x2}
                  y2={line.y2}
                  stroke="var(--color-primary)"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                  className="kundli-line-animate opacity-90"
                  style={{ animationDelay: line.delay }}
                />
              ))}
              {/* Houses (House Numbers H1-H12, Sign Numbers & Planet Badges) */}
              {Object.entries(NORTH_INDIAN_HOUSES).map(([hStr, houseInfo]) => {
                const hNum = Number(hStr)
                const signNum = getHouseSignNumber(hNum, meta.ascendant_sign)
                const planetsInHouse = housePlanets[hNum] || []
                const isHovered = hoveredHouse === hNum

                return (
                  <g
                    key={`house-${hNum}`}
                    onMouseEnter={() => setHoveredHouse(hNum)}
                    onMouseLeave={() => setHoveredHouse(null)}
                    className="cursor-pointer transition-all"
                  >
                    {/* Explicit House Number Badge (H1 to H12) */}
                    <text
                      x={houseInfo.houseX}
                      y={houseInfo.houseY}
                      textAnchor="middle"
                      dominantBaseline="central"
                      className={`text-[10px] font-mono font-extrabold fill-primary transition-all ${
                        isHovered ? 'scale-110 fill-amber-700' : 'opacity-85'
                      }`}
                    >
                      H{hNum}
                    </text>

                    {/* Zodiac Sign Number Badge (Rashi 1-12) */}
                    <text
                      x={houseInfo.signX}
                      y={houseInfo.signY}
                      textAnchor="middle"
                      dominantBaseline="central"
                      className={`text-[12px] font-bold fill-[#B37D4E] transition-all ${
                        isHovered ? 'opacity-100 font-extrabold fill-primary' : 'opacity-75'
                      }`}
                    >
                      {signNum}
                    </text>

                    {/* Ascendant Badge in House 1 if no planet in House 1 */}
                    {hNum === 1 && planetsInHouse.length === 0 && (
                      <text
                        x={houseInfo.planetX}
                        y={houseInfo.planetY}
                        textAnchor="middle"
                        dominantBaseline="central"
                        className="text-[13px] font-extrabold fill-primary select-none animate-planet-in"
                        style={{ animationDelay: '1000ms' }}
                      >
                        Asc
                      </text>
                    )}


                    {/* Planet Badges inside House Centroid */}
                    {planetsInHouse.length > 0 && (
                      <g transform={`translate(${houseInfo.planetX}, ${houseInfo.planetY})`}>
                        {planetsInHouse.map((p, pIdx) => {
                          const info = PLANET_INFO_MAP[p.key] || {
                            short: p.key.slice(0, 2).toUpperCase(),
                            icon: '✨',
                            color: '#E67E22',
                          }

                          // Offset planets horizontally if multiple exist in same house
                          const total = planetsInHouse.length
                          const spacing = total >= 3 ? 26 : 30
                          const offsetX = (pIdx - (total - 1) / 2) * spacing
                          const offsetY = 0

                          const isPlanetHovered = hoveredPlanet?.key === p.key

                          return (
                            <g
                              key={p.key}
                              transform={`translate(${offsetX}, ${offsetY})`}
                              onMouseEnter={(e) => {
                                e.stopPropagation()
                                setHoveredPlanet({ key: p.key, data: p.data, house: hNum })
                              }}
                              onMouseLeave={() => setHoveredPlanet(null)}
                              className="animate-planet-in cursor-pointer"
                              style={{ animationDelay: `${1000 + pIdx * 100}ms` }}
                            >

                              {/* Planet Circle Badge */}
                              <circle
                                r="12"
                                fill="var(--color-surface)"
                                stroke={isPlanetHovered ? 'var(--color-primary)' : 'var(--color-outline-variant)'}
                                strokeWidth={isPlanetHovered ? '2' : '1.5'}
                                className="shadow-xs hover:scale-110 transition-all"
                              />
                              <text
                                textAnchor="middle"
                                dominantBaseline="central"
                                className="text-[10px] font-extrabold fill-primary select-none"
                              >
                                {info.short}
                              </text>
                            </g>
                          )
                        })}
                      </g>
                    )}
                  </g>
                )
              })}
            </svg>


            {/* Hover Tooltip Overlay */}
            {(hoveredPlanet || hoveredHouse) && (
              <div className="absolute bottom-3 left-1/2 -translate-x-1/2 bg-surface/95 backdrop-blur-md border border-primary/30 rounded-2xl px-4 py-2 shadow-lg text-center pointer-events-none animate-fade-in-up z-20 min-w-[220px]">
                {hoveredPlanet ? (
                  <div>
                    <p className="text-xs font-bold text-primary flex items-center justify-center gap-1">
                      <span>{PLANET_INFO_MAP[hoveredPlanet.key]?.icon}</span>
                      <span>
                        {hoveredPlanet.data?.name_sanskrit || hoveredPlanet.key.toUpperCase()} in House {hoveredPlanet.house}
                      </span>
                    </p>
                    <p className="text-[11px] text-on-surface-variant mt-0.5">
                      Sign: <strong>{formatSignWithHindi(hoveredPlanet.data?.sign)}</strong> · Degree: <strong>{hoveredPlanet.data?.degree?.toFixed(1)}°</strong>
                    </p>
                  </div>
                ) : hoveredHouse ? (
                  <div>
                    <p className="text-xs font-bold text-primary">
                      {NORTH_INDIAN_HOUSES[hoveredHouse]?.name} ({NORTH_INDIAN_HOUSES[hoveredHouse]?.hindiName})
                    </p>
                    <p className="text-[11px] text-on-surface-variant mt-0.5">
                      House Sign: <strong>{formatSignWithHindi(chartData?.houses?.[hoveredHouse]?.sign)}</strong> · Lord: <strong>{chartData?.houses?.[hoveredHouse]?.lord}</strong>
                    </p>
                  </div>
                ) : null}
              </div>
            )}
          </div>
        </div>

        {/* Side Info Panel — Key Chart Highlights */}
        <div className="lg:col-span-5 space-y-4">
          <div className="bg-primary-fixed/40 border border-primary/20 rounded-2xl p-4">
            <h4 className="font-display text-lg font-bold text-primary mb-2 flex items-center gap-2">
              <span className="material-symbols-outlined text-xl">auto_awesome</span>
              Chart Placement Legend
            </h4>
            <p className="text-xs text-on-surface-variant leading-relaxed">
              The top diamond represents <strong className="text-primary">House 1 (Lagna)</strong>. Sign numbers (1–12) follow the traditional North Indian counter-clockwise layout starting from your Ascendant sign.
            </p>
          </div>

          {/* Quick Planet Pills */}
          <div className="bg-surface rounded-2xl border border-outline-variant/60 p-4">
            <span className="text-[11px] font-bold uppercase tracking-wider text-on-surface-variant block mb-3">
              Planetary Locations ({Object.keys(planets).length} Grahas)
            </span>
            <div className="flex flex-wrap gap-2">
              {Object.entries(planets).map(([pName, pData]: [string, any]) => {
                const info = PLANET_INFO_MAP[pName.toLowerCase()] || {
                  short: pName.slice(0, 2).toUpperCase(),
                  icon: '✨',
                }
                return (
                  <div
                    key={pName}
                    className="flex items-center gap-1.5 bg-surface-variant/40 border border-outline-variant/50 px-2.5 py-1 rounded-xl text-xs font-semibold text-on-surface hover:border-primary/40 transition-colors"
                  >
                    <span>{info.icon}</span>
                    <span>{pName.charAt(0).toUpperCase() + pName.slice(1)}</span>
                    <span className="text-primary font-bold">H{pData?.house}</span>
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
