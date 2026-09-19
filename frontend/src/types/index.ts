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

export type UserRole = 'admin' | 'teacher'

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
  is_correct: boolean
  distractor_rationale?: string | null
}

export interface MultipleChoiceContent {
  activity_type: 'multiple_choice'
  question: string
  options: MultipleChoiceOption[]
  correct_answer_id: string
  explanation: string
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
  pairs: MatchingPair[]
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
  correct_sequence: string[]
  direction?: 'ascending' | 'descending' | 'chronological' | string
}

export interface VisualElement {
  id: string
  label: string
  category?: string
  is_target: boolean
  bounding_hint?: string | null
}

export interface VisualIdentificationContent {
  activity_type: 'visual_identification'
  prompt: string
  scene_description: string
  elements: VisualElement[]
  target_id: string
  feedback_clue: string
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
  correct_mapping: Record<string, string>
}

export type ActivityContent =
  | MultipleChoiceContent
  | MatchingContent
  | OrderingContent
  | VisualIdentificationContent
  | DragDropContent

export interface Activity {
  id: string
  objective_id: string
  activity_type: ActivityType
  title: string
  instructions: string
  difficulty_level: number
  content: ActivityContent
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

export interface ActivitySubmissionRequest {
  activity_id: string
  objective_id: string
  activity_type: ActivityType
  submission: ActivitySubmissionPayload
  learner_id?: string | null
  hints_used: number
  time_spent_seconds: number
  activity_content?: ActivityContent | null
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
}

type bool_or_boolean = boolean


// ── Performance & Analytics Types ──────────────────────────────────────────

export interface PerformanceEvent {
  id?: string
  learner_id: string
  activity_id: string
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

