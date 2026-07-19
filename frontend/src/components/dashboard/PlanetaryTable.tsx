import { formatSignWithHindi, formatPlanetWithHindi } from '../../utils/hindiMapping'
import { PLANET_INFO_MAP } from '../../utils/kundliGeometry'

interface PlanetaryTableProps {
  chartData: any
}

export default function PlanetaryTable({ chartData }: PlanetaryTableProps) {
  const planets = chartData?.raw_positions || chartData?.planets || {}

  return (
    <div className="celestial-card p-6 rounded-3xl bg-surface border border-outline-variant/60 shadow-xs mb-8 animate-fade-in-up">
      <div className="flex items-center justify-between mb-4 border-b border-outline-variant/40 pb-3">
        <div className="flex items-center gap-2">
          <span className="material-symbols-outlined text-primary text-2xl">table_chart</span>
          <h3 className="font-display text-2xl font-bold text-primary">
            Planetary Placements & Dignity (Graha Sthiti)
          </h3>
        </div>
        <span className="text-xs font-semibold text-primary bg-primary-fixed px-3 py-1 rounded-full">
          Sidereal Lahiri Ayanamsha
        </span>
      </div>

      <div className="overflow-x-auto custom-scrollbar">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="border-b border-outline-variant/60 text-on-surface-variant uppercase tracking-wider font-bold">
              <th className="py-3 px-3">Graha (Planet)</th>
              <th className="py-3 px-3">Rashi (Sign)</th>
              <th className="py-3 px-3">Degree</th>
              <th className="py-3 px-3">Bhava (House)</th>
              <th className="py-3 px-3">Nakshatra</th>
              <th className="py-3 px-3">State / Dignity</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-outline-variant/30">
            {Object.entries(planets).map(([pName, pData]: [string, any]) => {
              const info = PLANET_INFO_MAP[pName.toLowerCase()] || {
                icon: '✨',
                hindi: pName,
              }
              const isRetro = pData?.retrograde
              const isCombust = pData?.combust

              return (
                <tr key={pName} className="hover:bg-surface-variant/30 transition-colors">
                  <td className="py-3 px-3 font-bold text-on-surface flex items-center gap-2">
                    <span className="text-base">{info.icon}</span>
                    <span>{formatPlanetWithHindi(pName)}</span>
                  </td>
                  <td className="py-3 px-3 font-medium text-primary">
                    {formatSignWithHindi(pData?.sign)}
                  </td>
                  <td className="py-3 px-3 text-on-surface font-semibold">
                    {pData?.degree?.toFixed(2)}°
                  </td>
                  <td className="py-3 px-3 text-on-surface font-bold">
                    House {pData?.house}
                  </td>
                  <td className="py-3 px-3 text-on-surface-variant">
                    {pData?.nakshatra?.name || pData?.nakshatra || 'N/A'} (Pada {pData?.nakshatra?.pada || pData?.pada || 1})
                  </td>
                  <td className="py-3 px-3">
                    <div className="flex items-center gap-1.5">
                      <span className={`px-2 py-0.5 rounded-md font-semibold text-[10px] ${
                        pData?.dignity === 'exalted' || pData?.dignity === 'own'
                          ? 'bg-green-100 text-green-800 border border-green-300'
                          : pData?.dignity === 'debilitated'
                          ? 'bg-red-100 text-red-800 border border-red-300'
                          : 'bg-surface-variant text-on-surface-variant'
                      }`}>
                        {pData?.dignity || 'Direct'}
                      </span>
                      {isRetro && (
                        <span className="bg-amber-100 text-amber-800 border border-amber-300 px-1.5 py-0.5 rounded text-[10px] font-bold">
                          Retrograde [R]
                        </span>
                      )}
                      {isCombust && (
                        <span className="bg-orange-100 text-orange-800 border border-orange-300 px-1.5 py-0.5 rounded text-[10px] font-bold">
                          Combust
                        </span>
                      )}
                    </div>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}
