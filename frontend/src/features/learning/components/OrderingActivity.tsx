import React from 'react'
import { OrderingContent } from '@/types'
import { ArrowUp, ArrowDown, ArrowUpDown } from 'lucide-react'

interface OrderingActivityProps {
  content: OrderingContent
  orderedIds: string[]
  onChange: (orderedIds: string[]) => void
  disabled?: boolean
}

export const OrderingActivity: React.FC<OrderingActivityProps> = ({
  content,
  orderedIds,
  onChange,
  disabled = false,
}) => {
  // If orderedIds not fully populated, initialize with content.items order
  const currentOrder =
    orderedIds && orderedIds.length === content.items.length
      ? orderedIds
      : content.items.map((i) => i.id)

  const moveItem = (fromIndex: number, toIndex: number) => {
    if (disabled) return
    if (toIndex < 0 || toIndex >= currentOrder.length) return

    const next = [...currentOrder]
    const [moved] = next.splice(fromIndex, 1)
    next.splice(toIndex, 0, moved)
    onChange(next)
  }

  const directionLabel =
    content.direction === 'ascending'
      ? 'First to Last / Smallest to Largest'
      : content.direction === 'descending'
      ? 'Last to First / Largest to Smallest'
      : 'Chronological Order'

  return (
    <div className="space-y-6 w-full max-w-2xl mx-auto">
      {/* Prompt Card */}
      <div className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm border border-slate-200 dark:border-slate-700 rounded-2xl p-6 shadow-sm text-center">
        <h2 className="text-xl sm:text-2xl font-semibold text-slate-900 dark:text-white leading-relaxed">
          {content.prompt}
        </h2>
        <div className="inline-flex items-center gap-1.5 mt-2 px-3 py-1 rounded-full bg-slate-100 dark:bg-slate-700 text-xs font-medium text-slate-600 dark:text-slate-300">
          <ArrowUpDown className="w-3.5 h-3.5" />
          <span>{directionLabel}</span>
        </div>
      </div>

      {/* Ordered Items List */}
      <div className="space-y-3" role="list" aria-label={content.prompt}>
        {currentOrder.map((id, index) => {
          const item = content.items.find((i) => i.id === id)
          if (!item) return null

          const isFirst = index === 0
          const isLast = index === currentOrder.length - 1

          return (
            <div
              key={item.id}
              role="listitem"
              className="flex items-center justify-between p-4 bg-white dark:bg-slate-800 border-2 border-slate-200 dark:border-slate-700 rounded-2xl shadow-sm hover:border-slate-300 dark:hover:border-slate-600 transition-all"
            >
              {/* Position Badge & Item Label */}
              <div className="flex items-center gap-4">
                <span className="flex items-center justify-center w-8 h-8 rounded-full bg-indigo-100 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300 font-bold text-sm select-none">
                  {index + 1}
                </span>
                <span className="text-lg sm:text-xl font-medium text-slate-800 dark:text-slate-100">
                  {item.label}
                </span>
                {item.visual_cue && (
                  <span className="text-2xl ml-2 select-none">{item.visual_cue}</span>
                )}
              </div>

              {/* Accessible Reorder Controls */}
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  disabled={disabled || isFirst}
                  onClick={() => moveItem(index, index - 1)}
                  aria-label={`Move ${item.label} up`}
                  className="p-3 rounded-xl border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-700 disabled:opacity-30 disabled:cursor-not-allowed focus:outline-none focus:ring-4 focus:ring-indigo-400/50"
                >
                  <ArrowUp className="w-5 h-5 text-slate-600 dark:text-slate-300" />
                </button>

                <button
                  type="button"
                  disabled={disabled || isLast}
                  onClick={() => moveItem(index, index + 1)}
                  aria-label={`Move ${item.label} down`}
                  className="p-3 rounded-xl border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-700 disabled:opacity-30 disabled:cursor-not-allowed focus:outline-none focus:ring-4 focus:ring-indigo-400/50"
                >
                  <ArrowDown className="w-5 h-5 text-slate-600 dark:text-slate-300" />
                </button>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
