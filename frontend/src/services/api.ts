/**
 * Eduvia API Service
 *
 * Centralized HTTP client for all backend communication.
 * Uses Axios with interceptors for auth, error handling, and logging.
 *
 * All API calls in the application should go through this service,
 * never raw fetch() or raw Axios calls scattered in components.
 */
import axios, {
  type AxiosInstance,
  type AxiosRequestConfig,
  type AxiosResponse,
  type InternalAxiosRequestConfig,
} from 'axios'
import type { HealthCheckResponse } from '@/types'
import tokenStorage from './tokenStorage'

// ── Axios Instance ────────────────────────────────────────────────────────

const RAW_BASE_URL = import.meta.env.VITE_API_BASE_URL
// Use Vite reverse-proxy path (/api/v1) when in dev mode or fallback to IPv4 loopback
const API_BASE_URL = RAW_BASE_URL === '' || RAW_BASE_URL === undefined
  ? ''
  : RAW_BASE_URL.replace('localhost', '127.0.0.1')
const API_V1_PREFIX = '/api/v1'

const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL ? `${API_BASE_URL}${API_V1_PREFIX}` : API_V1_PREFIX,
  timeout: 30_000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
})

// ── Request Interceptor: Auth Token ───────────────────────────────────────

apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig): InternalAxiosRequestConfig => {
    const token = tokenStorage.getAccessToken()
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error instanceof Error ? error : new Error(String(error))),
)

// ── Response Interceptor: Error Normalization ─────────────────────────────

apiClient.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error) => {
    const status = error.response?.status

    if (status === 401) {
      // Auth token expired / invalid — clear canonical tokens via tokenStorage
      tokenStorage.clearTokens()
      if (typeof window !== 'undefined' && window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }

    // Distinguish specific HTTP status classes per Phase 18 requirements
    let message = error.response?.data?.message || error.response?.data?.detail
    if (!message) {
      if (status === 404) {
        message = 'Requested educational resource or endpoint was not found.'
      } else if (status === 403) {
        message = 'You do not have permission to access this educational resource.'
      } else if (status === 401) {
        message = 'Your session has expired. Please sign in again.'
      } else if (status === 422) {
        message = 'The provided data could not be validated by the server.'
      } else if (status && status >= 500) {
        message = 'The backend server encountered an error. Please try again shortly.'
      } else if (!error.response) {
        message = 'Unable to connect to the backend server. Please verify the API is running.'
      } else {
        message = error.message || 'An unexpected error occurred'
      }
    }

    const normalizedError = new Error(message) as Error & {
      code?: string
      status?: number
    }
    normalizedError.code = error.response?.data?.error || (status ? `HTTP_${status}` : 'NETWORK_ERROR')
    normalizedError.status = status

    return Promise.reject(normalizedError)
  },
)

// ── API Service Methods ───────────────────────────────────────────────────

/**
 * Generic GET request
 */
async function get<T>(
  url: string,
  config?: AxiosRequestConfig,
): Promise<T> {
  const response = await apiClient.get<T>(url, config)
  return response.data
}

/**
 * Generic POST request
 */
async function post<T, D = unknown>(
  url: string,
  data?: D,
  config?: AxiosRequestConfig,
): Promise<T> {
  const response = await apiClient.post<T>(url, data, config)
  return response.data
}

/**
 * Generic PUT request
 */
async function put<T, D = unknown>(
  url: string,
  data?: D,
  config?: AxiosRequestConfig,
): Promise<T> {
  const response = await apiClient.put<T>(url, data, config)
  return response.data
}

/**
 * Generic PATCH request
 */
async function patch<T, D = unknown>(
  url: string,
  data?: D,
  config?: AxiosRequestConfig,
): Promise<T> {
  const response = await apiClient.patch<T>(url, data, config)
  return response.data
}

/**
 * Generic DELETE request
 */
async function del<T>(
  url: string,
  config?: AxiosRequestConfig,
): Promise<T> {
  const response = await apiClient.delete<T>(url, config)
  return response.data
}

// ── Specific API Endpoints ────────────────────────────────────────────────

/**
 * Health check API endpoints
 */
export const healthApi = {
  /** Basic health check — fast, for connectivity verification */
  check: () => get<HealthCheckResponse>('/health'),

  /** Detailed health check — includes dependency status */
  detailed: () => get<HealthCheckResponse>('/health/detailed'),
}

// ── Activities API (Phase 4 & 5) ──────────────────────────────────────────

