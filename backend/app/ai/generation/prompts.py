"""
Eduvia — Structured Prompt Compiler for Activity & Lesson Generation (Phase 4 & Phase 8)

Translates GenerationSpec, curriculum objectives, authoritative ContentBank facts,
retrieved RAG pedagogical knowledge, and teacher-controlled custom instructions into
rigorously structured prompts for the AI Orchestrator / Gemini Provider.

Enforces clear prompt ownership boundaries:
- Immutable System Rules: Cognitive Calm, Zero-Strand Guarantee, safety, schema contracts,
  authoritative ground truth from Content Bank, and Phase 8 adaptive sovereign decisions.
- Teacher-Controlled Parameters: custom framing instructions, visual preferences,
  interaction styles, scaffolding tier, and item count.
"""
from __future__ import annotations

import json
from typing import Any

from app.activities.schemas import (
    Activity,
    ActivityGenerateRequest,
    ActivityType,
    EffectiveGenerationPrompt,
    LessonPlan,
)
from app.ai.providers.base import Message, MessageRole


IMMUTABLE_PROMPT_SECTIONS = [
    "SYSTEM RULES",
    "CURRICULUM CONTEXT",
    "AUTHORITATIVE CONTENT",
    "ADAPTIVE DECISION",
    "OUTPUT JSON CONTRACT",
]


