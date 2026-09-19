"""
Eduvia — Knowledge Base Pydantic Schemas (Phase 9)

Defines data transfer models for knowledge documents, chunk vectors,
semantic search queries, and retrieved pedagogical passages.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class KnowledgeCategory(StrEnum):
    """Supported categories of educational knowledge."""
    STRATEGY = "strategy"
    CURRICULUM = "curriculum"
    ACCESSIBILITY = "accessibility"
    ACTIVITY_DESIGN = "activity_design"


class KnowledgeChunkBase(BaseModel):
    content: str
    chunk_index: int = 0
    qdrant_id: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class KnowledgeChunkRead(KnowledgeChunkBase):
    id: uuid.UUID
    document_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class KnowledgeDocumentBase(BaseModel):
    title: str
    source: str
    category: KnowledgeCategory | str = KnowledgeCategory.STRATEGY


class KnowledgeDocumentCreate(KnowledgeDocumentBase):
    pass


class KnowledgeDocumentRead(KnowledgeDocumentBase):
    id: uuid.UUID
    chunk_count: int = 0
    embedded_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
    chunks: list[KnowledgeChunkRead] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class RetrievedChunk(BaseModel):
    """
    Structured passage returned from semantic similarity search.

    Preserves source grounding and citations for AI generation.
    """
    chunk_id: str
    document_title: str
    source: str
    category: str
    content: str
    score: float = 0.0
    metadata: dict[str, Any] = Field(default_factory=dict)


class KnowledgeSearchQuery(BaseModel):
    """Request query model for knowledge retrieval."""
    query: str
    strategy: str | None = None
    category: KnowledgeCategory | str | None = None
    top_k: int = 3
    min_score: float = 0.0


class KnowledgeIngestionResult(BaseModel):
    """Summary of knowledge ingestion batch execution."""
    total_documents_scanned: int = 0
    total_documents_ingested: int = 0
    total_chunks_indexed: int = 0
    collections_updated: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
