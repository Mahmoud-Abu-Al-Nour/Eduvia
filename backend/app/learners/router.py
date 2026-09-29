"""
Eduvia -- Learners API Router (Phase 3 & RBAC Extension)

REST endpoints for learner domain entity and learner profile management.
Enforces role-based permissions, scope isolation, and IDOR protection.
"""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import (
    SessionDep,
    get_current_user,
    require_permission,
)
from app.auth.permissions import Permission, get_user_role
from app.learners.models import Learner
from app.learners.schemas import (
    LearnerCreate,
    LearnerDetailResponse,
    LearnerObservationCreate,
    LearnerResponse,
    LearnerUpdate,
)
from app.learners.service import LearnerService
from app.users.models import User, UserRole

router = APIRouter(prefix="/learners", tags=["learners"])


def get_learner_service(session: SessionDep) -> LearnerService:
    return LearnerService(session)


def _sanitize_for_learner(learner: Learner, current_user: User) -> LearnerDetailResponse:
    """Sanitize learner profile to prevent leakage of teacher private notes to learners."""
    resp = LearnerDetailResponse.model_validate(learner)
    role = get_user_role(current_user)
    if role == UserRole.learner and resp.profile:
        resp.profile.teacher_notes = None
        resp.profile.teacher_constraints = {}
        resp.profile.teacher_overrides = {}
    return resp


@router.get("/me", response_model=LearnerDetailResponse)
async def get_current_learner_profile(
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[LearnerService, Depends(get_learner_service)],
) -> LearnerDetailResponse:
    """
    Retrieve authenticated learner's own profile.
    Only accessible by learners or teachers/admins with linked learner entity.
    """
    learner = await service.get_by_user_id(current_user.id)
    if not learner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No learner profile linked to the current user account.",
        )
    return _sanitize_for_learner(learner, current_user)


@router.get("", response_model=list[LearnerResponse])
async def list_learners(
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[LearnerService, Depends(get_learner_service)],
) -> list[LearnerResponse]:
    """
    List learners according to requester scope:
    - Teachers receive only their assigned learners.
    - Admins receive all registered learners.
    - Learners receive only their own learner record.
    """
    return await service.list_learners(current_user=current_user)


@router.post("", response_model=LearnerDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_learner(
    data: LearnerCreate,
    current_user: Annotated[User, Depends(require_permission(Permission.LEARNERS_CREATE))],
    service: Annotated[LearnerService, Depends(get_learner_service)],
) -> LearnerDetailResponse:
    """
    Create a new learner and initialize their pedagogical profile.
    Only authenticated teachers and admins can create learners.
    """
    role = get_user_role(current_user)
    teacher_id = current_user.id if role == UserRole.teacher else None
    learner = await service.create(data, teacher_id=teacher_id)
    return LearnerDetailResponse.model_validate(learner)


@router.get("/{learner_id}", response_model=LearnerDetailResponse)
async def get_learner(
    learner_id: uuid.UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[LearnerService, Depends(get_learner_service)],
) -> LearnerDetailResponse:
    """
    Retrieve full learner details and pedagogical profile.
    Enforces server-side IDOR protection across teachers and learners.
    """
    learner = await service.get_by_id(learner_id, current_user=current_user)
    if not learner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learner not found or access unauthorized",
        )
    return _sanitize_for_learner(learner, current_user)


@router.patch("/{learner_id}", response_model=LearnerDetailResponse)
async def update_learner(
    learner_id: uuid.UUID,
    data: LearnerUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[LearnerService, Depends(get_learner_service)],
) -> LearnerDetailResponse:
    """
    Update learner metadata or profile fields.
    Teachers/Admins can edit pedagogical fields. Learners can only update allowed preferences.
    """
    updated = await service.update(learner_id, data, current_user=current_user)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learner not found or update unauthorized",
        )
    return _sanitize_for_learner(updated, current_user)


@router.delete("/{learner_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_learner(
    learner_id: uuid.UUID,
    current_user: Annotated[User, Depends(require_permission(Permission.LEARNERS_MANAGE_ASSIGNED))],
    service: Annotated[LearnerService, Depends(get_learner_service)],
) -> None:
    """
    Delete a learner and cascade delete their profile.
    Accessible only to authorized teachers and administrators.
    """
    success = await service.delete(learner_id, current_user=current_user)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learner not found or deletion unauthorized",
        )


@router.post("/{learner_id}/observations", status_code=status.HTTP_201_CREATED)
async def add_observation(
    learner_id: uuid.UUID,
    observation: LearnerObservationCreate,
    current_user: Annotated[User, Depends(require_permission(Permission.LEARNERS_MANAGE_ASSIGNED))],
    service: Annotated[LearnerService, Depends(get_learner_service)],
) -> dict:
    """
    Record an educational learning pattern observation or evidence item.
    Only teachers and admins can record observations.
    """
    obs_item = await service.add_observation(learner_id, observation, current_user=current_user)
    if not obs_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learner not found or observation recording unauthorized",
        )
    return obs_item