def compile_generation_prompt(
    spec: ActivityGenerateRequest,
    objective_title: str,
    objective_description: str | None = None,
    curriculum_context: dict[str, str] | None = None,
    assessment_criteria: dict[str, Any] | None = None,
    learner_context: dict[str, Any] | None = None,
    grounding_chunks: list[Any] | None = None,
    authoritative_content: dict[str, Any] | None = None,
    phase8_decision: dict[str, Any] | None = None,
) -> EffectiveGenerationPrompt:
    """
    Structured Prompt Compiler.

    Transforms a GenerationSpec and surrounding pedagogical context into an
    EffectiveGenerationPrompt with 10 strictly isolated sections.
    """
    act_type = spec.activity_type or ActivityType.MULTIPLE_CHOICE
    target_difficulty = spec.difficulty_level or 1
    if spec.phase8_locked_difficulty is not None:
        target_difficulty = spec.phase8_locked_difficulty
    target_difficulty = max(1, min(5, target_difficulty))

    sections: dict[str, str] = {}

    # 1. SYSTEM RULES (Immutable)
    sections["SYSTEM RULES"] = (
        "You are Eduvia's expert pedagogical Activity Generation Engine.\n"
        "Your task is to generate an interactive, accessible learning activity for a student "
        "focusing strictly on foundational mastery.\n\n"
        "CORE PEDAGOGICAL INVARIANTS:\n"
        "1. Cognitive Calm: Use concise, distraction-free language. Avoid overly busy or sensory-overloading instructions.\n"
        "2. Positive Framing: State what to do clearly, avoiding complex negatives or confusing syntax.\n"
        "3. Accessible Distractors: In multiple-choice or visual identification, distractors should represent common "
        "instructional approximations without being tricky or frustrating.\n"
        "4. Scaffolding: Provide 2 to 3 graded hints (Hint 1: gentle nudge; Hint 2: specific clue; Hint 3: direct guidance).\n"
        "5. Language: All learner-facing text (title, instructions, prompts, options, explanation) must be in the specified language.\n"
        "6. Sovereign Correctness: Never invent alternative answers that contradict the authoritative educational ground truth.\n"
        "7. Zero-Strand Guarantee: Output must be strictly valid JSON conforming to the activity schema."
    )

    # 2. CURRICULUM CONTEXT (Immutable)
    curr_parts = [
        f"- Objective Title: {objective_title}",
        f"- Objective Description: {objective_description or 'Focus on foundational mastery.'}",
    ]
    if curriculum_context:
        if curriculum_context.get("subject"):
            curr_parts.append(f"- Subject: {curriculum_context['subject']}")
        if curriculum_context.get("unit"):
            curr_parts.append(f"- Unit: {curriculum_context['unit']}")
        if curriculum_context.get("lesson"):
            curr_parts.append(f"- Lesson: {curriculum_context['lesson']}")
    if assessment_criteria:
        curr_parts.append(f"- Mastery Criteria: {json.dumps(assessment_criteria)}")
    sections["CURRICULUM CONTEXT"] = "\n".join(curr_parts)

    # 3. LEARNER CONTEXT
    learner_parts = [
        f"- Target Learner: {'Individualized' if spec.learner_id else 'Cohort/Standard'}",
    ]
    if learner_context:
        comm_pref = learner_context.get("communication_preferences", {})
        support_req = learner_context.get("support_requirements", {})
        learner_parts.extend([
            f"- Communication Mode: {comm_pref.get('primary_mode', 'standard')}",
            f"- Guidance Level: {support_req.get('guidance_level', 'moderate')}",
            f"- Pacing: {support_req.get('pacing', 'standard')}",
        ])
        teacher_constraints = learner_context.get("teacher_constraints", {})
        if teacher_constraints.get("custom_guidelines"):
            learner_parts.append(f"- Teacher Guidelines: {teacher_constraints['custom_guidelines']}")
    sections["LEARNER CONTEXT"] = "\n".join(learner_parts)

    # 4. TEACHER PARAMETERS (Configured)
    sections["TEACHER PARAMETERS"] = (
        f"- Modality: {act_type.value}\n"
        f"- Difficulty Level: Level {target_difficulty} (scale 1 to 5)\n"
        f"- Target Item/Question Count: {spec.item_count}\n"
        f"- Language: {spec.language}\n"
        f"- Visual Style: {spec.visual_style}\n"
        f"- Scaffolding Level: Level {spec.scaffolding_level} (0=none, 1=gentle, 2=guided, 3=explicit)\n"
        f"- Interaction Style: {spec.interaction_style}\n"
        f"- Seed / Variation: {spec.seed if spec.seed is not None else 0}"
    )

    # 5. TEACHER INSTRUCTIONS (Teacher-Owned & Editable)
    teacher_inst = (spec.teacher_instructions or "").strip()
    if not teacher_inst:
        teacher_inst = "Standard curriculum-aligned instructional delivery. No custom teacher restrictions."
    sections["TEACHER INSTRUCTIONS"] = teacher_inst

    # 6. AUTHORITATIVE CONTENT (Immutable Truth)
    if authoritative_content:
        sections["AUTHORITATIVE CONTENT"] = (
            f"- Ground Truth Prompt/Fact: {authoritative_content.get('prompt')}\n"
            f"- Correct Answer: {authoritative_content.get('correct_answer')}\n"
            f"- Reference Payload: {json.dumps(authoritative_content.get('content_payload', {}))}\n"
            "- Invariant Rule: Adapt presentation to match the modality, but preserve the factual truth and correct answer."
        )
    else:
        sections["AUTHORITATIVE CONTENT"] = (
            "- Base educational truth grounded in objective mastery definition.\n"
            "- Construct unambiguous, pedagogically verified questions and answers."
        )

    # 7. RAG GUIDANCE (Verified Knowledge)
    grounding_sources_summary: list[dict[str, Any]] = []
    if grounding_chunks:
        rag_passages = []
        for i, chunk in enumerate(grounding_chunks, 1):
            c_title = getattr(chunk, "document_title", None) or (chunk.get("document_title") if isinstance(chunk, dict) else f"Pedagogical Guideline {i}")
            c_source = getattr(chunk, "source", None) or (chunk.get("source") if isinstance(chunk, dict) else "knowledge_base.md")
            c_content = getattr(chunk, "content", None) or (chunk.get("content") if isinstance(chunk, dict) else str(chunk))
            c_id = getattr(chunk, "chunk_id", None) or (chunk.get("chunk_id") if isinstance(chunk, dict) else f"chunk_{i}")
            c_score = getattr(chunk, "score", None) or (chunk.get("score") if isinstance(chunk, dict) else 1.0)
            c_cat = getattr(chunk, "category", None) or (chunk.get("category") if isinstance(chunk, dict) else "pedagogy")

            rag_passages.append(f"[Source {i}: {c_title} ({c_source})]\n{c_content.strip()}")
            grounding_sources_summary.append({
                "chunk_id": str(c_id),
                "title": str(c_title),
                "source": str(c_source),
                "category": str(c_cat),
                "score": float(c_score),
                "excerpt": str(c_content)[:200],
            })
        sections["RAG GUIDANCE"] = (
            "Evidence-based pedagogical strategies retrieved for this objective:\n"
            + "\n\n".join(rag_passages)
        )
    else:
        sections["RAG GUIDANCE"] = (
            "Standard evidence-based universal design for learning (UDL) principles:\n"
            "- Provide multiple means of representation.\n"
            "- Scaffold complex operations into progressive sub-tasks.\n"
            "- Ensure immediate, constructive, non-punitive feedback."
        )

    # 8. ADAPTIVE DECISION (Phase 8 Sovereign Authority)
    adaptive_notes = []
    if spec.phase8_locked_difficulty is not None:
        adaptive_notes.append(f"- Difficulty Locked by Adaptive Engine: Level {spec.phase8_locked_difficulty}")
    if phase8_decision:
        for k, v in phase8_decision.items():
            adaptive_notes.append(f"- {k}: {v}")
    if not adaptive_notes:
        adaptive_notes.append("- No active adaptive locks. Teacher parameters are sovereign within curriculum limits.")
    sections["ADAPTIVE DECISION"] = "\n".join(adaptive_notes)

    # 9. ACTIVITY-SPECIFIC RULES
    modality_rules = {
        ActivityType.MULTIPLE_CHOICE: (
            f"- Generate a question with exactly {min(5, max(2, spec.item_count))} options.\n"
            "- Exactly 1 option must have is_correct=True; all others is_correct=False.\n"
            "- Provide educational distractor_rationale for incorrect options explaining common misconceptions.\n"
            "- Include an encouraging explanation revealed after answering."
        ),
        ActivityType.MATCHING: (
            f"- Generate exactly {min(6, max(2, spec.item_count))} distinct pairs of items to match.\n"
            "- left_items and right_items must have unique IDs and corresponding correct_pairs.\n"
            "- Clear, unambiguous 1-to-1 correspondences."
        ),
        ActivityType.ORDERING: (
            f"- Generate {min(6, max(3, spec.item_count))} items to arrange in a clear, definite order.\n"
            "- correct_order must specify the ascending, progressive, or chronological sequence.\n"
            "- order_criterion must describe the ordering rule in calm, simple student language."
        ),
        ActivityType.VISUAL_IDENTIFICATION: (
            f"- Define an accessible visual scene containing {min(6, max(2, spec.item_count))} visual elements.\n"
            "- Exactly 1 element is the target_element_id matching the target prompt.\n"
            "- Use high-contrast, uncluttered visual cue descriptions."
        ),
        ActivityType.DRAG_DROP: (
            f"- Define 2 to 3 distinct drop zones and {min(6, max(2, spec.item_count))} draggable items.\n"
            "- correct_mapping must map every drag item ID to its correct target drop zone ID."
        ),
    }
    sections["ACTIVITY-SPECIFIC RULES"] = modality_rules.get(
        act_type,
        "- Ensure valid schema compliance for the requested activity type."
    )

    # 10. OUTPUT JSON CONTRACT (Immutable)
    sections["OUTPUT JSON CONTRACT"] = (
        "Respond with a single JSON object conforming to the Activity schema:\n"
        "{\n"
        '  "title": "Short calm title",\n'
        '  "instructions": "Simple 1-2 sentence instruction",\n'
        f'  "difficulty_level": {target_difficulty},\n'
        f'  "activity_type": "{act_type.value}",\n'
        '  "content": { ...activity-type specific content object... },\n'
        '  "hints": ["Hint 1 (nudge)", "Hint 2 (clue)", "Hint 3 (direct)"],\n'
        f'  "scaffolding_level": {spec.scaffolding_level}\n'
        "}\n"
        "Do not wrap in markdown or include conversational text."
    )

    # Assemble full readable prompt preview
    preview_blocks = []
    for title, content in sections.items():
        is_imm = " (Immutable)" if title in IMMUTABLE_PROMPT_SECTIONS else ""
        if title == "TEACHER INSTRUCTIONS":
            is_imm = " (Teacher-Owned & Editable)"
        preview_blocks.append(f"### {title}{is_imm}\n{content.strip()}")
    full_prompt_text = "\n\n".join(preview_blocks)

    # Build system and user messages
    system_prompt = (
        sections["SYSTEM RULES"]
        + "\n\n"
        + "VERIFIED PEDAGOGICAL KNOWLEDGE (Grounding Context):\n"
        + sections["RAG GUIDANCE"]
        + "\n\n"
        + "ACTIVITY CONSTRAINTS:\n"
        + sections["ACTIVITY-SPECIFIC RULES"]
    )

    user_prompt = (
        f"Generate a '{act_type.value}' activity for the following objective:\n\n"
        f"CURRICULUM:\n{sections['CURRICULUM CONTEXT']}\n\n"
        f"LEARNER CONTEXT:\n{sections['LEARNER CONTEXT']}\n\n"
        f"TEACHER PARAMETERS:\n{sections['TEACHER PARAMETERS']}\n\n"
        f"TEACHER INSTRUCTIONS:\n{sections['TEACHER INSTRUCTIONS']}\n\n"
        f"AUTHORITATIVE CONTENT GROUNDING:\n{sections['AUTHORITATIVE CONTENT']}\n\n"
        f"ADAPTIVE DECISION:\n{sections['ADAPTIVE DECISION']}\n\n"
        f"JSON SCHEMA CONTRACT:\n{sections['OUTPUT JSON CONTRACT']}"
    )

    return EffectiveGenerationPrompt(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        full_prompt_text=full_prompt_text,
        sections=sections,
        teacher_editable_section=teacher_inst,
        immutable_sections=IMMUTABLE_PROMPT_SECTIONS,
        grounding_sources=grounding_sources_summary,
        content_bank_grounded=authoritative_content is not None,
        objective_title=objective_title,
        activity_type=act_type.value,
        difficulty_level=target_difficulty,
    )


