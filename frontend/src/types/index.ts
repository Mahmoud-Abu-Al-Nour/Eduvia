/**
 * Eduvia TypeScript Type Definitions
 *
 * Shared types used across the frontend application.
 * Mirror the backend Pydantic models and API response schemas.
 *
 * Phase 0: Core type structure
 * Later phases will expand these types as features are implemented.
 */

// ── API Types ──────────────────────────────────────────────────────────────

export interface ApiResponse<T> {
  data?: T
  error?: string
  message?: string
}

export interface HealthCheckResponse {
  status: 'ok' | 'degraded' | 'error'
  service: string
  version: string
  uptime_seconds?: number
  dependencies?: {
    database: DependencyStatus
    qdrant: DependencyStatus
    ai_provider: AiProviderStatus
  }
}

export interface DependencyStatus {
  status: 'ok' | 'unreachable'
  healthy: boolean
}

export interface AiProviderStatus {
  provider: string
  configured: boolean
  healthy: boolean
}

// ── User & Auth Types ──────────────────────────────────────────────────────

export type UserRole = 'admin' | 'teacher' | 'learner' | 'researcher'

export interface PlatformStats {
  total_users: number
  total_admins: number
  total_teachers: number
  total_learners: number
  total_curricula: number
  total_activities_completed: number
}

export interface User {
  id: string
  email: string
  full_name: string
  role: UserRole
  is_active: boolean
  created_at: string
}

export interface AuthTokens {
  access_token: string
  refresh_token: string
  token_type: 'bearer'
}

// ── Learner & Profile Types (Phase 3) ──────────────────────────────────────

export type Modality = 'visual' | 'reading' | 'writing' | 'audio' | 'interactive'

export interface LearnerObservation {
  id: string
  timestamp: string
  category: string
  summary: string
  context?: Record<string, any>
  teacher_note?: string
}

export interface LearnerProfile {
  id: string
  learner_id: string
  communication_preferences: {
    primary_mode: string
    receptive_preference: string[]
    expressive_preference: string[]
    notes?: string
  }
  current_skill_level: {
    literacy_stage: string
    numeracy_stage: string
    attention_span_minutes: number
    strengths: string[]
    focus_areas: string[]
  }
  support_requirements: {
    sensory_accommodations: string[]
    pacing: string
    guidance_level: string
    frequent_breaks: boolean
  }
  teacher_constraints: {
    max_session_duration_minutes: number
    excluded_modalities: string[]
    required_modalities: string[]
    custom_guidelines?: string
  }
  teacher_notes?: string
  teacher_overrides: {
    lock_difficulty_level?: number | null
    enforce_strategy?: string | null
    manual_adjustments_active: boolean
  }
  modality_effectiveness: Record<string, { observed_count: number; engagement_rating?: string | null }>
  strategy_effectiveness: Record<string, { observed_count: number; success_rate?: number | null }>
  activity_type_effectiveness: Record<string, { observed_count: number; accuracy_average?: number | null }>
  difficulty_tolerance: {
    comfortable_difficulty_level: number
    highest_successful_level: number
    frustration_threshold_observed: string
  }
  assistance_requirements: {
    prompt_dependence: string
    most_effective_prompt_type: string
  }
  response_behavior: {
    average_response_latency_seconds?: number | null
    consistency_pattern: string
  }
  observations: LearnerObservation[]
  created_at: string
  updated_at: string
}

export interface Learner {
  id: string
  name: string
  age_group: string
  learning_level: string
  is_active: boolean
  teacher_id?: string | null
  user_id?: string | null
  created_at: string
  updated_at: string
  profile?: LearnerProfile
}

// ── Curriculum Types ───────────────────────────────────────────────────────

export interface Curriculum {
  id: string
  title: string
  description: string
  subjects: Subject[]
}

export interface Subject {
  id: string
  title: string
  curriculum_id: string
  units: Unit[]
}

export interface Unit {
  id: string
  title: string
  subject_id: string
  lessons: Lesson[]
}

export interface Lesson {
  id: string
  title: string
  unit_id: string
  objectives: LearningObjective[]
}

export interface LearningObjective {
  id: string
  title: string
  description: string
  lesson_id: string
  difficulty_level: 1 | 2 | 3 | 4 | 5
}

// ── Activity Types (Phase 4 & 5) ──────────────────────────────────────────

export type ActivityType =
  | 'matching'
  | 'multiple_choice'
  | 'ordering'
  | 'visual_identification'
  | 'drag_drop'

