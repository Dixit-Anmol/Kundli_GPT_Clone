import { useState } from 'react'

interface PrashnaQuestionSelectorProps {
  onSelectQuestion: (question: string, category: string) => void
}

export const PRASHNA_CATEGORIES = [
  { id: 'career', label: '💼 Career & Job', icon: 'work' },
  { id: 'marriage', label: '💍 Marriage & Love', icon: 'favorite' },
  { id: 'business', label: '📈 Business Venture', icon: 'trending_up' },
  { id: 'health', label: '🌿 Health & Energy', icon: 'healing' },
  { id: 'relationships', label: '❤️ Relationships', icon: 'diversity_3' },
  { id: 'finance', label: '💰 Wealth & Finance', icon: 'payments' },
  { id: 'spirituality', label: '🧘 Spiritual Path', icon: 'self_improvement' },
  { id: 'travel', label: '✈️ Foreign Travel', icon: 'flight' },
  { id: 'education', label: '🎓 Education & Exams', icon: 'school' },
]

export const SAMPLE_QUESTIONS: Record<string, string[]> = {
  career: ['Will I get this job promotion?', 'Is this the right time for a job transition?', 'Will my career performance improve this year?'],
  marriage: ['Will my relationship improve?', 'When is the most favorable timing for my marriage?', 'Is this romantic partner right for me?'],
  business: ['Should I launch this business venture now?', 'Will my new enterprise be profitable?', 'Is this business partnership favorable?'],
  health: ['How will my health & vitality be in the coming months?', 'When will my current health issue resolve?'],
  relationships: ['Will my relationship bond heal?', 'How can I harmonize my family dynamic?'],
  finance: ['Should I make this financial investment now?', 'How is my upcoming financial stability?'],
  spirituality: ['What is my core spiritual path right now?', 'How can I deepen my daily meditation practice?'],
  travel: ['Should I relocate or move abroad?', 'Will my visa & foreign travel plans succeed?'],
  education: ['Will I clear my competitive exams?', 'Is this university or course suitable for me?'],
}

export default function PrashnaQuestionSelector({ onSelectQuestion }: PrashnaQuestionSelectorProps) {
  const [selectedCat, setSelectedCat] = useState<string>('career')
  const [customQuestion, setCustomQuestion] = useState<string>('')

  const handleSelectSample = (q: string) => {
    onSelectQuestion(q, selectedCat)
  }

  const handleSubmitCustom = () => {
    if (customQuestion.trim()) {
      onSelectQuestion(customQuestion.trim(), selectedCat)
    }
  }

  return (
    <div className="space-y-6 animate-fade-in-up">
      {/* Category Pills */}
      <div className="space-y-2">
        <label className="text-xs sm:text-sm font-bold text-primary block">
          Select Your Guidance Topic:
        </label>
        <div className="flex flex-wrap gap-2.5">
          {PRASHNA_CATEGORIES.map((cat) => (
            <button
              key={cat.id}
              type="button"
              onClick={() => setSelectedCat(cat.id)}
              className={`px-4 py-2.5 rounded-2xl text-xs sm:text-sm font-bold transition-all cursor-pointer flex items-center gap-1.5 ${
                selectedCat === cat.id
                  ? 'bg-primary text-white shadow-md scale-[1.02]'
                  : 'bg-surface border border-outline-variant/60 text-on-surface-variant hover:bg-surface-variant/60 hover:text-primary'
              }`}
            >
              <span>{cat.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Sample Horary Questions */}
      <div className="space-y-3">
        <label className="text-xs sm:text-sm font-bold text-primary block">
          Click a Horary Prashna Question Below:
        </label>
        <div className="grid grid-cols-1 gap-2.5">
          {(SAMPLE_QUESTIONS[selectedCat] || SAMPLE_QUESTIONS['career']).map((q, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleSelectSample(q)}
              className="text-left bg-surface hover:bg-primary-fixed/80 border border-outline-variant/60 p-4 rounded-2xl text-xs sm:text-sm font-semibold text-primary transition-all cursor-pointer flex items-center justify-between group shadow-xs"
            >
              <span>"{q}"</span>
              <span className="material-symbols-outlined text-base text-primary group-hover:translate-x-1 transition-transform">
                arrow_forward
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Custom Question Input */}
      <div className="space-y-2 pt-3 border-t border-outline-variant/40">
        <label className="text-xs sm:text-sm font-bold text-primary block">
          Or Type Your Own Custom Question:
        </label>
        <div className="flex flex-wrap sm:flex-nowrap gap-3">
          <input
            type="text"
            value={customQuestion}
            onChange={(e) => setCustomQuestion(e.target.value)}
            placeholder="e.g. Will my visa approval come through this month?"
            className="flex-1 bg-surface border border-outline-variant/60 rounded-2xl px-4 py-3.5 text-xs sm:text-sm text-primary focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary font-medium"
          />
          <button
            type="button"
            onClick={handleSubmitCustom}
            disabled={!customQuestion.trim()}
            className="w-full sm:w-auto bg-primary text-white px-6 py-3.5 rounded-2xl text-xs sm:text-sm font-bold shadow-md shadow-primary/25 disabled:opacity-50 cursor-pointer flex items-center justify-center gap-1.5"
          >
            <span>Ask Prashna</span>
            <span className="material-symbols-outlined text-base">auto_awesome</span>
          </button>
        </div>
      </div>
    </div>
  )
}
