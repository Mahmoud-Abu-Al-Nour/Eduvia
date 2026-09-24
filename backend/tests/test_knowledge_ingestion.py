"""
Tests for KnowledgeIngestionService (Phase 9).
"""
from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest
from qdrant_client import QdrantClient

from app.knowledge.ingestion import KnowledgeIngestionService
from app.knowledge.qdrant_client import EduViaQdrantClient


class TestKnowledgeIngestionService:
    """Test markdown parsing, semantic chunking, and source directory ingestion."""

    @pytest.fixture
    def mock_ingestion_service(self) -> KnowledgeIngestionService:
        eduvia_qdrant = EduViaQdrantClient()
        eduvia_qdrant._client = QdrantClient(":memory:")

        mock_orchestrator = MagicMock()
        mock_orchestrator.is_available = True
        # Return dummy 768-dim vectors
        mock_orchestrator.embed_text = AsyncMock(side_effect=lambda texts: [[0.1] * 768 for _ in texts])

        return KnowledgeIngestionService(qdrant=eduvia_qdrant, orchestrator=mock_orchestrator)

    def test_chunk_markdown_splits_sections_on_headings(self) -> None:
        """chunk_markdown should split by ## headings and preserve titles."""
        sample_md = (
            "# Sensory and Learning Guidelines\n\n"
            "## Visual Cues\n"
            "Use clear, high-contrast symbols.\n\n"
            "## Auditory Prompts\n"
            "Keep verbal cues under 5 words.\n"
        )

        chunks = KnowledgeIngestionService.chunk_markdown(
            content=sample_md,
            source_name="sensory_guidelines.md",
            category="accessibility",
        )

        assert len(chunks) == 2
        assert chunks[0]["document_title"] == "Sensory and Learning Guidelines"
        assert chunks[0]["section_title"] == "Visual Cues"
        assert "high-contrast symbols" in chunks[0]["content"]
        assert chunks[0]["category"] == "accessibility"
        assert chunks[0]["chunk_index"] == 0

        assert chunks[1]["section_title"] == "Auditory Prompts"
        assert chunks[1]["chunk_index"] == 1

    def test_chunk_markdown_deterministic_point_ids(self) -> None:
        """Chunking the same source text should produce identical deterministic UUIDs."""
        sample_md = "## Scaffolding\nProvide structured support."
        chunks_1 = KnowledgeIngestionService.chunk_markdown(sample_md, "scaffolding.md")
        chunks_2 = KnowledgeIngestionService.chunk_markdown(sample_md, "scaffolding.md")

        assert chunks_1[0]["id"] == chunks_2[0]["id"]

    @pytest.mark.asyncio
    async def test_ingest_file_stores_points_in_qdrant(
        self, mock_ingestion_service: KnowledgeIngestionService, tmp_path: Path
    ) -> None:
        """ingest_file should parse a file, generate embeddings, and store points in Qdrant."""
        test_file = tmp_path / "strategies" / "sample.md"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text(
            "# Step-by-Step Guide\n\n## Step One\nBreak down the task.\n\n## Step Two\nReward completion.\n",
            encoding="utf-8",
        )

        points = await mock_ingestion_service.ingest_file(test_file)
        assert len(points) == 2
        assert points[0]["payload"]["document_title"] == "Step-by-Step Guide"

        # Verify point can be retrieved from in-memory Qdrant
        matches = await mock_ingestion_service.qdrant.search(
            collection_name=mock_ingestion_service.qdrant.knowledge_collection,
            query_vector=[0.1] * 768,
            limit=5,
        )
        assert len(matches) == 2

    @pytest.mark.asyncio
    async def test_ingest_sources_directory_scans_and_indexes(
        self, mock_ingestion_service: KnowledgeIngestionService, tmp_path: Path
    ) -> None:
        """ingest_sources_directory should scan directory, process files, and report counts."""
        dir1 = tmp_path / "strategies"
        dir1.mkdir(parents=True, exist_ok=True)
        (dir1 / "test1.md").write_text("## Strategy A\nContent A", encoding="utf-8")
        (dir1 / "test2.md").write_text("## Strategy B\nContent B", encoding="utf-8")

        result = await mock_ingestion_service.ingest_sources_directory(sources_dir=tmp_path)
        assert result.total_documents_scanned == 2
        assert result.total_documents_ingested == 2
        assert result.total_chunks_indexed == 2
        assert len(result.errors) == 0

    @pytest.mark.asyncio
    async def test_ingest_sources_handles_missing_directory(
        self, mock_ingestion_service: KnowledgeIngestionService, tmp_path: Path
    ) -> None:
        """Missing directory should return result with recorded error."""
        non_existent = tmp_path / "does_not_exist"
        result = await mock_ingestion_service.ingest_sources_directory(sources_dir=non_existent)
        assert result.total_documents_scanned == 0
        assert len(result.errors) == 1
        assert "not found" in result.errors[0]

    @pytest.mark.asyncio
    async def test_ingest_expanded_knowledge_base_sources(
        self, mock_ingestion_service: KnowledgeIngestionService
    ) -> None:
        """Verify the actual repository knowledge_base/sources parses and indexes all categories."""
        kb_path = Path(__file__).resolve().parent.parent.parent / "knowledge_base" / "sources"
        if not kb_path.exists():
            pytest.skip("knowledge_base/sources directory not found relative to test")

        result = await mock_ingestion_service.ingest_sources_directory(sources_dir=kb_path)
        assert result.total_documents_scanned >= 15
        assert result.total_documents_ingested >= 15
        assert result.total_chunks_indexed >= 40
        assert len(result.errors) == 0

