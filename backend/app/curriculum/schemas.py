from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class LocalizedString(BaseModel):
    """Pragmatic localization structure: dict containing language codes as keys."""
    en: Optional[str] = None
    ar: Optional[str] = None
    
    # Allow arbitrary other languages if needed
    model_config = ConfigDict(extra="allow")


class CurriculumBase(BaseModel):
    title: Dict[str, str] = Field(..., description="Localized titles")
    description: Optional[Dict[str, str]] = None
    version: str = "1.0.0"
    is_active: bool = True

class CurriculumCreate(CurriculumBase):
    pass

class CurriculumUpdate(CurriculumBase):
    title: Optional[Dict[str, str]] = None

class CurriculumResponse(CurriculumBase):
    id: UUID
    created_by_id: Optional[UUID]

    model_config = ConfigDict(from_attributes=True)


class SubjectBase(BaseModel):
    title: Dict[str, str] = Field(..., description="Localized titles")
    description: Optional[Dict[str, str]] = None
    order_index: int = 0

class SubjectCreate(SubjectBase):
    pass

class SubjectUpdate(SubjectBase):
    title: Optional[Dict[str, str]] = None

class SubjectResponse(SubjectBase):
    id: UUID
    curriculum_id: UUID

    model_config = ConfigDict(from_attributes=True)


class UnitBase(BaseModel):
    title: Dict[str, str] = Field(..., description="Localized titles")
    description: Optional[Dict[str, str]] = None
    order_index: int = 0

class UnitCreate(UnitBase):
    pass

class UnitUpdate(UnitBase):
    title: Optional[Dict[str, str]] = None

class UnitResponse(UnitBase):
    id: UUID
    subject_id: UUID

    model_config = ConfigDict(from_attributes=True)


class LessonBase(BaseModel):
    title: Dict[str, str] = Field(..., description="Localized titles")
    description: Optional[Dict[str, str]] = None
    order_index: int = 0

class LessonCreate(LessonBase):
    pass

class LessonUpdate(LessonBase):
    title: Optional[Dict[str, str]] = None

class LessonResponse(LessonBase):
    id: UUID
    unit_id: UUID

    model_config = ConfigDict(from_attributes=True)


class AssessmentCriteria(BaseModel):
    minimum_accuracy: Optional[float] = Field(None, ge=0.0, le=1.0)
    maximum_assistance_level: Optional[int] = Field(None, ge=0, le=3)
    required_completion: Optional[bool] = None
    
    model_config = ConfigDict(extra="allow")


class LearningObjectiveBase(BaseModel):
    title: Dict[str, str] = Field(..., description="Localized titles")
    description: Optional[Dict[str, str]] = None
    difficulty_level: int = Field(1, ge=1, le=5)
    assessment_criteria: Optional[Dict] = None
    order_index: int = 0
    is_active: bool = True

class LearningObjectiveCreate(LearningObjectiveBase):
    pass

class LearningObjectiveUpdate(LearningObjectiveBase):
    title: Optional[Dict[str, str]] = None

class LearningObjectiveResponse(LearningObjectiveBase):
    id: UUID
    lesson_id: UUID
    prerequisites: List["LearningObjectiveResponse"] = []

    model_config = ConfigDict(from_attributes=True)


# Nested Responses for API
class LessonWithObjectives(LessonResponse):
    learning_objectives: List[LearningObjectiveResponse] = []

class UnitWithLessons(UnitResponse):
    lessons: List[LessonWithObjectives] = []

class SubjectWithUnits(SubjectResponse):
    units: List[UnitWithLessons] = []

class CurriculumWithSubjects(CurriculumResponse):
    subjects: List[SubjectWithUnits] = []
