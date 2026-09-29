import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import type {
  ResearchArtifact,
  ResearchExperiment,
  ResearchProject,
  ResearchVariant,
} from '@/types'
import { researchApi } from '@/services/researchApi'
import { useAuth } from '@/features/auth/AuthContext'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import {
  FlaskConical,
  FolderPlus,
  Plus,
  Columns3,
  Layers,
  RotateCcw,
  Sparkles,
  ArrowRight,
  LogOut,
  Copy,
  ChevronRight,
  Compass,
} from 'lucide-react'
import { PromptStudio } from './PromptStudio'
import { ComparisonView } from './ComparisonView'
import { ArtifactViewerModal } from './ArtifactViewerModal'

interface ResearchWorkspacePageProps {
  initialTab?: 'projects' | 'experiments' | 'studio' | 'compare' | 'artifacts'
}

export const ResearchWorkspacePage: React.FC<ResearchWorkspacePageProps> = ({
  initialTab = 'projects',
}) => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const [activeTab, setActiveTab] = useState<'projects' | 'experiments' | 'studio' | 'compare' | 'artifacts'>(initialTab)

  const [projects, setProjects] = useState<ResearchProject[]>([])
  const [selectedProjectId, setSelectedProjectId] = useState<string>('')
  const [experiments, setExperiments] = useState<ResearchExperiment[]>([])
  const [selectedExperimentId, setSelectedExperimentId] = useState<string>('')
  const [variants, setVariants] = useState<ResearchVariant[]>([])
  const [selectedVariantId, setSelectedVariantId] = useState<string>('')

  const [isLoading, setIsLoading] = useState(true)
  const [inspectingArtifact, setInspectingArtifact] = useState<ResearchArtifact | null>(null)

  // Creation modals
  const [showNewProjectModal, setShowNewProjectModal] = useState(false)
  const [newProjectName, setNewProjectName] = useState('')
  const [newProjectDesc, setNewProjectDesc] = useState('')
  const [newProjectQuestion, setNewProjectQuestion] = useState('')
  const [newProjectHypothesis, setNewProjectHypothesis] = useState('')

  const [showNewExpModal, setShowNewExpModal] = useState(false)
  const [newExpName, setNewExpName] = useState('')
  const [newExpDesc, setNewExpDesc] = useState('')
  const [newExpQuestion, setNewExpQuestion] = useState('')
  const [newExpHypothesis, setNewExpHypothesis] = useState('')

  const [showNewVarModal, setShowNewVarModal] = useState(false)
  const [newVarName, setNewVarName] = useState('')
  const [newVarDesc, setNewVarDesc] = useState('')
  const [newVarConfig, setNewVarConfig] = useState('{\n  "temperature": 0.5,\n  "scaffolding_style": "visual"\n}')

  // Load projects
  const loadProjects = async () => {
    setIsLoading(true)
    try {
      const projs = await researchApi.getProjects()
      setProjects(projs)
      if (projs.length > 0 && !selectedProjectId) {
        setSelectedProjectId(projs[0].id)
      }
    } catch (err: any) {
      console.error('Failed to load projects', err)
    } finally {
      setIsLoading(false)
    }
  }

  // Load experiments for selected project
  const loadExperiments = async (projId: string) => {
    if (!projId) return
    try {
      const exps = await researchApi.getExperiments(projId)
      setExperiments(exps)
      if (exps.length > 0) {
        setSelectedExperimentId(exps[0].id)
      } else {
        setSelectedExperimentId('')
        setVariants([])
      }
    } catch (err: any) {
      console.error('Failed to load experiments', err)
    }
  }

  // Load variants for selected experiment
  const loadVariants = async (expId: string) => {
    if (!expId) return
    try {
      const vars = await researchApi.getVariants(expId)
      setVariants(vars)
      if (vars.length > 0) {
        setSelectedVariantId(vars[0].id)
      } else {
        setSelectedVariantId('')
      }
    } catch (err: any) {
      console.error('Failed to load variants', err)
    }
  }

  useEffect(() => {
    loadProjects()
  }, [])

  useEffect(() => {
    if (selectedProjectId) {
      loadExperiments(selectedProjectId)
    }
  }, [selectedProjectId])

  useEffect(() => {
    if (selectedExperimentId) {
      loadVariants(selectedExperimentId)
    }
  }, [selectedExperimentId])

  const selectedProject = projects.find((p) => p.id === selectedProjectId)
  const selectedExperiment = experiments.find((e) => e.id === selectedExperimentId)

  // Handlers
  const handleCreateProject = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newProjectName.trim()) return
    try {
      const created = await researchApi.createProject({
        name: newProjectName.trim(),
        description: newProjectDesc.trim() || undefined,
        research_question: newProjectQuestion.trim() || undefined,
        hypothesis: newProjectHypothesis.trim() || undefined,
      })
      setShowNewProjectModal(false)
      setNewProjectName('')
      setNewProjectDesc('')
      setNewProjectQuestion('')
      setNewProjectHypothesis('')
      await loadProjects()
      setSelectedProjectId(created.id)
    } catch (err: any) {
      alert(`Error creating project: ${err.message}`)
    }
  }

  const handleCreateExperiment = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!selectedProjectId || !newExpName.trim()) return
    try {
      const created = await researchApi.createExperiment(selectedProjectId, {
        name: newExpName.trim(),
        description: newExpDesc.trim() || undefined,
        research_question: newExpQuestion.trim() || undefined,
        hypothesis: newExpHypothesis.trim() || undefined,
      })
      setShowNewExpModal(false)
      setNewExpName('')
      setNewExpDesc('')
      setNewExpQuestion('')
      setNewExpHypothesis('')
      await loadExperiments(selectedProjectId)
      setSelectedExperimentId(created.id)
    } catch (err: any) {
      alert(`Error creating experiment: ${err.message}`)
    }
  }

  const handleCreateVariant = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!selectedExperimentId || !newVarName.trim()) return
    let parsedConfig = {}
    try {
      parsedConfig = JSON.parse(newVarConfig)
    } catch {
      alert('Variant configuration must be valid JSON.')
      return
    }
    try {
      const created = await researchApi.createVariant(selectedExperimentId, {
        name: newVarName.trim(),
        description: newVarDesc.trim() || undefined,
        configuration: parsedConfig,
      })
      setShowNewVarModal(false)
      setNewVarName('')
      setNewVarDesc('')
      await loadVariants(selectedExperimentId)
      setSelectedVariantId(created.id)
    } catch (err: any) {
      alert(`Error creating variant: ${err.message}`)
    }
  }

  const handleCloneVariant = async (v: ResearchVariant) => {
    try {
      const cloned = await researchApi.cloneVariant(v.id, {
        new_name: `${v.name} (Clone)`,
      })
      await loadVariants(v.experiment_id)
      setSelectedVariantId(cloned.id)
    } catch (err: any) {
      alert(`Error cloning variant: ${err.message}`)
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      {/* Top Navigation Header */}
      <header className="sticky top-0 z-40 bg-white border-b border-slate-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-700 via-indigo-600 to-purple-600 flex items-center justify-center text-white shadow-md">
              <FlaskConical className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-slate-900 tracking-tight text-base">
                  Eduvia <span className="text-indigo-600">Research</span>
                </span>
                <Badge variant="outline" className="bg-indigo-50 text-indigo-700 border-indigo-200 text-[10px] font-bold tracking-wider">
                  SANDBOX
                </Badge>
              </div>
              <p className="text-[11px] text-slate-500 font-medium">
                Pedagogical Experimentation & Comparative Analysis
              </p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="hidden sm:flex flex-col items-end">
              <span className="text-xs font-bold text-slate-800">{user?.full_name}</span>
              <span className="text-[10px] font-mono text-slate-500 uppercase">{user?.role}</span>
            </div>
            {user?.role === 'admin' && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => navigate('/admin')}
                className="text-xs h-8 gap-1.5 text-amber-700 border-amber-200 hover:bg-amber-50"
              >
                Admin Center
              </Button>
            )}
            <Button
              variant="outline"
              size="sm"
              onClick={logout}
              className="text-xs h-8 gap-1.5 text-slate-600 hover:text-slate-900"
            >
              <LogOut className="w-3.5 h-3.5" /> Sign Out
            </Button>
          </div>
        </div>

        {/* Tab Navigation Navigation */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 border-t border-slate-100 flex items-center gap-1 overflow-x-auto text-xs font-semibold py-1">
          <button
            onClick={() => setActiveTab('projects')}
            className={`px-3 py-2 rounded-lg flex items-center gap-1.5 transition-colors whitespace-nowrap ${
              activeTab === 'projects'
                ? 'bg-indigo-50 text-indigo-700 font-bold'
                : 'text-slate-600 hover:bg-slate-100'
            }`}
          >
            <Compass className="w-4 h-4" />
            <span>Overview & Projects</span>
            {projects.length > 0 && (
              <span className="ml-1 px-1.5 py-0.2 rounded-full bg-slate-200 text-[10px] font-mono">
                {projects.length}
              </span>
            )}
          </button>

          <button
            onClick={() => setActiveTab('experiments')}
            className={`px-3 py-2 rounded-lg flex items-center gap-1.5 transition-colors whitespace-nowrap ${
              activeTab === 'experiments'
                ? 'bg-indigo-50 text-indigo-700 font-bold'
                : 'text-slate-600 hover:bg-slate-100'
            }`}
          >
            <Layers className="w-4 h-4" />
            <span>Experiments & Variants</span>
            {experiments.length > 0 && (
              <span className="ml-1 px-1.5 py-0.2 rounded-full bg-slate-200 text-[10px] font-mono">
                {experiments.length}
              </span>
            )}
          </button>

          <button
            onClick={() => setActiveTab('studio')}
            className={`px-3 py-2 rounded-lg flex items-center gap-1.5 transition-colors whitespace-nowrap ${
              activeTab === 'studio'
                ? 'bg-indigo-50 text-indigo-700 font-bold'
                : 'text-slate-600 hover:bg-slate-100'
            }`}
          >
            <Sparkles className="w-4 h-4 text-indigo-600" />
            <span>Prompt Studio</span>
          </button>

          <button
            onClick={() => setActiveTab('compare')}
            className={`px-3 py-2 rounded-lg flex items-center gap-1.5 transition-colors whitespace-nowrap ${
              activeTab === 'compare'
                ? 'bg-indigo-50 text-indigo-700 font-bold'
                : 'text-slate-600 hover:bg-slate-100'
            }`}
          >
            <Columns3 className="w-4 h-4" />
            <span>Compare Variants</span>
          </button>
        </div>
      </header>

      {/* Main Content Body */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Project Selector bar if inside experiment/studio/compare tabs */}
        {activeTab !== 'projects' && (
          <div className="mb-6 p-3.5 rounded-xl bg-white border border-slate-200 shadow-sm flex flex-wrap items-center justify-between gap-3 text-xs">
            <div className="flex items-center gap-3">
              <span className="font-bold text-slate-500 uppercase tracking-wider text-[10px]">
                Active Context:
              </span>
              <div className="flex items-center gap-1.5">
                <span className="text-slate-500 font-medium">Project:</span>
                <select
                  value={selectedProjectId}
                  onChange={(e) => setSelectedProjectId(e.target.value)}
                  className="h-8 rounded-lg border border-slate-300 text-xs px-2.5 font-bold text-slate-900 bg-white"
                >
                  {projects.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.name}
                    </option>
                  ))}
                </select>
              </div>

              {experiments.length > 0 && (
                <div className="flex items-center gap-1.5">
                  <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
                  <span className="text-slate-500 font-medium">Experiment:</span>
                  <select
                    value={selectedExperimentId}
                    onChange={(e) => setSelectedExperimentId(e.target.value)}
                    className="h-8 rounded-lg border border-slate-300 text-xs px-2.5 font-bold text-slate-900 bg-white"
                  >
                    {experiments.map((ex) => (
                      <option key={ex.id} value={ex.id}>
                        {ex.name}
                      </option>
                    ))}
                  </select>
                </div>
              )}
            </div>

            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowNewExpModal(true)}
                className="text-xs h-8 gap-1"
              >
                <Plus className="w-3 h-3" /> New Experiment
              </Button>
            </div>
          </div>
        )}

        {/* ── TAB 1: Overview & Projects ─────────────────────────────────── */}
        {activeTab === 'projects' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xl font-black text-slate-900 tracking-tight">
                  Research Projects
                </h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  Organized initiatives for testing educational hypotheses and generative pipelines.
                </p>
              </div>
              <Button
                onClick={() => setShowNewProjectModal(true)}
                className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs h-9 gap-1.5 shadow-sm"
              >
                <FolderPlus className="w-4 h-4" /> New Research Project
              </Button>
            </div>

            {/* Project Cards Grid */}
            {isLoading ? (
              <div className="p-12 text-center text-slate-400 text-sm">
                <RotateCcw className="w-5 h-5 animate-spin mx-auto mb-2" />
                Loading research projects...
              </div>
            ) : projects.length === 0 ? (
              <div className="p-12 text-center border-2 border-dashed border-slate-200 rounded-2xl bg-white">
                <FlaskConical className="w-10 h-10 text-slate-300 mx-auto mb-3" />
                <h4 className="font-bold text-slate-800 text-base">No Research Projects Yet</h4>
                <p className="text-xs text-slate-500 max-w-sm mx-auto mt-1 mb-4">
                  Create your first isolated research project to begin testing pedagogical strategies and custom prompts.
                </p>
                <Button
                  onClick={() => setShowNewProjectModal(true)}
                  className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs h-9"
                >
                  Create Project
                </Button>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {projects.map((proj) => (
                  <Card
                    key={proj.id}
                    className={`border transition-all duration-200 hover:shadow-md cursor-pointer ${
                      selectedProjectId === proj.id ? 'border-indigo-500 ring-2 ring-indigo-500/20 bg-white' : 'border-slate-200 bg-white'
                    }`}
                    onClick={() => {
                      setSelectedProjectId(proj.id)
                    }}
                  >
                    <CardHeader className="pb-3 pt-5 px-5">
                      <div className="flex items-center justify-between mb-2">
                        <Badge variant="outline" className="text-[10px] font-bold uppercase tracking-wider bg-slate-100">
                          {proj.status}
                        </Badge>
                        <span className="text-[11px] text-slate-400 font-mono">
                          {new Date(proj.created_at).toLocaleDateString()}
                        </span>
                      </div>
                      <CardTitle className="text-base font-bold text-slate-900 group-hover:text-indigo-600">
                        {proj.name}
                      </CardTitle>
                      <CardDescription className="text-xs line-clamp-2 mt-1">
                        {proj.description || 'No description provided.'}
                      </CardDescription>
                    </CardHeader>

                    <CardContent className="px-5 pb-5 pt-0 space-y-3 text-xs border-t border-slate-100 mt-2">
                      {proj.research_question && (
                        <div className="mt-3">
                          <span className="font-bold text-slate-500 uppercase text-[10px] tracking-wider block">
                            Research Question:
                          </span>
                          <p className="text-slate-700 line-clamp-2 italic mt-0.5">
                            "{proj.research_question}"
                          </p>
                        </div>
                      )}

                      {proj.hypothesis && (
                        <div>
                          <span className="font-bold text-slate-500 uppercase text-[10px] tracking-wider block">
                            Hypothesis:
                          </span>
                          <p className="text-slate-700 line-clamp-2 mt-0.5">
                            {proj.hypothesis}
                          </p>
                        </div>
                      )}

                      <div className="pt-2 flex items-center justify-between border-t border-slate-100">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={(e) => {
                            e.stopPropagation()
                            setSelectedProjectId(proj.id)
                            setActiveTab('experiments')
                          }}
                          className="text-xs font-bold text-indigo-600 hover:text-indigo-800 p-0 h-auto gap-1"
                        >
                          View Experiments <ArrowRight className="w-3.5 h-3.5" />
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </div>
        )}

        {/* ── TAB 2: Experiments & Variants ─────────────────────────────── */}
        {activeTab === 'experiments' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xl font-black text-slate-900 tracking-tight">
                  Experiments & Treatment Variants
                </h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  Define specific test setups and configure variable treatment branches.
                </p>
              </div>
              <div className="flex items-center gap-2">
                <Button
                  onClick={() => setShowNewExpModal(true)}
                  className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs h-9 gap-1.5"
                >
                  <Plus className="w-4 h-4" /> New Experiment
                </Button>
              </div>
            </div>

            {experiments.length === 0 ? (
              <div className="p-12 text-center border-2 border-dashed border-slate-200 rounded-2xl bg-white">
                <Layers className="w-10 h-10 text-slate-300 mx-auto mb-3" />
                <h4 className="font-bold text-slate-800 text-base">No Experiments in this Project</h4>
                <p className="text-xs text-slate-500 max-w-sm mx-auto mt-1 mb-4">
                  Create an experiment to start comparing multiple pedagogical variants.
                </p>
                <Button
                  onClick={() => setShowNewExpModal(true)}
                  className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs h-9"
                >
                  Create Experiment
                </Button>
              </div>
            ) : (
              <div className="space-y-6">
                {experiments.map((exp) => (
                  <Card key={exp.id} className="border-slate-200 shadow-sm bg-white overflow-hidden">
                    <CardHeader className="bg-slate-50/70 border-b border-slate-100 p-5">
                      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
                        <div>
                          <div className="flex items-center gap-2">
                            <CardTitle className="text-base font-bold text-slate-900">
                              {exp.name}
                            </CardTitle>
                            <Badge variant="outline" className="text-xs font-semibold capitalize">
                              {exp.status}
                            </Badge>
                          </div>
                          <CardDescription className="text-xs mt-1">
                            {exp.description || 'No description.'}
                          </CardDescription>
                        </div>

                        <div className="flex items-center gap-2">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => {
                              setSelectedExperimentId(exp.id)
                              setShowNewVarModal(true)
                            }}
                            className="text-xs h-8 gap-1"
                          >
                            <Plus className="w-3.5 h-3.5" /> Add Variant
                          </Button>
                          <Button
                            variant="default"
                            size="sm"
                            onClick={() => {
                              setSelectedExperimentId(exp.id)
                              setActiveTab('compare')
                            }}
                            className="text-xs h-8 gap-1 bg-indigo-600 hover:bg-indigo-700"
                          >
                            <Columns3 className="w-3.5 h-3.5" /> Compare Variants
                          </Button>
                        </div>
                      </div>

                      {exp.research_question && (
                        <p className="text-xs text-slate-600 mt-2 italic border-l-2 border-indigo-400 pl-2">
                          <span className="font-semibold text-slate-800 not-italic">Question:</span> {exp.research_question}
                        </p>
                      )}
                    </CardHeader>

                    {/* Variants Table under this Experiment */}
                    <CardContent className="p-5">
                      <div className="space-y-3">
                        <div className="flex items-center justify-between">
                          <span className="font-bold uppercase tracking-wider text-slate-400 text-xs">
                            Experimental Variants
                          </span>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                          {variants
                            .filter((v) => v.experiment_id === exp.id)
                            .map((v) => (
                              <div
                                key={v.id}
                                className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 hover:bg-slate-50 hover:border-indigo-300 transition-all space-y-2.5 flex flex-col justify-between"
                              >
                                <div>
                                  <div className="flex items-center justify-between mb-1">
                                    <h5 className="font-bold text-slate-900 text-sm">{v.name}</h5>
                                    {v.parent_variant_id && (
                                      <Badge variant="outline" className="text-[10px] bg-slate-100">
                                        Clone
                                      </Badge>
                                    )}
                                  </div>
                                  <p className="text-xs text-slate-500 line-clamp-2">
                                    {v.description || 'No description.'}
                                  </p>

                                  <div className="mt-2.5 p-2 rounded bg-white border border-slate-200 font-mono text-[11px] space-y-1">
                                    {Object.entries(v.configuration).map(([k, val]) => (
                                      <div key={k} className="flex justify-between">
                                        <span className="text-slate-400">{k}:</span>
                                        <span className="font-semibold text-slate-800">{String(val)}</span>
                                      </div>
                                    ))}
                                  </div>
                                </div>

                                <div className="flex items-center gap-2 pt-2 border-t border-slate-200/60">
                                  <Button
                                    variant="outline"
                                    size="sm"
                                    onClick={() => {
                                      setSelectedExperimentId(exp.id)
                                      setSelectedVariantId(v.id)
                                      setActiveTab('studio')
                                    }}
                                    className="flex-1 text-xs h-7 gap-1 font-semibold text-indigo-700 hover:bg-indigo-50"
                                  >
                                    <Sparkles className="w-3 h-3" /> Launch in Studio
                                  </Button>
                                  <Button
                                    variant="ghost"
                                    size="sm"
                                    onClick={() => handleCloneVariant(v)}
                                    className="text-xs h-7 px-2"
                                    title="Clone Variant"
                                  >
                                    <Copy className="w-3.5 h-3.5 text-slate-500" />
                                  </Button>
                                </div>
                              </div>
                            ))}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </div>
        )}

        {/* ── TAB 3: Prompt Studio ────────────────────────────────────────── */}
        {activeTab === 'studio' && selectedProject && selectedExperiment && (
          <PromptStudio
            project={selectedProject}
            experiment={selectedExperiment}
            variants={variants}
            selectedVariantId={selectedVariantId}
            onVariantChange={setSelectedVariantId}
            onInspectArtifact={setInspectingArtifact}
          />
        )}

        {/* ── TAB 4: Side-by-Side Comparison ──────────────────────────────── */}
        {activeTab === 'compare' && selectedExperiment && (
          <ComparisonView
            experiment={selectedExperiment}
            onInspectArtifact={setInspectingArtifact}
          />
        )}
      </main>

      {/* ── Modals ──────────────────────────────────────────────────────── */}

      {/* 1. New Project Modal */}
      {showNewProjectModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-sm p-4">
          <div className="bg-white rounded-2xl shadow-xl border border-slate-200 w-full max-w-lg p-6">
            <h3 className="text-base font-bold text-slate-900 mb-1">Create Research Project</h3>
            <p className="text-xs text-slate-500 mb-4">
              Top-level isolated workspace for your educational experiment.
            </p>
            <form onSubmit={handleCreateProject} className="space-y-3.5">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Project Name <span className="text-rose-500">*</span>
                </label>
                <Input
                  required
                  value={newProjectName}
                  onChange={(e) => setNewProjectName(e.target.value)}
                  placeholder="e.g. Scaffolding in Early Literacy"
                  className="text-xs h-9"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Description
                </label>
                <textarea
                  value={newProjectDesc}
                  onChange={(e) => setNewProjectDesc(e.target.value)}
                  placeholder="Summary of this research initiative..."
                  rows={2}
                  className="w-full rounded-lg border border-slate-300 p-2 text-xs text-slate-800"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Research Question
                </label>
                <Input
                  value={newProjectQuestion}
                  onChange={(e) => setNewProjectQuestion(e.target.value)}
                  placeholder="e.g. Does visual cue placement increase accuracy?"
                  className="text-xs h-9"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Hypothesis
                </label>
                <Input
                  value={newProjectHypothesis}
                  onChange={(e) => setNewProjectHypothesis(e.target.value)}
                  placeholder="e.g. Icon cues reduce completion latency by 20%."
                  className="text-xs h-9"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-slate-100">
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => setShowNewProjectModal(false)}
                >
                  Cancel
                </Button>
                <Button type="submit" size="sm" className="bg-indigo-600 hover:bg-indigo-700 text-white">
                  Create Project
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* 2. New Experiment Modal */}
      {showNewExpModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-sm p-4">
          <div className="bg-white rounded-2xl shadow-xl border border-slate-200 w-full max-w-lg p-6">
            <h3 className="text-base font-bold text-slate-900 mb-1">Create Research Experiment</h3>
            <p className="text-xs text-slate-500 mb-4">
              Defines a specific comparative test setup under {selectedProject?.name}.
            </p>
            <form onSubmit={handleCreateExperiment} className="space-y-3.5">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Experiment Name <span className="text-rose-500">*</span>
                </label>
                <Input
                  required
                  value={newExpName}
                  onChange={(e) => setNewExpName(e.target.value)}
                  placeholder="e.g. Visual vs Text Explanation"
                  className="text-xs h-9"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Description
                </label>
                <textarea
                  value={newExpDesc}
                  onChange={(e) => setNewExpDesc(e.target.value)}
                  placeholder="Explain what treatment variables are being isolated..."
                  rows={2}
                  className="w-full rounded-lg border border-slate-300 p-2 text-xs text-slate-800"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Research Question
                </label>
                <Input
                  value={newExpQuestion}
                  onChange={(e) => setNewExpQuestion(e.target.value)}
                  placeholder="e.g. Which scaffolding approach maximizes comprehension?"
                  className="text-xs h-9"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Hypothesis
                </label>
                <Input
                  value={newExpHypothesis}
                  onChange={(e) => setNewExpHypothesis(e.target.value)}
                  placeholder="e.g. Visual explanations produce fewer retry loops."
                  className="text-xs h-9"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-slate-100">
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => setShowNewExpModal(false)}
                >
                  Cancel
                </Button>
                <Button type="submit" size="sm" className="bg-indigo-600 hover:bg-indigo-700 text-white">
                  Create Experiment
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* 3. New Variant Modal */}
      {showNewVarModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-sm p-4">
          <div className="bg-white rounded-2xl shadow-xl border border-slate-200 w-full max-w-lg p-6">
            <h3 className="text-base font-bold text-slate-900 mb-1">Create Experimental Variant</h3>
            <p className="text-xs text-slate-500 mb-4">
              Configure treatment parameters (e.g. temperature, scaffolding style, question count).
            </p>
            <form onSubmit={handleCreateVariant} className="space-y-3.5">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Variant Name <span className="text-rose-500">*</span>
                </label>
                <Input
                  required
                  value={newVarName}
                  onChange={(e) => setNewVarName(e.target.value)}
                  placeholder="e.g. Variant C: Worked Example"
                  className="text-xs h-9"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Description
                </label>
                <Input
                  value={newVarDesc}
                  onChange={(e) => setNewVarDesc(e.target.value)}
                  placeholder="e.g. Step-by-step worked demonstration"
                  className="text-xs h-9"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Configuration JSON
                </label>
                <textarea
                  value={newVarConfig}
                  onChange={(e) => setNewVarConfig(e.target.value)}
                  rows={4}
                  className="w-full rounded-lg border border-slate-300 p-2 text-xs font-mono text-slate-800"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-slate-100">
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => setShowNewVarModal(false)}
                >
                  Cancel
                </Button>
                <Button type="submit" size="sm" className="bg-indigo-600 hover:bg-indigo-700 text-white">
                  Create Variant
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* 4. Artifact Inspector Modal */}
      {inspectingArtifact && (
        <ArtifactViewerModal
          artifact={inspectingArtifact}
          onClose={() => setInspectingArtifact(null)}
          onArtifactPromoted={() => {
            if (selectedExperimentId) loadVariants(selectedExperimentId)
          }}
        />
      )}
    </div>
  )
}
