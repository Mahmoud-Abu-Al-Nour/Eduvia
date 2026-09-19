import React from 'react'
import { ActivityEvaluationResponse } from '@/types'
import { Sparkles, Star, Award, RotateCcw, ArrowRight, X } from 'lucide-react'

interface CognitiveCalmFeedbackProps {
  result: ActivityEvaluationResponse
  onTryAgain: () => void
  onNext?: () => void
  onClose: () => void
}

export const CognitiveCalmFeedback: React.FC<CognitiveCalmFeedbackProps> = ({
  result,
  onTryAgain,
  onNext,
  onClose,
}) => {
  const isPerfect = result.is_correct || result.score >= 1.0
  const isPartial = !isPerfect && result.score > 0.0

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="feedback-title"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-xs transition-opacity animate-in fade-in duration-200"
    >
      <div className="relative w-full max-w-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 sm:p-8 shadow-2xl overflow-hidden">
        {/* Close Button */}
        <button
          type="button"
          onClick={onClose}
          aria-label="Close feedback"
          className="absolute top-5 right-5 p-2 rounded-full text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Cognitive Calm Visual Header */}
        <div className="text-center space-y-3">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl shadow-inner mx-auto transition-transform scale-110">
            {isPerfect ? (
              <div className="w-16 h-16 rounded-2xl bg-emerald-100 dark:bg-emerald-950 flex items-center justify-center text-emerald-600 dark:text-emerald-400">
                <Star className="w-9 h-9 fill-emerald-500 stroke-emerald-600" />
              </div>
            ) : isPartial ? (
              <div className="w-16 h-16 rounded-2xl bg-amber-100 dark:bg-amber-950 flex items-center justify-center text-amber-600 dark:text-amber-400">
                <Sparkles className="w-9 h-9 text-amber-500" />
              </div>
            ) : (
              <div className="w-16 h-16 rounded-2xl bg-sky-100 dark:bg-sky-950 flex items-center justify-center text-sky-600 dark:text-sky-400">
                <Sparkles className="w-9 h-9 text-sky-500" />
              </div>
            )}
          </div>

          <h3
            id="feedback-title"
            className="text-2xl font-bold text-slate-900 dark:text-white"
          >
            {isPerfect
              ? 'Splendid Effort!'
              : isPartial
              ? 'Great Progress!'
              : 'Learning in Progress'}
          </h3>

          {/* Mastery Badge if confirmed */}
          {result.mastery_achieved && (
            <div className="inline-flex items-center gap-1.5 px-3.5 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-300 dark:border-emerald-700 text-xs font-semibold text-emerald-800 dark:text-emerald-300 shadow-xs">
              <Award className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
              <span>Objective Mastery Attained</span>
            </div>
          )}
        </div>

        {/* Feedback Message Body */}
        <div className="mt-6 p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-800 text-center">
          <p className="text-base sm:text-lg font-medium text-slate-800 dark:text-slate-200 leading-relaxed">
            {result.feedback}
          </p>

          {result.explanation && (
            <div className="mt-3 pt-3 border-t border-slate-200/60 dark:border-slate-700 text-sm text-slate-600 dark:text-slate-400 text-left">
              <span className="font-semibold text-slate-700 dark:text-slate-300 block mb-1">
                Pedagogical Note:
              </span>
              {result.explanation}
            </div>
          )}
        </div>

        {/* Action Controls */}
        <div className="mt-8 flex flex-col sm:flex-row items-center gap-3">
          <button
            type="button"
            onClick={onTryAgain}
            className="w-full sm:flex-1 flex items-center justify-center gap-2 px-5 py-3.5 rounded-2xl border-2 border-slate-200 dark:border-slate-700 font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors focus:outline-none focus:ring-4 focus:ring-slate-300"
          >
            <RotateCcw className="w-5 h-5" />
            <span>Try Again</span>
          </button>

          {onNext && (
            <button
              type="button"
              onClick={onNext}
              className="w-full sm:flex-1 flex items-center justify-center gap-2 px-5 py-3.5 rounded-2xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold shadow-md transition-colors focus:outline-none focus:ring-4 focus:ring-indigo-300"
            >
              <span>Continue</span>
              <ArrowRight className="w-5 h-5" />
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
