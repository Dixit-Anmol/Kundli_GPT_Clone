import React, { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import AssistantMessage from '../chat/AssistantMessage'
import SuggestionChips from '../chat/SuggestionChips'
import type { TabType } from './TabNavigation'

export interface Message {
  role: 'user' | 'assistant'
  content: string
}

interface TabChatProps {
  tab: TabType
  sessionId: string
  userId?: string
  messages: Message[]
  onSendMessage: (text: string) => void
  loading: boolean
}

const TAB_SUGGESTIONS: Record<TabType, string[]> = {
  overview: [
    'Explain my ascendant and moon sign',
    'What are my strongest planets?',
    'Explain active yogas in my chart',
    'Current Dasha period overview',
  ],
  career: [
    'Best career fields for me',
    'Should I do business or job?',
    'Favorable period for job change',
    'Government job chances',
  ],
  marriage: [
    'When will I get married?',
    'How will my spouse be?',
    'Love or arranged marriage?',
    'Is my Manglik dosha harmful?',
  ],
  health: [
    'What are my physical weak points?',
    'Mental stress management tips',
    'Immunity & disease tendencies',
    'Vulnerable age periods',
  ],
  food: [
    'What foods should I avoid?',
    'Best daily eating routine',
    'Which spices balance my dosha?',
    'Fasting recommendations for me',
  ],
  remedies: [
    'Which gemstone should I wear?',
    'Daily mantra for peace',
    'Charity for Saturn/Rahu',
    'Dosha reduction practices',
  ],
  finance: [
    'Will I accumulate wealth?',
    'Investment strategy for my chart',
    'Chances of sudden monetary gain',
    'Debt relief & savings advice',
  ],
  personality: [
    'My biggest hidden strength',
    'My blind spots & fear patterns',
    'How do people perceive me?',
    'My decision-making style',
  ],
  spiritual: [
    'What is my soul purpose?',
    'Best meditation style for me',
    'Karmic lessons in this life',
    'Bhagavad Gita guidance for me',
  ],
}

export default function TabChat({
  tab,
  messages,
  onSendMessage,
  loading,
}: TabChatProps) {
  const [input, setInput] = useState('')

  const handleSend = () => {
    if (!input.trim() || loading) return
    onSendMessage(input.trim())
    setInput('')
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const suggestions = TAB_SUGGESTIONS[tab] || TAB_SUGGESTIONS.overview

  return (
    <div className="mt-8 border-t border-outline-variant/40 pt-6">
      <h3 className="font-display text-2xl font-bold text-primary mb-4 flex items-center gap-2">
        <span className="material-symbols-outlined text-primary text-xl">forum</span>
        Ask {tab.charAt(0).toUpperCase() + tab.slice(1)} Guidance
      </h3>

      {/* Message History */}
      <div className="space-y-4 mb-6">
        {messages.map((msg, idx) =>
          msg.role === 'assistant' ? (
            <AssistantMessage key={idx} icon="auto_awesome">
              <div className="font-body text-sm leading-relaxed text-on-surface markdown-container">
                <ReactMarkdown>{msg.content}</ReactMarkdown>
              </div>
            </AssistantMessage>
          ) : (
            <div key={idx} className="flex justify-end animate-fade-in-up">
              <div className="max-w-[85%] bg-primary-fixed border border-primary/20 text-on-primary-fixed rounded-2xl rounded-tr-none px-4 py-3 text-sm leading-relaxed shadow-xs font-medium">
                {msg.content}
              </div>
            </div>
          )
        )}

        {loading && (
          <div className="flex gap-3 items-center pl-4 py-3 opacity-70">
            <div className="w-2 h-2 bg-primary rounded-full animate-bounce" />
            <div className="w-2 h-2 bg-primary rounded-full animate-bounce delay-100" />
            <div className="w-2 h-2 bg-primary rounded-full animate-bounce delay-200" />
            <span className="text-xs text-on-surface-variant italic ml-1">Consulting Jyotish charts...</span>
          </div>
        )}
      </div>

      {/* Suggestion Chips */}
      {!loading && (
        <div className="mb-4">
          <SuggestionChips suggestions={suggestions} onSelect={onSendMessage} />
        </div>
      )}

      {/* Input Bar */}
      <div className="flex items-center gap-2 bg-surface p-2 rounded-2xl border border-outline-variant shadow-xs focus-within:border-primary focus-within:ring-2 focus-within:ring-primary/20 transition-all">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={`Ask anything about your ${tab}...`}
          disabled={loading}
          className="flex-1 bg-transparent px-3 py-2 text-sm text-on-surface focus:outline-none placeholder:text-on-surface-variant/60"
        />
        <button
          onClick={handleSend}
          disabled={loading || !input.trim()}
          className="w-10 h-10 bg-primary text-white rounded-xl flex items-center justify-center hover:bg-primary-container disabled:opacity-40 transition-all cursor-pointer shrink-0"
        >
          <span className="material-symbols-outlined text-xl">send</span>
        </button>
      </div>
    </div>
  )
}
