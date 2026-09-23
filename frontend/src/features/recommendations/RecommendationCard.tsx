import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { recommendationsApi } from '@/services/api'
import type { RecommendationDecision } from '@/types'

interface RecommendationCardProps {
  learnerId: string
  recommendation: RecommendationDecision | null
  loading?: boolean
  onProfileSynced?: () => void
  onActivityLaunched?: (activityId: string) => void
}

export const RecommendationCard: React.FC<RecommendationCardProps> = ({
  learnerId,
  recommendation,
  loading = false,
  onProfileSynced,
  onActivityLaunched,
}) => {
  const navigate = useNavigate()
  const [isLaunching, setIsLaunching] = useState(false)
  const [isSyncing, setIsSyncing] = useState(false)
  const [syncMessage, setSyncMessage] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleLaunchActivity = async () => {
    try {
      setIsLaunching(true)
      setError(null)
      const res = await recommendationsApi.getNextActivity(learnerId)
      const activityId = res.activity.id
      if (onActivityLaunched) {
        onActivityLaunched(activityId)
      } else {
        navigate(`/learn/${activityId}`)
      }
    } catch (err: unknown) {
      console.error('Failed to launch next activity:', err)
      setError('Could not generate the recommended activity. Please try again.')
    } finally {
      setIsLaunching(false)
    }
  }

  const handleSyncProfile = async () => {
    try {
      setIsSyncing(true)
      setSyncMessage(null)
      setError(null)
      const res = await recommendationsApi.syncProfile(learnerId)
      setSyncMessage(`Profile synchronized with ${res.total_events_processed} telemetry events.`)
      if (onProfileSynced) {
        onProfileSynced()
      }
    } catch (err: unknown) {
      console.error('Failed to sync profile:', err)
      setError('Failed to synchronize profile weights.')
    } finally {
      setIsSyncing(false)
    }
  }

  if (loading) {
    return (
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm animate-pulse">
        <div className="h-5 bg-slate-200 rounded w-1/3 mb-4"></div>
        <div className="h-8 bg-slate-100 rounded w-3/4 mb-3"></div>
        <div className="h-4 bg-slate-100 rounded w-full mb-2"></div>
        <div className="h-4 bg-slate-100 rounded w-2/3"></div>
      </div>
    )
  }

  if (!recommendation) {
    return (
      <div className="bg-slate-50 border border-dashed border-slate-300 rounded-2xl p-8 text-center text-slate-500">
        <p className="text-base font-medium">No active recommendation available.</p>
        <p className="text-sm text-slate-400 mt-1">Select a student or complete practice activities to generate suggestions.</p>
      </div>
    )
  }

  const confidenceColor =
    recommendation.confidence_level === 'high'
      ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
      : recommendation.confidence_level === 'medium'
      ? 'bg-blue-50 text-blue-700 border-blue-200'
      : 'bg-amber-50 text-amber-700 border-amber-200'

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden transition-all duration-200 hover:shadow-md">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-brand-50/90 to-teal-50/60 px-6 py-4 border-b border-slate-100 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <span className="flex h-2.5 w-2.5 rounded-full bg-brand-700 ring-4 ring-brand-100" />
          <h3 className="text-xs font-bold uppercase tracking-wider text-brand-950">
            Recommended Next Step
          </h3>
        </div>
        <div className="flex items-center gap-2">
          <span
            className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border capitalize ${confidenceColor}`}
          >
            {recommendation.confidence_level} Confidence ({Math.round(recommendation.confidence_score * 100)}%)
          </span>
          <span className="text-xs text-slate-400">
            {recommendation.evidence_event_count} Evidence Events
          </span>
        </div>
      </div>

      <div className="p-6">
        {/* Recommended Target Title & Badges */}
        <div className="mb-4">
          <h4 className="text-xl font-bold text-slate-900 leading-snug">
            {recommendation.objective_title}
          </h4>
          <div className="mt-3 flex flex-wrap items-center gap-2">
            <span className="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-semibold bg-brand-50 text-brand-900 border border-brand-200/70 capitalize">
              Modality: {recommendation.recommended_modality}
            </span>
            <span className="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-semibold bg-teal-50 text-teal-800 border border-teal-200/70 capitalize">
              Activity: {recommendation.recommended_activity_type.replace('_', ' ')}
            </span>
            <span className="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-semibold bg-amber-50 text-amber-900 border border-amber-200/70 capitalize">
              Strategy: {recommendation.recommended_strategy.replace('_', ' ')}
            </span>
            <span className="inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-semibold bg-slate-100 text-slate-700 border border-slate-200">
              Tier {recommendation.difficulty_level} / 5
            </span>
          </div>
        </div>

        {/* Explainable Rationale Box */}
        <div className="bg-slate-50/80 rounded-xl p-4 border border-slate-200/70 mb-5">
          <p className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">
            Pedagogical Rationale
          </p>
          <p className="text-xs sm:text-sm text-slate-700 leading-relaxed">
            {recommendation.rationale}
          </p>
          {recommendation.applied_constraints.length > 0 && (
            <div className="mt-3 pt-3 border-t border-slate-200/60 flex flex-wrap items-center gap-1.5">
              <span className="text-xs text-slate-400 font-medium mr-1">Constraints:</span>
              {recommendation.applied_constraints.map((c, idx) => (
                <span
                  key={idx}
                  className="inline-flex items-center px-2 py-0.5 rounded text-[11px] bg-slate-200/70 text-slate-700 font-mono"
                >
                  {c}
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Notifications & Error State */}
        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-xl text-xs text-red-600">
            {error}
          </div>
        )}
        {syncMessage && (
          <div className="mb-4 p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-xs text-emerald-700">
            {syncMessage}
          </div>
        )}

        {/* Action Controls */}
        <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
          <button
            type="button"
            onClick={handleSyncProfile}
            disabled={isSyncing || isLaunching}
            className="px-3.5 py-2 text-xs font-semibold text-slate-700 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 rounded-xl transition-colors disabled:opacity-50"
          >
            {isSyncing ? 'Syncing Profile...' : 'Update Profile Weights'}
          </button>

          <button
            type="button"
            onClick={handleLaunchActivity}
            disabled={isLaunching || isSyncing}
            className="px-5 py-2.5 text-sm font-semibold text-white bg-brand-800 hover:bg-brand-900 rounded-xl shadow-xs hover:shadow transition-all disabled:opacity-50 flex items-center gap-2"
          >
            {isLaunching ? (
              <>
                <svg className="animate-spin h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                </svg>
                Generating Activity...
              </>
            ) : (
              <>
                Start Recommended Activity
                <span aria-hidden="true">&rarr;</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  )
}
