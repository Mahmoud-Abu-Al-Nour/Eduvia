import React, { useEffect, useState } from "react";
import { useAuth } from "@/features/auth/AuthContext";
import {
  BookOpen,
  Users,
  BarChart3,
  LogOut,
  PlayCircle,
  TrendingUp,
  Compass,
  GraduationCap,
  Menu,
  X,
  ChevronRight,
  ShieldCheck,
} from "lucide-react";
import { CurriculumBrowser } from "@/features/curriculum/CurriculumBrowser";
import { LearnerManager } from "@/features/learners/LearnerManager";
import { AnalyticsDashboard } from "@/features/analytics/AnalyticsDashboard";
import { RecommendationCard } from "@/features/recommendations";
import { TeacherOverview } from "./TeacherOverview";
import { CohortInsightsView } from "./CohortInsightsView";
import { IEPReportModal } from "./IEPReportModal";
import { recommendationsApi } from "@/services/api";
import api from "@/services/api";
import type { Learner, RecommendationDecision } from "@/types";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

interface DashboardPageProps {
  initialTab?: string;
}

const TABS = [
  { id: "overview", label: "Overview", icon: BarChart3, description: "Daily classroom briefing & intervention alerts" },
  { id: "cohort", label: "Classroom Cohort", icon: GraduationCap, description: "Cohort learning progress & distribution" },
  { id: "activities", label: "Activities & Practice", icon: PlayCircle, description: "Calibrated multi-sensory learner practice" },
  { id: "curriculum", label: "Curriculum", icon: BookOpen, description: "Standardized objectives & structured milestones" },
  { id: "learners", label: "Learners", icon: Users, description: "Individual learner profiles & sensory profiles" },
  { id: "analytics", label: "Analytics & Mastery", icon: TrendingUp, description: "Objective mastery & delivery effectiveness" },
  { id: "recommendations", label: "Adaptive Engine", icon: Compass, description: "Teacher-guided sequencing recommendations" },
];

