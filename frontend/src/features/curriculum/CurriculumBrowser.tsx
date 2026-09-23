import React, { useEffect, useState } from "react";
import api from "@/services/api";
import { BookOpen, ChevronRight, Layers, Award, ArrowLeft, CheckCircle2 } from "lucide-react";

interface LocalizedText {
  en?: string;
  ar?: string;
  [key: string]: string | undefined;
}

interface LearningObjective {
  id: string;
  title: LocalizedText;
  description?: LocalizedText;
  difficulty_level: number;
  assessment_criteria?: {
    minimum_accuracy?: number;
    maximum_assistance_level?: number;
    required_completion?: boolean;
    [key: string]: any;
  };
  order_index: number;
  is_active: boolean;
  prerequisites?: LearningObjective[];
}

interface Lesson {
  id: string;
  title: LocalizedText;
  description?: LocalizedText;
  order_index: number;
  learning_objectives: LearningObjective[];
}

interface Unit {
  id: string;
  title: LocalizedText;
  description?: LocalizedText;
  order_index: number;
  lessons: Lesson[];
}

interface Subject {
  id: string;
  title: LocalizedText;
  description?: LocalizedText;
  order_index: number;
  units: Unit[];
}

interface Curriculum {
  id: string;
  title: LocalizedText;
  description?: LocalizedText;
  version: string;
  is_active: boolean;
  subjects?: Subject[];
}

