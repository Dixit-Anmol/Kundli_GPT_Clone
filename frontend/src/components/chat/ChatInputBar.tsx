interface ChatInputBarProps {
  value: string
  onChange: (value: string) => void
  onSend: () => void
}

export default function ChatInputBar({ value, onChange, onSend }: ChatInputBarProps) {
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && value.trim()) {
      onSend()
    }
  }

  return (
    <div className="fixed bottom-0 left-0 right-0 p-4 md:pb-6 pointer-events-none z-50">
      <div className="max-w-[800px] mx-auto pointer-events-auto">
        <div className="glass celestial-card rounded-full p-2 flex items-center gap-2 shadow-xl ring-1 ring-primary/10">
          {/* Attach Button */}
          <button className="w-10 h-10 flex items-center justify-center rounded-full text-on-surface-variant hover:bg-primary-fixed hover:text-primary transition-colors">
            <span className="material-symbols-outlined">add</span>
          </button>

          {/* Input */}
          <input
            type="text"
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onKeyDown={handleKeyDown}
            className="flex-1 bg-transparent border-none focus:ring-0 px-2 text-[16px] leading-6 text-on-surface placeholder:text-on-surface-variant/50 outline-none"
            placeholder="Ask anything about your horoscope..."
          />

          {/* Action Buttons */}
          <div className="flex items-center gap-1">
            <button className="w-10 h-10 flex items-center justify-center rounded-full text-on-surface-variant hover:bg-primary-fixed hover:text-primary transition-colors">
              <span className="material-symbols-outlined">mic</span>
            </button>
            <button
              onClick={onSend}
              className="w-11 h-11 bg-gradient-to-tr from-primary to-primary-container text-on-primary rounded-full flex items-center justify-center shadow-lg shadow-primary/30 hover:scale-105 active:scale-95 transition-all"
            >
              <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>
                arrow_upward
              </span>
            </button>
          </div>
        </div>

        {/* Footer Text */}
        <div className="text-center mt-3">
          <p className="text-[12px] leading-4 font-semibold text-on-surface-variant/60">
            Powered by Ancient Vedic Algorithms & GPT-4o
          </p>
        </div>
      </div>
    </div>
  )
}
