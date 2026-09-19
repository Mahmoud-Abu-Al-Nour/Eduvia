"""
Tests for RAG-grounded Activity Generation (Phase 9).

Verifies that retrieved knowledge passages are injected into prompts,
source attribution is tracked in responses, and Zero-Strand fallbacks are preserved.
"""
from __future__ import annotations

import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from app.activities.schemas import ActivityGenerateRequest, ActivityType
from app.activities.service import ActivityService
from app.ai.generation.prompts import build_activity_generation_messages
from app.ai.providers.base import MessageRole
from app.curriculum.models import LearningObjective
from app.knowledge.schemas import RetrievedChunk
from app.users.models import User, UserRole


class TestRAGGroundedGeneration:
    """Test grounding prompt assembly and ActivityService RAG integration."""

    def test_build_activity_generation_messages_injects_rag_passages(self) -> None:
        """Prompt builder should inject verified pedagogical knowledge into system prompt."""
        chunks = [
            RetrievedChunk(
                chunk_id="chk-1",
                document_title="Teaching Strategies for SEN",
                source="teaching_strategies.md",
                category="strategy",
                content="Step-by-step instruction: break each counting task into discrete visual units.",
                score=0.91,
            )
        ]

        messages = build_activity_generation_messages(
            objective_title="Recognize Numbers 1 to 5",
            objective_description="Identify numerals visually",
            difficulty_level=1,
            activity_type=ActivityType.MULTIPLE_CHOICE,
            grounding_chunks=chunks,
        )

        assert len(messages) == 2
        system_msg = messages[0]
        assert system_msg.role == MessageRole.SYSTEM
        assert "VERIFIED PEDAGOGICAL KNOWLEDGE (Grounding Context)" in system_msg.content
        assert "Teaching Strategies for SEN" in system_msg.content
        assert "break each counting task into discrete visual units" in system_msg.content

    @pytest.mark.asyncio
    async def test_activity_service_populates_grounding_sources(self) -> None:
        """ActivityService.generate_activity should include retrieved grounding sources in response."""
        obj_id = uuid.uuid4()
        mock_objective = LearningObjective(
            id=obj_id,
            lesson_id=uuid.uuid4(),
            title={"en": "Basic Counting 1-5"},
            description={"en": "Match digits to items"},
            difficulty_level=1,
            is_active=True,
            order_index=1,
        )

        mock_session = AsyncMock()
        mock_session.get.return_value = mock_objective

        mock_orchestrator = MagicMock()
        mock_orchestrator.is_available = True
        mock_orchestrator.provider.provider_name = "gemini"
        mock_orchestrator.generate_structured = AsyncMock(
            return_value={
                "id": str(uuid.uuid4()),
                "objective_id": str(obj_id),
                "activity_type": "multiple_choice",
                "title": "Count the Stars",
                "instructions": "Tap the number that matches.",
                "difficulty_level": 1,
                "content": {
                    "activity_type": "multiple_choice",
                    "question": "How many stars do you see?",
                    "options": [
                        {"id": "opt1", "text": "3", "is_correct": True},
                        {"id": "opt2", "text": "5", "is_correct": False},
                    ],
                    "correct_answer_id": "opt1",
                    "explanation": "There are 3 stars.",
                },
                "hints": ["Count them one by one."],
                "scaffolding_level": 1,
            }
        )

        mock_retrieval = MagicMock()
        mock_retrieval.retrieve_pedagogical_context = AsyncMock(
            return_value=[
                RetrievedChunk(
                    chunk_id="chunk-42",
                    document_title="SEN Activity Design",
                    source="activity_design_principles.md",
                    category="activity_design",
                    content="Present no more than 2-4 options for beginner learners.",
                    score=0.89,
                )
            ]
        )

        service = ActivityService(session=mock_session, orchestrator=mock_orchestrator)
        req = ActivityGenerateRequest(
            objective_id=obj_id,
            activity_type=ActivityType.MULTIPLE_CHOICE,
            difficulty_level=1,
        )
        user = User(
            id=uuid.uuid4(),
            email="teacher@eduvia.org",
            hashed_password="",
            role=UserRole.teacher,
        )

        with (
            patch(
                "app.curriculum.service.CurriculumService.get_learning_objective",
                return_value=mock_objective,
            ),
            patch(
                "app.knowledge.retrieval.get_knowledge_retrieval_service",
                return_value=mock_retrieval,
            ),
        ):
            resp = await service.generate_activity(req, user)

        assert resp.fallback_used is False
        assert resp.generation_source == "gemini"
        assert len(resp.grounding_sources) == 1
        source = resp.grounding_sources[0]
        assert source["title"] == "SEN Activity Design"
        assert source["chunk_id"] == "chunk-42"
        assert source["score"] == 0.89

    @pytest.mark.asyncio
    async def test_zero_strand_fallback_preserved_on_rag_or_llm_failure(self) -> None:
        """When LLM generation fails, deterministic fallback should succeed with empty grounding sources."""
        obj_id = uuid.uuid4()
        mock_objective = LearningObjective(
            id=obj_id,
            lesson_id=uuid.uuid4(),
            title={"en": "Basic Counting 1-5"},
            description={"en": "Match digits to items"},
            difficulty_level=1,
            is_active=True,
            order_index=1,
        )

        mock_session = AsyncMock()

        mock_orchestrator = MagicMock()
        mock_orchestrator.is_available = True
        # Simulate LLM crash/timeout
        mock_orchestrator.generate_structured = AsyncMock(side_effect=RuntimeError("LLM Timeout"))

        service = ActivityService(session=mock_session, orchestrator=mock_orchestrator)
        req = ActivityGenerateRequest(
            objective_id=obj_id,
            activity_type=ActivityType.MULTIPLE_CHOICE,
            difficulty_level=1,
        )
        user = User(
            id=uuid.uuid4(),
            email="teacher@eduvia.org",
            hashed_password="",
            role=UserRole.teacher,
        )

        with patch(
            "app.curriculum.service.CurriculumService.get_learning_objective",
            return_value=mock_objective,
        ):
            resp = await service.generate_activity(req, user)

        assert resp.fallback_used is True
        assert resp.generation_source == "deterministic_fallback"
        assert resp.grounding_sources == []
        assert resp.activity is not None

