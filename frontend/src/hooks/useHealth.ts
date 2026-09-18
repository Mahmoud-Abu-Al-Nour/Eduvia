/**
 * useHealth — Custom React hook for backend health monitoring
 *
 * Fetches health status from the backend API.
 * Used by the developer status bar and monitoring components.
 */
import { useCallback, useEffect, useState } from 'react'
import { api } from '@/services/api'
import type { HealthCheckResponse } from '@/types'

interface UseHealthReturn {
  health: HealthCheckResponse | null
  isLoading: boolean
  error: string | null
  refresh: () => void
}

export function useHealth(): UseHealthReturn {
  const [health, setHealth] = useState<HealthCheckResponse | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchHealth = useCallback(async () => {
    setIsLoading(true)
    setError(null)
    try {
      const data = await api.health.detailed()
      setHealth(data)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to reach backend'
      setError(message)
      setHealth(null)
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    void fetchHealth()
  }, [fetchHealth])

  return {
    health,
    isLoading,
    error,
    refresh: fetchHealth,
  }
}