def compile_lesson_prompt(
    spec: ActivityGenerateRequest,
    objective_title: str,
    objective_description: str | None = None,
    curriculum_context: dict[str, str] | None = None,
    grounding_chunks: list[Any] | None = None,
    authoritative_content: dict[str, Any] | None = None,
) -> EffectiveGenerationPrompt:
    """
    Compile a structured prompt for a 10-minute mini-lesson plan.
    Enforces lesson phases: Warm-up, Demonstration, Guided Practice, Independent Practice, Recap.
    """
    sections: dict[str, str] = {}

    sections["SYSTEM RULES"] = (
        "You are Eduvia's expert Lesson Planning Engine.\n"
        "Your task is to generate a structured, calibrated 10-minute mini-lesson plan for teachers.\n"
        "CORE PHASES:\n"
        "1. Introduction / Warm-up (2 min): Hook learner curiosity and activate prior knowledge.\n"
        "2. Demonstration / 'I Do' (3 min): Teacher explicitly models the concept using concrete visuals.\n"
        "3. Guided Practice / 'We Do' (3 min): Interactive collaboration with low-stakes scaffolded checks.\n"
        "4. Independent Practice / 'You Do' (2 min): Student applies the skill with tailored scaffolding.\n"
        "5. Recap & Exit Check: Positive closure reinforcing foundational mastery."
    )

    curr_text = f"- Objective: {objective_title}\n- Details: {objective_description or 'Foundational mastery.'}"
    if curriculum_context:
        curr_text += f"\n- Subject: {curriculum_context.get('subject', 'General')}"
    sections["CURRICULUM CONTEXT"] = curr_text

    sections["TEACHER PARAMETERS"] = (
        f"- Target Duration: 10 minutes\n"
        f"- Target Difficulty: Level {spec.difficulty_level or 1}\n"
        f"- Language: {spec.language}\n"
        f"- Visual Style: {spec.visual_style}\n"
        f"- Scaffolding Level: Level {spec.scaffolding_level}"
    )

    t_inst = (spec.teacher_instructions or "").strip() or "Standard direct instruction with hands-on practice."
    sections["TEACHER INSTRUCTIONS"] = t_inst

    if authoritative_content:
        sections["AUTHORITATIVE CONTENT"] = (
            f"- Core Educational Fact: {authoritative_content.get('prompt')}\n"
            f"- Ground Truth: {authoritative_content.get('correct_answer')}"
        )
    else:
        sections["AUTHORITATIVE CONTENT"] = "- Ground truth aligned with standard curriculum objective."

    rag_summary: list[dict[str, Any]] = []
    if grounding_chunks:
        rag_passages = []
        for i, chunk in enumerate(grounding_chunks, 1):
            c_title = getattr(chunk, "document_title", None) or f"Lesson Strategy {i}"
            c_content = getattr(chunk, "content", None) or str(chunk)
            rag_passages.append(f"[Source {i}: {c_title}]\n{c_content.strip()}")
            rag_summary.append({
                "chunk_id": f"lesson_chunk_{i}",
                "title": str(c_title),
                "source": "knowledge_base",
                "category": "lesson_design",
                "score": 1.0,
                "excerpt": str(c_content)[:200],
            })
        sections["RAG GUIDANCE"] = "\n\n".join(rag_passages)
    else:
        sections["RAG GUIDANCE"] = "Gradual Release of Responsibility (I Do, We Do, You Do) framework."

    sections["OUTPUT JSON CONTRACT"] = (
        "Respond with a single JSON object conforming to the LessonPlan schema:\n"
        "{\n"
        '  "title": "Clear lesson title",\n'
        f'  "objective": "{objective_title}",\n'
        '  "duration_minutes": 10,\n'
        '  "introduction": "Warm-up hook description",\n'
        '  "demonstration": "Modeling explanation",\n'
        '  "guided_practice": "Interactive check description",\n'
        '  "independent_practice": "Hands-on practice task",\n'
        '  "scaffolding": "Tiered support instructions",\n'
        '  "teacher_notes": "Common misconceptions and observations",\n'
        '  "recap": "Exit summary",\n'
        f'  "suggested_activity_type": "{(spec.activity_type or ActivityType.MULTIPLE_CHOICE).value}"\n'
        "}\n"
        "Do not wrap in markdown or include conversational text."
    )

    preview_blocks = [f"### {k}\n{v.strip()}" for k, v in sections.items()]
    full_prompt_text = "\n\n".join(preview_blocks)

    system_prompt = sections["SYSTEM RULES"] + "\n\n" + sections["RAG GUIDANCE"]
    user_prompt = (
        f"Generate a 10-minute mini-lesson plan for:\n"
        f"{sections['CURRICULUM CONTEXT']}\n\n"
        f"TEACHER INSTRUCTIONS:\n{sections['TEACHER INSTRUCTIONS']}\n\n"
        f"AUTHORITATIVE CONTENT:\n{sections['AUTHORITATIVE CONTENT']}\n\n"
        f"{sections['OUTPUT JSON CONTRACT']}"
    )

    return EffectiveGenerationPrompt(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        full_prompt_text=full_prompt_text,
        sections=sections,
        teacher_editable_section=t_inst,
        immutable_sections=IMMUTABLE_PROMPT_SECTIONS,
        grounding_sources=rag_summary,
        content_bank_grounded=authoritative_content is not None,
        objective_title=objective_title,
        activity_type=(spec.activity_type or ActivityType.MULTIPLE_CHOICE).value,
        difficulty_level=spec.difficulty_level or 1,
    )


