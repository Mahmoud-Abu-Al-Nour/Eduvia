import pytest
from app.curriculum.schemas import AssessmentCriteria, CurriculumCreate, LearningObjectiveCreate
from pydantic import ValidationError


def test_curriculum_localization():
    # Valid localization
    curr = CurriculumCreate(title={"en": "Math", "ar": "الرياضيات"})
    assert curr.title["en"] == "Math"
    assert curr.title["ar"] == "الرياضيات"

def test_learning_objective_difficulty():
    # Valid difficulty
    obj = LearningObjectiveCreate(title={"en": "Test"}, difficulty_level=3)
    assert obj.difficulty_level == 3

    # Invalid difficulty (too high)
    with pytest.raises(ValidationError):
        LearningObjectiveCreate(title={"en": "Test"}, difficulty_level=6)

    # Invalid difficulty (too low)
    with pytest.raises(ValidationError):
        LearningObjectiveCreate(title={"en": "Test"}, difficulty_level=0)

def test_assessment_criteria():
    # Valid criteria
    obj = LearningObjectiveCreate(
        title={"en": "Test"},
        assessment_criteria={"minimum_accuracy": 0.8, "maximum_assistance_level": 2}
    )
    assert obj.assessment_criteria["minimum_accuracy"] == 0.8

    # Explicit criteria validation
    criteria = AssessmentCriteria(minimum_accuracy=0.9, maximum_assistance_level=1)
    assert criteria.minimum_accuracy == 0.9

    with pytest.raises(ValidationError):
        AssessmentCriteria(minimum_accuracy=1.5)  # Max is 1.0