export type TeachingStrategy =
  | 'step_by_step'
  | 'repetition'
  | 'scaffolding'
  | 'prompting'
  | 'simplification'
  | 'demonstration'
  | 'positive_reinforcement'
  | 'gradual_difficulty'


export interface MultipleChoiceOption {
  id: string
  text: string
  visual_cue?: string | null
  is_correct?: boolean
  distractor_rationale?: string | null
}

export interface MultipleChoiceContent {
  activity_type: 'multiple_choice'
  question: string
  options: MultipleChoiceOption[]
  correct_answer_id?: string
  explanation?: string
}

export interface MatchingItem {
  id: string
  label: string
  visual_cue?: string | null
}

export interface MatchingPair {
  left_id: string
  right_id: string
}

export interface MatchingContent {
  activity_type: 'matching'
  prompt: string
  left_items: MatchingItem[]
  right_items: MatchingItem[]
  pairs?: MatchingPair[]
}

export interface OrderingItem {
  id: string
  label: string
  visual_cue?: string | null
}

export interface OrderingContent {
  activity_type: 'ordering'
  prompt: string
  items: OrderingItem[]
  correct_sequence?: string[]
  direction?: 'ascending' | 'descending' | 'chronological' | string
}

export interface VisualElement {
  id: string
  label: string
  category?: string
  is_target?: boolean
  bounding_hint?: string | null
}

export interface VisualIdentificationContent {
  activity_type: 'visual_identification'
  prompt: string
  scene_description: string
  elements: VisualElement[]
  target_id?: string
  feedback_clue?: string
}

export interface DragItem {
  id: string
  label: string
  visual_cue?: string | null
}

export interface DropZone {
  id: string
  label: string
  capacity?: number
}

export interface DragDropContent {
  activity_type: 'drag_drop'
  prompt: string
  items: DragItem[]
  zones: DropZone[]
  correct_mapping?: Record<string, string>
}

export type ActivityContent =
  | MultipleChoiceContent
  | MatchingContent
  | OrderingContent
  | VisualIdentificationContent
  | DragDropContent

export interface ActivityQuestion {
  id: string
  question_number: number
  question_type: ActivityType
  content: ActivityContent
  content_source_key?: string | null
  hints?: string[]
  explanation?: string | null
  weight?: number
}

export interface Activity {
  id: string
  objective_id: string
  activity_type: ActivityType
  title: string
  instructions: string
  difficulty_level: number
  questions?: ActivityQuestion[]
  content?: ActivityContent
  hints: string[]
  scaffolding_level: number
  metadata?: Record<string, any>
  created_at?: string
}

export interface GroundingSource {
  chunk_id: string
  title: string
  source: string
  category: string
  score?: number
  excerpt?: string
}

export interface TeacherBriefSpec {
  objective_id: string
  subject_id?: string | null
  unit_id?: string | null
  lesson_id?: string | null
  activity_type?: ActivityType | string | null
  difficulty_level?: number | null
  item_count?: number
  language?: string
  visual_style?: string
  scaffolding_level?: number
  interaction_style?: string
  teacher_instructions?: string | null
  mode?: 'activity' | 'lesson'
  seed?: number
  learner_id?: string | null
}

export interface EffectiveGenerationPrompt {
  system_prompt: string
  user_prompt: string
  full_prompt_text: string
  sections: Record<string, string>
  teacher_editable_section: string
  immutable_sections: string[]
  grounding_sources: GroundingSource[]
  content_bank_grounded: boolean
  objective_title: string
  activity_type: string
  difficulty_level: number
}

export interface LessonPlan {
  id: string
  objective_id: string
  title: string
  objective: string
  duration_minutes: number
  introduction: string
  demonstration: string
  guided_practice: string
  independent_practice: string
  scaffolding: string
  teacher_notes: string
  recap: string
  suggested_activity_type: ActivityType
  activity?: Activity | null
  generation_source: string
  fallback_used: boolean
  grounding_sources?: GroundingSource[]
}

export interface LessonGenerateResponse {
  lesson_plan: LessonPlan
  fallback_used: boolean
  generation_source: string
  objective_id: string
  grounding_sources?: GroundingSource[]
}

export interface ActivityUpdateRequest {
  title?: string | null
  instructions?: string | null
  hints?: string[] | null
  teacher_notes?: string | null
}

export interface ActivityGenerationSummary {
  id: string
  objective_id: string
  activity_type: ActivityType
  difficulty_level: number
  title: string
  generation_source: string
  fallback_used: boolean
  created_at: string
  grounding_sources_count: number
}

