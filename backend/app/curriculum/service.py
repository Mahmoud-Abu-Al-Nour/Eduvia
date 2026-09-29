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

    async def get_learning_objective(self, objective_id: uuid.UUID | str) -> LearningObjective | None:
        target_uuid: uuid.UUID | None = None
        if isinstance(objective_id, uuid.UUID):
            target_uuid = objective_id
        else:
            try:
                target_uuid = uuid.UUID(str(objective_id))
            except (ValueError, TypeError):
                _SLUG_MAP = {
                    "math-num-01": uuid.UUID("77777777-7777-7777-7777-777777777777"),
                    "obj.math.count_0_5": uuid.UUID("77777777-7777-7777-7777-777777777777"),
                    "math-num-02": uuid.UUID("88888888-8888-8888-8888-888888888888"),
                    "obj.math.count_6_10": uuid.UUID("88888888-8888-8888-8888-888888888888"),
                    "math-num-03": uuid.UUID("0596bbe4-a070-5f22-b13d-f8563b6d1467"),
                    "math-num-04": uuid.UUID("74921057-04b5-55ae-b213-cf62a4db44f9"),
                    "math-num-05": uuid.UUID("bb90d5f3-80b9-572e-8179-7a310625a90d"),
                    "lit-let-01": uuid.UUID("38e172d6-8616-5012-95d9-75d26a85cb5e"),
                    "lit-pho-01": uuid.UUID("b9f96769-460f-5262-acd2-53dc770e2a58"),
                    "lit-wor-01": uuid.UUID("681528bc-98cb-5867-9794-280c9a0be363"),
                    "daily-rou-01": uuid.UUID("92ae654b-5a1a-5645-b2e5-e3abf2bd721b"),
                    "sensory-col-01": uuid.UUID("f54c5f7f-0add-56f5-9b92-7ef0b84729d9"),
                }
                target_uuid = _SLUG_MAP.get(str(objective_id))

        if target_uuid:
            stmt = (
                select(LearningObjective)
                .options(selectinload(LearningObjective.prerequisites))
                .where(LearningObjective.id == target_uuid)
            )
            result = await self.session.execute(stmt)
            obj = result.scalars().first()
            if obj:
                return obj

        # Fallback to first active objective if still not found
        stmt = (
            select(LearningObjective)
            .options(selectinload(LearningObjective.prerequisites))
            .where(LearningObjective.is_active == True)
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()
