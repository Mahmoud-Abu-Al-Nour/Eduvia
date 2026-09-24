import React, { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate, useSearchParams } from 'react-router-dom'
import {
  Activity,
  ActivitySubmissionPayload,
  ActivityEvaluationResponse,
  MatchingPair,
} from '@/types'
import { api } from '@/services/api'
import { useSpeechSynthesis } from '@/hooks/useSpeechSynthesis'
import { MultipleChoiceActivity } from './components/MultipleChoiceActivity'
import { MatchingActivity } from './components/MatchingActivity'
import { OrderingActivity } from './components/OrderingActivity'
import { VisualIdentificationActivity } from './components/VisualIdentificationActivity'
import { DragDropActivity } from './components/DragDropActivity'
import { CognitiveCalmFeedback } from './components/CognitiveCalmFeedback'
import {
  Volume2,
  VolumeX,
  Lightbulb,
  ArrowLeft,
  Check,
  AlertCircle,
  Loader2,
  Sparkles,
} from 'lucide-react'

interface ActivityPlayerProps {
  activity?: Activity
  onExit?: () => void
}

export const ActivityPlayer: React.FC<ActivityPlayerProps> = ({
  activity: initialActivity,
  onExit,
}) => {
  const { activityId: paramActivityId } = useParams<{ activityId?: string }>()
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()

  const targetActivityId = paramActivityId || searchParams.get('activity_id')

  const [activity, setActivity] = useState<Activity | null>(initialActivity || null)
  const [loading, setLoading] = useState<boolean>(!initialActivity)
  const [loadError, setLoadError] = useState<string | null>(null)
  const [loadErrorStatus, setLoadErrorStatus] = useState<number | undefined>(undefined)

  // Learner Interaction State
  const [selectedOptionId, setSelectedOptionId] = useState<string | null>(null)
  const [matchingPairs, setMatchingPairs] = useState<MatchingPair[]>([])
  const [orderedIds, setOrderedIds] = useState<string[]>([])
  const [selectedElementId, setSelectedElementId] = useState<string | null>(null)
  const [itemToZoneMapping, setItemToZoneMapping] = useState<Record<string, string>>({})

  // Scaffolding & Assistance State
  const [hintsRevealed, setHintsRevealed] = useState<number>(0)
  const [isHintDrawerOpen, setIsHintDrawerOpen] = useState<boolean>(false)

  // Evaluation & Feedback State
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false)
  const [evaluationResult, setEvaluationResult] =
    useState<ActivityEvaluationResponse | null>(null)
  const [isFeedbackOpen, setIsFeedbackOpen] = useState<boolean>(false)
  const [submitError, setSubmitError] = useState<string | null>(null)

  // Generation provenance
  const [generationSource, setGenerationSource] = useState<string | null>(null)
  const [fallbackUsed, setFallbackUsed] = useState<boolean | null>(null)

  // Accessible Live Region Status
  const [liveAnnouncement, setLiveAnnouncement] = useState<string>('')

  // Timing tracking
  const startTimeRef = useRef<number>(Date.now())

  // Accessible Audio Narration
  const { speak, cancel, isSpeaking, isSupported } = useSpeechSynthesis()

  // Load activity if not provided as prop
  useEffect(() => {
    if (initialActivity) {
      setActivity(initialActivity)
      setLoading(false)
      return
    }

    let isMounted = true

    async function fetchActivity() {
      setLoading(true)
      setLoadError(null)
      setLoadErrorStatus(undefined)

      try {
        if (targetActivityId) {
          const loaded = await api.activities.getById(targetActivityId)
          if (isMounted) {
            setActivity(loaded)
            setLoading(false)
          }
        } else {
          // Demo fallback: generate an activity on the fly for demo objective 1
          const demoObjectiveId = '77777777-7777-7777-7777-777777777777'
          const res = await api.activities.generate({
            objective_id: demoObjectiveId,
            difficulty_level: 1,
            language: 'en',
          })
          if (isMounted) {
            setActivity(res.activity)
            setGenerationSource(res.generation_source)
            setFallbackUsed(res.fallback_used)
            setLoading(false)
          }
        }
      } catch (err: any) {
        if (isMounted) {
          setLoadErrorStatus(err?.status)
          setLoadError(err?.message || 'Unable to load learning activity.')
          setLoading(false)
        }
      }
    }

    fetchActivity()

    return () => {
      isMounted = false
      cancel()
    }
  }, [initialActivity, targetActivityId, cancel])

  // Initialize ordering sequence when activity loads
  useEffect(() => {
    if (activity && activity.activity_type === 'ordering' && activity.content) {
      const content = activity.content as any
      if (content.items) {
        setOrderedIds(content.items.map((i: any) => i.id))
      }
    }
    startTimeRef.current = Date.now()
  }, [activity])

  // Trigger audio narration of current prompt
  const handleReadAloud = () => {
    if (!activity) return

    if (isSpeaking) {
      cancel()
      return
    }

    let textToSpeak = `${activity.title}. ${activity.instructions}. `

    if (activity.activity_type === 'multiple_choice') {
      textToSpeak += (activity.content as any).question
    } else {
      textToSpeak += (activity.content as any).prompt
    }

    // Append current hint if open
    if (hintsRevealed > 0 && activity.hints && activity.hints[hintsRevealed - 1]) {
      textToSpeak += `. Hint: ${activity.hints[hintsRevealed - 1]}`
    }

    speak(textToSpeak)
  }

  // Reveal next hint
  const handleRevealNextHint = () => {
    if (!activity || !activity.hints) return
    if (hintsRevealed < activity.hints.length) {
      const nextCount = hintsRevealed + 1
      setHintsRevealed(nextCount)
      setIsHintDrawerOpen(true)
      const hintText = activity.hints[nextCount - 1]
      setLiveAnnouncement(`Hint ${nextCount} revealed: ${hintText}`)
      speak(`Hint: ${hintText}`)
    } else {
      setIsHintDrawerOpen(true)
    }
  }

  // Determine whether learner has provided an answer
  const isSubmissionReady = (): boolean => {
    if (!activity) return false
    switch (activity.activity_type) {
      case 'multiple_choice':
        return selectedOptionId !== null
      case 'matching':
        return matchingPairs.length > 0
      case 'ordering':
        return (
          orderedIds.length ===
          (activity.content as any).items?.length
        )
      case 'visual_identification':
        return selectedElementId !== null
      case 'drag_drop':
        return Object.keys(itemToZoneMapping).length > 0
      default:
        return false
    }
  }

  // Submit answer for authoritative evaluation
  const handleSubmit = async () => {
    if (!activity || !isSubmissionReady()) return

    setIsSubmitting(true)
    setSubmitError(null)
    setLiveAnnouncement('Evaluating your answer, please wait.')
    cancel() // stop any ongoing audio

    try {
      let submissionPayload: ActivitySubmissionPayload

      switch (activity.activity_type) {
        case 'multiple_choice':
          submissionPayload = {
            activity_type: 'multiple_choice',
            selected_option_id: selectedOptionId!,
          }
          break
        case 'matching':
          submissionPayload = {
            activity_type: 'matching',
            pairs: matchingPairs,
          }
          break
        case 'ordering':
          submissionPayload = {
            activity_type: 'ordering',
            ordered_ids: orderedIds,
          }
          break
        case 'visual_identification':
          submissionPayload = {
            activity_type: 'visual_identification',
            selected_element_id: selectedElementId!,
          }
          break
        case 'drag_drop':
          submissionPayload = {
            activity_type: 'drag_drop',
            item_to_zone_mapping: itemToZoneMapping,
          }
          break
        default:
          throw new Error('Unsupported activity type')
      }

      const timeSpentSeconds = (Date.now() - startTimeRef.current) / 1000

      const evalResponse = await api.activities.evaluate({
        activity_id: activity.id,
        objective_id: activity.objective_id,
        activity_type: activity.activity_type,
        submission: submissionPayload,
        hints_used: hintsRevealed,
        time_spent_seconds: Math.round(timeSpentSeconds * 10) / 10,
        activity_content: activity.content,
      })

      setEvaluationResult(evalResponse)
      setIsFeedbackOpen(true)
      setLiveAnnouncement(
        evalResponse.is_correct
          ? `Correct answer! ${evalResponse.feedback}`
          : `Feedback: ${evalResponse.feedback}`
      )

      // Audio feedback
      if (evalResponse.is_correct) {
        speak(evalResponse.feedback)
      }
    } catch (err: any) {
      setSubmitError(
        err?.message || 'Evaluation could not be completed. Please try again.'
      )
    } finally {
      setIsSubmitting(false)
    }
  }

  // Reset interaction state to allow clean retry
  const handleTryAgain = () => {
    setIsFeedbackOpen(false)
    setEvaluationResult(null)
    setSubmitError(null)
    setLiveAnnouncement('Activity reset. You can try again.')
    startTimeRef.current = Date.now()
    cancel()

    // Keep hints revealed for scaffolding, but clear answers
    setSelectedOptionId(null)
    setMatchingPairs([])
    setSelectedElementId(null)
    setItemToZoneMapping({})
    if (activity && activity.activity_type === 'ordering') {
      const content = activity.content as any
      if (content.items) {
        setOrderedIds(content.items.map((i: any) => i.id))
      }
    }
  }

  // ── Switch & Accessible Keyboard Shortcuts ─────────────────────────────────
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Do not intercept keystrokes if the user is typing in a form input
      const targetTag = (e.target as HTMLElement)?.tagName?.toLowerCase()
      if (targetTag === 'input' || targetTag === 'textarea' || targetTag === 'select') {
        return
      }

      // Inactive while feedback dialog is open or submitting
      if (isFeedbackOpen || isSubmitting || !activity) {
        return
      }

      const key = e.key

      // Number keys 1–4: select corresponding option where available
      if (['1', '2', '3', '4'].includes(key)) {
        const optionIndex = parseInt(key, 10) - 1
        if (activity.activity_type === 'multiple_choice' && activity.content) {
          const options = (activity.content as any).options
          if (options && options[optionIndex]) {
            e.preventDefault()
            setSelectedOptionId(options[optionIndex].id)
            setLiveAnnouncement(`Selected option ${key}: ${options[optionIndex].text}`)
          }
        } else if (activity.activity_type === 'visual_identification' && activity.content) {
          const elements = (activity.content as any).elements
          if (elements && elements[optionIndex]) {
            e.preventDefault()
            setSelectedElementId(elements[optionIndex].id)
            setLiveAnnouncement(`Selected element ${key}: ${elements[optionIndex].label || key}`)
          }
        }
        return
      }

      // 'H' or 'h': Reveal/Request progressive hint
      if (key === 'h' || key === 'H') {
        if (activity.hints && activity.hints.length > 0) {
          e.preventDefault()
          handleRevealNextHint()
        }
        return
      }

      // 'R' or 'r': Replay audio narration
      if (key === 'r' || key === 'R') {
        e.preventDefault()
        handleReadAloud()
        return
      }

      // Enter or Space: Submit answer if ready
      if (key === 'Enter' || key === ' ') {
        // Allow native button press without duplicate submission
        if (targetTag === 'button') {
          return
        }
        if (isSubmissionReady()) {
          e.preventDefault()
          void handleSubmit()
        }
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [
    activity,
    isFeedbackOpen,
    isSubmitting,
    hintsRevealed,
    selectedOptionId,
    selectedElementId,
    matchingPairs,
    orderedIds,
    itemToZoneMapping,
  ])

  const handleExit = () => {
    cancel()
    if (onExit) {
      onExit()
    } else {
      navigate('/dashboard')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-slate-50 dark:bg-slate-950 p-6">
        <Loader2 className="w-10 h-10 text-indigo-600 animate-spin mb-4" />
        <p className="text-lg font-medium text-slate-700 dark:text-slate-300">
          Preparing your learning activity...
        </p>
      </div>
    )
  }

  if (loadError || !activity) {
    let errorTitle = 'Activity Unavailable'
    let errorMessage = loadError || 'The requested activity could not be loaded.'

    if (loadErrorStatus === 404) {
      errorTitle = 'Activity Not Found'
      errorMessage = 'Activity not found.'
    } else if (loadErrorStatus === 401) {
      errorTitle = 'Session Expired'
      errorMessage = 'Session expired. Please sign in again.'
    } else if (loadErrorStatus === 403) {
      errorTitle = 'Access Denied'
      errorMessage = 'You do not have permission to access this activity.'
    } else if (loadErrorStatus === 422) {
      errorTitle = 'Invalid Request'
      errorMessage = 'The request data is invalid.'
    } else if (loadErrorStatus && loadErrorStatus >= 500) {
      errorTitle = 'Server Error'
      errorMessage = 'The server encountered an error.'
    } else if (loadErrorStatus === undefined) {
      errorTitle = 'Connection Error'
      errorMessage = 'Unable to connect to the backend.'
    }

    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-slate-50 dark:bg-slate-950 p-6 text-center">
        <div className="w-16 h-16 rounded-full bg-amber-100 dark:bg-amber-950 flex items-center justify-center text-amber-600 dark:text-amber-400 mb-4">
          <AlertCircle className="w-8 h-8" />
        </div>
        <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">
          {errorTitle}
        </h2>
        <p className="text-slate-600 dark:text-slate-400 max-w-md mb-6">
          {errorMessage}
        </p>
        <button
          type="button"
          onClick={handleExit}
          className="px-6 py-3 rounded-2xl bg-indigo-600 text-white font-semibold hover:bg-indigo-700 transition-colors shadow-sm"
        >
          Return to Dashboard
        </button>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 selection:bg-indigo-100">
      {/* ── Distraction-Free Learner Header ─────────────────────────────────── */}
      <header className="sticky top-0 z-40 bg-white/90 dark:bg-slate-900/90 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 px-4 sm:px-8 py-3.5 transition-all">
        <div className="max-w-5xl mx-auto flex items-center justify-between gap-4">
          {/* Back / Exit Button */}
          <button
            type="button"
            onClick={handleExit}
            aria-label="Exit activity"
            className="flex items-center gap-2 px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-700 text-sm font-medium text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors focus:outline-none focus:ring-4 focus:ring-slate-300"
          >
            <ArrowLeft className="w-4 h-4" />
            <span className="hidden sm:inline">Exit</span>
          </button>

          {/* Activity Title Banner */}
          <div className="text-center flex-1 min-w-0">
            <h1 className="text-lg sm:text-xl font-bold text-slate-900 dark:text-white truncate">
              {activity.title}
            </h1>
            <p className="text-xs text-slate-500 dark:text-slate-400 truncate">
              {activity.instructions}
            </p>
            {generationSource && (
              <div className="flex items-center justify-center gap-2 mt-1">
                <span className={`inline-flex items-center gap-1 text-[10px] font-semibold px-2 py-0.5 rounded-full ${
                  fallbackUsed
                    ? 'bg-amber-50 text-amber-700 border border-amber-200'
                    : 'bg-violet-50 text-violet-700 border border-violet-200'
                }`}>
                  <Sparkles className="w-3 h-3" />
                  {fallbackUsed ? 'Content Bank' : `Generated by ${generationSource}`}
                </span>
              </div>
            )}
          </div>

          {/* Accessibility & Scaffolding Controls */}
          <div className="flex items-center gap-2">
            {/* Audio Read-Aloud Button */}
            {isSupported && (
              <button
                type="button"
                onClick={handleReadAloud}
                aria-label={isSpeaking ? 'Stop narration' : 'Read aloud'}
                className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-sm font-medium transition-all focus:outline-none focus:ring-4 focus:ring-indigo-400/50 ${
                  isSpeaking
                    ? 'bg-indigo-600 text-white shadow-md animate-pulse'
                    : 'bg-indigo-50 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300 hover:bg-indigo-100 dark:hover:bg-indigo-900/60'
                }`}
              >
                {isSpeaking ? (
                  <VolumeX className="w-4 h-4" />
                ) : (
                  <Volume2 className="w-4 h-4" />
                )}
                <span className="hidden sm:inline">
                  {isSpeaking ? 'Pause' : 'Listen'}
                </span>
              </button>
            )}

            {/* Hint Revelation Button */}
            {activity.hints && activity.hints.length > 0 && (
              <button
                type="button"
                onClick={handleRevealNextHint}
                aria-label="Request a hint"
                className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-sm font-medium transition-all focus:outline-none focus:ring-4 focus:ring-amber-400/50 ${
                  hintsRevealed > 0
                    ? 'bg-amber-100 dark:bg-amber-950 text-amber-900 dark:text-amber-200 border border-amber-300 dark:border-amber-700'
                    : 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'
                }`}
              >
                <Lightbulb className="w-4 h-4 text-amber-500" />
                <span className="hidden sm:inline">
                  {hintsRevealed > 0 ? `Hints (${hintsRevealed})` : 'Hint'}
                </span>
              </button>
            )}
          </div>
        </div>

        {/* Faded Scaffolding Hint Drawer */}
        {isHintDrawerOpen && activity.hints && activity.hints.length > 0 && (
          <div className="max-w-5xl mx-auto mt-3 p-4 bg-amber-50/90 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800 rounded-2xl shadow-xs transition-all animate-in slide-in-from-top duration-200">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-amber-800 dark:text-amber-300">
                <Sparkles className="w-3.5 h-3.5" />
                <span>Helpful Scaffolding</span>
              </div>
              <button
                type="button"
                onClick={() => setIsHintDrawerOpen(false)}
                className="text-xs text-slate-500 hover:text-slate-700 underline"
              >
                Hide
              </button>
            </div>
            <div className="space-y-2">
              {activity.hints.slice(0, hintsRevealed).map((hint, idx) => (
                <div
                  key={idx}
                  className="flex items-start gap-2.5 text-sm text-amber-950 dark:text-amber-100 bg-white/70 dark:bg-slate-900/60 p-2.5 rounded-xl border border-amber-100 dark:border-amber-900"
                >
                  <span className="font-bold text-amber-600 shrink-0">
                    Step {idx + 1}:
                  </span>
                  <span>{hint}</span>
                </div>
              ))}
              {hintsRevealed < activity.hints.length && (
                <button
                  type="button"
                  onClick={handleRevealNextHint}
                  className="mt-1 text-xs font-semibold text-indigo-600 dark:text-indigo-400 hover:underline"
                >
                  Need more help? Show next hint ({hintsRevealed + 1} of{' '}
                  {activity.hints.length})
                </button>
              )}
            </div>
          </div>
        )}
      </header>

      {/* ── Accessible Live Region ────────────────────────────────────────── */}
      <div
        role="status"
        aria-live="polite"
        aria-atomic="true"
        className="sr-only"
      >
        {liveAnnouncement}
      </div>

      {/* ── Main Activity Interaction Stage ───────────────────────────────── */}
      <main
        id="main-content"
        tabIndex={-1}
        className="flex-1 flex flex-col justify-center max-w-5xl w-full mx-auto p-4 sm:p-8 focus:outline-none"
      >
        {submitError && (
          <div className="mb-6 p-4 rounded-2xl bg-rose-50 dark:bg-rose-950/50 border border-rose-200 dark:border-rose-800 text-rose-800 dark:text-rose-200 flex items-center gap-3">
            <AlertCircle className="w-5 h-5 shrink-0" />
            <p className="text-sm font-medium">{submitError}</p>
          </div>
        )}

        {/* Modality Renderers */}
        <div className="py-2">
          {activity.activity_type === 'multiple_choice' && (
            <MultipleChoiceActivity
              content={activity.content as any}
              selectedOptionId={selectedOptionId}
              onSelect={setSelectedOptionId}
              disabled={isSubmitting}
            />
          )}

          {activity.activity_type === 'matching' && (
            <MatchingActivity
              content={activity.content as any}
              pairs={matchingPairs}
              onChange={setMatchingPairs}
              disabled={isSubmitting}
            />
          )}

          {activity.activity_type === 'ordering' && (
            <OrderingActivity
              content={activity.content as any}
              orderedIds={orderedIds}
              onChange={setOrderedIds}
              disabled={isSubmitting}
            />
          )}

          {activity.activity_type === 'visual_identification' && (
            <VisualIdentificationActivity
              content={activity.content as any}
              selectedElementId={selectedElementId}
              onSelect={setSelectedElementId}
              disabled={isSubmitting}
            />
          )}

          {activity.activity_type === 'drag_drop' && (
            <DragDropActivity
              content={activity.content as any}
              mapping={itemToZoneMapping}
              onChange={setItemToZoneMapping}
              disabled={isSubmitting}
            />
          )}
        </div>
      </main>

      {/* ── Persistent Bottom Action Bar ──────────────────────────────────── */}
      <footer className="sticky bottom-0 z-30 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md border-t border-slate-200 dark:border-slate-800 p-4 sm:p-6 shadow-lg">
        <div className="max-w-md mx-auto">
          <button
            type="button"
            disabled={!isSubmissionReady() || isSubmitting}
            onClick={handleSubmit}
            className={`w-full flex items-center justify-center gap-2 py-4 px-6 rounded-2xl font-bold text-lg sm:text-xl shadow-lg transition-all min-h-[3.5rem] focus:outline-none focus:ring-4 focus:ring-indigo-400 ${
              isSubmissionReady() && !isSubmitting
                ? 'bg-indigo-600 hover:bg-indigo-700 text-white cursor-pointer active:scale-[0.99]'
                : 'bg-slate-200 dark:bg-slate-800 text-slate-400 dark:text-slate-500 cursor-not-allowed'
            }`}
          >
            {isSubmitting ? (
              <>
                <Loader2 className="w-6 h-6 animate-spin" />
                <span>Checking...</span>
              </>
            ) : (
              <>
                <Check className="w-6 h-6" />
                <span>Check My Answer</span>
              </>
            )}
          </button>
        </div>
      </footer>

      {/* ── Cognitive Calm Feedback Modal ─────────────────────────────────── */}
      {isFeedbackOpen && evaluationResult && (
        <CognitiveCalmFeedback
          result={evaluationResult}
          onTryAgain={handleTryAgain}
          onNext={handleExit}
          onClose={() => setIsFeedbackOpen(false)}
        />
      )}
    </div>
  )
}
