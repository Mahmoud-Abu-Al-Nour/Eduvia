from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class LocalizedString(BaseModel):
    """Pragmatic localization structure: dict containing language codes as keys."""
    en: str | None = None
    ar: str | None = None

    # Allow arbitrary other languages if needed
    model_config = ConfigDict(extra="allow")


class CurriculumBase(BaseModel):
    title: dict[str, str] = Field(..., description="Localized titles")
    description: dict[str, str] | None = None
    version: str = "1.0.0"
    is_active: bool = True

class CurriculumCreate(CurriculumBase):
    pass

class CurriculumUpdate(CurriculumBase):
    title: dict[str, str] | None = None

class CurriculumResponse(CurriculumBase):
    id: UUID
    created_by_id: UUID | None

    model_config = ConfigDict(from_attributes=True)


class SubjectBase(BaseModel):
    title: dict[str, str] = Field(..., description="Localized titles")
    description: dict[str, str] | None = None
    order_index: int = 0

class SubjectCreate(SubjectBase):
    pass

class SubjectUpdate(SubjectBase):
    title: dict[str, str] | None = None

class SubjectResponse(SubjectBase):
    id: UUID
    curriculum_id: UUID

    model_config = ConfigDict(from_attributes=True)


class UnitBase(BaseModel):
    title: dict[str, str] = Field(..., description="Localized titles")
    description: dict[str, str] | None = None
    order_index: int = 0

class UnitCreate(UnitBase):
    pass

class UnitUpdate(UnitBase):
    title: dict[str, str] | None = None

class UnitResponse(UnitBase):
    id: UUID
    subject_id: UUID

    model_config = ConfigDict(from_attributes=True)


class LessonBase(BaseModel):
    title: dict[str, str] = Field(..., description="Localized titles")
    description: dict[str, str] | None = None
    order_index: int = 0

class LessonCreate(LessonBase):
    pass

class LessonUpdate(LessonBase):
    title: dict[str, str] | None = None

class LessonResponse(LessonBase):
    id: UUID
    unit_id: UUID

    model_config = ConfigDict(from_attributes=True)


class AssessmentCriteria(BaseModel):
    minimum_accuracy: float | None = Field(None, ge=0.0, le=1.0)
    maximum_assistance_level: int | None = Field(None, ge=0, le=3)
    required_completion: bool | None = None

    model_config = ConfigDict(extra="allow")


class LearningObjectiveBase(BaseModel):
    title: dict[str, str] = Field(..., description="Localized titles")
    description: dict[str, str] | None = None
    difficulty_level: int = Field(1, ge=1, le=5)
    assessment_criteria: dict | None = None
    order_index: int = 0
    is_active: bool = True

class LearningObjectiveCreate(LearningObjectiveBase):
    pass

class LearningObjectiveUpdate(LearningObjectiveBase):
    title: dict[str, str] | None = None

class LearningObjectiveResponse(LearningObjectiveBase):
    id: UUID
    lesson_id: UUID
    prerequisites: list["LearningObjectiveResponse"] = []

    model_config = ConfigDict(from_attributes=True)


# Nested Responses for API
class LessonWithObjectives(LessonResponse):
    learning_objectives: list[LearningObjectiveResponse] = []

class UnitWithLessons(UnitResponse):
    lessons: list[LessonWithObjectives] = []

class SubjectWithUnits(SubjectResponse):
    units: list[UnitWithLessons] = []

class CurriculumWithSubjects(CurriculumResponse):
    subjects: list[SubjectWithUnits] = []
