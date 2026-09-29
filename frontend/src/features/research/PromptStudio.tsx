import React, { useEffect, useState } from 'react'
import type {
  ResearchArtifact,
  ResearchExperiment,
  ResearchModelInfo,
  ResearchOutputTarget,
  ResearchProject,
  ResearchRun,
  ResearchVariant,
} from '@/types'
import { researchApi } from '@/services/researchApi'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import {
  Sparkles,
  Sliders,
  Play,
  RotateCcw,
  CheckCircle2,
  AlertTriangle,
  Clock,
  Eye,
  FileCode,
  ShieldCheck,
  ChevronDown,
  ChevronUp,
} from 'lucide-react'

interface PromptStudioProps {
  project: ResearchProject
  experiment: ResearchExperiment
  variants: ResearchVariant[]
  selectedVariantId?: string
  onVariantChange?: (variantId: string) => void
  onRunCreated?: (run: ResearchRun) => void
  onInspectArtifact?: (artifact: ResearchArtifact) => void
}

const DEFAULT_MODELS: ResearchModelInfo[] = [
  { id: 'gemini-3.8-flash', name: 'Gemini 3.8 Flash', description: 'Primary Research Model', is_default: true },
  { id: 'gemini-3.5-flash-lite', name: 'Gemini 3.5 Flash Lite', description: 'Lightweight & Fast', is_default: false },
  { id: 'gemini-2.5-flash', name: 'Gemini 2.5 Flash', description: 'Stable Legacy', is_default: false },
  { id: 'gemini-2.5-pro', name: 'Gemini 2.5 Pro', description: 'Stable Legacy Reasoning', is_default: false },
]

