"""
Eduvia — Knowledge Base SQLAlchemy ORM Models (Phase 9)

Implements persistent relational metadata for RAG knowledge sources
conforming strictly to docs/data-model.md (Knowledge Entities).
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import EduviaBase


class KnowledgeDocument(EduviaBase):
    """
    Metadata representation of an ingested knowledge source document.
    """
    __tablename__ = "knowledge_documents"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    source: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False, default="strategy", index=True)
    chunk_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    embedded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    chunks: Mapped[list[KnowledgeChunk]] = relationship(
        back_populates="document",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="KnowledgeChunk.chunk_index",
    )


class KnowledgeChunk(EduviaBase):
    """
    Relational record for an individual chunk linked to its vector in Qdrant.
    """
    __tablename__ = "knowledge_chunks"

    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("knowledge_documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    qdrant_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    metadata_: Mapped[dict[str, Any] | None] = mapped_column("metadata", JSONB, nullable=True)

    # Relationships
    document: Mapped[KnowledgeDocument] = relationship(back_populates="chunks")
