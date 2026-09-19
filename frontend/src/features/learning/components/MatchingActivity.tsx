import React, { useState } from 'react'
import { MatchingContent, MatchingPair } from '@/types'
import { Link2, Unlink } from 'lucide-react'

interface MatchingActivityProps {
  content: MatchingContent
  pairs: MatchingPair[]
  onChange: (pairs: MatchingPair[]) => void
  disabled?: boolean
}

const PAIR_COLORS = [
  'border-emerald-500 bg-emerald-50 dark:bg-emerald-950/30 text-emerald-900 dark:text-emerald-200',
  'border-amber-500 bg-amber-50 dark:bg-amber-950/30 text-amber-900 dark:text-amber-200',
  'border-sky-500 bg-sky-50 dark:bg-sky-950/30 text-sky-900 dark:text-sky-200',
  'border-purple-500 bg-purple-50 dark:bg-purple-950/30 text-purple-900 dark:text-purple-200',
  'border-rose-500 bg-rose-50 dark:bg-rose-950/30 text-rose-900 dark:text-rose-200',
]

export const MatchingActivity: React.FC<MatchingActivityProps> = ({
  content,
  pairs,
  onChange,
  disabled = false,
}) => {
  const [selectedLeftId, setSelectedLeftId] = useState<string | null>(null)

  // Map of item ID -> pair index
  const pairColorMap = new Map<string, number>()
  pairs.forEach((pair, idx) => {
    pairColorMap.set(pair.left_id, idx % PAIR_COLORS.length)
    pairColorMap.set(pair.right_id, idx % PAIR_COLORS.length)
  })

  const handleLeftClick = (id: string) => {
    if (disabled) return
    setSelectedLeftId(selectedLeftId === id ? null : id)
  }

  const handleRightClick = (id: string) => {
    if (disabled) return
    if (!selectedLeftId) {
      // Find and remove if already paired
      const existingIndex = pairs.findIndex((p) => p.right_id === id)
      if (existingIndex !== -1) {
        const next = pairs.filter((_, i) => i !== existingIndex)
        onChange(next)
      }
      return
    }

    // Filter out any prior pairings for either this left item or right item
    const nextPairs = pairs.filter(
      (p) => p.left_id !== selectedLeftId && p.right_id !== id
    )
    nextPairs.push({ left_id: selectedLeftId, right_id: id })
    onChange(nextPairs)
    setSelectedLeftId(null)
  }

  const removePair = (pairIndex: number) => {
    if (disabled) return
    onChange(pairs.filter((_, i) => i !== pairIndex))
  }

  return (
    <div className="space-y-6 w-full max-w-3xl mx-auto">
      {/* Prompt Card */}
      <div className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm border border-slate-200 dark:border-slate-700 rounded-2xl p-6 shadow-sm text-center">
        <h2 className="text-xl sm:text-2xl font-semibold text-slate-900 dark:text-white leading-relaxed">
          {content.prompt}
        </h2>
        <p className="text-sm text-slate-500 dark:text-slate-400 mt-2">
          {selectedLeftId
            ? 'Now select a matching item on the right.'
            : 'Select an item on the left, then connect it to the right.'}
        </p>
      </div>

      {/* Matching Columns Grid */}
      <div className="grid grid-cols-2 gap-4 sm:gap-8 items-start">
        {/* Left Column */}
        <div className="space-y-3">
          <div className="text-xs font-semibold uppercase tracking-wider text-slate-500 text-center pb-1">
            Group A
          </div>
          {content.left_items.map((item) => {
            const isSelected = selectedLeftId === item.id
            const pairIdx = pairColorMap.get(item.id)
            const isPaired = pairIdx !== undefined
            const pairStyle = isPaired ? PAIR_COLORS[pairIdx] : ''

            return (
              <button
                key={item.id}
                type="button"
                disabled={disabled}
                onClick={() => handleLeftClick(item.id)}
                className={`w-full flex items-center justify-between p-4 rounded-2xl border-2 text-left transition-all min-h-[4rem] focus:outline-none focus:ring-4 focus:ring-indigo-400/50 ${
                  isSelected
                    ? 'border-indigo-600 ring-2 ring-indigo-500 bg-indigo-50 dark:bg-indigo-950/50 shadow-md scale-[1.02]'
                    : isPaired
                    ? `${pairStyle} shadow-sm`
                    : 'border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:border-slate-300 dark:hover:border-slate-600 shadow-sm'
                } ${disabled ? 'opacity-60 cursor-not-allowed' : 'cursor-pointer active:scale-[0.99]'}`}
              >
                <span className="text-base sm:text-lg font-medium text-slate-800 dark:text-slate-100">
                  {item.label}
                </span>
                <div className="flex items-center gap-2">
                  {item.visual_cue && <span className="text-xl">{item.visual_cue}</span>}
                  {isPaired && <Link2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />}
                </div>
              </button>
            )
          })}
        </div>

        {/* Right Column */}
        <div className="space-y-3">
          <div className="text-xs font-semibold uppercase tracking-wider text-slate-500 text-center pb-1">
            Group B
          </div>
          {content.right_items.map((item) => {
            const pairIdx = pairColorMap.get(item.id)
            const isPaired = pairIdx !== undefined
            const pairStyle = isPaired ? PAIR_COLORS[pairIdx] : ''

            return (
              <button
                key={item.id}
                type="button"
                disabled={disabled}
                onClick={() => handleRightClick(item.id)}
                className={`w-full flex items-center justify-between p-4 rounded-2xl border-2 text-left transition-all min-h-[4rem] focus:outline-none focus:ring-4 focus:ring-indigo-400/50 ${
                  isPaired
                    ? `${pairStyle} shadow-sm`
                    : selectedLeftId
                    ? 'border-indigo-300 dark:border-indigo-700 bg-indigo-50/40 hover:bg-indigo-50 dark:hover:bg-indigo-900/30'
                    : 'border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:border-slate-300 dark:hover:border-slate-600 shadow-sm'
                } ${disabled ? 'opacity-60 cursor-not-allowed' : 'cursor-pointer active:scale-[0.99]'}`}
              >
                <span className="text-base sm:text-lg font-medium text-slate-800 dark:text-slate-100">
                  {item.label}
                </span>
                <div className="flex items-center gap-2">
                  {item.visual_cue && <span className="text-xl">{item.visual_cue}</span>}
                  {isPaired && <Link2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />}
                </div>
              </button>
            )
          })}
        </div>
      </div>

      {/* Connected Pairs Summary */}
      {pairs.length > 0 && (
        <div className="bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-800 rounded-2xl p-4">
          <div className="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-3">
            Connected Pairs ({pairs.length} of {content.pairs.length})
          </div>
          <div className="flex flex-wrap gap-2">
            {pairs.map((pair, idx) => {
              const leftLabel =
                content.left_items.find((i) => i.id === pair.left_id)?.label || pair.left_id
              const rightLabel =
                content.right_items.find((i) => i.id === pair.right_id)?.label || pair.right_id
              return (
                <div
                  key={`${pair.left_id}-${pair.right_id}`}
                  className="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl text-sm font-medium border border-indigo-200 dark:border-indigo-800 bg-white dark:bg-slate-800 shadow-sm"
                >
                  <span className="text-slate-900 dark:text-white">{leftLabel}</span>
                  <span className="text-slate-400">↔</span>
                  <span className="text-slate-900 dark:text-white">{rightLabel}</span>
                  {!disabled && (
                    <button
                      type="button"
                      onClick={() => removePair(idx)}
                      className="text-slate-400 hover:text-rose-500 ml-1 p-0.5"
                      title="Disconnect pair"
                      aria-label={`Disconnect ${leftLabel} and ${rightLabel}`}
                    >
                      <Unlink className="w-3.5 h-3.5" />
                    </button>
                  )}
                </div>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}
