"""
Eduvia — Full Target Foundational Curriculum Catalog

Defines the complete MVP educational curriculum across 3 foundational subjects:
1. Foundational Mathematics (5 Units, 31 Objectives)
2. Early Literacy (4 Units, 20 Objectives)
3. Everyday Learning Skills (4 Units, 19 Objectives)

Total: 3 Subjects, 13 Units, 70 Objectives.
All entity IDs are deterministic via uuid.uuid5(CURRICULUM_NAMESPACE, key).
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

CURRICULUM_NAMESPACE = uuid.UUID("33333333-3333-3333-3333-333333333333")


def get_curriculum_uuid(key: str) -> uuid.UUID:
    """Generate a deterministic UUID for a curriculum entity."""
    # Preserve existing legacy IDs if present
    legacy_map = {
        "curriculum.foundational": uuid.UUID("33333333-3333-3333-3333-333333333333"),
        "subject.math": uuid.UUID("44444444-4444-4444-4444-444444444444"),
        "unit.math.numbers": uuid.UUID("55555555-5555-5555-5555-555555555555"),
        "lesson.math.recognition": uuid.UUID("66666666-6666-6666-6666-666666666666"),
        "obj.math.count_0_5": uuid.UUID("77777777-7777-7777-7777-777777777777"),
        "obj.math.count_6_10": uuid.UUID("88888888-8888-8888-8888-888888888888"),
    }
    if key in legacy_map:
        return legacy_map[key]
    return uuid.uuid5(CURRICULUM_NAMESPACE, key)


@dataclass(frozen=True)
class ObjectiveDef:
    key: str
    id: uuid.UUID
    title: dict[str, str]
    description: dict[str, str]
    difficulty_level: int
    assessment_criteria: dict[str, Any]
    prerequisite_keys: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class LessonDef:
    key: str
    id: uuid.UUID
    title: dict[str, str]
    description: dict[str, str]
    objectives: list[ObjectiveDef]


@dataclass(frozen=True)
class UnitDef:
    key: str
    id: uuid.UUID
    title: dict[str, str]
    description: dict[str, str]
    lessons: list[LessonDef]


@dataclass(frozen=True)
class SubjectDef:
    key: str
    id: uuid.UUID
    title: dict[str, str]
    description: dict[str, str]
    units: list[UnitDef]


@dataclass(frozen=True)
class CurriculumDef:
    id: uuid.UUID
    title: dict[str, str]
    description: dict[str, str]
    subjects: list[SubjectDef]


def get_target_curriculum_catalog() -> CurriculumDef:
    """Build and return the complete target foundational curriculum structure."""

    # ══════════════════════════════════════════════════════════════════════════
    # SUBJECT 1: FOUNDATIONAL MATHEMATICS
    # ══════════════════════════════════════════════════════════════════════════
    math_units: list[UnitDef] = [
        # Unit 1: Number Sense & Counting
        UnitDef(
            key="unit.math.number_sense",
            id=get_curriculum_uuid("unit.math.numbers"),
            title={"en": "Number Sense & Counting", "ar": "الحس العددي والعد"},
            description={
                "en": "Understanding discrete quantities, numerals 0 to 10, and magnitude comparison.",
                "ar": "فهم الكميات المنفصلة، والأرقام من ٠ إلى ١٠، ومقارنة المقادير.",
            },
            lessons=[
                LessonDef(
                    key="lesson.math.num_recog",
                    id=get_curriculum_uuid("lesson.math.recognition"),
                    title={"en": "Number Recognition 0–10", "ar": "التعرف على الأرقام من ٠ إلى ١٠"},
                    description={
                        "en": "Identifying digits visually and mapping numerals to quantities.",
                        "ar": "التعرف البصري على الأرقام وربطها بالكميات.",
                    },
                    objectives=[
                        ObjectiveDef(
                            key="obj.math.count_0_5",
                            id=get_curriculum_uuid("obj.math.count_0_5"),
                            title={"en": "Identify numbers 0–5", "ar": "التعرف على الأرقام من ٠ إلى ٥"},
                            description={
                                "en": "Identify written numerals 0 to 5 and match them to dot or concrete representations.",
                                "ar": "التعرف على الأرقام المكتوبة من ٠ إلى ٥ ومطابقتها مع أنماط النقاط.",
                            },
                            difficulty_level=1,
                            assessment_criteria={"minimum_accuracy": 0.80, "maximum_assistance_level": 2},
                            prerequisite_keys=[],
                        ),
                        ObjectiveDef(
                            key="obj.math.count_6_10",
                            id=get_curriculum_uuid("obj.math.count_6_10"),
                            title={"en": "Identify numbers 6–10", "ar": "التعرف على الأرقام من ٦ إلى ١٠"},
                            description={
                                "en": "Identify written numerals 6 to 10 and recognize their symbolic form.",
                                "ar": "التعرف على الأرقام المكتوبة من ٦ إلى ١٠ والتعرف على شكلها الرمزي.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.80, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.math.count_0_5"],
                        ),
                        ObjectiveDef(
                            key="obj.math.count_objects_0_5",
                            id=get_curriculum_uuid("obj.math.count_objects_0_5"),
                            title={"en": "Count objects from 0–5", "ar": "عد الأشياء من ٠ إلى ٥"},
                            description={
                                "en": "Count discrete visual elements up to 5 with one-to-one correspondence.",
                                "ar": "عد العناصر البصرية حتى ٥ مع المطابقة الفردية.",
                            },
                            difficulty_level=1,
                            assessment_criteria={"minimum_accuracy": 0.80, "maximum_assistance_level": 2},
                            prerequisite_keys=["obj.math.count_0_5"],
                        ),
                        ObjectiveDef(
                            key="obj.math.count_objects_6_10",
                            id=get_curriculum_uuid("obj.math.count_objects_6_10"),
                            title={"en": "Count objects from 6–10", "ar": "عد الأشياء من ٦ إلى ١٠"},
                            description={
                                "en": "Count discrete visual elements between 6 and 10 with accuracy.",
                                "ar": "عد العناصر البصرية من ٦ إلى ١٠ بدقة.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.80, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.math.count_objects_0_5", "obj.math.count_6_10"],
                        ),
                        ObjectiveDef(
                            key="obj.math.numeral_qty_match",
                            id=get_curriculum_uuid("obj.math.numeral_qty_match"),
                            title={"en": "Match a numeral to a quantity", "ar": "مطابقة الرقم بالكمية"},
                            description={
                                "en": "Connect an abstract numeral to its exact count of visual objects.",
                                "ar": "ربط الرقم المجرد بعدده الفعلي من العناصر البصرية.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.math.count_objects_0_5"],
                        ),
                        ObjectiveDef(
                            key="obj.math.compare_quantities",
                            id=get_curriculum_uuid("obj.math.compare_quantities"),
                            title={"en": "Compare two quantities: more / less / equal", "ar": "مقارنة كميتين: أكثر / أقل / متساوي"},
                            description={
                                "en": "Compare two groups of items and identify which has more, less, or equal count.",
                                "ar": "مقارنة مجموعتين وتحديد أيهما أكثر أو أقل أو متساويتان.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.80, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.math.numeral_qty_match"],
                        ),
                    ],
                )
            ],
        ),
        # Unit 2: Number Sequence
        UnitDef(
            key="unit.math.number_sequence",
            id=get_curriculum_uuid("unit.math.number_sequence"),
            title={"en": "Number Sequence", "ar": "تسلسل الأرقام"},
            description={
                "en": "Understanding numerical order, preceding/succeeding numbers, and sequence patterns.",
                "ar": "فهم الترتيب العددي، والأرقام السابقة واللاحقة، والأنماط العددية.",
            },
            lessons=[
                LessonDef(
                    key="lesson.math.order_patterns",
                    id=get_curriculum_uuid("lesson.math.order_patterns"),
                    title={"en": "Ordering & Sequences", "ar": "الترتيب والتسلسل"},
                    description={
                        "en": "Arranging numbers and completing missing steps along a number line.",
                        "ar": "ترتيب الأرقام وإكمال الخطوات المفقودة على خط الأعداد.",
                    },
                    objectives=[
                        ObjectiveDef(
                            key="obj.math.number_before",
                            id=get_curriculum_uuid("obj.math.number_before"),
                            title={"en": "Identify the number that comes before", "ar": "تحديد الرقم السابق"},
                            description={
                                "en": "State or select the immediate predecessor of a given number within 10.",
                                "ar": "تحديد الرقم السابق مباشرة لرقم معين ضمن ١٠.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.80, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.math.count_6_10"],
                        ),
                        ObjectiveDef(
                            key="obj.math.number_after",
                            id=get_curriculum_uuid("obj.math.number_after"),
                            title={"en": "Identify the number that comes after", "ar": "تحديد الرقم التالي"},
                            description={
                                "en": "State or select the immediate successor of a given number within 10.",
                                "ar": "تحديد الرقم التالي مباشرة لرقم معين ضمن ١٠.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.80, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.math.number_before"],
                        ),
                        ObjectiveDef(
                            key="obj.math.order_smallest_largest",
                            id=get_curriculum_uuid("obj.math.order_smallest_largest"),
                            title={"en": "Order numbers from smallest to largest", "ar": "ترتيب الأرقام من الأصغر إلى الأكبر"},
                            description={
                                "en": "Arrange a set of numbers in ascending numerical sequence.",
                                "ar": "ترتيب مجموعة من الأرقام تصاعدياً.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.math.number_after"],
                        ),
                        ObjectiveDef(
                            key="obj.math.order_largest_smallest",
                            id=get_curriculum_uuid("obj.math.order_largest_smallest"),
                            title={"en": "Order numbers from largest to smallest", "ar": "ترتيب الأرقام من الأكبر إلى الأصغر"},
                            description={
                                "en": "Arrange a set of numbers in descending numerical sequence.",
                                "ar": "ترتيب مجموعة من الأرقام تنازلياً.",
                            },
                            difficulty_level=3,
                            assessment_criteria={"minimum_accuracy": 0.80, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.math.order_smallest_largest"],
                        ),
                        ObjectiveDef(
                            key="obj.math.complete_missing_sequence",
                            id=get_curriculum_uuid("obj.math.complete_missing_sequence"),
                            title={"en": "Complete a missing number sequence", "ar": "إكمال تسلسل الأرقام الناقص"},
                            description={
                                "en": "Fill in the missing blank numeral within a sequence from 1 to 10.",
                                "ar": "ملء الفراغ بالرقم المفقود في تسلسل من ١ إلى ١٠.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.math.order_smallest_largest"],
                        ),
                        ObjectiveDef(
                            key="obj.math.recognize_numerical_patterns",
                            id=get_curriculum_uuid("obj.math.recognize_numerical_patterns"),
                            title={"en": "Recognize simple numerical patterns", "ar": "التعرف على الأنماط العددية البسيطة"},
                            description={
                                "en": "Identify recurring alternating or skip sequences (e.g. 2, 4, 6 or 1, 2, 1, 2).",
                                "ar": "التعرف على الأنماط المتكررة البسيطة.",
                            },
                            difficulty_level=3,
                            assessment_criteria={"minimum_accuracy": 0.80, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.math.complete_missing_sequence"],
                        ),
                    ],
                )
            ],
        ),
        # Unit 3: Addition Within 10
        UnitDef(
            key="unit.math.addition_within_10",
            id=get_curriculum_uuid("unit.math.addition_within_10"),
            title={"en": "Addition Within 10", "ar": "الجمع حتى ١٠"},
            description={
                "en": "Combining sets, representing sums with visual models, and solving equations within 10.",
                "ar": "ضم المجموعات، وتمثيل الجمع بالنماذج البصرية، وحل المعادلات حتى ١٠.",
            },
            lessons=[
                LessonDef(
                    key="lesson.math.addition_concepts",
                    id=get_curriculum_uuid("lesson.math.addition_concepts"),
                    title={"en": "Basic Addition", "ar": "مفاهيم الجمع الأساسية"},
                    description={
                        "en": "Concrete manipulation and visual equations for addition.",
                        "ar": "التعامل الملموس والمعادلات البصرية لعملية الجمع.",
                    },
                    objectives=[
                        ObjectiveDef(
                            key="obj.math.combine_two_groups",
                            id=get_curriculum_uuid("obj.math.combine_two_groups"),
                            title={"en": "Combine two groups of objects", "ar": "ضم مجموعتين من الأشياء"},
                            description={
                                "en": "Physically or visually join two distinct groups and determine total count.",
                                "ar": "ضم مجموعتين منفصلتين وتحديد المجموع الكلي.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.80, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.math.numeral_qty_match"],
                        ),
                        ObjectiveDef(
                            key="obj.math.represent_addition_objects",
                            id=get_curriculum_uuid("obj.math.represent_addition_objects"),
                            title={"en": "Represent addition using objects", "ar": "تمثيل الجمع باستخدام الأشياء"},
                            description={
                                "en": "Model a simple addition expression (e.g. 2 + 3) using movable counters.",
                                "ar": "تمثيل مسألة جمع بسيطة باستخدام عناصر متحركة.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.80, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.math.combine_two_groups"],
                        ),
                        ObjectiveDef(
                            key="obj.math.represent_addition_visual_groups",
                            id=get_curriculum_uuid("obj.math.represent_addition_visual_groups"),
                            title={"en": "Represent addition using visual groups", "ar": "تمثيل الجمع بالمجموعات البصرية"},
                            description={
                                "en": "Read side-by-side grouped images to find the total sum.",
                                "ar": "قراءة المجموعات البصرية المتجاورة لإيجاد الناتج الكلي.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.math.represent_addition_objects"],
                        ),
                        ObjectiveDef(
                            key="obj.math.solve_addition_equations_10",
                            id=get_curriculum_uuid("obj.math.solve_addition_equations_10"),
                            title={"en": "Solve simple addition equations within 10", "ar": "حل معادلات جمع بسيطة حتى ١٠"},
                            description={
                                "en": "Calculate the correct sum for numerical equations up to 10.",
                                "ar": "حساب الناتج الصحيح لمعادلات الجمع حتى ١٠.",
                            },
                            difficulty_level=3,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.math.represent_addition_visual_groups"],
                        ),
                        ObjectiveDef(
                            key="obj.math.add_plus_1",
                            id=get_curriculum_uuid("obj.math.add_plus_1"),
                            title={"en": "Identify the result of adding 1", "ar": "تحديد ناتج إضافة ١"},
                            description={
                                "en": "Quickly apply the +1 rule to any number from 0 to 9.",
                                "ar": "تطبيق قاعدة إضافة ١ بسرعة على أي رقم من ٠ إلى ٩.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.90, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.math.solve_addition_equations_10"],
                        ),
                        ObjectiveDef(
                            key="obj.math.add_plus_2_or_more",
                            id=get_curriculum_uuid("obj.math.add_plus_2_or_more"),
                            title={"en": "Identify the result of adding 2 or more", "ar": "تحديد ناتج إضافة ٢ أو أكثر"},
                            description={
                                "en": "Accurately compute sums with addends of 2, 3, or more within 10.",
                                "ar": "حساب نواتج الجمع بإضافة ٢ أو ٣ أو أكثر ضمن ١٠ بدقة.",
                            },
                            difficulty_level=3,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.math.add_plus_1"],
                        ),
                    ],
                )
            ],
        ),
        # Unit 4: Subtraction Within 10
        UnitDef(
            key="unit.math.subtraction_within_10",
            id=get_curriculum_uuid("unit.math.subtraction_within_10"),
            title={"en": "Subtraction Within 10", "ar": "الطرح حتى ١٠"},
            description={
                "en": "Separating groups, taking away objects, and solving subtraction equations within 10.",
                "ar": "فصل المجموعات، وأخذ الأشياء، وحل معادلات الطرح حتى ١٠.",
            },
            lessons=[
                LessonDef(
                    key="lesson.math.subtraction_concepts",
                    id=get_curriculum_uuid("lesson.math.subtraction_concepts"),
                    title={"en": "Basic Subtraction", "ar": "مفاهيم الطرح الأساسية"},
                    description={
                        "en": "Concrete removal of objects and visual subtraction equations.",
                        "ar": "الإزالة الملموسة للأشياء ومعادلات الطرح البصرية.",
                    },
                    objectives=[
                        ObjectiveDef(
                            key="obj.math.remove_objects_group",
                            id=get_curriculum_uuid("obj.math.remove_objects_group"),
                            title={"en": "Remove objects from a group", "ar": "إزالة عناصر من مجموعة"},
                            description={
                                "en": "Take away a specified number of items from a concrete collection.",
                                "ar": "أخذ عدد محدد من العناصر من مجموعة ملموسة.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.80, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.math.combine_two_groups"],
                        ),
                        ObjectiveDef(
                            key="obj.math.represent_subtraction_visually",
                            id=get_curriculum_uuid("obj.math.represent_subtraction_visually"),
                            title={"en": "Represent subtraction visually", "ar": "تمثيل الطرح بصرياً"},
                            description={
                                "en": "Interpret crossed-out items or separated sets as subtraction.",
                                "ar": "تفسير العناصر المشطوبة أو المجموعات المنفصلة كعملية طرح.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.80, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.math.remove_objects_group"],
                        ),
                        ObjectiveDef(
                            key="obj.math.identify_remaining_objects",
                            id=get_curriculum_uuid("obj.math.identify_remaining_objects"),
                            title={"en": "Identify how many objects remain", "ar": "تحديد عدد الأشياء المتبقية"},
                            description={
                                "en": "Count the remaining items after taking away a subset.",
                                "ar": "عد العناصر المتبقية بعد إزالة جزء منها.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.math.represent_subtraction_visually"],
                        ),
                        ObjectiveDef(
                            key="obj.math.solve_subtraction_equations_10",
                            id=get_curriculum_uuid("obj.math.solve_subtraction_equations_10"),
                            title={"en": "Solve simple subtraction equations within 10", "ar": "حل معادلات طرح بسيطة حتى ١٠"},
                            description={
                                "en": "Calculate the difference in numerical subtraction problems within 10.",
                                "ar": "حساب الفرق في مسائل الطرح العددية حتى ١٠.",
                            },
                            difficulty_level=3,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.math.identify_remaining_objects"],
                        ),
                        ObjectiveDef(
                            key="obj.math.sub_minus_1",
                            id=get_curriculum_uuid("obj.math.sub_minus_1"),
                            title={"en": "Identify the result of subtracting 1", "ar": "تحديد ناتج طرح ١"},
                            description={
                                "en": "Quickly recognize that subtracting 1 yields the preceding number.",
                                "ar": "إدراك أن طرح ١ يعطي الرقم السابق مباشرة.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.90, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.math.solve_subtraction_equations_10"],
                        ),
                        ObjectiveDef(
                            key="obj.math.sub_minus_2_or_more",
                            id=get_curriculum_uuid("obj.math.sub_minus_2_or_more"),
                            title={"en": "Identify the result of subtracting 2 or more", "ar": "تحديد ناتج طرح ٢ أو أكثر"},
                            description={
                                "en": "Accurately compute differences when subtracting 2, 3, or more within 10.",
                                "ar": "حساب الفروق بدقة عند طرح ٢ أو ٣ أو أكثر ضمن ١٠.",
                            },
                            difficulty_level=3,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.math.sub_minus_1"],
                        ),
                    ],
                )
            ],
        ),
        # Unit 5: Basic Shapes & Classification
        UnitDef(
            key="unit.math.shapes_classification",
            id=get_curriculum_uuid("unit.math.shapes_classification"),
            title={"en": "Basic Shapes & Classification", "ar": "الأشكال الأساسية والتصنيف"},
            description={
                "en": "Identifying geometric shapes, sorting by attributes, and comparing visual properties.",
                "ar": "التعرف على الأشكال الهندسية، والتصنيف حسب الخصائص، ومقارنة السمات البصرية.",
            },
            lessons=[
                LessonDef(
                    key="lesson.math.shapes_sorting",
                    id=get_curriculum_uuid("lesson.math.shapes_sorting"),
                    title={"en": "Geometric Shapes & Sorting", "ar": "الأشكال الهندسية والفرز"},
                    description={
                        "en": "Recognizing circles, squares, triangles, rectangles, and classifying them.",
                        "ar": "التعرف على الدوائر والمربعات والمثلثات والمستطيلات وفرزها.",
                    },
                    objectives=[
                        ObjectiveDef(
                            key="obj.math.identify_circle",
                            id=get_curriculum_uuid("obj.math.identify_circle"),
                            title={"en": "Identify a circle", "ar": "التعرف على الدائرة"},
                            description={
                                "en": "Distinguish circles from non-round shapes in visual scenes.",
                                "ar": "تمييز الدائرة عن الأشكال الأخرى في المشاهد البصرية.",
                            },
                            difficulty_level=1,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 2},
                            prerequisite_keys=[],
                        ),
                        ObjectiveDef(
                            key="obj.math.identify_square",
                            id=get_curriculum_uuid("obj.math.identify_square"),
                            title={"en": "Identify a square", "ar": "التعرف على المربع"},
                            description={
                                "en": "Identify squares by recognizing their four equal straight sides.",
                                "ar": "التعرف على المربع بأضلاعه الأربعة المتساوية.",
                            },
                            difficulty_level=1,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 2},
                            prerequisite_keys=[],
                        ),
                        ObjectiveDef(
                            key="obj.math.identify_triangle",
                            id=get_curriculum_uuid("obj.math.identify_triangle"),
                            title={"en": "Identify a triangle", "ar": "التعرف على المثلث"},
                            description={
                                "en": "Recognize three-sided geometric shapes in various orientations.",
                                "ar": "التعرف على الشكل ثلاثي الأضلاع في اتجاهات مختلفة.",
                            },
                            difficulty_level=1,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 2},
                            prerequisite_keys=[],
                        ),
                        ObjectiveDef(
                            key="obj.math.identify_rectangle",
                            id=get_curriculum_uuid("obj.math.identify_rectangle"),
                            title={"en": "Identify a rectangle", "ar": "التعرف على المستطيل"},
                            description={
                                "en": "Identify rectangles by recognizing their four right-angled sides with opposite pairs equal.",
                                "ar": "التعرف على المستطيل بأضلاعه الأربعة وزواياه القائمة.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.80, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.math.identify_square"],
                        ),
                        ObjectiveDef(
                            key="obj.math.match_identical_shapes",
                            id=get_curriculum_uuid("obj.math.match_identical_shapes"),
                            title={"en": "Match identical shapes", "ar": "مطابقة الأشكال المتطابقة"},
                            description={
                                "en": "Connect pairs of matching geometric figures regardless of color or size.",
                                "ar": "توصيل أزواج الأشكال الهندسية المتطابقة بغض النظر عن اللون أو الحجم.",
                            },
                            difficulty_level=1,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 2},
                            prerequisite_keys=["obj.math.identify_circle", "obj.math.identify_square", "obj.math.identify_triangle"],
                        ),
                        ObjectiveDef(
                            key="obj.math.sort_objects_by_shape",
                            id=get_curriculum_uuid("obj.math.sort_objects_by_shape"),
                            title={"en": "Sort objects by shape", "ar": "فرز الأشياء حسب الشكل"},
                            description={
                                "en": "Sort diverse everyday objects into categories according to their fundamental geometry.",
                                "ar": "فرز أشياء متنوعة في مجموعات بناءً على شكلها الهندسي.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.math.match_identical_shapes"],
                        ),
                        ObjectiveDef(
                            key="obj.math.identify_visual_attributes",
                            id=get_curriculum_uuid("obj.math.identify_visual_attributes"),
                            title={"en": "Identify simple visual attributes such as size or shape", "ar": "تحديد الخصائص البصرية البسيطة كالحجم والشكل"},
                            description={
                                "en": "Describe or group objects according to comparative size (big/small) or shape.",
                                "ar": "وصف أو تصنيف العناصر وفق الحجم (كبير/صغير) أو الشكل.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.math.sort_objects_by_shape"],
                        ),
                    ],
                )
            ],
        ),
    ]

    # ══════════════════════════════════════════════════════════════════════════
    # SUBJECT 2: EARLY LITERACY
    # ══════════════════════════════════════════════════════════════════════════
    literacy_units: list[UnitDef] = [
        # Unit 1: Letter Recognition
        UnitDef(
            key="unit.lit.letter_recognition",
            id=get_curriculum_uuid("unit.lit.letter_recognition"),
            title={"en": "Letter Recognition", "ar": "التعرف على الحروف"},
            description={
                "en": "Visual identification of uppercase and lowercase letters and letter discrimination.",
                "ar": "التعرف البصري على الحروف الكبيرة والصغيرة والتمييز بينها.",
            },
            lessons=[
                LessonDef(
                    key="lesson.lit.alphabet_basics",
                    id=get_curriculum_uuid("lesson.lit.alphabet_basics"),
                    title={"en": "Alphabet Characters", "ar": "حروف الهجاء"},
                    description={
                        "en": "Recognizing letter shapes, cases, and distinguishing letters among visual distractors.",
                        "ar": "التعرف على أشكال الحروف وحالاتها والتمييز بينها.",
                    },
                    objectives=[
                        ObjectiveDef(
                            key="obj.lit.identify_uppercase",
                            id=get_curriculum_uuid("obj.lit.identify_uppercase"),
                            title={"en": "Identify uppercase letters", "ar": "التعرف على الحروف الكبيرة"},
                            description={
                                "en": "Name and point to target uppercase letters (e.g. A, B, C, D).",
                                "ar": "تسمية وتحديد الحروف الكبيرة المستهدفة.",
                            },
                            difficulty_level=1,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 2},
                            prerequisite_keys=[],
                        ),
                        ObjectiveDef(
                            key="obj.lit.identify_lowercase",
                            id=get_curriculum_uuid("obj.lit.identify_lowercase"),
                            title={"en": "Identify lowercase letters", "ar": "التعرف على الحروف الصغيرة"},
                            description={
                                "en": "Name and point to target lowercase letters (e.g. a, b, c, d).",
                                "ar": "تسمية وتحديد الحروف الصغيرة المستهدفة.",
                            },
                            difficulty_level=1,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 2},
                            prerequisite_keys=[],
                        ),
                        ObjectiveDef(
                            key="obj.lit.match_upper_to_lower",
                            id=get_curriculum_uuid("obj.lit.match_upper_to_lower"),
                            title={"en": "Match uppercase to lowercase", "ar": "مطابقة الحروف الكبيرة بالصغيرة"},
                            description={
                                "en": "Connect uppercase letter forms to their corresponding lowercase forms (e.g. A ↔ a).",
                                "ar": "ربط الحرف الكبير بشكله الصغير المقابل.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.lit.identify_uppercase", "obj.lit.identify_lowercase"],
                        ),
                        ObjectiveDef(
                            key="obj.lit.identify_letter_distractors",
                            id=get_curriculum_uuid("obj.lit.identify_letter_distractors"),
                            title={"en": "Identify a target letter among distractors", "ar": "تحديد حرف مستهدف بين مشتتات"},
                            description={
                                "en": "Find and select a specified letter from a visual field of dissimilar letters.",
                                "ar": "إيجاد وتحديد حرف محدد ضمن مجموعة من الحروف الأخرى.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.80, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.lit.identify_uppercase"],
                        ),
                        ObjectiveDef(
                            key="obj.lit.recognize_repeated_letters",
                            id=get_curriculum_uuid("obj.lit.recognize_repeated_letters"),
                            title={"en": "Recognize repeated letters", "ar": "التعرف على الحروف المتكررة"},
                            description={
                                "en": "Identify letter occurrences that appear more than once in a short row or word.",
                                "ar": "تحديد الحروف التي تظهر أكثر من مرة في سطر أو كلمة.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.lit.identify_letter_distractors"],
                        ),
                        ObjectiveDef(
                            key="obj.lit.group_identical_letters",
                            id=get_curriculum_uuid("obj.lit.group_identical_letters"),
                            title={"en": "Group identical letters", "ar": "تجميع الحروف المتطابقة"},
                            description={
                                "en": "Sort a mixed collection of letters into groups of identical graphemes.",
                                "ar": "فرز مجموعة مختلطة من الحروف إلى مجموعات متطابقة.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.lit.recognize_repeated_letters"],
                        ),
                    ],
                )
            ],
        ),
        # Unit 2: Letter Sounds
        UnitDef(
            key="unit.lit.letter_sounds",
            id=get_curriculum_uuid("unit.lit.letter_sounds"),
            title={"en": "Letter Sounds", "ar": "أصوات الحروف"},
            description={
                "en": "Phonological awareness, initial letter sounds, and associating phonemes with familiar words.",
                "ar": "الوعي الصوتي، وأصوات الحروف الأولى، وربط الأصوات بالكلمات المألوفة.",
            },
            lessons=[
                LessonDef(
                    key="lesson.lit.phonics_foundations",
                    id=get_curriculum_uuid("lesson.lit.phonics_foundations"),
                    title={"en": "Initial Phonics", "ar": "الأصوات الأولية"},
                    description={
                        "en": "Connecting speech sounds to written characters and identifying starting sounds.",
                        "ar": "ربط الأصوات المنطوقة بالحروف المكتوبة وتحديد الصوت الأولي.",
                    },
                    objectives=[
                        ObjectiveDef(
                            key="obj.lit.initial_sound_word",
                            id=get_curriculum_uuid("obj.lit.initial_sound_word"),
                            title={"en": "Identify the initial sound of a simple word", "ar": "تحديد الصوت الأولي لكلمة بسيطة"},
                            description={
                                "en": "Isolate the first phoneme heard in common single-syllable or familiar words (e.g. /b/ in ball).",
                                "ar": "تمييز الصوت الأول في الكلمات الشائعة البسيطة.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.80, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.lit.match_upper_to_lower"],
                        ),
                        ObjectiveDef(
                            key="obj.lit.match_letter_initial_sound",
                            id=get_curriculum_uuid("obj.lit.match_letter_initial_sound"),
                            title={"en": "Match a letter with its common initial sound", "ar": "مطابقة الحرف بصوته الأولي الشائع"},
                            description={
                                "en": "Pair a written letter with the primary phoneme it represents.",
                                "ar": "مطابقة الحرف المكتوب بالصوت الأساسي الذي يمثله.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.lit.initial_sound_word"],
                        ),
                        ObjectiveDef(
                            key="obj.lit.word_starts_target_sound",
                            id=get_curriculum_uuid("obj.lit.word_starts_target_sound"),
                            title={"en": "Identify which word starts with a target sound", "ar": "تحديد الكلمة التي تبدأ بصوت مستهدف"},
                            description={
                                "en": "Given a target sound (e.g. /s/), select the picture/word that begins with it (e.g. sun).",
                                "ar": "اختيار الكلمة أو الصورة التي تبدأ بالصوت المطلوب.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.lit.match_letter_initial_sound"],
                        ),
                        ObjectiveDef(
                            key="obj.lit.distinguish_two_initial_sounds",
                            id=get_curriculum_uuid("obj.lit.distinguish_two_initial_sounds"),
                            title={"en": "Distinguish between two simple initial sounds", "ar": "التمييز بين صوتين أوليين بسيطين"},
                            description={
                                "en": "Contrast words starting with distinct phonemes (e.g. /m/ vs /t/).",
                                "ar": "المقارنة بين كلمات تبدأ بأصوات أولية مختلفة والتمييز بينها.",
                            },
                            difficulty_level=3,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.lit.word_starts_target_sound"],
                        ),
                    ],
                )
            ],
        ),
        # Unit 3: Word Recognition
        UnitDef(
            key="unit.lit.word_recognition",
            id=get_curriculum_uuid("unit.lit.word_recognition"),
            title={"en": "Word Recognition", "ar": "التعرف على الكلمات"},
            description={
                "en": "Recognizing whole sight words, matching words to illustrations, and identifying familiar vocabulary.",
                "ar": "التعرف على الكلمات البصرية، ومطابقة الكلمات بالرسوم، وتحديد المفردات المألوفة.",
            },
            lessons=[
                LessonDef(
                    key="lesson.lit.sight_words",
                    id=get_curriculum_uuid("lesson.lit.sight_words"),
                    title={"en": "Familiar Words", "ar": "الكلمات المألوفة"},
                    description={
                        "en": "Visual word matching, picture association, and word spotting.",
                        "ar": "المطابقة البصرية للكلمات، وربطها بالصور، وتحديدها.",
                    },
                    objectives=[
                        ObjectiveDef(
                            key="obj.lit.recognize_simple_words",
                            id=get_curriculum_uuid("obj.lit.recognize_simple_words"),
                            title={"en": "Recognize simple familiar words", "ar": "التعرف على كلمات بسيطة مألوفة"},
                            description={
                                "en": "Visually identify high-frequency functional words (e.g. cat, dog, sun, book).",
                                "ar": "التعرف البصري على الكلمات الشائعة والمفيدة.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.80, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.lit.word_starts_target_sound"],
                        ),
                        ObjectiveDef(
                            key="obj.lit.match_identical_words",
                            id=get_curriculum_uuid("obj.lit.match_identical_words"),
                            title={"en": "Match identical words", "ar": "مطابقة الكلمات المتطابقة"},
                            description={
                                "en": "Pair printed words that have the exact same spelling.",
                                "ar": "مطابقة الكلمات المطبوعة المتماثلة في التهجئة.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.lit.recognize_simple_words"],
                        ),
                        ObjectiveDef(
                            key="obj.lit.match_word_to_image",
                            id=get_curriculum_uuid("obj.lit.match_word_to_image"),
                            title={"en": "Match a word to a familiar image", "ar": "مطابقة الكلمة بالصورة المألوفة"},
                            description={
                                "en": "Connect a printed noun to its clear pictorial representation.",
                                "ar": "ربط الكلمة المكتوبة بالصورة التوضيحية المقابلة لها.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.lit.match_identical_words"],
                        ),
                        ObjectiveDef(
                            key="obj.lit.target_word_among_distractors",
                            id=get_curriculum_uuid("obj.lit.target_word_among_distractors"),
                            title={"en": "Identify a target word among distractors", "ar": "تحديد كلمة مستهدفة بين مشتتات"},
                            description={
                                "en": "Pick out a requested word from a display of other words.",
                                "ar": "اختيار الكلمة المطلوبة من بين كلمات أخرى معروضة.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.lit.match_word_to_image"],
                        ),
                        ObjectiveDef(
                            key="obj.lit.recognize_repeated_words",
                            id=get_curriculum_uuid("obj.lit.recognize_repeated_words"),
                            title={"en": "Recognize repeated familiar words", "ar": "التعرف على الكلمات المألوفة المتكررة"},
                            description={
                                "en": "Spot instances where the same word appears multiple times in a short line of text.",
                                "ar": "تحديد تكرار الكلمة نفسها في نص قصير.",
                            },
                            difficulty_level=3,
                            assessment_criteria={"minimum_accuracy": 0.80, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.lit.target_word_among_distractors"],
                        ),
                    ],
                )
            ],
        ),
        # Unit 4: Simple Sequencing & Comprehension
        UnitDef(
            key="unit.lit.sequencing_comprehension",
            id=get_curriculum_uuid("unit.lit.sequencing_comprehension"),
            title={"en": "Simple Sequencing & Comprehension", "ar": "التسلسل البسيط والفهم"},
            description={
                "en": "Narrative chronology, determining what happens first and next, and sentence-image alignment.",
                "ar": "التسلسل الزمني للقصة، وتحديد ما يحدث أولاً ثم لاحقاً، ومطابقة الجملة بالصورة.",
            },
            lessons=[
                LessonDef(
                    key="lesson.lit.story_order",
                    id=get_curriculum_uuid("lesson.lit.story_order"),
                    title={"en": "Event Sequences", "ar": "تسلسل الأحداث"},
                    description={
                        "en": "Chronological order of familiar actions and reading short narrative captions.",
                        "ar": "الترتيب الزمني للأفعال المألوفة وقراءة العبارات القصيرة.",
                    },
                    objectives=[
                        ObjectiveDef(
                            key="obj.lit.order_two_events",
                            id=get_curriculum_uuid("obj.lit.order_two_events"),
                            title={"en": "Put two events in the correct order", "ar": "ترتيب حدثين في التتابع الصحيح"},
                            description={
                                "en": "Order a 2-step sequence representing cause-and-effect or everyday action (e.g. peel banana → eat banana).",
                                "ar": "ترتيب تسلسل من خطوتين يمثل السبب والنتيجة أو حدثاً يومياً.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.lit.match_word_to_image"],
                        ),
                        ObjectiveDef(
                            key="obj.lit.order_three_events",
                            id=get_curriculum_uuid("obj.lit.order_three_events"),
                            title={"en": "Put three simple events in order", "ar": "ترتيب ثلاثة أحداث بسيطة"},
                            description={
                                "en": "Sequence beginning, middle, and end cards of a familiar brief story.",
                                "ar": "ترتيب بطاقات البداية والوسط والنهاية لقصة قصيرة مألوفة.",
                            },
                            difficulty_level=3,
                            assessment_criteria={"minimum_accuracy": 0.80, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.lit.order_two_events"],
                        ),
                        ObjectiveDef(
                            key="obj.lit.identify_first_event",
                            id=get_curriculum_uuid("obj.lit.identify_first_event"),
                            title={"en": "Identify what happens first", "ar": "تحديد ما يحدث أولاً"},
                            description={
                                "en": "Pinpoint the starting event in a multi-step illustration.",
                                "ar": "تحديد الحدث الأول في رسم توضيحي متعدد الخطوات.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.lit.order_three_events"],
                        ),
                        ObjectiveDef(
                            key="obj.lit.identify_next_event",
                            id=get_curriculum_uuid("obj.lit.identify_next_event"),
                            title={"en": "Identify what happens next", "ar": "تحديد ما يحدث بعد ذلك"},
                            description={
                                "en": "Predict or choose the logical continuation after an initial action.",
                                "ar": "توقع أو اختيار الحدث التالي المنطقي بعد فعل أولي.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.lit.identify_first_event"],
                        ),
                        ObjectiveDef(
                            key="obj.lit.match_sentence_to_image",
                            id=get_curriculum_uuid("obj.lit.match_sentence_to_image"),
                            title={"en": "Match a simple sentence to an appropriate image", "ar": "مطابقة جملة بسيطة بالصورة المناسبة"},
                            description={
                                "en": "Read a 3-to-4 word sentence (e.g. 'The sun is hot') and pair it with the corresponding picture.",
                                "ar": "قراءة جملة قصيرة من ٣-٤ كلمات وربطها بالصورة المعبرة عنها.",
                            },
                            difficulty_level=3,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.lit.identify_next_event"],
                        ),
                    ],
                )
            ],
        ),
    ]

    # ══════════════════════════════════════════════════════════════════════════
    # SUBJECT 3: EVERYDAY LEARNING SKILLS
    # ══════════════════════════════════════════════════════════════════════════
    everyday_units: list[UnitDef] = [
        # Unit 1: Daily Routines
        UnitDef(
            key="unit.life.daily_routines",
            id=get_curriculum_uuid("unit.life.daily_routines"),
            title={"en": "Daily Routines", "ar": "الروتين اليومي"},
            description={
                "en": "Recognizing daily activities, morning routines, sequence of self-care steps, and time-of-day association.",
                "ar": "التعرف على الأنشطة اليومية، وروتين الصباح، وتسلسل خطوات العناية الذاتية.",
            },
            lessons=[
                LessonDef(
                    key="lesson.life.routines_care",
                    id=get_curriculum_uuid("lesson.life.routines_care"),
                    title={"en": "Everyday Schedule", "ar": "الجدول اليومي"},
                    description={
                        "en": "Understanding predictable schedules and steps in daily routines.",
                        "ar": "فهم الجداول الزمنية والخطوات المنتظمة في الروتين اليومي.",
                    },
                    objectives=[
                        ObjectiveDef(
                            key="obj.life.identify_daily_activities",
                            id=get_curriculum_uuid("obj.life.identify_daily_activities"),
                            title={"en": "Identify common daily activities", "ar": "التعرف على الأنشطة اليومية الشائعة"},
                            description={
                                "en": "Name and recognize essential activities such as waking up, eating breakfast, washing hands, and sleeping.",
                                "ar": "تسمية وتحديد الأنشطة الأساسية مثل الاستيقاظ، وتناول الإفطار، وغسل اليدين، والنوم.",
                            },
                            difficulty_level=1,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 2},
                            prerequisite_keys=[],
                        ),
                        ObjectiveDef(
                            key="obj.life.order_morning_routines",
                            id=get_curriculum_uuid("obj.life.order_morning_routines"),
                            title={"en": "Order simple morning routines", "ar": "ترتيب الروتين الصباحي البسيط"},
                            description={
                                "en": "Arrange morning steps in chronological sequence (e.g. wake up → brush teeth → get dressed).",
                                "ar": "ترتيب خطوات الصباح بتسلسل زمني سليم.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.life.identify_daily_activities"],
                        ),
                        ObjectiveDef(
                            key="obj.life.identify_next_in_routine",
                            id=get_curriculum_uuid("obj.life.identify_next_in_routine"),
                            title={"en": "Identify what comes next in a routine", "ar": "تحديد الخطوة التالية في الروتين"},
                            description={
                                "en": "Given a current step in a known routine, choose the immediate subsequent action.",
                                "ar": "تحديد الخطوة اللاحقة مباشرة لخطوة حالية في روتين معروف.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.life.order_morning_routines"],
                        ),
                        ObjectiveDef(
                            key="obj.life.match_activity_to_stage",
                            id=get_curriculum_uuid("obj.life.match_activity_to_stage"),
                            title={"en": "Match an activity to the correct routine stage", "ar": "مطابقة النشاط بمرحلة الروتين المناسبة"},
                            description={
                                "en": "Categorize activities into appropriate times of day: morning, afternoon, or bedtime.",
                                "ar": "تصنيف الأنشطة في أوقاتها المناسبة: الصباح، بعد الظهر، أو وقت النوم.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.80, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.life.identify_next_in_routine"],
                        ),
                    ],
                )
            ],
        ),
        # Unit 2: Object Recognition
        UnitDef(
            key="unit.life.object_recognition",
            id=get_curriculum_uuid("unit.life.object_recognition"),
            title={"en": "Object Recognition", "ar": "التعرف على الأشياء"},
            description={
                "en": "Identifying classroom and household tools, matching objects to names, and identifying objects by functional descriptions.",
                "ar": "التعرف على أدوات الصف والمنزل، ومطابقة الأشياء بأسمائها ووصفها الوظيفي.",
            },
            lessons=[
                LessonDef(
                    key="lesson.life.environment_objects",
                    id=get_curriculum_uuid("lesson.life.environment_objects"),
                    title={"en": "Familiar Tools & Items", "ar": "الأدوات والعناصر المألوفة"},
                    description={
                        "en": "Classroom items, household items, and descriptive matching.",
                        "ar": "أدوات الفصل المدرسي، والأدوات المنزلية، والمطابقة الوصفية.",
                    },
                    objectives=[
                        ObjectiveDef(
                            key="obj.life.identify_classroom_objects",
                            id=get_curriculum_uuid("obj.life.identify_classroom_objects"),
                            title={"en": "Identify familiar classroom objects", "ar": "التعرف على أدوات الفصل المألوفة"},
                            description={
                                "en": "Name and locate pencil, paper, backpack, book, and desk.",
                                "ar": "تسمية وتحديد القلم والورقة والحقيبة والكتاب والمكتب.",
                            },
                            difficulty_level=1,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 2},
                            prerequisite_keys=[],
                        ),
                        ObjectiveDef(
                            key="obj.life.identify_household_objects",
                            id=get_curriculum_uuid("obj.life.identify_household_objects"),
                            title={"en": "Identify familiar household objects", "ar": "التعرف على الأدوات المنزلية المألوفة"},
                            description={
                                "en": "Name and locate cup, plate, spoon, bed, and chair.",
                                "ar": "تسمية وتحديد الكوب والطبق والملعقة والسرير والكرسي.",
                            },
                            difficulty_level=1,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 2},
                            prerequisite_keys=[],
                        ),
                        ObjectiveDef(
                            key="obj.life.match_objects_to_names",
                            id=get_curriculum_uuid("obj.life.match_objects_to_names"),
                            title={"en": "Match objects to their names", "ar": "مطابقة الأشياء بأسمائها"},
                            description={
                                "en": "Connect picture cards of common objects to their written labels.",
                                "ar": "ربط صور الأشياء الشائعة بتسمياتها المكتوبة.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.life.identify_classroom_objects", "obj.life.identify_household_objects"],
                        ),
                        ObjectiveDef(
                            key="obj.life.match_identical_objects",
                            id=get_curriculum_uuid("obj.life.match_identical_objects"),
                            title={"en": "Match identical objects", "ar": "مطابقة الأشياء المتطابقة"},
                            description={
                                "en": "Pair identical visual objects among distracting items.",
                                "ar": "مطابقة عناصر بصرية متماثلة بين عناصر مشتتة.",
                            },
                            difficulty_level=1,
                            assessment_criteria={"minimum_accuracy": 0.90, "maximum_assistance_level": 2},
                            prerequisite_keys=["obj.life.match_objects_to_names"],
                        ),
                        ObjectiveDef(
                            key="obj.life.identify_object_by_description",
                            id=get_curriculum_uuid("obj.life.identify_object_by_description"),
                            title={"en": "Identify an object based on a simple description", "ar": "تحديد شيء بناءً على وصف بسيط"},
                            description={
                                "en": "Select the correct object from functional clue (e.g. 'You use this to drink water').",
                                "ar": "اختيار الشيء الصحيح بناءً على وظيفته (مثال: 'نستخدمه لشرب الماء').",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.life.match_identical_objects"],
                        ),
                    ],
                )
            ],
        ),
        # Unit 3: Sorting & Classification
        UnitDef(
            key="unit.life.sorting_classification",
            id=get_curriculum_uuid("unit.life.sorting_classification"),
            title={"en": "Sorting & Classification", "ar": "الفرز والتصنيف"},
            description={
                "en": "Grouping objects by function, size, visual characteristics, finding related pairs, and odd-one-out.",
                "ar": "تجميع الأشياء حسب الوظيفة والحجم والخصائص البصرية، واكتشاف العنصر المختلف.",
            },
            lessons=[
                LessonDef(
                    key="lesson.life.sorting_categories",
                    id=get_curriculum_uuid("lesson.life.sorting_categories"),
                    title={"en": "Categorization Skills", "ar": "مهارات التصنيف"},
                    description={
                        "en": "Sorting into buckets and identifying category relationships.",
                        "ar": "الفرز في مجموعات وتحديد العلاقات التصنيفية.",
                    },
                    objectives=[
                        ObjectiveDef(
                            key="obj.life.sort_by_type",
                            id=get_curriculum_uuid("obj.life.sort_by_type"),
                            title={"en": "Sort objects by type", "ar": "فرز الأشياء حسب النوع"},
                            description={
                                "en": "Categorize objects into clear domains (e.g. clothing vs food vs school supplies).",
                                "ar": "تصنيف العناصر في مجالات واضحة (مثل الملابس مقابل الطعام مقابل الأدوات المدرسية).",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.life.match_identical_objects"],
                        ),
                        ObjectiveDef(
                            key="obj.life.sort_by_size",
                            id=get_curriculum_uuid("obj.life.sort_by_size"),
                            title={"en": "Sort objects by size", "ar": "فرز الأشياء حسب الحجم"},
                            description={
                                "en": "Classify items into Big and Small containers.",
                                "ar": "تصنيف العناصر إلى حاويات الكبير والصغير.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.life.sort_by_type"],
                        ),
                        ObjectiveDef(
                            key="obj.life.sort_by_shape",
                            id=get_curriculum_uuid("obj.life.sort_by_shape"),
                            title={"en": "Sort objects by shape", "ar": "فرز الأشياء حسب الشكل"},
                            description={
                                "en": "Group everyday items based on their primary visual contour (round items vs boxy items).",
                                "ar": "تجميع الأدوات اليومية بناءً على محيطها البصري الأساسي.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.life.sort_by_size"],
                        ),
                        ObjectiveDef(
                            key="obj.life.match_objects_belong_together",
                            id=get_curriculum_uuid("obj.life.match_objects_belong_together"),
                            title={"en": "Match objects that belong together", "ar": "مطابقة الأشياء المترابطة معاً"},
                            description={
                                "en": "Pair functionally related tools (e.g. toothbrush ↔ toothpaste, lock ↔ key).",
                                "ar": "ربط الأدوات المترابطة وظيفياً معاً.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.life.sort_by_shape"],
                        ),
                        ObjectiveDef(
                            key="obj.life.identify_does_not_belong",
                            id=get_curriculum_uuid("obj.life.identify_does_not_belong"),
                            title={"en": "Identify which item does not belong", "ar": "تحديد العنصر الذي لا ينتمي للمجموعة"},
                            description={
                                "en": "Find the odd item out in a group of 3 or 4 similar category members.",
                                "ar": "اكتشاف العنصر المختلف ضمن مجموعة من العناصر المتشابهة.",
                            },
                            difficulty_level=3,
                            assessment_criteria={"minimum_accuracy": 0.80, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.life.match_objects_belong_together"],
                        ),
                    ],
                )
            ],
        ),
        # Unit 4: Everyday Decisions & Basic Safety
        UnitDef(
            key="unit.life.everyday_safety",
            id=get_curriculum_uuid("unit.life.everyday_safety"),
            title={"en": "Everyday Decisions & Basic Safety", "ar": "القرارات اليومية والسلامة الأساسية"},
            description={
                "en": "Practical decision-making, distinguishing safe from unsafe scenarios, pedestrian awareness, and safe household routines.",
                "ar": "اتخاذ القرارات العملية، والتمييز بين الآمن وغير الآمن، وإدراك السلامة المرورية والمنزلية.",
            },
            lessons=[
                LessonDef(
                    key="lesson.life.safety_awareness",
                    id=get_curriculum_uuid("lesson.life.safety_awareness"),
                    title={"en": "Safe Choices", "ar": "الخيارات الآمنة"},
                    description={
                        "en": "Simple, non-medical everyday awareness and positive decision choices.",
                        "ar": "الوعي اليومي البسيط والقرارات الإيجابية غير الطبية.",
                    },
                    objectives=[
                        ObjectiveDef(
                            key="obj.life.appropriate_action_everyday",
                            id=get_curriculum_uuid("obj.life.appropriate_action_everyday"),
                            title={"en": "Identify an appropriate action in a simple everyday situation", "ar": "تحديد التصرف المناسب في موقف يومي بسيط"},
                            description={
                                "en": "Choose the helpful or polite action (e.g. wipe up spilled water, raise hand to speak).",
                                "ar": "اختيار التصرف المفيد أو اللائق في المواقف اليومية.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.life.identify_daily_activities"],
                        ),
                        ObjectiveDef(
                            key="obj.life.distinguish_safe_vs_unsafe",
                            id=get_curriculum_uuid("obj.life.distinguish_safe_vs_unsafe"),
                            title={"en": "Distinguish safe vs unsafe everyday scenarios", "ar": "التمييز بين المواقف الآمنة وغير الآمنة"},
                            description={
                                "en": "Categorize illustrated scenes into Safe or Unsafe actions (e.g. walking carefully vs running on wet floor).",
                                "ar": "تصنيف المواقف المصورة إلى آمنة أو غير آمنة.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.life.appropriate_action_everyday"],
                        ),
                        ObjectiveDef(
                            key="obj.life.before_crossing_road",
                            id=get_curriculum_uuid("obj.life.before_crossing_road"),
                            title={"en": "Identify what to do before crossing a road", "ar": "تحديد ما يجب فعله قبل عبور الطريق"},
                            description={
                                "en": "Recognize the core pedestrian rule: stop at the curb, hold an adult's hand, and look both ways.",
                                "ar": "التعرف على قاعدة المشاة الأساسية: التوقف، ومسك يد شخص بالغ، والنظر في الاتجاهين.",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.90, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.life.distinguish_safe_vs_unsafe"],
                        ),
                        ObjectiveDef(
                            key="obj.life.safe_household_behavior",
                            id=get_curriculum_uuid("obj.life.safe_household_behavior"),
                            title={"en": "Identify appropriate behavior around common household situations", "ar": "تحديد السلوك المناسب حول المواقف المنزلية الشائعة"},
                            description={
                                "en": "Choose safe conduct around hot objects, electrical plugs, and cleaning tools (e.g. ask an adult for help).",
                                "ar": "اختيار السلوك الآمن حول الأدوات الساخنة والكهرباء (مثل طلب مساعدة شخص بالغ).",
                            },
                            difficulty_level=2,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.life.before_crossing_road"],
                        ),
                        ObjectiveDef(
                            key="obj.life.sequence_safe_routine",
                            id=get_curriculum_uuid("obj.life.sequence_safe_routine"),
                            title={"en": "Sequence a simple safe routine", "ar": "تسلسل روتين آمن بسيط"},
                            description={
                                "en": "Arrange the steps of a safe process in order (e.g. washing hands before eating: wet hands → soap → rinse → dry).",
                                "ar": "ترتيب خطوات عملية آمنة بالتتابع الصحيح (مثل غسل اليدين).",
                            },
                            difficulty_level=3,
                            assessment_criteria={"minimum_accuracy": 0.85, "maximum_assistance_level": 1},
                            prerequisite_keys=["obj.life.safe_household_behavior"],
                        ),
                    ],
                )
            ],
        ),
    ]

    # Combine into top-level CurriculumDef
    subjects: list[SubjectDef] = [
        SubjectDef(
            key="subject.math",
            id=get_curriculum_uuid("subject.math"),
            title={"en": "Foundational Mathematics", "ar": "الرياضيات التأسيسية"},
            description={
                "en": "Counting, numerical sequence, early arithmetic, and spatial geometry.",
                "ar": "العد، والتسلسل العددي، والحساب المبكر، والهندسة الفراغية.",
            },
            units=math_units,
        ),
        SubjectDef(
            key="subject.literacy",
            id=get_curriculum_uuid("subject.literacy"),
            title={"en": "Early Literacy", "ar": "القراءة والكتابة المبكرة"},
            description={
                "en": "Letter recognition, phonics, sight words, and narrative comprehension.",
                "ar": "التعرف على الحروف، والأصوات اللغوية، والكلمات البصرية، والفهم القرائي.",
            },
            units=literacy_units,
        ),
        SubjectDef(
            key="subject.everyday",
            id=get_curriculum_uuid("subject.everyday"),
            title={"en": "Everyday Learning Skills", "ar": "مهارات التعلم الحياتية"},
            description={
                "en": "Daily functional routines, object categorization, and safety awareness.",
                "ar": "الروتين اليومي الوظيفي، وتصنيف الأدوات، والوعي بالسلامة الشخصية.",
            },
            units=everyday_units,
        ),
    ]

    return CurriculumDef(
        id=get_curriculum_uuid("curriculum.foundational"),
        title={"en": "Eduvia Foundational Curriculum", "ar": "منهج إدوفيا التأسيسي"},
        description={
            "en": "Accessible, structured, mastery-based foundational curriculum designed for diverse learners.",
            "ar": "منهج تأسيسي منظم وقائم على الإتقان وميسر الوصول لجميع المتعلمين.",
        },
        subjects=subjects,
    )


TARGET_CURRICULUM: CurriculumDef = get_target_curriculum_catalog()
CURRICULUM_ID: uuid.UUID = TARGET_CURRICULUM.id
CURRICULUM_TITLE: dict[str, str] = TARGET_CURRICULUM.title
CURRICULUM_DESCRIPTION: dict[str, str] = TARGET_CURRICULUM.description
CURRICULUM_VERSION: str = "demo-1.0"

SUBJECT_MATH_ID: uuid.UUID = get_curriculum_uuid("subject.math")
SUBJECT_LITERACY_ID: uuid.UUID = get_curriculum_uuid("subject.literacy")
SUBJECT_EVERYDAY_ID: uuid.UUID = get_curriculum_uuid("subject.everyday")


def _convert_catalog_to_dicts(catalog_def: CurriculumDef) -> list[dict[str, Any]]:
    """Convert CurriculumDef dataclass tree into plain dictionaries for services."""
    subjects_list: list[dict[str, Any]] = []
    for s_idx, s in enumerate(catalog_def.subjects, 1):
        units_list: list[dict[str, Any]] = []
        for u_idx, u in enumerate(s.units, 1):
            lessons_list: list[dict[str, Any]] = []
            for l_idx, l in enumerate(u.lessons, 1):
                objs_list: list[dict[str, Any]] = []
                for o_idx, o in enumerate(l.objectives, 1):
                    prereq_uuids = [get_curriculum_uuid(pk) for pk in o.prerequisite_keys]
                    objs_list.append(
                        {
                            "id": o.id,
                            "key": o.key,
                            "lesson_id": l.id,
                            "title": o.title,
                            "description": o.description,
                            "difficulty_level": o.difficulty_level,
                            "assessment_criteria": o.assessment_criteria,
                            "prerequisites": prereq_uuids,
                            "order_index": o_idx,
                            "is_active": True,
                        }
                    )
                lessons_list.append(
                    {
                        "id": l.id,
                        "key": l.key,
                        "unit_id": u.id,
                        "title": l.title,
                        "description": l.description,
                        "order_index": l_idx,
                        "learning_objectives": objs_list,
                    }
                )
            units_list.append(
                {
                    "id": u.id,
                    "key": u.key,
                    "subject_id": s.id,
                    "title": u.title,
                    "description": u.description,
                    "order_index": u_idx,
                    "lessons": lessons_list,
                }
            )
        subjects_list.append(
            {
                "id": s.id,
                "key": s.key,
                "curriculum_id": catalog_def.id,
                "title": s.title,
                "description": s.description,
                "order_index": s_idx,
                "units": units_list,
            }
        )
    return subjects_list


FULL_CURRICULUM_CATALOG: list[dict[str, Any]] = _convert_catalog_to_dicts(TARGET_CURRICULUM)


def get_all_curriculum_objectives() -> list[dict[str, Any]]:
    """Return a flat list of all learning objectives in the curriculum."""
    objs: list[dict[str, Any]] = []
    for s in FULL_CURRICULUM_CATALOG:
        for u in s.get("units", []):
            for l in u.get("lessons", []):
                for o in l.get("learning_objectives", []):
                    objs.append(o)
    return objs


def get_objective_by_id(oid: uuid.UUID) -> dict[str, Any] | None:
    """Retrieve an objective by its UUID."""
    for obj in get_all_curriculum_objectives():
        if obj["id"] == oid:
            return obj
    return None


def get_prerequisites_map() -> dict[uuid.UUID, list[uuid.UUID]]:
    """Return a mapping of objective_id -> list of prerequisite objective_ids."""
    prereq_map: dict[uuid.UUID, list[uuid.UUID]] = {}
    for obj in get_all_curriculum_objectives():
        if obj.get("prerequisites"):
            prereq_map[obj["id"]] = list(obj["prerequisites"])
    return prereq_map

