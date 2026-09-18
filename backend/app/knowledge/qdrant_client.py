"""
Eduvia — Qdrant Vector Database Client

Provides a centralized interface for all vector database operations.
Used by the Knowledge Base (RAG) and potentially the Curriculum Engine.

Collections:
- eduvia_knowledge: General educational/pedagogical knowledge
- eduvia_curriculum: Curriculum objectives and content embeddings

Phase 0: Client initialization and connectivity check.
Phase 9: Full RAG ingestion and retrieval implementation.
"""
from __future__ import annotations

from functools import lru_cache
from typing import Any

import structlog

from app.core.config import settings
from app.core.errors import EduviaError

logger = structlog.get_logger(__name__)


class QdrantClientError(EduviaError):
    """Qdrant operation failed."""
    error_code = "qdrant_error"
    message = "Vector database operation failed."


class EduViaQdrantClient:
    """
    Eduvia's abstraction layer over the Qdrant vector database.

    All RAG retrieval and knowledge embedding operations go through
    this class. This ensures we can change the underlying vector DB
    implementation without touching business logic.

    Phase 0 responsibilities:
    - Initialize client connection
    - Verify connectivity
    - Expose collection names from config

    Phase 9 responsibilities:
    - Embed and ingest knowledge documents
    - Semantic similarity search
    - Curriculum objective retrieval
    - Learning strategy retrieval
    """

    def __init__(self) -> None:
        self._url = settings.QDRANT_URL
        self._api_key = settings.QDRANT_API_KEY or None
        self._client: Any | None = None

        # Collection names from config
        self.knowledge_collection = settings.QDRANT_COLLECTION_KNOWLEDGE
        self.curriculum_collection = settings.QDRANT_COLLECTION_CURRICULUM

    def _get_client(self) -> Any:
        """Get or lazily initialize the Qdrant client."""
        if self._client is None:
            try:
                from qdrant_client import QdrantClient  # type: ignore[import]

                kwargs: dict[str, Any] = {"url": self._url}
                if self._api_key:
                    kwargs["api_key"] = self._api_key

                self._client = QdrantClient(**kwargs)
                logger.info("qdrant_client_initialized", url=self._url)
            except ImportError as e:
                raise QdrantClientError(
                    "qdrant-client package is not installed. "
                    "Run: pip install qdrant-client"
                ) from e
            except Exception as e:
                logger.error("qdrant_client_init_error", error=str(e))
                raise QdrantClientError(f"Failed to initialize Qdrant client: {e}") from e
        return self._client

    async def health_check(self) -> bool:
        """
        Verify Qdrant connectivity.

        Returns:
            True if Qdrant is reachable and responsive.
        """
        try:
            import asyncio
            client = self._get_client()

            # QdrantClient is synchronous; wrap in executor
            result = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: client.get_collections(),
            )
            logger.debug("qdrant_health_check_ok", collections=str(result))
            return True
        except Exception as e:
            logger.warning("qdrant_health_check_failed", error=str(e))
            return False

    async def list_collections(self) -> list[str]:
        """Return a list of existing collection names."""
        try:
            import asyncio
            client = self._get_client()
            result = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: client.get_collections(),
            )
            return [col.name for col in result.collections]
        except Exception as e:
            logger.error("qdrant_list_collections_error", error=str(e))
            raise QdrantClientError(f"Failed to list Qdrant collections: {e}") from e

    async def ensure_collections_exist(self) -> None:
        """
        Create required collections if they don't already exist.

        Called during application startup or database initialization.
        Vector size uses 768 dimensions (text-embedding-004 / similar models).
        This will be made configurable in Phase 9.
        """
        from qdrant_client.models import Distance, VectorParams  # type: ignore[import]

        existing = await self.list_collections()
        collections_to_create = [
            self.knowledge_collection,
            self.curriculum_collection,
        ]

        for collection_name in collections_to_create:
            if collection_name not in existing:
                try:
                    import asyncio
                    client = self._get_client()
                    await asyncio.get_event_loop().run_in_executor(
                        None,
                        lambda name=collection_name: client.create_collection(
                            collection_name=name,
                            vectors_config=VectorParams(
                                size=768,
                                distance=Distance.COSINE,
                            ),
                        ),
                    )
                    logger.info("qdrant_collection_created", collection=collection_name)
                except Exception as e:
                    logger.error(
                        "qdrant_collection_create_error",
                        collection=collection_name,
                        error=str(e),
                    )
                    raise QdrantClientError(
                        f"Failed to create collection '{collection_name}': {e}"
                    ) from e


@lru_cache(maxsize=1)
def get_qdrant_client() -> EduViaQdrantClient:
    """
    Return the singleton Qdrant client instance.

    FastAPI dependency:
        async def my_route(qdrant: EduViaQdrantClient = Depends(get_qdrant_client)):
    """
    return EduViaQdrantClient()
