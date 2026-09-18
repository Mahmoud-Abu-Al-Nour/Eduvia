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

// ── Learner Types ──────────────────────────────────────────────────────────

export type AgeGroup = 'early_childhood' | 'childhood' | 'adolescent' | 'adult'
export type CommunicationPreference = 'verbal' | 'visual' | 'augmentative' | 'mixed'
export type LearningLevel = 'foundation' | 'developing' | 'emerging' | 'established'

export interface Learner {
  id: string
  display_name: string
  age_group: AgeGroup
  learning_level: LearningLevel
  communication_preference: CommunicationPreference
  support_requirements: string[]
  teacher_notes: string
  is_active: boolean
  created_at: string
  updated_at: string
}

// ── Learner Profile Types ──────────────────────────────────────────────────

export type Modality = 'visual' | 'reading' | 'writing' | 'audio' | 'interactive'

export interface ModalityScore {
  score: number          // 0.0 – 1.0
  confidence: number     // 0.0 – 1.0
  evidence_count: number
}

export interface LearnerProfile {
  learner_id: string
  modality_scores: Record<Modality, ModalityScore>
  strategy_scores: Record<string, ModalityScore>
  last_updated: string
  total_activities_completed: number
  exploration_phase: boolean
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
