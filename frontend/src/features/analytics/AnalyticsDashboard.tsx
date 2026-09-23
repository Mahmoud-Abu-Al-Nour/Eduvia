import React, { useEffect, useState } from "react";
import api from "@/services/api";
import {
  Learner,
  LearnerAnalyticsSummary,
  LearnerMasteryReport,
  LearnerProgressReport,
} from "@/types";
import {
  BarChart3,
  Award,
  Clock,
  HelpCircle,
  CheckCircle2,
  Calendar,
  Layers,
  Sparkles,
  ArrowRight,
  User,
} from "lucide-react";

export const AnalyticsDashboard: React.FC = () => {
  const [learners, setLearners] = useState<Learner[]>([]);
  const [selectedLearnerId, setSelectedLearnerId] = useState<string>("");
  const [loadingLearners, setLoadingLearners] = useState<boolean>(true);

  const [summary, setSummary] = useState<LearnerAnalyticsSummary | null>(null);
  const [mastery, setMastery] = useState<LearnerMasteryReport | null>(null);
  const [progress, setProgress] = useState<LearnerProgressReport | null>(null);
  const [loadingAnalytics, setLoadingAnalytics] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch all learners assigned to this teacher
  useEffect(() => {
    const fetchLearners = async () => {
      try {
        setLoadingLearners(true);
        const data = await api.get<Learner[]>("/learners");
        setLearners(data);
        if (data.length > 0) {
          setSelectedLearnerId(data[0].id);
        }
      } catch (err: any) {
        setError(err.message || "Failed to load learners list.");
      } finally {
        setLoadingLearners(false);
      }
    };
    void fetchLearners();
  }, []);

  // Fetch analytics for selected learner
  useEffect(() => {
    if (!selectedLearnerId) return;

    const fetchAnalytics = async () => {
      try {
        setLoadingAnalytics(true);
        setError(null);
        const [sumData, mastData, progData] = await Promise.all([
          api.analytics.getLearnerSummary(selectedLearnerId),
          api.analytics.getLearnerMastery(selectedLearnerId),
          api.analytics.getLearnerProgress(selectedLearnerId, 30),
        ]);
        setSummary(sumData);
        setMastery(mastData);
        setProgress(progData);
      } catch (err: any) {
        setError(err.message || "Failed to load performance analytics.");
      } finally {
        setLoadingAnalytics(false);
      }
    };

    void fetchAnalytics();
  }, [selectedLearnerId]);

  const selectedLearner = learners.find((l) => l.id === selectedLearnerId);

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      {/* Header & Learner Selector */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2.5 mb-1">
            <div className="w-9 h-9 rounded-xl bg-brand-50 flex items-center justify-center text-brand-800">
              <BarChart3 className="w-5 h-5" />
            </div>
            <h2 className="text-xl font-bold text-slate-900">Learning Analytics &amp; Mastery</h2>
          </div>
          <p className="text-xs sm:text-sm text-slate-600">
            Authoritative performance evaluation, objective mastery tracking, and modality breakdowns.
          </p>
        </div>

        {/* Learner Dropdown */}
        <div className="flex items-center gap-2.5 bg-slate-50 p-2 rounded-xl border border-slate-200/80">
          <label htmlFor="learner-selector" className="text-xs font-semibold text-slate-700 flex items-center gap-1.5 whitespace-nowrap">
            <User className="w-3.5 h-3.5 text-slate-500" />
            <span>Learner:</span>
          </label>
          {loadingLearners ? (
            <div className="h-9 w-44 bg-slate-200 rounded-lg animate-pulse" />
          ) : (
            <select
              id="learner-selector"
              value={selectedLearnerId}
              onChange={(e) => setSelectedLearnerId(e.target.value)}
              className="px-3 py-1.5 bg-white border border-slate-300 rounded-lg text-xs font-semibold text-slate-900 focus:ring-2 focus:ring-brand-700 focus:outline-none shadow-2xs"
            >
              {learners.map((l) => (
                <option key={l.id} value={l.id}>
                  {l.name} ({l.learning_level})
                </option>
              ))}
              {learners.length === 0 && <option value="">No learners available</option>}
            </select>
          )}
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-xs text-rose-800">
          {error}
        </div>
      )}

      {loadingAnalytics ? (
        <div className="space-y-6">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-32 bg-slate-100 rounded-2xl animate-pulse" />
            ))}
          </div>
          <div className="h-64 bg-slate-100 rounded-2xl animate-pulse" />
        </div>
      ) : summary && summary.total_events === 0 ? (
        /* Empty State: Zero activities recorded yet */
        <div className="bg-white p-12 rounded-2xl border border-slate-200/80 text-center space-y-4 shadow-xs">
          <div className="w-14 h-14 rounded-full bg-brand-50 text-brand-800 flex items-center justify-center mx-auto">
            <Sparkles className="w-7 h-7" />
          </div>
          <h3 className="text-lg font-bold text-slate-900">
            No Performance Events Recorded Yet
          </h3>
          <p className="text-xs text-slate-600 max-w-md mx-auto leading-relaxed">
            {selectedLearner?.name || "This student"} has not completed any learning activities yet. 
            Once they practice activities in the Learner Player, objective mastery and sensory metrics will populate here.
          </p>
          <a
            href="/learn"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-brand-800 text-white text-xs font-semibold hover:bg-brand-900 transition-colors shadow-xs"
          >
            <span>Launch Activity Session</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </a>
        </div>
      ) : summary ? (
        /* Populated Analytics Dashboard */
        <div className="space-y-8">
          {/* Key Metric KPI Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
            {/* Total Activities */}
            <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-xs">
              <div className="flex items-center justify-between text-slate-500 mb-2">
                <span className="text-[11px] font-semibold tracking-wider uppercase">Completed Activities</span>
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              </div>
              <div className="text-3xl font-extrabold text-slate-900">
                {summary.completed_activities}
              </div>
              <p className="text-[11px] text-slate-500 mt-1">Recorded attempts: {summary.total_events}</p>
            </div>

            {/* Overall Accuracy */}
            <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-xs">
              <div className="flex items-center justify-between text-slate-500 mb-2">
                <span className="text-[11px] font-semibold tracking-wider uppercase">Overall Accuracy</span>
                <Award className="w-4 h-4 text-brand-800" />
              </div>
              <div className="text-3xl font-extrabold text-brand-800">
                {Math.round(summary.overall_accuracy * 100)}%
              </div>
              <p className="text-[11px] text-slate-500 mt-1">Average score: {(summary.avg_score * 100).toFixed(1)}%</p>
            </div>

            {/* Avg Response Latency */}
            <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-xs">
              <div className="flex items-center justify-between text-slate-500 mb-2">
                <span className="text-[11px] font-semibold tracking-wider uppercase">Avg Response Time</span>
                <Clock className="w-4 h-4 text-amber-600" />
              </div>
              <div className="text-3xl font-extrabold text-slate-900">
                {(summary.avg_response_time_ms / 1000).toFixed(1)}s
              </div>
              <p className="text-[11px] text-slate-500 mt-1">Cognitive processing speed</p>
            </div>

            {/* Assistance Level */}
            <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-xs">
              <div className="flex items-center justify-between text-gray-500 mb-2">
                <span className="text-xs font-semibold tracking-wider uppercase">Avg Assistance</span>
                <HelpCircle className="w-4 h-4 text-blue-600" />
              </div>
              <div className="text-3xl font-extrabold text-gray-900">
                Level {summary.avg_assistance_level.toFixed(1)}
              </div>
              <p className="text-xs text-gray-500 mt-1">{summary.avg_hints_per_activity.toFixed(1)} hints/activity</p>
            </div>
          </div>

          {/* Objective Mastery Section */}
          {mastery && (
            <div className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm space-y-6">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <h3 className="text-lg font-bold text-gray-900">Curriculum Objective Mastery</h3>
                  <p className="text-xs text-gray-600 mt-0.5">
                    Deterministic evaluation: Accuracy ≥ 80% with independent / minimal assistance (≤ Level 1).
                  </p>
                </div>
                <div className="flex items-center gap-3">
                  <div className="px-3 py-1.5 rounded-xl bg-teal-50 text-teal-700 text-xs font-semibold">
                    {mastery.mastered_count} Mastered
                  </div>
                  <div className="px-3 py-1.5 rounded-xl bg-blue-50 text-blue-700 text-xs font-semibold">
                    {mastery.in_progress_count} In Progress
                  </div>
                  <div className="text-sm font-bold text-gray-900">
                    {mastery.mastery_percentage}% Overall Mastery
                  </div>
                </div>
              </div>

              {/* Objectives List */}
              <div className="divide-y divide-gray-100 border border-gray-100 rounded-xl overflow-hidden">
                {mastery.objectives.length === 0 ? (
                  <div className="p-6 text-center text-sm text-gray-500">
                    No curriculum objectives have been evaluated yet.
                  </div>
                ) : (
                  mastery.objectives.map((obj) => (
                    <div
                      key={obj.objective_id}
                      className="p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 hover:bg-gray-50/50 transition-colors"
                    >
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <span className="font-semibold text-sm text-gray-900">{obj.objective_title}</span>
                          <span className="px-2 py-0.5 rounded text-[11px] font-medium bg-gray-100 text-gray-600">
                            Diff {obj.difficulty_level}
                          </span>
                        </div>
                        <div className="flex items-center gap-4 text-xs text-gray-500">
                          <span>Attempts: {obj.total_attempts}</span>
                          <span>Avg Assistance: Level {obj.avg_assistance_level}</span>
                          {obj.last_attempt_at && (
                            <span>Last: {new Date(obj.last_attempt_at).toLocaleDateString()}</span>
                          )}
                        </div>
                      </div>

                      <div className="flex items-center gap-4">
                        <div className="text-right">
                          <div className="text-sm font-bold text-gray-900">{Math.round(obj.accuracy * 100)}%</div>
                          <div className="w-24 bg-gray-200 h-1.5 rounded-full overflow-hidden mt-1">
                            <div
                              className={`h-full rounded-full ${
                                obj.mastery_achieved ? "bg-teal-500" : "bg-indigo-500"
                              }`}
                              style={{ width: `${Math.min(100, Math.round(obj.accuracy * 100))}%` }}
                            />
                          </div>
                        </div>

                        <span
                          className={`px-3 py-1 rounded-full text-xs font-semibold ${
                            obj.status === "mastered"
                              ? "bg-teal-100 text-teal-800"
                              : obj.status === "in_progress"
                              ? "bg-indigo-100 text-indigo-800"
                              : "bg-gray-100 text-gray-600"
                          }`}
                        >
                          {obj.status === "mastered"
                            ? "Mastered"
                            : obj.status === "in_progress"
                            ? "In Progress"
                            : "Not Started"}
                        </span>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}

          {/* Modality Breakdown & Activity Types */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Sensory Modality Breakdown */}
            <div className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm space-y-4">
              <div className="flex items-center gap-2">
                <Layers className="w-5 h-5 text-indigo-600" />
                <h3 className="font-bold text-gray-900">Sensory Modality Efficacy</h3>
              </div>
              <p className="text-xs text-gray-600">
                Measures learner accuracy and required assistance across different sensory presentations.
              </p>

              <div className="space-y-3">
                {summary.modality_breakdown.map((mod) => (
                  <div key={mod.modality} className="p-3 bg-gray-50 rounded-xl flex items-center justify-between">
                    <div>
                      <div className="font-semibold text-sm capitalize text-gray-900">{mod.modality}</div>
                      <div className="text-xs text-gray-500">
                        {mod.total_events} events • Level {mod.avg_assistance_level.toFixed(1)} assist
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-bold text-gray-900">{Math.round(mod.accuracy * 100)}%</div>
                      <div className="text-xs text-gray-500">{(mod.avg_response_time_ms / 1000).toFixed(1)}s avg</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Longitudinal Activity Progress */}
            <div className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm space-y-4">
              <div className="flex items-center gap-2">
                <Calendar className="w-5 h-5 text-indigo-600" />
                <h3 className="font-bold text-gray-900">Recent Activity Timeline (30 Days)</h3>
              </div>
              <p className="text-xs text-gray-600">
                Daily activity engagement and accuracy consistency.
              </p>

              <div className="space-y-2.5 max-h-72 overflow-y-auto pr-1">
                {progress && progress.data_points.length > 0 ? (
                  progress.data_points.map((pt) => (
                    <div key={pt.date} className="p-3 bg-gray-50 rounded-xl flex items-center justify-between text-xs">
                      <span className="font-medium text-gray-800">{pt.date}</span>
                      <span className="text-gray-600">{pt.events_count} activities</span>
                      <span className="font-semibold text-indigo-600">{Math.round(pt.accuracy * 100)}% accuracy</span>
                    </div>
                  ))
                ) : (
                  <div className="p-6 text-center text-xs text-gray-500">
                    No longitudinal data points available.
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
};
export default AnalyticsDashboard;
