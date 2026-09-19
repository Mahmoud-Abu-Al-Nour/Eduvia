import React, { useEffect, useState } from "react";
import api from "@/services/api";
import { Learner } from "@/types";
import {
  Users,
  Plus,
  ArrowLeft,
  Edit3,
  Search,
  BookOpen,
  MessageSquare,
  Layers,
  AlertCircle,
  X,
  FileText,
} from "lucide-react";

export const LearnerManager: React.FC = () => {
  const [learners, setLearners] = useState<Learner[]>([]);
  const [selectedLearner, setSelectedLearner] = useState<Learner | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [ageFilter, setAgeFilter] = useState("all");

  // Modals
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isObsModalOpen, setIsObsModalOpen] = useState(false);

  // Active profile sub-tab
  const [profileTab, setProfileTab] = useState<"overview" | "controls" | "patterns" | "evidence">("overview");

  const fetchLearners = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.get<Learner[]>("/learners");
      setLearners(data);
    } catch (err: any) {
      setError(err.message || "Failed to load learners");
    } finally {
      setLoading(false);
    }
  };

  const fetchLearnerDetail = async (id: string) => {
    try {
      const detail = await api.get<Learner>(`/learners/${id}`);
      setSelectedLearner(detail);
    } catch (err: any) {
      setError(err.message || "Failed to fetch learner details");
    }
  };

  useEffect(() => {
    void fetchLearners();
  }, []);

  const handleSelectLearner = (learner: Learner) => {
    void fetchLearnerDetail(learner.id);
  };

  const filteredLearners = learners.filter((l) => {
    const matchesSearch = l.name.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesAge = ageFilter === "all" || l.age_group === ageFilter;
    return matchesSearch && matchesAge;
  });

  return (
    <div className="space-y-6">
      {error && (
        <div
          role="alert"
          className="p-4 bg-red-50 border border-red-200 text-red-700 rounded-xl flex items-center justify-between"
        >
          <div className="flex items-center space-x-2">
            <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0" />
            <span className="text-sm">{error}</span>
          </div>
          <button
            onClick={() => setError(null)}
            className="text-red-500 hover:text-red-700 p-1"
            aria-label="Dismiss error"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {selectedLearner ? (
        /* Detailed Learner Profile View */
        <div className="space-y-6">
          {/* Top Breadcrumb & Actions */}
          <div className="flex flex-wrap items-center justify-between gap-4">
            <button
              onClick={() => {
                setSelectedLearner(null);
                void fetchLearners();
              }}
              className="inline-flex items-center text-sm font-medium text-gray-600 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-lg px-2 py-1 transition-colors"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Learner List
            </button>

            <div className="flex items-center space-x-3">
              <button
                onClick={() => setIsObsModalOpen(true)}
                className="inline-flex items-center px-3.5 py-2 text-sm font-medium text-blue-700 bg-blue-50 hover:bg-blue-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
              >
                <Plus className="w-4 h-4 mr-1.5" />
                Record Observation
              </button>
              <button
                onClick={() => setIsEditModalOpen(true)}
                className="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors shadow-sm"
              >
                <Edit3 className="w-4 h-4 mr-1.5" />
                Edit Profile
              </button>
            </div>
          </div>

          {/* Profile Header Card */}
          <div className="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h2 className="text-2xl font-bold text-gray-900">{selectedLearner.name}</h2>
                <div className="flex flex-wrap items-center gap-2 mt-2">
                  <span className="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-semibold bg-blue-50 text-blue-700 capitalize">
                    {selectedLearner.age_group.replace("_", " ")}
                  </span>
                  <span className="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-semibold bg-emerald-50 text-emerald-700 capitalize">
                    {selectedLearner.learning_level}
                  </span>
                  <span className="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-700">
                    Status: {selectedLearner.is_active ? "Active" : "Inactive"}
                  </span>
                </div>
              </div>

              {selectedLearner.profile?.teacher_overrides?.manual_adjustments_active && (
                <div className="bg-amber-50 border border-amber-200 rounded-xl px-4 py-2 text-xs text-amber-800 flex items-center">
                  <span className="font-semibold mr-1">Teacher Override Active:</span>
                  Difficulty locked at Level {selectedLearner.profile.teacher_overrides.lock_difficulty_level ?? "N/A"}
                </div>
              )}
            </div>

            {/* Profile Navigation Tabs */}
            <div className="flex border-b border-gray-200 mt-6 space-x-6">
              {[
                { id: "overview", label: "Overview & Support", icon: BookOpen },
                { id: "controls", label: "Preferences & Controls", icon: MessageSquare },
                { id: "patterns", label: "Observed Patterns", icon: Layers },
                { id: "evidence", label: "Observation Log", icon: FileText },
              ].map((tab) => {
                const Icon = tab.icon;
                const isActive = profileTab === tab.id;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setProfileTab(tab.id as any)}
                    className={`inline-flex items-center py-3 text-sm font-medium border-b-2 transition-colors ${
                      isActive
                        ? "border-blue-600 text-blue-600 font-semibold"
                        : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                    }`}
                  >
                    <Icon className="w-4 h-4 mr-2" />
                    {tab.label}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Profile Content Body */}
          <div className="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm">
            {profileTab === "overview" && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-base font-semibold text-gray-900 mb-2">Teacher Notes & Guidance</h3>
                  <div className="bg-gray-50 p-4 rounded-xl text-sm text-gray-700 border border-gray-100">
                    {selectedLearner.profile?.teacher_notes || "No teacher notes recorded yet."}
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="border border-gray-100 p-5 rounded-xl bg-gray-50/50">
                    <h4 className="text-sm font-semibold text-gray-900 mb-3">Support Requirements</h4>
                    <dl className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <dt className="text-gray-500">Pacing:</dt>
                        <dd className="font-medium text-gray-900 capitalize">
                          {selectedLearner.profile?.support_requirements?.pacing || "standard"}
                        </dd>
                      </div>
                      <div className="flex justify-between">
                        <dt className="text-gray-500">Instructional Guidance:</dt>
                        <dd className="font-medium text-gray-900 capitalize">
                          {selectedLearner.profile?.support_requirements?.guidance_level || "moderate"}
                        </dd>
                      </div>
                      <div className="flex justify-between">
                        <dt className="text-gray-500">Frequent Breaks:</dt>
                        <dd className="font-medium text-gray-900">
                          {selectedLearner.profile?.support_requirements?.frequent_breaks ? "Yes" : "No"}
                        </dd>
                      </div>
                    </dl>
                  </div>

                  <div className="border border-gray-100 p-5 rounded-xl bg-gray-50/50">
                    <h4 className="text-sm font-semibold text-gray-900 mb-3">Current Skill Baseline</h4>
                    <dl className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <dt className="text-gray-500">Literacy Stage:</dt>
                        <dd className="font-medium text-gray-900 capitalize">
                          {selectedLearner.profile?.current_skill_level?.literacy_stage || "emerging"}
                        </dd>
                      </div>
                      <div className="flex justify-between">
                        <dt className="text-gray-500">Numeracy Stage:</dt>
                        <dd className="font-medium text-gray-900 capitalize">
                          {selectedLearner.profile?.current_skill_level?.numeracy_stage || "emerging"}
                        </dd>
                      </div>
                      <div className="flex justify-between">
                        <dt className="text-gray-500">Observed Focus Span:</dt>
                        <dd className="font-medium text-gray-900">
                          {selectedLearner.profile?.current_skill_level?.attention_span_minutes ?? 10} minutes
                        </dd>
                      </div>
                    </dl>
                  </div>
                </div>
              </div>
            )}

            {profileTab === "controls" && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-base font-semibold text-gray-900 mb-3">Communication Preferences</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-gray-50 p-4 rounded-xl border border-gray-100">
                      <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Primary Mode</span>
                      <p className="mt-1 font-medium text-gray-900 capitalize">
                        {selectedLearner.profile?.communication_preferences?.primary_mode || "verbal"}
                      </p>
                    </div>
                    <div className="bg-gray-50 p-4 rounded-xl border border-gray-100">
                      <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Communication Notes</span>
                      <p className="mt-1 text-sm text-gray-700">
                        {selectedLearner.profile?.communication_preferences?.notes || "None specified."}
                      </p>
                    </div>
                  </div>
                </div>

                <div>
                  <h3 className="text-base font-semibold text-gray-900 mb-3">Teacher Constraints & Boundaries</h3>
                  <div className="border border-gray-200 rounded-xl p-5 space-y-3 bg-gray-50/30">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600">Max Session Duration:</span>
                      <span className="font-semibold text-gray-900">
                        {selectedLearner.profile?.teacher_constraints?.max_session_duration_minutes ?? 20} min
                      </span>
                    </div>
                    <div className="text-sm">
                      <span className="text-gray-600">Teacher Guidelines:</span>
                      <p className="mt-1 text-gray-800 bg-white p-3 rounded-lg border border-gray-200">
                        {selectedLearner.profile?.teacher_constraints?.custom_guidelines || "No specific restrictions."}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {profileTab === "patterns" && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-base font-semibold text-gray-900 mb-3">Modality Effectiveness</h3>
                  <p className="text-xs text-gray-500 mb-4">
                    Evidence recorded across presentation modalities. Dynamic observations, not permanent classifications.
                  </p>
                  <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
                    {["Visual", "Reading/Text", "Writing", "Audio", "Interactive"].map((mod) => {
                      const data = selectedLearner.profile?.modality_effectiveness?.[mod] || { observed_count: 0 };
                      return (
                        <div key={mod} className="p-4 bg-gray-50 rounded-xl border border-gray-100 text-center">
                          <span className="text-xs font-medium text-gray-500 block mb-1">{mod}</span>
                          <span className="text-lg font-bold text-gray-900">{data.observed_count}</span>
                          <span className="text-xs text-gray-400 block mt-1">observations</span>
                        </div>
                      );
                    })}
                  </div>
                </div>

                <div>
                  <h3 className="text-base font-semibold text-gray-900 mb-3">Teaching Strategy Effectiveness</h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3">
                    {[
                      "Step-by-Step",
                      "Repetition",
                      "Scaffolding",
                      "Prompting",
                      "Simplification",
                      "Demonstration",
                      "Positive Reinforcement",
                      "Gradual Difficulty",
                    ].map((strat) => {
                      const data = selectedLearner.profile?.strategy_effectiveness?.[strat] || { observed_count: 0 };
                      return (
                        <div key={strat} className="p-3.5 bg-gray-50 rounded-xl border border-gray-100">
                          <span className="text-xs font-semibold text-gray-700 block">{strat}</span>
                          <div className="flex items-baseline justify-between mt-2 text-xs">
                            <span className="text-gray-500">Count: {data.observed_count}</span>
                            <span className="text-emerald-700 font-medium">
                              {data.success_rate != null ? `${Math.round(data.success_rate * 100)}%` : "N/A"}
                            </span>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            )}

            {profileTab === "evidence" && (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-base font-semibold text-gray-900">Recorded Learning Observations</h3>
                  <button
                    onClick={() => setIsObsModalOpen(true)}
                    className="text-xs font-semibold text-blue-600 hover:text-blue-800"
                  >
                    + Add New Observation
                  </button>
                </div>

                {(!selectedLearner.profile?.observations || selectedLearner.profile.observations.length === 0) ? (
                  <div className="p-8 text-center text-gray-500 bg-gray-50 rounded-xl border border-dashed border-gray-200">
                    No observations recorded yet. Click "Record Observation" to log pedagogical evidence.
                  </div>
                ) : (
                  <div className="space-y-3">
                    {selectedLearner.profile.observations.map((obs) => (
                      <div key={obs.id} className="p-4 bg-gray-50 rounded-xl border border-gray-100 text-sm">
                        <div className="flex items-center justify-between mb-1">
                          <span className="px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-700 capitalize">
                            {obs.category}
                          </span>
                          <span className="text-xs text-gray-400">
                            {new Date(obs.timestamp).toLocaleDateString()}
                          </span>
                        </div>
                        <p className="text-gray-900 font-medium mt-1">{obs.summary}</p>
                        {obs.teacher_note && (
                          <p className="text-xs text-gray-600 mt-2 bg-white p-2 rounded border border-gray-200">
                            <span className="font-semibold text-gray-700">Teacher Note:</span> {obs.teacher_note}
                          </p>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      ) : (
        /* Learner List View */
        <div className="space-y-6">
          {/* List Header & Controls */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h2 className="text-xl font-bold text-gray-900">Learners</h2>
              <p className="text-sm text-gray-500">
                Manage student profiles and observed learning evidence.
              </p>
            </div>
            <button
              onClick={() => setIsCreateModalOpen(true)}
              className="inline-flex items-center justify-center px-4 py-2.5 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors shadow-sm"
            >
              <Plus className="w-4 h-4 mr-2" />
              Add Learner
            </button>
          </div>

          {/* Search & Filter Bar */}
          <div className="flex flex-col sm:flex-row gap-3">
            <div className="relative flex-1">
              <Search className="w-4 h-4 absolute left-3.5 top-3.5 text-gray-400" />
              <input
                type="text"
                placeholder="Search learners by name..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white"
              />
            </div>
            <select
              value={ageFilter}
              onChange={(e) => setAgeFilter(e.target.value)}
              className="px-4 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-gray-700"
              aria-label="Filter by age group"
            >
              <option value="all">All Age Groups</option>
              <option value="early_childhood">Early Childhood</option>
              <option value="primary">Primary</option>
              <option value="intermediate">Intermediate</option>
              <option value="secondary">Secondary</option>
            </select>
          </div>

          {/* Learners Grid */}
          {loading ? (
            <div className="p-12 text-center text-gray-500" role="status">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-600 border-t-transparent mb-2"></div>
              <p className="text-sm">Loading learners...</p>
            </div>
          ) : filteredLearners.length === 0 ? (
            <div className="bg-white p-12 rounded-2xl border border-gray-100 text-center shadow-sm">
              <Users className="w-12 h-12 text-gray-300 mx-auto mb-3" />
              <h3 className="text-base font-semibold text-gray-900 mb-1">No learners found</h3>
              <p className="text-sm text-gray-500 mb-6">
                {searchQuery ? "No learners match your search filter." : "Get started by adding your first student profile."}
              </p>
              {!searchQuery && (
                <button
                  onClick={() => setIsCreateModalOpen(true)}
                  className="inline-flex items-center px-4 py-2 text-sm font-medium text-blue-600 bg-blue-50 hover:bg-blue-100 rounded-xl transition-colors"
                >
                  <Plus className="w-4 h-4 mr-1.5" />
                  Add Learner
                </button>
              )}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
              {filteredLearners.map((learner) => (
                <div
                  key={learner.id}
                  onClick={() => handleSelectLearner(learner)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" || e.key === " ") {
                      e.preventDefault();
                      handleSelectLearner(learner);
                    }
                  }}
                  tabIndex={0}
                  role="button"
                  aria-label={`View profile for ${learner.name}`}
                  className="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm hover:shadow-md hover:border-blue-200 transition-all cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500 group"
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="w-10 h-10 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-bold text-base">
                      {learner.name.charAt(0).toUpperCase()}
                    </div>
                    <span className="text-xs px-2 py-0.5 rounded-md font-medium bg-gray-100 text-gray-700 capitalize">
                      {learner.learning_level}
                    </span>
                  </div>

                  <h3 className="text-base font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
                    {learner.name}
                  </h3>

                  <p className="text-xs text-gray-500 mt-1 capitalize">
                    Age Group: {learner.age_group.replace("_", " ")}
                  </p>

                  <div className="mt-4 pt-3 border-t border-gray-100 flex items-center justify-between text-xs text-gray-400">
                    <span>Active Profile</span>
                    <span className="text-blue-600 font-medium group-hover:underline">View Profile &rarr;</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* ---------------------------------------------------------
          Create Learner Modal
         --------------------------------------------------------- */}
      {isCreateModalOpen && (
        <CreateLearnerModal
          onClose={() => setIsCreateModalOpen(false)}
          onCreated={() => {
            setIsCreateModalOpen(false);
            void fetchLearners();
          }}
        />
      )}

      {/* ---------------------------------------------------------
          Edit Profile Modal
         --------------------------------------------------------- */}
      {isEditModalOpen && selectedLearner && (
        <EditProfileModal
          learner={selectedLearner}
          onClose={() => setIsEditModalOpen(false)}
          onUpdated={(updated) => {
            setSelectedLearner(updated);
            setIsEditModalOpen(false);
          }}
        />
      )}

      {/* ---------------------------------------------------------
          Record Observation Modal
         --------------------------------------------------------- */}
      {isObsModalOpen && selectedLearner && (
        <RecordObservationModal
          learnerId={selectedLearner.id}
          onClose={() => setIsObsModalOpen(false)}
          onAdded={() => {
            setIsObsModalOpen(false);
            void fetchLearnerDetail(selectedLearner.id);
          }}
        />
      )}
    </div>
  );
};

// ---------------------------------------------------------
// Sub-component: Create Learner Modal
// ---------------------------------------------------------

interface CreateLearnerModalProps {
  onClose: () => void;
  onCreated: () => void;
}

const CreateLearnerModal: React.FC<CreateLearnerModalProps> = ({ onClose, onCreated }) => {
  const [name, setName] = useState("");
  const [ageGroup, setAgeGroup] = useState("primary");
  const [learningLevel, setLearningLevel] = useState("beginner");
  const [teacherNotes, setTeacherNotes] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) {
      setError("Learner name is required");
      return;
    }

    setSubmitting(true);
    setError(null);
    try {
      await api.post("/learners", {
        name: name.trim(),
        age_group: ageGroup,
        learning_level: learningLevel,
        teacher_notes: teacherNotes.trim() || undefined,
      });
      onCreated();
    } catch (err: any) {
      setError(err.message || "Failed to create learner");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div
      className="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="create-learner-title"
    >
      <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-xl border border-gray-100">
        <div className="flex items-center justify-between pb-4 border-b border-gray-100">
          <h3 id="create-learner-title" className="text-lg font-bold text-gray-900">
            Add New Learner
          </h3>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-gray-400 hover:text-gray-600 focus:ring-2 focus:ring-blue-500"
            aria-label="Close modal"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {error && (
          <div className="mt-4 p-3 bg-red-50 text-red-700 text-xs rounded-lg">{error}</div>
        )}

        <form onSubmit={handleSubmit} className="mt-4 space-y-4">
          <div>
            <label className="block text-xs font-semibold text-gray-700 uppercase tracking-wider mb-1">
              Learner Name *
            </label>
            <input
              type="text"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Tariq Ahmed"
              className="w-full px-3.5 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-gray-700 uppercase tracking-wider mb-1">
                Age Group
              </label>
              <select
                value={ageGroup}
                onChange={(e) => setAgeGroup(e.target.value)}
                className="w-full px-3.5 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
              >
                <option value="early_childhood">Early Childhood</option>
                <option value="primary">Primary</option>
                <option value="intermediate">Intermediate</option>
                <option value="secondary">Secondary</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-gray-700 uppercase tracking-wider mb-1">
                Learning Level
              </label>
              <select
                value={learningLevel}
                onChange={(e) => setLearningLevel(e.target.value)}
                className="w-full px-3.5 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
              >
                <option value="emerging">Emerging</option>
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-gray-700 uppercase tracking-wider mb-1">
              Initial Teacher Notes
            </label>
            <textarea
              rows={3}
              value={teacherNotes}
              onChange={(e) => setTeacherNotes(e.target.value)}
              placeholder="Enter initial pedagogical observations or support preferences..."
              className="w-full px-3.5 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div className="flex justify-end space-x-3 pt-4 border-t border-gray-100">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-xl transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="px-5 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-xl shadow-sm focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
            >
              {submitting ? "Creating..." : "Create Learner"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

// ---------------------------------------------------------
// Sub-component: Edit Profile Modal
// ---------------------------------------------------------

interface EditProfileModalProps {
  learner: Learner;
  onClose: () => void;
  onUpdated: (updated: Learner) => void;
}

const EditProfileModal: React.FC<EditProfileModalProps> = ({ learner, onClose, onUpdated }) => {
  const [name, setName] = useState(learner.name);
  const [learningLevel, setLearningLevel] = useState(learner.learning_level);
  const [teacherNotes, setTeacherNotes] = useState(learner.profile?.teacher_notes || "");
  const [pacing, setPacing] = useState(learner.profile?.support_requirements?.pacing || "standard");
  const [guidanceLevel, setGuidanceLevel] = useState(
    learner.profile?.support_requirements?.guidance_level || "moderate"
  );
  const [frequentBreaks, setFrequentBreaks] = useState(
    learner.profile?.support_requirements?.frequent_breaks || false
  );
  const [maxDuration, setMaxDuration] = useState(
    learner.profile?.teacher_constraints?.max_session_duration_minutes || 20
  );
  const [customGuidelines, setCustomGuidelines] = useState(
    learner.profile?.teacher_constraints?.custom_guidelines || ""
  );

  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);

    try {
      const payload = {
        name: name.trim(),
        learning_level: learningLevel,
        profile: {
          teacher_notes: teacherNotes.trim(),
          support_requirements: {
            ...learner.profile?.support_requirements,
            pacing,
            guidance_level: guidanceLevel,
            frequent_breaks: frequentBreaks,
          },
          teacher_constraints: {
            ...learner.profile?.teacher_constraints,
            max_session_duration_minutes: Number(maxDuration),
            custom_guidelines: customGuidelines.trim(),
          },
        },
      };

      const updated = await api.patch<Learner>(`/learners/${learner.id}`, payload);
      onUpdated(updated);
    } catch (err: any) {
      setError(err.message || "Failed to update profile");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div
      className="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="edit-profile-title"
    >
      <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-xl border border-gray-100 max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between pb-4 border-b border-gray-100">
          <h3 id="edit-profile-title" className="text-lg font-bold text-gray-900">
            Edit Pedagogical Profile
          </h3>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-gray-400 hover:text-gray-600 focus:ring-2 focus:ring-blue-500"
            aria-label="Close modal"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {error && (
          <div className="mt-4 p-3 bg-red-50 text-red-700 text-xs rounded-lg">{error}</div>
        )}

        <form onSubmit={handleUpdate} className="mt-4 space-y-4">
          <div>
            <label className="block text-xs font-semibold text-gray-700 uppercase tracking-wider mb-1">
              Learner Name
            </label>
            <input
              type="text"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-3.5 py-2.5 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-gray-700 uppercase tracking-wider mb-1">
              Learning Level
            </label>
            <select
              value={learningLevel}
              onChange={(e) => setLearningLevel(e.target.value)}
              className="w-full px-3.5 py-2.5 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 bg-white"
            >
              <option value="emerging">Emerging</option>
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-gray-700 uppercase tracking-wider mb-1">
              Teacher Notes
            </label>
            <textarea
              rows={3}
              value={teacherNotes}
              onChange={(e) => setTeacherNotes(e.target.value)}
              className="w-full px-3.5 py-2.5 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-gray-700 uppercase tracking-wider mb-1">
                Pacing
              </label>
              <select
                value={pacing}
                onChange={(e) => setPacing(e.target.value)}
                className="w-full px-3.5 py-2.5 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 bg-white"
              >
                <option value="relaxed">Relaxed</option>
                <option value="standard">Standard</option>
                <option value="accelerated">Accelerated</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-gray-700 uppercase tracking-wider mb-1">
                Guidance Level
              </label>
              <select
                value={guidanceLevel}
                onChange={(e) => setGuidanceLevel(e.target.value)}
                className="w-full px-3.5 py-2.5 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 bg-white"
              >
                <option value="minimal">Minimal</option>
                <option value="moderate">Moderate</option>
                <option value="intensive">Intensive</option>
              </select>
            </div>
          </div>

          <div className="flex items-center space-x-2 pt-1">
            <input
              type="checkbox"
              id="frequentBreaks"
              checked={frequentBreaks}
              onChange={(e) => setFrequentBreaks(e.target.checked)}
              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500 h-4 w-4"
            />
            <label htmlFor="frequentBreaks" className="text-sm text-gray-700">
              Needs Frequent Breaks
            </label>
          </div>

          <div className="border-t border-gray-100 pt-3">
            <label className="block text-xs font-semibold text-gray-700 uppercase tracking-wider mb-1">
              Max Session Duration (Minutes)
            </label>
            <input
              type="number"
              min={5}
              max={120}
              value={maxDuration}
              onChange={(e) => setMaxDuration(Number(e.target.value))}
              className="w-full px-3.5 py-2.5 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-gray-700 uppercase tracking-wider mb-1">
              Custom Teacher Guidelines
            </label>
            <input
              type="text"
              value={customGuidelines}
              onChange={(e) => setCustomGuidelines(e.target.value)}
              placeholder="e.g. Prioritize interactive manipulatives"
              className="w-full px-3.5 py-2.5 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div className="flex justify-end space-x-3 pt-4 border-t border-gray-100">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-xl transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="px-5 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-xl shadow-sm focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
            >
              {submitting ? "Saving..." : "Save Changes"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

// ---------------------------------------------------------
// Sub-component: Record Observation Modal
// ---------------------------------------------------------

interface RecordObservationModalProps {
  learnerId: string;
  onClose: () => void;
  onAdded: () => void;
}

const RecordObservationModal: React.FC<RecordObservationModalProps> = ({ learnerId, onClose, onAdded }) => {
  const [category, setCategory] = useState("modality");
  const [summary, setSummary] = useState("");
  const [teacherNote, setTeacherNote] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!summary.trim()) {
      setError("Observation summary is required");
      return;
    }

    setSubmitting(true);
    setError(null);
    try {
      await api.post(`/learners/${learnerId}/observations`, {
        category,
        summary: summary.trim(),
        teacher_note: teacherNote.trim() || undefined,
      });
      onAdded();
    } catch (err: any) {
      setError(err.message || "Failed to record observation");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div
      className="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="obs-modal-title"
    >
      <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-xl border border-gray-100">
        <div className="flex items-center justify-between pb-4 border-b border-gray-100">
          <h3 id="obs-modal-title" className="text-lg font-bold text-gray-900">
            Record Learning Observation
          </h3>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-gray-400 hover:text-gray-600 focus:ring-2 focus:ring-blue-500"
            aria-label="Close modal"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {error && (
          <div className="mt-4 p-3 bg-red-50 text-red-700 text-xs rounded-lg">{error}</div>
        )}

        <form onSubmit={handleSubmit} className="mt-4 space-y-4">
          <div>
            <label className="block text-xs font-semibold text-gray-700 uppercase tracking-wider mb-1">
              Category
            </label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full px-3.5 py-2.5 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 bg-white"
            >
              <option value="modality">Modality Effectiveness</option>
              <option value="strategy">Teaching Strategy</option>
              <option value="activity_type">Activity Type</option>
              <option value="response_behavior">Response Behavior</option>
              <option value="general">General Learning Pattern</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-gray-700 uppercase tracking-wider mb-1">
              Observation Summary *
            </label>
            <textarea
              required
              rows={3}
              value={summary}
              onChange={(e) => setSummary(e.target.value)}
              placeholder="e.g. Demonstrated high engagement and accuracy when visual cues accompanied audio prompts."
              className="w-full px-3.5 py-2.5 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-gray-700 uppercase tracking-wider mb-1">
              Teacher Reflection Note
            </label>
            <input
              type="text"
              value={teacherNote}
              onChange={(e) => setTeacherNote(e.target.value)}
              placeholder="Optional teacher interpretation or next step..."
              className="w-full px-3.5 py-2.5 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div className="flex justify-end space-x-3 pt-4 border-t border-gray-100">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-xl transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="px-5 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-xl shadow-sm focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
            >
              {submitting ? "Recording..." : "Save Observation"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LearnerManager;
