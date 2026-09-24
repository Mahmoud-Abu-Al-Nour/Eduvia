import React, { useEffect, useState } from "react";
import { 
  Users, 
  Target, 
  HelpCircle, 
  Award, 
  Calendar, 
  FileText, 
  RefreshCw, 
  AlertTriangle,
  ArrowUpDown,
  Search
} from "lucide-react";
import { teachersApi } from "@/services/api";
import type { CohortInsights, CohortLearnerSummary } from "@/types";

interface CohortInsightsViewProps {
  onSelectLearnerForIEP: (learnerId: string, learnerName: string) => void;
}

export const CohortInsightsView: React.FC<CohortInsightsViewProps> = ({
  onSelectLearnerForIEP,
}) => {
  const [days, setDays] = useState<number>(30);
  const [insights, setInsights] = useState<CohortInsights | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [sortField, setSortField] = useState<keyof CohortLearnerSummary>("display_name");
  const [sortAsc, setSortAsc] = useState<boolean>(true);

  const loadCohortInsights = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await teachersApi.getCohortInsights(days);
      setInsights(data);
    } catch (err: any) {
      console.error("Failed to load cohort insights:", err);
      setError(err?.message || "Failed to load classroom cohort insights.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadCohortInsights();
  }, [days]);

  const handleSort = (field: keyof CohortLearnerSummary) => {
    if (sortField === field) {
      setSortAsc(!sortAsc);
    } else {
      setSortField(field);
      setSortAsc(true);
    }
  };

  const rawLearners = insights?.learners || (insights as any)?.learner_summaries || [];
  const filteredLearners = rawLearners.filter((l: any) =>
    (l.display_name || l.name || "").toLowerCase().includes(searchQuery.toLowerCase()) ||
    (l.learning_level || "").toLowerCase().includes(searchQuery.toLowerCase())
  ).sort((a: any, b: any) => {
    const aVal = a[sortField] ?? (sortField === "display_name" ? a.name : undefined);
    const bVal = b[sortField] ?? (sortField === "display_name" ? b.name : undefined);
    if (aVal === undefined || aVal === null) return 1;
    if (bVal === undefined || bVal === null) return -1;
    if (typeof aVal === "string" && typeof bVal === "string") {
      return sortAsc ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
    }
    if (typeof aVal === "number" && typeof bVal === "number") {
      return sortAsc ? aVal - bVal : bVal - aVal;
    }
    return 0;
  });

  return (
    <div className="space-y-8 max-w-6xl">
      {/* Header with Date Range Filter */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 tracking-tight">
            Classroom & Cohort Performance Insights
          </h2>
          <p className="text-sm text-gray-600 mt-0.5">
            Aggregated learning progress and sensory modality distributions for your assigned learners.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 bg-white border border-gray-200 rounded-xl px-3 py-1.5 shadow-sm">
            <Calendar className="w-4 h-4 text-gray-500" />
            <label htmlFor="period-select" className="sr-only">Select Reporting Period</label>
            <select
              id="period-select"
              value={days}
              onChange={(e) => setDays(Number(e.target.value))}
              className="text-xs font-semibold text-gray-700 bg-transparent border-0 focus:ring-0 focus:outline-none cursor-pointer"
            >
              <option value={7}>Last 7 Days</option>
              <option value={14}>Last 14 Days</option>
              <option value={30}>Last 30 Days</option>
              <option value={90}>Last 90 Days</option>
              <option value={0}>All Time Baseline</option>
            </select>
          </div>

          <button
            onClick={() => void loadCohortInsights()}
            className="p-2 bg-white border border-gray-200 text-gray-700 hover:bg-gray-50 rounded-xl shadow-sm transition-colors focus:ring-2 focus:ring-teal-600 focus:outline-none"
            aria-label="Refresh Cohort Data"
          >
            <RefreshCw className="w-4 h-4 text-gray-500" />
          </button>
        </div>
      </div>

      {loading ? (
        <div className="space-y-6" aria-busy="true" aria-live="polite">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-28 bg-white rounded-2xl border border-gray-100 p-6 animate-pulse" />
            ))}
          </div>
          <div className="h-64 bg-white rounded-2xl border border-gray-100 p-6 animate-pulse" />
        </div>
      ) : error || !insights ? (
        <div className="bg-rose-50 border border-rose-200 rounded-2xl p-6 text-center" role="alert">
          <AlertTriangle className="w-10 h-10 text-rose-500 mx-auto mb-3" />
          <h3 className="text-lg font-semibold text-rose-900 mb-1">Classroom Cohort Data Unavailable</h3>
          <p className="text-sm text-rose-700 max-w-md mx-auto mb-4">{error || "We couldn't load the latest cohort analytics. Please retry or check server connection."}</p>
          <button
            onClick={() => void loadCohortInsights()}
            className="px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white text-sm font-medium rounded-xl transition-colors focus:ring-2 focus:ring-rose-500 focus:outline-none"
          >
            Retry Connection
          </button>
        </div>
      ) : (
        <>
          {/* Cohort KPIs */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            <div className="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-semibold text-gray-500 uppercase">Active In Period</span>
                <Users className="w-4 h-4 text-teal-700" />
              </div>
              <div className="text-2xl font-bold text-gray-900">
                {insights.active_learners_in_period}{" "}
                <span className="text-xs font-normal text-gray-500">/ {insights.total_cohort_learners} learners</span>
              </div>
              <p className="text-xs text-gray-500 mt-1">{insights.reporting_period}</p>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-semibold text-gray-500 uppercase">Cohort Accuracy</span>
                <Target className="w-4 h-4 text-teal-700" />
              </div>
              <div className="text-2xl font-bold text-gray-900">
                {(insights.cohort_accuracy * 100).toFixed(0)}%
              </div>
              <p className="text-xs text-gray-500 mt-1">Aggregated target accuracy</p>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-semibold text-gray-500 uppercase">Mean Assistance</span>
                <HelpCircle className="w-4 h-4 text-amber-600" />
              </div>
              <div className="text-2xl font-bold text-gray-900">
                {insights.cohort_avg_assistance_level.toFixed(2)}{" "}
                <span className="text-xs font-normal text-gray-500">/ 3.0</span>
              </div>
              <p className="text-xs text-gray-500 mt-1">Scaffolding reliance score</p>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-semibold text-gray-500 uppercase">Activities Completed</span>
                <Award className="w-4 h-4 text-emerald-700" />
              </div>
              <div className="text-2xl font-bold text-gray-900">
                {insights.total_activities_completed}
              </div>
              <p className="text-xs text-gray-500 mt-1">Verified practice iterations</p>
            </div>
          </div>

          {/* Aggregations Grid: Modality & Mastery Distribution */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Sensory Modality Distribution */}
            <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6">
              <h3 className="text-base font-bold text-gray-900 mb-1">Sensory Modality Engagement</h3>
              <p className="text-xs text-gray-500 mb-4">
                Telemetry interaction counts across presentation channels.
              </p>
              
              {Object.keys(insights.modality_distribution).length === 0 ? (
                <p className="text-xs text-gray-400 py-6 text-center">No modality events recorded in this period.</p>
              ) : (
                <div className="space-y-3">
                  {Object.entries(insights.modality_distribution).map(([mod, count]) => {
                    const total = Object.values(insights.modality_distribution).reduce((a, b) => a + b, 0) || 1;
                    const pct = Math.round((count / total) * 100);
                    return (
                      <div key={mod} className="space-y-1">
                        <div className="flex items-center justify-between text-xs font-medium">
                          <span className="capitalize text-gray-700 font-semibold">{mod}</span>
                          <span className="text-gray-500">{count} events ({pct}%)</span>
                        </div>
                        <div className="w-full bg-gray-100 rounded-full h-2 overflow-hidden">
                          <div
                            className="bg-teal-700 h-2 rounded-full transition-all duration-300"
                            style={{ width: `${pct}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>

            {/* Curriculum Mastery Status */}
            <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6">
              <h3 className="text-base font-bold text-gray-900 mb-1">Curriculum Mastery Breakdown</h3>
              <p className="text-xs text-gray-500 mb-4">
                Objective competency states across evaluated curriculum standards.
              </p>

              <div className="grid grid-cols-3 gap-3 pt-2">
                <div className="bg-emerald-50/70 border border-emerald-100 rounded-xl p-4 text-center">
                  <div className="text-2xl font-bold text-emerald-800">
                    {insights.mastery_status_counts["mastered"] || 0}
                  </div>
                  <div className="text-xs font-semibold text-emerald-700 mt-1 uppercase tracking-wide">
                    Mastered
                  </div>
                </div>

                <div className="bg-teal-50/70 border border-teal-100 rounded-xl p-4 text-center">
                  <div className="text-2xl font-bold text-teal-800">
                    {insights.mastery_status_counts["in_progress"] || 0}
                  </div>
                  <div className="text-xs font-semibold text-teal-700 mt-1 uppercase tracking-wide">
                    In Progress
                  </div>
                </div>

                <div className="bg-gray-50 border border-gray-200 rounded-xl p-4 text-center">
                  <div className="text-2xl font-bold text-gray-700">
                    {insights.mastery_status_counts["not_started"] || 0}
                  </div>
                  <div className="text-xs font-semibold text-gray-500 mt-1 uppercase tracking-wide">
                    Not Started
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Student Roster Table */}
          <section aria-labelledby="roster-heading" className="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
            <div className="p-6 border-b border-gray-100 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h3 id="roster-heading" className="text-lg font-bold text-gray-900">
                  Learner Roster & Progress
                </h3>
                <p className="text-xs text-gray-500 mt-0.5">
                  Individual performance metrics and 1-click IEP reporting.
                </p>
              </div>

              <div className="relative w-full sm:w-64">
                <Search className="w-4 h-4 text-gray-400 absolute left-3 top-2.5" />
                <input
                  type="text"
                  placeholder="Filter by name or level..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-9 pr-3 py-1.5 bg-gray-50 border border-gray-200 rounded-xl text-xs text-gray-900 placeholder:text-gray-400 focus:bg-white focus:ring-2 focus:ring-teal-600 focus:outline-none"
                  aria-label="Filter learners by name or level"
                />
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse" role="table">
                <thead>
                  <tr className="border-b border-gray-100 bg-gray-50/50 text-[11px] font-bold text-gray-500 uppercase tracking-wider">
                    <th 
                      scope="col" 
                      className="py-3.5 px-4 cursor-pointer hover:text-gray-900"
                      onClick={() => handleSort("display_name")}
                    >
                      <div className="flex items-center gap-1">
                        Learner Name
                        <ArrowUpDown className="w-3 h-3" />
                      </div>
                    </th>
                    <th scope="col" className="py-3.5 px-4">Level</th>
                    <th 
                      scope="col" 
                      className="py-3.5 px-4 cursor-pointer hover:text-gray-900"
                      onClick={() => handleSort("completed_activities")}
                    >
                      <div className="flex items-center gap-1">
                        Completed
                        <ArrowUpDown className="w-3 h-3" />
                      </div>
                    </th>
                    <th 
                      scope="col" 
                      className="py-3.5 px-4 cursor-pointer hover:text-gray-900"
                      onClick={() => handleSort("overall_accuracy")}
                    >
                      <div className="flex items-center gap-1">
                        Accuracy
                        <ArrowUpDown className="w-3 h-3" />
                      </div>
                    </th>
                    <th scope="col" className="py-3.5 px-4">Assistance Level</th>
                    <th scope="col" className="py-3.5 px-4">Mastery</th>
                    <th scope="col" className="py-3.5 px-4">Status / Alerts</th>
                    <th scope="col" className="py-3.5 px-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100 text-xs">
                  {filteredLearners.length === 0 ? (
                    <tr>
                      <td colSpan={8} className="py-8 text-center text-gray-400">
                        No learners matched your query or filter.
                      </td>
                    </tr>
                  ) : (
                    filteredLearners.map((learner: any) => (
                      <tr key={learner.learner_id} className="hover:bg-gray-50/50 transition-colors">
                        <td className="py-3.5 px-4 font-semibold text-gray-900">
                          {learner.display_name || (learner as any).name}
                        </td>
                        <td className="py-3.5 px-4">
                          <span className="px-2 py-0.5 rounded-md bg-gray-100 text-gray-700 capitalize font-medium">
                            {learner.learning_level}
                          </span>
                        </td>
                        <td className="py-3.5 px-4 text-gray-700 font-medium">
                          {learner.completed_activities} activities
                        </td>
                        <td className="py-3.5 px-4">
                          <span className={`font-semibold ${
                            learner.overall_accuracy >= 0.75
                              ? "text-emerald-700"
                              : learner.overall_accuracy >= 0.50
                              ? "text-teal-700"
                              : "text-amber-700"
                          }`}>
                            {(learner.overall_accuracy * 100).toFixed(0)}%
                          </span>
                        </td>
                        <td className="py-3.5 px-4 text-gray-600">
                          {learner.average_assistance_level.toFixed(2)} / 3.0
                        </td>
                        <td className="py-3.5 px-4">
                          <span className="text-emerald-700 font-semibold">{learner.mastered_objectives_count}</span>
                          <span className="text-gray-400"> / {learner.mastered_objectives_count + learner.in_progress_objectives_count}</span>
                        </td>
                        <td className="py-3.5 px-4">
                          {learner.active_alerts_count > 0 ? (
                            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-amber-50 text-amber-700 border border-amber-200">
                              <span className="w-1.5 h-1.5 rounded-full bg-amber-500" />
                              {learner.active_alerts_count} alert{learner.active_alerts_count > 1 ? "s" : ""}
                            </span>
                          ) : (
                            <span className="inline-flex items-center gap-1 text-[11px] text-emerald-700 font-medium">
                              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                              On Track
                            </span>
                          )}
                        </td>
                        <td className="py-3.5 px-4 text-right">
                          <button
                            onClick={() => onSelectLearnerForIEP(learner.learner_id, learner.display_name)}
                            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-teal-50 text-teal-800 hover:bg-teal-700 hover:text-white font-semibold transition-colors focus:ring-2 focus:ring-teal-600 focus:outline-none"
                            aria-label={`View IEP Report for ${learner.display_name}`}
                          >
                            <FileText className="w-3.5 h-3.5" />
                            IEP Report
                          </button>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </section>
        </>
      )}
    </div>
  );
};
