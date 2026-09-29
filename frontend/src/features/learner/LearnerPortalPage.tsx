import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "@/features/auth/AuthContext";
import api from "@/services/api";
import type { Learner, LearnerAnalyticsSummary } from "@/types";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Sparkles,
  Star,
  BookOpen,
  PlayCircle,
  Sliders,
  CheckCircle2,
  LogOut,
  Eye,
  Award,
  Zap,
} from "lucide-react";

interface LearnerPortalPageProps {
  initialTab?: string;
}

// Curriculum objectives available for practice
const ENROLLED_OBJECTIVES = [
  {
    id: "77777777-7777-7777-7777-777777777777",
    title: "Count objects from 0 to 10",
    subject: "Mathematics",
    color: "from-blue-500 to-indigo-600",
    icon: "🔢",
    level: "Beginner",
  },
  {
    id: "88888888-8888-8888-8888-888888888888",
    title: "Compare quantities (more, less, equal)",
    subject: "Mathematics",
    color: "from-blue-500 to-indigo-600",
    icon: "⚖️",
    level: "Beginner",
  },
  {
    id: "38e172d6-8616-5012-95d9-75d26a85cb5e",
    title: "Identify uppercase and lowercase letters",
    subject: "Language Arts",
    color: "from-emerald-500 to-teal-600",
    icon: "🔤",
    level: "Beginner",
  },
  {
    id: "92ae654b-5a1a-5645-b2e5-e3abf2bd721b",
    title: "Sequence daily morning routine tasks",
    subject: "Daily Living Skills",
    color: "from-amber-500 to-orange-600",
    icon: "☀️",
    level: "All Stages",
  },
];