export const DashboardPage: React.FC<DashboardPageProps> = ({ initialTab = "overview" }) => {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState(initialTab);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  // IEP Modal state
  const [iepLearner, setIepLearner] = useState<{ id: string; name: string } | null>(null);
  const [isIepOpen, setIsIepOpen] = useState<boolean>(false);

  const handleOpenIEP = (id: string, name: string) => {
    setIepLearner({ id, name });
    setIsIepOpen(true);
  };

  const [learners, setLearners] = useState<Learner[]>([]);
  const [selectedLearnerId, setSelectedLearnerId] = useState<string>("");
  const [loadingLearners, setLoadingLearners] = useState<boolean>(false);
  const [recommendation, setRecommendation] = useState<RecommendationDecision | null>(null);
  const [loadingRec, setLoadingRec] = useState<boolean>(false);
  const [recError, setRecError] = useState<string | null>(null);

  // Fetch learners when tab is recommendations
  useEffect(() => {
    const fetchLearners = async () => {
      try {
        setLoadingLearners(true);
        const data = await api.get<Learner[]>("/learners");
        setLearners(data);
        if (data.length > 0 && !selectedLearnerId) {
          setSelectedLearnerId(data[0].id);
        }
      } catch (err: any) {
        console.error("Failed to load learners for adaptive engine:", err);
      } finally {
        setLoadingLearners(false);
      }
    };
    if (activeTab === "recommendations" && learners.length === 0) {
      void fetchLearners();
    }
  }, [activeTab, learners.length, selectedLearnerId]);

  // Fetch recommendation when selected learner changes or tab becomes recommendations
  const fetchRecommendation = async (learnerId: string) => {
    if (!learnerId) return;
    try {
      setLoadingRec(true);
      setRecError(null);
      const res = await recommendationsApi.getRecommendation(learnerId);
      setRecommendation(res);
    } catch (err: any) {
      console.error("Failed to fetch recommendation:", err);
      setRecError(err?.message || "Failed to retrieve adaptive recommendation.");
      setRecommendation(null);
    } finally {
      setLoadingRec(false);
    }
  };

  useEffect(() => {
    if (activeTab === "recommendations" && selectedLearnerId) {
      void fetchRecommendation(selectedLearnerId);
    }
  }, [activeTab, selectedLearnerId]);

  const currentTabObj = TABS.find((t) => t.id === activeTab) || TABS[0];

  return (
    <div className="min-h-screen bg-[#faf8f5] flex text-slate-900">
      {/* ── Mobile Sidebar Backdrop ───────────────────────────────────────── */}
      {isMobileMenuOpen && (
        <div
          className="fixed inset-0 z-40 bg-slate-900/40 backdrop-blur-xs lg:hidden"
          onClick={() => setIsMobileMenuOpen(false)}
          aria-hidden="true"
        />
      )}

      {/* ── Sidebar ───────────────────────────────────────────────────────── */}
      <aside
        className={`fixed inset-y-0 left-0 z-50 w-64 bg-white border-r border-slate-200/90 flex flex-col transition-transform duration-200 ease-in-out lg:static lg:translate-x-0 ${
          isMobileMenuOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        {/* Brand Header */}
        <div className="h-16 flex items-center justify-between px-5 border-b border-slate-200/80">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-brand-800 text-white flex items-center justify-center font-bold text-base shadow-2xs">
              E
            </div>
            <div>
              <span className="font-bold text-base tracking-tight text-slate-900 leading-none block">
                Eduvia
              </span>
              <span className="text-[10px] font-medium text-slate-500 uppercase tracking-wider block mt-0.5">
                Special Ed Platform
              </span>
            </div>
          </div>
          <button
            type="button"
            className="lg:hidden p-1 rounded-md text-slate-400 hover:text-slate-600"
            onClick={() => setIsMobileMenuOpen(false)}
            aria-label="Close menu"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Navigation Tabs */}
        <nav
          role="tablist"
          aria-label="Teacher Dashboard Tabs"
          className="flex-1 px-3 py-4 space-y-1 overflow-y-auto"
        >
          {TABS.map((tab) => {
            const Icon = tab.icon;
            const isSelected = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                type="button"
                role="tab"
                id={`tab-${tab.id}`}
                aria-selected={isSelected}
                aria-controls={`tabpanel-${tab.id}`}
                tabIndex={isSelected ? 0 : -1}
                onClick={() => {
                  setActiveTab(tab.id);
                  setIsMobileMenuOpen(false);
                }}
                className={`w-full flex items-center px-3 py-2.5 text-sm font-medium rounded-lg transition-all text-left focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-700 ${
                  isSelected
                    ? "bg-brand-50 text-brand-900 font-semibold shadow-2xs border border-brand-200/70"
                    : "text-slate-600 hover:bg-slate-100/70 hover:text-slate-900"
                }`}
              >
                <Icon
                  className={`w-4 h-4 mr-3 shrink-0 ${
                    isSelected ? "text-brand-800" : "text-slate-400"
                  }`}
                  aria-hidden="true"
                />
                <span className="truncate">{tab.label}</span>
              </button>
            );
          })}
        </nav>

        {/* User Card & Logout */}
        <div className="p-3 border-t border-slate-200/80 bg-slate-50/50">
          <div className="flex items-center gap-3 p-2 rounded-lg bg-white border border-slate-200/70 shadow-2xs mb-2">
            <div className="w-8 h-8 rounded-full bg-brand-800 text-white flex items-center justify-center font-bold text-xs shrink-0">
              {user?.full_name?.charAt(0) || user?.email.charAt(0).toUpperCase()}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-semibold text-slate-900 truncate">
                {user?.full_name || "Educator"}
              </p>
              <div className="flex items-center gap-1.5 mt-0.5">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                <p className="text-[10px] text-slate-500 uppercase tracking-wide font-medium">
                  {user?.role || "Teacher"}
                </p>
              </div>
            </div>
          </div>

          <button
            onClick={logout}
            type="button"
            className="flex w-full items-center justify-center px-3 py-2 text-xs font-semibold text-slate-600 hover:text-rose-700 hover:bg-rose-50/60 rounded-lg transition-colors border border-transparent hover:border-rose-200/50"
          >
            <LogOut className="w-3.5 h-3.5 mr-2" />
            Sign Out
          </button>
        </div>
      </aside>

      {/* ── Main Content Area ────────────────────────────────────────────── */}
      <main
        id="main-content"
        tabIndex={-1}
        className="flex-1 flex flex-col focus:outline-none min-w-0 overflow-y-auto"
      >
        {/* Top Header */}
        <header className="h-16 bg-white border-b border-slate-200/80 sticky top-0 z-30 flex items-center justify-between px-4 sm:px-8">
          <div className="flex items-center gap-3 min-w-0">
            <button
              type="button"
              className="lg:hidden p-2 -ml-2 text-slate-500 hover:text-slate-800 focus:outline-none"
              onClick={() => setIsMobileMenuOpen(true)}
              aria-label="Open navigation sidebar"
            >
              <Menu className="w-5 h-5" />
            </button>
            <div className="flex items-center gap-2 text-xs text-slate-400 font-medium">
              <span>Workspace</span>
              <ChevronRight className="w-3 h-3 text-slate-300" />
              <span className="text-slate-800 font-semibold">{currentTabObj.label}</span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Badge variant="secondary" className="hidden sm:inline-flex items-center gap-1.5 py-1 px-2.5 text-[11px]">
              <ShieldCheck className="w-3.5 h-3.5 text-brand-700" />
              <span>Standardized Curriculum Mode</span>
            </Badge>
          </div>
        </header>

        {/* Tab Panel Body */}
        <div
          role="tabpanel"
          id={`tabpanel-${activeTab}`}
          aria-labelledby={`tab-${activeTab}`}
          className="flex-1 p-4 sm:p-8 focus:outline-none max-w-7xl w-full mx-auto"
        >
          {activeTab === "overview" && (
            <TeacherOverview
              onSelectLearnerForIEP={handleOpenIEP}
              onNavigateTab={(tab) => setActiveTab(tab)}
            />
          )}

          {activeTab === "cohort" && (
            <CohortInsightsView
              onSelectLearnerForIEP={handleOpenIEP}
            />
          )}

          {activeTab === "activities" && (
            <div className="space-y-6 max-w-5xl">
              <Card className="border-brand-200/80 bg-gradient-to-r from-brand-50/60 to-white shadow-xs">
                <CardHeader className="pb-3">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <Badge variant="default" className="text-[10px] uppercase tracking-wider">
                          Distraction-Free Environment
                        </Badge>
                      </div>
                      <CardTitle className="text-xl font-bold text-slate-900">
                        Learner Activity Player
                      </CardTitle>
                      <CardDescription className="text-xs max-w-2xl">
                        Accessible learning interface equipped with text-to-speech narration, progressive hints, large touch targets, and Cognitive Calm feedback.
                      </CardDescription>
                    </div>

                    <a
                      href="/learn"
                      className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-brand-800 text-white font-semibold hover:bg-brand-900 shadow-xs transition-all text-sm shrink-0"
                    >
                      <PlayCircle className="w-4 h-4" />
                      <span>Launch Player</span>
                    </a>
                  </div>
                </CardHeader>
              </Card>

              {/* Supported Modalities Showcase */}
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
                    5 Validated Delivery Modalities
                  </h3>
                  <span className="text-xs text-slate-500">Curriculum-Aligned Formats</span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                  {[
                    { name: "Multiple Choice", type: "multiple_choice", desc: "Select target among calibrated options with hint scaffolding" },
                    { name: "Matching Pairs", type: "matching", desc: "Connect related items across concrete and abstract representations" },
                    { name: "Sequential Ordering", type: "ordering", desc: "Arrange items along an ordered progressive continuum" },
                    { name: "Visual Identification", type: "visual_identification", desc: "Identify target elements in accessible high-contrast scenes" },
                    { name: "Tactile Drag & Drop", type: "drag_drop", desc: "Categorize items into distinct target buckets with touch targets" },
                  ].map((mod) => (
                    <Card key={mod.type} className="flex flex-col justify-between hover:border-brand-200 transition-all">
                      <CardHeader className="pb-3">
                        <Badge variant="outline" className="w-fit text-[10px] mb-1 font-mono uppercase">
                          {mod.type}
                        </Badge>
                        <CardTitle className="text-base font-semibold">{mod.name}</CardTitle>
                        <CardDescription className="text-xs">{mod.desc}</CardDescription>
                      </CardHeader>
                      <CardContent className="pt-0">
                        <a
                          href={`/learn?activity_type=${mod.type}`}
                          className="inline-flex items-center justify-center gap-1.5 w-full py-2 px-3 rounded-lg bg-brand-50 text-brand-900 hover:bg-brand-100 text-xs font-semibold border border-brand-200/60 transition-colors"
                        >
                          <PlayCircle className="w-3.5 h-3.5 text-brand-700" />
                          <span>Preview {mod.name}</span>
                        </a>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === "curriculum" && (
            <div className="max-w-6xl">
              <CurriculumBrowser />
            </div>
          )}

          {activeTab === "learners" && (
            <div className="max-w-6xl">
              <LearnerManager />
            </div>
          )}

          {activeTab === "analytics" && (
            <div className="max-w-6xl">
              <AnalyticsDashboard />
            </div>
          )}

          {activeTab === "recommendations" && (
            <div className="max-w-4xl space-y-6">
              <Card className="border-slate-200/90 shadow-xs bg-white">
                <CardHeader className="pb-4">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <Badge variant="secondary" className="text-[10px] uppercase font-semibold">
                          Teacher Decision Cockpit
                        </Badge>
                      </div>
                      <CardTitle className="text-lg font-bold text-slate-900 flex items-center gap-2">
                        <Compass className="w-5 h-5 text-brand-800" />
                        Adaptive Sequencing Recommendations
                      </CardTitle>
                      <CardDescription className="text-xs mt-1">
                        Deterministic curriculum progression calibrated to each learner&apos;s observed performance and sensory preferences.
                      </CardDescription>
                    </div>

                    {learners.length > 0 && (
                      <div className="flex items-center gap-2.5 bg-slate-50 p-2 rounded-xl border border-slate-200/80">
                        <label htmlFor="learner-select" className="text-xs font-semibold text-slate-700 whitespace-nowrap">
                          Active Learner:
                        </label>
                        <select
                          id="learner-select"
                          value={selectedLearnerId}
                          onChange={(e) => setSelectedLearnerId(e.target.value)}
                          className="rounded-lg border-slate-300 text-xs font-semibold py-1.5 px-2.5 bg-white text-slate-900 focus:ring-brand-700 focus:border-brand-700 shadow-2xs"
                        >
                          {learners.map((l) => (
                            <option key={l.id} value={l.id}>
                              {l.name} ({l.learning_level})
                            </option>
                          ))}
                        </select>
                      </div>
                    )}
                  </div>
                </CardHeader>
              </Card>

              {loadingLearners ? (
                <div className="p-12 text-center bg-white rounded-2xl border border-slate-200/80 shadow-xs">
                  <div className="animate-spin w-7 h-7 border-3 border-brand-800 border-t-transparent rounded-full mx-auto mb-3" />
                  <p className="text-xs text-slate-600 font-medium">Loading classroom learners...</p>
                </div>
              ) : learners.length === 0 ? (
                <div className="p-12 text-center bg-white rounded-2xl border border-slate-200/80 shadow-xs">
                  <p className="text-sm text-slate-600 font-medium">No learners found in your assigned cohort.</p>
                </div>
              ) : (
                <>
                  {recError && (
                    <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 text-xs">
                      {recError}
                    </div>
                  )}
                  <RecommendationCard
                    learnerId={selectedLearnerId}
                    recommendation={recommendation}
                    loading={loadingRec}
                    onProfileSynced={() => fetchRecommendation(selectedLearnerId)}
                  />
                </>
              )}
            </div>
          )}
        </div>
      </main>

      {/* IEP Progress Report Modal */}
      <IEPReportModal
        isOpen={isIepOpen}
        onClose={() => setIsIepOpen(false)}
        learnerId={iepLearner?.id || null}
        learnerName={iepLearner?.name || ""}
      />
    </div>
  );
};
