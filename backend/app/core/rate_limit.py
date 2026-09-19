"""
Eduvia — In-Memory Sliding-Window Rate Limiter
Phase 11: System Hardening & Abuse Protection

Provides thread-safe, bounded, in-memory rate limiting with automatic
eviction of stale entries to protect security-sensitive endpoints from abuse.
"""
import math
import threading
import time
from collections import deque
from collections.abc import Callable

from fastapi import HTTPException, Request, status
import structlog

logger = structlog.get_logger(__name__)


def get_client_ip(request: Request) -> str:
    """
    Extract the client IP address from the request.
    Prioritizes X-Forwarded-For when behind a proxy.
    """
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client and request.client.host:
        return request.client.host
    return "127.0.0.1"


class InMemoryRateLimiter:
    """
    Thread-safe, bounded in-memory rate limiter using a sliding-window algorithm.

    Attributes:
        max_requests: Maximum allowed requests within the time window.
        window_seconds: Duration of the sliding window in seconds.
        max_entries: Maximum number of tracked keys to prevent memory exhaustion.
        time_func: Callable returning current epoch time (injectable for tests).
    """

    def __init__(
        self,
        max_requests: int,
        window_seconds: int = 60,
        max_entries: int = 10_000,
        time_func: Callable[[], float] | None = None,
    ) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.max_entries = max_entries
        self._time_func = time_func or time.time
        self._buckets: dict[str, deque[float]] = {}
        self._lock = threading.Lock()

    def _evict_stale_locked(self, now: float) -> None:
        """Evict keys whose newest timestamp is older than the window."""
        cutoff = now - self.window_seconds
        stale_keys = [
            k for k, timestamps in self._buckets.items()
            if not timestamps or timestamps[-1] <= cutoff
        ]
        for k in stale_keys:
            del self._buckets[k]

        # If still over capacity, remove oldest half
        if len(self._buckets) >= self.max_entries:
            sorted_items = sorted(
                self._buckets.items(),
                key=lambda item: item[1][-1] if item[1] else 0.0,
            )
            to_remove = len(self._buckets) - (self.max_entries // 2)
            for k, _ in sorted_items[:to_remove]:
                del self._buckets[k]

    def check(self, key: str) -> None:
        """
        Record an access attempt for key.
        Raises HTTP 429 Too Many Requests if the threshold is exceeded.
        """
        now = self._time_func()
        cutoff = now - self.window_seconds

        with self._lock:
            # Capacity guard: prune stale keys if near max entries
            if len(self._buckets) >= self.max_entries and key not in self._buckets:
                self._evict_stale_locked(now)

            if key not in self._buckets:
                self._buckets[key] = deque()

            bucket = self._buckets[key]

            # Prune timestamps outside current sliding window
            while bucket and bucket[0] <= cutoff:
                bucket.popleft()

            if len(bucket) >= self.max_requests:
                earliest = bucket[0]
                retry_after = max(1, math.ceil(earliest + self.window_seconds - now))
                logger.warning(
                    "rate_limit_exceeded",
                    key=key,
                    limit=self.max_requests,
                    window=self.window_seconds,
                    retry_after=retry_after,
                )
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded. Please retry after {retry_after} seconds.",
                    headers={"Retry-After": str(retry_after)},
                )

            bucket.append(now)

    def reset(self) -> None:
        """Clear all rate limit entries (useful for test resets)."""
        with self._lock:
            self._buckets.clear()

    @property
    def tracked_keys_count(self) -> int:
        """Return the number of tracked keys."""
        with self._lock:
            return len(self._buckets)


# ── Global Rate Limiter Instances ─────────────────────────────────────────────
# 1. Login Endpoint: Client/IP based throttling (5 attempts / min)
login_rate_limiter = InMemoryRateLimiter(max_requests=5, window_seconds=60)

# 2. Activity Generation: Teacher / User identity throttling (20 reqs / min)
activity_generate_rate_limiter = InMemoryRateLimiter(max_requests=20, window_seconds=60)

# 3. Activity Evaluation: Learner interaction throttling (60 reqs / min per client)
activity_evaluate_rate_limiter = InMemoryRateLimiter(max_requests=60, window_seconds=60)
