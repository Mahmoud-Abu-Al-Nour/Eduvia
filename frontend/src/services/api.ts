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

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const API_V1_PREFIX = '/api/v1'

const apiClient: AxiosInstance = axios.create({
  baseURL: `${API_BASE_URL}${API_V1_PREFIX}`,
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
    if (error.response?.status === 401) {
      // Auth token expired / invalid — clear canonical tokens via tokenStorage
      tokenStorage.clearTokens()
      if (typeof window !== 'undefined' && window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }

    // Normalize error message from backend error schema
    const message =
      error.response?.data?.message ||
      error.response?.data?.detail ||
      error.message ||
      'An unexpected error occurred'

    const normalizedError = new Error(message) as Error & {
      code?: string
      status?: number
    }
    normalizedError.code = error.response?.data?.error
    normalizedError.status = error.response?.status

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
  client: apiClient,
}

export default api

