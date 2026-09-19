"""
Eduvia — System Prompts & Context Builder for Activity Generation (Phase 4)

Translates curriculum objectives and learner profile context into structured
prompts for the AI Orchestrator / LLM Provider.

Adheres strictly to:
- Cognitive calm principles: concise wording, sensory-safe language, constructive feedback
- Educational terminology only (no diagnostic or deficit labels)
- Preservation of teacher authority and explicit constraints
"""
from __future__ import annotations

from typing import Any

from app.activities.schemas import ActivityType
from app.ai.providers.base import Message, MessageRole


def build_activity_generation_messages(
    objective_title: str,
    objective_description: str | None,
    difficulty_level: int,
    activity_type: ActivityType,
    assessment_criteria: dict[str, Any] | None = None,
    learner_context: dict[str, Any] | None = None,
    language: str = "en",
) -> list[Message]:
    """
    Construct system and user messages for structured activity generation.
    """
    system_prompt = (
        "You are Eduvia's expert pedagogical Activity Generation Engine. "
        "Your task is to generate an interactive, accessible learning activity for a student "
        "focusing strictly on foundational mastery.\n\n"
        "CORE PEDAGOGICAL PRINCIPLES:\n"
        "1. Cognitive Calm: Use concise, distraction-free language. Avoid overly busy or sensory-overloading instructions.\n"
        "2. Positive Framing: State what to do clearly, avoiding complex negatives or confusing syntax.\n"
        "3. Accessible Distractors: In multiple-choice or visual identification, distractors should represent common "
        "instructional approximations without being tricky or frustrating.\n"
        "4. Scaffolding: Provide 2 to 3 graded hints (Hint 1: gentle nudge; Hint 2: specific clue; Hint 3: direct guidance).\n"
        "5. Language: All learner-facing text (title, instructions, prompts, options, explanation) must be in the specified language.\n"
    )

    # Format learner profile context safely if provided
    learner_notes = ""
    if learner_context:
        comm_pref = learner_context.get("communication_preferences", {})
        support_req = learner_context.get("support_requirements", {})
        constraints = learner_context.get("teacher_constraints", {})

        learner_notes = (
            f"\nLEARNER CONSIDERATIONS (Respect strictly):\n"
            f"- Communication Mode: {comm_pref.get('primary_mode', 'standard')}\n"
            f"- Guidance Level: {support_req.get('guidance_level', 'moderate')}\n"
            f"- Pacing: {support_req.get('pacing', 'standard')}\n"
            f"- Teacher Custom Guidelines: {constraints.get('custom_guidelines', 'None specified')}\n"
        )

    user_prompt = (
        f"Generate a '{activity_type.value}' activity.\n\n"
        f"LEARNING OBJECTIVE:\n"
        f"- Title: {objective_title}\n"
        f"- Description: {objective_description or 'Focus on foundational understanding.'}\n"
        f"- Target Difficulty: Level {difficulty_level} (scale 1 to 5)\n"
        f"- Target Language: {language}\n"
        f"{learner_notes}\n"
        f"FORMAT REQUIREMENTS:\n"
        f"Ensure your output contains:\n"
        f"- title: A calm, encouraging short title\n"
        f"- instructions: Clear 1-2 sentence instructions for the student\n"
        f"- difficulty_level: {difficulty_level}\n"
        f"- activity_type: '{activity_type.value}'\n"
        f"- content: Object conforming precisely to the '{activity_type.value}' schema\n"
        f"- hints: Array of 2-3 graded helpful hints\n"
        f"- scaffolding_level: 1\n"
    )

    return [
        Message(role=MessageRole.SYSTEM, content=system_prompt),
        Message(role=MessageRole.USER, content=user_prompt),
    ]
