"""
Eduvia — Knowledge Retrieval Service (Phase 9)

Provides clean semantic retrieval over pedagogical knowledge documents.
Decouples vector search from LLM generation and ensures robust source attribution.

Conforms to:
- docs/ai-architecture.md (RAG Knowledge Base)
- Eduvia Notes/03 - AI & Adaptive Learning/RAG Knowledge Base.md
"""
from __future__ import annotations

from typing import Any

import structlog

from app.ai.orchestrator.orchestrator import AIOrchestrator, get_ai_orchestrator
from app.core.config import settings
from app.knowledge.qdrant_client import EduViaQdrantClient, get_qdrant_client
from app.knowledge.schemas import RetrievedChunk

logger = structlog.get_logger(__name__)


class KnowledgeRetrievalService:
    """
    Retrieves evidence-based pedagogical context from Qdrant vector collections.
    """

    def __init__(
        self,
        qdrant: EduViaQdrantClient | None = None,
        orchestrator: AIOrchestrator | None = None,
    ) -> None:
        self.qdrant = qdrant or get_qdrant_client()
        self.orchestrator = orchestrator or get_ai_orchestrator()

    async def retrieve_pedagogical_context(
        self,
        query: str,
        strategy: str | None = None,
        category: str | None = None,
        top_k: int = 3,
        min_score: float = 0.0,
        collection_name: str | None = None,
    ) -> list[RetrievedChunk]:
        """
        Retrieve relevant pedagogical passages based on the objective query and strategy.

        Args:
            query: Objective title, description, or activity design query.
            strategy: Optional selected pedagogical strategy (e.g., 'scaffolding', 'step_by_step').
            category: Optional knowledge category filter ('strategy', 'activity_design', etc.).
            top_k: Maximum chunks to retrieve.
            min_score: Minimum similarity threshold.
            collection_name: Target collection (defaults to settings.QDRANT_COLLECTION_KNOWLEDGE).

        Returns:
            List of structured RetrievedChunk instances with source attribution.
        """
        if not query and not strategy:
            return []

        search_text = query
        if strategy:
            search_text = f"{query}\nTeaching Strategy: {strategy}"

        collection = collection_name or settings.QDRANT_COLLECTION_KNOWLEDGE

        try:
            # 1. Generate query embedding vector
            if self.orchestrator.is_available:
                vectors = await self.orchestrator.embed_text([search_text])
                if not vectors or not vectors[0]:
                    logger.warning("rag_retrieval_empty_query_embedding")
                    return []
                query_vector = vectors[0]
            else:
                # Deterministic fallback vector in offline/test environments
                query_vector = [0.1] * 768

            # 2. Search Qdrant vector database
            raw_matches = await self.qdrant.search(
                collection_name=collection,
                query_vector=query_vector,
                limit=top_k,
                score_threshold=min_score,
                category_filter=category,
            )

            # 3. Format matches into structured RetrievedChunk items
            chunks: list[RetrievedChunk] = []
            for match in raw_matches:
                payload: dict[str, Any] = match.get("payload", {})
                content = payload.get("content", "").strip()
                if not content:
                    continue

                chunk = RetrievedChunk(
                    chunk_id=match.get("id", ""),
                    document_title=payload.get("document_title", "Pedagogical Guide"),
                    source=payload.get("source", "unknown_source.md"),
                    category=payload.get("category", "strategy"),
                    content=content,
                    score=round(match.get("score", 0.0), 4),
                    metadata={
                        "section_title": payload.get("section_title"),
                        "chunk_index": payload.get("chunk_index"),
                    },
                )
                chunks.append(chunk)

            logger.info(
                "pedagogical_context_retrieved",
                query=query[:60],
                strategy=strategy,
                chunks_found=len(chunks),
            )
            return chunks

        except Exception as e:
            # Graceful degradation: never fail user request path if retrieval fails
            logger.warning("rag_retrieval_failed_gracefully", error=str(e))
            return []


_RETRIEVAL_SERVICE_INSTANCE: KnowledgeRetrievalService | None = None


def get_knowledge_retrieval_service() -> KnowledgeRetrievalService:
    """Singleton getter for FastAPI dependency injection."""
    global _RETRIEVAL_SERVICE_INSTANCE
    if _RETRIEVAL_SERVICE_INSTANCE is None:
        _RETRIEVAL_SERVICE_INSTANCE = KnowledgeRetrievalService()
    return _RETRIEVAL_SERVICE_INSTANCE
