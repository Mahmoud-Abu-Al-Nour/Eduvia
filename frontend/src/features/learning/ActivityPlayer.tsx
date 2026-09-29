import React, { useState, useEffect, useRef, useMemo } from 'react'
import { useParams, useNavigate, useSearchParams } from 'react-router-dom'
import {
  Activity,
  ActivityQuestion,
  ActivitySubmissionPayload,
  ActivityEvaluationResponse,
  ActivityType,
  MatchingPair,
  MultipleChoiceSubmission,
  MatchingSubmission,
  OrderingSubmission,
  VisualIdentificationSubmission,
  DragDropSubmission,
  QuestionSubmission,
} from '@/types'
import { api } from '@/services/api'
import { useSpeechSynthesis } from '@/hooks/useSpeechSynthesis'
import { MultipleChoiceActivity } from './components/MultipleChoiceActivity'
import { MatchingActivity } from './components/MatchingActivity'
import { OrderingActivity } from './components/OrderingActivity'
import { VisualIdentificationActivity } from './components/VisualIdentificationActivity'
import { DragDropActivity } from './components/DragDropActivity'
import {
  Volume2,
  VolumeX,
  Lightbulb,
  ArrowLeft,
  ArrowRight,
  Check,
  AlertCircle,
  Loader2,
  Sparkles,
  RotateCcw,
  CheckCircle2,
  XCircle,
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
  const rawActivityType = searchParams.get('activity_type')
  const validActivityTypes: ActivityType[] = [
    'multiple_choice',
    'matching',
    'ordering',
    'visual_identification',
    'drag_drop',
  ]
  const targetActivityType: ActivityType | undefined = validActivityTypes.includes(rawActivityType as any)
    ? (rawActivityType as ActivityType)
    : undefined

  const [activity, setActivity] = useState<Activity | null>(initialActivity || null)
  const [loading, setLoading] = useState<boolean>(!initialActivity)
  const [loadError, setLoadError] = useState<string | null>(null)
  const [loadErrorStatus, setLoadErrorStatus] = useState<number | undefined>(undefined)

  // Multi-Question State
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState<number>(0)
  // Per-question state keyed by question id
  const [answersByQuestionId, setAnswersByQuestionId] = useState<Record<string, ActivitySubmissionPayload>>({})

  // Scaffolding & Assistance State
  const [hintsRevealed, setHintsRevealed] = useState<number>(0)
  const [isHintDrawerOpen, setIsHintDrawerOpen] = useState<boolean>(false)

  // Evaluation & Feedback State
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false)
  const [evaluationResult, setEvaluationResult] = useState<ActivityEvaluationResponse | null>(null)
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
          // Demo/Practice mode: generate an activity for demo objective 1
          const demoObjectiveId = '77777777-7777-7777-7777-777777777777'
          const res = await api.activities.generate({
            objective_id: demoObjectiveId,
            activity_type: targetActivityType || 'multiple_choice',
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
  }, [initialActivity, targetActivityId, targetActivityType, cancel])

  // Normalize questions array (backward compatibility with legacy 1-question activities)
  const questions: ActivityQuestion[] = useMemo(() => {
    if (!activity) return []
    if (activity.questions && activity.questions.length > 0) {
      return activity.questions
    }
    if (activity.content) {
      return [
        {
          id: activity.id || 'q1',
          question_number: 1,
          question_type: activity.activity_type,
          content: activity.content,
          hints: activity.hints,
        },
      ]
    }
    return []
  }, [activity])

  // Reset interaction state when activity changes
  useEffect(() => {
    setCurrentQuestionIndex(0)
    setAnswersByQuestionId({})
    setHintsRevealed(0)
    setIsHintDrawerOpen(false)
    setEvaluationResult(null)
    setIsFeedbackOpen(false)
    setSubmitError(null)
    startTimeRef.current = Date.now()
  }, [activity])

  const currentQuestion: ActivityQuestion | undefined = questions[currentQuestionIndex]
  const currentHints = currentQuestion?.hints && currentQuestion.hints.length > 0
    ? currentQuestion.hints
    : (activity?.hints || [])

  // Trigger audio narration of current prompt
  const handleReadAloud = () => {
    if (!activity || !currentQuestion) return

    if (isSpeaking) {
      cancel()
      return
    }

    let textToSpeak = `${activity.title}. Question ${currentQuestionIndex + 1} of ${questions.length}. `

    const content = currentQuestion.content as any
    if (content.question) {
      textToSpeak += content.question
    } else if (content.prompt) {
      textToSpeak += content.prompt
    }

    // Append current hint if open
    if (hintsRevealed > 0 && currentHints[hintsRevealed - 1]) {
      textToSpeak += `. Hint: ${currentHints[hintsRevealed - 1]}`
    }

    speak(textToSpeak)
  }

  // Reveal next hint
  const handleRevealNextHint = () => {
    if (!currentHints || currentHints.length === 0) return
    if (hintsRevealed < currentHints.length) {
      const nextCount = hintsRevealed + 1
      setHintsRevealed(nextCount)
      setIsHintDrawerOpen(true)
      const hintText = currentHints[nextCount - 1]
      setLiveAnnouncement(`Hint ${nextCount} revealed: ${hintText}`)
      speak(`Hint: ${hintText}`)
    } else {
      setIsHintDrawerOpen(true)
    }
  }

  // Determine whether a question has an answer
  const isQuestionAnswered = (qId: string): boolean => {
    const ans = answersByQuestionId[qId]
    if (!ans) return false
    switch (ans.activity_type) {
      case 'multiple_choice':
        return Boolean((ans as MultipleChoiceSubmission).selected_option_id)
      case 'matching':
        return Boolean((ans as MatchingSubmission).pairs && (ans as MatchingSubmission).pairs.length > 0)
      case 'ordering':
        return Boolean((ans as OrderingSubmission).ordered_ids && (ans as OrderingSubmission).ordered_ids.length > 0)
      case 'visual_identification':
        return Boolean((ans as VisualIdentificationSubmission).selected_element_id)
      case 'drag_drop':
        return Boolean((ans as DragDropSubmission).item_to_zone_mapping && Object.keys((ans as DragDropSubmission).item_to_zone_mapping).length > 0)
      default:
        return false
    }
  }

  const answeredQuestionsCount = questions.filter((q) => isQuestionAnswered(q.id)).length
  const isAnyQuestionAnswered = answeredQuestionsCount > 0

  // Per-Question interaction setters
  const handleOptionSelect = (selectedOptionId: string) => {
    if (!currentQuestion) return
    setAnswersByQuestionId((prev) => ({
      ...prev,
      [currentQuestion.id]: {
        activity_type: 'multiple_choice',
        selected_option_id: selectedOptionId,
      },
    }))
  }

  const handleMatchingChange = (matchingPairs: MatchingPair[]) => {
    if (!currentQuestion) return
    setAnswersByQuestionId((prev) => ({
      ...prev,
      [currentQuestion.id]: {
        activity_type: 'matching',
        pairs: matchingPairs,
      },
    }))
  }

  const handleOrderingChange = (orderedIds: string[]) => {
    if (!currentQuestion) return
    setAnswersByQuestionId((prev) => ({
      ...prev,
      [currentQuestion.id]: {
        activity_type: 'ordering',
        ordered_ids: orderedIds,
      },
    }))
  }

  const handleVisualSelect = (selectedElementId: string) => {
    if (!currentQuestion) return
    setAnswersByQuestionId((prev) => ({
      ...prev,
      [currentQuestion.id]: {
        activity_type: 'visual_identification',
        selected_element_id: selectedElementId,
      },
    }))
  }

  const handleDragDropChange = (itemToZoneMapping: Record<string, string>) => {
    if (!currentQuestion) return
    setAnswersByQuestionId((prev) => ({
      ...prev,
      [currentQuestion.id]: {
        activity_type: 'drag_drop',
        item_to_zone_mapping: itemToZoneMapping,
      },
    }))
  }

  // Navigation handlers
  const handlePreviousQuestion = () => {
    if (currentQuestionIndex > 0) {
      cancel()
      setCurrentQuestionIndex((prev) => prev - 1)
      setIsHintDrawerOpen(false)
      setLiveAnnouncement(`Navigated to Question ${currentQuestionIndex} of ${questions.length}`)
    }
  }

  const handleNextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      cancel()
      setCurrentQuestionIndex((prev) => prev + 1)
      setIsHintDrawerOpen(false)
      setLiveAnnouncement(`Navigated to Question ${currentQuestionIndex + 2} of ${questions.length}`)
    }
  }

  const handleJumpToQuestion = (index: number) => {
    if (index >= 0 && index < questions.length) {
      cancel()
      setCurrentQuestionIndex(index)
      setIsHintDrawerOpen(false)
      setLiveAnnouncement(`Switched to Question ${index + 1} of ${questions.length}`)
    }
  }

  // Submit all answers for authoritative evaluation
  const handleSubmit = async () => {
    if (!activity || !isAnyQuestionAnswered) return

    setIsSubmitting(true)
    setSubmitError(null)
    setLiveAnnouncement('Evaluating your answer, please wait.')
    cancel()

    try {
      // Assemble structured QuestionSubmission array
      const submissions: QuestionSubmission[] = questions.map((q) => {
        const ans = answersByQuestionId[q.id]
        if (ans) {
          return { question_id: q.id, submission: ans }
        }
        // Fallback placeholder payload for unanswered question
        if (q.question_type === 'multiple_choice') {
          return { question_id: q.id, submission: { activity_type: 'multiple_choice', selected_option_id: '' } }
        }
        if (q.question_type === 'matching') {
          return { question_id: q.id, submission: { activity_type: 'matching', pairs: [] } }
        }
        if (q.question_type === 'ordering') {
          return { question_id: q.id, submission: { activity_type: 'ordering', ordered_ids: [] } }
        }
        if (q.question_type === 'visual_identification') {
          return { question_id: q.id, submission: { activity_type: 'visual_identification', selected_element_id: '' } }
        }
        return { question_id: q.id, submission: { activity_type: 'drag_drop', item_to_zone_mapping: {} } }
      })

      const timeSpentSeconds = (Date.now() - startTimeRef.current) / 1000

      const evalResponse = await api.activities.evaluate({
        activity_id: activity.id,
        objective_id: activity.objective_id,
        activity_type: activity.activity_type,
        submission: submissions[0]?.submission,
        questions: submissions,
        hints_used: hintsRevealed,
        time_spent_seconds: Math.round(timeSpentSeconds * 10) / 10,
        activity_content: activity.content,
      })

      setEvaluationResult(evalResponse)
      setIsFeedbackOpen(true)
      const correctCount = evalResponse.questions_correct ?? (evalResponse.is_correct ? questions.length : 0)
      const totalCount = evalResponse.questions_total ?? questions.length
      setLiveAnnouncement(
        `Activity completed. ${correctCount} of ${totalCount} correct. ${evalResponse.feedback}`
      )

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
    setAnswersByQuestionId({})
    setCurrentQuestionIndex(0)
    setHintsRevealed(0)
    setLiveAnnouncement('Activity reset. You can try again.')
    startTimeRef.current = Date.now()
    cancel()
  }

  // Keyboard navigation & accessibility
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const targetTag = (e.target as HTMLElement)?.tagName?.toLowerCase()
      if (targetTag === 'input' || targetTag === 'textarea' || targetTag === 'select') {
        return
      }

      if (isFeedbackOpen || isSubmitting || !currentQuestion) {
        return
      }

      const key = e.key

      // Number keys 1–4: select corresponding option where available
      if (['1', '2', '3', '4'].includes(key)) {
        const optionIndex = parseInt(key, 10) - 1
        if (currentQuestion.question_type === 'multiple_choice' && currentQuestion.content) {
          const options = (currentQuestion.content as any).options
          if (options && options[optionIndex]) {
            e.preventDefault()
            handleOptionSelect(options[optionIndex].id)
            setLiveAnnouncement(`Selected option ${key}: ${options[optionIndex].text}`)
          }
        } else if (currentQuestion.question_type === 'visual_identification' && currentQuestion.content) {
          const elements = (currentQuestion.content as any).elements
          if (elements && elements[optionIndex]) {
            e.preventDefault()
            handleVisualSelect(elements[optionIndex].id)
            setLiveAnnouncement(`Selected element ${key}: ${elements[optionIndex].label || key}`)
          }
        }
        return
      }

      // 'H' or 'h': Reveal hint
      if (key === 'h' || key === 'H') {
        if (currentHints.length > 0) {
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

      // Enter or Space: Advance or Submit
      if (key === 'Enter' || key === ' ') {
        if (targetTag === 'button') {
          return
        }
        if (isFinalQuestion) {
          if (isAnyQuestionAnswered && !isSubmitting) {
            e.preventDefault()
            void handleSubmit()
          }
        } else {
          e.preventDefault()
          handleNextQuestion()
        }
        return
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [
    currentQuestion,
    currentHints,
    isFeedbackOpen,
    isSubmitting,
    hintsRevealed,
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

  if (loadError || !activity || questions.length === 0) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-slate-50 dark:bg-slate-950 p-6">
        <div className="max-w-md w-full p-8 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-xl text-center space-y-4">
          <div className="w-14 h-14 mx-auto rounded-2xl bg-amber-50 dark:bg-amber-950/60 border border-amber-200 dark:border-amber-800 flex items-center justify-center text-amber-600">
            <AlertCircle className="w-7 h-7" />
          </div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-white">
            {loadErrorStatus === 404 ? 'Activity Not Found' : 'Unable to Load Activity'}
          </h2>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            {loadError || 'The requested educational activity could not be loaded.'}
          </p>
          <button
            type="button"
            onClick={handleExit}
            className="w-full py-3 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold transition-all focus:outline-none focus:ring-4 focus:ring-indigo-400"
          >
            Return to Dashboard
          </button>
        </div>
      </div>
    )
  }

  const isFinalQuestion = currentQuestionIndex === questions.length - 1

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
                <span
                  className={`inline-flex items-center gap-1 text-[10px] font-semibold px-2 py-0.5 rounded-full ${
                    fallbackUsed
                      ? 'bg-amber-50 text-amber-700 border border-amber-200 dark:bg-amber-950/60 dark:text-amber-300 dark:border-amber-800'
                      : 'bg-violet-50 text-violet-700 border border-violet-200 dark:bg-violet-950/60 dark:text-violet-300 dark:border-violet-800'
                  }`}
                >
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
                {isSpeaking ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
                <span className="hidden sm:inline">{isSpeaking ? 'Pause' : 'Listen'}</span>
              </button>
            )}

            {/* Hint Revelation Button */}
            {currentHints.length > 0 && (
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
        {isHintDrawerOpen && currentHints.length > 0 && (
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
              {currentHints.slice(0, hintsRevealed).map((hint, idx) => (
                <div
                  key={idx}
                  className="flex items-start gap-2.5 text-sm text-amber-950 dark:text-amber-100 bg-white/70 dark:bg-slate-900/60 p-2.5 rounded-xl border border-amber-100 dark:border-amber-900"
                >
                  <span className="font-bold text-amber-600 shrink-0">Step {idx + 1}:</span>
                  <span>{hint}</span>
                </div>
              ))}
              {hintsRevealed < currentHints.length && (
                <button
                  type="button"
                  onClick={handleRevealNextHint}
                  className="mt-1 text-xs font-semibold text-indigo-600 dark:text-indigo-400 hover:underline"
                >
                  Need more help? Show next hint ({hintsRevealed + 1} of {currentHints.length})
                </button>
              )}
            </div>
          </div>
        )}
      </header>

      {/* ── Multi-Question Progress Header ─────────────────────────────────── */}
      <section
        aria-label="Question progression"
        className="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 px-4 py-3 shadow-2xs"
      >
        <div className="max-w-5xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span className="text-sm font-bold text-slate-800 dark:text-slate-200">
              Question {currentQuestionIndex + 1} of {questions.length}
            </span>
            <span className="text-xs text-slate-500 dark:text-slate-400">
              ({answeredQuestionsCount} answered)
            </span>
          </div>

          {/* Interactive Question Step Pills */}
          <div className="flex items-center gap-2 overflow-x-auto py-1">
            {questions.map((q, idx) => {
              const isCurrent = idx === currentQuestionIndex
              const isAnswered = isQuestionAnswered(q.id)
              return (
                <button
                  key={q.id}
                  type="button"
                  onClick={() => handleJumpToQuestion(idx)}
                  aria-label={`Jump to question ${idx + 1}${isAnswered ? ' (Answered)' : ''}`}
                  aria-current={isCurrent ? 'step' : undefined}
                  className={`w-8 h-8 rounded-full text-xs font-bold transition-all flex items-center justify-center focus:outline-none focus:ring-2 focus:ring-indigo-400 ${
                    isCurrent
                      ? 'bg-indigo-600 text-white shadow-sm ring-2 ring-indigo-300 dark:ring-indigo-700'
                      : isAnswered
                      ? 'bg-emerald-100 dark:bg-emerald-950/80 text-emerald-800 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-700'
                      : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700 border border-slate-200 dark:border-slate-700'
                  }`}
                >
                  {isAnswered && !isCurrent ? (
                    <Check className="w-3.5 h-3.5 text-emerald-700 dark:text-emerald-400" />
                  ) : (
                    idx + 1
                  )}
                </button>
              )
            })}
          </div>
        </div>
      </section>

      {/* ── Accessible Live Region ────────────────────────────────────────── */}
      <div role="status" aria-live="polite" aria-atomic="true" className="sr-only">
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

        {/* Current Question Modality Renderer */}
        {currentQuestion && (
          <div className="py-2 animate-in fade-in duration-200" key={currentQuestion.id}>
            {currentQuestion.question_type === 'multiple_choice' && (
              <MultipleChoiceActivity
                content={currentQuestion.content as any}
                selectedOptionId={
                  (answersByQuestionId[currentQuestion.id] as MultipleChoiceSubmission)?.selected_option_id || null
                }
                onSelect={handleOptionSelect}
                disabled={isSubmitting}
              />
            )}

            {currentQuestion.question_type === 'matching' && (
              <MatchingActivity
                content={currentQuestion.content as any}
                pairs={
                  (answersByQuestionId[currentQuestion.id] as MatchingSubmission)?.pairs || []
                }
                onChange={handleMatchingChange}
                disabled={isSubmitting}
              />
            )}

            {currentQuestion.question_type === 'ordering' && (
              <OrderingActivity
                content={currentQuestion.content as any}
                orderedIds={
                  (answersByQuestionId[currentQuestion.id] as OrderingSubmission)?.ordered_ids ||
                  ((currentQuestion.content as any).items || []).map((i: any) => i.id)
                }
                onChange={handleOrderingChange}
                disabled={isSubmitting}
              />
            )}

            {currentQuestion.question_type === 'visual_identification' && (
              <VisualIdentificationActivity
                content={currentQuestion.content as any}
                selectedElementId={
                  (answersByQuestionId[currentQuestion.id] as VisualIdentificationSubmission)?.selected_element_id || null
                }
                onSelect={handleVisualSelect}
                disabled={isSubmitting}
              />
            )}

            {currentQuestion.question_type === 'drag_drop' && (
              <DragDropActivity
                content={currentQuestion.content as any}
                mapping={
                  (answersByQuestionId[currentQuestion.id] as DragDropSubmission)?.item_to_zone_mapping || {}
                }
                onChange={handleDragDropChange}
                disabled={isSubmitting}
              />
            )}
          </div>
        )}
      </main>

      {/* ── Persistent Bottom Navigation Bar ──────────────────────────────── */}
      <footer className="sticky bottom-0 z-30 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md border-t border-slate-200 dark:border-slate-800 p-4 sm:p-5 shadow-lg">
        <div className="max-w-5xl mx-auto flex items-center justify-between gap-4">
          {/* Previous Question Button */}
          <button
            type="button"
            disabled={currentQuestionIndex === 0 || isSubmitting}
            onClick={handlePreviousQuestion}
            className={`flex items-center gap-2 px-5 py-3 rounded-2xl font-semibold text-sm transition-all focus:outline-none focus:ring-4 focus:ring-slate-300 ${
              currentQuestionIndex > 0 && !isSubmitting
                ? 'bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700 cursor-pointer'
                : 'opacity-40 cursor-not-allowed bg-slate-100 dark:bg-slate-800 text-slate-400'
            }`}
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Previous</span>
          </button>

          {/* Action Center: Next or Submit */}
          <div className="flex items-center gap-3">
            {!isFinalQuestion ? (
              <button
                type="button"
                onClick={handleNextQuestion}
                className="flex items-center gap-2 py-3 px-6 rounded-2xl font-bold text-base bg-indigo-600 hover:bg-indigo-700 text-white shadow-md transition-all active:scale-[0.99] focus:outline-none focus:ring-4 focus:ring-indigo-400"
              >
                <span>Next Question</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            ) : (
              <button
                type="button"
                disabled={!isAnyQuestionAnswered || isSubmitting}
                onClick={handleSubmit}
                className={`flex items-center gap-2 py-3.5 px-8 rounded-2xl font-bold text-base sm:text-lg shadow-lg transition-all focus:outline-none focus:ring-4 focus:ring-emerald-400 ${
                  isAnyQuestionAnswered && !isSubmitting
                    ? 'bg-emerald-600 hover:bg-emerald-700 text-white cursor-pointer active:scale-[0.99]'
                    : 'bg-slate-200 dark:bg-slate-800 text-slate-400 dark:text-slate-500 cursor-not-allowed'
                }`}
              >
                {isSubmitting ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    <span>Evaluating...</span>
                  </>
                ) : (
                  <>
                    <Check className="w-5 h-5" />
                    <span>Submit Activity</span>
                  </>
                )}
              </button>
            )}
          </div>
        </div>
      </footer>

      {/* ── Multi-Question Activity Results Modal ─────────────────────────── */}
      {isFeedbackOpen && evaluationResult && (
        <div
          role="dialog"
          aria-modal="true"
          aria-labelledby="feedback-title"
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in duration-200"
        >
          <div className="max-w-xl w-full bg-white dark:bg-slate-900 rounded-3xl p-6 sm:p-8 shadow-2xl border border-slate-200 dark:border-slate-800 space-y-6 max-h-[90vh] overflow-y-auto">
            {/* Header Result Badge */}
            <div className="text-center space-y-2">
              <div
                className={`w-16 h-16 mx-auto rounded-3xl flex items-center justify-center text-3xl shadow-lg ${
                  evaluationResult.is_correct || (evaluationResult.percentage && evaluationResult.percentage >= 80)
                    ? 'bg-emerald-500 text-white'
                    : 'bg-indigo-600 text-white'
                }`}
              >
                {evaluationResult.is_correct || (evaluationResult.percentage && evaluationResult.percentage >= 80)
                  ? '🌟'
                  : '🌱'}
              </div>
              <h2 id="feedback-title" className="text-2xl font-bold text-slate-900 dark:text-white">
                {evaluationResult.is_correct
                  ? 'Activity Complete — Perfect Score!'
                  : 'Activity Complete!'}
              </h2>
              <div className="flex items-center justify-center gap-3">
                <span className="text-xl font-extrabold text-indigo-600 dark:text-indigo-400">
                  {evaluationResult.questions_correct ?? (evaluationResult.is_correct ? questions.length : 0)} /{' '}
                  {evaluationResult.questions_total ?? questions.length} Correct
                </span>
                <span className="text-sm font-bold px-2.5 py-1 rounded-full bg-indigo-50 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800">
                  {evaluationResult.percentage ?? Math.round(evaluationResult.score * 100)}%
                </span>
              </div>
            </div>

            {/* Cognitive Calm Feedback Banner */}
            <div className="p-4 rounded-2xl bg-indigo-50/80 dark:bg-indigo-950/40 border border-indigo-100 dark:border-indigo-900 text-indigo-950 dark:text-indigo-200 text-sm leading-relaxed text-center">
              {evaluationResult.feedback}
            </div>

            {/* Question-by-Question Breakdown */}
            {evaluationResult.question_results && evaluationResult.question_results.length > 0 && (
              <div className="space-y-3">
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                  Question Summary
                </h3>
                <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
                  {evaluationResult.question_results.map((qr) => (
                    <div
                      key={qr.question_id}
                      className="p-3 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/50 flex items-start gap-3"
                    >
                      {qr.is_correct ? (
                        <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
                      ) : (
                        <XCircle className="w-5 h-5 text-rose-500 shrink-0 mt-0.5" />
                      )}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between gap-2">
                          <span className="text-xs font-bold text-slate-800 dark:text-slate-200">
                            Question {qr.question_number}
                          </span>
                          <span
                            className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${
                              qr.is_correct
                                ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300'
                                : 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300'
                            }`}
                          >
                            {qr.is_correct ? 'Correct' : 'Needs Review'}
                          </span>
                        </div>
                        <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">
                          {qr.feedback}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Footer Buttons */}
            <div className="flex items-center gap-3 pt-2">
              <button
                type="button"
                onClick={handleTryAgain}
                className="flex-1 flex items-center justify-center gap-2 py-3 px-4 rounded-xl border border-slate-200 dark:border-slate-700 font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              >
                <RotateCcw className="w-4 h-4" />
                <span>Practice Again</span>
              </button>
              <button
                type="button"
                onClick={handleExit}
                className="flex-1 py-3 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold transition-all shadow-md"
              >
                Done
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
