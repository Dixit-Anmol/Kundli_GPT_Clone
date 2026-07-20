/**
 * Feature Flags Configuration
 * Controls feature availability and tab visibility across Kundli GPT.
 */

export interface FeatureFlags {
  enableOverviewTab: boolean
  enableCareerTab: boolean
  enableMarriageTab: boolean
  enableHealthTab: boolean
  enableFoodTab: boolean
  enableRemediesTab: boolean
  enableFinanceTab: boolean
  enablePersonalityTab: boolean
  enableSpiritualTab: boolean
}

export const FEATURE_FLAGS: FeatureFlags = {
  enableOverviewTab: true,
  enableCareerTab: true,
  enableMarriageTab: true,
  enableHealthTab: true,
  enableFoodTab: true,
  enableRemediesTab: true,    // ✅ Enabled Remedies tab
  enableFinanceTab: true,
  enablePersonalityTab: true, // ✅ Enabled Personality tab with The Four Temperaments
  enableSpiritualTab: false,   // ❌ Disabled via feature flag per request
}


/** Check if a specific tab ID is enabled by feature flags */
export function isTabEnabled(tabId: string): boolean {
  switch (tabId) {
    case 'overview':
      return FEATURE_FLAGS.enableOverviewTab
    case 'career':
      return FEATURE_FLAGS.enableCareerTab
    case 'marriage':
      return FEATURE_FLAGS.enableMarriageTab
    case 'health':
      return FEATURE_FLAGS.enableHealthTab
    case 'food':
      return FEATURE_FLAGS.enableFoodTab
    case 'remedies':
      return FEATURE_FLAGS.enableRemediesTab
    case 'finance':
      return FEATURE_FLAGS.enableFinanceTab
    case 'personality':
      return FEATURE_FLAGS.enablePersonalityTab
    case 'spiritual':
      return FEATURE_FLAGS.enableSpiritualTab
    default:
      return true
  }
}