export const activitiesApi = {
  /** Generate a structured learning activity */
  generate: (data: {
    objective_id: string
    learner_id?: string | null
    activity_type?: string | null
    difficulty_level?: number | null
    language?: string
  }) =>
    post<{
      activity: import('@/types').Activity
      fallback_used: boolean
      generation_source: string
      learner_id?: string | null
      objective_id: string
    }>('/activities/generate', data),

  /** Retrieve an activity by ID */
  getById: (activityId: string) =>
    get<import('@/types').Activity>(`/activities/${activityId}`),

  /** Evaluate a learner submission authoritatively */
  evaluate: (data: import('@/types').ActivitySubmissionRequest) =>
    post<import('@/types').ActivityEvaluationResponse>('/activities/evaluate', data),

  /** List supported activity types */
  listTypes: () =>
    get<Array<{ type: string; name: string; description: string; primary_modality: string }>>(
      '/activities/types'
    ),
}

// ── Analytics API (Phase 6) ───────────────────────────────────────────

export const analyticsApi = {
  /** Record a performance telemetry event */
  recordEvent: (event: import('@/types').PerformanceEvent) =>
    post<import('@/types').PerformanceEvent>('/analytics/events', event),

  /** Record an activity attempt session */
  recordAttempt: (attempt: Partial<import('@/types').ActivityAttempt> & { activity_id: string; learner_id: string }) =>
    post<import('@/types').ActivityAttempt>('/analytics/attempts', attempt),

  /** Query performance events for a learner */
  getLearnerEvents: (
    learnerId: string,
    params?: {
      activity_type?: string
      objective_id?: string
      correct?: boolean
      limit?: number
      offset?: number
    }
  ) =>
    get<import('@/types').PerformanceEvent[]>(`/analytics/learners/${learnerId}/events`, {
      params,
    }),

  /** Get a single performance event by ID */
  getEventById: (eventId: string) =>
    get<import('@/types').PerformanceEvent>(`/analytics/events/${eventId}`),

  /** Get performance analytics summary for a learner */
  getLearnerSummary: (learnerId: string) =>
    get<import('@/types').LearnerAnalyticsSummary>(`/analytics/learners/${learnerId}/summary`),

  /** Get curriculum objective mastery report for a learner */
  getLearnerMastery: (learnerId: string) =>
    get<import('@/types').LearnerMasteryReport>(`/analytics/learners/${learnerId}/mastery`),

  /** Get longitudinal progress timeline for a learner */
  getLearnerProgress: (learnerId: string, days: number = 30) =>
    get<import('@/types').LearnerProgressReport>(`/analytics/learners/${learnerId}/progress`, {
      params: { days },
    }),
}

/** Recommendations & Adaptive Learning API endpoints (Phase 8) */
export const recommendationsApi = {
  /** Get current adaptive recommendation for a learner */
  getRecommendation: (learnerId: string, language: string = 'en') =>
    get<import('@/types').RecommendationDecision>(`/recommendations/learners/${learnerId}`, {
      params: { language },
    }),

  /** Get recommendation and generate next activity in a unified call */
  getNextActivity: (learnerId: string, language: string = 'en') =>
    post<import('@/types').AdaptiveNextActivityResponse>(
      `/recommendations/learners/${learnerId}/next-activity`,
      null,
      { params: { language } }
    ),

  /** Synchronize learner profile modality and strategy effectiveness */
  syncProfile: (learnerId: string) =>
    post<import('@/types').ProfileSyncResult>(`/recommendations/learners/${learnerId}/sync-profile`),
}

/** Teacher Dashboard & Insights API endpoints (Phase 10) */
export const teachersApi = {
  /** Get teacher overview metrics and active alerts */
  getDashboardOverview: () =>
    get<import('@/types').TeacherDashboardOverview>('/teachers/dashboard'),

  /** Get classroom / cohort aggregated performance insights */
  getCohortInsights: (days?: number) =>
    get<import('@/types').CohortInsights>('/teachers/cohort/insights', {
      params: days ? { days } : undefined,
    }),

  /** Get intervention alerts for assigned learners */
  getAlerts: (includeResolved: boolean = false) =>
    get<import('@/types').InterventionAlert[]>('/teachers/alerts', {
      params: { include_resolved: includeResolved },
    }),

  /** Get Individualized Education Plan (IEP) progress report */
  getIEPReport: (learnerId: string, days?: number) =>
    get<import('@/types').IEPReport>(`/teachers/learners/${learnerId}/iep-report`, {
      params: days ? { days } : undefined,
    }),
}

export const api = {
  get,
  post,
  put,
  patch,
  delete: del,
  health: healthApi,
  activities: activitiesApi,
  analytics: analyticsApi,
  recommendations: recommendationsApi,
  teachers: teachersApi,
  client: apiClient,
}

export default api