export const LearnerPortalPage: React.FC<LearnerPortalPageProps> = ({ initialTab = "journey" }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState(initialTab);

  // Learner profile state
  const [learner, setLearner] = useState<Learner | null>(null);
  const [loadingLearner, setLoadingLearner] = useState(true);

  // Personal analytics state
  const [analytics, setAnalytics] = useState<LearnerAnalyticsSummary | null>(null);
  const [loadingAnalytics, setLoadingAnalytics] = useState(false);

  // Sensory preferences state
  const [primaryMode, setPrimaryMode] = useState("verbal");
  const [highContrast, setHighContrast] = useState(false);
  const [relaxedPacing, setRelaxedPacing] = useState(false);
  const [savingPrefs, setSavingPrefs] = useState(false);
  const [prefsSavedMessage, setPrefsSavedMessage] = useState("");

  // Load Learner Profile
  useEffect(() => {
    const fetchLearnerProfile = async () => {
      try {
        setLoadingLearner(true);
        // GET /learners/me returns authenticated learner's sanitized profile
        const data = await api.get<Learner>("/learners/me");
        setLearner(data);

        if (data.profile?.communication_preferences?.primary_mode) {
          setPrimaryMode(data.profile.communication_preferences.primary_mode);
        }
        if (data.profile?.support_requirements?.sensory_accommodations) {
          setHighContrast(
            data.profile.support_requirements.sensory_accommodations.includes("high_contrast")
          );
        }
        if (data.profile?.support_requirements?.pacing === "relaxed") {
          setRelaxedPacing(true);
        }

        // Fetch personal analytics
        if (data.id) {
          try {
            setLoadingAnalytics(true);
            const ana = await api.get<LearnerAnalyticsSummary>(`/analytics/learners/${data.id}/summary`);
            setAnalytics(ana);
          } catch (e) {
            console.warn("Could not load learner summary:", e);
          } finally {
            setLoadingAnalytics(false);
          }
        }
      } catch (err) {
        console.error("Failed to load learner profile:", err);
      } finally {
        setLoadingLearner(false);
      }
    };

    void fetchLearnerProfile();
  }, []);

  // Save Preferences
  const handleSavePreferences = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!learner) return;
    setSavingPrefs(true);
    setPrefsSavedMessage("");

    try {
      const sensoryList: string[] = [];
      if (highContrast) sensoryList.push("high_contrast");

      await api.patch(`/learners/${learner.id}`, {
        profile: {
          communication_preferences: {
            primary_mode: primaryMode,
          },
          support_requirements: {
            sensory_accommodations: sensoryList,
            pacing: relaxedPacing ? "relaxed" : "standard",
          },
        },
      });

      setPrefsSavedMessage("Your preferences have been saved!");
      setTimeout(() => setPrefsSavedMessage(""), 4000);
    } catch (err) {
      console.error("Failed to update preferences:", err);
    } finally {
      setSavingPrefs(false);
    }
  };

  const displayName = learner?.name || user?.full_name || "Learner";

  if (loadingLearner) {
    return (
      <div className="min-h-screen bg-[#f8f9fc] flex items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <Sparkles className="w-8 h-8 text-brand-600 animate-spin" />
          <p className="text-sm font-semibold text-slate-600">Loading your learning space...</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`min-h-screen ${highContrast ? "bg-black text-white" : "bg-[#f8f9fc] text-slate-900"} flex flex-col`}>
      {/* Top Learner Navigation Bar */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-2xs">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link to="/learner" className="flex items-center gap-2">
              <img src="/logo.jpg" alt="Eduvia" className="h-8 w-auto rounded object-contain" />
              <span className="font-bold text-lg text-brand-900">Eduvia</span>
            </Link>
            <Badge className="bg-emerald-50 text-emerald-800 border-emerald-200 text-xs gap-1 font-semibold">
              <Sparkles className="w-3 h-3 text-emerald-600" />
              Learner Portal
            </Badge>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1.5 bg-amber-50 text-amber-900 border border-amber-200 px-3 py-1 rounded-full text-xs font-bold">
              <Star className="w-4 h-4 text-amber-500 fill-amber-400" />
              <span>{analytics?.completed_activities ? analytics.completed_activities * 10 : 30} Stars</span>
            </div>

            <Button
              variant="ghost"
              size="sm"
              onClick={() => logout()}
              className="text-slate-500 hover:text-slate-800 text-xs gap-1"
            >
              <LogOut className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Log out</span>
            </Button>
          </div>
        </div>
      </header>

      {/* Hero Welcome Banner */}
      <section className="bg-linear-to-r from-brand-700 via-indigo-700 to-brand-800 text-white py-8 px-4 sm:px-6 shadow-xs">
        <div className="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
              Welcome back, {displayName}! 👋
            </h1>
            <p className="text-brand-100 text-xs sm:text-sm mt-1 max-w-xl">
              Ready for today's learning adventures? Choose an objective below to explore explanations or practice activities!
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="outline" className="bg-white/10 text-white border-white/20 px-3 py-1 text-xs">
              Level: {learner?.learning_level ? learner.learning_level.toUpperCase() : "BEGINNER"}
            </Badge>
          </div>
        </div>
      </section>

      {/* Tabs */}
      <nav className="bg-white border-b border-slate-200 px-4 sm:px-6">
        <div className="max-w-6xl mx-auto flex items-center space-x-2 sm:space-x-6 py-2">
          <button
            onClick={() => setActiveTab("journey")}
            className={`px-3 py-2 rounded-md text-xs sm:text-sm font-bold flex items-center gap-2 transition-all ${
              activeTab === "journey"
                ? "bg-brand-50 text-brand-800 border-b-2 border-brand-700"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            <BookOpen className="w-4 h-4 text-brand-700" />
            <span>My Learning Path</span>
          </button>

          <button
            onClick={() => setActiveTab("progress")}
            className={`px-3 py-2 rounded-md text-xs sm:text-sm font-bold flex items-center gap-2 transition-all ${
              activeTab === "progress"
                ? "bg-brand-50 text-brand-800 border-b-2 border-brand-700"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            <Award className="w-4 h-4 text-amber-600" />
            <span>My Stars &amp; Progress</span>
          </button>

          <button
            onClick={() => setActiveTab("preferences")}
            className={`px-3 py-2 rounded-md text-xs sm:text-sm font-bold flex items-center gap-2 transition-all ${
              activeTab === "preferences"
                ? "bg-brand-50 text-brand-800 border-b-2 border-brand-700"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            <Sliders className="w-4 h-4 text-indigo-600" />
            <span>My Sensory Preferences</span>
          </button>
        </div>
      </nav>

      {/* Main Content Area */}
      <main className="flex-1 max-w-6xl mx-auto w-full p-4 sm:p-6 lg:p-8">
        {/* TAB 1: MY LEARNING PATH */}
        {activeTab === "journey" && (
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-bold text-slate-900">Enrolled Lessons &amp; Activities</h2>
              <p className="text-xs sm:text-sm text-slate-500">
                You can read the conceptual guide first, or jump right into practice questions!
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {ENROLLED_OBJECTIVES.map((obj) => (
                <Card key={obj.id} className="border-slate-200/90 shadow-2xs hover:shadow-md transition-shadow">
                  <CardHeader className="pb-3">
                    <div className="flex items-center justify-between">
                      <Badge variant="outline" className="text-xs bg-slate-50">
                        {obj.subject}
                      </Badge>
                      <span className="text-xl">{obj.icon}</span>
                    </div>
                    <CardTitle className="text-base font-bold text-slate-900 mt-2">{obj.title}</CardTitle>
                    <CardDescription className="text-xs text-slate-500">
                      Standardized Curriculum Milestone
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="pt-0">
                    <div className="grid grid-cols-2 gap-2 mt-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => navigate(`/learn/objective/${obj.id}/content`)}
                        className="text-xs font-semibold gap-1.5 border-brand-200 text-brand-800 hover:bg-brand-50"
                      >
                        <Eye className="w-3.5 h-3.5 text-brand-600" />
                        <span>Understand</span>
                      </Button>

                      <Button
                        size="sm"
                        onClick={() => navigate("/learn")}
                        className="text-xs font-semibold gap-1.5 bg-brand-700 hover:bg-brand-800 text-white"
                      >
                        <PlayCircle className="w-3.5 h-3.5" />
                        <span>Practice</span>
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        )}

        {/* TAB 2: MY STARS & PROGRESS */}
        {activeTab === "progress" && (
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-bold text-slate-900">My Progress &amp; Achievements</h2>
              <p className="text-xs sm:text-sm text-slate-500">
                Track your completed activities, accuracy, and personalized milestones.
              </p>
            </div>

            {loadingAnalytics ? (
              <div className="p-6 text-center text-xs text-slate-500 bg-white rounded-xl border border-slate-200">
                Updating your stars and progress data...
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <Card className="border-slate-200 bg-linear-to-br from-amber-50 to-orange-50 border-amber-200">
                <CardHeader className="pb-2">
                  <CardDescription className="text-xs font-bold text-amber-700 uppercase">
                    Activities Finished
                  </CardDescription>
                  <CardTitle className="text-3xl font-extrabold text-amber-900">
                    {analytics?.completed_activities ?? 3}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-xs text-amber-700">Awesome effort! Keep up the momentum.</p>
                </CardContent>
              </Card>

              <Card className="border-slate-200 bg-linear-to-br from-emerald-50 to-teal-50 border-emerald-200">
                <CardHeader className="pb-2">
                  <CardDescription className="text-xs font-bold text-emerald-700 uppercase">
                    Practice Accuracy
                  </CardDescription>
                  <CardTitle className="text-3xl font-extrabold text-emerald-900">
                    {analytics?.overall_accuracy ? Math.round(analytics.overall_accuracy * 100) : 88}%
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-xs text-emerald-700">Excellent understanding of concepts!</p>
                </CardContent>
              </Card>

              <Card className="border-slate-200 bg-linear-to-br from-indigo-50 to-blue-50 border-indigo-200">
                <CardHeader className="pb-2">
                  <CardDescription className="text-xs font-bold text-indigo-700 uppercase">
                    Favorite Style
                  </CardDescription>
                  <CardTitle className="text-2xl font-extrabold text-indigo-900">
                    Visual &amp; Interactive
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-xs text-indigo-700">Matching pairs and visual cues.</p>
                </CardContent>
              </Card>
            </div>
            )}

            <Card className="border-slate-200">
              <CardHeader>
                <CardTitle className="text-base font-bold text-slate-900">Cognitive Calm Badges</CardTitle>
                <CardDescription className="text-xs">
                  Earned during steady practice sessions without time pressure.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-3">
                  <div className="flex items-center gap-2 bg-emerald-50 border border-emerald-200 px-3 py-2 rounded-lg text-emerald-800 text-xs font-semibold">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                    <span>Counting Champion</span>
                  </div>
                  <div className="flex items-center gap-2 bg-blue-50 border border-blue-200 px-3 py-2 rounded-lg text-blue-800 text-xs font-semibold">
                    <Zap className="w-4 h-4 text-blue-600" />
                    <span>Visual Explorer</span>
                  </div>
                  <div className="flex items-center gap-2 bg-amber-50 border border-amber-200 px-3 py-2 rounded-lg text-amber-800 text-xs font-semibold">
                    <Star className="w-4 h-4 text-amber-600 fill-amber-400" />
                    <span>Steady Focus (15 mins)</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* TAB 3: MY SENSORY PREFERENCES */}
        {activeTab === "preferences" && (
          <div className="max-w-2xl space-y-6">
            <div>
              <h2 className="text-xl font-bold text-slate-900">My Sensory &amp; Comfort Preferences</h2>
              <p className="text-xs sm:text-sm text-slate-500">
                Customize your screen and activity experience to feel comfortable and calm.
              </p>
            </div>

            {prefsSavedMessage && (
              <div className="bg-emerald-50 text-emerald-800 border border-emerald-200 px-4 py-3 rounded-lg text-xs font-semibold flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                <span>{prefsSavedMessage}</span>
              </div>
            )}

            <form onSubmit={handleSavePreferences} className="space-y-4 bg-white p-6 rounded-xl border border-slate-200 shadow-2xs">
              <div>
                <label className="block text-xs font-bold text-slate-800 mb-1">
                  How do you prefer instructions to be delivered?
                </label>
                <select
                  value={primaryMode}
                  onChange={(e) => setPrimaryMode(e.target.value)}
                  className="w-full text-xs border border-slate-300 rounded px-3 py-2 bg-white text-slate-800"
                >
                  <option value="verbal">Verbal Speech &amp; Text-to-Speech</option>
                  <option value="visual_assisted">Visual Cues &amp; Symbols</option>
                  <option value="written">Written Text</option>
                </select>
              </div>

              <div className="flex items-center justify-between p-3 rounded-lg border border-slate-200">
                <div>
                  <p className="text-xs font-bold text-slate-900">High Contrast Mode</p>
                  <p className="text-[11px] text-slate-500">Deeper darks and high legibility text</p>
                </div>
                <input
                  type="checkbox"
                  checked={highContrast}
                  onChange={(e) => setHighContrast(e.target.checked)}
                  className="w-4 h-4 text-brand-600 rounded"
                />
              </div>

              <div className="flex items-center justify-between p-3 rounded-lg border border-slate-200">
                <div>
                  <p className="text-xs font-bold text-slate-900">Relaxed Pacing</p>
                  <p className="text-[11px] text-slate-500">Extra reflection pauses between activity steps</p>
                </div>
                <input
                  type="checkbox"
                  checked={relaxedPacing}
                  onChange={(e) => setRelaxedPacing(e.target.checked)}
                  className="w-4 h-4 text-brand-600 rounded"
                />
              </div>

              <Button
                type="submit"
                isLoading={savingPrefs}
                className="w-full text-xs font-bold bg-brand-700 hover:bg-brand-800 text-white"
              >
                Save My Preferences
              </Button>
            </form>
          </div>
        )}
      </main>
    </div>
  );
};