export interface ActivityGenerateResponse {
  activity: Activity
  fallback_used: boolean
  generation_source: string
  learner_id?: string | null
  objective_id: string
  grounding_sources?: GroundingSource[]
}

// ── Phase 5: Submission & Interaction Types ─────────────────────────────────

export interface MultipleChoiceSubmission {
  activity_type: 'multiple_choice'
  selected_option_id: string
}

export interface MatchingSubmission {
  activity_type: 'matching'
  pairs: MatchingPair[]
}

export interface OrderingSubmission {
  activity_type: 'ordering'
  ordered_ids: string[]
}

export interface VisualIdentificationSubmission {
  activity_type: 'visual_identification'
  selected_element_id: string
}

export interface DragDropSubmission {
  activity_type: 'drag_drop'
  item_to_zone_mapping: Record<string, string>
}

export type ActivitySubmissionPayload =
  | MultipleChoiceSubmission
  | MatchingSubmission
  | OrderingSubmission
  | VisualIdentificationSubmission
  | DragDropSubmission

export interface QuestionSubmission {
  question_id: string
  submission: ActivitySubmissionPayload
}

export interface ActivitySubmissionRequest {
  activity_id: string
  objective_id: string
  activity_type: ActivityType
  submission?: ActivitySubmissionPayload
  questions?: QuestionSubmission[]
  learner_id?: string | null
  hints_used: number
  time_spent_seconds: number
  activity_content?: ActivityContent | null
}

export interface QuestionEvaluationResult {
  question_id: string
  question_number: number
  is_correct: boolean
  score: number
  feedback: string
  explanation?: string | null
  correct_answer_summary?: Record<string, any>
  evaluation_details?: Record<string, any>
}

export interface ActivityEvaluationResponse {
  activity_id: string
  is_correct: bool_or_boolean
  score: number
  mastery_achieved: boolean
  feedback: string
  explanation?: string | null
  correct_answer_summary: Record<string, any>
  hints_used: number
  assistance_level: number
  evaluation_details?: Record<string, any>
  question_results?: QuestionEvaluationResult[]
  questions_total?: number
  questions_answered?: number
  questions_correct?: number
  percentage?: number
}

type bool_or_boolean = boolean


// ── Performance & Analytics Types ──────────────────────────────────────────

export interface PerformanceEvent {
  id?: string
  learner_id: string
  activity_id: string
  question_id?: string | null
  attempt_id?: string | null
  objective_id: string
  activity_type: ActivityType
  modality: Modality
  strategy: TeachingStrategy
  correct: boolean
  score: number
  attempts: number
  response_time_ms: number
  hints_used: number
  assistance_level: number
  completed: boolean
  difficulty: number
  metadata?: Record<string, any>
  timestamp?: string
  created_at?: string
}

export interface ActivityAttempt {
  id: string
  activity_id: string
  learner_id: string
  session_id?: string | null
  started_at: string
  completed_at?: string | null
  response_data?: Record<string, any> | null
  score?: number | null
  completed: boolean
  created_at: string
  updated_at: string
}

export interface ModalityMetrics {
  modality: string
  total_events: number
  accuracy: number
  avg_score: number
  avg_response_time_ms: number
  avg_assistance_level: number
}

export interface ActivityTypeMetrics {
  activity_type: string
  total_events: number
  accuracy: number
  avg_score: number
}

export interface LearnerAnalyticsSummary {
  learner_id: string
  total_events: number
  completed_activities: number
  overall_accuracy: number
  avg_score: number
  avg_response_time_ms: number
  avg_hints_per_activity: number
  avg_assistance_level: number
  modality_breakdown: ModalityMetrics[]
  activity_type_breakdown: ActivityTypeMetrics[]
  first_activity_at?: string | null
  last_activity_at?: string | null
}

export interface ObjectiveMasteryStatus {
  objective_id: string
  objective_title: string
  subject_title?: string | null
  difficulty_level: number
  total_attempts: number
  accuracy: number
  avg_assistance_level: number
  mastery_achieved: boolean
  status: 'not_started' | 'in_progress' | 'mastered' | string
  last_attempt_at?: string | null
}

export interface LearnerMasteryReport {
  learner_id: string
  total_objectives_evaluated: number
  mastered_count: number
  in_progress_count: number
  not_started_count: number
  mastery_percentage: number
  objectives: ObjectiveMasteryStatus[]
}

export interface ProgressDataPoint {
  date: string
  events_count: number
  accuracy: number
  avg_score: number
}

