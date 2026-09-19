"""
Tests for AI provider abstractions.

Tests the LLM provider interface and GeminiProvider without
making real API calls. All Gemini calls are mocked.
"""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from app.ai.providers.base import (
    GenerationConfig,
    LLMProvider,
    LLMResponse,
    Message,
    MessageRole,
)
from app.ai.providers.gemini import GeminiProvider


class TestLLMProviderInterface:
    """Tests that the LLMProvider abstract interface is correctly designed."""

    def test_llm_provider_is_abstract(self) -> None:
        """LLMProvider should not be directly instantiable."""
        with pytest.raises(TypeError):
            LLMProvider()  # type: ignore[abstract]

    def test_message_role_values(self) -> None:
        """MessageRole enum should have the expected values."""
        assert MessageRole.SYSTEM == "system"
        assert MessageRole.USER == "user"
        assert MessageRole.ASSISTANT == "assistant"

    def test_generation_config_defaults(self) -> None:
        """GenerationConfig should have sensible defaults."""
        config = GenerationConfig()
        assert 0.0 <= config.temperature <= 2.0
        assert config.max_tokens > 0
        assert 0.0 <= config.top_p <= 1.0

    def test_llm_response_token_properties(self) -> None:
        """LLMResponse should correctly compute token totals."""
        response = LLMResponse(
            content="Hello",
            model="test-model",
            provider="test",
            usage={"input_tokens": 10, "output_tokens": 20},
        )
        assert response.input_tokens == 10
        assert response.output_tokens == 20
        assert response.total_tokens == 30

    def test_llm_response_empty_usage(self) -> None:
        """LLMResponse should handle missing usage gracefully."""
        response = LLMResponse(
            content="Hello",
            model="test-model",
            provider="test",
        )
        assert response.input_tokens == 0
        assert response.output_tokens == 0
        assert response.total_tokens == 0


class TestGeminiProvider:
    """Tests for the Gemini provider implementation."""

    def test_gemini_provider_name(self) -> None:
        """GeminiProvider should identify itself as 'gemini'."""
        provider = GeminiProvider(api_key="test-key")
        assert provider.provider_name == "gemini"

    def test_gemini_not_available_with_placeholder_key(self) -> None:
        """GeminiProvider should report unavailable with placeholder key."""
        # Inject placeholder key directly — no env patching needed
        provider = GeminiProvider(api_key="CHANGE_ME_GEMINI_API_KEY")
        assert not provider.is_available

    @pytest.mark.asyncio
    async def test_gemini_health_check_returns_false_without_key(self) -> None:
        """Health check should return False when API key is not configured."""
        # Inject a placeholder key — health check should return False
        provider = GeminiProvider(api_key="CHANGE_ME_KEY")
        result = await provider.health_check()
        assert result is False


class TestAIOrchestrator:
    """Tests for the AI Orchestrator."""

    @pytest.mark.asyncio
    async def test_orchestrator_health_check_structure(self) -> None:
        """Orchestrator health_check should return dict with expected keys."""
        from app.ai.orchestrator.orchestrator import get_ai_orchestrator
        get_ai_orchestrator.cache_clear()

        orchestrator = get_ai_orchestrator()
        result = await orchestrator.health_check()

        assert "provider" in result
        assert "configured" in result
        assert "healthy" in result
        get_ai_orchestrator.cache_clear()

    @pytest.mark.asyncio
    async def test_orchestrator_raises_when_provider_unavailable(self) -> None:
        """Orchestrator should raise AIProviderError when provider is not configured."""
        from app.ai.orchestrator.orchestrator import AIOrchestrator
        from app.core.errors import AIProviderError

        mock_provider = MagicMock()
        mock_provider.is_available = False
        mock_provider.provider_name = "mock"

        orchestrator = AIOrchestrator(provider=mock_provider)

        with pytest.raises(AIProviderError):
            await orchestrator.generate(
                messages=[Message(role=MessageRole.USER, content="test")]
            )
