"""
Eduvia — Knowledge Ingestion Service (Phase 9)

Implements the deterministic RAG ingestion pipeline:
Source Documents → Parsing → Semantic Chunking → Metadata → Embeddings → Qdrant.

Conforms strictly to:
- knowledge_base/README.md
- docs/ai-architecture.md (RAG Knowledge Base)
- docs/data-model.md (Knowledge Entities)
"""
from __future__ import annotations

import re
import uuid
from pathlib import Path
from typing import Any

import structlog

from app.ai.orchestrator.orchestrator import AIOrchestrator, get_ai_orchestrator
from app.core.config import settings
from app.knowledge.qdrant_client import EduViaQdrantClient, get_qdrant_client
from app.knowledge.schemas import KnowledgeCategory, KnowledgeIngestionResult

logger = structlog.get_logger(__name__)

# Fixed namespace UUID for deterministic chunk point IDs
EDUVIA_KNOWLEDGE_NAMESPACE = uuid.UUID("11111111-2222-3333-4444-555555555555")


class KnowledgeIngestionService:
    """
    Ingests pedagogical source documents into Qdrant vector collections.
    """

    def __init__(
        self,
        qdrant: EduViaQdrantClient | None = None,
        orchestrator: AIOrchestrator | None = None,
    ) -> None:
        self.qdrant = qdrant or get_qdrant_client()
        self.orchestrator = orchestrator or get_ai_orchestrator()

    @staticmethod
    def chunk_markdown(
        content: str,
        source_name: str,
        category: str = "strategy",
    ) -> list[dict[str, Any]]:
        """
        Parse and semantically chunk a markdown document.

        Splits on markdown headings (`## `) to preserve logical pedagogical units
        (e.g., Step-by-Step, Scaffolding, Positive Reinforcement).
        """
        lines = content.splitlines()
        doc_title = source_name

        # Extract top # Title if present
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("# ") and not stripped.startswith("## "):
                doc_title = stripped.lstrip("# ").strip()
                break

        # Split content into sections based on ## headers
        sections: list[tuple[str, str]] = []
        current_section_title = doc_title
        current_lines: list[str] = []

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("## "):
                if current_lines:
                    # Ignore preamble if it only contains the document title
                    body_lines = [
                        l for l in current_lines
                        if not (l.strip().startswith("# ") and not l.strip().startswith("## "))
                    ]
                    body = "\n".join(body_lines).strip()
                    if body:
                        sections.append((current_section_title, body))
                current_section_title = stripped.lstrip("# ").strip()
                current_lines = [line]
            else:
                current_lines.append(line)

        if current_lines:
            body = "\n".join(current_lines).strip()
            if body:
                sections.append((current_section_title, body))

        # If no ## headings were found, chunk the entire text as a single section
        if not sections and content.strip():
            sections.append((doc_title, content.strip()))

        chunks: list[dict[str, Any]] = []
        chunk_idx = 0

        for section_title, body in sections:
            # If a section is very long (> 1200 characters), break into paragraphs
            if len(body) > 1200:
                paragraphs = re.split(r"\n\s*\n", body)
                sub_body = ""
                for p in paragraphs:
                    if len(sub_body) + len(p) > 1000 and sub_body.strip():
                        # Produce chunk
                        point_id = str(
                            uuid.uuid5(
                                EDUVIA_KNOWLEDGE_NAMESPACE,
                                f"{source_name}:{chunk_idx}",
                            )
                        )
                        chunks.append(
                            {
                                "id": point_id,
                                "chunk_index": chunk_idx,
                                "document_title": doc_title,
                                "section_title": section_title,
                                "source": source_name,
                                "category": category,
                                "content": sub_body.strip(),
                            }
                        )
                        chunk_idx += 1
                        sub_body = p + "\n\n"
                    else:
                        sub_body += p + "\n\n"
                if sub_body.strip():
                    point_id = str(
                        uuid.uuid5(
                            EDUVIA_KNOWLEDGE_NAMESPACE,
                            f"{source_name}:{chunk_idx}",
                        )
                    )
                    chunks.append(
                        {
                            "id": point_id,
                            "chunk_index": chunk_idx,
                            "document_title": doc_title,
                            "section_title": section_title,
                            "source": source_name,
                            "category": category,
                            "content": sub_body.strip(),
                        }
                    )
                    chunk_idx += 1
            else:
                point_id = str(
                    uuid.uuid5(
                        EDUVIA_KNOWLEDGE_NAMESPACE,
                        f"{source_name}:{chunk_idx}",
                    )
                )
                chunks.append(
                    {
                        "id": point_id,
                        "chunk_index": chunk_idx,
                        "document_title": doc_title,
                        "section_title": section_title,
                        "source": source_name,
                        "category": category,
                        "content": body,
                    }
                )
                chunk_idx += 1

        return chunks

    async def ingest_file(
        self,
        file_path: Path,
        category: str | None = None,
        collection_name: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Parse, chunk, embed, and index a single document file into Qdrant.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Source file not found: {file_path}")

        collection = collection_name or settings.QDRANT_COLLECTION_KNOWLEDGE
        await self.qdrant.ensure_collections_exist()

        inferred_category = category
        if not inferred_category:
            parent_dir = file_path.parent.name.lower()
            if "strateg" in parent_dir:
                inferred_category = KnowledgeCategory.STRATEGY.value
            elif "design" in parent_dir:
                inferred_category = KnowledgeCategory.ACTIVITY_DESIGN.value
            elif "access" in parent_dir:
                inferred_category = KnowledgeCategory.ACCESSIBILITY.value
            elif "curric" in parent_dir:
                inferred_category = KnowledgeCategory.CURRICULUM.value
            else:
                inferred_category = KnowledgeCategory.STRATEGY.value

        content = file_path.read_text(encoding="utf-8")
        raw_chunks = self.chunk_markdown(
            content=content,
            source_name=file_path.name,
            category=inferred_category,
        )

        if not raw_chunks:
            return []

        # Generate embeddings for chunks
        chunk_texts = [f"{c['section_title']}\n{c['content']}" for c in raw_chunks]

        if self.orchestrator.is_available:
            vectors = await self.orchestrator.embed_text(chunk_texts)
        else:
            # Deterministic fallback vectors for offline/test environments (768 dimensions)
            vectors = []
            for idx in range(len(raw_chunks)):
                base_val = ((idx + 1) % 10) / 10.0
                vec = [base_val] * 768
                vectors.append(vec)

        # Build Qdrant points
        points = []
        for chunk, vector in zip(raw_chunks, vectors, strict=False):
            points.append(
                {
                    "id": chunk["id"],
                    "vector": vector,
                    "payload": {
                        "document_title": chunk["document_title"],
                        "section_title": chunk["section_title"],
                        "source": chunk["source"],
                        "category": chunk["category"],
                        "chunk_index": chunk["chunk_index"],
                        "content": chunk["content"],
                    },
                }
            )

        await self.qdrant.upsert_points(collection, points)
        logger.info(
            "file_ingested_successfully",
            file=file_path.name,
            chunks=len(points),
            collection=collection,
        )
        return points

    async def ingest_sources_directory(
        self,
        sources_dir: Path | None = None,
        collection_name: str | None = None,
    ) -> KnowledgeIngestionResult:
        """
        Scan and ingest all markdown files in the sources directory.
        """
        target_dir = sources_dir
        if target_dir is None:
            # Default to repo root knowledge_base/sources
            backend_dir = Path(__file__).resolve().parent.parent.parent
            target_dir = backend_dir.parent / "knowledge_base" / "sources"

        result = KnowledgeIngestionResult()
        collection = collection_name or settings.QDRANT_COLLECTION_KNOWLEDGE

        if not target_dir.exists():
            result.errors.append(f"Knowledge sources directory not found: {target_dir}")
            return result

        md_files = list(target_dir.rglob("*.md"))
        result.total_documents_scanned = len(md_files)

        for file_path in md_files:
            try:
                points = await self.ingest_file(
                    file_path=file_path,
                    collection_name=collection,
                )
                result.total_documents_ingested += 1
                result.total_chunks_indexed += len(points)
            except Exception as e:
                logger.error("ingestion_file_failed", file=file_path.name, error=str(e))
                result.errors.append(f"{file_path.name}: {e}")

        if collection not in result.collections_updated and result.total_chunks_indexed > 0:
            result.collections_updated.append(collection)

        return result
