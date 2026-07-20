import { formatSignWithHindi, formatPlanetWithHindi } from '../../utils/hindiMapping'
import type { RelationshipTarget } from './RelationshipTargetSelector'

interface RelationshipScoreCardProps {
  target: RelationshipTarget
  chartData: any
}

// Client-side quick target helper to compute primary indicator badges
export default function RelationshipScoreCard({ target, chartData }: RelationshipScoreCardProps) {
  const planets = chartData?.raw_positions || chartData?.planets || {}
  const houses = chartData?.houses || {}
  const doshas = chartData?.doshas || {}

  const meta = getTargetMetadata(target, planets, houses, doshas)

  return (
    <div className="celestial-card p-5 rounded-3xl bg-surface border border-outline-variant/60 shadow-xs mb-6 animate-fade-in-up">
      <div className="flex flex-wrap items-center justify-between gap-4">
        {/* Score Ring & Title */}
        <div className="flex items-center gap-4">
          <div className="relative w-16 h-16 flex items-center justify-center rounded-2xl bg-primary-fixed border border-primary/30 shadow-xs">
            <span className="material-symbols-outlined text-primary text-3xl">
              {meta.icon}
            </span>
          </div>

          <div>
            <div className="flex items-center gap-2">
              <h3 className="font-display text-2xl font-bold text-primary">
                {meta.title} Analysis
              </h3>
              <span className="text-xs font-bold text-primary bg-primary-fixed/80 border border-primary/20 px-2.5 py-0.5 rounded-full">
                Vedic Engine
              </span>
            </div>
            <p className="text-xs text-on-surface-variant font-medium mt-0.5">
              Primary Houses: <strong className="text-primary">{meta.primaryHouses}</strong> · Karakas: <strong className="text-primary">{meta.karakas}</strong>
            </p>
          </div>
        </div>

        {/* Dynamic Key Indicators */}
        <div className="flex flex-wrap items-center gap-2">
          <div className="bg-surface-variant/40 border border-outline-variant/50 px-3 py-1.5 rounded-2xl text-xs font-medium text-on-surface">
            <span className="text-on-surface-variant text-[11px] block font-semibold">Primary Lord</span>
            <strong className="text-primary">{meta.primaryLord}</strong>
          </div>

          <div className="bg-surface-variant/40 border border-outline-variant/50 px-3 py-1.5 rounded-2xl text-xs font-medium text-on-surface">
            <span className="text-on-surface-variant text-[11px] block font-semibold">Primary Karaka</span>
            <strong className="text-primary">{meta.karakaStatus}</strong>
          </div>

          {meta.doshaBadge && (
            <div className="bg-amber-50 border border-amber-200 px-3 py-1.5 rounded-2xl text-xs font-semibold text-amber-800">
              <span className="text-amber-600 text-[11px] block font-semibold">Key Affliction</span>
              <span>{meta.doshaBadge}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

function getTargetMetadata(target: RelationshipTarget, planets: any, houses: any, doshas: any) {
  switch (target) {
    case 'father': {
      const h9 = houses['9']
      const lord9 = h9?.lord ? formatPlanetWithHindi(h9.lord) : 'Moon'
      const sun = planets.sun || {}
      return {
        title: 'Father (Pitr)',
        icon: 'person',
        primaryHouses: '9th (Father), 10th, 1st',
        karakas: 'Sun, Jupiter',
        primaryLord: `${lord9} (${formatSignWithHindi(h9?.sign)})`,
        karakaStatus: sun.sign ? `Sun in ${formatSignWithHindi(sun.sign)}` : 'Sun',
        doshaBadge: sun.dignity === 'debilitated' ? 'Sun Weakened' : null,
      }
    }
    case 'mother': {
      const h4 = houses['4']
      const lord4 = h4?.lord ? formatPlanetWithHindi(h4.lord) : 'Saturn'
      const moon = planets.moon || {}
      return {
        title: 'Mother (Matr)',
        icon: 'face_3',
        primaryHouses: '4th (Mother), 1st, 10th',
        karakas: 'Moon, Venus',
        primaryLord: `${lord4} (${formatSignWithHindi(h4?.sign)})`,
        karakaStatus: moon.sign ? `Moon in ${formatSignWithHindi(moon.sign)}` : 'Moon',
        doshaBadge: moon.dignity === 'debilitated' ? 'Moon Afflicted' : null,
      }
    }
    case 'siblings': {
      const h3 = houses['3']
      const lord3 = h3?.lord ? formatPlanetWithHindi(h3.lord) : 'Saturn'
      const mars = planets.mars || {}
      return {
        title: 'Siblings (Bhratr)',
        icon: 'groups',
        primaryHouses: '3rd (Younger), 11th (Elder)',
        karakas: 'Mars, Mercury',
        primaryLord: `${lord3} (${formatSignWithHindi(h3?.sign)})`,
        karakaStatus: mars.sign ? `Mars in ${formatSignWithHindi(mars.sign)}` : 'Mars',
        doshaBadge: null,
      }
    }
    case 'children': {
      const h5 = houses['5']
      const lord5 = h5?.lord ? formatPlanetWithHindi(h5.lord) : 'Jupiter'
      const jup = planets.jupiter || {}
      return {
        title: 'Children (Santana)',
        icon: 'child_care',
        primaryHouses: '5th (Progeny), 9th',
        karakas: 'Jupiter, Sun',
        primaryLord: `${lord5} (${formatSignWithHindi(h5?.sign)})`,
        karakaStatus: jup.sign ? `Jupiter in ${formatSignWithHindi(jup.sign)}` : 'Jupiter',
        doshaBadge: jup.house === 6 || jup.house === 8 || jup.house === 12 ? 'Jupiter in Dusthana' : null,
      }
    }
    case 'friends': {
      const h11 = houses['11']
      const lord11 = h11?.lord ? formatPlanetWithHindi(h11.lord) : 'Mercury'
      const merc = planets.mercury || {}
      return {
        title: 'Friends (Maitri)',
        icon: 'handshake',
        primaryHouses: '11th (Gains), 3rd',
        karakas: 'Mercury, Jupiter',
        primaryLord: `${lord11} (${formatSignWithHindi(h11?.sign)})`,
        karakaStatus: merc.sign ? `Mercury in ${formatSignWithHindi(merc.sign)}` : 'Mercury',
        doshaBadge: null,
      }
    }
    case 'boss': {
      const h10 = houses['10']
      const lord10 = h10?.lord ? formatPlanetWithHindi(h10.lord) : 'Sun'
      const sun = planets.sun || {}
      return {
        title: 'Boss & Authorities (Adhikari)',
        icon: 'badge',
        primaryHouses: '10th (Karma), 6th, 9th',
        karakas: 'Sun, Saturn, Jupiter',
        primaryLord: `${lord10} (${formatSignWithHindi(h10?.sign)})`,
        karakaStatus: sun.sign ? `Sun in ${formatSignWithHindi(sun.sign)}` : 'Sun',
        doshaBadge: null,
      }
    }
    case 'mentors': {
      const h9 = houses['9']
      const lord9 = h9?.lord ? formatPlanetWithHindi(h9.lord) : 'Moon'
      const jup = planets.jupiter || {}
      return {
        title: 'Mentors & Teachers (Guru)',
        icon: 'school',
        primaryHouses: '9th (Dharma/Guru), 5th',
        karakas: 'Jupiter, Sun',
        primaryLord: `${lord9} (${formatSignWithHindi(h9?.sign)})`,
        karakaStatus: jup.sign ? `Jupiter in ${formatSignWithHindi(jup.sign)}` : 'Jupiter',
        doshaBadge: null,
      }
    }
    case 'inlaws': {
      const h8 = houses['8']
      const lord8 = h8?.lord ? formatPlanetWithHindi(h8.lord) : 'Mercury'
      const venus = planets.venus || {}
      return {
        title: 'In-Laws (Kutumba)',
        icon: 'home',
        primaryHouses: '7th (Spouse), 8th (In-Laws), 2nd',
        karakas: 'Venus, Jupiter',
        primaryLord: `${lord8} (${formatSignWithHindi(h8?.sign)})`,
        karakaStatus: venus.sign ? `Venus in ${formatSignWithHindi(venus.sign)}` : 'Venus',
        doshaBadge: null,
      }
    }
    case 'spouse':
    default: {
      const h7 = houses['7']
      const lord7 = h7?.lord ? formatPlanetWithHindi(h7.lord) : 'Venus'
      const venus = planets.venus || {}
      const manglik = doshas?.manglik?.is_present
      return {
        title: 'Spouse / Partner (Kalatra)',
        icon: 'favorite',
        primaryHouses: '7th (Marriage), 2nd, 8th, 12th',
        karakas: 'Venus, Jupiter, Darakaraka',
        primaryLord: `${lord7} (${formatSignWithHindi(h7?.sign)})`,
        karakaStatus: venus.sign ? `Venus in ${formatSignWithHindi(venus.sign)}` : 'Venus',
        doshaBadge: manglik ? 'Manglik Active' : null,
      }
    }
  }
}
