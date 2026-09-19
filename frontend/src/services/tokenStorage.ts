/**
 * Eduvia Token Storage Service
 *
 * Centralized, canonical token management across the Eduvia frontend.
 * Provides the single source of truth for authentication token persistence and lifecycle.
 * All components and services must use this module rather than scattered direct localStorage access.
 */

export const TOKEN_KEYS = {
  ACCESS_TOKEN: "eduvia_access_token",
  REFRESH_TOKEN: "eduvia_refresh_token",
} as const;

type AuthExpiredListener = () => void;
const expiredListeners: Set<AuthExpiredListener> = new Set();

export const tokenStorage = {
  /**
   * Retrieve the current JWT access token.
   */
  getAccessToken(): string | null {
    if (typeof window === "undefined" || !window.localStorage) {
      return null;
    }
    return window.localStorage.getItem(TOKEN_KEYS.ACCESS_TOKEN);
  },

  /**
   * Retrieve the current JWT refresh token.
   */
  getRefreshToken(): string | null {
    if (typeof window === "undefined" || !window.localStorage) {
      return null;
    }
    return window.localStorage.getItem(TOKEN_KEYS.REFRESH_TOKEN);
  },

  /**
   * Persist access and refresh tokens canonically.
   */
  setTokens(accessToken: string, refreshToken: string): void {
    if (typeof window === "undefined" || !window.localStorage) {
      return;
    }
    window.localStorage.setItem(TOKEN_KEYS.ACCESS_TOKEN, accessToken);
    window.localStorage.setItem(TOKEN_KEYS.REFRESH_TOKEN, refreshToken);
  },

  /**
   * Clear all persisted tokens and notify active listeners.
   */
  clearTokens(): void {
    if (typeof window !== "undefined" && window.localStorage) {
      window.localStorage.removeItem(TOKEN_KEYS.ACCESS_TOKEN);
      window.localStorage.removeItem(TOKEN_KEYS.REFRESH_TOKEN);
    }

    expiredListeners.forEach((listener) => {
      try {
        listener();
      } catch (err) {
        console.error("Error executing auth expired listener:", err);
      }
    });
  },

  /**
   * Check whether an access token exists.
   */
  hasAccessToken(): boolean {
    return Boolean(this.getAccessToken());
  },

  /**
   * Register a subscriber callback triggered when tokens are cleared / session expires.
   * Returns an unsubscribe function.
   */
  onAuthExpired(listener: AuthExpiredListener): () => void {
    expiredListeners.add(listener);
    return () => {
      expiredListeners.delete(listener);
    };
  },
};

export default tokenStorage;
