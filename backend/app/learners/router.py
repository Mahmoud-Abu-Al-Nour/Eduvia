"""
Eduvia -- Learners API Router (Phase 3)

REST endpoints for learner domain entity and learner profile management.
Enforces teacher/admin authorization and protects learner privacy.
"""
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import SessionDep, get_current_user
from app.learners.schemas import (
    LearnerCreate,
    LearnerDetailResponse,
    LearnerObservationCreate,
    LearnerResponse,
    LearnerUpdate,
)
from app.learners.service import LearnerService
from app.users.models import User

router = APIRouter(prefix="/learners", tags=["learners"])


def get_learner_service(session: SessionDep) -> LearnerService:
    return LearnerService(session)


@router.get("", response_model=list[LearnerResponse])
async def list_learners(
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[LearnerService, Depends(get_learner_service)],
) -> list[LearnerResponse]:
    """
    List learners.
    Teachers receive their assigned learners.
    Admins receive all registered learners.
    """
    is_admin = current_user.role.value == "admin"
    return await service.list_learners(teacher_id=current_user.id, is_admin=is_admin)


@router.post("", response_model=LearnerDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_learner(
    data: LearnerCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[LearnerService, Depends(get_learner_service)],
) -> LearnerDetailResponse:
    """
    Create a new learner and initialize their pedagogical profile.
    Only authenticated teachers and admins can create learners.
    """
    learner = await service.create(data, teacher_id=current_user.id)
    return learner


@router.get("/{learner_id}", response_model=LearnerDetailResponse)
async def get_learner(
    learner_id: uuid.UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[LearnerService, Depends(get_learner_service)],
) -> LearnerDetailResponse:
    """
    Retrieve full learner details and pedagogical profile.
    """
    is_admin = current_user.role.value == "admin"
    learner = await service.get_by_id(learner_id, teacher_id=current_user.id, is_admin=is_admin)
    if not learner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learner not found or access unauthorized",
        )
    return learner


@router.patch("/{learner_id}", response_model=LearnerDetailResponse)
async def update_learner(
    learner_id: uuid.UUID,
    data: LearnerUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[LearnerService, Depends(get_learner_service)],
) -> LearnerDetailResponse:
    """
    Update learner metadata or teacher-provided profile fields.
    Preserves teacher overrides and constraints.
    """
    is_admin = current_user.role.value == "admin"
    updated = await service.update(
        learner_id, data, teacher_id=current_user.id, is_admin=is_admin
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learner not found or update unauthorized",
        )
    return updated


@router.delete("/{learner_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_learner(
    learner_id: uuid.UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[LearnerService, Depends(get_learner_service)],
) -> None:
    """
    Delete a learner and cascade delete their profile.
    """
    is_admin = current_user.role.value == "admin"
    success = await service.delete(learner_id, teacher_id=current_user.id, is_admin=is_admin)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learner not found or deletion unauthorized",
        )


@router.post("/{learner_id}/observations", status_code=status.HTTP_201_CREATED)
async def add_observation(
    learner_id: uuid.UUID,
    observation: LearnerObservationCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[LearnerService, Depends(get_learner_service)],
) -> dict:
    """
    Record an educational learning pattern observation or evidence item.
    """
    is_admin = current_user.role.value == "admin"
    obs_item = await service.add_observation(
        learner_id, observation, teacher_id=current_user.id, is_admin=is_admin
    )
    if not obs_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learner not found or observation recording unauthorized",
        )
    return obs_item