export const CurriculumBrowser: React.FC = () => {
  const [curricula, setCurricula] = useState<Curriculum[]>([]);
  const [selectedCurriculum, setSelectedCurriculum] = useState<Curriculum | null>(null);
  const [selectedSubject, setSelectedSubject] = useState<Subject | null>(null);
  const [selectedUnit, setSelectedUnit] = useState<Unit | null>(null);
  const [selectedLesson, setSelectedLesson] = useState<Lesson | null>(null);

  const [loading, setLoading] = useState(true);
  const [loadingDetails, setLoadingDetails] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchCurricula = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.get<Curriculum[]>("/curricula");
      setCurricula(data);
    } catch (err: any) {
      setError(err.message || "Failed to load curricula");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCurricula();
  }, []);

  const handleSelectCurriculum = async (curr: Curriculum) => {
    setLoadingDetails(true);
    setError(null);
    try {
      const fullCurr = await api.get<Curriculum>(`/curricula/${curr.id}`);
      setSelectedCurriculum(fullCurr);
      setSelectedSubject(null);
      setSelectedUnit(null);
      setSelectedLesson(null);
    } catch (err: any) {
      setError(err.message || "Failed to load curriculum hierarchy");
    } finally {
      setLoadingDetails(false);
    }
  };

  const getText = (textObj?: LocalizedText): string => {
    if (!textObj) return "";
    return textObj.en || textObj.ar || Object.values(textObj)[0] || "";
  };

  const getSubText = (textObj?: LocalizedText): string | null => {
    if (!textObj) return null;
    if (textObj.en && textObj.ar && textObj.en !== textObj.ar) {
      return textObj.ar;
    }
    return null;
  };

  if (loading) {
    return (
      <div className="p-12 text-center text-gray-500" role="status" aria-live="polite">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-teal-600 border-t-transparent mb-2"></div>
        <p>Loading curricula...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 bg-red-50 rounded-xl border border-red-200 text-red-700" role="alert">
        <p className="font-semibold mb-2">Error loading data</p>
        <p className="text-sm">{error}</p>
        <button
          onClick={fetchCurricula}
          className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header & Breadcrumbs */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Curriculum Browser</h2>
        <p className="text-gray-600 text-sm mt-1">
          Explore standardized educational curricula, subjects, units, lessons, and learning objectives.
        </p>

        {/* Navigation Breadcrumbs */}
        <nav aria-label="Curriculum Navigation" className="mt-4 flex flex-wrap items-center gap-1.5 text-sm">
          <button
            onClick={() => {
              setSelectedCurriculum(null);
              setSelectedSubject(null);
              setSelectedUnit(null);
              setSelectedLesson(null);
            }}
            className={`px-2.5 py-1 rounded-lg transition-colors ${
              !selectedCurriculum
                ? "font-semibold text-teal-800 bg-teal-50 border border-teal-200/60"
                : "text-gray-600 hover:text-gray-900 hover:bg-gray-100"
            }`}
          >
            All Curricula
          </button>

          {selectedCurriculum && (
            <>
              <ChevronRight className="w-4 h-4 text-gray-400" aria-hidden="true" />
              <button
                onClick={() => {
                  setSelectedSubject(null);
                  setSelectedUnit(null);
                  setSelectedLesson(null);
                }}
                className={`px-2.5 py-1 rounded-lg transition-colors ${
                  !selectedSubject
                    ? "font-semibold text-teal-800 bg-teal-50 border border-teal-200/60"
                    : "text-gray-600 hover:text-gray-900 hover:bg-gray-100"
                }`}
              >
                {getText(selectedCurriculum.title)}
              </button>
            </>
          )}

          {selectedSubject && (
            <>
              <ChevronRight className="w-4 h-4 text-gray-400" aria-hidden="true" />
              <button
                onClick={() => {
                  setSelectedUnit(null);
                  setSelectedLesson(null);
                }}
                className={`px-2.5 py-1 rounded-lg transition-colors ${
                  !selectedUnit
                    ? "font-semibold text-teal-800 bg-teal-50 border border-teal-200/60"
                    : "text-gray-600 hover:text-gray-900 hover:bg-gray-100"
                }`}
              >
                {getText(selectedSubject.title)}
              </button>
            </>
          )}

          {selectedUnit && (
            <>
              <ChevronRight className="w-4 h-4 text-gray-400" aria-hidden="true" />
              <button
                onClick={() => setSelectedLesson(null)}
                className={`px-2.5 py-1 rounded-lg transition-colors ${
                  !selectedLesson
                    ? "font-semibold text-teal-800 bg-teal-50 border border-teal-200/60"
                    : "text-gray-600 hover:text-gray-900 hover:bg-gray-100"
                }`}
              >
                {getText(selectedUnit.title)}
              </button>
            </>
          )}

          {selectedLesson && (
            <>
              <ChevronRight className="w-4 h-4 text-gray-400" aria-hidden="true" />
              <span className="font-semibold text-teal-800 bg-teal-50 border border-teal-200/60 px-2.5 py-1 rounded-lg">
                {getText(selectedLesson.title)}
              </span>
            </>
          )}
        </nav>
      </div>

      {loadingDetails && (
        <div className="p-8 text-center text-gray-500" role="status">
          <div className="inline-block animate-spin rounded-full h-6 w-6 border-2 border-teal-600 border-t-transparent mb-2"></div>
          <p className="text-sm">Loading details...</p>
        </div>
      )}

      {/* Level 0: Curricula List */}
      {!selectedCurriculum && !loadingDetails && (
        <>
          {curricula.length === 0 ? (
            <div className="p-8 bg-gray-50 rounded-2xl border border-gray-200 text-center text-gray-500">
              <BookOpen className="w-10 h-10 mx-auto text-gray-400 mb-2" />
              <p className="font-medium">No curricula found.</p>
              <p className="text-sm text-gray-400 mt-1">Please seed the database using the seed script.</p>
            </div>
          ) : (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {curricula.map((curr) => (
                <div
                  key={curr.id}
                  className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 hover:shadow-md transition-all flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-start justify-between gap-2 mb-2">
                      <h3 className="text-lg font-bold text-gray-900">
                        {getText(curr.title)}
                      </h3>
                      <span className="text-xs font-semibold bg-teal-50 text-teal-800 border border-teal-200/60 px-2.5 py-0.5 rounded-full whitespace-nowrap">
                        v{curr.version}
                      </span>
                    </div>
                    {getSubText(curr.title) && (
                      <p className="text-sm font-arabic text-gray-500 mb-2" dir="rtl">
                        {getSubText(curr.title)}
                      </p>
                    )}
                    <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                      {getText(curr.description) || "No description provided."}
                    </p>
                  </div>

                  <button
                    onClick={() => handleSelectCurriculum(curr)}
                    className="w-full mt-2 inline-flex items-center justify-center gap-2 px-4 py-2 bg-teal-50 text-teal-800 hover:bg-teal-700 hover:text-white rounded-xl text-sm font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-teal-600"
                    aria-label={`Explore ${getText(curr.title)}`}
                  >
                    <span>Explore Hierarchy</span>
                    <ChevronRight className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </>
      )}

      {/* Level 1: Curriculum Selected -> Show Subjects */}
      {selectedCurriculum && !selectedSubject && !loadingDetails && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-xl font-bold text-gray-900">Subjects</h3>
              <p className="text-sm text-gray-600">Select a subject to view its structured units.</p>
            </div>
            <button
              onClick={() => setSelectedCurriculum(null)}
              className="inline-flex items-center gap-1.5 text-sm text-gray-600 hover:text-gray-900 font-medium"
            >
              <ArrowLeft className="w-4 h-4" /> Back to Curricula
            </button>
          </div>

          {!selectedCurriculum.subjects || selectedCurriculum.subjects.length === 0 ? (
            <div className="p-6 bg-gray-50 rounded-xl border border-gray-200 text-center text-gray-500">
              No subjects found in this curriculum.
            </div>
          ) : (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {selectedCurriculum.subjects.map((subj) => (
                <div
                  key={subj.id}
                  className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <Layers className="w-5 h-5 text-indigo-600" />
                      <h4 className="font-bold text-gray-900">{getText(subj.title)}</h4>
                    </div>
                    {getSubText(subj.title) && (
                      <p className="text-sm text-gray-500 font-arabic mb-2" dir="rtl">
                        {getSubText(subj.title)}
                      </p>
                    )}
                    <p className="text-sm text-gray-600 line-clamp-2 mb-4">
                      {getText(subj.description) || "Standard subject curriculum track."}
                    </p>
                  </div>

                  <button
                    onClick={() => setSelectedSubject(subj)}
                    className="w-full inline-flex items-center justify-center gap-1.5 px-3 py-2 bg-teal-50 text-teal-800 hover:bg-teal-700 hover:text-white rounded-xl text-sm font-semibold transition-colors focus:ring-2 focus:ring-teal-600"
                  >
                    <span>View Units ({subj.units?.length || 0})</span>
                    <ChevronRight className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Level 2: Subject Selected -> Show Units */}
      {selectedSubject && !selectedUnit && !loadingDetails && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-xl font-bold text-gray-900">{getText(selectedSubject.title)}: Units</h3>
              <p className="text-sm text-gray-600">Select a unit to inspect lessons.</p>
            </div>
            <button
              onClick={() => setSelectedSubject(null)}
              className="inline-flex items-center gap-1.5 text-sm text-gray-600 hover:text-gray-900 font-medium"
            >
              <ArrowLeft className="w-4 h-4" /> Back to Subjects
            </button>
          </div>

          {!selectedSubject.units || selectedSubject.units.length === 0 ? (
            <div className="p-6 bg-gray-50 rounded-xl border border-gray-200 text-center text-gray-500">
              No units found in this subject.
            </div>
          ) : (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {selectedSubject.units.map((unit) => (
                <div
                  key={unit.id}
                  className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all flex flex-col justify-between"
                >
                  <div>
                    <h4 className="font-bold text-gray-900 mb-1">{getText(unit.title)}</h4>
                    {getSubText(unit.title) && (
                      <p className="text-sm text-gray-500 font-arabic mb-2" dir="rtl">
                        {getSubText(unit.title)}
                      </p>
                    )}
                    <p className="text-sm text-gray-600 line-clamp-2 mb-4">
                      {getText(unit.description) || "Progressive learning unit."}
                    </p>
                  </div>

                  <button
                    onClick={() => setSelectedUnit(unit)}
                    className="w-full inline-flex items-center justify-center gap-1.5 px-3 py-2 bg-teal-50 text-teal-800 hover:bg-teal-700 hover:text-white rounded-xl text-sm font-semibold transition-colors focus:ring-2 focus:ring-teal-600"
                  >
                    <span>View Lessons ({unit.lessons?.length || 0})</span>
                    <ChevronRight className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Level 3: Unit Selected -> Show Lessons */}
      {selectedUnit && !selectedLesson && !loadingDetails && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-xl font-bold text-gray-900">{getText(selectedUnit.title)}: Lessons</h3>
              <p className="text-sm text-gray-600">Select a lesson to review target learning objectives.</p>
            </div>
            <button
              onClick={() => setSelectedUnit(null)}
              className="inline-flex items-center gap-1.5 text-sm text-gray-600 hover:text-gray-900 font-medium"
            >
              <ArrowLeft className="w-4 h-4" /> Back to Units
            </button>
          </div>

          {!selectedUnit.lessons || selectedUnit.lessons.length === 0 ? (
            <div className="p-6 bg-gray-50 rounded-xl border border-gray-200 text-center text-gray-500">
              No lessons found in this unit.
            </div>
          ) : (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {selectedUnit.lessons.map((lesson) => (
                <div
                  key={lesson.id}
                  className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all flex flex-col justify-between"
                >
                  <div>
                    <h4 className="font-bold text-gray-900 mb-1">{getText(lesson.title)}</h4>
                    {getSubText(lesson.title) && (
                      <p className="text-sm text-gray-500 font-arabic mb-2" dir="rtl">
                        {getSubText(lesson.title)}
                      </p>
                    )}
                    <p className="text-sm text-gray-600 line-clamp-2 mb-4">
                      {getText(lesson.description) || "Interactive didactic lesson."}
                    </p>
                  </div>

                  <button
                    onClick={() => setSelectedLesson(lesson)}
                    className="w-full inline-flex items-center justify-center gap-1.5 px-3 py-2 bg-teal-50 text-teal-800 hover:bg-teal-700 hover:text-white rounded-xl text-sm font-semibold transition-colors focus:ring-2 focus:ring-teal-600"
                  >
                    <span>View Objectives ({lesson.learning_objectives?.length || 0})</span>
                    <ChevronRight className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Level 4: Lesson Selected -> Show Learning Objectives */}
      {selectedLesson && !loadingDetails && (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-xl font-bold text-gray-900">
                Objectives for: {getText(selectedLesson.title)}
              </h3>
              <p className="text-sm text-gray-600">
                Measurable mastery targets with assessment criteria and prerequisites.
              </p>
            </div>
            <button
              onClick={() => setSelectedLesson(null)}
              className="inline-flex items-center gap-1.5 text-sm text-gray-600 hover:text-gray-900 font-medium"
            >
              <ArrowLeft className="w-4 h-4" /> Back to Lessons
            </button>
          </div>

          {!selectedLesson.learning_objectives || selectedLesson.learning_objectives.length === 0 ? (
            <div className="p-6 bg-gray-50 rounded-xl border border-gray-200 text-center text-gray-500">
              No learning objectives defined for this lesson.
            </div>
          ) : (
            <div className="grid gap-4">
              {selectedLesson.learning_objectives.map((obj) => (
                <div
                  key={obj.id}
                  className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm space-y-4"
                >
                  <div className="flex flex-wrap items-start justify-between gap-3">
                    <div>
                      <div className="flex items-center gap-2">
                        <Award className="w-5 h-5 text-amber-500" />
                        <h4 className="text-lg font-bold text-gray-900">{getText(obj.title)}</h4>
                      </div>
                      {getSubText(obj.title) && (
                        <p className="text-sm text-gray-500 font-arabic mt-1" dir="rtl">
                          {getSubText(obj.title)}
                        </p>
                      )}
                    </div>

                    <div className="flex items-center gap-2">
                      <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-amber-50 text-amber-800 border border-amber-200">
                        Difficulty Level {obj.difficulty_level}/5
                      </span>
                      {obj.is_active && (
                        <span className="inline-flex items-center gap-1 text-xs font-medium text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
                          <CheckCircle2 className="w-3 h-3" /> Active
                        </span>
                      )}
                    </div>
                  </div>

                  {obj.description && (
                    <p className="text-sm text-gray-600">{getText(obj.description)}</p>
                  )}

                  {/* Assessment Criteria Grid */}
                  {obj.assessment_criteria && (
                    <div className="bg-gray-50 p-4 rounded-xl border border-gray-100">
                      <h5 className="text-xs font-bold uppercase tracking-wider text-gray-500 mb-2">
                        Assessment Criteria
                      </h5>
                      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-sm">
                        {obj.assessment_criteria.minimum_accuracy !== undefined && (
                          <div>
                            <span className="text-xs text-gray-500 block">Min. Accuracy</span>
                            <span className="font-semibold text-gray-800">
                              {(obj.assessment_criteria.minimum_accuracy * 100).toFixed(0)}%
                            </span>
                          </div>
                        )}
                        {obj.assessment_criteria.maximum_assistance_level !== undefined && (
                          <div>
                            <span className="text-xs text-gray-500 block">Max. Assistance</span>
                            <span className="font-semibold text-gray-800">
                              Level {obj.assessment_criteria.maximum_assistance_level}
                            </span>
                          </div>
                        )}
                        {obj.assessment_criteria.required_completion !== undefined && (
                          <div>
                            <span className="text-xs text-gray-500 block">Required Completion</span>
                            <span className="font-semibold text-gray-800">
                              {obj.assessment_criteria.required_completion ? "Yes" : "Optional"}
                            </span>
                          </div>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Prerequisites */}
                  {obj.prerequisites && obj.prerequisites.length > 0 && (
                    <div className="pt-2 border-t border-gray-100">
                      <h5 className="text-xs font-bold uppercase tracking-wider text-gray-500 mb-1.5">
                        Prerequisites
                      </h5>
                      <div className="flex flex-wrap gap-2">
                        {obj.prerequisites.map((prereq) => (
                          <span
                            key={prereq.id}
                            className="text-xs font-medium px-2.5 py-1 rounded-md bg-gray-100 text-gray-700 border border-gray-200"
                          >
                            {getText(prereq.title)}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
