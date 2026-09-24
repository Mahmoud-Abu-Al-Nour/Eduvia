import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  Sparkles,
  Loader2,
  Play,
  RotateCcw,
  Eye,
  CheckCircle2,
  AlertTriangle,
  BookOpen,
  Shield,
  Edit3,
  Save,
  X,
  History,
} from "lucide-react";
import { activitiesApi } from "@/services/api";
import type {
  Activity,
  EffectiveGenerationPrompt,
  LessonPlan,
  ActivityGenerationSummary,
} from "@/types";

export interface TeacherActivityGeneratorProps {
  objectiveId?: string;
  objectiveTitle?: string;
  subjectTitle?: string;
  unitTitle?: string;
  lessonTitle?: string;
  defaultDifficulty?: number;
  onLaunch?: (activityId: string) => void;
  onClose?: () => void;
  standalone?: boolean;
}

const ACTIVITY_TYPES = [
  { value: "auto", label: "Auto (Curriculum Recommended)" },
  { value: "multiple_choice", label: "Multiple Choice" },
  { value: "matching", label: "Matching Pairs" },
  { value: "ordering", label: "Ordering / Sequencing" },
  { value: "visual_identification", label: "Visual Identification" },
  { value: "drag_drop", label: "Drag & Drop" },
];

const VISUAL_STYLES = [
  { value: "calm", label: "Calm & Focused (Pastels, Minimal)", desc: "Reduces cognitive stimulation" },
  { value: "simple", label: "Simple High Contrast", desc: "Clear shapes and high legibility" },
  { value: "playful", label: "Playful Illustrated", desc: "Engaging motifs for younger learners" },
  { value: "concrete", label: "Concrete Everyday", desc: "Real-world objects and familiar items" },
];

const SCAFFOLDING_LEVELS = [
  { value: 1, label: "Level 1: Low (Autonomous)", desc: "Direct challenge, minimal baseline hints" },
  { value: 2, label: "Level 2: Medium (Guided)", desc: "Progressive progressive hints and cues" },
  { value: 3, label: "Level 3: High (Step-by-Step)", desc: "Rich audio/visual guidance & full scaffolding" },
];

const INTERACTION_STYLES = [
  { value: "direct", label: "Direct Click / Touch", desc: "Single tap or point selection" },
  { value: "multistep", label: "Multi-Step Flow", desc: "Structured sequential interactions" },
  { value: "calm_pace", label: "Relaxed Focus Pace", desc: "Un-timed, distraction-free progression" },
];

const PRESET_INSTRUCTIONS = [
  "Use everyday objects (apples, blocks, stars).",
  "Avoid ambiguous distractors.",
  "Keep instructions short and calm.",
  "Avoid numbers above 10.",
  "Provide gentle error recovery guidance.",
  "Focus on high-contrast visual cues.",
];

