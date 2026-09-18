"""
Eduvia — Gemini LLM Provider

Concrete implementation of LLMProvider using Google Gemini API.
API key is loaded exclusively from environment configuration.
No keys are ever hardcoded here.

IMPORTANT: This class must never be instantiated directly in
business logic. Use the AIOrchestrator instead.
"""
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

# Lazy import to avoid import-time failures when key is not yet set
_google_genai: Any = None


def _get_genai() -> Any:
    """Lazily import google.generativeai."""
    global _google_genai
    if _google_genai is None:
        try:
            import google.generativeai as genai  # type: ignore[import]
            _google_genai = genai
        except ImportError as e:
            raise AIProviderError(
                "google-generativeai package is not installed. "
                "Run: pip install google-generativeai"
            ) from e
    return _google_genai


class GeminiProvider(LLMProvider):
    """
    Google Gemini LLM provider implementation.

    Configuration is read entirely from app.core.config.settings.
    The API key must be set in the GEMINI_API_KEY environment variable.

    Supports:
    - Text generation
    - Structured (JSON) generation for activity schemas
    - Health checks
    """

    def __init__(self, api_key: str | None = None) -> None:
        self._model_name = settings.GEMINI_MODEL
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
        """Get or create the Gemini generative model client."""
        if not self.is_available:
            raise AIProviderError(
                "Gemini API key is not configured. "
                "Set GEMINI_API_KEY in your .env file."
            )
        if self._client is None:
            genai = _get_genai()
            genai.configure(api_key=self._api_key)
            self._client = genai.GenerativeModel(self._model_name)
        return self._client

    def _build_prompt(self, messages: list[Message]) -> str:
        """
        Convert our Message list into a single prompt string for Gemini.

        For Phase 0 we use a simple concatenation approach.
        Phase 9 will implement proper multi-turn conversation.
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

    def _build_generation_config(self, config: GenerationConfig) -> dict[str, Any]:
        """Map our GenerationConfig to Gemini's generation_config format."""
        cfg: dict[str, Any] = {
            "temperature": config.temperature,
            "max_output_tokens": config.max_tokens,
            "top_p": config.top_p,
        }
        if config.stop_sequences:
            cfg["stop_sequences"] = config.stop_sequences
        return cfg

    async def generate(
        self,
        messages: list[Message],
        config: GenerationConfig | None = None,
    ) -> LLMResponse:
        """Generate a text response from Gemini."""
        cfg = config or GenerationConfig()
        client = self._get_client()
        prompt = self._build_prompt(messages)
        gen_cfg = self._build_generation_config(cfg)

        try:
            logger.debug(
                "gemini_generate_request",
                model=self._model_name,
                message_count=len(messages),
                temperature=cfg.temperature,
            )

            # Note: google-generativeai is synchronous; wrap in thread executor
            # for async compatibility. Full async support added in later phase.
            import asyncio
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: client.generate_content(
                    prompt,
                    generation_config=gen_cfg,
                ),
            )

            content = response.text
            usage: dict[str, int] = {}

            # Extract token usage if available
            if hasattr(response, "usage_metadata") and response.usage_metadata:
                meta = response.usage_metadata
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

        # Append schema instruction to the last user message
        augmented_messages = list(messages)
        if augmented_messages and augmented_messages[-1].role == MessageRole.USER:
            last = augmented_messages[-1]
            augmented_messages[-1] = Message(
                role=last.role,
                content=last.content + schema_instruction,
            )
        else:
            from app.ai.providers.base import Message as Msg
            augmented_messages.append(
                Msg(role=MessageRole.USER, content=schema_instruction)
            )

        json_config = GenerationConfig(
            temperature=0.3,  # Lower temperature for structured output
            max_tokens=config.max_tokens if config else 2048,
            response_format="json",
        )

        response = await self.generate(augmented_messages, json_config)

        try:
            # Extract JSON from response, handling possible markdown code blocks
            content = response.content.strip()
            if content.startswith("```"):
                lines = content.split("\n")
                content = "\n".join(lines[1:-1])  # Remove ``` markers

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
