import type { TabType } from './TabNavigation'

interface SummaryCardItem {
  label: string
  value: string | number
  subtext?: string
  icon?: string
  color?: string
}

interface SummaryCardsProps {
  tab: TabType
  chartData: any
  computed?: any
}

export default function SummaryCards({ tab, chartData, computed }: SummaryCardsProps) {
  const cards = getCardsForTab(tab, chartData, computed)

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
      {cards.map((card, i) => (
        <div
          key={i}
          className="celestial-card p-4 rounded-2xl bg-surface border border-outline-variant/60 shadow-xs hover:border-primary/40 transition-all flex flex-col justify-between"
        >
          <div className="flex items-center justify-between mb-2">
            <span className="text-[11px] font-bold uppercase tracking-wider text-on-surface-variant/80">
              {card.label}
            </span>
            {card.icon && (
              <span className="material-symbols-outlined text-primary text-xl opacity-80">
                {card.icon}
              </span>
            )}
          </div>
          <div>
            <p className="font-display text-2xl font-bold text-primary leading-tight">
              {card.value}
            </p>
            {card.subtext && (
              <p className="text-[11px] text-on-surface-variant mt-1 leading-snug line-clamp-1">
                {card.subtext}
              </p>
            )}
          </div>
        </div>
      ))}
    </div>
  )
}

