"""
Eduvia — AI Orchestrator

Central coordinator for all AI operations in Eduvia.
Business logic should only interact with this orchestrator,
never with LLM providers directly.

Architecture:
    Business Logic (activities, recommendations, analytics)
              ↓
        AIOrchestrator  ← single entry point
              ↓
        LLMProvider (interface)
              ↓
        GeminiProvider | FutureProvider

The orchestrator is responsible for:
- Selecting the active LLM provider
- Building prompts with retrieved RAG context
- Routing requests to appropriate generation methods
- Handling retries and fallback logic
- Logging all AI interactions for auditability

IMPORTANT: This is a Phase 0 shell.
Full orchestration logic is implemented in Phase 9 (Gemini + RAG).
"""
from __future__ import annotations

from functools import lru_cache
from typing import Any

import structlog

from app.ai.providers.base import GenerationConfig, LLMProvider, LLMResponse, Message
from app.ai.providers.gemini import GeminiProvider
from app.core.errors import AIProviderError

logger = structlog.get_logger(__name__)


class AIOrchestrator:
    """
    Central AI orchestrator for Eduvia.

    Manages provider selection and provides a unified API
    for all AI-powered features.

    Phase 0: Basic provider wiring and health check.
    Phase 9: Full RAG integration, prompt engineering, and adaptive logic.
    """

    def __init__(self, provider: LLMProvider) -> None:
        self._provider = provider
        logger.info(
            "ai_orchestrator_initialized",
            provider=provider.provider_name,
            available=provider.is_available,
        )

    @property
    def provider(self) -> LLMProvider:
        """The active LLM provider."""
        return self._provider

    @property
    def is_available(self) -> bool:
        """Whether the AI system is currently operational."""
        return self._provider.is_available

    async def generate(
        self,
        messages: list[Message],
        config: GenerationConfig | None = None,
    ) -> LLMResponse:
        """
        Generate a text response using the active LLM provider.

        Args:
            messages: Conversation messages.
            config: Optional generation configuration.

        Returns:
            LLMResponse with generated content.

        Raises:
            AIProviderError: If generation fails.
        """
        if not self.is_available:
            raise AIProviderError(
                "AI provider is not configured. "
                "Please set GEMINI_API_KEY in your environment."
            )

        logger.info(
            "ai_orchestrator_generate",
            provider=self._provider.provider_name,
            message_count=len(messages),
        )

        return await self._provider.generate(messages, config)

    async def generate_structured(
        self,
        messages: list[Message],
        output_schema: dict[str, Any],
        config: GenerationConfig | None = None,
    ) -> dict[str, Any]:
        """
        Generate a structured JSON response.

        Used by the Activity Generator to produce validated activity schemas.
        The output will be validated by Pydantic models in the calling service.

        Args:
            messages: Conversation messages.
            output_schema: JSON Schema the response must conform to.
            config: Optional generation configuration.

        Returns:
            Parsed dict conforming to output_schema.

        Raises:
            AIProviderError: If generation or parsing fails.
        """
        if not self.is_available:
            raise AIProviderError("AI provider is not configured.")

        return await self._provider.generate_structured(messages, output_schema, config)

    async def health_check(self) -> dict[str, Any]:
        """
        Check the health of the AI subsystem.

        Returns:
            Dict with provider name, availability, and connectivity status.
        """
        healthy = await self._provider.health_check()
        return {
            "provider": self._provider.provider_name,
            "configured": self._provider.is_available,
            "healthy": healthy,
        }


@lru_cache(maxsize=1)
def get_ai_orchestrator() -> AIOrchestrator:
    """
    Return the singleton AI Orchestrator instance.

    Provider selection is based on configuration.
    Currently defaults to Gemini.

    Future: Support provider selection via APP_AI_PROVIDER env var.
    """
    provider = GeminiProvider()
    return AIOrchestrator(provider=provider)
