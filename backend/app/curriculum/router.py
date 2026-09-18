import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_active_admin, get_current_user
from app.curriculum.schemas import (
    CurriculumCreate,
    CurriculumResponse,
    CurriculumWithSubjects,
    LearningObjectiveResponse,
    LessonWithObjectives,
    SubjectWithUnits,
    UnitWithLessons,
)
from app.curriculum.service import CurriculumService
from app.database.session import get_db_session
from app.users.models import User

router = APIRouter(prefix="/curricula", tags=["curriculum"])

async def get_curriculum_service(db: AsyncSession = Depends(get_db_session)) -> CurriculumService:
    return CurriculumService(db)


@router.get("", response_model=List[CurriculumResponse])
async def list_curricula(
    service: CurriculumService = Depends(get_curriculum_service),
    current_user: User = Depends(get_current_user),
):
    """List all curricula. Teachers and admins can view."""
    return await service.get_all()


@router.post("", response_model=CurriculumResponse, status_code=status.HTTP_201_CREATED)
async def create_curriculum(
    data: CurriculumCreate,
    service: CurriculumService = Depends(get_curriculum_service),
    current_user: User = Depends(get_current_active_admin),
):
    """Create a new curriculum. Admin only."""
    return await service.create(data, user_id=current_user.id)


@router.get("/{curriculum_id}", response_model=CurriculumWithSubjects)
async def get_curriculum(
    curriculum_id: uuid.UUID,
    service: CurriculumService = Depends(get_curriculum_service),
    current_user: User = Depends(get_current_user),
):
    """Get a curriculum with its full hierarchy."""
    curr = await service.get_by_id(curriculum_id)
    if not curr:
        raise HTTPException(status_code=404, detail="Curriculum not found")
    return curr


@router.get("/subjects/{subject_id}", response_model=SubjectWithUnits)
async def get_subject(
    subject_id: uuid.UUID,
    service: CurriculumService = Depends(get_curriculum_service),
    current_user: User = Depends(get_current_user),
):
    subj = await service.get_subject(subject_id)
    if not subj:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subj


@router.get("/units/{unit_id}", response_model=UnitWithLessons)
async def get_unit(
    unit_id: uuid.UUID,
    service: CurriculumService = Depends(get_curriculum_service),
    current_user: User = Depends(get_current_user),
):
    unit = await service.get_unit(unit_id)
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    return unit


@router.get("/lessons/{lesson_id}", response_model=LessonWithObjectives)
async def get_lesson(
    lesson_id: uuid.UUID,
    service: CurriculumService = Depends(get_curriculum_service),
    current_user: User = Depends(get_current_user),
):
    lesson = await service.get_lesson(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.get("/learning-objectives/{objective_id}", response_model=LearningObjectiveResponse)
async def get_learning_objective(
    objective_id: uuid.UUID,
    service: CurriculumService = Depends(get_curriculum_service),
    current_user: User = Depends(get_current_user),
):
    obj = await service.get_learning_objective(objective_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Learning objective not found")
    return obj
