"""
Eduvia — Teachers Module (Phase 10)
"""

from app.teachers.router import get_teacher_dashboard_service, router
from app.teachers.schemas import (
    AlertSeverity,
    AlertTriggerType,
    CohortInsights,
    CohortLearnerSummary,
    IEPObjectiveSummary,
    IEPReport,
    IEPReportingPeriod,
    InterventionAlert,
    TeacherDashboardOverview,
)
from app.teachers.service import TeacherDashboardService

__all__ = [
    "router",
    "TeacherDashboardService",
    "get_teacher_dashboard_service",
    "TeacherDashboardOverview",
    "CohortInsights",
    "CohortLearnerSummary",
    "InterventionAlert",
    "AlertSeverity",
    "AlertTriggerType",
    "IEPReport",
    "IEPObjectiveSummary",
    "IEPReportingPeriod",
]
