"""
Eduvia — SQLAlchemy Declarative Base

All ORM models inherit from EduviaBase which includes
common audit columns (id, created_at, updated_at).
"""
import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class EduviaBase(DeclarativeBase):
    """
    Base class for all Eduvia ORM models.

    Provides:
    - UUID primary key
    - created_at timestamp (auto-set on insert)
    - updated_at timestamp (auto-set on insert and update)
    """

    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id}>"
