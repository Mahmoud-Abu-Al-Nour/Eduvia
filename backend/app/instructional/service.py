"""
Eduvia — Instructional Content Service (Phase 4 Extension)

Provides authoritative instructional explanations and modeling separate from
practice activities. Manages generation via Gemini + RAG, deterministic fallbacks,
and the teacher review / approval / publish lifecycle.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

import structlog
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession


from app.ai.orchestrator.orchestrator import AIOrchestrator, get_ai_orchestrator
from app.content.bank import get_content_bank
from app.core.errors import NotFoundError, ValidationError
from app.curriculum.service import CurriculumService
from app.instructional.models import InstructionalContent
from app.instructional.schemas import (
    ContentBlockType,
    ExplanationMethod,
    InstructionalBlock,
    InstructionalContentRead,
    InstructionalContentUpdate,
    InstructionalGenerateRequest,
    InstructionalGenerateResponse,
    InstructionalStatus,
)
from app.users.models import User

logger = structlog.get_logger(__name__)


def _extract_text(val: Any, lang: str = "en") -> str:
    if isinstance(val, dict):
        return str(val.get(lang) or val.get("en") or next(iter(val.values()), ""))
    return str(val or "")


def create_fallback_instructional_content(
    objective_id: uuid.UUID,
    objective_title: str,
    objective_description: str | None = None,
    method: ExplanationMethod = ExplanationMethod.STEP_BY_STEP,
    difficulty_level: int = 1,
    language: str = "en",
) -> dict[str, Any]:
    """
    Deterministic zero-strand fallback generator for instructional content.
    Produces rich, accessible instructional blocks without requiring Gemini or external APIs.
    """
    title = objective_title or "Foundational Learning"
    blocks: list[dict[str, Any]] = []

    if method == ExplanationMethod.VISUAL_EXPLANATION:
        blocks = [
            {
                "id": "blk_vis_1",
                "block_type": ContentBlockType.HEADING.value,
                "title": f"Visual Exploration: {title}",
                "body": f"Look closely at the visual patterns that represent {title}.",
                "visual_cue": "👁️",
                "order_index": 1,
                "metadata": {},
            },
            {
                "id": "blk_vis_2",
                "block_type": ContentBlockType.VISUAL_CUE.value,
                "title": "Visual Representation",
                "body": "Here are distinct visual anchors arranged clearly: 🌟 🌟 🌟",
                "visual_cue": "🌟",
                "order_index": 2,
                "metadata": {"layout": "horizontal_grid"},
            },
            {
                "id": "blk_vis_3",
                "block_type": ContentBlockType.TEXT.value,
                "title": "Observation Guide",
                "body": "Notice how each item has its own place. We can count or identify each one without rushing.",
                "visual_cue": "🔍",
                "order_index": 3,
                "metadata": {},
            },
            {
                "id": "blk_vis_4",
                "block_type": ContentBlockType.CALLOUT.value,
                "title": "Key Visual Clue",
                "body": f"Always start observing from left to right when exploring {title}.",
                "visual_cue": "💡",
                "order_index": 4,
                "metadata": {},
            },
        ]
        summary = f"Visual guide demonstrating {title} using clear spatial cues."

    elif method == ExplanationMethod.STEP_BY_STEP:
        blocks = [
            {
                "id": "blk_step_1",
                "block_type": ContentBlockType.HEADING.value,
                "title": f"Step-by-Step: {title}",
                "body": "Let's break this learning goal into small, calm steps.",
                "visual_cue": "🚶",
                "order_index": 1,
                "metadata": {},
            },
            {
                "id": "blk_step_2",
                "block_type": ContentBlockType.STEP.value,
                "title": "Step 1: Notice the Starting Point",
                "body": "Focus on the first element. Say its name or recognize its shape calmly.",
                "visual_cue": "1️⃣",
                "order_index": 2,
                "metadata": {"step_number": 1},
            },
            {
                "id": "blk_step_3",
                "block_type": ContentBlockType.STEP.value,
                "title": "Step 2: Follow the Pattern",
                "body": "Move forward one piece at a time. Each step builds directly on the previous one.",
                "visual_cue": "2️⃣",
                "order_index": 3,
                "metadata": {"step_number": 2},
            },
            {
                "id": "blk_step_4",
                "block_type": ContentBlockType.STEP.value,
                "title": "Step 3: Review and Conclude",
                "body": "Check your progress. You have completed the sequence successfully!",
                "visual_cue": "3️⃣",
                "order_index": 4,
                "metadata": {"step_number": 3},
            },
        ]
        summary = f"A 3-step structured progression for mastering {title}."

    elif method == ExplanationMethod.WORKED_EXAMPLE:
        blocks = [
            {
                "id": "blk_we_1",
                "block_type": ContentBlockType.HEADING.value,
                "title": f"Worked Example: {title}",
                "body": "Here is a complete demonstration showing how this concept works in practice.",
                "visual_cue": "📝",
                "order_index": 1,
                "metadata": {},
            },
            {
                "id": "blk_we_2",
                "block_type": ContentBlockType.WORKED_EXAMPLE.value,
                "title": "Example Scenario",
                "body": f"Scenario: Suppose we want to demonstrate {title}. First, we inspect the available items. Next, we apply the rule. Result: We arrive at the exact match accurately.",
                "visual_cue": "✨",
                "order_index": 2,
                "metadata": {"highlight": "accurate_completion"},
            },
            {
                "id": "blk_we_3",
                "block_type": ContentBlockType.TEXT.value,
                "title": "Why This Works",
                "body": "By taking it one step at a time, we ensure no mistakes are made along the way.",
                "visual_cue": "🎯",
                "order_index": 3,
                "metadata": {},
            },
            {
                "id": "blk_we_4",
                "block_type": ContentBlockType.CALLOUT.value,
                "title": "Takeaway",
                "body": f"You can apply this same approach whenever you practice {title}.",
                "visual_cue": "🌟",
                "order_index": 4,
                "metadata": {},
            },
        ]
        summary = f"A complete worked demonstration explaining the thought process behind {title}."

    else:  # TEXT_EXPLANATION
        blocks = [
            {
                "id": "blk_txt_1",
                "block_type": ContentBlockType.HEADING.value,
                "title": f"Understanding {title}",
                "body": f"A simple, clear explanation of {title}.",
                "visual_cue": "📖",
                "order_index": 1,
                "metadata": {},
            },
            {
                "id": "blk_txt_2",
                "block_type": ContentBlockType.TEXT.value,
                "title": "What Does This Mean?",
                "body": f"{title} helps us understand important relationships in our daily learning. When we understand this, other concepts become much easier.",
                "visual_cue": "💡",
                "order_index": 2,
                "metadata": {},
            },
            {
                "id": "blk_txt_3",
                "block_type": ContentBlockType.TEXT.value,
                "title": "Everyday Connection",
                "body": f"We see examples of {title} in our everyday routines, school activities, and quiet practice sessions.",
                "visual_cue": "🌱",
                "order_index": 3,
                "metadata": {},
            },
            {
                "id": "blk_txt_4",
                "block_type": ContentBlockType.CALLOUT.value,
                "title": "Remember",
                "body": "Take your time, read each part with calm focus, and enjoy discovering new ideas.",
                "visual_cue": "🌿",
                "order_index": 4,
                "metadata": {},
            },
        ]
        summary = f"A straightforward text overview explaining the fundamentals of {title}."

    return {
        "title": f"{title} — Explanation",
        "explanation_method": method.value,
        "difficulty_level": difficulty_level,
        "language": language,
        "summary": summary,
        "blocks": blocks,
    }


class InstructionalService:
    """Business logic service for generating and managing Instructional Content."""

    def __init__(
        self,
        session: AsyncSession,
        orchestrator: AIOrchestrator | None = None,
    ) -> None:
        self.session = session
        self._orchestrator = orchestrator

    @property
    def orchestrator(self) -> AIOrchestrator:
        if self._orchestrator is None:
            self._orchestrator = get_ai_orchestrator()
        return self._orchestrator

    async def generate(
        self,
        request: InstructionalGenerateRequest,
        current_user: User,
    ) -> InstructionalGenerateResponse:
        """
        Generate structured instructional content for an objective using Gemini + RAG,
        with seamless deterministic fallback. Persisted with status 'review_required'.
        """
        curriculum_service = CurriculumService(self.session)
        objective = await curriculum_service.get_learning_objective(request.objective_id)
        if not objective:
            raise NotFoundError(f"Learning objective with id '{request.objective_id}' not found.")

        obj_title = _extract_text(objective.title, request.language)
        obj_desc = _extract_text(objective.description, request.language) if objective.description else None

        fallback_used = False
        generation_source = "deterministic_fallback"
        grounding_sources: list[dict[str, Any]] = []
        payload: dict[str, Any] | None = None

        if self.orchestrator.is_available:
            try:
                # Retrieve RAG pedagogical context
                grounding_chunks = []
                try:
                    from app.knowledge.retrieval import get_knowledge_retrieval_service
                    retrieval_service = get_knowledge_retrieval_service()
                    grounding_chunks = await retrieval_service.retrieve_pedagogical_context(
                        query=f"{obj_title} {request.explanation_method.value}".strip(),
                        top_k=3,
                    )
                    for c in grounding_chunks:
                        grounding_sources.append({
                            "chunk_id": c.chunk_id,
                            "title": c.document_title,
                            "source": c.source,
                            "category": c.category,
                            "score": c.score,
                            "excerpt": c.content[:200],
                        })
                except Exception as rag_err:
                    logger.warning("rag_retrieval_skipped_in_instructional", error=str(rag_err))

                # Fetch authoritative content for grounding
                bank = get_content_bank()
                auth_items = bank.get_items_for_objective(request.objective_id, count=1)
                auth_payload = None
                if auth_items:
                    item0 = auth_items[0]
                    auth_payload = {
                        "prompt": item0.get_prompt(request.language),
                        "correct_answer": item0.correct_answer,
                    }

                from app.ai.generation.prompts import compile_instructional_prompt
                from app.ai.providers.base import Message, MessageRole

                compiled = compile_instructional_prompt(
                    objective_title=obj_title,
                    objective_description=obj_desc,
                    explanation_method=request.explanation_method.value,
                    difficulty_level=request.difficulty_level,
                    language=request.language,
                    authoritative_content=auth_payload,
                    grounding_chunks=grounding_chunks,
                    teacher_instructions=request.teacher_instructions,
                )

                messages = [
                    Message(role=MessageRole.SYSTEM, content=compiled.system_prompt),
                    Message(role=MessageRole.USER, content=compiled.user_prompt),
                ]

                output_schema = {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "explanation_method": {"type": "string"},
                        "summary": {"type": "string"},
                        "blocks": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "block_type": {"type": "string"},
                                    "title": {"type": "string"},
                                    "body": {"type": "string"},
                                    "visual_cue": {"type": "string"},
                                    "order_index": {"type": "integer"},
                                    "metadata": {"type": "object"},
                                },
                                "required": ["id", "block_type", "body", "order_index"],
                            },
                        },
                    },
                    "required": ["title", "explanation_method", "summary", "blocks"],
                }

                raw = await self.orchestrator.generate_structured(messages=messages, output_schema=output_schema)
                if raw and isinstance(raw.get("blocks"), list) and len(raw["blocks"]) > 0:
                    payload = raw
                    generation_source = self.orchestrator.provider.provider_name
                    fallback_used = False
            except Exception as llm_err:
                logger.warning("instructional_generation_llm_failed_falling_back", error=str(llm_err))

        if payload is None:
            fallback_used = True
            generation_source = "deterministic_fallback"
            payload = create_fallback_instructional_content(
                objective_id=request.objective_id,
                objective_title=obj_title,
                objective_description=obj_desc,
                method=request.explanation_method,
                difficulty_level=request.difficulty_level,
                language=request.language,
            )

        # Validate blocks into InstructionalBlock schemas
        blocks_data: list[InstructionalBlock] = []
        for idx, b in enumerate(payload.get("blocks", []), start=1):
            block_type_str = b.get("block_type", "text")
            try:
                b_type = ContentBlockType(block_type_str)
            except ValueError:
                b_type = ContentBlockType.TEXT

            blocks_data.append(
                InstructionalBlock(
                    id=b.get("id") or f"blk_{idx}",
                    block_type=b_type,
                    title=b.get("title"),
                    body=b.get("body", ""),
                    visual_cue=b.get("visual_cue"),
                    order_index=b.get("order_index", idx),
                    metadata=b.get("metadata", {}),
                )
            )

        now = datetime.now(timezone.utc)
        record = InstructionalContent(
            id=uuid.uuid4(),
            objective_id=request.objective_id,
            title=payload.get("title") or f"{obj_title} — Explanation",
            explanation_method=request.explanation_method.value,
            difficulty_level=request.difficulty_level,
            language=request.language,
            blocks=[b.model_dump() for b in blocks_data],
            summary=payload.get("summary") or "Instructional explanation.",
            status=InstructionalStatus.REVIEW_REQUIRED.value,
            teacher_notes=request.teacher_instructions,
            created_by=current_user.id,
            metadata_info={
                "fallback_used": fallback_used,
                "generation_source": generation_source,
                "grounding_sources_count": len(grounding_sources),
            },
            created_at=now,
            updated_at=now,
        )

        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)

        read_model = self._to_read_model(record)
        return InstructionalGenerateResponse(
            content=read_model,
            fallback_used=fallback_used,
            generation_source=generation_source,
            objective_id=request.objective_id,
            grounding_sources=grounding_sources,
        )

    async def get_by_id(self, content_id: uuid.UUID) -> InstructionalContentRead:
        stmt = select(InstructionalContent).where(InstructionalContent.id == content_id)
        res = await self.session.execute(stmt)
        record = res.scalars().first()
        if not record:
            raise NotFoundError(f"Instructional content with id '{content_id}' not found.")
        return self._to_read_model(record)

    async def get_by_objective(
        self,
        objective_id: uuid.UUID,
        published_only: bool = True,
    ) -> list[InstructionalContentRead]:
        """
        Retrieve instructional content items for an objective.
        For learners (published_only=True), returns approved/published items.
        If none found and published_only=True, generates a deterministic zero-strand approved item!
        """
        stmt = select(InstructionalContent).where(InstructionalContent.objective_id == objective_id)
        if published_only:
            stmt = stmt.where(InstructionalContent.status.in_([
                InstructionalStatus.APPROVED.value,
                InstructionalStatus.PUBLISHED.value,
            ]))
        stmt = stmt.order_by(desc(InstructionalContent.created_at))

        res = await self.session.execute(stmt)
        records = list(res.scalars().all())

        if not records and published_only:
            # Zero-strand guarantee: synthesize an approved default instructional item
            curriculum_service = CurriculumService(self.session)
            objective = await curriculum_service.get_learning_objective(objective_id)
            obj_title = _extract_text(objective.title) if objective else "Learning Concept"
            obj_desc = _extract_text(objective.description) if objective and objective.description else None

            synth = create_fallback_instructional_content(
                objective_id=objective_id,
                objective_title=obj_title,
                objective_description=obj_desc,
                method=ExplanationMethod.STEP_BY_STEP,
                difficulty_level=getattr(objective, "difficulty_level", 1) or 1,
            )
            now = datetime.now(timezone.utc)
            auto_rec = InstructionalContent(
                id=uuid.uuid4(),
                objective_id=objective_id,
                title=synth["title"],
                explanation_method=synth["explanation_method"],
                difficulty_level=synth["difficulty_level"],
                language=synth["language"],
                blocks=synth["blocks"],
                summary=synth["summary"],
                status=InstructionalStatus.APPROVED.value,
                created_at=now,
                updated_at=now,
            )
            self.session.add(auto_rec)
            await self.session.commit()
            await self.session.refresh(auto_rec)
            return [self._to_read_model(auto_rec)]

        return [self._to_read_model(r) for r in records]

    async def update(
        self,
        content_id: uuid.UUID,
        update_in: InstructionalContentUpdate,
        current_user: User,
    ) -> InstructionalContentRead:
        stmt = select(InstructionalContent).where(InstructionalContent.id == content_id)
        res = await self.session.execute(stmt)
        record = res.scalars().first()
        if not record:
            raise NotFoundError(f"Instructional content with id '{content_id}' not found.")

        if update_in.title is not None:
            record.title = update_in.title
        if update_in.summary is not None:
            record.summary = update_in.summary
        if update_in.teacher_notes is not None:
            record.teacher_notes = update_in.teacher_notes
        if update_in.blocks is not None:
            record.blocks = [b.model_dump() for b in update_in.blocks]
        if update_in.status is not None:
            record.status = update_in.status.value

        record.updated_at = datetime.now(timezone.utc)
        await self.session.commit()
        await self.session.refresh(record)
        return self._to_read_model(record)

    async def approve(self, content_id: uuid.UUID, current_user: User) -> InstructionalContentRead:
        stmt = select(InstructionalContent).where(InstructionalContent.id == content_id)
        res = await self.session.execute(stmt)
        record = res.scalars().first()
        if not record:
            raise NotFoundError(f"Instructional content with id '{content_id}' not found.")

        record.status = InstructionalStatus.APPROVED.value
        record.updated_at = datetime.now(timezone.utc)
        await self.session.commit()
        await self.session.refresh(record)
        return self._to_read_model(record)

    async def publish(self, content_id: uuid.UUID, current_user: User) -> InstructionalContentRead:
        stmt = select(InstructionalContent).where(InstructionalContent.id == content_id)
        res = await self.session.execute(stmt)
        record = res.scalars().first()
        if not record:
            raise NotFoundError(f"Instructional content with id '{content_id}' not found.")

        record.status = InstructionalStatus.PUBLISHED.value
        record.updated_at = datetime.now(timezone.utc)
        await self.session.commit()
        await self.session.refresh(record)
        return self._to_read_model(record)

    def _to_read_model(self, record: InstructionalContent) -> InstructionalContentRead:
        blocks = []
        for b in (record.blocks or []):
            try:
                b_type = ContentBlockType(b.get("block_type", "text"))
            except ValueError:
                b_type = ContentBlockType.TEXT
            blocks.append(
                InstructionalBlock(
                    id=b.get("id") or "b1",
                    block_type=b_type,
                    title=b.get("title"),
                    body=b.get("body", ""),
                    visual_cue=b.get("visual_cue"),
                    order_index=b.get("order_index", 1),
                    metadata=b.get("metadata", {}),
                )
            )

        return InstructionalContentRead(
            id=record.id,
            objective_id=record.objective_id,
            title=record.title,
            explanation_method=ExplanationMethod(record.explanation_method),
            difficulty_level=record.difficulty_level,
            language=record.language,
            blocks=blocks,
            summary=record.summary,
            status=InstructionalStatus(record.status),
            teacher_notes=record.teacher_notes,
            created_by=record.created_by,
            metadata=record.metadata_info or {},
            created_at=record.created_at,
            updated_at=record.updated_at,
        )
