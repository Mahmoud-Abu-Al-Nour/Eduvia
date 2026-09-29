import React, { useState } from 'react'
import type { ResearchArtifact } from '@/types'
import { researchApi } from '@/services/researchApi'
import { useAuth } from '@/features/auth/AuthContext'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import {
  FileText,
  Download,
  UploadCloud,
  CheckCircle2,
  AlertTriangle,
  X,
  Copy,
  Check,
} from 'lucide-react'

interface ArtifactViewerModalProps {
  artifact: ResearchArtifact | null
  onClose: () => void
  onArtifactPromoted?: () => void
}

export const ArtifactViewerModal: React.FC<ArtifactViewerModalProps> = ({
  artifact,
  onClose,
  onArtifactPromoted,
}) => {
  const { user } = useAuth()
  const [activeView, setActiveView] = useState<'json' | 'raw' | 'preview'>('json')
  const [copied, setCopied] = useState(false)
  const [isPromoting, setIsPromoting] = useState(false)
  const [promotionResult, setPromotionResult] = useState<string | null>(null)
  const [promotionError, setPromotionError] = useState<string | null>(null)

  if (!artifact) return null

  const handleCopy = () => {
    const textToCopy =
      activeView === 'raw'
        ? artifact.raw_text || ''
        : JSON.stringify(artifact.payload, null, 2)
    navigator.clipboard.writeText(textToCopy)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleExport = async (format: 'json' | 'markdown') => {
    try {
      const res = await researchApi.exportArtifact(artifact.id, format)
      const blob = new Blob(
        [typeof res.content === 'string' ? res.content : JSON.stringify(res.content, null, 2)],
        { type: format === 'json' ? 'application/json' : 'text/markdown' }
      )
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = res.filename
      a.click()
      URL.revokeObjectURL(url)
    } catch (err: any) {
      alert(`Export failed: ${err.message || 'Unknown error'}`)
    }
  }

  const handlePromote = async () => {
    if (!window.confirm('Promote this research artifact to a Production Draft? This does NOT auto-publish.')) {
      return
    }
    setIsPromoting(true)
    setPromotionError(null)
    setPromotionResult(null)
    try {
      const res = await researchApi.promoteArtifact(artifact.id, {
        target_destination: 'activity',
        notes: `Promoted by ${user?.full_name} (${user?.email})`,
      })
      setPromotionResult(res.message)
      if (onArtifactPromoted) onArtifactPromoted()
    } catch (err: any) {
      setPromotionError(err.message || 'Promotion failed')
    } finally {
      setIsPromoting(false)
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-sm p-4">
      <div className="bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-4xl max-h-[90vh] flex flex-col overflow-hidden animate-in fade-in-50 zoom-in-95">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-200 flex items-center justify-between bg-slate-50/80">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-indigo-100 text-indigo-700">
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-bold text-slate-900 text-base">Research Artifact Inspector</h3>
                <Badge variant="outline" className="text-xs capitalize font-medium">
                  {artifact.artifact_type}
                </Badge>
                {artifact.is_production_compatible ? (
                  <Badge variant="outline" className="bg-emerald-50 text-emerald-700 border-emerald-300 text-xs gap-1">
                    <CheckCircle2 className="w-3 h-3" /> Compatible
                  </Badge>
                ) : (
                  <Badge variant="outline" className="bg-amber-50 text-amber-700 border-amber-300 text-xs gap-1">
                    <AlertTriangle className="w-3 h-3" /> Experimental Schema
                  </Badge>
                )}
                {artifact.promoted_to_production && (
                  <Badge variant="outline" className="bg-purple-50 text-purple-700 border-purple-300 text-xs">
                    Promoted to Draft
                  </Badge>
                )}
              </div>
              <p className="text-xs text-slate-500 font-mono mt-0.5">
                ID: {artifact.id} | Run: {artifact.run_id}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-200 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Toolbar */}
        <div className="px-6 py-2.5 border-b border-slate-100 bg-white flex items-center justify-between gap-3 text-xs">
          <div className="flex items-center gap-1.5 bg-slate-100 p-1 rounded-lg">
            <button
              onClick={() => setActiveView('json')}
              className={`px-3 py-1 rounded-md font-medium transition-all ${
                activeView === 'json'
                  ? 'bg-white text-slate-900 shadow-sm'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Structured JSON
            </button>
            <button
              onClick={() => setActiveView('raw')}
              className={`px-3 py-1 rounded-md font-medium transition-all ${
                activeView === 'raw'
                  ? 'bg-white text-slate-900 shadow-sm'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Raw LLM Output
            </button>
            <button
              onClick={() => setActiveView('preview')}
              className={`px-3 py-1 rounded-md font-medium transition-all ${
                activeView === 'preview'
                  ? 'bg-white text-slate-900 shadow-sm'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Formatted Preview
            </button>
          </div>

          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={handleCopy}
              className="text-xs h-7 gap-1"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
              {copied ? 'Copied' : 'Copy'}
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => handleExport('json')}
              className="text-xs h-7 gap-1"
            >
              <Download className="w-3.5 h-3.5" /> JSON
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => handleExport('markdown')}
              className="text-xs h-7 gap-1"
            >
              <Download className="w-3.5 h-3.5" /> Markdown
            </Button>

            {user?.role === 'admin' && !artifact.promoted_to_production && (
              <Button
                variant="default"
                size="sm"
                onClick={handlePromote}
                disabled={!artifact.is_production_compatible || isPromoting}
                className="text-xs h-7 gap-1 bg-purple-700 hover:bg-purple-800"
                title={!artifact.is_production_compatible ? 'Artifact must be validated as production-compatible first' : ''}
              >
                <UploadCloud className="w-3.5 h-3.5" /> Promote to Draft
              </Button>
            )}
          </div>
        </div>

        {/* Promotion banner */}
        {promotionResult && (
          <div className="px-6 py-2 bg-emerald-50 border-b border-emerald-200 text-xs text-emerald-800 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0" />
            <span>{promotionResult}</span>
          </div>
        )}
        {promotionError && (
          <div className="px-6 py-2 bg-rose-50 border-b border-rose-200 text-xs text-rose-800 flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-rose-600 flex-shrink-0" />
            <span>{promotionError}</span>
          </div>
        )}

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto p-6 bg-slate-900 text-slate-100 font-mono text-xs">
          {activeView === 'json' && (
            <pre className="whitespace-pre-wrap leading-relaxed text-indigo-300">
              {JSON.stringify(artifact.payload, null, 2)}
            </pre>
          )}

          {activeView === 'raw' && (
            <pre className="whitespace-pre-wrap leading-relaxed text-amber-200">
              {artifact.raw_text || '// No raw output preserved for this run.'}
            </pre>
          )}

          {activeView === 'preview' && (
            <div className="bg-white text-slate-900 p-6 rounded-xl font-sans text-sm space-y-4 shadow-inner">
              <h4 className="font-bold text-base text-slate-800 border-b pb-2">
                Artifact Content Summary
              </h4>
              {artifact.payload?.items ? (
                <div className="space-y-3">
                  <p className="text-xs text-slate-500 font-medium">
                    Question / Item Count: {artifact.payload.items.length}
                  </p>
                  <div className="space-y-2.5">
                    {artifact.payload.items.map((it: any, idx: number) => (
                      <div key={idx} className="p-3 rounded-lg border border-slate-200 bg-slate-50">
                        <div className="flex items-center justify-between mb-1">
                          <span className="font-bold text-xs text-indigo-700">Item #{idx + 1} ({it.type || 'Question'})</span>
                          {it.visual_cue && (
                            <Badge variant="outline" className="text-[10px] bg-sky-50 text-sky-700">
                              Cue: {it.visual_cue}
                            </Badge>
                          )}
                        </div>
                        <p className="font-medium text-slate-800">{it.prompt || it.title || it.question}</p>
                        {it.choices && (
                          <div className="mt-2 flex flex-wrap gap-1.5">
                            {it.choices.map((c: any, cIdx: number) => (
                              <span key={cIdx} className="px-2 py-0.5 rounded bg-white border border-slate-300 text-xs">
                                {typeof c === 'string' ? c : c.text}
                              </span>
                            ))}
                          </div>
                        )}
                        {it.answer && (
                          <p className="mt-2 text-xs text-emerald-700 font-medium">
                            Correct Answer: {it.answer}
                          </p>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="prose prose-sm max-w-none text-slate-700">
                  <pre className="p-4 bg-slate-50 rounded-lg border border-slate-200 text-xs font-mono">
                    {JSON.stringify(artifact.payload, null, 2)}
                  </pre>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-slate-200 bg-slate-50 flex items-center justify-between text-xs text-slate-500">
          <span>Schema Version: {artifact.schema_version}</span>
          <span>Created: {new Date(artifact.created_at).toLocaleString()}</span>
        </div>
      </div>
    </div>
  )
}
