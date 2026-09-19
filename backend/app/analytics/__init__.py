"""
Eduvia — Analytics & Telemetry Module (Phase 6)
"""
from app.analytics.models import ActivityAttempt, PerformanceEvent
from app.analytics.schemas import (
    ActivityAttemptCreate,
    ActivityAttemptRead,
    ActivityTypeMetrics,
    LearnerAnalyticsSummary,
    LearnerMasteryReport,
    LearnerProgressReport,
    Modality,
    ModalityMetrics,
    ObjectiveMasteryStatus,
    PerformanceEventCreate,
    PerformanceEventQueryFilter,
    PerformanceEventRead,
    ProgressDataPoint,
    TeachingStrategy,
)
from app.analytics.service import AnalyticsService

__all__ = [
    "ActivityAttempt",
    "PerformanceEvent",
    "ActivityAttemptCreate",
    "ActivityAttemptRead",
    "ActivityTypeMetrics",
    "LearnerAnalyticsSummary",
    "LearnerMasteryReport",
    "LearnerProgressReport",
    "ModalityMetrics",
    "ObjectiveMasteryStatus",
    "PerformanceEventCreate",
    "PerformanceEventQueryFilter",
    "PerformanceEventRead",
    "ProgressDataPoint",
    "Modality",
    "TeachingStrategy",
    "AnalyticsService",
]
