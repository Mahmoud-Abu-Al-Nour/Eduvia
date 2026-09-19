import React from 'react'
import { VisualIdentificationContent } from '@/types'
import { Eye, CheckCircle2, Circle } from 'lucide-react'

interface VisualIdentificationActivityProps {
  content: VisualIdentificationContent
  selectedElementId: string | null
  onSelect: (elementId: string) => void
  disabled?: boolean
}

export const VisualIdentificationActivity: React.FC<VisualIdentificationActivityProps> = ({
  content,
  selectedElementId,
  onSelect,
  disabled = false,
}) => {
  return (
    <div className="space-y-6 w-full max-w-3xl mx-auto">
      {/* Prompt & Scene Description */}
      <div className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm border border-slate-200 dark:border-slate-700 rounded-2xl p-6 shadow-sm text-center">
        <h2 className="text-xl sm:text-2xl font-semibold text-slate-900 dark:text-white leading-relaxed">
          {content.prompt}
        </h2>
        <div className="mt-3 p-4 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 flex items-start gap-3 text-left">
          <Eye className="w-5 h-5 text-indigo-500 shrink-0 mt-0.5" />
          <div>
            <div className="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-1">
              Scene Description
            </div>
            <p className="text-sm sm:text-base text-slate-700 dark:text-slate-300 leading-relaxed">
              {content.scene_description}
            </p>
          </div>
        </div>
      </div>

      {/* Selectable Scene Elements Grid */}
      <div>
        <div className="text-xs font-semibold uppercase tracking-wider text-slate-500 text-center mb-3">
          Select the Target Object
        </div>
        <div
          role="radiogroup"
          aria-label={content.prompt}
          className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4"
        >
          {content.elements.map((element) => {
            const isSelected = selectedElementId === element.id

            return (
              <button
                key={element.id}
                type="button"
                role="radio"
                aria-checked={isSelected}
                disabled={disabled}
                onClick={() => onSelect(element.id)}
                className={`flex flex-col justify-between p-5 rounded-2xl border-2 text-left transition-all min-h-[5.5rem] focus:outline-none focus:ring-4 focus:ring-indigo-400/50 ${
                  isSelected
                    ? 'border-indigo-600 bg-indigo-50/80 dark:bg-indigo-950/40 dark:border-indigo-400 shadow-md scale-[1.02]'
                    : 'border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:border-slate-300 dark:hover:border-slate-600 shadow-sm'
                } ${disabled ? 'opacity-60 cursor-not-allowed' : 'cursor-pointer active:scale-[0.99]'}`}
              >
                <div className="flex items-start justify-between gap-2 w-full">
                  <span className="text-lg font-semibold text-slate-800 dark:text-slate-100">
                    {element.label}
                  </span>
                  <div className="shrink-0 mt-0.5">
                    {isSelected ? (
                      <CheckCircle2 className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
                    ) : (
                      <Circle className="w-6 h-6 text-slate-300 dark:text-slate-600" />
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-2 mt-3 pt-2 border-t border-slate-100 dark:border-slate-700/60 text-xs text-slate-500 dark:text-slate-400">
                  <span className="capitalize">{element.category || 'Object'}</span>
                  {element.bounding_hint && (
                    <>
                      <span>•</span>
                      <span>{element.bounding_hint}</span>
                    </>
                  )}
                </div>
              </button>
            )
          })}
        </div>
      </div>
    </div>
  )
}
