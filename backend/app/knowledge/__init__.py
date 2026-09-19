"""Eduvia knowledge and RAG package."""
from app.knowledge.ingestion import KnowledgeIngestionService
from app.knowledge.models import KnowledgeChunk, KnowledgeDocument
from app.knowledge.qdrant_client import EduViaQdrantClient, get_qdrant_client
from app.knowledge.retrieval import KnowledgeRetrievalService, get_knowledge_retrieval_service
from app.knowledge.schemas import (
    KnowledgeCategory,
    KnowledgeChunkRead,
    KnowledgeDocumentCreate,
    KnowledgeDocumentRead,
    KnowledgeIngestionResult,
    KnowledgeSearchQuery,
    RetrievedChunk,
)

__all__ = [
    "EduViaQdrantClient",
    "get_qdrant_client",
    "KnowledgeDocument",
    "KnowledgeChunk",
    "KnowledgeCategory",
    "KnowledgeDocumentCreate",
    "KnowledgeDocumentRead",
    "KnowledgeChunkRead",
    "RetrievedChunk",
    "KnowledgeSearchQuery",
    "KnowledgeIngestionResult",
    "KnowledgeIngestionService",
    "KnowledgeRetrievalService",
    "get_knowledge_retrieval_service",
]
