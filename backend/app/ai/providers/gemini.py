"""
Eduvia — Gemini LLM Provider

Concrete implementation of LLMProvider using the modern Google GenAI SDK (google-genai).
API key is loaded exclusively from environment configuration.
No keys are ever hardcoded here.

IMPORTANT: This class must never be instantiated directly in
business logic. Use the AIOrchestrator instead.
"""
from __future__ import annotations

import asyncio
import json
from typing import Any

import structlog

from app.ai.providers.base import (
    GenerationConfig,
    LLMProvider,
    LLMResponse,
    Message,
    MessageRole,
)
from app.core.config import settings
from app.core.errors import AIProviderError

logger = structlog.get_logger(__name__)

# Lazy import cache
_google_genai_module: Any = None


def _get_genai() -> Any:
    """Lazily import google.genai."""
    global _google_genai_module
    if _google_genai_module is None:
        try:
            from google import genai
            _google_genai_module = genai
        except ImportError as e:
            raise AIProviderError(
                "google-genai package is not installed. "
                "Run: pip install google-genai"
            ) from e
    return _google_genai_module


class GeminiProvider(LLMProvider):
    """
    Google Gemini LLM provider implementation using google-genai SDK.

    Configuration is read entirely from app.core.config.settings.
    The API key must be set in the GEMINI_API_KEY environment variable.

    Supports:
    - Text generation
    - Structured (JSON) generation for activity schemas
    - Vector embeddings generation (text-embedding-004)
    - Health checks with robust error normalization
    """

    def __init__(self, api_key: str | None = None) -> None:
        self._model_name = settings.GEMINI_MODEL
        self._embedding_model = settings.GEMINI_EMBEDDING_MODEL
        # Allow explicit key injection (useful for testing without env hacks)
        self._api_key = api_key if api_key is not None else settings.GEMINI_API_KEY
        self._client: Any | None = None

    @property
    def provider_name(self) -> str:
        return "gemini"

    @property
    def is_available(self) -> bool:
        """Check if Gemini API key is configured and non-placeholder."""
        return (
            bool(self._api_key)
            and not self._api_key.startswith("CHANGE_ME")
            and self._api_key.lower() not in ("placeholder", "test", "", "your-api-key")
        )

    def _get_client(self) -> Any:
        """Get or create the Google GenAI client."""
        if not self.is_available:
            raise AIProviderError(
                "Gemini API key is not configured. "
                "Set GEMINI_API_KEY in your .env file."
            )
        if self._client is None:
            genai = _get_genai()
            self._client = genai.Client(api_key=self._api_key)
        return self._client

    def _build_prompt(self, messages: list[Message]) -> str:
        """
        Convert our Message list into a single structured prompt string.
        """
        parts = []
        for msg in messages:
            if msg.role == MessageRole.SYSTEM:
                parts.append(f"[System Instructions]\n{msg.content}")
            elif msg.role == MessageRole.USER:
                parts.append(f"[User]\n{msg.content}")
            elif msg.role == MessageRole.ASSISTANT:
                parts.append(f"[Assistant]\n{msg.content}")
        return "\n\n".join(parts)

    async def generate(
        self,
        messages: list[Message],
        config: GenerationConfig | None = None,
    ) -> LLMResponse:
        """Generate a text response from Gemini via google-genai."""
        cfg = config or GenerationConfig()
        client = self._get_client()
        prompt = self._build_prompt(messages)

        try:
            logger.debug(
                "gemini_generate_request",
                model=self._model_name,
                message_count=len(messages),
                temperature=cfg.temperature,
            )

            from google.genai import types

            gen_config = types.GenerateContentConfig(
                temperature=cfg.temperature,
                max_output_tokens=cfg.max_tokens,
                top_p=cfg.top_p,
                stop_sequences=cfg.stop_sequences if cfg.stop_sequences else None,
            )

            # Support both async aio client and synchronous/mocked client
            if hasattr(client, "aio") and hasattr(client.aio, "models"):
                resp = await client.aio.models.generate_content(
                    model=self._model_name,
                    contents=prompt,
                    config=gen_config,
                )
            else:
                resp = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: client.models.generate_content(
                        model=self._model_name,
                        contents=prompt,
                        config=gen_config,
                    ),
                )

            content = resp.text or ""
            usage: dict[str, int] = {}

            if hasattr(resp, "usage_metadata") and resp.usage_metadata:
                meta = resp.usage_metadata
                usage = {
                    "input_tokens": getattr(meta, "prompt_token_count", 0),
                    "output_tokens": getattr(meta, "candidates_token_count", 0),
                }

            logger.debug(
                "gemini_generate_response",
                model=self._model_name,
                usage=usage,
            )

            return LLMResponse(
                content=content,
                model=self._model_name,
                provider=self.provider_name,
                usage=usage,
            )

        except AIProviderError:
            raise
        except Exception as e:
            logger.error("gemini_generate_error", error=str(e))
            raise AIProviderError(f"Gemini generation failed: {e}") from e

    async def generate_structured(
        self,
        messages: list[Message],
        output_schema: dict[str, Any],
        config: GenerationConfig | None = None,
    ) -> dict[str, Any]:
        """
        Generate a structured JSON response from Gemini.

        Appends schema instructions to the prompt and parses the JSON response.
        Pydantic validation is expected to be done by the caller.
        """
        schema_instruction = (
            f"\n\nIMPORTANT: Respond with ONLY valid JSON conforming to this schema:\n"
            f"{json.dumps(output_schema, indent=2)}\n"
            f"Do not include any text before or after the JSON."
        )

        augmented_messages = list(messages)
        if augmented_messages and augmented_messages[-1].role == MessageRole.USER:
            last = augmented_messages[-1]
            augmented_messages[-1] = Message(
                role=last.role,
                content=last.content + schema_instruction,
            )
        else:
            augmented_messages.append(
                Message(role=MessageRole.USER, content=schema_instruction)
            )

        json_config = GenerationConfig(
            temperature=0.3,
            max_tokens=config.max_tokens if config else 2048,
            response_format="json",
        )

        response = await self.generate(augmented_messages, json_config)

        try:
            content = response.content.strip()
            if content.startswith("```"):
                lines = content.split("\n")
                # Remove ```json or ``` opening and closing ```
                first_line_end = 1
                if lines[0].startswith("```"):
                    lines = lines[first_line_end:]
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]
                content = "\n".join(lines).strip()

            return dict(json.loads(content))
        except json.JSONDecodeError as e:
            logger.error(
                "gemini_structured_json_parse_error",
                content=response.content[:500],
                error=str(e),
            )
            raise AIProviderError(
                f"Failed to parse Gemini structured response as JSON: {e}"
            ) from e

    async def embed_text(self, texts: list[str]) -> list[list[float]]:
        """
        Generate vector embeddings using Google GenAI embedding model.

        Args:
            texts: List of text strings to embed.

        Returns:
            List of float embedding vectors (768 dimensions for text-embedding-004).
        """
        if not texts:
            return []

        client = self._get_client()
        try:
            logger.debug(
                "gemini_embed_request",
                model=self._embedding_model,
                passage_count=len(texts),
            )

            embed_config = {"output_dimensionality": 768}
            if hasattr(client, "aio") and hasattr(client.aio, "models"):
                resp = await client.aio.models.embed_content(
                    model=self._embedding_model,
                    contents=texts,
                    config=embed_config,
                )
            else:
                resp = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: client.models.embed_content(
                        model=self._embedding_model,
                        contents=texts,
                        config=embed_config,
                    ),
                )

            embeddings: list[list[float]] = []
            if hasattr(resp, "embeddings") and resp.embeddings:
                for item in resp.embeddings:
                    embeddings.append(list(item.values))

            logger.debug(
                "gemini_embed_response",
                model=self._embedding_model,
                generated_count=len(embeddings),
            )
            return embeddings

        except AIProviderError:
            raise
        except Exception as e:
            logger.error("gemini_embed_error", error=str(e))
            raise AIProviderError(f"Gemini embedding generation failed: {e}") from e

    async def health_check(self) -> bool:
        """Verify Gemini API connectivity with a minimal generation call."""
        if not self.is_available:
            logger.warning("gemini_health_check_skipped", reason="api_key_not_configured")
            return False

        try:
            response = await self.generate(
                messages=[Message(role=MessageRole.USER, content="Reply with: ok")],
                config=GenerationConfig(temperature=0.0, max_tokens=5),
            )
            return len(response.content) > 0
        except Exception as e:
            logger.warning("gemini_health_check_failed", error=str(e))
            return False

