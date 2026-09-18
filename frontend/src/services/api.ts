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
    const token = localStorage.getItem('eduvia_access_token')
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
      // Auth token expired — clear and redirect to login
      localStorage.removeItem('eduvia_access_token')
      localStorage.removeItem('eduvia_refresh_token')
      window.location.href = '/login'
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

/**
 * Future API namespaces — implemented in later phases:
 *
 * export const authApi = { ... }          // Phase 1
 * export const learnersApi = { ... }      // Phase 3
 * export const curriculumApi = { ... }    // Phase 2
 * export const activitiesApi = { ... }    // Phase 4
 * export const analyticsApi = { ... }     // Phase 7
 * export const recommendationsApi = { ... } // Phase 8
 */

// ── Export ────────────────────────────────────────────────────────────────

export const api = {
  get,
  post,
  put,
  patch,
  delete: del,
  health: healthApi,
}

export default apiClient
