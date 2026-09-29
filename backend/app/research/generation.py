"""
Eduvia — Research Generation Service

Pure research sandbox generation pipeline.
Strictly isolated from Production curriculum, Content Bank, RAG, Phase 8,
and Learner Profile adaptation.

Pipeline:
Research Prompt + Research config + Optional explicitly supplied context
    ↓
Gemini Provider
    ↓
Raw Output + Normalized Artifact + Reproducibility Metadata
"""
from __future__ import annotations

import json
import re
import time
from typing import Any

import structlog
from pydantic import ValidationError

from app.ai.providers.base import GenerationConfig, Message, MessageRole
from app.ai.providers.gemini import GeminiProvider
from app.core.config import settings
from app.core.errors import AIProviderError
from app.research.catalog import DEFAULT_RESEARCH_MODEL_ID

logger = structlog.get_logger(__name__)


def _extract_json_payload(raw_text: str) -> tuple[dict[str, Any] | list[Any] | None, bool]:
    """
    Attempt to extract and parse a JSON object or array from LLM response text.
    Handles raw JSON, markdown-fenced ```json code blocks, and embedded JSON.

    Returns:
        (parsed_data, parse_warning_flag)
    """
    if not raw_text or not raw_text.strip():
        return None, True

    cleaned = raw_text.strip()

    # 1. Try direct JSON parse
    try:
        data = json.loads(cleaned)
        if isinstance(data, (dict, list)):
            return data, False
    except Exception:
        pass

    # 2. Try markdown fenced code block: ```json ... ``` or ``` ... ```
    pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
    matches = re.findall(pattern, cleaned, re.IGNORECASE)
    for match in matches:
        try:
            data = json.loads(match.strip())
            if isinstance(data, (dict, list)):
                return data, False
        except Exception:
            continue

    # 3. Try finding outer brackets { ... } or [ ... ]
    first_brace = cleaned.find("{")
    last_brace = cleaned.rfind("}")
    if first_brace != -1 and last_brace > first_brace:
        candidate = cleaned[first_brace : last_brace + 1]
        try:
            data = json.loads(candidate)
            if isinstance(data, dict):
                return data, False
        except Exception:
            pass

    first_sq = cleaned.find("[")
    last_sq = cleaned.rfind("]")
    if first_sq != -1 and last_sq > first_sq:
        candidate = cleaned[first_sq : last_sq + 1]
        try:
            data = json.loads(candidate)
            if isinstance(data, list):
                return data, False
        except Exception:
            pass

    return None, True


def validate_production_compatibility(
    payload: Any,
    target_schema: str | None = None,
) -> tuple[bool, dict[str, Any]]:
    """
    Optional validation against Production schemas without altering the payload.
    Used exclusively when production_compatibility_mode=True.
    """
    if not isinstance(payload, dict):
        return False, {"errors": ["Payload is not a structured JSON object."]}

    errors: list[str] = []

    target = (target_schema or "").lower()

    if target in ("activity", "practice_activity"):
        try:
            from app.activities.schemas import Activity
            Activity.model_validate(payload)
            return True, {"valid": True, "target": "Activity"}
        except ValidationError as ve:
            errors = [f"{err['loc']}: {err['msg']}" for err in ve.errors()]
            return False, {"valid": False, "target": "Activity", "errors": errors}
        except Exception as e:
            return False, {"valid": False, "target": "Activity", "errors": [str(e)]}

    elif target in ("instructional", "instructional_content"):
        try:
            from app.instructional.schemas import InstructionalContentRead
            InstructionalContentRead.model_validate(payload)
            return True, {"valid": True, "target": "InstructionalContentRead"}
        except ValidationError as ve:
            errors = [f"{err['loc']}: {err['msg']}" for err in ve.errors()]
            return False, {"valid": False, "target": "InstructionalContentRead", "errors": errors}
        except Exception as e:
            return False, {"valid": False, "target": "InstructionalContentRead", "errors": [str(e)]}

    # Default heuristic: check if it looks like an activity or question set
    if "questions" in payload and isinstance(payload["questions"], list):
        try:
            from app.activities.schemas import Activity
            Activity.model_validate(payload)
            return True, {"valid": True, "target": "Activity"}
        except ValidationError as ve:
            errors = [f"{err['loc']}: {err['msg']}" for err in ve.errors()]
            return False, {"valid": False, "target": "Activity", "errors": errors}
        except Exception as e:
            return False, {"valid": False, "target": "Activity", "errors": [str(e)]}

    return False, {"valid": False, "target": target_schema or "unknown", "errors": ["No matching production schema recognized"]}


