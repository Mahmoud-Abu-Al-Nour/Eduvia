import React, { useEffect, useState } from "react";
import {
  Users,
  CheckCircle2,
  AlertTriangle,
  Target,
  FileText,
  ArrowRight,
  RefreshCw,
  Info,
  ShieldAlert,
  Compass,
} from "lucide-react";
import { teachersApi } from "@/services/api";
import type { TeacherDashboardOverview, InterventionAlert } from "@/types";
import { Card, CardContent, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";

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
          <Skeleton className="h-8 w-48" />
          <Skeleton className="h-9 w-24" />
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} className="h-32 rounded-xl" />
          ))}
        </div>
        <Skeleton className="h-64 rounded-xl" />
      </div>
    );
  }

  if (error || !overview) {
    return (
      <Card className="border-rose-200 bg-rose-50/50 p-8 text-center max-w-lg mx-auto" role="alert">
        <AlertTriangle className="w-10 h-10 text-rose-600 mx-auto mb-3" />
        <h3 className="text-base font-semibold text-rose-900 mb-1">Dashboard Unavailable</h3>
        <p className="text-xs text-rose-700 max-w-md mx-auto mb-4">
          We couldn&apos;t load the latest classroom overview.
          {error && <span className="block text-[11px] text-rose-600/80 mt-1 font-mono">{error}</span>}
        </p>
        <Button
          onClick={() => void loadDashboard()}
          variant="destructive"
          size="sm"
          className="mx-auto"
        >
          <RefreshCw className="w-3.5 h-3.5 mr-1.5" />
          Try Again
        </Button>
      </Card>
    );
  }

  const alertsList = overview.pending_alerts || overview.recent_alerts || [];
  const filteredAlerts = alertsList.filter((alert: any) => {
    if (alertFilter === "all") return true;
    return alert.severity === alertFilter;
  });

  return (
    <div className="space-y-8 max-w-6xl">
      {/* Header with Welcome and Actions */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight">
            Welcome, {overview.teacher_name || "Educator"}
          </h2>
          <p className="text-xs sm:text-sm text-slate-600 mt-1">
            Empirical pedagogical briefing across your assigned learners and objective milestones.
          </p>
        </div>
        <div className="flex items-center gap-2.5">
          <Button
            onClick={() => void loadDashboard()}
            variant="outline"
            size="sm"
            aria-label="Refresh Dashboard Metrics"
          >
            <RefreshCw className="w-3.5 h-3.5 mr-1.5 text-slate-500" />
            Refresh Data
          </Button>
          {onNavigateTab && (
            <Button
              onClick={() => onNavigateTab("cohort")}
              variant="default"
              size="sm"
            >
              <Users className="w-3.5 h-3.5 mr-1.5" />
              Classroom Cohort
              <ArrowRight className="w-3.5 h-3.5 ml-1" />
            </Button>
          )}
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
        {/* Card 1: Assigned Learners */}
        <Card className="border-slate-200/80 bg-white">
          <CardContent className="p-5">
            <div className="flex items-center justify-between mb-3">
              <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500">
                Assigned Learners
              </span>
              <div className="w-8 h-8 rounded-lg bg-brand-50 text-brand-800 flex items-center justify-center">
                <Users className="w-4 h-4" />
              </div>
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-bold text-slate-900">{overview.total_assigned_learners}</span>
              <Badge variant="success" className="text-[10px]">
                {overview.active_learners_count} active
              </Badge>
            </div>
            <p className="text-[11px] text-slate-500 mt-1.5">Classroom roster cohort</p>
          </CardContent>
        </Card>

        {/* Card 2: Completed Practice */}
        <Card className="border-slate-200/80 bg-white">
          <CardContent className="p-5">
            <div className="flex items-center justify-between mb-3">
              <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500">
                Completed Practice
              </span>
              <div className="w-8 h-8 rounded-lg bg-teal-50 text-teal-800 flex items-center justify-center">
                <CheckCircle2 className="w-4 h-4" />
              </div>
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-bold text-slate-900">{overview.total_completed_activities}</span>
              <span className="text-xs text-slate-500 font-medium">sessions</span>
            </div>
            <p className="text-[11px] text-slate-500 mt-1.5">Recorded learner attempts</p>
          </CardContent>
        </Card>

        {/* Card 3: Cohort Accuracy */}
        <Card className="border-slate-200/80 bg-white">
          <CardContent className="p-5">
            <div className="flex items-center justify-between mb-3">
              <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500">
                Cohort Accuracy
              </span>
              <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center">
                <Target className="w-4 h-4" />
              </div>
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-bold text-slate-900">
                {(((overview.average_cohort_accuracy ?? overview.cohort_average_accuracy_7d) || 0) * 100).toFixed(0)}%
              </span>
              <span className="text-xs text-slate-500 font-medium">mean</span>
            </div>
            <p className="text-[11px] text-slate-500 mt-1.5">Mastery progress index</p>
          </CardContent>
        </Card>

        {/* Card 4: Actionable Alerts */}
        <Card className="border-slate-200/80 bg-white">
          <CardContent className="p-5">
            <div className="flex items-center justify-between mb-3">
              <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500">
                Pedagogical Alerts
              </span>
              <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${alertsList.length > 0 ? 'bg-amber-50 text-amber-700' : 'bg-slate-100 text-slate-500'}`}>
                <ShieldAlert className="w-4 h-4" />
              </div>
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-bold text-slate-900">{alertsList.length}</span>
              {alertsList.length > 0 && (
                <Badge variant="warning" className="text-[10px]">
                  Action suggested
                </Badge>
              )}
            </div>
            <p className="text-[11px] text-slate-500 mt-1.5">Observed behavioral indicators</p>
          </CardContent>
        </Card>
      </div>

      {/* Intervention Alerts Section */}
      <Card className="border-slate-200/90 shadow-xs bg-white overflow-hidden">
        <div className="p-5 border-b border-slate-200/80 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <CardTitle className="text-base font-bold text-slate-900">
                Teacher Intervention Attention List
              </CardTitle>
              <Badge variant="secondary" className="text-[11px] font-bold">
                {filteredAlerts.length}
              </Badge>
            </div>
            <CardDescription className="text-xs mt-0.5">
              Empirical learning signals identified from recent attempts requiring pedagogical review.
            </CardDescription>
          </div>

          {/* Filter severity tabs */}
          <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-lg text-xs" role="tablist" aria-label="Alert Severity Filter">
            {(["all", "priority", "advisory", "info"] as const).map((sev) => (
              <button
                key={sev}
                role="tab"
                aria-selected={alertFilter === sev}
                onClick={() => setAlertFilter(sev)}
                className={`px-2.5 py-1 rounded-md capitalize text-xs transition-all font-medium ${
                  alertFilter === sev
                    ? "bg-white text-slate-900 shadow-2xs font-semibold"
                    : "text-slate-600 hover:text-slate-900"
                }`}
              >
                {sev}
              </button>
            ))}
          </div>
        </div>

        {filteredAlerts.length === 0 ? (
          <div className="p-12 text-center">
            <div className="w-12 h-12 rounded-full bg-emerald-50 text-emerald-700 flex items-center justify-center mx-auto mb-3">
              <CheckCircle2 className="w-6 h-6" />
            </div>
            <h4 className="text-sm font-semibold text-slate-900 mb-1">No Active Intervention Alerts</h4>
            <p className="text-xs text-slate-500 max-w-sm mx-auto">
              All learners are currently progressing within standard difficulty bounds and assistance levels.
            </p>
          </div>
        ) : (
          <div className="divide-y divide-slate-100">
            {filteredAlerts.map((alert: InterventionAlert) => {
              const variant =
                alert.severity === "priority"
                  ? "destructive"
                  : alert.severity === "advisory"
                  ? "warning"
                  : "secondary";

              return (
                <div key={alert.id || alert.alert_id} className="p-5 hover:bg-slate-50/60 transition-colors">
                  <div className="flex flex-col lg:flex-row lg:items-start justify-between gap-4">
                    <div className="flex-1 space-y-2">
                      <div className="flex items-center gap-2 flex-wrap">
                        <Badge variant={variant} className="text-[10px] uppercase font-bold tracking-wider">
                          {alert.severity === "priority" && <AlertTriangle className="w-3 h-3 mr-1 inline" />}
                          {alert.severity}
                        </Badge>
                        <span className="font-semibold text-slate-900 text-sm">
                          {alert.learner_display_name}
                        </span>
                        <span className="text-xs text-slate-300">•</span>
                        <span className="text-[11px] text-slate-500 font-medium">
                          Window: {alert.evidence_window || "Last 7 days"}
                        </span>
                      </div>

                      <p className="text-xs text-slate-700 font-medium leading-relaxed">
                        {alert.summary || alert.message}
                      </p>

                      <div className="bg-brand-50/60 border border-brand-100 rounded-lg p-2.5 text-xs text-brand-950 flex items-start gap-2">
                        <Info className="w-3.5 h-3.5 text-brand-800 mt-0.5 shrink-0" />
                        <div>
                          <strong className="font-semibold text-brand-900">Pedagogical Recommendation:</strong>{" "}
                          <span className="text-brand-950">{alert.recommended_pedagogical_action || alert.recommended_action}</span>
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center gap-2 lg:self-center shrink-0">
                      {onSelectLearnerForIEP && (
                        <Button
                          onClick={() => onSelectLearnerForIEP(alert.learner_id, alert.learner_display_name)}
                          variant="outline"
                          size="sm"
                          className="text-xs"
                        >
                          <FileText className="w-3.5 h-3.5 mr-1.5 text-brand-800" />
                          IEP Report
                        </Button>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </Card>

      {/* Recent Adaptive Decisions */}
      {overview.recent_recommendations && overview.recent_recommendations.length > 0 && (
        <Card className="border-slate-200/90 shadow-xs bg-white p-5">
          <div className="flex items-center justify-between mb-4">
            <div>
              <CardTitle className="text-base font-bold text-slate-900 flex items-center gap-2">
                <Compass className="w-4 h-4 text-brand-800" />
                Recent Adaptive Decisions
              </CardTitle>
              <CardDescription className="text-xs mt-0.5">
                Teacher-in-the-loop recommendations based on learner response patterns.
              </CardDescription>
            </div>
            {onNavigateTab && (
              <button
                onClick={() => onNavigateTab("recommendations")}
                className="text-xs font-semibold text-brand-800 hover:text-brand-900 flex items-center gap-1"
              >
                <span>Adaptive Engine</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
            {overview.recent_recommendations.map((rec, idx) => (
              <div key={idx} className="border border-slate-200/80 rounded-xl p-3.5 bg-slate-50/50 hover:bg-white hover:border-slate-300 transition-all space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-900 truncate max-w-[200px]">
                    {rec.objective_title}
                  </span>
                  <Badge variant="secondary" className="text-[10px] capitalize">
                    {rec.recommended_modality}
                  </Badge>
                </div>
                <p className="text-xs text-slate-600 line-clamp-2 leading-relaxed">
                  {rec.rationale}
                </p>
                <div className="flex items-center justify-between text-[10px] text-slate-500 pt-2 border-t border-slate-200/60">
                  <span>Confidence: <strong className="text-slate-700 capitalize">{rec.confidence_level}</strong></span>
                  <span>Scaffolding: Tier {rec.scaffolding_tier}</span>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
};