export const PromptStudio: React.FC<PromptStudioProps> = ({
  project,
  experiment,
  variants,
  selectedVariantId,
  onVariantChange,
  onRunCreated,
  onInspectArtifact,
}) => {
  const [activeVariantId, setActiveVariantId] = useState<string>(
    selectedVariantId || (variants[0]?.id ?? '')
  )

  const [availableModels, setAvailableModels] = useState<ResearchModelInfo[]>(DEFAULT_MODELS)
  const [prompt, setPrompt] = useState(
    'Design an experimental 5-question multi-modal assessment on phonemic awareness. Include sound prompts, visual icon cues, and 3 distinct answer options per question.'
  )
  const [systemPrompt, setSystemPrompt] = useState(
    'You are an AI research sandbox assistant for educational experimentation. Follow the prompt strictly.'
  )
  const [outputTarget, setOutputTarget] = useState<ResearchOutputTarget>('assessment')
  const [model, setModel] = useState('gemini-3.8-flash')
  const [questionCount, setQuestionCount] = useState<number | ''>(5)
  const [temperature, setTemperature] = useState(0.7)
  const [maxTokens, setMaxTokens] = useState(2048)
  const [manualContext, setManualContext] = useState('')
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [productionCompatMode, setProductionCompatMode] = useState(false)
  const [targetProductionSchema, setTargetProductionSchema] = useState('activity')

  const [isGenerating, setIsGenerating] = useState(false)
  const [latestRun, setLatestRun] = useState<ResearchRun | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    researchApi.getModels()
      .then((models) => {
        if (models && models.length > 0) {
          setAvailableModels(models)
        }
      })
      .catch(() => {})
  }, [])

  const handleSelectPreset = (presetPrompt: string, target: ResearchOutputTarget, temp: number) => {
    setPrompt(presetPrompt)
    setOutputTarget(target)
    setTemperature(temp)
  }

  const handleGenerate = async () => {
    if (!activeVariantId) {
      alert('Please select or create an experimental variant first.')
      return
    }
    if (!prompt.trim()) {
      alert('Please enter a research prompt.')
      return
    }

    setIsGenerating(true)
    setError(null)

    try {
      const run = await researchApi.executePromptStudio({
        project_id: project.id,
        experiment_id: experiment.id,
        variant_id: activeVariantId,
        prompt: prompt.trim(),
        system_prompt: systemPrompt.trim() || undefined,
        output_target: outputTarget,
        model,
        model_configuration: {
          temperature,
          max_output_tokens: maxTokens,
        },
        explicit_context: manualContext.trim() ? { manual_context: manualContext.trim() } : null,
        question_count: questionCount ? Number(questionCount) : undefined,
        production_compatibility_mode: productionCompatMode,
        target_production_schema: productionCompatMode ? targetProductionSchema : undefined,
      })

      setLatestRun(run)
      if (onRunCreated) onRunCreated(run)
    } catch (err: any) {
      setError(err.message || 'Generation failed')
    } finally {
      setIsGenerating(false)
    }
  }

  const handleCloneRun = async () => {
    if (!latestRun) return
    try {
      const cloned = await researchApi.cloneRun(latestRun.id, {
        override_model_configuration: { temperature: Math.min(1.0, temperature + 0.2) },
      })
      alert(`Run cloned successfully! Cloned Run ID: ${cloned.id}`)
      if (onRunCreated) onRunCreated(cloned)
    } catch (err: any) {
      alert(`Clone failed: ${err.message}`)
    }
  }

  return (
    <div className="space-y-6">
      {/* Sandbox Isolation Status Banner */}
      <div className="rounded-xl border border-indigo-200 bg-gradient-to-r from-indigo-50/90 to-purple-50/70 p-4 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-indigo-600 text-white shadow-sm">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-slate-900 text-sm">Research Prompt Studio</span>
              <Badge variant="outline" className="bg-indigo-100 text-indigo-800 border-indigo-300 font-semibold text-[11px]">
                SANDBOX ISOLATED
              </Badge>
            </div>
            <p className="text-xs text-slate-600 mt-0.5">
              Experiment freely with custom schemas, question counts, and instructions.
            </p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-1.5 text-[11px] font-mono text-slate-600">
          <span className="px-2 py-0.5 rounded bg-white/80 border border-slate-200">RAG: OFF</span>
          <span className="px-2 py-0.5 rounded bg-white/80 border border-slate-200">Content Bank: OFF</span>
          <span className="px-2 py-0.5 rounded bg-white/80 border border-slate-200">Phase 8: OFF</span>
          <span className="px-2 py-0.5 rounded bg-white/80 border border-slate-200">Adaptive Rules: OFF</span>
        </div>
      </div>

      {/* Main Studio Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Form: Prompt & Settings (7 cols) */}
        <div className="lg:col-span-7 space-y-4">
          <Card className="border-slate-200 shadow-sm">
            <CardHeader className="pb-3 pt-4 px-5">
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-base font-bold text-slate-900">
                    Prompt Definition
                  </CardTitle>
                  <CardDescription className="text-xs">
                    Target Experiment: <span className="font-semibold text-slate-700">{experiment.name}</span>
                  </CardDescription>
                </div>

                {/* Target Variant Selector */}
                <div className="flex items-center gap-2">
                  <span className="text-xs text-slate-500 font-medium">Variant:</span>
                  <select
                    value={activeVariantId}
                    onChange={(e) => {
                      setActiveVariantId(e.target.value)
                      if (onVariantChange) onVariantChange(e.target.value)
                    }}
                    className="h-8 rounded-lg border border-slate-300 text-xs font-medium px-2.5 bg-white text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  >
                    {variants.map((v) => (
                      <option key={v.id} value={v.id}>
                        {v.name}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </CardHeader>

            <CardContent className="space-y-4 px-5 pb-5">
              {/* Preset Shortcuts */}
              <div>
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
                  Quick Presets
                </span>
                <div className="flex flex-wrap gap-1.5 mt-1.5">
                  <button
                    type="button"
                    onClick={() =>
                      handleSelectPreset(
                        'Design a 5-question multi-modal literacy quiz with phonemic cues, image tags, and 3 options.',
                        'assessment',
                        0.3
                      )
                    }
                    className="text-xs px-2.5 py-1 rounded-md border border-slate-200 bg-slate-50 hover:bg-indigo-50 hover:border-indigo-300 transition-colors text-slate-700"
                  >
                    5-Question Multi-Modal
                  </button>
                  <button
                    type="button"
                    onClick={() =>
                      handleSelectPreset(
                        'Generate a worked example for double-digit addition with visual block models and step guidance.',
                        'instructional_content',
                        0.5
                      )
                    }
                    className="text-xs px-2.5 py-1 rounded-md border border-slate-200 bg-slate-50 hover:bg-indigo-50 hover:border-indigo-300 transition-colors text-slate-700"
                  >
                    Worked Math Example
                  </button>
                  <button
                    type="button"
                    onClick={() =>
                      handleSelectPreset(
                        'Draft an experimental 3-week unit progression for spatial reasoning without prerequisites.',
                        'curriculum',
                        0.7
                      )
                    }
                    className="text-xs px-2.5 py-1 rounded-md border border-slate-200 bg-slate-50 hover:bg-indigo-50 hover:border-indigo-300 transition-colors text-slate-700"
                  >
                    Curriculum Prototype
                  </button>
                </div>
              </div>

              {/* Research Prompt Editor */}
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                  Research Prompt <span className="text-rose-500">*</span>
                </label>
                <textarea
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  rows={6}
                  placeholder="Enter your exact generation prompt here..."
                  className="w-full rounded-xl border border-slate-300 p-3 text-sm font-sans text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 font-normal leading-relaxed resize-y"
                />
              </div>

              {/* Output Target & Model Bar */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">
                    Output Target Format
                  </label>
                  <select
                    value={outputTarget}
                    onChange={(e) => setOutputTarget(e.target.value as ResearchOutputTarget)}
                    className="w-full h-9 rounded-lg border border-slate-300 text-xs px-3 bg-white text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 capitalize"
                  >
                    <option value="freeform">Freeform Text / Markdown</option>
                    <option value="assessment">Assessment (Multi-Question)</option>
                    <option value="activity">Practice Activity</option>
                    <option value="instructional_content">Instructional Content / Modeling</option>
                    <option value="question_set">Question Bank Set</option>
                    <option value="curriculum">Curriculum Structure</option>
                    <option value="lesson_plan">Lesson Plan</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">
                    LLM Engine Model
                  </label>
                  <select
                    value={model}
                    onChange={(e) => setModel(e.target.value)}
                    className="w-full h-9 rounded-lg border border-slate-300 text-xs px-3 bg-white text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  >
                    {availableModels.map((m) => (
                      <option key={m.id} value={m.id}>
                        {m.name} ({m.description})
                      </option>
                    ))}
                  </select>
                </div>

                {['assessment', 'question_set', 'activity'].includes(outputTarget) && (
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                      Target Question Count (1–50)
                    </label>
                    <input
                      type="number"
                      min="1"
                      max="50"
                      value={questionCount}
                      onChange={(e) => setQuestionCount(e.target.value ? parseInt(e.target.value) : '')}
                      placeholder="e.g. 5, 10, 20"
                      className="w-full h-9 rounded-lg border border-slate-300 text-xs px-3 bg-white text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>
                )}
              </div>

              {/* Advanced Parameters Toggle */}
              <div className="pt-2 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowAdvanced(!showAdvanced)}
                  className="flex items-center gap-1.5 text-xs font-semibold text-indigo-700 hover:text-indigo-900"
                >
                  <Sliders className="w-3.5 h-3.5" />
                  <span>{showAdvanced ? 'Hide Advanced Configuration' : 'Show Advanced Configuration & Context'}</span>
                  {showAdvanced ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                </button>

                {showAdvanced && (
                  <div className="mt-3 space-y-4 p-4 rounded-xl bg-slate-50 border border-slate-200 animate-in fade-in-50">
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div>
                        <div className="flex justify-between text-xs mb-1">
                          <span className="font-semibold text-slate-700">Temperature</span>
                          <span className="font-mono text-slate-600">{temperature}</span>
                        </div>
                        <input
                          type="range"
                          min="0.0"
                          max="1.0"
                          step="0.05"
                          value={temperature}
                          onChange={(e) => setTemperature(parseFloat(e.target.value))}
                          className="w-full accent-indigo-600"
                        />
                        <span className="text-[10px] text-slate-500">Lower: deterministic | Higher: exploratory</span>
                      </div>

                      <div>
                        <div className="flex justify-between text-xs mb-1">
                          <span className="font-semibold text-slate-700">Max Output Tokens</span>
                          <span className="font-mono text-slate-600">{maxTokens}</span>
                        </div>
                        <select
                          value={maxTokens}
                          onChange={(e) => setMaxTokens(parseInt(e.target.value))}
                          className="w-full h-8 rounded-lg border border-slate-300 text-xs px-2.5 bg-white text-slate-800"
                        >
                          <option value="1024">1,024 Tokens</option>
                          <option value="2048">2,048 Tokens</option>
                          <option value="4096">4,096 Tokens</option>
                          <option value="8192">8,192 Tokens</option>
                        </select>
                      </div>
                    </div>

                    <div>
                      <label className="block text-xs font-semibold text-slate-700 mb-1">
                        Custom Research System Prompt
                      </label>
                      <textarea
                        value={systemPrompt}
                        onChange={(e) => setSystemPrompt(e.target.value)}
                        rows={2}
                        className="w-full rounded-lg border border-slate-300 p-2 text-xs font-mono text-slate-800"
                        placeholder="Optional system instructions..."
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-semibold text-slate-700 mb-1">
                        Explicit Manual Context
                      </label>
                      <textarea
                        value={manualContext}
                        onChange={(e) => setManualContext(e.target.value)}
                        rows={2}
                        className="w-full rounded-lg border border-slate-300 p-2 text-xs text-slate-800"
                        placeholder="Paste research notes, references, or excerpts here (Production RAG is not queried)..."
                      />
                    </div>

                    {/* Production Compatibility Mode Toggle */}
                    <div className="pt-2 border-t border-slate-200 flex items-center justify-between">
                      <div>
                        <div className="flex items-center gap-1.5">
                          <span className="text-xs font-bold text-slate-800">Production Compatibility Validation</span>
                          <Badge variant="outline" className="text-[10px] uppercase font-mono">Optional</Badge>
                        </div>
                        <p className="text-[11px] text-slate-500">
                          Validates payload against production schema without modifying the output.
                        </p>
                      </div>
                      <div className="flex items-center gap-2">
                        <input
                          type="checkbox"
                          id="compatMode"
                          checked={productionCompatMode}
                          onChange={(e) => setProductionCompatMode(e.target.checked)}
                          className="w-4 h-4 rounded text-indigo-600 focus:ring-indigo-500"
                        />
                        <label htmlFor="compatMode" className="text-xs font-medium text-slate-700 cursor-pointer">
                          Enable
                        </label>
                      </div>
                    </div>

                    {productionCompatMode && (
                      <div className="flex items-center justify-between text-xs pt-1">
                        <label className="text-slate-700 font-semibold">Production Schema to Test Against:</label>
                        <select
                          value={targetProductionSchema}
                          onChange={(e) => setTargetProductionSchema(e.target.value)}
                          className="rounded border border-slate-300 p-1 text-xs text-slate-800"
                        >
                          <option value="activity">Activity (Homogeneous)</option>
                          <option value="instructional_content">Instructional Content</option>
                        </select>
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* Generate Button */}
              <div className="pt-2">
                <Button
                  onClick={handleGenerate}
                  disabled={isGenerating || !activeVariantId}
                  className="w-full h-11 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm shadow-md gap-2"
                >
                  {isGenerating ? (
                    <>
                      <RotateCcw className="w-4 h-4 animate-spin" />
                      <span>Generating in Sandbox...</span>
                    </>
                  ) : (
                    <>
                      <Play className="w-4 h-4 fill-white" />
                      <span>Generate in Research Sandbox</span>
                    </>
                  )}
                </Button>
              </div>

              {error && (
                <div className="p-3 rounded-lg bg-rose-50 border border-rose-200 text-xs text-rose-800 flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-rose-600 flex-shrink-0" />
                  <span>{error}</span>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Right Panel: Output & Artifact Viewer (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          <Card className="border-slate-200 shadow-sm h-full flex flex-col">
            <CardHeader className="pb-3 pt-4 px-5 border-b border-slate-100 bg-slate-50/50">
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-base font-bold text-slate-900">
                    Execution Outcome
                  </CardTitle>
                  <CardDescription className="text-xs">
                    {latestRun ? `Run ID: ${latestRun.id.slice(0, 8)}...` : 'Ready for generation'}
                  </CardDescription>
                </div>

                {latestRun && (
                  <div className="flex items-center gap-2">
                    {latestRun.status === 'completed' && (
                      <Badge variant="outline" className="bg-emerald-50 text-emerald-700 border-emerald-300 text-xs gap-1">
                        <CheckCircle2 className="w-3 h-3" /> Completed
                      </Badge>
                    )}
                    {latestRun.status === 'completed_with_parse_warning' && (
                      <Badge variant="outline" className="bg-amber-50 text-amber-700 border-amber-300 text-xs gap-1">
                        <AlertTriangle className="w-3 h-3" /> Parse Warning
                      </Badge>
                    )}
                    {latestRun.status === 'failed' && (
                      <Badge variant="outline" className="bg-rose-50 text-rose-700 border-rose-300 text-xs gap-1">
                        <AlertTriangle className="w-3 h-3" /> Failed
                      </Badge>
                    )}
                  </div>
                )}
              </div>
            </CardHeader>

            <CardContent className="flex-1 p-5 flex flex-col justify-between">
              {latestRun ? (
                <div className="space-y-4 flex-1 flex flex-col">
                  {/* Telemetry Chips */}
                  <div className="flex flex-wrap items-center gap-2 text-xs">
                    <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-mono">
                      Model: {latestRun.model}
                    </span>
                    {latestRun.metadata_info?.execution_time_ms && (
                      <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-mono flex items-center gap-1">
                        <Clock className="w-3 h-3 text-slate-500" />
                        {latestRun.metadata_info.execution_time_ms} ms
                      </span>
                    )}
                    {latestRun.artifact?.is_production_compatible && (
                      <span className="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 text-[11px] font-semibold flex items-center gap-1">
                        <ShieldCheck className="w-3 h-3" /> Production Compatible
                      </span>
                    )}
                  </div>

                  {/* Output Preview Window */}
                  <div className="flex-1 rounded-xl bg-slate-900 text-slate-100 p-4 font-mono text-xs overflow-y-auto max-h-[380px] shadow-inner leading-relaxed">
                    <pre className="whitespace-pre-wrap text-emerald-400">
                      {latestRun.normalized_output
                        ? JSON.stringify(latestRun.normalized_output, null, 2)
                        : latestRun.raw_output || '// No output received.'}
                    </pre>
                  </div>

                  {/* Run Actions */}
                  <div className="flex items-center gap-2 pt-2 border-t border-slate-100">
                    {latestRun.artifact && onInspectArtifact && (
                      <Button
                        variant="default"
                        size="sm"
                        onClick={() => onInspectArtifact(latestRun.artifact!)}
                        className="flex-1 text-xs h-8 gap-1 bg-indigo-600 hover:bg-indigo-700"
                      >
                        <Eye className="w-3.5 h-3.5" /> Inspect Full Artifact
                      </Button>
                    )}
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={handleCloneRun}
                      className="text-xs h-8 gap-1"
                    >
                      <RotateCcw className="w-3.5 h-3.5" /> Clone / Re-run
                    </Button>
                  </div>
                </div>
              ) : (
                <div className="flex-1 flex flex-col items-center justify-center p-8 text-center text-slate-400">
                  <div className="p-4 rounded-full bg-slate-100 mb-3">
                    <FileCode className="w-8 h-8 text-slate-400" />
                  </div>
                  <h4 className="font-semibold text-slate-700 text-sm">No Active Run Yet</h4>
                  <p className="text-xs text-slate-500 max-w-[260px] mt-1">
                    Select your variant, adjust parameters, and click "Generate in Research Sandbox" to produce an artifact.
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
