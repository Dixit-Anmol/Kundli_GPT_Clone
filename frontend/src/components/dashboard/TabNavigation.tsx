import { isTabEnabled } from '../../config/featureFlags'

export type TabType =
  | 'overview'
  | 'career'
  | 'marriage'
  | 'health'
  | 'food'
  | 'remedies'
  | 'finance'
  | 'personality'
  | 'spiritual'

export interface TabConfig {
  id: TabType
  label: string
  icon: string
  description: string
}

export const ALL_TABS: TabConfig[] = [
  { id: 'overview', label: 'Overview', icon: 'grid_view', description: 'Complete Horoscope Summary' },
  { id: 'career', label: 'Career', icon: 'work', description: 'Profession, Business & Growth' },
  { id: 'marriage', label: 'Marriage', icon: 'favorite', description: 'Compatibility & Relationships' },
  { id: 'health', label: 'Health', icon: 'medical_services', description: 'Body Systems & Wellness' },
  { id: 'food', label: 'Food & Diet', icon: 'restaurant', description: 'Ayurvedic Prakriti & Nutrition' },
  { id: 'remedies', label: 'Remedies', icon: 'self_improvement', description: 'Mantras, Gemstones & Charity' },
  { id: 'finance', label: 'Finance', icon: 'payments', description: 'Wealth, Savings & Yogas' },
  { id: 'personality', label: 'Personality', icon: 'psychology', description: 'Mind, Traits & Strengths' },
  { id: 'spiritual', label: 'Spiritual Growth', icon: 'auto_awesome', description: 'Dharma, Meditation & Gita' },
]

export const TABS: TabConfig[] = ALL_TABS.filter((tab) => isTabEnabled(tab.id))

interface TabNavigationProps {
  activeTab: TabType
  onTabChange: (tab: TabType) => void
}

export default function TabNavigation({ activeTab, onTabChange }: TabNavigationProps) {
  const visibleTabs = TABS

  return (
    <div className="bg-surface border-b border-outline-variant/60 sticky top-[72px] z-40 shadow-xs">
      <div className="max-w-[1200px] mx-auto px-4">
        <div className="flex items-center gap-1 overflow-x-auto custom-scrollbar py-2 no-scrollbar">
          {visibleTabs.map((tab) => {
            const isActive = activeTab === tab.id
            return (
              <button
                key={tab.id}
                onClick={() => onTabChange(tab.id)}
                className={`flex items-center gap-2 px-4 py-2.5 rounded-2xl whitespace-nowrap transition-all text-sm font-medium cursor-pointer shrink-0 ${
                  isActive
                    ? 'bg-primary text-white shadow-md shadow-primary/20 scale-[1.02]'
                    : 'text-on-surface-variant hover:text-primary hover:bg-surface-variant/40'
                }`}
              >
                <span
                  className={`material-symbols-outlined text-lg ${isActive ? 'text-white' : 'text-primary'}`}
                  style={{ fontVariationSettings: isActive ? "'FILL' 1" : "'FILL' 0" }}
                >
                  {tab.icon}
                </span>
                <span>{tab.label}</span>
              </button>
            )
          })}
        </div>
      </div>
    </div>
  )
}

