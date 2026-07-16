interface SuggestionChipsProps {
  suggestions: string[]
  onSelect: (suggestion: string) => void
}

const defaultSuggestions = [
  'Explain my birth chart',
  'Career Guidance',
  'Marriage Compatibility',
  'Gemstone Recommendation',
  'Health Forecast',
]

export default function SuggestionChips({
  suggestions = defaultSuggestions,
  onSelect,
}: SuggestionChipsProps) {
  return (
    <div className="ml-12 overflow-x-auto flex gap-3 py-4 custom-scrollbar scroll-smooth animate-fade-in-up delay-700">
      {suggestions.map((text, i) => (
        <button
          key={i}
          onClick={() => onSelect(text)}
          className="whitespace-nowrap px-6 py-2.5 bg-secondary-container text-on-secondary-container rounded-full text-[14px] leading-5 tracking-wide font-medium hover:bg-primary-fixed hover:text-primary transition-all border border-outline-variant/60"
        >
          {text}
        </button>
      ))}
    </div>
  )
}