export interface LearnerProgressReport {
  learner_id: string
  total_days_active: number
  data_points: ProgressDataPoint[]
}

// ── Recommendation & Adaptive Learning Types (Phase 8) ─────────────────────

export interface RecommendationDecision {
  learner_id: string
  objective_id: string
  objective_title: string
  lesson_id?: string | null
  unit_id?: string | null
  difficulty_level: number
  recommended_modality: Modality
  recommended_activity_type: ActivityType
  recommended_strategy: TeachingStrategy
  scaffolding_tier: number
  rationale: string
  confidence_level: 'high' | 'medium' | 'low'
  confidence_score: number
  evidence_event_count: number
  applied_constraints: string[]
  created_at: string
}

export interface AdaptiveNextActivityResponse {
  decision: RecommendationDecision
  activity: Activity
  fallback_used: boolean
  generation_source: string
}

export interface ProfileSyncResult {
  learner_id: string
  updated_modalities: Record<string, unknown>
  updated_strategies: Record<string, unknown>
  total_events_processed: number
  synced_at: string
}

// ── Teacher Dashboard & Insights Types (Phase 10) ───────────────────────────

export type AlertSeverity = 'info' | 'advisory' | 'priority'

export type AlertTriggerType =
  | 'low_accuracy_repeated'
  | 'assistance_reliance_high'
  | 'mastery_stalled'
  | 'inactivity_threshold'

export interface InterventionAlert {
  id?: string
  alert_id?: string
  learner_id: string
  learner_display_name: string
  trigger_type: AlertTriggerType | string
  severity: AlertSeverity | string
  evidence_window?: string
  summary?: string
  message?: string
  recommended_pedagogical_action?: string
  recommended_action?: string
  evidence_metrics?: Record<string, unknown>
  evidence_context?: Record<string, unknown>
  created_at?: string
  detected_at?: string
  is_resolved?: boolean
}

export interface TeacherDashboardOverview {
  teacher_id?: string
  teacher_name?: string
  total_assigned_learners: number
  total_learners?: number
  active_learners_count: number
  active_learners_7d?: number
  total_completed_activities: number
  total_activities_completed_7d?: number
  average_cohort_accuracy: number
  cohort_average_accuracy_7d?: number
  pending_alerts: InterventionAlert[]
  recent_alerts?: InterventionAlert[]
  recent_recommendations?: RecommendationDecision[]
}

export interface CohortLearnerSummary {
  learner_id: string
  display_name: string
  learning_level: string
  age_group: string
  is_active: boolean
  total_events: number
  completed_activities: number
  overall_accuracy: number
  average_assistance_level: number
  mastered_objectives_count: number
  in_progress_objectives_count: number
  last_active_at?: string | null
  active_alerts_count: number
}

export interface CohortInsights {
  teacher_id: string
  reporting_period: string
  total_cohort_learners: number
  active_learners_in_period: number
  cohort_accuracy: number
  cohort_avg_assistance_level: number
  total_activities_completed: number
  modality_distribution: Record<string, number>
  mastery_status_counts: Record<string, number>
  learners: CohortLearnerSummary[]
}

export interface IEPObjectiveSummary {
  objective_id: string
  title: string
  attempts_count: number
  accuracy: number
  average_assistance: number
  status: string
}

export interface IEPReport {
  report_id: string
  generated_at: string
  reporting_period: string
  start_date?: string | null
  end_date: string
  learner_id: string
  learner_display_name: string
  learning_level: string
  communication_preference: string
  teacher_notes?: string | null
  total_activities_attempted: number
  overall_accuracy: number
  overall_assistance_average: number
  modality_efficacy: Record<string, number>
  objectives_progress: IEPObjectiveSummary[]
  teacher_recommendations: string[]
  printable_summary_markdown: string
}

// ── Instructional Content Types ─────────────────────────────────────────────

export type ExplanationMethod =
  | 'visual_explanation'
  | 'step_by_step'
  | 'worked_example'
  | 'text_explanation'

export type ContentBlockType =
  | 'heading'
  | 'text'
  | 'visual_cue'
  | 'step'
  | 'worked_example'
  | 'callout'
  | 'audio_script'

export type InstructionalStatus =
  | 'draft'
  | 'review_required'
  | 'approved'
  | 'published'
  | 'archived'

export interface InstructionalBlock {
  id: string
  block_type: ContentBlockType
  title?: string | null
  body: string
  visual_cue?: string | null
  order_index: number
  metadata?: Record<string, any>
}

