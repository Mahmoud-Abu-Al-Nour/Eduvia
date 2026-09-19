"""
Tests for Qdrant client vector operations and KnowledgeRetrievalService (Phase 9).
"""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from qdrant_client import QdrantClient, models

from app.knowledge.qdrant_client import EduViaQdrantClient
from app.knowledge.retrieval import KnowledgeRetrievalService
from app.knowledge.schemas import RetrievedChunk


class TestEduViaQdrantClient:
    """Test Qdrant client integration using an in-memory client."""

    @pytest.fixture
    def in_memory_qdrant_client(self) -> EduViaQdrantClient:
        eduvia_qdrant = EduViaQdrantClient()
        # Inject fast in-memory synchronous QdrantClient
        eduvia_qdrant._client = QdrantClient(":memory:")
        return eduvia_qdrant

    @pytest.mark.asyncio
    async def test_ensure_collections_exist(
        self, in_memory_qdrant_client: EduViaQdrantClient
    ) -> None:
        """ensure_collections_exist should create both eduvia_knowledge and eduvia_curriculum."""
        await in_memory_qdrant_client.ensure_collections_exist()
        collections = await in_memory_qdrant_client.list_collections()
        assert in_memory_qdrant_client.knowledge_collection in collections
        assert in_memory_qdrant_client.curriculum_collection in collections

    @pytest.mark.asyncio
    async def test_upsert_and_search_points(
        self, in_memory_qdrant_client: EduViaQdrantClient
    ) -> None:
        """upsert_points should store points, and search should retrieve matching payload."""
        col = in_memory_qdrant_client.knowledge_collection
        await in_memory_qdrant_client.ensure_collections_exist()

        test_points = [
            {
                "id": "11111111-1111-1111-1111-111111111111",
                "vector": [1.0] + [0.0] * 767,
                "payload": {
                    "document_title": "Teaching Strategies",
                    "section_title": "Step-by-Step",
                    "category": "strategy",
                    "content": "Break instructions into small steps.",
                },
            },
            {
                "id": "22222222-2222-2222-2222-222222222222",
                "vector": [0.0, 1.0] + [0.0] * 766,
                "payload": {
                    "document_title": "Activity Design",
                    "section_title": "Visual Cues",
                    "category": "activity_design",
                    "content": "Use high contrast visuals.",
                },
            },
        ]

        count = await in_memory_qdrant_client.upsert_points(col, test_points)
        assert count == 2

        # Search with vector close to point 1
        results = await in_memory_qdrant_client.search(
            collection_name=col,
            query_vector=[1.0] + [0.0] * 767,
            limit=1,
        )
        assert len(results) == 1
        assert results[0]["id"] == "11111111-1111-1111-1111-111111111111"
        assert results[0]["payload"]["category"] == "strategy"

    @pytest.mark.asyncio
    async def test_search_with_category_filter(
        self, in_memory_qdrant_client: EduViaQdrantClient
    ) -> None:
        """search should filter points by category metadata."""
        col = in_memory_qdrant_client.knowledge_collection
        await in_memory_qdrant_client.ensure_collections_exist()

        test_points = [
            {
                "id": "33333333-3333-3333-3333-333333333333",
                "vector": [0.5] * 768,
                "payload": {"category": "strategy", "content": "Strategy content"},
            },
            {
                "id": "44444444-4444-4444-4444-444444444444",
                "vector": [0.5] * 768,
                "payload": {"category": "accessibility", "content": "Accessibility content"},
            },
        ]
        await in_memory_qdrant_client.upsert_points(col, test_points)

        results = await in_memory_qdrant_client.search(
            collection_name=col,
            query_vector=[0.5] * 768,
            limit=5,
            category_filter="accessibility",
        )
        assert len(results) == 1
        assert results[0]["payload"]["category"] == "accessibility"

    @pytest.mark.asyncio
    async def test_search_handles_exception_gracefully(self) -> None:
        """Unreachable Qdrant should return an empty list without crashing."""
        broken_client = EduViaQdrantClient()
        broken_client._get_client = MagicMock(side_effect=RuntimeError("Connection refused"))

        results = await broken_client.search(
            collection_name="eduvia_knowledge",
            query_vector=[0.1] * 768,
        )
        assert results == []


class TestKnowledgeRetrievalService:
    """Test KnowledgeRetrievalService abstraction."""

    @pytest.mark.asyncio
    async def test_retrieve_pedagogical_context_returns_retrieved_chunks(self) -> None:
        """Service should map search matches into structured RetrievedChunk objects."""
        mock_qdrant = MagicMock(spec=EduViaQdrantClient)
        mock_qdrant.search = AsyncMock(
            return_value=[
                {
                    "id": "chunk-101",
                    "score": 0.92,
                    "payload": {
                        "document_title": "Teaching Strategies for SEN",
                        "source": "teaching_strategies.md",
                        "category": "strategy",
                        "content": "Provide immediate positive reinforcement for correct answers.",
                        "section_title": "Positive Reinforcement",
                        "chunk_index": 3,
                    },
                }
            ]
        )

        mock_orchestrator = MagicMock()
        mock_orchestrator.is_available = True
        mock_orchestrator.embed_text = AsyncMock(return_value=[[0.2] * 768])

        service = KnowledgeRetrievalService(qdrant=mock_qdrant, orchestrator=mock_orchestrator)
        chunks = await service.retrieve_pedagogical_context(
            query="Number recognition 1-10",
            strategy="positive_reinforcement",
            top_k=2,
        )

        assert len(chunks) == 1
        c = chunks[0]
        assert isinstance(c, RetrievedChunk)
        assert c.chunk_id == "chunk-101"
        assert c.document_title == "Teaching Strategies for SEN"
        assert c.score == 0.92
        assert "positive reinforcement" in c.content.lower()

    @pytest.mark.asyncio
    async def test_retrieve_empty_query_returns_empty(self) -> None:
        """Empty query and strategy should return empty list."""
        service = KnowledgeRetrievalService()
        chunks = await service.retrieve_pedagogical_context(query="", strategy=None)
        assert chunks == []
