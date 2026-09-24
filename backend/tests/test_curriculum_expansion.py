"""
Eduvia — Curriculum Expansion Verification Tests

Validates:
- 3 Subjects (Foundational Mathematics, Early Literacy, Everyday Learning Skills)
- 13 Units across the curriculum hierarchy
- ~70 Objectives with deterministic UUIDs
- Acyclic, deterministic prerequisite graph
- Bilingual (EN/AR) metadata coverage
"""
from __future__ import annotations

import uuid

import pytest

from app.curriculum.curriculum_catalog import (
    CURRICULUM_ID,
    FULL_CURRICULUM_CATALOG,
    SUBJECT_EVERYDAY_ID,
    SUBJECT_LITERACY_ID,
    SUBJECT_MATH_ID,
    get_all_curriculum_objectives,
    get_objective_by_id,
    get_prerequisites_map,
)


def test_curriculum_catalog_subjects() -> None:
    """Verify the 3 primary foundational subjects exist with proper UUIDs."""
    subject_ids = {s["id"] for s in FULL_CURRICULUM_CATALOG}
    assert SUBJECT_MATH_ID in subject_ids
    assert SUBJECT_LITERACY_ID in subject_ids
    assert SUBJECT_EVERYDAY_ID in subject_ids
    assert len(FULL_CURRICULUM_CATALOG) == 3


def test_curriculum_units_count() -> None:
    """Verify that the 13 units are correctly distributed across subjects."""
    math_subj = next(s for s in FULL_CURRICULUM_CATALOG if s["id"] == SUBJECT_MATH_ID)
    lit_subj = next(s for s in FULL_CURRICULUM_CATALOG if s["id"] == SUBJECT_LITERACY_ID)
    everyday_subj = next(s for s in FULL_CURRICULUM_CATALOG if s["id"] == SUBJECT_EVERYDAY_ID)

    assert len(math_subj["units"]) == 5  # Counting, Sequence, Addition, Subtraction, Shapes
    assert len(lit_subj["units"]) == 4   # Letters, Sounds, Words, Sequencing
    assert len(everyday_subj["units"]) == 4  # Routines, Objects, Sorting, Safety

    total_units = len(math_subj["units"]) + len(lit_subj["units"]) + len(everyday_subj["units"])
    assert total_units == 13


def test_curriculum_objectives_count_and_uniqueness() -> None:
    """Verify objective counts, valid UUIDs, and uniqueness across the catalog."""
    objectives = get_all_curriculum_objectives()
    assert len(objectives) >= 60, f"Expected at least 60 objectives, found {len(objectives)}"

    # All IDs must be valid, unique UUIDs
    ids = [o["id"] for o in objectives]
    assert len(ids) == len(set(ids)), "Duplicate objective IDs found in curriculum catalog!"
    for oid in ids:
        assert isinstance(oid, uuid.UUID)


def test_bilingual_metadata_coverage() -> None:
    """Verify all subjects, units, and objectives have both English and Arabic titles."""
    for subject in FULL_CURRICULUM_CATALOG:
        assert "en" in subject["title"] and "ar" in subject["title"]
        assert len(subject["title"]["en"]) > 0
        assert len(subject["title"]["ar"]) > 0

        for unit in subject.get("units", []):
            assert "en" in unit["title"] and "ar" in unit["title"]

            for lesson in unit.get("lessons", []):
                assert "en" in lesson["title"] and "ar" in lesson["title"]

                for obj in lesson.get("learning_objectives", []):
                    assert "en" in obj["title"] and "ar" in obj["title"]
                    assert 1 <= obj["difficulty_level"] <= 5
                    assert "minimum_accuracy" in obj["assessment_criteria"]


def test_prerequisite_graph_acyclic_and_valid() -> None:
    """Verify prerequisite links reference existing objectives and do not form cycles."""
    prereq_map = get_prerequisites_map()
    all_obj_ids = {o["id"] for o in get_all_curriculum_objectives()}

    for obj_id, prereqs in prereq_map.items():
        assert obj_id in all_obj_ids, f"Prerequisite source {obj_id} not in catalog"
        for p_id in prereqs:
            assert p_id in all_obj_ids, f"Prerequisite target {p_id} not in catalog"
            assert p_id != obj_id, f"Self-referential prerequisite detected on {obj_id}"

    # Cycle detection via DFS
    visited: set[uuid.UUID] = set()
    rec_stack: set[uuid.UUID] = set()

    def has_cycle(node: uuid.UUID) -> bool:
        visited.add(node)
        rec_stack.add(node)
        for neighbor in prereq_map.get(node, []):
            if neighbor not in visited:
                if has_cycle(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True
        rec_stack.remove(node)
        return False

    for obj_id in all_obj_ids:
        if obj_id not in visited:
            assert not has_cycle(obj_id), f"Cycle detected in curriculum prerequisites at {obj_id}"


def test_legacy_objective_ids_preserved() -> None:
    """Verify legacy demo objective IDs remain identical for backwards compatibility."""
    legacy_obj1_id = uuid.UUID("77777777-7777-7777-7777-777777777777")
    legacy_obj2_id = uuid.UUID("88888888-8888-8888-8888-888888888888")

    obj1 = get_objective_by_id(legacy_obj1_id)
    obj2 = get_objective_by_id(legacy_obj2_id)

    assert obj1 is not None, "Legacy obj1 ID was lost"
    assert obj2 is not None, "Legacy obj2 ID was lost"
    assert "0" in obj1["title"]["en"] or "1–5" in obj1["title"]["en"]
    assert legacy_obj1_id in obj2.get("prerequisites", [])
