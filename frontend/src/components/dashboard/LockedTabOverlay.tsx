/**
 * LockedTabOverlay — Premium lock overlay shown when user tries to access a tab
 * that requires a higher subscription tier.
 */
import type { SubscriptionTier } from '../../config/subscriptionConfig'
import { TIER_CONFIG } from '../../config/subscriptionConfig'

interface LockedTabOverlayProps {
  requiredTier: SubscriptionTier
  tabLabel: string
  onUpgrade: () => void
}

export default function LockedTabOverlay({ requiredTier, tabLabel, onUpgrade }: LockedTabOverlayProps) {
  const tierInfo = TIER_CONFIG[requiredTier]

  return (
    <div className="flex items-center justify-center py-16">
      <div
        className="relative max-w-md w-full mx-4 rounded-3xl border-2 p-8 text-center overflow-hidden"
        style={{
          borderColor: tierInfo.borderColor + '60',
          background: tierInfo.bgGradient,
        }}
      >
        {/* Decorative glow */}
        <div
          className="absolute -top-20 -right-20 w-40 h-40 rounded-full blur-3xl opacity-20"
          style={{ backgroundColor: tierInfo.color }}
        />
        <div
          className="absolute -bottom-20 -left-20 w-40 h-40 rounded-full blur-3xl opacity-15"
          style={{ backgroundColor: tierInfo.color }}
        />

        {/* Lock Icon */}
        <div className="relative z-10">
          <div
            className="w-20 h-20 mx-auto rounded-2xl flex items-center justify-center mb-5 shadow-lg"
            style={{
              background: `linear-gradient(135deg, ${tierInfo.color}20, ${tierInfo.color}40)`,
              border: `2px solid ${tierInfo.color}30`,
            }}
          >
            <span
              className="material-symbols-outlined text-4xl"
              style={{ color: tierInfo.color, fontVariationSettings: "'FILL' 1" }}
            >
              lock
            </span>
          </div>

          {/* Title */}
          <h3 className="font-display text-2xl font-bold text-on-background mb-2">
            {tabLabel} is a {tierInfo.label} Feature
          </h3>
          <p className="text-sm text-on-surface-variant mb-6 leading-relaxed">
            Upgrade to <strong style={{ color: tierInfo.color }}>{tierInfo.label}</strong> ({tierInfo.price}{tierInfo.priceSubtext}) to unlock {tabLabel} and more premium features.
          </p>

          {/* Feature preview */}
          <div className="bg-surface/60 backdrop-blur-sm rounded-2xl p-4 mb-6 border border-outline-variant/40 text-left">
            <p className="text-xs font-bold uppercase tracking-wider text-on-surface-variant mb-3">
              What you'll unlock
            </p>
            <ul className="space-y-2">
              {tierInfo.features.slice(0, 5).map((feature, i) => (
                <li key={i} className="flex items-center gap-2 text-sm text-on-surface">
                  <span
                    className="material-symbols-outlined text-base"
                    style={{ color: tierInfo.color, fontVariationSettings: "'FILL' 1" }}
                  >
                    check_circle
                  </span>
                  {feature}
                </li>
              ))}
            </ul>
          </div>

          {/* CTA Button */}
          <button
            onClick={onUpgrade}
            className="w-full py-3.5 px-6 rounded-2xl text-white font-bold text-sm shadow-lg hover:shadow-xl transition-all hover:scale-[1.02] active:scale-[0.98] cursor-pointer"
            style={{
              background: `linear-gradient(135deg, ${tierInfo.color}, ${tierInfo.color}CC)`,
            }}
          >
            <span className="flex items-center justify-center gap-2">
              <span className="material-symbols-outlined text-lg" style={{ fontVariationSettings: "'FILL' 1" }}>
                {tierInfo.icon}
              </span>
              Upgrade to {tierInfo.label}
            </span>
          </button>

          <p className="text-[11px] text-on-surface-variant mt-3">
            Cancel anytime · Instant access
          </p>
        </div>
      </div>
    </div>
  )
}
