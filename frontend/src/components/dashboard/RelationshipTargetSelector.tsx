import { isRelationshipTargetAllowed } from '../../config/subscriptionConfig'
import { getCurrentTier } from '../../utils/subscriptionManager'

export type RelationshipTarget =
  | 'spouse'
  | 'father'
  | 'mother'
  | 'siblings'
  | 'children'
  | 'friends'
  | 'boss'
  | 'mentors'
  | 'inlaws'

export interface RelationshipTargetConfig {
  id: RelationshipTarget
  label: string
  icon: string
  hindiLabel: string
}

export const RELATIONSHIP_TARGETS: RelationshipTargetConfig[] = [
  { id: 'spouse', label: 'Spouse / Partner', icon: 'favorite', hindiLabel: 'Kalatra' },
  { id: 'father', label: 'Father', icon: 'person', hindiLabel: 'Pitr' },
  { id: 'mother', label: 'Mother', icon: 'face_3', hindiLabel: 'Matr' },
  { id: 'siblings', label: 'Siblings', icon: 'groups', hindiLabel: 'Bhratr' },
  { id: 'children', label: 'Children', icon: 'child_care', hindiLabel: 'Santana' },
  { id: 'friends', label: 'Friends', icon: 'handshake', hindiLabel: 'Maitri' },
  { id: 'boss', label: 'Boss & Authorities', icon: 'badge', hindiLabel: 'Adhikari' },
  { id: 'mentors', label: 'Mentors & Teachers', icon: 'school', hindiLabel: 'Guru' },
  { id: 'inlaws', label: 'In-Laws', icon: 'home', hindiLabel: 'Kutumba' },
]

interface RelationshipTargetSelectorProps {
  selectedTarget: RelationshipTarget
  onSelectTarget: (target: RelationshipTarget) => void
}

export default function RelationshipTargetSelector({
  selectedTarget,
  onSelectTarget,
}: RelationshipTargetSelectorProps) {
  const currentTier = getCurrentTier()

  return (
    <div className="bg-surface p-4 rounded-3xl border border-outline-variant/60 shadow-xs mb-6 animate-fade-in-up">
      <div className="flex items-center justify-between mb-3 px-1">
        <div className="flex items-center gap-2">
          <span className="material-symbols-outlined text-primary text-xl">diversity_3</span>
          <h4 className="font-display text-lg font-bold text-primary">
            Select Relationship Focus Area
          </h4>
        </div>
        <span className="text-[11px] font-semibold text-on-surface-variant bg-surface-variant/50 px-2.5 py-0.5 rounded-full">
          9 Vedic Relational Engines
        </span>
      </div>

      <div className="flex items-center gap-2 overflow-x-auto custom-scrollbar pb-1 no-scrollbar">
        {RELATIONSHIP_TARGETS.map((target) => {
          const isActive = selectedTarget === target.id
          const isAllowed = isRelationshipTargetAllowed(target.id, currentTier)

          return (
            <button
              key={target.id}
              onClick={() => onSelectTarget(target.id)}
              className={`flex items-center gap-2 px-3.5 py-2 rounded-2xl whitespace-nowrap transition-all text-xs font-semibold cursor-pointer shrink-0 border ${
                isActive
                  ? 'bg-primary text-white border-primary shadow-md shadow-primary/20 scale-[1.02]'
                  : !isAllowed
                  ? 'bg-surface-variant/30 text-on-surface-variant/70 border-outline-variant/40 hover:bg-surface-variant/60'
                  : 'bg-surface text-on-surface-variant border-outline-variant/60 hover:border-primary/40 hover:text-primary hover:bg-surface-variant/30'
              }`}
            >
              <span className="material-symbols-outlined text-base">
                {target.icon}
              </span>
              <span>{target.label}</span>
              <span className={`text-[10px] opacity-80 font-normal ${isActive ? 'text-white/90' : 'text-primary'}`}>
                ({target.hindiLabel})
              </span>

              {/* Pro Lock Badge for Pro-only targets */}
              {!isAllowed && (
                <span className="material-symbols-outlined text-xs text-amber-600" style={{ fontVariationSettings: "'FILL' 1" }}>
                  lock
                </span>
              )}
            </button>
          )
        })}
      </div>
    </div>
  )
}
