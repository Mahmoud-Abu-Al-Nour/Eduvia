"""
Eduvia — Teacher Insights & Dashboard API Router (Phase 10)

REST API endpoints for teacher overview dashboard, cohort aggregations,
deterministic intervention alerts, and IEP progress reports.
"""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.auth.dependencies import SessionDep, get_current_user
from app.core.errors import AuthorizationError, NotFoundError, ValidationError
from app.teachers.schemas import (
    CohortInsights,
    IEPReport,
    InterventionAlert,
    TeacherDashboardOverview,
)
from app.teachers.service import TeacherDashboardService
from app.users.models import User

router = APIRouter(prefix="/teachers", tags=["teachers"])


def get_teacher_dashboard_service(session: SessionDep) -> TeacherDashboardService:
    return TeacherDashboardService(session)


@router.get(
    "/dashboard",
    response_model=TeacherDashboardOverview,
    status_code=status.HTTP_200_OK,
    summary="Get teacher overview dashboard KPIs",
    description="Returns high-level active student counts, 7-day activities, cohort accuracy, and active alerts.",
)
async def get_teacher_dashboard(
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[TeacherDashboardService, Depends(get_teacher_dashboard_service)],
) -> TeacherDashboardOverview:
    try:
        return await service.get_dashboard_overview(current_user)
    except AuthorizationError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.message) from exc
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc


@router.get(
    "/cohort/insights",
    response_model=CohortInsights,
    status_code=status.HTTP_200_OK,
    summary="Get classroom/cohort-wide aggregated insights",
    description="Returns class-wide modality distributions, mastery distributions, and individual student progress summaries.",
)
async def get_cohort_insights(
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[TeacherDashboardService, Depends(get_teacher_dashboard_service)],
    days: int = Query(default=30, ge=0, le=365, description="Reporting period in days (0 for all-time)"),
) -> CohortInsights:
    try:
        return await service.get_cohort_insights(current_user, days=days)
    except AuthorizationError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.message) from exc
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc


@router.get(
    "/alerts",
    response_model=list[InterventionAlert],
    status_code=status.HTTP_200_OK,
    summary="Get active deterministic intervention alerts",
    description="Returns rule-based educational signals requiring teacher intervention across assigned learners.",
)
async def get_intervention_alerts(
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[TeacherDashboardService, Depends(get_teacher_dashboard_service)],
    learner_id: uuid.UUID | None = Query(default=None, description="Filter alerts by specific learner ID"),
) -> list[InterventionAlert]:
    try:
        return await service.get_intervention_alerts(current_user, target_learner_id=learner_id)
    except AuthorizationError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.message) from exc
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc


@router.get(
    "/learners/{learner_id}/iep-report",
    response_model=IEPReport,
    status_code=status.HTTP_200_OK,
    summary="Generate Individualized Education Plan (IEP) progress report",
    description="Compiles objective mastery status, assistance history, modality efficacy, and printable Markdown export.",
)
async def get_learner_iep_report(
    learner_id: uuid.UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[TeacherDashboardService, Depends(get_teacher_dashboard_service)],
    days: int = Query(default=30, ge=0, le=365, description="Reporting window in days (0 for all-time)"),
) -> IEPReport:
    try:
        return await service.get_learner_iep_report(current_user, learner_id=learner_id, days=days)
    except AuthorizationError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.message) from exc
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc
