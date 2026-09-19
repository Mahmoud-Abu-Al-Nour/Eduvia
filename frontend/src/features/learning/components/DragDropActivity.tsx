import React, { useState } from 'react'
import { DragDropContent } from '@/types'
import { FolderDown, X, Layers } from 'lucide-react'

interface DragDropActivityProps {
  content: DragDropContent
  mapping: Record<string, string>
  onChange: (mapping: Record<string, string>) => void
  disabled?: boolean
}

export const DragDropActivity: React.FC<DragDropActivityProps> = ({
  content,
  mapping,
  onChange,
  disabled = false,
}) => {
  const [selectedItemId, setSelectedItemId] = useState<string | null>(null)

  // Determine which items are currently unassigned
  const unassignedItems = content.items.filter((item) => !mapping[item.id])

  const handleItemSelect = (id: string) => {
    if (disabled) return
    setSelectedItemId(selectedItemId === id ? null : id)
  }

  const handleZoneClick = (zoneId: string) => {
    if (disabled) return
    if (!selectedItemId) return

    // Assign selected item to this zone
    const next = { ...mapping, [selectedItemId]: zoneId }
    onChange(next)
    setSelectedItemId(null)
  }

  const handleRemoveFromZone = (itemId: string) => {
    if (disabled) return
    const next = { ...mapping }
    delete next[itemId]
    onChange(next)
  }

  // HTML5 Drag handlers for desktop mouse interaction
  const handleDragStart = (e: React.DragEvent, id: string) => {
    if (disabled) return
    e.dataTransfer.setData('text/plain', id)
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
  }

  const handleDrop = (e: React.DragEvent, zoneId: string) => {
    e.preventDefault()
    if (disabled) return
    const id = e.dataTransfer.getData('text/plain')
    if (id && content.items.some((i) => i.id === id)) {
      onChange({ ...mapping, [id]: zoneId })
    }
  }

  return (
    <div className="space-y-6 w-full max-w-4xl mx-auto">
      {/* Prompt Card */}
      <div className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm border border-slate-200 dark:border-slate-700 rounded-2xl p-6 shadow-sm text-center">
        <h2 className="text-xl sm:text-2xl font-semibold text-slate-900 dark:text-white leading-relaxed">
          {content.prompt}
        </h2>
        <p className="text-sm text-slate-500 dark:text-slate-400 mt-2">
          {selectedItemId
            ? 'Now tap a target zone to place the item.'
            : 'Tap or drag an item below, then choose its correct zone.'}
        </p>
      </div>

      {/* Unassigned Items Tray */}
      <div className="bg-slate-50 dark:bg-slate-900/40 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm">
        <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-slate-500 mb-3">
          <Layers className="w-4 h-4" />
          <span>Items to Sort ({unassignedItems.length} remaining)</span>
        </div>

        {unassignedItems.length === 0 ? (
          <div className="py-4 text-center text-sm font-medium text-emerald-600 dark:text-emerald-400">
            All items have been categorized! Review your zones below.
          </div>
        ) : (
          <div className="flex flex-wrap gap-3">
            {unassignedItems.map((item) => {
              const isSelected = selectedItemId === item.id
              return (
                <button
                  key={item.id}
                  type="button"
                  draggable={!disabled}
                  onDragStart={(e) => handleDragStart(e, item.id)}
                  onClick={() => handleItemSelect(item.id)}
                  disabled={disabled}
                  className={`inline-flex items-center gap-2 px-4 py-3 rounded-xl border-2 font-medium text-base sm:text-lg transition-all focus:outline-none focus:ring-4 focus:ring-indigo-400/50 ${
                    isSelected
                      ? 'border-indigo-600 bg-indigo-50 dark:bg-indigo-950 text-indigo-900 dark:text-indigo-200 shadow-md scale-105'
                      : 'border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 hover:border-indigo-400 shadow-sm'
                  } ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-grab active:cursor-grabbing'}`}
                >
                  <span>{item.label}</span>
                  {item.visual_cue && <span className="text-xl">{item.visual_cue}</span>}
                </button>
              )
            })}
          </div>
        )}
      </div>

      {/* Target Drop Zones Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {content.zones.map((zone) => {
          const zoneItems = content.items.filter((i) => mapping[i.id] === zone.id)
          const isTargeted = selectedItemId !== null

          return (
            <div
              key={zone.id}
              onClick={() => handleZoneClick(zone.id)}
              onDragOver={handleDragOver}
              onDrop={(e) => handleDrop(e, zone.id)}
              className={`flex flex-col justify-between p-5 rounded-2xl border-2 transition-all min-h-[12rem] ${
                isTargeted
                  ? 'border-dashed border-indigo-400 bg-indigo-50/30 dark:bg-indigo-950/20 cursor-pointer hover:border-indigo-600 hover:bg-indigo-50/60 dark:hover:bg-indigo-950/40'
                  : 'border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 shadow-sm'
              }`}
            >
              <div>
                <div className="flex items-center justify-between gap-2 border-b border-slate-100 dark:border-slate-700 pb-2 mb-3">
                  <div className="flex items-center gap-2">
                    <FolderDown className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                    <span className="font-semibold text-lg text-slate-900 dark:text-white">
                      {zone.label}
                    </span>
                  </div>
                  <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300">
                    {zoneItems.length}
                  </span>
                </div>

                {/* Items in Zone */}
                <div className="flex flex-wrap gap-2">
                  {zoneItems.map((item) => (
                    <div
                      key={item.id}
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-50 dark:bg-indigo-950/60 border border-indigo-200 dark:border-indigo-800 text-sm font-medium text-slate-800 dark:text-slate-200 shadow-xs"
                    >
                      <span>{item.label}</span>
                      {item.visual_cue && <span>{item.visual_cue}</span>}
                      {!disabled && (
                        <button
                          type="button"
                          onClick={(e) => {
                            e.stopPropagation()
                            handleRemoveFromZone(item.id)
                          }}
                          aria-label={`Remove ${item.label} from ${zone.label}`}
                          className="text-slate-400 hover:text-rose-500 p-0.5"
                        >
                          <X className="w-3.5 h-3.5" />
                        </button>
                      )}
                    </div>
                  ))}
                  {zoneItems.length === 0 && (
                    <div className="text-xs text-slate-400 italic py-4 text-center w-full">
                      Empty zone
                    </div>
                  )}
                </div>
              </div>

              {isTargeted && (
                <div className="mt-4 pt-2 text-center text-xs font-medium text-indigo-600 dark:text-indigo-400">
                  Tap to place selected item here
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
