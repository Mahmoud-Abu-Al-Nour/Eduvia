"""
Eduvia — Activity Generation API Router (Phase 4)

Endpoints:
- POST /activities/generate: Generates an activity for a learning objective & learner.
- GET /activities/types: Lists supported activity modalities and descriptions.
"""
import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.activities.schemas import (
    Activity,
    ActivityEvaluationResponse,
    ActivityGenerateRequest,
    ActivityGenerateResponse,
    ActivitySubmissionRequest,
    ActivityType,
)
from app.activities.service import ActivityService
from app.auth.dependencies import get_current_user
from app.core.errors import NotFoundError, ValidationError
from app.core.rate_limit import (
    activity_evaluate_rate_limiter,
    activity_generate_rate_limiter,
    get_client_ip,
)
from app.database.session import get_db_session
from app.users.models import User


router = APIRouter(prefix="/activities", tags=["activities"])



def get_activity_service(
    session: AsyncSession = Depends(get_db_session),
) -> ActivityService:
    """Dependency provider for ActivityService."""
    return ActivityService(session=session)


@router.post(
    "/generate",
    response_model=ActivityGenerateResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate an accessible learning activity",
    description=(
        "Generates a validated, structured activity for a specific learning objective. "
        "Optionally tailors delivery using learner profile evidence, sensory accommodations, "
        "and teacher constraints. Falls back to a deterministic activity if the generative "
        "AI provider is unavailable or fails validation."
    ),
)
async def generate_activity(
    request: ActivityGenerateRequest,
    http_request: Request,
    current_user: User = Depends(get_current_user),
    service: ActivityService = Depends(get_activity_service),
) -> ActivityGenerateResponse:
    # Rate limit check by teacher identity
    key = f"generate:user:{current_user.id}" if current_user and current_user.id else f"generate:ip:{get_client_ip(http_request)}"
    activity_generate_rate_limiter.check(key)
    return await service.generate_activity(request=request, current_user=current_user)


@router.get(
    "/types",
    response_model=list[dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="List supported activity modalities",
    description="Returns metadata about all supported activity types.",
)
async def list_activity_types() -> list[dict[str, Any]]:
    return [
        {
            "type": ActivityType.MULTIPLE_CHOICE.value,
            "name": "Multiple Choice",
            "description": "Select the correct option among 2-5 calibrated alternatives.",
            "primary_modality": "Visual / Reading",
        },
        {
            "type": ActivityType.MATCHING.value,
            "name": "Matching Pairs",
            "description": "Connect corresponding items across two columns.",
            "primary_modality": "Visual / Interactive",
        },
        {
            "type": ActivityType.ORDERING.value,
            "name": "Sequential Ordering",
            "description": "Arrange items along an ascending, descending, or chronological continuum.",
            "primary_modality": "Interactive / Conceptual",
        },
        {
            "type": ActivityType.VISUAL_IDENTIFICATION.value,
            "name": "Visual Identification",
            "description": "Identify a target element within an accessible visual scene.",
            "primary_modality": "Visual / Spatial",
        },
        {
            "type": ActivityType.DRAG_DROP.value,
            "name": "Drag and Drop Categorization",
            "description": "Categorize items into designated target zones.",
            "primary_modality": "Kinesthetic / Interactive",
        },
    ]


@router.post(
    "/evaluate",
    response_model=ActivityEvaluationResponse,
    status_code=status.HTTP_200_OK,
    summary="Evaluate learner activity submission",
    description=(
        "Authoritatively evaluates a learner's submission against activity content. "
        "Enforces schema validation, calculates accuracy score, evaluates objective "
        "mastery criteria, and returns encouraging Cognitive Calm feedback."
    ),
)
async def evaluate_submission(
    request: ActivitySubmissionRequest,
    http_request: Request,
    service: ActivityService = Depends(get_activity_service),
) -> ActivityEvaluationResponse:
    # Rate limit check by client IP
    client_ip = get_client_ip(http_request)
    activity_evaluate_rate_limiter.check(f"evaluate:{client_ip}")

    try:
        return await service.evaluate_submission(request=request)
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=exc.message,
        )
    except NotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.message,
        )


@router.get(
    "/{activity_id}",
    response_model=Activity,
    status_code=status.HTTP_200_OK,
    summary="Retrieve activity by ID",
    description="Fetches an activity instance from the registry for learner interaction.",
)
async def get_activity(
    activity_id: uuid.UUID,
    service: ActivityService = Depends(get_activity_service),
) -> Activity:
    activity = await service.get_activity(activity_id=activity_id)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Activity with id '{activity_id}' not found.",
        )
    return activity


