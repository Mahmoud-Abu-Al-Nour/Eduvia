"""
Eduvia — Analytics & Telemetry Module (Phase 6)
"""
from app.analytics.models import ActivityAttempt, PerformanceEvent
from app.analytics.schemas import (
    ActivityAttemptCreate,
    ActivityAttemptRead,
    Modality,
    PerformanceEventCreate,
    PerformanceEventQueryFilter,
    PerformanceEventRead,
    TeachingStrategy,
)
from app.analytics.service import AnalyticsService

__all__ = [
    "ActivityAttempt",
    "PerformanceEvent",
    "ActivityAttemptCreate",
    "ActivityAttemptRead",
    "PerformanceEventCreate",
    "PerformanceEventQueryFilter",
    "PerformanceEventRead",
    "Modality",
    "TeachingStrategy",
    "AnalyticsService",
]
