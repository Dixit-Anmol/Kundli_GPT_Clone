/**
 * PricingPage — Beautiful 3-tier subscription pricing page for AstroSutra AI.
 */
import { useState } from 'react'
import { TIER_CONFIG, type SubscriptionTier } from '../config/subscriptionConfig'
import { getCurrentTier, setCurrentTier } from '../utils/subscriptionManager'

interface PricingPageProps {
  onNavigateBack: () => void
}

export default function PricingPage({ onNavigateBack }: PricingPageProps) {
  const [activeTier, setActiveTier] = useState<SubscriptionTier>(getCurrentTier())

  const handleSelectTier = (tier: SubscriptionTier) => {
    setCurrentTier(tier)
    setActiveTier(tier)
  }

  const tiers = Object.values(TIER_CONFIG)

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <nav className="glass border-b border-outline-variant/50 h-[72px] sticky top-0 z-50 flex items-center justify-between px-4 md:px-10">
        <button
          onClick={onNavigateBack}
          className="flex items-center gap-2 text-on-surface-variant hover:text-primary transition-colors cursor-pointer"
        >
          <span className="material-symbols-outlined text-xl">arrow_back</span>
          <span className="text-sm font-medium">Back to Dashboard</span>
        </button>
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center text-on-primary shadow-xs">
            <span className="material-symbols-outlined text-2xl" style={{ fontVariationSettings: "'FILL' 1" }}>
              auto_awesome
            </span>
          </div>
          <h1 className="font-display text-[28px] leading-tight font-semibold text-primary">
            AstroSutra AI
          </h1>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="max-w-5xl mx-auto px-4 pt-12 pb-6 text-center">
        <div className="inline-flex items-center gap-2 bg-primary-fixed text-primary px-4 py-1.5 rounded-full text-xs font-bold mb-5 border border-primary/20">
          <span className="material-symbols-outlined text-sm" style={{ fontVariationSettings: "'FILL' 1" }}>
            workspace_premium
          </span>
          Choose Your Cosmic Plan
        </div>
        <h2 className="font-display text-4xl md:text-5xl font-bold text-on-background mb-4 leading-tight">
          Unlock Your Full<br />
          <span className="text-primary">Astrological Potential</span>
        </h2>
        <p className="text-on-surface-variant text-base md:text-lg max-w-2xl mx-auto leading-relaxed">
          From basic chart insights to deep D2 Hora wealth analysis, Prashna Kundli, and unlimited AI guidance — choose the plan that matches your spiritual journey.
        </p>
      </div>

      {/* Pricing Cards */}
      <div className="max-w-5xl mx-auto px-4 pb-16">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-stretch">
          {tiers.map((tier) => {
            const isCurrent = activeTier === tier.id
            const isHighlighted = tier.highlighted

            return (
              <div
                key={tier.id}
                className={`relative rounded-3xl p-[2px] transition-all duration-300 ${
                  isHighlighted
                    ? 'scale-[1.03] md:scale-105 z-10'
                    : 'hover:scale-[1.01]'
                }`}
                style={{
                  background: isHighlighted
                    ? `linear-gradient(135deg, ${tier.color}, ${tier.color}80, ${tier.color})`
                    : tier.borderColor,
                }}
              >
                {/* Most Popular Badge */}
                {isHighlighted && (
                  <div
                    className="absolute -top-4 left-1/2 -translate-x-1/2 px-5 py-1.5 rounded-full text-white text-xs font-bold shadow-lg z-20 whitespace-nowrap"
                    style={{ backgroundColor: tier.color }}
                  >
                    ✨ Most Popular
                  </div>
                )}

                <div
                  className="h-full rounded-[22px] p-6 md:p-7 flex flex-col"
                  style={{ background: tier.bgGradient }}
                >
                  {/* Tier Icon & Label */}
                  <div className="flex items-center gap-3 mb-4">
                    <div
                      className="w-11 h-11 rounded-xl flex items-center justify-center shadow-sm"
                      style={{
                        background: `${tier.color}15`,
                        border: `1.5px solid ${tier.color}30`,
                      }}
                    >
                      <span
                        className="material-symbols-outlined text-2xl"
                        style={{ color: tier.color, fontVariationSettings: "'FILL' 1" }}
                      >
                        {tier.icon}
                      </span>
                    </div>
                    <div>
                      <h3 className="font-display text-xl font-bold text-on-background">
                        {tier.label}
                      </h3>
                      {isCurrent && (
                        <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full text-white" style={{ backgroundColor: tier.color }}>
                          Current Plan
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Price */}
                  <div className="mb-5">
                    <span className="font-display text-4xl font-bold text-on-background">
                      {tier.price}
                    </span>
                    <span className="text-sm text-on-surface-variant ml-1">
                      {tier.priceSubtext}
                    </span>
                  </div>

                  {/* Features List */}
                  <ul className="space-y-2.5 mb-7 flex-1">
                    {tier.features.map((feature, i) => {
                      const isHeader = feature.includes('plus:')
                      return (
                        <li key={i} className={`flex items-start gap-2.5 text-sm ${isHeader ? 'font-semibold text-on-surface-variant pt-1' : 'text-on-surface'}`}>
                          {!isHeader && (
                            <span
                              className="material-symbols-outlined text-base mt-0.5 shrink-0"
                              style={{ color: tier.color, fontVariationSettings: "'FILL' 1" }}
                            >
                              check_circle
                            </span>
                          )}
                          <span>{feature}</span>
                        </li>
                      )
                    })}
                  </ul>

                  {/* CTA Button */}
                  {isCurrent ? (
                    <div
                      className="w-full py-3 px-6 rounded-2xl text-center text-sm font-bold border-2"
                      style={{
                        borderColor: tier.color + '40',
                        color: tier.color,
                        backgroundColor: tier.color + '10',
                      }}
                    >
                      <span className="flex items-center justify-center gap-2">
                        <span className="material-symbols-outlined text-lg" style={{ fontVariationSettings: "'FILL' 1" }}>
                          check_circle
                        </span>
                        Active Plan
                      </span>
                    </div>
                  ) : (
                    <button
                      onClick={() => handleSelectTier(tier.id)}
                      className="w-full py-3 px-6 rounded-2xl text-white font-bold text-sm shadow-lg hover:shadow-xl transition-all hover:scale-[1.02] active:scale-[0.98] cursor-pointer"
                      style={{
                        background: `linear-gradient(135deg, ${tier.color}, ${tier.color}CC)`,
                      }}
                    >
                      {tier.id === 'free' ? 'Downgrade to Free' : `Upgrade to ${tier.label}`}
                    </button>
                  )}
                </div>
              </div>
            )
          })}
        </div>

        {/* Footer Note */}
        <div className="text-center mt-10">
          <p className="text-xs text-on-surface-variant leading-relaxed max-w-lg mx-auto">
            🔒 Secure payments powered by Razorpay · Cancel anytime · All plans include core birth chart computation
          </p>
        </div>
      </div>
    </div>
  )
}