class ResearchGenerationService:
    """
    Executes raw experimental generation using the shared Gemini client,
    bypassing all production RAG, Content Bank, and adaptive restrictions.
    """

    def __init__(self, provider: GeminiProvider | None = None) -> None:
        self._provider = provider or GeminiProvider()

    async def execute_generation(
        self,
        prompt: str,
        system_prompt: str | None = None,
        model: str = DEFAULT_RESEARCH_MODEL_ID,
        model_configuration: dict[str, Any] | None = None,
        explicit_context: dict[str, Any] | None = None,
        output_target: str = "freeform",
        production_compatibility_mode: bool = False,
        target_production_schema: str | None = None,
        question_count: int | None = None,
    ) -> dict[str, Any]:
        """
        Execute research generation.

        Returns a dictionary containing:
        - raw_output
        - normalized_output
        - status: 'completed' | 'completed_with_parse_warning' | 'failed'
        - is_production_compatible: bool
        - compatibility_validation: dict | None
        - execution_time_ms: float
        - error: str | None
        """
        start_time = time.perf_counter()
        config_dict = model_configuration or {}

        temperature = float(config_dict.get("temperature", 0.7))
        max_tokens = int(config_dict.get("max_output_tokens", 2048))
        top_p = float(config_dict.get("top_p", 0.95))

        gen_config = GenerationConfig(
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            model=model,
        )

        # Build messages ONLY from researcher inputs
        messages: list[Message] = []

        # 1. Custom or default sandbox system instructions
        active_system_prompt = system_prompt or (
            "You are an AI research sandbox assistant for educational experimentation. "
            "Follow the researcher's instructions precisely without being constrained by production rules."
        )
        messages.append(Message(role=MessageRole.SYSTEM, content=active_system_prompt))

        # 2. Explicit context (ONLY if explicitly supplied by researcher)
        user_content_parts = []
        if explicit_context and explicit_context.get("manual_context"):
            user_content_parts.append(f"[Explicit Context]\n{explicit_context['manual_context']}")

        # Optional explicit question count target
        if question_count is not None:
            user_content_parts.append(f"[Requested Question Count]\nTarget count: {question_count} questions.")

        # 3. User prompt
        user_content_parts.append(prompt)
        messages.append(Message(role=MessageRole.USER, content="\n\n".join(user_content_parts)))

        try:
            logger.info(
                "research_generation_start",
                model=model,
                output_target=output_target,
                temp=temperature,
            )

            # Generate via Gemini
            response = await self._provider.generate(messages, gen_config)
            raw_text = response.content or ""
            execution_time_ms = round((time.perf_counter() - start_time) * 1000, 2)

            # Extract normalized payload
            parsed_json, has_warning = _extract_json_payload(raw_text)

            if parsed_json is not None:
                normalized_payload: dict[str, Any] = (
                    parsed_json if isinstance(parsed_json, dict) else {"items": parsed_json}
                )
                run_status = "completed"
            else:
                # Store text in normalized envelope so nothing is lost
                normalized_payload = {"text": raw_text, "format": "freeform"}
                run_status = "completed_with_parse_warning" if output_target != "freeform" else "completed"

            # Optional compatibility validation
            is_compat = False
            compat_report: dict[str, Any] | None = None
            if production_compatibility_mode:
                is_compat, compat_report = validate_production_compatibility(
                    normalized_payload,
                    target_schema=target_production_schema,
                )

            return {
                "raw_output": raw_text,
                "normalized_output": normalized_payload,
                "status": run_status,
                "is_production_compatible": is_compat,
                "compatibility_validation": compat_report,
                "execution_time_ms": execution_time_ms,
                "error": None,
            }

        except Exception as e:
            execution_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
            safe_error = f"Research generation failed: {type(e).__name__} - {str(e)}"
            logger.error("research_generation_error", error=str(e), duration_ms=execution_time_ms)
            return {
                "raw_output": None,
                "normalized_output": None,
                "status": "failed",
                "is_production_compatible": False,
                "compatibility_validation": None,
                "execution_time_ms": execution_time_ms,
                "error": safe_error,
            }


_research_gen_service: ResearchGenerationService | None = None


def get_research_generation_service() -> ResearchGenerationService:
    global _research_gen_service
    if _research_gen_service is None:
        _research_gen_service = ResearchGenerationService()
    return _research_gen_service
