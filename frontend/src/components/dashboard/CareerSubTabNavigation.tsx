export type CareerSubTab = 'overview' | 'kala_vidya'

interface CareerSubTabNavigationProps {
  activeSubTab: CareerSubTab
  onSubTabChange: (subTab: CareerSubTab) => void
}

export default function CareerSubTabNavigation({
  activeSubTab,
  onSubTabChange,
}: CareerSubTabNavigationProps) {
  return (
    <div className="flex flex-wrap items-center gap-2 bg-surface-variant/40 p-1.5 rounded-2xl border border-outline-variant/60 w-fit mb-6 animate-fade-in-up">
      <button
        onClick={() => onSubTabChange('overview')}
        className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
          activeSubTab === 'overview'
            ? 'bg-primary text-white shadow-md shadow-primary/20 scale-[1.02]'
            : 'text-on-surface-variant hover:text-primary hover:bg-surface-variant/60'
        }`}
      >
        <span className="material-symbols-outlined text-base">work</span>
        <span>Career Overview</span>
      </button>

      <button
        onClick={() => onSubTabChange('kala_vidya')}
        className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
          activeSubTab === 'kala_vidya'
            ? 'bg-primary text-white shadow-md shadow-primary/20 scale-[1.02]'
            : 'text-on-surface-variant hover:text-primary hover:bg-surface-variant/60'
        }`}
      >
        <span className="material-symbols-outlined text-base">school</span>
        <span>🎓 Kala, Vidya & Student Receptivity</span>
      </button>
    </div>
  )
}
