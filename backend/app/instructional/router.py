"""
Eduvia — Instructional Content Router (Phase 4 Extension)

Exposes REST endpoints for:
- Generating non-evaluative instructional explanations via Gemini + RAG
- Teacher review, editing, approval, and publishing
- Learner consumption of approved/published instructional material
"""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import (
    get_current_active_teacher,
    get_current_user,
    get_current_user_optional,
)
from app.core.errors import NotFoundError
from app.database.session import get_db_session
from app.instructional.schemas import (
    InstructionalContentRead,
    InstructionalContentUpdate,
    InstructionalGenerateRequest,
    InstructionalGenerateResponse,
)
from app.instructional.service import InstructionalService
from app.users.models import User

router = APIRouter(prefix="/instructional-content", tags=["instructional-content"])


def get_instructional_service(
    session: AsyncSession = Depends(get_db_session),
) -> InstructionalService:
    return InstructionalService(session=session)


@router.post(
    "/generate",
    response_model=InstructionalGenerateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate instructional content for an objective",
)
async def generate_instructional_content(
    request: InstructionalGenerateRequest,
    current_user: Annotated[User, Depends(get_current_active_teacher)],
    service: InstructionalService = Depends(get_instructional_service),
) -> InstructionalGenerateResponse:
    """Generate structured explanation blocks (review_required status)."""
    return await service.generate(request=request, current_user=current_user)


@router.get(
    "/objective/{objective_id}",
    response_model=list[InstructionalContentRead],
    summary="Get instructional content for an objective",
)
async def get_by_objective(
    objective_id: uuid.UUID,
    published_only: bool = Query(True, description="Filter for approved/published items only"),
    current_user: User | None = Depends(get_current_user_optional),
    service: InstructionalService = Depends(get_instructional_service),
) -> list[InstructionalContentRead]:
    """Retrieve instructional explanations. Non-teachers can only view published/approved items."""
    is_teacher = current_user is not None and current_user.role.value in ("teacher", "admin")
    effective_published_only = published_only if is_teacher else True
    results = await service.get_by_objective(
        objective_id=objective_id,
        published_only=effective_published_only,
    )
    if not is_teacher:
        for item in results:
            item.teacher_notes = None
    return results


@router.get(
    "/{content_id}",
    response_model=InstructionalContentRead,
    summary="Get single instructional content item",
)
async def get_by_id(
    content_id: uuid.UUID,
    current_user: User | None = Depends(get_current_user_optional),
    service: InstructionalService = Depends(get_instructional_service),
) -> InstructionalContentRead:
    """Retrieve an instructional content item by ID. Non-teachers cannot view unpublished items or private teacher notes."""
    is_teacher = current_user is not None and current_user.role.value in ("teacher", "admin")
    content = await service.get_by_id(content_id=content_id)
    if not is_teacher and content.status.value not in ("approved", "published"):
        raise NotFoundError("Instructional content not found or not published.")
    if not is_teacher:
        content.teacher_notes = None
    return content


@router.patch(
    "/{content_id}",
    response_model=InstructionalContentRead,
    summary="Update instructional content (Teacher edit)",
)
async def update_instructional_content(
    content_id: uuid.UUID,
    update_in: InstructionalContentUpdate,
    current_user: Annotated[User, Depends(get_current_active_teacher)],
    service: InstructionalService = Depends(get_instructional_service),
) -> InstructionalContentRead:
    """Update title, summary, blocks, or notes while preserving teacher edits."""
    return await service.update(
        content_id=content_id,
        update_in=update_in,
        current_user=current_user,
    )


@router.post(
    "/{content_id}/approve",
    response_model=InstructionalContentRead,
    summary="Approve instructional content",
)
async def approve_instructional_content(
    content_id: uuid.UUID,
    current_user: Annotated[User, Depends(get_current_active_teacher)],
    service: InstructionalService = Depends(get_instructional_service),
) -> InstructionalContentRead:
    """Transition content from review_required/draft to approved."""
    return await service.approve(content_id=content_id, current_user=current_user)


@router.post(
    "/{content_id}/publish",
    response_model=InstructionalContentRead,
    summary="Publish instructional content for learners",
)
async def publish_instructional_content(
    content_id: uuid.UUID,
    current_user: Annotated[User, Depends(get_current_active_teacher)],
    service: InstructionalService = Depends(get_instructional_service),
) -> InstructionalContentRead:
    """Transition approved content to published."""
    return await service.publish(content_id=content_id, current_user=current_user)
