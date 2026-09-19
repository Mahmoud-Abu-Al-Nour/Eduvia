import uuid
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import EduviaBase
from app.users.models import User

# Many-to-Many Association Table for Prerequisites
objective_prerequisites = Table(
    "objective_prerequisites",
    EduviaBase.metadata,
    Column("objective_id", UUID(as_uuid=True), ForeignKey("learning_objectives.id", ondelete="CASCADE"), primary_key=True),
    Column("prerequisite_id", UUID(as_uuid=True), ForeignKey("learning_objectives.id", ondelete="CASCADE"), primary_key=True),
)


class Curriculum(EduviaBase):
    __tablename__ = "curricula"

    title: Mapped[dict] = mapped_column(JSONB, nullable=False)
    description: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    version: Mapped[str] = mapped_column(String, default="1.0.0")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_by_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    # Relationships
    created_by: Mapped[Optional["User"]] = relationship(lazy="selectin")
    subjects: Mapped[list["Subject"]] = relationship(
        back_populates="curriculum", cascade="all, delete-orphan", lazy="selectin", order_by="Subject.order_index"
    )


class Subject(EduviaBase):
    __tablename__ = "subjects"

    curriculum_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("curricula.id", ondelete="CASCADE")
    )
    title: Mapped[dict] = mapped_column(JSONB, nullable=False)
    description: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    curriculum: Mapped["Curriculum"] = relationship(back_populates="subjects")
    units: Mapped[list["Unit"]] = relationship(
        back_populates="subject", cascade="all, delete-orphan", lazy="selectin", order_by="Unit.order_index"
    )


class Unit(EduviaBase):
    __tablename__ = "units"

    subject_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("subjects.id", ondelete="CASCADE")
    )
    title: Mapped[dict] = mapped_column(JSONB, nullable=False)
    description: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    subject: Mapped["Subject"] = relationship(back_populates="units")
    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="unit", cascade="all, delete-orphan", lazy="selectin", order_by="Lesson.order_index"
    )


class Lesson(EduviaBase):
    __tablename__ = "lessons"

    unit_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("units.id", ondelete="CASCADE")
    )
    title: Mapped[dict] = mapped_column(JSONB, nullable=False)
    description: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    unit: Mapped["Unit"] = relationship(back_populates="lessons")
    learning_objectives: Mapped[list["LearningObjective"]] = relationship(
        back_populates="lesson", cascade="all, delete-orphan", lazy="selectin", order_by="LearningObjective.order_index"
    )


class LearningObjective(EduviaBase):
    __tablename__ = "learning_objectives"

    lesson_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("lessons.id", ondelete="CASCADE")
    )
    title: Mapped[dict] = mapped_column(JSONB, nullable=False)
    description: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    # 1 (Beginner) to 5 (Mastery)
    difficulty_level: Mapped[int] = mapped_column(Integer, default=1)

    # e.g., {"minimum_accuracy": 0.80, "maximum_assistance_level": 1, "required_completion": true}
    assessment_criteria: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    order_index: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    lesson: Mapped["Lesson"] = relationship(back_populates="learning_objectives")

    # Self-referencing many-to-many relationship for prerequisites
    prerequisites: Mapped[list["LearningObjective"]] = relationship(
        "LearningObjective",
        secondary=objective_prerequisites,
        primaryjoin="LearningObjective.id == objective_prerequisites.c.objective_id",
        secondaryjoin="LearningObjective.id == objective_prerequisites.c.prerequisite_id",
        backref="required_by",
        lazy="selectin",
    )
