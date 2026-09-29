import React, { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import {
  BookOpen,
  Sparkles,
  Loader2,
  CheckCircle2,
  AlertCircle,
  Edit3,
  Save,
  Check,
  Send,
  Layers,
  Volume2,
  VolumeX,
  ArrowRight,
  Info,
} from 'lucide-react'
import { api } from '@/services/api'
import { useSpeechSynthesis } from '@/hooks/useSpeechSynthesis'
import type {
  ExplanationMethod,
  InstructionalBlock,
  InstructionalContent,
} from '@/types'

interface LocalizedText {
  en?: string
  ar?: string
  [key: string]: string | undefined
}

interface ObjectiveItem {
  id: string
  title: LocalizedText | string
  description?: LocalizedText | string
  difficulty_level?: number
}

interface LessonItem {
  id: string
  title: LocalizedText | string
  learning_objectives: ObjectiveItem[]
}

interface UnitItem {
  id: string
  title: LocalizedText | string
  lessons: LessonItem[]
}

interface SubjectItem {
  id: string
  title: LocalizedText | string
  units: UnitItem[]
}

interface CurriculumItem {
  id: string
  title: LocalizedText | string
  subjects?: SubjectItem[]
}

const EXPLANATION_METHODS: Array<{
  value: ExplanationMethod
  label: string
  shortDesc: string
  badge: string
  icon: string
}> = [
  {
    value: 'visual_explanation',
    label: 'Visual Explanation',
    shortDesc: 'Uses concrete spatial arrangements and high-contrast visual cues to illustrate ideas.',
    badge: 'Concrete & Visual',
    icon: '👁️',
  },
  {
    value: 'step_by_step',
    label: 'Step-by-Step (Task Analysis)',
    shortDesc: 'Breaks complex concepts down into 2–4 sequential, digestible learning steps.',
    badge: 'Sequential Scaffolding',
    icon: '🚶',
  },
  {
    value: 'worked_example',
    label: 'Worked Example',
    shortDesc: 'Models the entire problem scenario and thought process from start to finish.',
    badge: 'Cognitive Modeling',
    icon: '📝',
  },
  {
    value: 'text_explanation',
    label: 'Simple Text Explanation',
    shortDesc: 'Clear, gentle narrative definitions using accessible and familiar vocabulary.',
    badge: 'Calm & Concise',
    icon: '📖',
  },
]

export const TeacherInstructionalContent: React.FC = () => {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const preselectedObjectiveId = searchParams.get('objective_id')

  // Curriculum Hierarchy State
  const [subjects, setSubjects] = useState<SubjectItem[]>([])
  const [selectedSubjectId, setSelectedSubjectId] = useState<string>('')
  const [selectedUnitId, setSelectedUnitId] = useState<string>('')
  const [selectedLessonId, setSelectedLessonId] = useState<string>('')
  const [selectedObjectiveId, setSelectedObjectiveId] = useState<string>(preselectedObjectiveId || '')

  const [loadingCurriculum, setLoadingCurriculum] = useState<boolean>(true)

  // Generation brief state
  const [method, setMethod] = useState<ExplanationMethod>('step_by_step')
  const [difficulty, setDifficulty] = useState<number>(2)
  const [language, setLanguage] = useState<string>('en')
  const [teacherInstructions, setTeacherInstructions] = useState<string>('')

  // Content state
  const [isGenerating, setIsGenerating] = useState<boolean>(false)
  const [generatedContent, setGeneratedContent] = useState<InstructionalContent | null>(null)
  const [editMode, setEditMode] = useState<boolean>(false)
  const [editedTitle, setEditedTitle] = useState<string>('')
  const [editedSummary, setEditedSummary] = useState<string>('')
  const [editedBlocks, setEditedBlocks] = useState<InstructionalBlock[]>([])
  const [editedNotes, setEditedNotes] = useState<string>('')

  // UI status state
  const [isSaving, setIsSaving] = useState<boolean>(false)
  const [isApproving, setIsApproving] = useState<boolean>(false)
  const [isPublishing, setIsPublishing] = useState<boolean>(false)
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null)

  // Speech preview
  const { speak, cancel, isSpeaking, isSupported } = useSpeechSynthesis()

  const getText = (textObj: LocalizedText | string | undefined, lang: string = 'en'): string => {
    if (!textObj) return ''
    if (typeof textObj === 'string') return textObj
    return textObj[lang] || textObj['en'] || Object.values(textObj)[0] || ''
  }

  // Load curriculum hierarchy
  useEffect(() => {
    async function loadData() {
      setLoadingCurriculum(true)
      try {
        const currs = await api.get<CurriculumItem[]>('/curricula')
        if (currs.length > 0) {
          const full = await api.get<CurriculumItem>(`/curricula/${currs[0].id}`)
          const subs = full.subjects || []
          setSubjects(subs)
          if (subs.length > 0) {
            setSelectedSubjectId(subs[0].id)
            if (subs[0].units && subs[0].units.length > 0) {
              setSelectedUnitId(subs[0].units[0].id)
              if (subs[0].units[0].lessons && subs[0].units[0].lessons.length > 0) {
                setSelectedLessonId(subs[0].units[0].lessons[0].id)
                if (
                  !preselectedObjectiveId &&
                  subs[0].units[0].lessons[0].learning_objectives &&
                  subs[0].units[0].lessons[0].learning_objectives.length > 0
                ) {
                  setSelectedObjectiveId(subs[0].units[0].lessons[0].learning_objectives[0].id)
                }
              }
            }
          }
        }
      } catch (err) {
        console.error('Failed to load curricula:', err)
      } finally {
        setLoadingCurriculum(false)
      }
    }
    loadData()
  }, [preselectedObjectiveId])

  // Derive cascaded lists
  const currentSubject = subjects.find((s) => s.id === selectedSubjectId)
  const units = currentSubject?.units || []
  const currentUnit = units.find((u) => u.id === selectedUnitId)
  const lessons = currentUnit?.lessons || []
  const currentLesson = lessons.find((l) => l.id === selectedLessonId)
  const objectives = currentLesson?.learning_objectives || []

  // Load existing content for selected objective if present
  useEffect(() => {
    if (!selectedObjectiveId) return
    let active = true

    async function checkExisting() {
      try {
        const list = await api.instructional.getByObjective(selectedObjectiveId, false)
        if (active && list.length > 0) {
          const item = list[0]
          setGeneratedContent(item)
          setEditedTitle(item.title)
          setEditedSummary(item.summary)
          setEditedBlocks(item.blocks)
          setEditedNotes(item.teacher_notes || '')
          setMethod(item.explanation_method)
          setDifficulty(item.difficulty_level)
        }
      } catch (err) {
        // Silent
      }
    }
    checkExisting()
    return () => {
      active = false
    }
  }, [selectedObjectiveId])

  const handleSubjectChange = (sId: string) => {
    setSelectedSubjectId(sId)
    const s = subjects.find((sub) => sub.id === sId)
    const firstU = s?.units?.[0]
    setSelectedUnitId(firstU?.id || '')
    const firstL = firstU?.lessons?.[0]
    setSelectedLessonId(firstL?.id || '')
    const firstO = firstL?.learning_objectives?.[0]
    setSelectedObjectiveId(firstO?.id || '')
  }

  const handleUnitChange = (uId: string) => {
    setSelectedUnitId(uId)
    const u = units.find((unit) => unit.id === uId)
    const firstL = u?.lessons?.[0]
    setSelectedLessonId(firstL?.id || '')
    const firstO = firstL?.learning_objectives?.[0]
    setSelectedObjectiveId(firstO?.id || '')
  }

  const handleLessonChange = (lId: string) => {
    setSelectedLessonId(lId)
    const l = lessons.find((les) => les.id === lId)
    const firstO = l?.learning_objectives?.[0]
    setSelectedObjectiveId(firstO?.id || '')
  }

  const handleGenerate = async () => {
    if (!selectedObjectiveId) {
      setMessage({ type: 'error', text: 'Please select a learning objective first.' })
      return
    }

    setIsGenerating(true)
    setMessage(null)
    cancel()

    try {
      const res = await api.instructional.generate({
        objective_id: selectedObjectiveId,
        explanation_method: method,
        difficulty_level: difficulty,
        language,
        teacher_instructions: teacherInstructions.trim() || null,
      })

      setGeneratedContent(res.content)
      setEditedTitle(res.content.title)
      setEditedSummary(res.content.summary)
      setEditedBlocks(res.content.blocks)
      setEditedNotes(res.content.teacher_notes || '')
      setEditMode(false)
      setMessage({
        type: 'success',
        text: `Instructional content generated successfully (${
          res.fallback_used ? 'Deterministic Fallback' : `AI: ${res.generation_source}`
        }). Review required before publication.`,
      })
    } catch (err: any) {
      setMessage({
        type: 'error',
        text: err?.message || 'Failed to generate instructional content. Please try again.',
      })
    } finally {
      setIsGenerating(false)
    }
  }

  const handleSaveEdits = async () => {
    if (!generatedContent) return
    setIsSaving(true)
    setMessage(null)

    try {
      const updated = await api.instructional.update(generatedContent.id, {
        title: editedTitle,
        summary: editedSummary,
        blocks: editedBlocks,
        teacher_notes: editedNotes,
      })
      setGeneratedContent(updated)
      setEditMode(false)
      setMessage({ type: 'success', text: 'Teacher edits saved successfully.' })
    } catch (err: any) {
      setMessage({ type: 'error', text: err?.message || 'Failed to save changes.' })
    } finally {
      setIsSaving(false)
    }
  }

  const handleApprove = async () => {
    if (!generatedContent) return
    setIsApproving(true)
    setMessage(null)

    try {
      const approved = await api.instructional.approve(generatedContent.id)
      setGeneratedContent(approved)
      setMessage({
        type: 'success',
        text: 'Content marked as Approved! It can now be published for learners.',
      })
    } catch (err: any) {
      setMessage({ type: 'error', text: err?.message || 'Approval failed.' })
    } finally {
      setIsApproving(false)
    }
  }

  const handlePublish = async () => {
    if (!generatedContent) return
    setIsPublishing(true)
    setMessage(null)

    try {
      const pub = await api.instructional.publish(generatedContent.id)
      setGeneratedContent(pub)
      setMessage({
        type: 'success',
        text: 'Content published! It is now live and visible to learners.',
      })
    } catch (err: any) {
      setMessage({ type: 'error', text: err?.message || 'Publication failed.' })
    } finally {
      setIsPublishing(false)
    }
  }

  const handleBlockChange = (index: number, field: keyof InstructionalBlock, value: any) => {
    setEditedBlocks((prev) => {
      const next = [...prev]
      next[index] = { ...next[index], [field]: value }
      return next
    })
  }

  const handlePlayAudioPreview = () => {
    if (isSpeaking) {
      cancel()
      return
    }
    const blocksToSpeak = editMode ? editedBlocks : (generatedContent?.blocks || [])
    const text = blocksToSpeak
      .map((b) => `${b.title ? b.title + '. ' : ''}${b.body}`)
      .join(' ')
    speak(text)
  }

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 p-4 sm:p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-6 border-b border-slate-200 dark:border-slate-800">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-indigo-100 text-indigo-800 dark:bg-indigo-950 dark:text-indigo-300">
                Teacher Studio
              </span>
              <span className="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-violet-100 text-violet-800 dark:bg-violet-950 dark:text-violet-300">
                Instructional Modeling
              </span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white mt-2">
              Instructional Content & Explanations
            </h1>
            <p className="text-sm text-slate-600 dark:text-slate-400 mt-1 max-w-2xl">
              Create and review structured, non-evaluative conceptual explanations and modeling.
              Learners consume these before practicing with activities.
            </p>
          </div>
          <button
            type="button"
            onClick={() => navigate('/dashboard')}
            className="px-4 py-2 text-sm font-semibold rounded-xl border border-slate-200 dark:border-slate-800 hover:bg-slate-100 dark:hover:bg-slate-900 transition-colors"
          >
            Back to Dashboard
          </button>
        </div>

        {/* Global Alert Notification */}
        {message && (
          <div
            className={`p-4 rounded-2xl flex items-center gap-3 text-sm font-medium ${
              message.type === 'success'
                ? 'bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800 text-emerald-800 dark:text-emerald-200'
                : 'bg-rose-50 dark:bg-rose-950/60 border border-rose-200 dark:border-rose-800 text-rose-800 dark:text-rose-200'
            }`}
          >
            {message.type === 'success' ? (
              <CheckCircle2 className="w-5 h-5 shrink-0 text-emerald-600" />
            ) : (
              <AlertCircle className="w-5 h-5 shrink-0 text-rose-600" />
            )}
            <span>{message.text}</span>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* ── Left Column: Configuration Brief ────────────────────────────── */}
          <div className="lg:col-span-5 space-y-6">
            <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-5">
              <h2 className="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-indigo-600" />
                <span>1. Curriculum Selection</span>
              </h2>

              {loadingCurriculum ? (
                <div className="flex items-center justify-center p-6 text-sm text-slate-500">
                  <Loader2 className="w-5 h-5 animate-spin mr-2" />
                  Loading curriculum structure...
                </div>
              ) : (
                <div className="space-y-4">
                  {/* Subject */}
                  <div>
                    <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-1.5">
                      Subject
                    </label>
                    <select
                      value={selectedSubjectId}
                      onChange={(e) => handleSubjectChange(e.target.value)}
                      className="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800 text-sm font-medium focus:ring-2 focus:ring-indigo-500 outline-none"
                    >
                      {subjects.map((s) => (
                        <option key={s.id} value={s.id}>
                          {getText(s.title)}
                        </option>
                      ))}
                    </select>
                  </div>

                  {/* Unit */}
                  <div>
                    <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-1.5">
                      Unit
                    </label>
                    <select
                      value={selectedUnitId}
                      onChange={(e) => handleUnitChange(e.target.value)}
                      className="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800 text-sm font-medium focus:ring-2 focus:ring-indigo-500 outline-none"
                    >
                      {units.map((u) => (
                        <option key={u.id} value={u.id}>
                          {getText(u.title)}
                        </option>
                      ))}
                    </select>
                  </div>

                  {/* Lesson */}
                  <div>
                    <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-1.5">
                      Lesson
                    </label>
                    <select
                      value={selectedLessonId}
                      onChange={(e) => handleLessonChange(e.target.value)}
                      className="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800 text-sm font-medium focus:ring-2 focus:ring-indigo-500 outline-none"
                    >
                      {lessons.map((l) => (
                        <option key={l.id} value={l.id}>
                          {getText(l.title)}
                        </option>
                      ))}
                    </select>
                  </div>

                  {/* Learning Objective */}
                  <div>
                    <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-1.5">
                      Learning Objective
                    </label>
                    <select
                      value={selectedObjectiveId}
                      onChange={(e) => setSelectedObjectiveId(e.target.value)}
                      className="w-full p-2.5 rounded-xl border border-indigo-200 dark:border-indigo-800 bg-indigo-50/50 dark:bg-indigo-950/30 text-sm font-semibold text-indigo-950 dark:text-indigo-200 focus:ring-2 focus:ring-indigo-500 outline-none"
                    >
                      {objectives.map((o) => (
                        <option key={o.id} value={o.id}>
                          {getText(o.title)} (Lvl {o.difficulty_level || 1})
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
              )}
            </div>

            {/* Explanation Method Selection */}
            <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
              <h2 className="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <Layers className="w-5 h-5 text-indigo-600" />
                <span>2. Explanation Method</span>
              </h2>

              <div className="space-y-2.5">
                {EXPLANATION_METHODS.map((m) => {
                  const isSelected = method === m.value
                  return (
                    <button
                      key={m.value}
                      type="button"
                      onClick={() => setMethod(m.value)}
                      className={`w-full p-3.5 rounded-2xl text-left border transition-all flex items-start gap-3 ${
                        isSelected
                          ? 'bg-indigo-50/90 dark:bg-indigo-950/60 border-indigo-400 dark:border-indigo-600 ring-2 ring-indigo-200 dark:ring-indigo-800'
                          : 'bg-slate-50/70 dark:bg-slate-800/40 border-slate-200 dark:border-slate-800 hover:bg-slate-100 dark:hover:bg-slate-800'
                      }`}
                    >
                      <span className="text-2xl mt-0.5">{m.icon}</span>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between gap-2">
                          <span className="text-sm font-bold text-slate-900 dark:text-white">
                            {m.label}
                          </span>
                          <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300">
                            {m.badge}
                          </span>
                        </div>
                        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                          {m.shortDesc}
                        </p>
                      </div>
                    </button>
                  )
                })}
              </div>

              {/* Extra Parameters */}
              <div className="grid grid-cols-2 gap-4 pt-2">
                <div>
                  <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-1">
                    Difficulty Level
                  </label>
                  <select
                    value={difficulty}
                    onChange={(e) => setDifficulty(Number(e.target.value))}
                    className="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800 text-sm font-medium"
                  >
                    <option value={1}>Level 1 (Foundational)</option>
                    <option value={2}>Level 2 (Standard)</option>
                    <option value={3}>Level 3 (Intermediate)</option>
                    <option value={4}>Level 4 (Advanced)</option>
                    <option value={5}>Level 5 (Mastery)</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-1">
                    Language
                  </label>
                  <select
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    className="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800 text-sm font-medium"
                  >
                    <option value="en">English (en)</option>
                    <option value="ar">Arabic (ar)</option>
                  </select>
                </div>
              </div>

              {/* Teacher Guidance / Prompt Notes */}
              <div>
                <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-1">
                  Teacher Guidance (Optional)
                </label>
                <textarea
                  value={teacherInstructions}
                  onChange={(e) => setTeacherInstructions(e.target.value)}
                  placeholder="e.g. Focus on counting stars and apples, keep sentences under 8 words."
                  rows={2}
                  className="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800 text-sm font-medium outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              {/* Generate Button */}
              <button
                type="button"
                disabled={isGenerating || !selectedObjectiveId}
                onClick={handleGenerate}
                className="w-full py-3.5 px-6 rounded-2xl bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-bold text-base shadow-lg transition-all flex items-center justify-center gap-2 cursor-pointer"
              >
                {isGenerating ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    <span>Generating with Pedagogical Grounding...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5" />
                    <span>Generate Structured Explanation</span>
                  </>
                )}
              </button>
            </div>
          </div>

          {/* ── Right Column: Content Review, Editing & Approval ────────────── */}
          <div className="lg:col-span-7 space-y-6">
            {generatedContent ? (
              <div className="p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-6">
                {/* Content Header & Status */}
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 pb-4 border-b border-slate-200 dark:border-slate-800">
                  <div className="flex items-center gap-2">
                    <span
                      className={`text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider ${
                        generatedContent.status === 'published'
                          ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-700'
                          : generatedContent.status === 'approved'
                          ? 'bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-300 border border-blue-300 dark:border-blue-700'
                          : generatedContent.status === 'review_required'
                          ? 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 border border-amber-300 dark:border-amber-700'
                          : 'bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-300'
                      }`}
                    >
                      Status: {generatedContent.status.replace('_', ' ')}
                    </span>
                    <span className="text-xs text-slate-500 font-medium">
                      Method: {generatedContent.explanation_method}
                    </span>
                  </div>

                  {/* Top Action Buttons */}
                  <div className="flex items-center gap-2">
                    {isSupported && (
                      <button
                        type="button"
                        onClick={handlePlayAudioPreview}
                        aria-label="Preview speech"
                        className="p-2 rounded-xl border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                      >
                        {isSpeaking ? (
                          <VolumeX className="w-4 h-4 text-indigo-600 animate-pulse" />
                        ) : (
                          <Volume2 className="w-4 h-4" />
                        )}
                      </button>
                    )}
                    <button
                      type="button"
                      onClick={() => setEditMode(!editMode)}
                      className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-700 text-xs font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800"
                    >
                      <Edit3 className="w-3.5 h-3.5" />
                      <span>{editMode ? 'View Mode' : 'Edit Mode'}</span>
                    </button>
                  </div>
                </div>

                {/* Title & Summary */}
                {editMode ? (
                  <div className="space-y-3">
                    <div>
                      <label className="block text-xs font-bold text-slate-600 dark:text-slate-400 mb-1">
                        Title
                      </label>
                      <input
                        type="text"
                        value={editedTitle}
                        onChange={(e) => setEditedTitle(e.target.value)}
                        className="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800 text-base font-bold"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-bold text-slate-600 dark:text-slate-400 mb-1">
                        Summary
                      </label>
                      <textarea
                        value={editedSummary}
                        onChange={(e) => setEditedSummary(e.target.value)}
                        rows={2}
                        className="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800 text-sm font-medium"
                      />
                    </div>
                  </div>
                ) : (
                  <div>
                    <h3 className="text-xl font-extrabold text-slate-900 dark:text-white">
                      {generatedContent.title}
                    </h3>
                    <p className="text-sm text-slate-600 dark:text-slate-400 mt-1 italic">
                      "{generatedContent.summary}"
                    </p>
                  </div>
                )}

                {/* Blocks Display / Editing */}
                <div className="space-y-4">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
                    Instructional Blocks ({editMode ? editedBlocks.length : generatedContent.blocks.length})
                  </h4>

                  {(editMode ? editedBlocks : generatedContent.blocks).map((block, idx) => (
                    <div
                      key={block.id || idx}
                      className="p-4 rounded-2xl border border-slate-200 dark:border-slate-800 bg-slate-50/60 dark:bg-slate-800/40 space-y-3"
                    >
                      <div className="flex items-center justify-between gap-2">
                        <span className="text-xs font-bold px-2 py-0.5 rounded-md bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300">
                          {block.block_type.toUpperCase()}
                        </span>
                        <span className="text-xs text-slate-400 font-mono">#{idx + 1}</span>
                      </div>

                      {editMode ? (
                        <div className="space-y-2">
                          <input
                            type="text"
                            value={block.title || ''}
                            onChange={(e) => handleBlockChange(idx, 'title', e.target.value)}
                            placeholder="Block Title (optional)"
                            className="w-full p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-sm font-semibold"
                          />
                          <textarea
                            value={block.body}
                            onChange={(e) => handleBlockChange(idx, 'body', e.target.value)}
                            rows={3}
                            placeholder="Block explanation body text"
                            className="w-full p-2 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-sm font-medium"
                          />
                          <div className="flex items-center gap-2">
                            <span className="text-xs text-slate-500">Visual Cue:</span>
                            <input
                              type="text"
                              value={block.visual_cue || ''}
                              onChange={(e) => handleBlockChange(idx, 'visual_cue', e.target.value)}
                              placeholder="🌟 or shape"
                              className="w-24 p-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-sm"
                            />
                          </div>
                        </div>
                      ) : (
                        <div className="space-y-2">
                          {block.title && (
                            <div className="flex items-center gap-2 font-bold text-base text-slate-900 dark:text-white">
                              {block.visual_cue && <span className="text-xl">{block.visual_cue}</span>}
                              <span>{block.title}</span>
                            </div>
                          )}
                          <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed whitespace-pre-line">
                            {block.body}
                          </p>
                        </div>
                      )}
                    </div>
                  ))}
                </div>

                {/* Review & Publish Action Bar */}
                <div className="pt-4 border-t border-slate-200 dark:border-slate-800 flex flex-wrap items-center justify-between gap-3">
                  {editMode ? (
                    <button
                      type="button"
                      disabled={isSaving}
                      onClick={handleSaveEdits}
                      className="py-2.5 px-5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm flex items-center gap-2 shadow-sm"
                    >
                      {isSaving ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
                      <span>Save Teacher Edits</span>
                    </button>
                  ) : (
                    <div className="flex items-center gap-2 text-xs text-slate-500">
                      <Info className="w-4 h-4 text-indigo-500" />
                      <span>Review content carefully before learner approval.</span>
                    </div>
                  )}

                  <div className="flex items-center gap-3">
                    {/* Approve button */}
                    <button
                      type="button"
                      disabled={isApproving || generatedContent.status === 'approved' || generatedContent.status === 'published'}
                      onClick={handleApprove}
                      className="py-2.5 px-4 rounded-xl border border-blue-300 dark:border-blue-700 bg-blue-50 dark:bg-blue-950 text-blue-800 dark:text-blue-200 hover:bg-blue-100 dark:hover:bg-blue-900 disabled:opacity-50 text-sm font-semibold flex items-center gap-2"
                    >
                      {isApproving ? <Loader2 className="w-4 h-4 animate-spin" /> : <Check className="w-4 h-4" />}
                      <span>Approve</span>
                    </button>

                    {/* Publish button */}
                    <button
                      type="button"
                      disabled={isPublishing || generatedContent.status === 'published'}
                      onClick={handlePublish}
                      className="py-2.5 px-5 rounded-xl bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white font-bold text-sm flex items-center gap-2 shadow-sm"
                    >
                      {isPublishing ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                      <span>Publish for Learners</span>
                    </button>
                  </div>
                </div>

                {/* Learner View Shortcut Link */}
                <div className="p-3.5 rounded-2xl bg-slate-100 dark:bg-slate-800/60 flex items-center justify-between text-xs text-slate-600 dark:text-slate-300">
                  <span>Want to see how learners experience this?</span>
                  <button
                    type="button"
                    onClick={() => navigate(`/learn/objective/${selectedObjectiveId}/content`)}
                    className="font-bold text-indigo-600 dark:text-indigo-400 hover:underline flex items-center gap-1"
                  >
                    <span>Open Learner View</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            ) : (
              <div className="p-12 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm text-center space-y-3">
                <div className="w-12 h-12 mx-auto rounded-2xl bg-indigo-50 dark:bg-indigo-950/60 flex items-center justify-center text-indigo-600">
                  <Sparkles className="w-6 h-6" />
                </div>
                <h3 className="text-lg font-bold text-slate-800 dark:text-slate-200">
                  No Content Generated Yet
                </h3>
                <p className="text-sm text-slate-500 max-w-sm mx-auto">
                  Select an objective and explanation method on the left, then click{' '}
                  <span className="font-semibold text-indigo-600">Generate Structured Explanation</span>.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
