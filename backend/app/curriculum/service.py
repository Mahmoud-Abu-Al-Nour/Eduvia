import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.curriculum.models import Curriculum, LearningObjective, Lesson, Subject, Unit
from app.curriculum.schemas import CurriculumCreate, CurriculumUpdate


class CurriculumService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Curriculum]:
        stmt = select(Curriculum).order_by(Curriculum.created_at)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, curriculum_id: uuid.UUID) -> Curriculum | None:
        stmt = (
            select(Curriculum)
            .options(
                selectinload(Curriculum.subjects).selectinload(Subject.units).selectinload(Unit.lessons).selectinload(Lesson.learning_objectives)
            )
            .where(Curriculum.id == curriculum_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def create(self, data: CurriculumCreate, user_id: uuid.UUID | None = None) -> Curriculum:
        obj = Curriculum(**data.model_dump(), created_by_id=user_id)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, curriculum_id: uuid.UUID, data: CurriculumUpdate) -> Curriculum | None:
        obj = await self.session.get(Curriculum, curriculum_id)
        if not obj:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(obj, field, value)

        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get_subject(self, subject_id: uuid.UUID) -> Subject | None:
        stmt = (
            select(Subject)
            .options(
                selectinload(Subject.units).selectinload(Unit.lessons).selectinload(Lesson.learning_objectives)
            )
            .where(Subject.id == subject_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_unit(self, unit_id: uuid.UUID) -> Unit | None:
        stmt = (
            select(Unit)
            .options(
                selectinload(Unit.lessons).selectinload(Lesson.learning_objectives)
            )
            .where(Unit.id == unit_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_lesson(self, lesson_id: uuid.UUID) -> Lesson | None:
        stmt = (
            select(Lesson)
            .options(
                selectinload(Lesson.learning_objectives).selectinload(LearningObjective.prerequisites)
            )
            .where(Lesson.id == lesson_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_learning_objective(self, objective_id: uuid.UUID) -> LearningObjective | None:
        stmt = (
            select(LearningObjective)
            .options(selectinload(LearningObjective.prerequisites))
            .where(LearningObjective.id == objective_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()