def build_activity_generation_messages(
    objective_title: str,
    objective_description: str | None,
    difficulty_level: int,
    activity_type: ActivityType,
    assessment_criteria: dict[str, Any] | None = None,
    learner_context: dict[str, Any] | None = None,
    language: str = "en",
    grounding_chunks: list[Any] | None = None,
    authoritative_content: dict[str, Any] | None = None,
    teacher_instructions: str | None = None,
    item_count: int = 4,
    visual_style: str = "calm",
    scaffolding_level: int = 1,
    interaction_style: str = "direct",
    seed: int | None = None,
) -> list[Message]:
    """
    Backward-compatible wrapper around compile_generation_prompt().
    """
    spec = ActivityGenerateRequest(
        objective_id=authoritative_content.get("objective_id", "00000000-0000-0000-0000-000000000000")
        if authoritative_content and "objective_id" in authoritative_content
        else "00000000-0000-0000-0000-000000000000",
        activity_type=activity_type,
        difficulty_level=difficulty_level,
        item_count=item_count,
        language=language,
        visual_style=visual_style,
        scaffolding_level=scaffolding_level,
        interaction_style=interaction_style,
        teacher_instructions=teacher_instructions,
        seed=seed,
    )

    compiled = compile_generation_prompt(
        spec=spec,
        objective_title=objective_title,
        objective_description=objective_description,
        assessment_criteria=assessment_criteria,
        learner_context=learner_context,
        grounding_chunks=grounding_chunks,
        authoritative_content=authoritative_content,
    )

    return [
        Message(role=MessageRole.SYSTEM, content=compiled.system_prompt),
        Message(role=MessageRole.USER, content=compiled.user_prompt),
    ]
