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

// ── Activity Types ─────────────────────────────────────────────────────────

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

export interface Activity {
  id: string
  objective_id: string
  activity_type: ActivityType
  modality: Modality
  strategy: TeachingStrategy
  difficulty: 1 | 2 | 3 | 4 | 5
  content: ActivityContent
  audio_enabled: boolean
  created_at: string
}

// Activity content is a discriminated union based on activity_type
export type ActivityContent =
  | MatchingContent
  | MultipleChoiceContent
  | OrderingContent
  | VisualIdentificationContent
  | DragDropContent

export interface MatchingContent {
  type: 'matching'
  instruction: string
  pairs: Array<{ left: string; right: string }>
}

export interface MultipleChoiceContent {
  type: 'multiple_choice'
  question: string
  options: string[]
  correct_index: number
  explanation?: string
}

export interface OrderingContent {
  type: 'ordering'
  instruction: string
  items: string[]
  correct_order: number[]
}

export interface VisualIdentificationContent {
  type: 'visual_identification'
  instruction: string
  image_url: string
  target: string
  options: string[]
}

export interface DragDropContent {
  type: 'drag_drop'
  instruction: string
  items: string[]
  targets: string[]
  correct_mapping: Record<string, string>
}

// ── Performance & Analytics Types ──────────────────────────────────────────

export interface PerformanceEvent {
  learner_id: string
  activity_id: string
  objective_id: string
  activity_type: ActivityType
  modality: Modality
  strategy: TeachingStrategy
  correct: boolean
  attempts: number
  response_time_ms: number
  hints_used: number
  assistance_level: number
  completed: boolean
}

// ── Recommendation Types ───────────────────────────────────────────────────

export interface Recommendation {
  learner_id: string
  objective_id: string
  recommended_modality: Modality
  recommended_strategy: TeachingStrategy
  recommended_activity_type: ActivityType
  confidence: number
  explanation: string
  evidence_summary: string
}
