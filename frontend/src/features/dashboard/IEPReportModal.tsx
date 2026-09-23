import React, { useEffect, useState, useCallback } from "react";
import { 
  X, 
  Download, 
  Printer, 
  FileText, 
  Calendar, 
  RefreshCw, 
  CheckCircle2, 
  AlertTriangle,
  User,
  Sparkles
} from "lucide-react";
import { teachersApi } from "@/services/api";
import type { IEPReport } from "@/types";

interface IEPReportModalProps {
  learnerId: string | null;
  learnerName: string;
  isOpen: boolean;
  onClose: () => void;
}

export const IEPReportModal: React.FC<IEPReportModalProps> = ({
  learnerId,
  learnerName,
  isOpen,
  onClose,
}) => {
  const [days, setDays] = useState<number>(30);
  const [report, setReport] = useState<IEPReport | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchReport = useCallback(async () => {
    if (!learnerId) return;
    try {
      setLoading(true);
      setError(null);
      const data = await teachersApi.getIEPReport(learnerId, days);
      setReport(data);
    } catch (err: any) {
      console.error("Failed to load IEP report:", err);
      setError(err?.message || "Failed to load Individualized Education Plan report.");
    } finally {
      setLoading(false);
    }
  }, [learnerId, days]);

  useEffect(() => {
    if (isOpen && learnerId) {
      void fetchReport();
    }
  }, [isOpen, learnerId, fetchReport]);

  const openerElementRef = React.useRef<HTMLElement | null>(null);
  const modalContainerRef = React.useRef<HTMLDivElement | null>(null);

  // Capture opener element on open and restore on close
  useEffect(() => {
    if (isOpen) {
      openerElementRef.current = document.activeElement as HTMLElement | null;
      const timer = setTimeout(() => {
        if (modalContainerRef.current) {
          const firstFocusable = modalContainerRef.current.querySelector<HTMLElement>(
            'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
          );
          if (firstFocusable) {
            firstFocusable.focus();
          } else {
            modalContainerRef.current.focus();
          }
        }
      }, 50);
      return () => clearTimeout(timer);
    } else if (openerElementRef.current && document.body.contains(openerElementRef.current)) {
      openerElementRef.current.focus();
    }
  }, [isOpen]);

  // Trap focus within modal and handle Escape
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!isOpen || !modalContainerRef.current) return;

      if (e.key === "Escape") {
        e.preventDefault();
        onClose();
        return;
      }

      if (e.key === "Tab") {
        const focusables = modalContainerRef.current.querySelectorAll<HTMLElement>(
          'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
        );
        const visibleFocusables = Array.from(focusables).filter(
          (el) => el.offsetParent !== null || el.offsetWidth > 0 || el.offsetHeight > 0
        );

        if (visibleFocusables.length === 0) {
          e.preventDefault();
          return;
        }

        const firstElement = visibleFocusables[0];
        const lastElement = visibleFocusables[visibleFocusables.length - 1];

        if (e.shiftKey) {
          if (document.activeElement === firstElement || document.activeElement === modalContainerRef.current) {
            e.preventDefault();
            lastElement.focus();
          }
        } else {
          if (document.activeElement === lastElement) {
            e.preventDefault();
            firstElement.focus();
          }
        }
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, onClose]);

  const handleDownloadMarkdown = () => {
    if (!report) return;
    const blob = new Blob([report.printable_summary_markdown], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `IEP_Report_${learnerName.replace(/\s+/g, "_")}_${new Date().toISOString().slice(0, 10)}.md`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handleDownloadJSON = () => {
    if (!report) return;
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: "application/json;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `IEP_Data_${learnerName.replace(/\s+/g, "_")}_${new Date().toISOString().slice(0, 10)}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handlePrint = () => {
    window.print();
  };

  if (!isOpen) return null;

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm overflow-y-auto"
      role="dialog"
      aria-modal="true"
      aria-labelledby="iep-modal-title"
    >
      <div 
        ref={modalContainerRef}
        tabIndex={-1}
        className="bg-white rounded-2xl max-w-4xl w-full max-h-[90vh] flex flex-col shadow-2xl border border-gray-200 overflow-hidden my-auto focus:outline-none"
      >
        {/* Modal Header */}
        <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between bg-slate-50">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-blue-600 text-white flex items-center justify-center font-bold">
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <h2 id="iep-modal-title" className="text-lg font-bold text-gray-900">
                Individualized Education Plan (IEP) Progress Report
              </h2>
              <p className="text-xs text-gray-600">
                Learner: <strong className="text-gray-900">{learnerName}</strong>
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 text-gray-400 hover:text-gray-700 hover:bg-gray-200/60 rounded-xl transition-colors focus:ring-2 focus:ring-blue-500 focus:outline-none"
            aria-label="Close modal"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Controls Bar */}
        <div className="px-6 py-3 border-b border-gray-100 flex flex-wrap items-center justify-between gap-3 bg-white">
          <div className="flex items-center gap-2">
            <Calendar className="w-4 h-4 text-gray-500" />
            <label htmlFor="iep-period-select" className="text-xs font-semibold text-gray-600">Period:</label>
            <select
              id="iep-period-select"
              value={days}
              onChange={(e) => setDays(Number(e.target.value))}
              className="text-xs font-semibold text-gray-800 bg-gray-50 border border-gray-200 rounded-lg px-2.5 py-1 focus:ring-2 focus:ring-teal-600 focus:outline-none cursor-pointer"
            >
              <option value={7}>Last 7 Days</option>
              <option value={14}>Last 14 Days</option>
              <option value={30}>Last 30 Days</option>
              <option value={90}>Last 90 Days</option>
              <option value={0}>All Time Baseline</option>
            </select>
            <button
              onClick={() => void fetchReport()}
              className="p-1 text-gray-500 hover:text-gray-800 rounded-md transition-colors"
              title="Refresh report"
              aria-label="Refresh report"
            >
              <RefreshCw className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handlePrint}
              disabled={!report || loading}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-gray-200 hover:bg-gray-50 text-gray-700 text-xs font-semibold rounded-xl shadow-sm transition-colors disabled:opacity-50"
            >
              <Printer className="w-3.5 h-3.5" />
              Print
            </button>
            <button
              onClick={handleDownloadMarkdown}
              disabled={!report || loading}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-gray-200 hover:bg-gray-50 text-gray-700 text-xs font-semibold rounded-xl shadow-sm transition-colors disabled:opacity-50"
            >
              <Download className="w-3.5 h-3.5 text-teal-700" />
              Markdown
            </button>
            <button
              onClick={handleDownloadJSON}
              disabled={!report || loading}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-teal-700 hover:bg-teal-800 text-white text-xs font-semibold rounded-xl shadow-sm transition-colors disabled:opacity-50"
            >
              <Download className="w-3.5 h-3.5" />
              JSON Data
            </button>
          </div>
        </div>

        {/* Modal Scrollable Content */}
        <div className="p-6 overflow-y-auto flex-1 space-y-6">
          {loading ? (
            <div className="space-y-4 py-8" aria-busy="true" aria-live="polite">
              <div className="h-20 bg-gray-100 rounded-xl animate-pulse" />
              <div className="h-40 bg-gray-100 rounded-xl animate-pulse" />
              <div className="h-28 bg-gray-100 rounded-xl animate-pulse" />
            </div>
          ) : error || !report ? (
            <div className="bg-rose-50 border border-rose-200 rounded-xl p-6 text-center" role="alert">
              <AlertTriangle className="w-8 h-8 text-rose-500 mx-auto mb-2" />
              <h4 className="text-sm font-bold text-rose-900 mb-1">Unable to Load IEP Progress Report</h4>
              <p className="text-xs text-rose-700 mb-3">{error || "Server error retrieving report."}</p>
              <button
                onClick={() => void fetchReport()}
                className="px-3 py-1.5 bg-rose-600 text-white text-xs font-semibold rounded-lg hover:bg-rose-700"
              >
                Retry
              </button>
            </div>
          ) : (
            <>
              {/* Executive Summary Cards */}
              <div className="bg-slate-50 border border-slate-200/80 rounded-2xl p-5">
                <div className="flex items-center gap-2 mb-3">
                  <User className="w-4 h-4 text-teal-700" />
                  <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
                    Learner Profile & Period Snapshot
                  </h3>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
                  <div>
                    <span className="text-gray-500 block">Learning Level</span>
                    <strong className="text-gray-900 font-semibold capitalize">{report.learning_level}</strong>
                  </div>
                  <div>
                    <span className="text-gray-500 block">Communication</span>
                    <strong className="text-gray-900 font-semibold capitalize">{report.communication_preference}</strong>
                  </div>
                  <div>
                    <span className="text-gray-500 block">Overall Accuracy</span>
                    <strong className="text-emerald-700 font-semibold">
                      {(report.overall_accuracy * 100).toFixed(1)}%
                    </strong>
                  </div>
                  <div>
                    <span className="text-gray-500 block">Assistance Average</span>
                    <strong className="text-gray-900 font-semibold">
                      {report.overall_assistance_average.toFixed(2)} / 3.0
                    </strong>
                  </div>
                </div>
              </div>

              {/* Objectives Progress Table */}
              <div className="space-y-2">
                <h3 className="text-sm font-bold text-gray-900">
                  Curriculum Learning Objectives Progress
                </h3>
                <div className="border border-gray-200 rounded-xl overflow-hidden">
                  <table className="w-full text-left text-xs border-collapse">
                    <thead className="bg-gray-50 text-gray-500 font-semibold border-b border-gray-200">
                      <tr>
                        <th className="py-2.5 px-3">Objective</th>
                        <th className="py-2.5 px-3 text-center">Attempts</th>
                        <th className="py-2.5 px-3 text-center">Accuracy</th>
                        <th className="py-2.5 px-3 text-center">Avg Scaffolding</th>
                        <th className="py-2.5 px-3 text-right">Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                      {report.objectives_progress.length === 0 ? (
                        <tr>
                          <td colSpan={5} className="py-6 text-center text-gray-400">
                            No objective mastery recorded in this reporting window.
                          </td>
                        </tr>
                      ) : (
                        report.objectives_progress.map((obj) => (
                          <tr key={obj.objective_id} className="hover:bg-gray-50/50">
                            <td className="py-2.5 px-3 font-semibold text-gray-900">{obj.title}</td>
                            <td className="py-2.5 px-3 text-center text-gray-600">{obj.attempts_count}</td>
                            <td className="py-2.5 px-3 text-center font-medium">
                              {(obj.accuracy * 100).toFixed(0)}%
                            </td>
                            <td className="py-2.5 px-3 text-center text-gray-600">
                              {obj.average_assistance.toFixed(1)}
                            </td>
                            <td className="py-2.5 px-3 text-right">
                              <span className={`px-2 py-0.5 rounded-full text-[11px] font-semibold ${
                                obj.status === "mastered"
                                  ? "bg-emerald-50 text-emerald-700 border border-emerald-200"
                                  : obj.status === "in_progress"
                                  ? "bg-teal-50 text-teal-800 border border-teal-200"
                                  : "bg-gray-100 text-gray-600"
                              }`}>
                                {obj.status.replace("_", " ").toUpperCase()}
                              </span>
                            </td>
                          </tr>
                        ))
                      )}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Sensory Modality Efficacy */}
              <div className="space-y-2">
                <h3 className="text-sm font-bold text-gray-900">
                  Sensory Modality Efficacy
                </h3>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  {Object.keys(report.modality_efficacy).length === 0 ? (
                    <p className="text-xs text-gray-400 col-span-4">No modality telemetry recorded.</p>
                  ) : (
                    Object.entries(report.modality_efficacy).map(([mod, eff]) => (
                      <div key={mod} className="border border-gray-200 rounded-xl p-3 bg-white">
                        <span className="text-xs font-semibold text-gray-500 capitalize block">{mod}</span>
                        <div className="text-lg font-bold text-gray-900 mt-1">
                          {(eff * 100).toFixed(0)}%
                        </div>
                        <span className="text-[11px] text-gray-500 block mt-0.5">
                          {eff >= 0.8 ? "Optimal Channel" : eff >= 0.6 ? "Developing" : "Needs Support"}
                        </span>
                      </div>
                    ))
                  )}
                </div>
              </div>

              {/* Pedagogical Recommendations */}
              <div className="space-y-2">
                <h3 className="text-sm font-bold text-gray-900 flex items-center gap-1.5">
                  <Sparkles className="w-4 h-4 text-teal-700" />
                  Evidence-Based Pedagogical Recommendations
                </h3>
                <div className="bg-teal-50/50 border border-teal-100 rounded-xl p-4 space-y-2 text-xs text-teal-950">
                  {report.teacher_recommendations.length === 0 ? (
                    <p className="text-gray-500">Continue current instructional trajectory.</p>
                  ) : (
                    report.teacher_recommendations.map((rec, i) => (
                      <div key={i} className="flex items-start gap-2">
                        <CheckCircle2 className="w-3.5 h-3.5 text-teal-700 shrink-0 mt-0.5" />
                        <span className="leading-relaxed">{rec}</span>
                      </div>
                    ))
                  )}
                </div>
              </div>

              {/* Teacher Observations & Notes */}
              {report.teacher_notes && (
                <div className="space-y-1">
                  <h3 className="text-sm font-bold text-gray-900">Teacher Notes & Accommodations</h3>
                  <div className="bg-gray-50 border border-gray-200 rounded-xl p-3.5 text-xs text-gray-700 italic">
                    "{report.teacher_notes}"
                  </div>
                </div>
              )}
            </>
          )}
        </div>

        {/* Modal Footer */}
        <div className="px-6 py-3 border-t border-gray-200 bg-gray-50 flex items-center justify-between text-xs text-gray-500">
          <span>Report ID: {report?.report_id || "Loading..."}</span>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-white border border-gray-200 hover:bg-gray-100 text-gray-700 font-semibold rounded-xl transition-colors focus:ring-2 focus:ring-teal-600 focus:outline-none"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
