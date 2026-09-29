import React, { useState, useEffect } from 'react'
import type {
  ExperimentComparisonResponse,
  ResearchArtifact,
  ResearchExperiment,
} from '@/types'
import { researchApi } from '@/services/researchApi'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import {
  Columns3,
  RotateCcw,
  Star,
  Plus,
  Eye,
} from 'lucide-react'

interface ComparisonViewProps {
  experiment: ResearchExperiment
  onInspectArtifact?: (artifact: ResearchArtifact) => void
}

export const ComparisonView: React.FC<ComparisonViewProps> = ({
  experiment,
  onInspectArtifact,
}) => {
  const [data, setData] = useState<ExperimentComparisonResponse | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Evaluation modal / inline scoring state
  const [evaluatingArtifactId, setEvaluatingArtifactId] = useState<string | null>(null)
  const [metricName, setMetricName] = useState('Instructional Clarity')
  const [score, setScore] = useState(4)
  const [notes, setNotes] = useState('')
  const [isSubmittingEval, setIsSubmittingEval] = useState(false)

  const loadComparison = async () => {
    setIsLoading(true)
    setError(null)
    try {
      const res = await researchApi.getComparison(experiment.id)
      setData(res)
    } catch (err: any) {
      setError(err.message || 'Failed to load comparison data')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    loadComparison()
  }, [experiment.id])

  const handleAddEvaluation = async (artifactId: string) => {
    setIsSubmittingEval(true)
    try {
      await researchApi.createEvaluation(artifactId, {
        metric_name: metricName,
        value: { score, max: 5 },
        notes: notes.trim() || undefined,
        evaluator_type: 'manual',
      })
      setEvaluatingArtifactId(null)
      setNotes('')
      await loadComparison()
    } catch (err: any) {
      alert(`Evaluation failed: ${err.message}`)
    } finally {
      setIsSubmittingEval(false)
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-12 text-slate-500">
        <RotateCcw className="w-5 h-5 animate-spin mr-2" />
        <span>Loading comparative evidence matrix...</span>
      </div>
    )
  }

  if (error || !data) {
    return (
      <div className="p-6 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-sm">
        <p className="font-semibold">Unable to load comparison view</p>
        <p className="text-xs mt-1">{error}</p>
        <Button variant="outline" size="sm" onClick={loadComparison} className="mt-3 text-xs">
          Retry
        </Button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header bar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
        <div>
          <div className="flex items-center gap-2">
            <Columns3 className="w-5 h-5 text-indigo-600" />
            <h3 className="font-bold text-slate-900 text-base">
              Variant Comparative Analysis
            </h3>
            <Badge variant="outline" className="text-xs">
              {data.variants.length} Variants
            </Badge>
          </div>
          <p className="text-xs text-slate-500 mt-0.5">
            Side-by-side evidence inspection without automated ranking.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={loadComparison} className="text-xs gap-1">
            <RotateCcw className="w-3.5 h-3.5" /> Refresh
          </Button>
        </div>
      </div>

      {/* Side-by-Side Comparison Columns */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 items-start">
        {data.variants.map((item, idx) => {
          const { variant, latest_run, artifact, evaluations } = item
          return (
            <Card key={variant.id} className="border-slate-200 shadow-sm flex flex-col h-full bg-white">
              <CardHeader className="pb-3 pt-4 px-4 bg-slate-50/70 border-b border-slate-100 rounded-t-xl">
                <div className="flex items-center justify-between">
                  <Badge variant="outline" className="bg-indigo-100 text-indigo-800 border-indigo-200 font-bold text-xs">
                    Variant {String.fromCharCode(65 + idx)}
                  </Badge>
                  {variant.parent_variant_id && (
                    <span className="text-[10px] text-slate-400 font-mono">
                      (Clone Lineage)
                    </span>
                  )}
                </div>
                <CardTitle className="text-sm font-bold text-slate-900 mt-1">
                  {variant.name}
                </CardTitle>
                <CardDescription className="text-xs line-clamp-2">
                  {variant.description || 'No description provided.'}
                </CardDescription>
              </CardHeader>

              <CardContent className="p-4 flex-1 space-y-4 text-xs">
                {/* Configuration Variables */}
                <div>
                  <span className="font-bold uppercase tracking-wider text-slate-400 text-[10px]">
                    Treatment Variables
                  </span>
                  <div className="mt-1.5 p-2.5 rounded-lg bg-slate-50 border border-slate-200 font-mono text-[11px] space-y-1">
                    {Object.entries(variant.configuration).map(([k, v]) => (
                      <div key={k} className="flex justify-between">
                        <span className="text-slate-500">{k}:</span>
                        <span className="font-bold text-slate-800">{String(v)}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Latest Run & Prompt */}
                <div>
                  <span className="font-bold uppercase tracking-wider text-slate-400 text-[10px]">
                    Latest Execution Run
                  </span>
                  {latest_run ? (
                    <div className="mt-1.5 p-2.5 rounded-lg border border-slate-200 space-y-2">
                      <div className="flex items-center justify-between text-[11px]">
                        <span className="font-mono text-slate-500">Model: {latest_run.model}</span>
                        {latest_run.status === 'completed' ? (
                          <Badge variant="outline" className="text-[10px] bg-emerald-50 text-emerald-700">
                            Completed
                          </Badge>
                        ) : (
                          <Badge variant="outline" className="text-[10px] bg-amber-50 text-amber-700">
                            {latest_run.status}
                          </Badge>
                        )}
                      </div>
                      <div className="text-slate-700 bg-slate-50 p-2 rounded text-[11px] line-clamp-3">
                        <span className="font-semibold text-slate-500 block mb-0.5">Prompt:</span>
                        {latest_run.user_prompt}
                      </div>
                    </div>
                  ) : (
                    <p className="mt-1 text-slate-400 italic">No runs executed yet.</p>
                  )}
                </div>

                {/* Artifact Summary */}
                <div>
                  <span className="font-bold uppercase tracking-wider text-slate-400 text-[10px]">
                    Generated Artifact
                  </span>
                  {artifact ? (
                    <div className="mt-1.5 p-2.5 rounded-lg border border-indigo-100 bg-indigo-50/30 space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-slate-800 capitalize">
                          {artifact.artifact_type}
                        </span>
                        {artifact.is_production_compatible && (
                          <Badge variant="outline" className="text-[10px] bg-emerald-100 text-emerald-800">
                            Compatible
                          </Badge>
                        )}
                      </div>
                      <pre className="p-2 bg-slate-900 text-slate-100 rounded text-[10px] font-mono max-h-32 overflow-y-auto">
                        {JSON.stringify(artifact.payload, null, 2)}
                      </pre>
                      {onInspectArtifact && (
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => onInspectArtifact(artifact)}
                          className="w-full text-xs h-7 gap-1 mt-1"
                        >
                          <Eye className="w-3 h-3" /> Inspect Artifact
                        </Button>
                      )}
                    </div>
                  ) : (
                    <p className="mt-1 text-slate-400 italic">No artifact produced.</p>
                  )}
                </div>

                {/* Evaluations & Metrics */}
                <div>
                  <div className="flex items-center justify-between">
                    <span className="font-bold uppercase tracking-wider text-slate-400 text-[10px]">
                      Evaluations ({evaluations?.length || 0})
                    </span>
                    {artifact && (
                      <button
                        onClick={() => setEvaluatingArtifactId(artifact.id)}
                        className="text-[11px] font-semibold text-indigo-600 hover:text-indigo-800 flex items-center gap-0.5"
                      >
                        <Plus className="w-3 h-3" /> Add Evaluation
                      </button>
                    )}
                  </div>

                  <div className="mt-1.5 space-y-1.5">
                    {evaluations && evaluations.length > 0 ? (
                      evaluations.map((ev) => (
                        <div key={ev.id} className="p-2 rounded bg-slate-50 border border-slate-200">
                          <div className="flex items-center justify-between font-medium text-slate-800">
                            <span>{ev.metric_name}</span>
                            <span className="font-bold text-indigo-700 flex items-center gap-0.5">
                              <Star className="w-3 h-3 fill-indigo-600 text-indigo-600" />
                              {ev.value?.score ?? JSON.stringify(ev.value)} / 5
                            </span>
                          </div>
                          {ev.notes && (
                            <p className="text-[11px] text-slate-500 mt-1 italic">
                              "{ev.notes}"
                            </p>
                          )}
                        </div>
                      ))
                    ) : (
                      <p className="text-slate-400 italic text-[11px]">No evaluations recorded.</p>
                    )}
                  </div>
                </div>

                {/* Inline Evaluation Modal/Drawer */}
                {evaluatingArtifactId === artifact?.id && (
                  <div className="p-3 rounded-xl border border-indigo-200 bg-indigo-50/50 space-y-2 mt-2">
                    <span className="font-bold text-slate-900 text-xs">Record Human Evaluation</span>
                    <div>
                      <label className="text-[11px] text-slate-600">Metric</label>
                      <select
                        value={metricName}
                        onChange={(e) => setMetricName(e.target.value)}
                        className="w-full h-7 rounded border border-slate-300 text-xs px-2 bg-white"
                      >
                        <option value="Instructional Clarity">Instructional Clarity</option>
                        <option value="Cognitive Load">Cognitive Load</option>
                        <option value="Question Diversity">Question Diversity</option>
                        <option value="Pedagogical Rigor">Pedagogical Rigor</option>
                      </select>
                    </div>
                    <div>
                      <div className="flex justify-between text-[11px]">
                        <span>Rating Score</span>
                        <span className="font-bold text-indigo-700">{score} / 5</span>
                      </div>
                      <input
                        type="range"
                        min="1"
                        max="5"
                        value={score}
                        onChange={(e) => setScore(parseInt(e.target.value))}
                        className="w-full accent-indigo-600"
                      />
                    </div>
                    <div>
                      <input
                        type="text"
                        placeholder="Evaluation notes / rationale..."
                        value={notes}
                        onChange={(e) => setNotes(e.target.value)}
                        className="w-full h-7 rounded border border-slate-300 text-xs px-2"
                      />
                    </div>
                    <div className="flex gap-1.5 pt-1">
                      <Button
                        size="sm"
                        onClick={() => handleAddEvaluation(artifact.id)}
                        disabled={isSubmittingEval}
                        className="flex-1 text-xs h-7 bg-indigo-600 hover:bg-indigo-700"
                      >
                        Save
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setEvaluatingArtifactId(null)}
                        className="text-xs h-7"
                      >
                        Cancel
                      </Button>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          )
        })}
      </div>
    </div>
  )
}
