interface LoadingStep {
  label: string
  status: 'done' | 'active' | 'waiting'
  progress?: number
}

interface ComputingCardProps {
  steps: LoadingStep[]
}

const defaultSteps: LoadingStep[] = [
  { label: 'Finding Planetary Positions', status: 'done' },
  { label: 'Calculating Houses', status: 'active', progress: 82 },
  { label: 'Computing Nakshatras', status: 'waiting' },
]

export default function ComputingCard({ steps = defaultSteps }: ComputingCardProps) {
  return (
    <div className="ml-12 celestial-card rounded-2xl p-6 flex flex-col gap-4 animate-fade-in-up">
      {/* Header */}
      <div className="flex items-center gap-4 text-on-surface-variant text-[14px] leading-5 tracking-wide font-medium">
        <div className="w-5 h-5 border-2 border-primary border-t-transparent rounded-full animate-spin" />
        <span>✨ Computing Celestial Alignment...</span>
      </div>

      {/* Steps */}
      <div className="space-y-3">
        {steps.map((step, i) => (
          <div key={i}>
            <div
              className={`flex items-center justify-between text-[12px] leading-4 font-semibold ${
                step.status === 'done'
                  ? 'opacity-60'
                  : step.status === 'active'
                  ? 'text-primary'
                  : 'opacity-40'
              }`}
            >
              <div className="flex items-center gap-2">
                <span
                  className={`material-symbols-outlined text-[16px] ${
                    step.status === 'done'
                      ? 'text-primary'
                      : step.status === 'active'
                      ? 'animate-pulse'
                      : ''
                  }`}
                >
                  {step.status === 'done' ? 'check_circle' : step.status === 'active' ? 'sync' : 'pending'}
                </span>
                {step.label}
              </div>
              <span className={step.status === 'active' ? 'text-primary' : ''}>
                {step.status === 'done' ? 'Done' : step.status === 'active' ? `${step.progress}%` : 'Waiting'}
              </span>
            </div>

            {/* Progress Bar (only for active step) */}
            {step.status === 'active' && step.progress !== undefined && (
              <div className="w-full h-1 bg-surface-variant rounded-full overflow-hidden mt-2">
                <div
                  className="h-full bg-primary rounded-full transition-all duration-500"
                  style={{ width: `${step.progress}%` }}
                />
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
