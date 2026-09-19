import React, { useEffect, useState } from "react";
import { useAuth } from "@/features/auth/AuthContext";
import { BookOpen, Users, BarChart3, LogOut, PlayCircle, TrendingUp, Sparkles } from "lucide-react";
import { CurriculumBrowser } from "@/features/curriculum/CurriculumBrowser";
import { LearnerManager } from "@/features/learners/LearnerManager";
import { AnalyticsDashboard } from "@/features/analytics/AnalyticsDashboard";
import { RecommendationCard } from "@/features/recommendations";
import { recommendationsApi } from "@/services/api";
import api from "@/services/api";
import type { Learner, RecommendationDecision } from "@/types";


interface DashboardPageProps {
  initialTab?: string;
}

export const DashboardPage: React.FC<DashboardPageProps> = ({ initialTab = "overview" }) => {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState(initialTab);

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

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
        <div className="h-16 flex items-center px-6 border-b border-gray-200">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center mr-3">
            <span className="text-white font-bold text-xl">E</span>
          </div>
          <span className="text-xl font-bold text-gray-900">Eduvia</span>
        </div>
        
        <nav className="flex-1 px-4 py-6 space-y-1">
          <a
            href="#"
            onClick={(e) => { e.preventDefault(); setActiveTab("overview"); }}
            className={`flex items-center px-3 py-2.5 text-sm font-medium rounded-lg transition-colors ${activeTab === 'overview' ? 'bg-blue-50 text-blue-700' : 'text-gray-700 hover:bg-gray-100'}`}
          >
            <BarChart3 className={`w-5 h-5 mr-3 ${activeTab === 'overview' ? 'text-blue-700' : 'text-gray-400'}`} />
            Overview
          </a>
          
          <a
            href="#"
            onClick={(e) => { e.preventDefault(); setActiveTab("activities"); }}
            className={`flex items-center px-3 py-2.5 text-sm font-medium rounded-lg transition-colors ${activeTab === 'activities' ? 'bg-blue-50 text-blue-700' : 'text-gray-700 hover:bg-gray-100'}`}
          >
            <PlayCircle className={`w-5 h-5 mr-3 ${activeTab === 'activities' ? 'text-blue-700' : 'text-gray-400'}`} />
            Activities & Practice
          </a>

          <a
            href="#"
            onClick={(e) => { e.preventDefault(); setActiveTab("curriculum"); }}
            className={`flex items-center px-3 py-2.5 text-sm font-medium rounded-lg transition-colors ${activeTab === 'curriculum' ? 'bg-blue-50 text-blue-700' : 'text-gray-700 hover:bg-gray-100'}`}
          >
            <BookOpen className={`w-5 h-5 mr-3 ${activeTab === 'curriculum' ? 'text-blue-700' : 'text-gray-400'}`} />
            Curriculum
          </a>

          <a
            href="#"
            onClick={(e) => { e.preventDefault(); setActiveTab("learners"); }}
            className={`flex items-center px-3 py-2.5 text-sm font-medium rounded-lg transition-colors ${activeTab === 'learners' ? 'bg-blue-50 text-blue-700' : 'text-gray-700 hover:bg-gray-100'}`}
          >
            <Users className={`w-5 h-5 mr-3 ${activeTab === 'learners' ? 'text-blue-700' : 'text-gray-400'}`} />
            Learners
          </a>

          <a
            href="#"
            onClick={(e) => { e.preventDefault(); setActiveTab("analytics"); }}
            className={`flex items-center px-3 py-2.5 text-sm font-medium rounded-lg transition-colors ${activeTab === 'analytics' ? 'bg-blue-50 text-blue-700' : 'text-gray-700 hover:bg-gray-100'}`}
          >
            <TrendingUp className={`w-5 h-5 mr-3 ${activeTab === 'analytics' ? 'text-blue-700' : 'text-gray-400'}`} />
            Analytics & Mastery
          </a>

          <a
            href="#"
            onClick={(e) => { e.preventDefault(); setActiveTab("recommendations"); }}
            className={`flex items-center px-3 py-2.5 text-sm font-medium rounded-lg transition-colors ${activeTab === 'recommendations' ? 'bg-blue-50 text-blue-700' : 'text-gray-700 hover:bg-gray-100'}`}
          >
            <Sparkles className={`w-5 h-5 mr-3 ${activeTab === 'recommendations' ? 'text-blue-700' : 'text-gray-400'}`} />
            Adaptive Engine
          </a>
        </nav>

        <div className="p-4 border-t border-gray-200">
          <div className="flex items-center mb-4 px-3">
            <div className="w-8 h-8 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-bold mr-3">
              {user?.full_name?.charAt(0) || user?.email.charAt(0).toUpperCase()}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">{user?.full_name || "Teacher"}</p>
              <p className="text-xs text-gray-500 truncate">{user?.email}</p>
            </div>
          </div>
          
          <button
            onClick={logout}
            className="flex w-full items-center px-3 py-2 text-sm font-medium text-red-600 rounded-lg hover:bg-red-50 transition-colors"
          >
            <LogOut className="w-5 h-5 mr-3 text-red-500" />
            Sign Out
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col">
        <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-8">
          <h1 className="text-xl font-semibold text-gray-900 capitalize">{activeTab}</h1>
        </header>
        
        <div className="flex-1 p-8 overflow-auto">
          {activeTab === "overview" && (
            <div className="max-w-4xl">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Welcome back!</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
                  <div className="text-sm font-medium text-gray-500 mb-1">Active Learners</div>
                  <div className="text-3xl font-bold text-gray-900">0</div>
                </div>
                
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
                  <div className="text-sm font-medium text-gray-500 mb-1">Pending Activities</div>
                  <div className="text-3xl font-bold text-gray-900">0</div>
                </div>
                
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
                  <div className="text-sm font-medium text-gray-500 mb-1">Alerts</div>
                  <div className="text-3xl font-bold text-gray-900">0</div>
                </div>
              </div>
            </div>
          )}

          {activeTab === "activities" && (
            <div className="max-w-4xl space-y-6">
              <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200">
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                  <div>
                    <h2 className="text-xl font-bold text-gray-900">Learner Activity Launcher</h2>
                    <p className="text-sm text-gray-600 mt-1">
                      Experience the distraction-free learner interface with TTS narration, progressive hints, and Cognitive Calm feedback.
                    </p>
                  </div>
                  <a
                    href="/learn"
                    className="inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-indigo-600 text-white font-semibold hover:bg-indigo-700 shadow-sm transition-all"
                  >
                    <PlayCircle className="w-5 h-5" />
                    <span>Launch Learner Experience</span>
                  </a>
                </div>
              </div>

              {/* Supported Modalities Showcase */}
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {[
                  { name: "Multiple Choice", type: "multiple_choice", desc: "Select target among calibrated options" },
                  { name: "Matching Pairs", type: "matching", desc: "Connect related items across two columns" },
                  { name: "Sequential Ordering", type: "ordering", desc: "Arrange items along an ordered continuum" },
                  { name: "Visual Identification", type: "visual_identification", desc: "Identify target items in accessible scenes" },
                  { name: "Drag & Drop", type: "drag_drop", desc: "Categorize items into distinct target buckets" },
                ].map((mod) => (
                  <div key={mod.type} className="bg-white p-5 rounded-2xl border border-gray-200 shadow-sm flex flex-col justify-between">
                    <div>
                      <h3 className="font-bold text-gray-900 mb-1">{mod.name}</h3>
                      <p className="text-xs text-gray-600 mb-4">{mod.desc}</p>
                    </div>
                    <a
                      href={`/learn?activity_type=${mod.type}`}
                      className="inline-flex items-center justify-center gap-1.5 px-3 py-2 rounded-xl bg-indigo-50 text-indigo-700 hover:bg-indigo-600 hover:text-white text-xs font-semibold transition-colors"
                    >
                      <PlayCircle className="w-4 h-4" />
                      <span>Practice {mod.name}</span>
                    </a>
                  </div>
                ))}
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
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-gray-200 shadow-sm">
                <div>
                  <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-indigo-600" />
                    Adaptive Learning Intelligence Engine
                  </h2>
                  <p className="text-sm text-gray-600 mt-1">
                    Deterministic curriculum sequencing, difficulty calibration, and modality optimization.
                  </p>
                </div>
                {learners.length > 0 && (
                  <div className="flex items-center gap-3">
                    <label htmlFor="learner-select" className="text-sm font-semibold text-gray-700 whitespace-nowrap">
                      Select Learner:
                    </label>
                    <select
                      id="learner-select"
                      value={selectedLearnerId}
                      onChange={(e) => setSelectedLearnerId(e.target.value)}
                      className="rounded-xl border-gray-300 shadow-sm text-sm font-medium py-2 px-3 focus:ring-indigo-500 focus:border-indigo-500 bg-gray-50 text-gray-900"
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

              {loadingLearners ? (
                <div className="p-8 text-center bg-white rounded-2xl border border-gray-200">
                  <div className="animate-spin w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full mx-auto mb-3" />
                  <p className="text-sm text-gray-600">Loading learners...</p>
                </div>
              ) : learners.length === 0 ? (
                <div className="p-8 text-center bg-white rounded-2xl border border-gray-200">
                  <p className="text-sm text-gray-600">No learners found in your classroom.</p>
                </div>
              ) : (
                <>
                  {recError && (
                    <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 text-amber-800 text-sm">
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

    </div>
  );
};