export const TeacherActivityGenerator: React.FC<TeacherActivityGeneratorProps> = ({
  objectiveId: propObjectiveId,
  objectiveTitle,
  subjectTitle,
  unitTitle,
  lessonTitle,
  defaultDifficulty = 2,
  onLaunch,
  onClose,
  standalone = false,
}) => {
  const navigate = useNavigate();

  // Mode: Activity vs Lesson Plan
  const [mode, setMode] = useState<"activity" | "lesson">("activity");

  // Brief configuration
  const [objectiveId, setObjectiveId] = useState<string>(propObjectiveId || "math-num-01");
  const [activityType, setActivityType] = useState<string>("auto");
  const [difficulty, setDifficulty] = useState<number>(defaultDifficulty);
  const [itemCount, setItemCount] = useState<number>(5);
  const [language, setLanguage] = useState<string>("en");
  const [visualStyle, setVisualStyle] = useState<string>("calm");
  const [scaffolding, setScaffolding] = useState<number>(2);
  const [interactionStyle, setInteractionStyle] = useState<string>("direct");
  const [teacherInstructions, setTeacherInstructions] = useState<string>(
    "Use everyday objects. Keep instructions calm and concise. Avoid ambiguous distractors."
  );
  const [seed, setSeed] = useState<number>(1);

  // Prompt preview state
  const [previewOpen, setPreviewOpen] = useState(false);
  const [previewLoading, setPreviewLoading] = useState(false);
  const [effectivePrompt, setEffectivePrompt] = useState<EffectiveGenerationPrompt | null>(null);
  const [previewActiveTab, setPreviewActiveTab] = useState<string>("full");

  // Execution state
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Result state
  const [generatedActivity, setGeneratedActivity] = useState<Activity | null>(null);
  const [generatedLesson, setGeneratedLesson] = useState<LessonPlan | null>(null);
  const [provenance, setProvenance] = useState<{
    source: string;
    fallbackUsed: boolean;
    groundingSources: string[];
  } | null>(null);

  // Editing state for activity details
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState("");
  const [editInstruction, setEditInstruction] = useState("");
  const [savingEdit, setSavingEdit] = useState(false);

  // Session history state
  const [showHistory, setShowHistory] = useState(false);
  const [historyList, setHistoryList] = useState<ActivityGenerationSummary[]>([]);
  const [loadingHistory, setLoadingHistory] = useState(false);

  useEffect(() => {
    if (propObjectiveId) {
      setObjectiveId(propObjectiveId);
    }
  }, [propObjectiveId]);

  const loadHistory = async () => {
    setLoadingHistory(true);
    try {
      const data = await activitiesApi.getHistory();
      setHistoryList(data);
    } catch (e) {
      console.warn("Could not load history", e);
    } finally {
      setLoadingHistory(false);
    }
  };

  const handlePreviewPrompt = async () => {
    setPreviewLoading(true);
    setError(null);
    try {
      const promptData = await activitiesApi.previewPrompt({
        objective_id: objectiveId,
        activity_type: activityType,
        difficulty_level: difficulty,
        item_count: itemCount,
        language,
        visual_style: visualStyle,
        scaffolding_level: scaffolding,
        interaction_style: interactionStyle,
        teacher_instructions: teacherInstructions,
        mode,
        seed,
      });
      setEffectivePrompt(promptData);
      setPreviewOpen(true);
    } catch (e: any) {
      setError(e?.message || "Failed to compile prompt preview");
    } finally {
      setPreviewLoading(false);
    }
  };

  const handleGenerate = async (useNewSeed: boolean = false) => {
    setGenerating(true);
    setError(null);
    const activeSeed = useNewSeed ? seed + 1 : seed;
    if (useNewSeed) {
      setSeed(activeSeed);
    }

    try {
      if (mode === "lesson") {
        const res = await activitiesApi.generateLesson({
          objective_id: objectiveId,
          activity_type: activityType === "auto" ? "multiple_choice" : activityType,
          difficulty_level: difficulty,
          item_count: itemCount,
          language,
          visual_style: visualStyle,
          scaffolding_level: scaffolding,
          interaction_style: interactionStyle,
          teacher_instructions: teacherInstructions,
          mode: "lesson",
          seed: activeSeed,
        });

        setGeneratedLesson(res.lesson_plan);
        setGeneratedActivity(res.lesson_plan.activity || null);
        setProvenance({
          source: res.generation_source,
          fallbackUsed: res.fallback_used,
          groundingSources: (res.grounding_sources || []).map((g) => g.title || g.source || "Curriculum Content"),
        });
      } else {
        const res = await activitiesApi.generate({
          objective_id: objectiveId,
          activity_type: activityType,
          difficulty_level: difficulty,
          item_count: itemCount,
          language,
          visual_style: visualStyle,
          scaffolding_level: scaffolding,
          interaction_style: interactionStyle,
          teacher_instructions: teacherInstructions,
          mode: "activity",
          seed: activeSeed,
        });

        setGeneratedActivity(res.activity);
        setGeneratedLesson(null);
        setEditTitle(res.activity.title || "");
        setEditInstruction(res.activity.instructions || "");
        setProvenance({
          source: res.generation_source,
          fallbackUsed: res.fallback_used,
          groundingSources: (res.grounding_sources || []).map((g) => g.title || g.source || "Curriculum Content"),
        });
      }
    } catch (e: any) {
      setError(e?.message || "Generation request failed.");
    } finally {
      setGenerating(false);
    }
  };

  const handleSaveEdit = async () => {
    if (!generatedActivity) return;
    setSavingEdit(true);
    try {
      const updated = await activitiesApi.update(generatedActivity.id, {
        title: editTitle || undefined,
        instructions: editInstruction || undefined,
        teacher_notes: teacherInstructions,
      });
      setGeneratedActivity(updated);
      setIsEditing(false);
    } catch (e: any) {
      setError(e?.message || "Failed to update activity");
    } finally {
      setSavingEdit(false);
    }
  };

  const handleLaunchActivity = (actId: string) => {
    if (onLaunch) {
      onLaunch(actId);
    } else {
      navigate(`/learn/${actId}`);
    }
  };

  return (
    <div className={`bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden ${standalone ? "p-6" : "p-5"}`}>
      {/* ── Top Bar / Header ── */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-slate-100">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-600 to-indigo-700 flex items-center justify-center text-white shadow-sm">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-lg font-bold text-slate-900">
                {mode === "activity" ? "Teacher Activity Brief" : "Teacher Mini-Lesson Brief"}
              </h3>
              <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-violet-50 text-violet-700 border border-violet-200">
                AI + RAG Grounded
              </span>
            </div>
            <p className="text-xs text-slate-500">
              {objectiveTitle ? (
                <>Target: <span className="font-semibold text-slate-700">{objectiveTitle}</span></>
              ) : (
                "Configure pedagogical controls, preview compiled prompt, and generate with Gemini."
              )}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {/* Mode Switcher */}
          <div className="inline-flex p-1 rounded-xl bg-slate-100 border border-slate-200 text-xs font-semibold">
            <button
              onClick={() => { setMode("activity"); setGeneratedLesson(null); }}
              className={`px-3 py-1.5 rounded-lg transition-all ${
                mode === "activity"
                  ? "bg-white text-violet-800 shadow-xs"
                  : "text-slate-600 hover:text-slate-900"
              }`}
            >
              Activity & Practice
            </button>
            <button
              onClick={() => { setMode("lesson"); setGeneratedActivity(null); }}
              className={`px-3 py-1.5 rounded-lg transition-all ${
                mode === "lesson"
                  ? "bg-white text-violet-800 shadow-xs"
                  : "text-slate-600 hover:text-slate-900"
              }`}
            >
              Mini-Lesson Plan
            </button>
          </div>

          <button
            onClick={() => { setShowHistory(!showHistory); if (!showHistory) void loadHistory(); }}
            className="p-2 rounded-xl text-slate-600 hover:text-slate-900 hover:bg-slate-100 border border-slate-200 text-xs font-medium inline-flex items-center gap-1.5"
            title="Session Generation History"
          >
            <History className="w-4 h-4 text-slate-500" />
            <span className="hidden sm:inline">History</span>
          </button>

          {onClose && (
            <button
              onClick={onClose}
              className="p-2 rounded-xl text-slate-400 hover:text-slate-700 hover:bg-slate-100"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>

      {/* History Drawer */}
      {showHistory && (
        <div className="my-4 p-4 rounded-xl bg-slate-50 border border-slate-200">
          <div className="flex items-center justify-between mb-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-1.5">
              <History className="w-3.5 h-3.5" /> Recent Generations In This Session
            </h4>
            <button onClick={() => setShowHistory(false)} className="text-xs text-slate-400 hover:text-slate-600">Close</button>
          </div>
          {loadingHistory ? (
            <div className="text-xs text-slate-500 py-3 text-center flex items-center justify-center gap-2">
              <Loader2 className="w-3.5 h-3.5 animate-spin" /> Loading generation history...
            </div>
          ) : historyList.length === 0 ? (
            <div className="text-xs text-slate-500 py-2 text-center">No recent activities generated yet.</div>
          ) : (
            <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
              {historyList.map((item) => (
                <div key={item.id} className="flex items-center justify-between bg-white p-2.5 rounded-lg border border-slate-200 text-xs">
                  <div>
                    <span className="font-semibold text-slate-800">{item.title}</span>
                    <span className="ml-2 text-slate-400">({item.activity_type}, Diff {item.difficulty_level})</span>
                    <span className={`ml-2 px-1.5 py-0.5 rounded text-[10px] font-semibold ${
                      item.generation_source === "gemini" ? "bg-violet-50 text-violet-700" : "bg-amber-50 text-amber-700"
                    }`}>
                      {item.generation_source}
                    </span>
                  </div>
                  <button
                    onClick={() => handleLaunchActivity(item.id)}
                    className="inline-flex items-center gap-1 px-2.5 py-1 bg-brand-800 text-white rounded text-xs font-medium hover:bg-brand-900"
                  >
                    <Play className="w-3 h-3" /> Launch
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* ── Form Controls Grid ── */}
      <div className="mt-5 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {/* Objective & Hierarchy info */}
        <div className="space-y-1.5">
          <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
            Curriculum Objective
          </label>
          <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs space-y-1">
            <div className="font-semibold text-slate-900 truncate">
              {objectiveTitle || "Count objects from 0–10"}
            </div>
            {(subjectTitle || unitTitle) && (
              <div className="text-slate-500 text-[11px] truncate">
                {subjectTitle} {unitTitle ? `› ${unitTitle}` : ""} {lessonTitle ? `› ${lessonTitle}` : ""}
              </div>
            )}
            <div className="flex items-center gap-1.5 pt-1 text-[11px] text-emerald-700 font-medium">
              <CheckCircle2 className="w-3.5 h-3.5" /> Content Bank Grounded
            </div>
          </div>
        </div>

        {/* Activity Type Selector */}
        {mode === "activity" && (
          <div className="space-y-1.5">
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
              Activity Type
            </label>
            <select
              value={activityType}
              onChange={(e) => setActivityType(e.target.value)}
              className="w-full text-xs font-medium px-3 py-2.5 rounded-xl border border-slate-200 bg-white text-slate-800 focus:ring-2 focus:ring-violet-500 focus:outline-none"
            >
              {ACTIVITY_TYPES.map((t) => (
                <option key={t.value} value={t.value}>{t.label}</option>
              ))}
            </select>
            <p className="text-[11px] text-slate-400">
              {activityType === "auto" ? "Curriculum will select optimal modality" : `Strict canonical schema: ${activityType}`}
            </p>
          </div>
        )}

        {/* Difficulty Level */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between">
            <label className="text-xs font-bold text-slate-700 uppercase tracking-wider">
              Difficulty Tier
            </label>
            <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-violet-100 text-violet-800">
              Level {difficulty} of 5
            </span>
          </div>
          <input
            type="range"
            min={1}
            max={5}
            value={difficulty}
            onChange={(e) => setDifficulty(Number(e.target.value))}
            className="w-full h-2 rounded-lg bg-slate-200 accent-violet-600 cursor-pointer"
          />
          <div className="flex justify-between text-[10px] text-slate-400">
            <span>1 (Foundational)</span>
            <span>3 (Standard)</span>
            <span>5 (Mastery)</span>
          </div>
        </div>

        {/* Question Count / Item Quantity */}
        <div className="space-y-1.5">
          <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
            {mode === "activity" ? "Item / Question Count" : "Target Items in Practice"}
          </label>
          <div className="grid grid-cols-4 gap-2">
            {[3, 5, 8, 10].map((count) => (
              <button
                key={count}
                type="button"
                onClick={() => setItemCount(count)}
                className={`py-2 text-xs font-semibold rounded-xl border transition-all ${
                  itemCount === count
                    ? "bg-violet-600 text-white border-violet-600 shadow-xs"
                    : "bg-white text-slate-700 border-slate-200 hover:border-violet-300"
                }`}
              >
                {count} items
              </button>
            ))}
          </div>
        </div>

        {/* Visual Style */}
        <div className="space-y-1.5">
          <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
            Visual Style & Theme
          </label>
          <select
            value={visualStyle}
            onChange={(e) => setVisualStyle(e.target.value)}
            className="w-full text-xs font-medium px-3 py-2.5 rounded-xl border border-slate-200 bg-white text-slate-800 focus:ring-2 focus:ring-violet-500 focus:outline-none"
          >
            {VISUAL_STYLES.map((vs) => (
              <option key={vs.value} value={vs.value}>{vs.label}</option>
            ))}
          </select>
          <p className="text-[11px] text-slate-400">
            {VISUAL_STYLES.find((vs) => vs.value === visualStyle)?.desc}
          </p>
        </div>

        {/* Scaffolding Level */}
        <div className="space-y-1.5">
          <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
            Scaffolding & Assistance
          </label>
          <select
            value={scaffolding}
            onChange={(e) => setScaffolding(Number(e.target.value))}
            className="w-full text-xs font-medium px-3 py-2.5 rounded-xl border border-slate-200 bg-white text-slate-800 focus:ring-2 focus:ring-violet-500 focus:outline-none"
          >
            {SCAFFOLDING_LEVELS.map((sc) => (
              <option key={sc.value} value={sc.value}>{sc.label}</option>
            ))}
          </select>
          <p className="text-[11px] text-slate-400">
            {SCAFFOLDING_LEVELS.find((sc) => sc.value === scaffolding)?.desc}
          </p>
        </div>

        {/* Language */}
        <div className="space-y-1.5">
          <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
            Language
          </label>
          <div className="grid grid-cols-2 gap-2">
            {[
              { code: "en", label: "English" },
              { code: "ar", label: "Arabic (العربية)" },
            ].map((lang) => (
              <button
                key={lang.code}
                type="button"
                onClick={() => setLanguage(lang.code)}
                className={`py-2 text-xs font-semibold rounded-xl border transition-all ${
                  language === lang.code
                    ? "bg-violet-600 text-white border-violet-600 shadow-xs"
                    : "bg-white text-slate-700 border-slate-200 hover:border-violet-300"
                }`}
              >
                {lang.label}
              </button>
            ))}
          </div>
        </div>

        {/* Interaction Style */}
        <div className="space-y-1.5">
          <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
            Interaction Style
          </label>
          <select
            value={interactionStyle}
            onChange={(e) => setInteractionStyle(e.target.value)}
            className="w-full text-xs font-medium px-3 py-2.5 rounded-xl border border-slate-200 bg-white text-slate-800 focus:ring-2 focus:ring-violet-500 focus:outline-none"
          >
            {INTERACTION_STYLES.map((is) => (
              <option key={is.value} value={is.value}>{is.label}</option>
            ))}
          </select>
          <p className="text-[11px] text-slate-400">
            {INTERACTION_STYLES.find((is) => is.value === interactionStyle)?.desc}
          </p>
        </div>
      </div>

      {/* ── Teacher Instructions (Editable Textarea) ── */}
      <div className="mt-5 space-y-2">
        <div className="flex items-center justify-between">
          <label className="text-xs font-bold text-slate-700 uppercase tracking-wider flex items-center gap-1.5">
            <Edit3 className="w-3.5 h-3.5 text-violet-600" />
            Teacher Instructions & Prompt Notes (Teacher-Controlled)
          </label>
          <span className="text-[11px] text-slate-400">
            Injected directly into Gemini prompt
          </span>
        </div>

        <textarea
          rows={3}
          value={teacherInstructions}
          onChange={(e) => setTeacherInstructions(e.target.value)}
          placeholder="e.g. Use everyday objects. Avoid ambiguous distractors. Keep instructions short. Use calm visuals. Avoid numbers above 10."
          className="w-full text-xs font-medium p-3 rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-violet-500 focus:outline-none transition-all"
        />

        {/* Quick Suggestion Chips */}
        <div className="flex flex-wrap gap-1.5 pt-1">
          <span className="text-[10px] text-slate-400 uppercase tracking-wider py-1 mr-1">Presets:</span>
          {PRESET_INSTRUCTIONS.map((preset, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => {
                if (!teacherInstructions.includes(preset)) {
                  setTeacherInstructions(teacherInstructions ? `${teacherInstructions} ${preset}` : preset);
                }
              }}
              className="text-[11px] px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-violet-50 hover:text-violet-700 text-slate-600 border border-slate-200 transition-colors"
            >
              + {preset}
            </button>
          ))}
        </div>
      </div>

      {/* ── Action Buttons: Preview & Generate ── */}
      <div className="mt-6 pt-5 border-t border-slate-100 flex flex-wrap items-center justify-between gap-3">
        <button
          type="button"
          onClick={handlePreviewPrompt}
          disabled={previewLoading || generating}
          className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl border border-slate-300 hover:border-violet-400 bg-white text-slate-700 hover:text-violet-800 text-xs font-bold transition-all disabled:opacity-50"
        >
          {previewLoading ? (
            <><Loader2 className="w-4 h-4 animate-spin text-violet-600" /> Compiling Prompt...</>
          ) : (
            <><Eye className="w-4 h-4 text-violet-600" /> Preview Effective Prompt</>
          )}
        </button>

        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={() => handleGenerate(false)}
            disabled={generating || previewLoading}
            className="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-700 hover:to-indigo-700 text-white text-xs font-bold shadow-sm transition-all disabled:opacity-50 disabled:cursor-wait"
          >
            {generating ? (
              <><Loader2 className="w-4 h-4 animate-spin" /> Compiling & Calling Gemini...</>
            ) : (
              <><Sparkles className="w-4 h-4" /> Generate with Gemini</>
            )}
          </button>
        </div>
      </div>

      {/* Error Banner */}
      {error && (
        <div className="mt-4 p-3.5 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-start gap-2.5">
          <AlertTriangle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
          <div className="flex-1">
            <span className="font-bold">Generation Notice: </span>
            {error}
          </div>
          <button onClick={() => setError(null)} className="text-rose-500 hover:text-rose-700"><X className="w-3.5 h-3.5" /></button>
        </div>
      )}

      {/* ── Generated Result: Activity View ── */}
      {generatedActivity && (
        <div className="mt-6 p-5 rounded-2xl bg-gradient-to-br from-slate-50 to-violet-50/40 border border-violet-200/80 space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center gap-2.5">
              <CheckCircle2 className="w-5 h-5 text-emerald-600" />
              <div>
                <h4 className="text-sm font-bold text-slate-900">
                  {generatedActivity.title || "Generated Activity"}
                </h4>
                <div className="flex items-center gap-2 mt-0.5">
                  <span className={`text-[11px] font-bold px-2 py-0.5 rounded-full border ${
                    provenance?.fallbackUsed
                      ? "bg-amber-50 text-amber-800 border-amber-200"
                      : "bg-emerald-50 text-emerald-800 border-emerald-200"
                  }`}>
                    {provenance?.fallbackUsed ? "Safe Local Fallback" : "AI Generated"}
                  </span>
                  <span className="text-[11px] text-slate-500">
                    Source: <strong className="text-slate-700">{provenance?.source}</strong>
                  </span>
                  {provenance?.groundingSources && provenance.groundingSources.length > 0 && (
                    <span className="text-[11px] text-slate-500">
                      • {provenance.groundingSources.length} Grounding Sources
                    </span>
                  )}
                </div>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => handleGenerate(true)}
                disabled={generating}
                className="inline-flex items-center gap-1.5 px-3 py-2 rounded-xl bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 text-xs font-semibold transition-all disabled:opacity-50"
                title="Regenerate with variation using alternate content items"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span>Regenerate Variation</span>
              </button>

              <button
                type="button"
                onClick={() => setIsEditing(!isEditing)}
                className="inline-flex items-center gap-1.5 px-3 py-2 rounded-xl bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 text-xs font-semibold transition-all"
              >
                <Edit3 className="w-3.5 h-3.5" />
                <span>{isEditing ? "Close Editor" : "Edit Details"}</span>
              </button>

              <button
                type="button"
                onClick={() => handleLaunchActivity(generatedActivity.id)}
                className="inline-flex items-center gap-1.5 px-5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold shadow-xs transition-all"
              >
                <Play className="w-4 h-4" />
                <span>Launch Activity</span>
              </button>
            </div>
          </div>

          {/* Activity Metadata details */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs bg-white p-3 rounded-xl border border-slate-200">
            <div>
              <span className="text-slate-400 block text-[10px] uppercase">Modality</span>
              <span className="font-semibold text-slate-800">{generatedActivity.activity_type}</span>
            </div>
            <div>
              <span className="text-slate-400 block text-[10px] uppercase">Difficulty Tier</span>
              <span className="font-semibold text-slate-800">Level {generatedActivity.difficulty_level}/5</span>
            </div>
            <div>
              <span className="text-slate-400 block text-[10px] uppercase">Instructions</span>
              <span className="font-semibold text-slate-800 truncate block">
                {generatedActivity.instructions || "Follow instructions"}
              </span>
            </div>
            <div>
              <span className="text-slate-400 block text-[10px] uppercase">Items Grounded</span>
              <span className="font-semibold text-slate-800">
                {(generatedActivity.content as any)?.items?.length ||
                 (generatedActivity.content as any)?.options?.length ||
                 (generatedActivity.content as any)?.pairs?.length ||
                 itemCount} Items
              </span>
            </div>
          </div>

          {/* Teacher Inline Editor */}
          {isEditing && (
            <div className="bg-white p-4 rounded-xl border border-violet-200 space-y-3">
              <h5 className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
                <Edit3 className="w-3.5 h-3.5 text-violet-600" />
                Safe Teacher Content Modifications
              </h5>
              <div className="space-y-2">
                <div>
                  <label className="block text-[11px] font-semibold text-slate-600 mb-1">Title</label>
                  <input
                    type="text"
                    value={editTitle}
                    onChange={(e) => setEditTitle(e.target.value)}
                    className="w-full text-xs p-2 rounded-lg border border-slate-200 focus:ring-1 focus:ring-violet-500"
                  />
                </div>
                <div>
                  <label className="block text-[11px] font-semibold text-slate-600 mb-1">Learner Instruction</label>
                  <input
                    type="text"
                    value={editInstruction}
                    onChange={(e) => setEditInstruction(e.target.value)}
                    className="w-full text-xs p-2 rounded-lg border border-slate-200 focus:ring-1 focus:ring-violet-500"
                  />
                </div>
              </div>
              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setIsEditing(false)}
                  className="px-3 py-1.5 text-xs text-slate-500 hover:text-slate-700"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  onClick={handleSaveEdit}
                  disabled={savingEdit}
                  className="inline-flex items-center gap-1.5 px-4 py-1.5 bg-violet-600 text-white rounded-lg text-xs font-semibold hover:bg-violet-700 transition-colors disabled:opacity-50"
                >
                  {savingEdit ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Save className="w-3.5 h-3.5" />}
                  Save Validated Edits
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* ── Generated Result: Lesson Plan View ── */}
      {generatedLesson && (
        <div className="mt-6 p-5 rounded-2xl bg-gradient-to-br from-slate-50 to-indigo-50/50 border border-indigo-200 space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center gap-2.5">
              <BookOpen className="w-5 h-5 text-indigo-600" />
              <div>
                <h4 className="text-base font-bold text-slate-900">{generatedLesson.title}</h4>
                <div className="flex items-center gap-2 mt-0.5">
                  <span className={`text-[11px] font-bold px-2 py-0.5 rounded-full border ${
                    provenance?.fallbackUsed
                      ? "bg-amber-50 text-amber-800 border-amber-200"
                      : "bg-emerald-50 text-emerald-800 border-emerald-200"
                  }`}>
                    {provenance?.fallbackUsed ? "Safe Local Fallback" : "AI Generated"}
                  </span>
                  <span className="text-[11px] text-slate-500">
                    Est. Duration: <strong>{generatedLesson.duration_minutes || 10} minutes</strong>
                  </span>
                </div>
              </div>
            </div>

            {generatedActivity && (
              <button
                type="button"
                onClick={() => handleLaunchActivity(generatedActivity.id)}
                className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold shadow-xs transition-all"
              >
                <Play className="w-4 h-4" />
                <span>Launch Practice Activity</span>
              </button>
            )}
          </div>

          {/* Structured Lesson Sections */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
            <div className="bg-white p-3.5 rounded-xl border border-slate-200 space-y-1">
              <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-700 block">
                1. Warm-Up & Introduction
              </span>
              <p className="text-slate-700">{generatedLesson.introduction}</p>
            </div>
            <div className="bg-white p-3.5 rounded-xl border border-slate-200 space-y-1">
              <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-700 block">
                2. Teacher Demonstration ("I Do")
              </span>
              <p className="text-slate-700">{generatedLesson.demonstration}</p>
            </div>
            <div className="bg-white p-3.5 rounded-xl border border-slate-200 space-y-1">
              <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-700 block">
                3. Guided Practice ("We Do")
              </span>
              <p className="text-slate-700">{generatedLesson.guided_practice}</p>
            </div>
            <div className="bg-white p-3.5 rounded-xl border border-slate-200 space-y-1">
              <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-700 block">
                4. Independent Practice ("You Do")
              </span>
              <p className="text-slate-700">{generatedLesson.independent_practice}</p>
            </div>
          </div>

          <div className="bg-white p-3.5 rounded-xl border border-slate-200 text-xs space-y-2">
            <div className="flex flex-wrap gap-4 text-slate-600">
              <div>
                <strong className="text-slate-900 block text-[10px] uppercase">Scaffolding:</strong>
                {generatedLesson.scaffolding}
              </div>
              <div>
                <strong className="text-slate-900 block text-[10px] uppercase">Recap:</strong>
                {generatedLesson.recap}
              </div>
            </div>
            {generatedLesson.teacher_notes && (
              <div className="pt-2 border-t border-slate-100 text-slate-500 italic">
                Note: {generatedLesson.teacher_notes}
              </div>
            )}
          </div>
        </div>
      )}

      {/* ── Prompt Preview Modal ── */}
      {previewOpen && effectivePrompt && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-xl max-w-4xl w-full max-h-[90vh] flex flex-col overflow-hidden border border-slate-200">
            {/* Modal Header */}
            <div className="px-6 py-4 border-b border-slate-200 flex items-center justify-between bg-slate-50">
              <div className="flex items-center gap-2.5">
                <Shield className="w-5 h-5 text-violet-600" />
                <div>
                  <h3 className="text-base font-bold text-slate-900">
                    Effective Prompt Compiler Preview
                  </h3>
                  <p className="text-xs text-slate-500">
                    Inspecting compiled 10-section prompt supplied to Gemini. Zero secrets exposed.
                  </p>
                </div>
              </div>
              <button
                onClick={() => setPreviewOpen(false)}
                className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-200"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Ownership Boundary Notice */}
            <div className="px-6 py-2.5 bg-violet-50/70 border-b border-violet-100 text-xs text-violet-900 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="px-2 py-0.5 rounded bg-violet-200 font-bold text-[10px] uppercase tracking-wider text-violet-900">
                  Ownership Model
                </span>
                <span>
                  <strong>Immutable:</strong> Safety rules, curriculum objective, schema contract & evaluation authority. | <strong>Teacher-controlled:</strong> Instructions, style & item count.
                </span>
              </div>
            </div>

            {/* Tabs for Section View vs Full Raw Text */}
            <div className="px-6 pt-3 border-b border-slate-100 flex gap-2 text-xs font-semibold">
              <button
                onClick={() => setPreviewActiveTab("full")}
                className={`pb-2.5 px-2 border-b-2 transition-all ${
                  previewActiveTab === "full"
                    ? "border-violet-600 text-violet-700"
                    : "border-transparent text-slate-500 hover:text-slate-800"
                }`}
              >
                Full Compiled Prompt ({effectivePrompt.full_prompt_text.length} chars)
              </button>
              <button
                onClick={() => setPreviewActiveTab("sections")}
                className={`pb-2.5 px-2 border-b-2 transition-all ${
                  previewActiveTab === "sections"
                    ? "border-violet-600 text-violet-700"
                    : "border-transparent text-slate-500 hover:text-slate-800"
                }`}
              >
                Structured Sections ({Object.keys(effectivePrompt.sections).length})
              </button>
              <button
                onClick={() => setPreviewActiveTab("grounding")}
                className={`pb-2.5 px-2 border-b-2 transition-all ${
                  previewActiveTab === "grounding"
                    ? "border-violet-600 text-violet-700"
                    : "border-transparent text-slate-500 hover:text-slate-800"
                }`}
              >
                Authoritative Grounding ({effectivePrompt.grounding_sources?.length || 0} Sources)
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-6 overflow-y-auto flex-1 font-mono text-xs text-slate-800 bg-slate-50/40">
              {previewActiveTab === "full" && (
                <pre className="whitespace-pre-wrap font-sans text-xs bg-white p-4 rounded-xl border border-slate-200 leading-relaxed">
                  {effectivePrompt.full_prompt_text}
                </pre>
              )}

              {previewActiveTab === "sections" && (
                <div className="space-y-4 font-sans">
                  {Object.entries(effectivePrompt.sections).map(([sectionKey, content]) => (
                    <div key={sectionKey} className="bg-white p-4 rounded-xl border border-slate-200">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-bold text-xs uppercase tracking-wider text-slate-900">
                          {sectionKey}
                        </span>
                        {sectionKey.includes("TEACHER") ? (
                          <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-50 text-emerald-800 border border-emerald-200">
                            Teacher-Controlled
                          </span>
                        ) : (
                          <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-slate-100 text-slate-600">
                            System-Enforced Immutable
                          </span>
                        )}
                      </div>
                      <pre className="whitespace-pre-wrap text-xs text-slate-700 bg-slate-50 p-2.5 rounded-lg border border-slate-100">
                        {content}
                      </pre>
                    </div>
                  ))}
                </div>
              )}

              {previewActiveTab === "grounding" && (
                <div className="space-y-3 font-sans">
                  <div className="bg-white p-4 rounded-xl border border-slate-200">
                    <h5 className="font-bold text-xs uppercase tracking-wider text-slate-800 mb-2">
                      Content Bank Authority
                    </h5>
                    <p className="text-xs text-slate-600 mb-3">
                      Gemini is strictly grounded against authoritative curriculum facts. It is not permitted to hallucinate correct answers.
                    </p>
                    <div className="space-y-1.5 text-xs text-slate-700">
                      <div>Target Objective: <strong>{effectivePrompt.objective_title}</strong></div>
                      <div>Delivery Format: <strong>{effectivePrompt.activity_type}</strong></div>
                      <div>Difficulty Tier: <strong>Level {effectivePrompt.difficulty_level}/5</strong></div>
                    </div>
                  </div>

                  <div className="bg-white p-4 rounded-xl border border-slate-200">
                    <h5 className="font-bold text-xs uppercase tracking-wider text-slate-800 mb-2">
                      Retrieved Pedagogical Sources
                    </h5>
                    {effectivePrompt.grounding_sources?.map((src, i) => (
                      <div key={i} className="text-xs text-slate-600 flex items-center gap-2 py-1">
                        <span className="w-1.5 h-1.5 rounded-full bg-violet-600" />
                        <span>{src.title || src.source}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Modal Footer */}
            <div className="px-6 py-3.5 border-t border-slate-200 flex items-center justify-between bg-slate-50">
              <span className="text-xs text-slate-500">
                Safe preview: No headers, API keys, or backend secrets are ever rendered.
              </span>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setPreviewOpen(false)}
                  className="px-4 py-2 text-xs font-semibold text-slate-600 hover:text-slate-800"
                >
                  Close
                </button>
                <button
                  onClick={() => { setPreviewOpen(false); void handleGenerate(false); }}
                  className="inline-flex items-center gap-2 px-5 py-2 bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-700 hover:to-indigo-700 text-white rounded-xl text-xs font-bold transition-all shadow-xs"
                >
                  <Sparkles className="w-3.5 h-3.5" />
                  Proceed to Generate with Gemini
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
