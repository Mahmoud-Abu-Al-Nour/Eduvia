import React, { useEffect, useState } from "react";
import { 
  Users, 
  CheckCircle2, 
  AlertTriangle, 
  Target, 
  Sparkles, 
  FileText, 
  ArrowRight, 
  RefreshCw,
  Info,
  ShieldAlert
} from "lucide-react";
import { teachersApi } from "@/services/api";
import type { TeacherDashboardOverview, InterventionAlert } from "@/types";

interface TeacherOverviewProps {
  onSelectLearnerForIEP?: (learnerId: string, learnerName: string) => void;
  onNavigateTab?: (tab: string) => void;
}

export const TeacherOverview: React.FC<TeacherOverviewProps> = ({
  onSelectLearnerForIEP,
  onNavigateTab,
}) => {
  const [overview, setOverview] = useState<TeacherDashboardOverview | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [alertFilter, setAlertFilter] = useState<string>("all");

  const loadDashboard = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await teachersApi.getDashboardOverview();
      setOverview(data);
    } catch (err: any) {
      console.error("Failed to load teacher dashboard overview:", err);
      setError(err?.message || "Failed to load dashboard overview. Please ensure backend is running.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadDashboard();
  }, []);

  if (loading) {
    return (
      <div className="space-y-6" aria-busy="true" aria-live="polite">
        <div className="flex items-center justify-between">
          <div className="h-8 w-48 bg-gray-200 rounded-lg animate-pulse" />
          <div className="h-9 w-24 bg-gray-200 rounded-lg animate-pulse" />
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-32 bg-white rounded-2xl border border-gray-100 p-6 animate-pulse" />
          ))}
        </div>
        <div className="h-64 bg-white rounded-2xl border border-gray-100 p-6 animate-pulse" />
      </div>
    );
  }

  if (error || !overview) {
    return (
      <div className="bg-rose-50 border border-rose-200 rounded-2xl p-6 text-center" role="alert">
        <AlertTriangle className="w-10 h-10 text-rose-500 mx-auto mb-3" />
        <h3 className="text-lg font-semibold text-rose-900 mb-1">Dashboard Loading Error</h3>
        <p className="text-sm text-rose-700 max-w-md mx-auto mb-4">{error || "Unable to retrieve dashboard metrics."}</p>
        <button
          onClick={() => void loadDashboard()}
          className="inline-flex items-center gap-2 px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white text-sm font-medium rounded-xl transition-colors focus:ring-2 focus:ring-rose-500 focus:outline-none"
        >
          <RefreshCw className="w-4 h-4" />
          Try Again
        </button>
      </div>
    );
  }

  const filteredAlerts = overview.pending_alerts.filter((alert) => {
    if (alertFilter === "all") return true;
    return alert.severity === alertFilter;
  });

  return (
    <div className="space-y-8 max-w-6xl">
      {/* Header with Welcome and Refresh */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 tracking-tight">
            Welcome, {overview.teacher_name || "Educator"}
          </h2>
          <p className="text-sm text-gray-600 mt-0.5">
            Holistic pedagogical overview across your assigned learners and learning objectives.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={() => void loadDashboard()}
            className="inline-flex items-center gap-2 px-3.5 py-2 bg-white border border-gray-200 text-gray-700 hover:bg-gray-50 text-sm font-medium rounded-xl shadow-sm transition-colors focus:ring-2 focus:ring-blue-500 focus:outline-none"
            aria-label="Refresh Dashboard Metrics"
          >
            <RefreshCw className="w-4 h-4 text-gray-500" />
            Refresh
          </button>
          {onNavigateTab && (
            <button
              onClick={() => onNavigateTab("cohort")}
              className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-xl shadow-sm transition-colors focus:ring-2 focus:ring-blue-500 focus:outline-none"
            >
              <Users className="w-4 h-4" />
              Classroom Cohort
              <ArrowRight className="w-4 h-4 ml-0.5" />
            </button>
          )}
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {/* Card 1: Assigned Learners */}
        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm relative overflow-hidden">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold uppercase tracking-wider text-gray-500">Assigned Learners</span>
            <div className="w-9 h-9 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center">
              <Users className="w-5 h-5" />
            </div>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-bold text-gray-900">{overview.total_assigned_learners}</span>
            <span className="text-xs font-medium text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full">
              {overview.active_learners_count} active
            </span>
          </div>
          <p className="text-xs text-gray-500 mt-2">Active in verified assignments</p>
        </div>

        {/* Card 2: Completed Activities */}
        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm relative overflow-hidden">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold uppercase tracking-wider text-gray-500">Completed Practice</span>
            <div className="w-9 h-9 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5" />
            </div>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-bold text-gray-900">{overview.total_completed_activities}</span>
            <span className="text-xs text-gray-500">sessions</span>
          </div>
          <p className="text-xs text-gray-500 mt-2">Activities verified across cohort</p>
        </div>

        {/* Card 3: Cohort Accuracy */}
        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm relative overflow-hidden">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold uppercase tracking-wider text-gray-500">Cohort Accuracy</span>
            <div className="w-9 h-9 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
              <Target className="w-5 h-5" />
            </div>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-bold text-gray-900">
              {(overview.average_cohort_accuracy * 100).toFixed(0)}%
            </span>
            <span className="text-xs text-gray-500">mean score</span>
          </div>
          <p className="text-xs text-gray-500 mt-2">Aggregated performance mastery</p>
        </div>

        {/* Card 4: Actionable Alerts */}
        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm relative overflow-hidden">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold uppercase tracking-wider text-gray-500">Pedagogical Alerts</span>
            <div className={`w-9 h-9 rounded-xl flex items-center justify-center ${overview.pending_alerts.length > 0 ? 'bg-amber-50 text-amber-600' : 'bg-slate-50 text-slate-500'}`}>
              <ShieldAlert className="w-5 h-5" />
            </div>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-bold text-gray-900">{overview.pending_alerts.length}</span>
            {overview.pending_alerts.length > 0 && (
              <span className="text-xs font-medium text-amber-700 bg-amber-50 px-2 py-0.5 rounded-full">
                Attention needed
              </span>
            )}
          </div>
          <p className="text-xs text-gray-500 mt-2">Deterministic signal triggers</p>
        </div>
      </div>

      {/* Intervention Alerts Section */}
      <section aria-labelledby="alerts-heading" className="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
        <div className="p-6 border-b border-gray-100 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <h3 id="alerts-heading" className="text-lg font-bold text-gray-900">
                Pedagogical Intervention Alerts
              </h3>
              <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-gray-100 text-gray-700">
                {filteredAlerts.length}
              </span>
            </div>
            <p className="text-xs text-gray-500 mt-0.5">
              Observable learning signals calculated deterministically from recent student attempts.
            </p>
          </div>

          {/* Filter severity tabs */}
          <div className="flex items-center gap-1.5 bg-gray-100 p-1 rounded-xl text-xs font-medium" role="tablist" aria-label="Alert Severity Filter">
            {(["all", "priority", "advisory", "info"] as const).map((sev) => (
              <button
                key={sev}
                role="tab"
                aria-selected={alertFilter === sev}
                onClick={() => setAlertFilter(sev)}
                className={`px-3 py-1.5 rounded-lg capitalize transition-colors ${
                  alertFilter === sev
                    ? "bg-white text-gray-900 shadow-sm font-semibold"
                    : "text-gray-600 hover:text-gray-900"
                }`}
              >
                {sev}
              </button>
            ))}
          </div>
        </div>

        {filteredAlerts.length === 0 ? (
          <div className="p-12 text-center">
            <div className="w-12 h-12 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center mx-auto mb-3">
              <CheckCircle2 className="w-6 h-6" />
            </div>
            <h4 className="text-base font-semibold text-gray-900 mb-1">No Active Alerts</h4>
            <p className="text-sm text-gray-500 max-w-sm mx-auto">
              All assigned learners are currently progressing within standard accuracy and scaffolding parameters.
            </p>
          </div>
        ) : (
          <div className="divide-y divide-gray-100">
            {filteredAlerts.map((alert: InterventionAlert) => {
              const badgeClass =
                alert.severity === "priority"
                  ? "bg-rose-50 text-rose-700 border-rose-200"
                  : alert.severity === "advisory"
                  ? "bg-amber-50 text-amber-700 border-amber-200"
                  : "bg-blue-50 text-blue-700 border-blue-200";

              return (
                <div key={alert.id} className="p-6 hover:bg-gray-50/50 transition-colors">
                  <div className="flex flex-col lg:flex-row lg:items-start justify-between gap-4">
                    <div className="flex-1 space-y-2">
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold border ${badgeClass}`}>
                          {alert.severity.toUpperCase()}
                        </span>
                        <span className="font-semibold text-gray-900 text-base">
                          {alert.learner_display_name}
                        </span>
                        <span className="text-xs text-gray-400">•</span>
                        <span className="text-xs text-gray-500 font-medium">
                          Window: {alert.evidence_window}
                        </span>
                      </div>

                      <p className="text-sm text-gray-800 font-medium leading-relaxed">
                        {alert.summary}
                      </p>

                      <div className="bg-slate-50 border border-slate-200/80 rounded-xl p-3 text-xs text-slate-700 flex items-start gap-2">
                        <Info className="w-4 h-4 text-blue-600 mt-0.5 shrink-0" />
                        <div>
                          <strong className="font-semibold text-slate-900">Pedagogical Recommendation:</strong>{" "}
                          {alert.recommended_pedagogical_action}
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center gap-2 lg:self-center shrink-0">
                      {onSelectLearnerForIEP && (
                        <button
                          onClick={() => onSelectLearnerForIEP(alert.learner_id, alert.learner_display_name)}
                          className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-white border border-gray-200 hover:bg-gray-50 text-gray-700 text-xs font-semibold shadow-sm transition-colors focus:ring-2 focus:ring-blue-500 focus:outline-none"
                        >
                          <FileText className="w-3.5 h-3.5 text-blue-600" />
                          Generate IEP Report
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </section>

      {/* Recent Adaptive Decisions (Phase 8 integration preview) */}
      {overview.recent_recommendations && overview.recent_recommendations.length > 0 && (
        <section aria-labelledby="recommendations-heading" className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 id="recommendations-heading" className="text-lg font-bold text-gray-900 flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-indigo-600" />
                Recent Adaptive Engine Decisions
              </h3>
              <p className="text-xs text-gray-500 mt-0.5">
                Authoritative recommendations generated by Phase 8 Adaptive Intelligence.
              </p>
            </div>
            {onNavigateTab && (
              <button
                onClick={() => onNavigateTab("recommendations")}
                className="text-xs font-semibold text-indigo-600 hover:text-indigo-700 flex items-center gap-1"
              >
                Open Adaptive Engine
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {overview.recent_recommendations.map((rec, idx) => (
              <div key={idx} className="border border-gray-100 rounded-xl p-4 bg-gray-50/50 hover:bg-white hover:border-gray-200 transition-all">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-bold text-gray-900 truncate max-w-[200px]">
                    {rec.objective_title}
                  </span>
                  <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-100 capitalize">
                    {rec.recommended_modality}
                  </span>
                </div>
                <p className="text-xs text-gray-600 line-clamp-2 mb-3">
                  {rec.rationale}
                </p>
                <div className="flex items-center justify-between text-[11px] text-gray-500 pt-2 border-t border-gray-100">
                  <span>Confidence: <strong className="text-gray-700 capitalize">{rec.confidence_level}</strong></span>
                  <span>Scaffolding: Tier {rec.scaffolding_tier}</span>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
};
