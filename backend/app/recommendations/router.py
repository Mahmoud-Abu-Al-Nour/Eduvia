"""
Eduvia — Recommendations API Router (Phase 8)

REST API endpoints for adaptive recommendations, next-activity generation,
and learner profile effectiveness synchronization.
"""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.core.errors import AuthorizationError, NotFoundError, ValidationError
from app.database.session import get_db_session
from app.recommendations.schemas import (
    AdaptiveNextActivityResponse,
    ProfileSyncResult,
    RecommendationDecision,
)
from app.recommendations.service import RecommendationService
from app.users.models import User

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


def get_recommendation_service(
    session: AsyncSession = Depends(get_db_session),
) -> RecommendationService:
    return RecommendationService(session)


@router.get(
    "/learners/{learner_id}",
    response_model=RecommendationDecision,
    status_code=status.HTTP_200_OK,
    summary="Get current adaptive recommendation for a learner",
)
async def get_recommendation(
    learner_id: uuid.UUID,
    language: str = Query(default="en", description="Localization language code"),
    service: RecommendationService = Depends(get_recommendation_service),
    current_user: User = Depends(get_current_user),
) -> RecommendationDecision:
    """
    Computes a deterministic recommendation for the learner's next educational target,
    calibrating difficulty, presentation modality, and teaching strategy from empirical evidence.
    """
    try:
        return await service.get_recommendation(learner_id, current_user, language=language)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc
    except AuthorizationError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.message) from exc
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message) from exc


@router.post(
    "/learners/{learner_id}/next-activity",
    response_model=AdaptiveNextActivityResponse,
    status_code=status.HTTP_200_OK,
    summary="Get recommendation and generate next activity in a unified call",
)
async def get_next_activity(
    learner_id: uuid.UUID,
    language: str = Query(default="en", description="Localization language code"),
    service: RecommendationService = Depends(get_recommendation_service),
    current_user: User = Depends(get_current_user),
) -> AdaptiveNextActivityResponse:
    """
    Computes the adaptive recommendation decision and invokes the Phase 4 Activity Generation
    Engine to generate a playable activity tailored to the recommended parameters.
    """
    try:
        return await service.get_next_activity(learner_id, current_user, language=language)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc
    except AuthorizationError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.message) from exc
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message) from exc


@router.post(
    "/learners/{learner_id}/sync-profile",
    response_model=ProfileSyncResult,
    status_code=status.HTTP_200_OK,
    summary="Synchronize learner profile modality and strategy effectiveness",
)
async def sync_learner_profile(
    learner_id: uuid.UUID,
    service: RecommendationService = Depends(get_recommendation_service),
    current_user: User = Depends(get_current_user),
) -> ProfileSyncResult:
    """
    Derives empirical modality and strategy success ratings from historical telemetry events
    and writes the updated matrix into the learner's persistent profile.
    """
    try:
        return await service.sync_learner_profile_effectiveness(learner_id, current_user)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc
    except AuthorizationError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=exc.message) from exc
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.message) from exc