function getCardsForTab(tab: TabType, chartData: any, computed?: any): SummaryCardItem[] {
  const meta = {
    ascendant_sign: chartData?.metadata?.ascendant_sign || chartData?.ascendant_sign || 'Aries',
    moon_sign: chartData?.metadata?.moon_sign || chartData?.moon_sign || 'Cancer',
    nakshatra: chartData?.metadata?.nakshatra || chartData?.nakshatra || 'Pushya',
    pada: chartData?.metadata?.pada || chartData?.pada || 1,
  }
  const planets = chartData?.raw_positions || chartData?.planets || {}
  const houses = chartData?.houses || {}
  const doshas = chartData?.doshas || {}
  const yogas = chartData?.yogas || []
  const comp = computed || chartData?.computed || {}
  const currentDasha = chartData?.current_dasha || 'Jupiter'

  switch (tab) {
    case 'overview':
      return [
        { label: 'Lagna (Ascendant)', value: meta.ascendant_sign, icon: 'person', subtext: 'Core personality & body' },
        { label: 'Moon Sign (Rashi)', value: meta.moon_sign, icon: 'brightness_3', subtext: 'Mind & emotions' },
        { label: 'Nakshatra', value: meta.nakshatra, icon: 'auto_awesome', subtext: `Pada ${meta.pada}` },
        { label: 'Current Dasha', value: currentDasha, icon: 'schedule', subtext: 'Major life chapter' },
        { label: 'Lucky Color', value: comp.lucky?.lucky_colors?.[0] || 'Gold', icon: 'palette' },
        { label: 'Lucky Number', value: comp.lucky?.lucky_numbers?.[0] ?? 1, icon: 'pin' },
        { label: 'Lucky Day', value: comp.lucky?.lucky_day || 'Sunday', icon: 'calendar_today' },
        { label: 'Dominant Element', value: comp.elements?.dominant || 'Fire', icon: 'water_drop' },
      ]

    case 'career':
      return [
        { label: '10th House (Karma)', value: getHouseLord('10', chartData), icon: 'work', subtext: `Sign: ${houses['10']?.sign || 'N/A'}` },
        { label: 'Sun Sign', value: planets.sun?.sign ? `${planets.sun.sign} (H${planets.sun.house || '?'})` : 'N/A', icon: 'wb_sunny', subtext: 'Authority & status' },
        { label: 'Career Yogas', value: `${yogas.length} Active`, icon: 'stars', subtext: yogas[0]?.name || 'Raj Yoga' },
        { label: '10th Lord Status', value: getLordDignity('10', chartData, planets), icon: 'trending_up', subtext: 'Karma lord strength' },
      ]

    case 'marriage':
      return [
        { label: '7th House Lord', value: getHouseLord('7', chartData), icon: 'favorite', subtext: `Sign: ${houses['7']?.sign || 'N/A'}` },
        { label: 'Venus Placement', value: planets.venus?.sign ? `${planets.venus.sign} (H${planets.venus.house || '?'})` : 'N/A', icon: 'favorite_border', subtext: planets.venus?.dignity || 'Relationships' },
        { label: 'Manglik Status', value: doshas.manglik?.is_present ? 'Active' : 'Non-Manglik', icon: 'shield_moon', subtext: doshas.manglik?.is_present ? doshas.manglik.description || 'Mars in 7th' : 'No affliction' },
        { label: '7th House Sign', value: houses['7']?.sign || 'N/A', icon: 'groups', subtext: 'Partnership Sign' },
      ]

    case 'health':
      return [
        { label: '1st House Lord', value: getHouseLord('1', chartData), icon: 'fitness_center', subtext: 'Vitality Lord' },
        { label: '6th House Lord', value: getHouseLord('6', chartData), icon: 'medical_services', subtext: 'Immunity Lord' },
        { label: 'Dominant Dosha', value: comp.prakriti?.dominant_dosha || 'Kapha', icon: 'spa', subtext: `Vata ${comp.prakriti?.vata || 30}% | Pitta ${comp.prakriti?.pitta || 35}%` },
        { label: 'Weakest Planet', value: comp.remedy_data?.weak_planets?.[0]?.display_name || 'Balanced', icon: 'warning', subtext: comp.remedy_data?.weak_planets?.[0]?.status || 'No severe affliction' },
      ]

    case 'food':
      return [
        { label: 'Vata Proportion', value: `${comp.prakriti?.vata ?? 33.3}%`, icon: 'air', subtext: 'Air & Ether element' },
        { label: 'Pitta Proportion', value: `${comp.prakriti?.pitta ?? 33.3}%`, icon: 'local_fire_department', subtext: 'Fire & Water element' },
        { label: 'Kapha Proportion', value: `${comp.prakriti?.kapha ?? 33.4}%`, icon: 'water', subtext: 'Earth & Water element' },
        { label: 'Dominant Constitution', value: comp.prakriti?.dominant_dosha || 'Kapha', icon: 'restaurant', subtext: 'Prakriti Type' },
      ]

    case 'remedies':
      return [
        { label: 'Afflicted Planets', value: `${comp.remedy_data?.weak_planets?.length || 0} Planets`, icon: 'warning', subtext: 'Requires remedy' },
        { label: 'Primary Weak Planet', value: comp.remedy_data?.weak_planets?.[0]?.display_name || 'None', icon: 'nature_people', subtext: comp.remedy_data?.weak_planets?.[0]?.status || 'Chart Balanced' },
        { label: 'Recommended Gem', value: comp.remedy_data?.weak_planets?.[0]?.remedies?.gemstone?.primary || 'Pearl / Ruby', icon: 'diamond', subtext: 'Consult Jyotish expert' },
        { label: 'Fasting Day', value: comp.remedy_data?.weak_planets?.[0]?.remedies?.fasting_day || 'Monday', icon: 'event', subtext: 'Weekly discipline' },
      ]

    case 'finance':
      return [
        { label: '2nd House (Wealth)', value: getHouseLord('2', chartData), icon: 'account_balance', subtext: `Sign: ${houses['2']?.sign || 'N/A'}` },
        { label: '11th House (Gains)', value: getHouseLord('11', chartData), icon: 'payments', subtext: `Sign: ${houses['11']?.sign || 'N/A'}` },
        { label: 'Jupiter Placement', value: planets.jupiter?.sign ? `${planets.jupiter.sign} (H${planets.jupiter.house || '?'})` : 'N/A', icon: 'monetization_on', subtext: 'Karak for Wealth' },
        { label: '5th House (Investments)', value: getHouseLord('5', chartData), icon: 'pie_chart', subtext: `Sign: ${houses['5']?.sign || 'N/A'}` },
      ]

    case 'personality':
      return [
        { label: 'Ascendant Sign', value: meta.ascendant_sign, icon: 'face', subtext: 'Outer persona' },
        { label: 'Moon Sign', value: meta.moon_sign, icon: 'psychology', subtext: 'Emotional core' },
        { label: 'Mercury Sign', value: planets.mercury?.sign ? `${planets.mercury.sign} (H${planets.mercury.house || '?'})` : 'N/A', icon: 'chat', subtext: 'Intellect & Speech' },
        { label: 'Mars Sign', value: planets.mars?.sign ? `${planets.mars.sign} (H${planets.mars.house || '?'})` : 'N/A', icon: 'bolt', subtext: 'Courage & Action' },
      ]

    case 'spiritual':
      return [
        { label: '9th House (Dharma)', value: getHouseLord('9', chartData), icon: 'auto_awesome', subtext: `Sign: ${houses['9']?.sign || 'N/A'}` },
        { label: '12th House (Moksha)', value: getHouseLord('12', chartData), icon: 'self_improvement', subtext: `Sign: ${houses['12']?.sign || 'N/A'}` },
        { label: 'Ketu Placement', value: planets.ketu?.sign ? `${planets.ketu.sign} (H${planets.ketu.house || '?'})` : 'N/A', icon: 'landscape', subtext: 'Detachment path' },
        { label: 'Recommended Path', value: getSpiritualPath(comp.elements?.dominant), icon: 'menu_book', subtext: 'Based on element' },
      ]

    default:
      return []
  }
}

function getHouseLord(houseNum: string, chartData: any): string {
  const houses = chartData?.houses || {}
  const h = houses[houseNum]
  if (h?.lord) return h.lord.charAt(0).toUpperCase() + h.lord.slice(1)
  return 'Benefic'
}

function getLordDignity(houseNum: string, chartData: any, planets: any): string {
  const houses = chartData?.houses || {}
  const lord = houses[houseNum]?.lord?.toLowerCase()
  if (lord && planets[lord]) {
    const p = planets[lord]
    return p.dignity ? `${p.dignity.charAt(0).toUpperCase() + p.dignity.slice(1)}` : `House ${p.house || '?'}`
  }
  return 'Favorable'
}

function getSpiritualPath(element?: string): string {
  switch (element) {
    case 'Air':
      return 'Pranayama & Kriya'
    case 'Water':
      return 'Bhakti & Devotion'
    case 'Fire':
      return 'Tapas & Discipline'
    case 'Earth':
      return 'Karma Yoga & Service'
    default:
      return 'Jnana & Self-Inquiry'
  }
}
