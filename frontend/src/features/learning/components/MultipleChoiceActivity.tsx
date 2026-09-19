import React from 'react'
import { MultipleChoiceContent } from '@/types'
import { CheckCircle2, Circle } from 'lucide-react'

interface MultipleChoiceActivityProps {
  content: MultipleChoiceContent
  selectedOptionId: string | null
  onSelect: (optionId: string) => void
  disabled?: boolean
}

export const MultipleChoiceActivity: React.FC<MultipleChoiceActivityProps> = ({
  content,
  selectedOptionId,
  onSelect,
  disabled = false,
}) => {
  return (
    <div className="space-y-6 w-full max-w-2xl mx-auto">
      {/* Question Prompt */}
      <div className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm border border-slate-200 dark:border-slate-700 rounded-2xl p-6 shadow-sm">
        <h2 className="text-xl sm:text-2xl font-semibold text-slate-900 dark:text-white text-center leading-relaxed">
          {content.question}
        </h2>
      </div>

      {/* Selectable Options */}
      <div
        role="radiogroup"
        aria-label={content.question}
        className="grid grid-cols-1 sm:grid-cols-2 gap-4"
      >
        {content.options.map((option) => {
          const isSelected = selectedOptionId === option.id
          return (
            <button
              key={option.id}
              type="button"
              role="radio"
              aria-checked={isSelected}
              disabled={disabled}
              onClick={() => onSelect(option.id)}
              className={`group flex items-center gap-4 p-5 rounded-2xl border-2 text-left transition-all duration-200 min-h-[4rem] sm:min-h-[4.5rem] focus:outline-none focus:ring-4 focus:ring-indigo-400/50 ${
                isSelected
                  ? 'border-indigo-600 bg-indigo-50/80 dark:bg-indigo-950/40 dark:border-indigo-400 shadow-md scale-[1.01]'
                  : 'border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:border-slate-300 dark:hover:border-slate-600 hover:bg-slate-50 dark:hover:bg-slate-750 shadow-sm'
              } ${disabled ? 'opacity-60 cursor-not-allowed' : 'cursor-pointer active:scale-[0.99]'}`}
            >
              <div className="shrink-0">
                {isSelected ? (
                  <CheckCircle2 className="w-7 h-7 text-indigo-600 dark:text-indigo-400" />
                ) : (
                  <Circle className="w-7 h-7 text-slate-300 dark:text-slate-600 group-hover:text-slate-400" />
                )}
              </div>

              <div className="flex-1 flex items-center justify-between gap-2">
                <span className="text-lg sm:text-xl font-medium text-slate-800 dark:text-slate-100">
                  {option.text}
                </span>

                {option.visual_cue && (
                  <span className="text-2xl ml-2 select-none" aria-hidden="true">
                    {option.visual_cue}
                  </span>
                )}
              </div>
            </button>
          )
        })}
      </div>
    </div>
  )
}
