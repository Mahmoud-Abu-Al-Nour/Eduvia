"""
Eduvia — Abstract LLM Provider Interface

Defines the contract all LLM providers must implement.
Business logic must only interact with this interface,
never with concrete provider implementations directly.

Design:
    AI Orchestrator
          ↓
    LLMProvider (this interface)
          ↓
    GeminiProvider | FutureProvider
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class MessageRole(StrEnum):
    """Roles in an LLM conversation."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class Message:
    """A single message in an LLM conversation."""
    role: MessageRole
    content: str


@dataclass
class GenerationConfig:
    """
    Configuration for an LLM generation request.

    Not all providers support all options.
    Providers must gracefully ignore unsupported options.
    """
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 0.95
    stop_sequences: list[str] = field(default_factory=list)
    response_format: str = "text"  # "text" | "json"


@dataclass
class LLMResponse:
    """
    Standardized response from any LLM provider.

    All provider-specific response objects must be mapped
    to this structure before returning to business logic.
    """
    content: str
    model: str
    provider: str
    usage: dict[str, int] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def input_tokens(self) -> int:
        return self.usage.get("input_tokens", 0)

    @property
    def output_tokens(self) -> int:
        return self.usage.get("output_tokens", 0)

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens


class LLMProvider(ABC):
    """
    Abstract base class for all LLM provider integrations.

    To add a new provider (e.g. OpenAI, Anthropic):
    1. Create a new class in app/ai/providers/
    2. Inherit from LLMProvider
    3. Implement all abstract methods
    4. Register the provider in the orchestrator

    IMPORTANT: Provider implementations must NEVER be called
    directly from business logic. Always use the AI Orchestrator.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Human-readable name for this provider (e.g. 'gemini', 'openai')."""
        ...

    @property
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if this provider is currently configured and available.
        Should return False if API key is missing or invalid.
        """
        ...

    @abstractmethod
    async def generate(
        self,
        messages: list[Message],
        config: GenerationConfig | None = None,
    ) -> LLMResponse:
        """
        Generate a response from the LLM.

        Args:
            messages: Conversation history including the current prompt.
            config: Optional generation configuration.

        Returns:
            Standardized LLMResponse.

        Raises:
            AIProviderError: If the provider call fails.
        """
        ...

    @abstractmethod
    async def generate_structured(
        self,
        messages: list[Message],
        output_schema: dict[str, Any],
        config: GenerationConfig | None = None,
    ) -> dict[str, Any]:
        """
        Generate a structured (JSON) response conforming to a schema.

        Used for activity generation where output must be validated
        against a Pydantic model.

        Args:
            messages: Conversation history.
            output_schema: JSON Schema the output must conform to.
            config: Optional generation configuration.

        Returns:
            Parsed dict conforming to output_schema.

        Raises:
            AIProviderError: If generation or parsing fails.
        """
        ...

    @abstractmethod
    async def embed_text(self, texts: list[str]) -> list[list[float]]:
        """
        Generate vector embeddings for a list of text strings.

        Used for RAG knowledge ingestion and semantic retrieval.

        Args:
            texts: List of text passages to embed.

        Returns:
            List of embedding vectors (float lists).

        Raises:
            AIProviderError: If embedding generation fails.
        """
        ...

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Verify the provider is operational.

        Returns:
            True if the provider is reachable and functional.
        """
        ...