export interface InstructionalContent {
  id: string
  objective_id: string
  title: string
  explanation_method: ExplanationMethod
  difficulty_level: number
  language: string
  blocks: InstructionalBlock[]
  summary: string
  status: InstructionalStatus
  teacher_notes?: string | null
  created_by?: string | null
  metadata?: Record<string, any>
  created_at: string
  updated_at: string
}

export interface InstructionalGenerateRequest {
  objective_id: string
  explanation_method?: ExplanationMethod
  difficulty_level?: number
  language?: string
  teacher_instructions?: string | null
}

export interface InstructionalGenerateResponse {
  content: InstructionalContent
  fallback_used: boolean
  generation_source: string
  grounding_sources: GroundingSource[]
}

export interface InstructionalContentUpdate {
  title?: string | null
  summary?: string | null
  teacher_notes?: string | null
  blocks?: InstructionalBlock[] | null
  status?: InstructionalStatus | null
}

// ── Research Mode & Sandbox Types ──────────────────────────────────────────

export type ResearchOutputTarget =
  | 'freeform'
  | 'instructional_content'
  | 'question_set'
  | 'activity'
  | 'assessment'
  | 'curriculum'
  | 'lesson_plan'

export interface ResearchProject {
  id: string
  name: string
  description?: string | null
  research_question?: string | null
  hypothesis?: string | null
  owner_id: string
  status: string
  metadata_info?: Record<string, any>
  created_at: string
  updated_at: string
}

export interface ResearchExperiment {
  id: string
  project_id: string
  name: string
  description?: string | null
  research_question?: string | null
  hypothesis?: string | null
  status: string
  metadata_info?: Record<string, any>
  created_at: string
  updated_at: string
}

export interface ResearchVariant {
  id: string
  experiment_id: string
  name: string
  description?: string | null
  configuration: Record<string, any>
  parent_variant_id?: string | null
  metadata_info?: Record<string, any>
  created_at: string
  updated_at: string
}

export interface ResearchRun {
  id: string
  variant_id: string
  model: string
  model_configuration: Record<string, any>
  system_prompt?: string | null
  user_prompt: string
  input_snapshot?: Record<string, any> | null
  raw_output?: string | null
  normalized_output?: Record<string, any> | null
  status: string
  error?: string | null
  parent_run_id?: string | null
  metadata_info?: Record<string, any>
  started_at?: string | null
  completed_at?: string | null
  created_at: string
  updated_at: string
  artifact?: ResearchArtifact | null
}

export interface ResearchArtifact {
  id: string
  run_id: string
  artifact_type: string
  schema_version: string
  payload: Record<string, any>
  raw_text?: string | null
  is_production_compatible: boolean
  compatibility_validation?: Record<string, any> | null
  promoted_to_production: boolean
  production_entity_id?: string | null
  metadata_info?: Record<string, any>
  created_at: string
  updated_at: string
}

export interface ResearchMetric {
  id: string
  experiment_id: string
  name: string
  description?: string | null
  metric_type: string
  configuration: Record<string, any>
  created_at: string
  updated_at: string
}

export interface ResearchEvaluation {
  id: string
  artifact_id: string
  metric_id?: string | null
  metric_name: string
  value: Record<string, any>
  evaluator_type: string
  evaluator_id: string
  notes?: string | null
  created_at: string
  updated_at: string
}

export interface ResearchSnapshot {
  id: string
  project_id: string
  source_type: string
  source_reference: string
  snapshot_version: string
  snapshot_data: Record<string, any>
  created_at: string
  updated_at: string
}

export interface ResearchModelInfo {
  id: string
  name: string
  description: string
  is_default: boolean
}

export interface ResearchGenerationRequest {
  project_id: string
  experiment_id: string
  variant_id: string
  prompt: string
  system_prompt?: string | null
  output_target: ResearchOutputTarget
  model?: string
  model_configuration?: Record<string, any>
  explicit_context?: Record<string, any> | null
  question_count?: number | null
  production_compatibility_mode?: boolean
  target_production_schema?: string | null
}

export interface VariantComparisonItem {
  variant: ResearchVariant
  latest_run?: ResearchRun | null
  artifact?: ResearchArtifact | null
  evaluations?: ResearchEvaluation[]
}

export interface ExperimentComparisonResponse {
  experiment_id: string
  experiment_name: string
  project_id: string
  metrics: ResearchMetric[]
  variants: VariantComparisonItem[]
}

export interface ArtifactPromotionResponse {
  success: boolean
  promoted_entity_id?: string | null
  destination: string
  message: string
}
