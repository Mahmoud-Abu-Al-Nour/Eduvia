import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  BookOpen,
  ArrowRight,
  ArrowLeft,
  Volume2,
  VolumeX,
  Sparkles,
  Loader2,
  AlertCircle,
} from 'lucide-react'
import { api } from '@/services/api'
import { useSpeechSynthesis } from '@/hooks/useSpeechSynthesis'
import type { InstructionalContent, InstructionalBlock } from '@/types'

export const InstructionalContentView: React.FC = () => {
  const { objectiveId } = useParams<{ objectiveId: string }>()
  const navigate = useNavigate()

  const [content, setContent] = useState<InstructionalContent | null>(null)
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  const { speak, cancel, isSpeaking, isSupported } = useSpeechSynthesis()

  useEffect(() => {
    if (!objectiveId) return
    let active = true

    async function loadContent() {
      setLoading(true)
      setError(null)
      try {
        const list = await api.instructional.getByObjective(objectiveId!, true)
        if (active) {
          if (list.length > 0) {
            setContent(list[0])
          } else {
            setError('No instructional material currently available for this objective.')
          }
        }
      } catch (err: any) {
        if (active) {
          setError(err?.message || 'Failed to load instructional explanation.')
        }
      } finally {
        if (active) {
          setLoading(false)
        }
      }
    }

    loadContent()

    return () => {
      active = false
      cancel()
    }
  }, [objectiveId, cancel])

  const handleReadAloud = () => {
    if (!content) return
    if (isSpeaking) {
      cancel()
      return
    }

    const narration = [
      content.title,
      ...content.blocks.map((b) => `${b.title ? b.title + '. ' : ''}${b.body}`),
      `Summary: ${content.summary}`,
    ].join('. ')

    speak(narration)
  }

  const handleStartPractice = () => {
    cancel()
    navigate(`/learn?objective_id=${objectiveId}`)
  }

  const handleBack = () => {
    cancel()
    navigate(-1)
  }

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-slate-50 dark:bg-slate-950 p-6">
        <Loader2 className="w-10 h-10 text-indigo-600 animate-spin mb-4" />
        <p className="text-lg font-medium text-slate-700 dark:text-slate-300">
          Loading learning explanation...
        </p>
      </div>
    )
  }

  if (error || !content) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-slate-50 dark:bg-slate-950 p-6">
        <div className="max-w-md w-full p-8 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-xl text-center space-y-4">
          <AlertCircle className="w-12 h-12 text-amber-500 mx-auto" />
          <h2 className="text-xl font-bold text-slate-900 dark:text-white">Explanation Unavailable</h2>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            {error || 'We could not find an instructional guide for this objective.'}
          </p>
          <div className="flex gap-3 pt-2">
            <button
              type="button"
              onClick={handleBack}
              className="flex-1 py-3 px-4 rounded-xl border border-slate-200 dark:border-slate-800 text-sm font-semibold"
            >
              Go Back
            </button>
            <button
              type="button"
              onClick={handleStartPractice}
              className="flex-1 py-3 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-bold"
            >
              Start Practice
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100">
      {/* ── Top Navigation Bar ────────────────────────────────────────────── */}
      <header className="sticky top-0 z-30 bg-white/90 dark:bg-slate-900/90 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 px-4 sm:px-8 py-4">
        <div className="max-w-4xl mx-auto flex items-center justify-between gap-4">
          <button
            type="button"
            onClick={handleBack}
            className="flex items-center gap-2 px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 text-sm font-medium text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            <span className="hidden sm:inline">Back</span>
          </button>

          <div className="text-center flex-1 min-w-0">
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-indigo-50 text-indigo-700 dark:bg-indigo-950 dark:text-indigo-300 mb-1">
              <BookOpen className="w-3.5 h-3.5" />
              <span>Instructional Learning</span>
            </div>
            <h1 className="text-lg sm:text-xl font-extrabold text-slate-900 dark:text-white truncate">
              {content.title}
            </h1>
          </div>

          {/* Audio TTS Button */}
          {isSupported && (
            <button
              type="button"
              onClick={handleReadAloud}
              aria-label={isSpeaking ? 'Pause narration' : 'Listen to explanation'}
              className={`flex items-center gap-1.5 px-4 py-2 rounded-xl text-sm font-semibold transition-all shadow-sm ${
                isSpeaking
                  ? 'bg-indigo-600 text-white animate-pulse'
                  : 'bg-indigo-50 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300 hover:bg-indigo-100 dark:hover:bg-indigo-900'
              }`}
            >
              {isSpeaking ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
              <span>{isSpeaking ? 'Pause' : 'Listen'}</span>
            </button>
          )}
        </div>
      </header>

      {/* ── Main Instructional Presentation ───────────────────────────────── */}
      <main className="flex-1 max-w-4xl w-full mx-auto p-4 sm:p-8 space-y-6">
        {/* Method Badge & Summary Header */}
        <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-3">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold px-3 py-1 rounded-full bg-violet-100 text-violet-800 dark:bg-violet-950 dark:text-violet-300">
              {content.explanation_method.replace('_', ' ').toUpperCase()}
            </span>
            <span className="text-xs text-slate-500">Foundational Concept</span>
          </div>
          <p className="text-base sm:text-lg text-slate-700 dark:text-slate-300 leading-relaxed font-medium">
            {content.summary}
          </p>
        </div>

        {/* Structured Explanation Blocks */}
        <div className="space-y-4">
          {content.blocks.map((block: InstructionalBlock, idx: number) => {
            if (block.block_type === 'heading') {
              return (
                <div
                  key={block.id || idx}
                  className="pt-2 pb-1 flex items-center gap-3 border-b border-slate-200 dark:border-slate-800"
                >
                  {block.visual_cue && <span className="text-2xl">{block.visual_cue}</span>}
                  <div>
                    <h2 className="text-xl font-extrabold text-slate-900 dark:text-white">
                      {block.title || block.body}
                    </h2>
                    {block.title && block.body && (
                      <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">{block.body}</p>
                    )}
                  </div>
                </div>
              )
            }

            if (block.block_type === 'step') {
              return (
                <div
                  key={block.id || idx}
                  className="p-5 rounded-2xl border border-indigo-100 dark:border-indigo-900/60 bg-white dark:bg-slate-900 shadow-xs flex items-start gap-4"
                >
                  <div className="w-10 h-10 rounded-2xl bg-indigo-100 dark:bg-indigo-950 flex items-center justify-center font-extrabold text-indigo-700 dark:text-indigo-300 shrink-0">
                    {block.visual_cue || `${idx + 1}`}
                  </div>
                  <div className="space-y-1">
                    {block.title && (
                      <h3 className="font-bold text-base text-slate-900 dark:text-white">
                        {block.title}
                      </h3>
                    )}
                    <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed">
                      {block.body}
                    </p>
                  </div>
                </div>
              )
            }

            if (block.block_type === 'worked_example') {
              return (
                <div
                  key={block.id || idx}
                  className="p-6 rounded-3xl border-2 border-indigo-200 dark:border-indigo-800 bg-indigo-50/40 dark:bg-indigo-950/20 space-y-3"
                >
                  <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-indigo-700 dark:text-indigo-300">
                    <Sparkles className="w-4 h-4" />
                    <span>Modeled Example</span>
                  </div>
                  {block.title && (
                    <h3 className="font-extrabold text-lg text-slate-900 dark:text-white">
                      {block.title}
                    </h3>
                  )}
                  <p className="text-base text-slate-800 dark:text-slate-200 leading-relaxed font-medium">
                    {block.body}
                  </p>
                </div>
              )
            }

            if (block.block_type === 'visual_cue') {
              return (
                <div
                  key={block.id || idx}
                  className="p-6 rounded-3xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-center space-y-3"
                >
                  {block.visual_cue && <div className="text-5xl">{block.visual_cue}</div>}
                  {block.title && (
                    <h3 className="font-bold text-base text-slate-900 dark:text-white">
                      {block.title}
                    </h3>
                  )}
                  <p className="text-sm text-slate-600 dark:text-slate-400 max-w-lg mx-auto">
                    {block.body}
                  </p>
                </div>
              )
            }

            if (block.block_type === 'callout') {
              return (
                <div
                  key={block.id || idx}
                  className="p-5 rounded-2xl border border-amber-200 dark:border-amber-800 bg-amber-50/70 dark:bg-amber-950/30 flex items-start gap-3.5"
                >
                  <span className="text-2xl mt-0.5">{block.visual_cue || '💡'}</span>
                  <div>
                    {block.title && (
                      <h4 className="font-bold text-sm text-amber-900 dark:text-amber-200 mb-1">
                        {block.title}
                      </h4>
                    )}
                    <p className="text-sm text-amber-950 dark:text-amber-100 leading-relaxed">
                      {block.body}
                    </p>
                  </div>
                </div>
              )
            }

            // Standard Text Block
            if (block.block_type === 'text' || block.block_type === 'audio_script') {
              return (
                <div
                  key={block.id || idx}
                  className="p-5 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs space-y-1.5"
                >
                  {block.title && (
                    <h3 className="font-bold text-base text-slate-900 dark:text-white flex items-center gap-2">
                      {block.visual_cue && <span>{block.visual_cue}</span>}
                      <span>{block.title}</span>
                    </h3>
                  )}
                  <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed">
                    {block.body}
                  </p>
                </div>
              )
            }

            return null
          })}
        </div>
      </main>

      {/* ── Bottom Transition Bar (Explanation -> Practice) ────────────────── */}
      <footer className="sticky bottom-0 z-30 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md border-t border-slate-200 dark:border-slate-800 p-4 sm:p-6 shadow-lg">
        <div className="max-w-4xl mx-auto flex items-center justify-between gap-4">
          <div className="hidden sm:block">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Ready to Practice?
            </span>
            <p className="text-sm font-semibold text-slate-900 dark:text-white">
              Try interactive multi-question practice now.
            </p>
          </div>

          <button
            type="button"
            onClick={handleStartPractice}
            className="w-full sm:w-auto flex items-center justify-center gap-2 py-3.5 px-8 rounded-2xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-base shadow-lg transition-all active:scale-[0.99] focus:outline-none focus:ring-4 focus:ring-indigo-400 cursor-pointer"
          >
            <span>Start Practice Activity</span>
            <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </footer>
    </div>
  )
}
