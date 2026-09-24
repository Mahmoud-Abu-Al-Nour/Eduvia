"""
Eduvia — Expanded Everyday Learning Content Bank Items

Provides authoritative educational items for all 19 everyday learning objectives,
ensuring complete coverage across all 5 activity modalities.
"""
from __future__ import annotations

from app.activities.schemas import ActivityType
from app.content.definitions import ContentItemDef

def get_expanded_everyday_items() -> list[ContentItemDef]:
    items: list[ContentItemDef] = []
    items.append(
        ContentItemDef(
            content_key='life.routine.mc_brush_teeth',
            objective_key='obj.life.identify_daily_activities',
            subject_code='everyday',
            unit_code='unit.life.daily_routines',
            difficulty_level=1,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which activity shows brushing teeth 🪥?', 'ar': 'أي نشاط يظهر تنظيف الأسنان 🪥؟'},
            content_payload={'question': 'Which activity shows brushing teeth 🪥?', 'options': [{'id': 'ans_brush', 'text': 'Brushing Teeth 🪥', 'visual_cue': 'brushing teeth', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_sleep', 'text': 'Sleeping in Bed 🛏️', 'visual_cue': 'sleeping', 'is_correct': False, 'distractor_rationale': 'Shows resting in bed'}, {'id': 'ans_eat', 'text': 'Eating Lunch 🥪', 'visual_cue': 'eating', 'is_correct': False, 'distractor_rationale': 'Shows eating meal'}], 'correct_answer_id': 'ans_brush', 'explanation': 'Correct! Brushing teeth keeps smiles healthy and clean.'},
            correct_answer={'correct_answer_id': 'ans_brush'},
            explanation={'en': 'Correct! Brushing teeth keeps smiles healthy and clean.', 'ar': 'صحيح! تنظيف الأسنان يحافظ على صحة الابتسامة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.routine.vis_eat_breakfast',
            objective_key='obj.life.identify_daily_activities',
            subject_code='everyday',
            unit_code='unit.life.daily_routines',
            difficulty_level=1,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the child eating breakfast at the kitchen table.', 'ar': 'حدد الطفل الذي يتناول وجبة الإفطار على طاولة المطبخ.'},
            content_payload={'prompt': 'Spot the child eating breakfast at the kitchen table.', 'scene_description': 'A kitchen scene with breakfast cereal, a school bag, and a coat rack.', 'elements': [{'id': 'act_bag', 'label': 'Packing Backpack 🎒', 'category': 'activity', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'act_breakfast', 'label': 'Child Eating Breakfast 🥣', 'category': 'activity', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'act_coat', 'label': 'Hanging Coat 🧥', 'category': 'activity', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'act_breakfast', 'feedback_clue': 'Look at the kitchen table with the cereal bowl.'},
            correct_answer={'target_id': 'act_breakfast'},
            explanation={'en': 'Super! That is eating a nutritious breakfast.', 'ar': 'ممتاز! هذا تناول وجبة إفطار مغذية.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.routine.match_day_times',
            objective_key='obj.life.identify_daily_activities',
            subject_code='everyday',
            unit_code='unit.life.daily_routines',
            difficulty_level=1,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match daily activities to the correct time of day.', 'ar': 'طابق الأنشطة اليومية بوقتها المناسب من اليوم.'},
            content_payload={'prompt': 'Match daily activities to the correct time of day.', 'left_items': [{'id': 'act_wake', 'label': 'Waking Up ⏰', 'visual_cue': 'wake'}, {'id': 'act_sleep_night', 'label': 'Sleeping in Bed 🛏️', 'visual_cue': 'bed'}], 'right_items': [{'id': 'time_morn', 'label': 'Morning Time 🌅', 'visual_cue': 'morning'}, {'id': 'time_night', 'label': 'Night Time 🌙', 'visual_cue': 'night'}], 'pairs': [{'left_id': 'act_wake', 'right_id': 'time_morn'}, {'left_id': 'act_sleep_night', 'right_id': 'time_night'}]},
            correct_answer={'pairs': [{'left_id': 'act_wake', 'right_id': 'time_morn'}, {'left_id': 'act_sleep_night', 'right_id': 'time_night'}]},
            explanation={'en': 'Great routine matching! Waking up in morning, sleeping at night.', 'ar': 'مطابقة روتينية رائعة! الاستيقاظ صباحاً والنوم ليلاً.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.routine.drag.sort_morning_night',
            objective_key='obj.life.identify_daily_activities',
            subject_code='everyday',
            unit_code='unit.life.daily_routines',
            difficulty_level=1,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort activities into 'Morning Routine' and 'Night Routine'.", 'ar': "صنف الأنشطة إلى 'روتين الصباح' و 'روتين المساء'."},
            content_payload={'prompt': "Sort activities into 'Morning Routine' and 'Night Routine'.", 'items': [{'id': 'm_face', 'label': 'Wash face 🧼', 'visual_cue': 'wash face'}, {'id': 'm_cereal', 'label': 'Eat morning cereal 🥣', 'visual_cue': 'cereal'}, {'id': 'n_pajamas', 'label': 'Put on pajamas 👕', 'visual_cue': 'pajamas'}, {'id': 'n_story', 'label': 'Listen to bedtime story 📖', 'visual_cue': 'bedtime story'}], 'zones': [{'id': 'z_morning', 'label': 'Morning Routine 🌅', 'capacity': 3}, {'id': 'z_night', 'label': 'Night Routine 🌙', 'capacity': 3}], 'correct_mapping': {'m_face': 'z_morning', 'm_cereal': 'z_morning', 'n_pajamas': 'z_night', 'n_story': 'z_night'}},
            correct_answer={'correct_mapping': {'m_face': 'z_morning', 'm_cereal': 'z_morning', 'n_pajamas': 'z_night', 'n_story': 'z_night'}},
            explanation={'en': 'Terrific sorting of daily activities by routine time!', 'ar': 'فرز رائع للأنشطة اليومية حسب وقت الروتين!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.routine.mc_before_sleep',
            objective_key='obj.life.identify_daily_activities',
            subject_code='everyday',
            unit_code='unit.life.daily_routines',
            difficulty_level=1,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'What activity do we do before going to sleep at night?', 'ar': 'ما النشاط الذي نقوم به قبل النوم ليلاً؟'},
            content_payload={'question': 'What activity do we do before going to sleep at night?', 'options': [{'id': 'ans_pajamas', 'text': 'Put on pajamas and get into bed 🛏️', 'visual_cue': 'bed', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_school_bus', 'text': 'Get on the school bus 🚌', 'visual_cue': 'bus', 'is_correct': False, 'distractor_rationale': 'School bus is in the morning'}], 'correct_answer_id': 'ans_pajamas', 'explanation': 'Spot on! We change into pajamas before sleeping.'},
            correct_answer={'correct_answer_id': 'ans_pajamas'},
            explanation={'en': 'Spot on! We change into pajamas before sleeping.', 'ar': 'صحيح! نرتدي ملابس النوم قبل النوم.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.routine.order.wake_wash_eat',
            objective_key='obj.life.order_morning_routines',
            subject_code='everyday',
            unit_code='unit.life.daily_routines',
            difficulty_level=2,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Order morning steps in sequence.', 'ar': 'رتب خطوات الصباح بالتسلسل.'},
            content_payload={'prompt': 'Order morning steps in sequence.', 'items': [{'id': 'st_wash', 'label': 'Wash Face 🧼', 'visual_cue': 'wash'}, {'id': 'st_wake', 'label': 'Wake Up in Bed ⏰', 'visual_cue': 'wake'}, {'id': 'st_eat', 'label': 'Eat Breakfast 🥣', 'visual_cue': 'breakfast'}], 'correct_sequence': ['st_wake', 'st_wash', 'st_eat'], 'direction': 'chronological'},
            correct_answer={'correct_sequence': ['st_wake', 'st_wash', 'st_eat']},
            explanation={'en': 'Awesome! Wake up, wash face, eat breakfast.', 'ar': 'رائع! استيقاظ، غسل الوجه، تناول الإفطار.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.routine.mc_after_wash_hands',
            objective_key='obj.life.order_morning_routines',
            subject_code='everyday',
            unit_code='unit.life.daily_routines',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'In the morning, after washing your face and hands, what do you do?', 'ar': 'في الصباح، بعد غسل وجهك ويديك، ماذا تفعل؟'},
            content_payload={'question': 'In the morning, after washing your face and hands, what do you do?', 'options': [{'id': 'ans_dry_towel', 'text': 'Dry with a clean towel 🧻', 'visual_cue': 'towel', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_go_bed', 'text': 'Go to sleep for the night 🌙', 'visual_cue': 'sleep', 'is_correct': False, 'distractor_rationale': 'It is morning, not nighttime'}], 'correct_answer_id': 'ans_dry_towel', 'explanation': 'Correct! You dry with a towel after washing.'},
            correct_answer={'correct_answer_id': 'ans_dry_towel'},
            explanation={'en': 'Correct! You dry with a towel after washing.', 'ar': 'صحيح! تجفف بالمنشفة بعد الغسيل.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.routine.match.step_numbers',
            objective_key='obj.life.order_morning_routines',
            subject_code='everyday',
            unit_code='unit.life.daily_routines',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match morning sequence steps to their order.', 'ar': 'طابق خطوات الصباح بترتيبها.'},
            content_payload={'prompt': 'Match morning sequence steps to their order.', 'left_items': [{'id': 'm_step1', 'label': 'Step 1: First', 'visual_cue': '1️⃣'}, {'id': 'm_step2', 'label': 'Step 2: Next', 'visual_cue': '2️⃣'}], 'right_items': [{'id': 'act_step1', 'label': 'Wake up ⏰', 'visual_cue': 'wake up'}, {'id': 'act_step2', 'label': 'Brush teeth 🪥', 'visual_cue': 'brush teeth'}], 'pairs': [{'left_id': 'm_step1', 'right_id': 'act_step1'}, {'left_id': 'm_step2', 'right_id': 'act_step2'}]},
            correct_answer={'pairs': [{'left_id': 'm_step1', 'right_id': 'act_step1'}, {'left_id': 'm_step2', 'right_id': 'act_step2'}]},
            explanation={'en': 'Super matching of morning sequence order!', 'ar': 'مطابقة ممتازة لترتيب تسلسل الصباح!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.routine.drag.sort_early_before_leave',
            objective_key='obj.life.order_morning_routines',
            subject_code='everyday',
            unit_code='unit.life.daily_routines',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort actions into 'Early Morning' and 'Before Leaving Home'.", 'ar': "صنف الأفعال إلى 'الصباح الباكر' و 'قبل مغادرة المنزل'."},
            content_payload={'prompt': "Sort actions into 'Early Morning' and 'Before Leaving Home'.", 'items': [{'id': 'act_open_eyes', 'label': 'Open eyes in bed ☀️', 'visual_cue': 'wake'}, {'id': 'act_stretch', 'label': 'Stretch arms 🙆', 'visual_cue': 'stretch'}, {'id': 'act_backpack', 'label': 'Pick up backpack 🎒', 'visual_cue': 'backpack'}, {'id': 'act_shoes_door', 'label': 'Put on shoes at door 👟', 'visual_cue': 'shoes'}], 'zones': [{'id': 'z_early', 'label': 'Early Morning', 'capacity': 3}, {'id': 'z_leave', 'label': 'Before Leaving Home', 'capacity': 3}], 'correct_mapping': {'act_open_eyes': 'z_early', 'act_stretch': 'z_early', 'act_backpack': 'z_leave', 'act_shoes_door': 'z_leave'}},
            correct_answer={'correct_mapping': {'act_open_eyes': 'z_early', 'act_stretch': 'z_early', 'act_backpack': 'z_leave', 'act_shoes_door': 'z_leave'}},
            explanation={'en': 'Terrific routine stage sorting!', 'ar': 'فرز رائع لمراحل الروتين!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.routine.mc_next_lunch',
            objective_key='obj.life.identify_next_in_routine',
            subject_code='everyday',
            unit_code='unit.life.daily_routines',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'You finish eating your lunch. What is the appropriate next step?', 'ar': 'أنهيت تناول غدائك. ما الخطوة التالية المناسبة؟'},
            content_payload={'question': 'You finish eating your lunch. What is the appropriate next step?', 'options': [{'id': 'ans_clean_plate', 'text': 'Clear plate and wash hands 🍽️🧼', 'visual_cue': 'clear plate', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_eat_breakfast', 'text': 'Eat breakfast again', 'visual_cue': 'breakfast', 'is_correct': False, 'distractor_rationale': 'Lunch was just completed'}], 'correct_answer_id': 'ans_clean_plate', 'explanation': 'Correct! We clear our plate and wash hands after eating.'},
            correct_answer={'correct_answer_id': 'ans_clean_plate'},
            explanation={'en': 'Correct! We clear our plate and wash hands after eating.', 'ar': 'صحيح! ننظف الطبق ونغسل أيدينا بعد الأكل.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.routine.vis_next_wash_dry',
            objective_key='obj.life.identify_next_in_routine',
            subject_code='everyday',
            unit_code='unit.life.daily_routines',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot what comes NEXT after rinsing soapy hands: clean towel 🧻.', 'ar': 'حدد ما يأتي تالياً بعد شطف اليدين بالماء: المنشفة النظيفة 🧻.'},
            content_payload={'prompt': 'Spot what comes NEXT after rinsing soapy hands: clean towel 🧻.', 'scene_description': 'A bathroom sink area.', 'elements': [{'id': 'it_sponge', 'label': 'Bath Sponge', 'category': 'item', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'it_towel', 'label': 'Clean Hand Towel 🧻', 'category': 'item', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'it_shampoo', 'label': 'Shampoo Bottle', 'category': 'item', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'it_towel', 'feedback_clue': 'Look next to the sink for the hanging dry towel.'},
            correct_answer={'target_id': 'it_towel'},
            explanation={'en': 'Wonderful! Next step is drying hands on the towel.', 'ar': 'رائع! الخطوة التالية تجفيف اليدين بالمنشفة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.routine.match_routine_pairs',
            objective_key='obj.life.identify_next_in_routine',
            subject_code='everyday',
            unit_code='unit.life.daily_routines',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match current routine step to what comes NEXT.', 'ar': 'طابق خطوة الروتين الحالية بما يأتي تالياً.'},
            content_payload={'prompt': 'Match current routine step to what comes NEXT.', 'left_items': [{'id': 'cur_socks', 'label': 'Put on socks 🧦', 'visual_cue': 'socks'}, {'id': 'cur_school_bus', 'label': 'Arrive at school 🏫', 'visual_cue': 'school'}], 'right_items': [{'id': 'nxt_shoes', 'label': 'Put on shoes 👟', 'visual_cue': 'shoes'}, {'id': 'nxt_classroom', 'label': 'Enter classroom 🚪', 'visual_cue': 'classroom'}], 'pairs': [{'left_id': 'cur_socks', 'right_id': 'nxt_shoes'}, {'left_id': 'cur_school_bus', 'right_id': 'nxt_classroom'}]},
            correct_answer={'pairs': [{'left_id': 'cur_socks', 'right_id': 'nxt_shoes'}, {'left_id': 'cur_school_bus', 'right_id': 'nxt_classroom'}]},
            explanation={'en': 'Great routine progression matching!', 'ar': 'مطابقة رائعة لتقدم الروتين!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.routine.mc_next_arrive_class',
            objective_key='obj.life.identify_next_in_routine',
            subject_code='everyday',
            unit_code='unit.life.daily_routines',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'You arrive at your classroom. What is the appropriate next step?', 'ar': 'وصلت إلى فصلك الدراسي. ما الخطوة التالية المناسبة؟'},
            content_payload={'question': 'You arrive at your classroom. What is the appropriate next step?', 'options': [{'id': 'ans_hang_bag', 'text': 'Hang up your backpack and sit at desk 🎒', 'visual_cue': 'desk', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_sleep_desk', 'text': 'Go to sleep on floor', 'visual_cue': 'sleep', 'is_correct': False, 'distractor_rationale': 'Class is beginning'}], 'correct_answer_id': 'ans_hang_bag', 'explanation': 'Super! Hang up your backpack and prepare to learn.'},
            correct_answer={'correct_answer_id': 'ans_hang_bag'},
            explanation={'en': 'Super! Hang up your backpack and prepare to learn.', 'ar': 'ممتاز! علق حقيبتك واستعد للتعلم.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.routine.drag.sort_now_next',
            objective_key='obj.life.identify_next_in_routine',
            subject_code='everyday',
            unit_code='unit.life.daily_routines',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort actions into 'Current Action' and 'Next Action'.", 'ar': "صنف الأفعال إلى 'الفعل الحالي' و 'الفعل التالي'."},
            content_payload={'prompt': "Sort actions into 'Current Action' and 'Next Action'.", 'items': [{'id': 'cur_read_story', 'label': 'Finish reading book chapter 📖', 'visual_cue': 'reading'}, {'id': 'nxt_bookmark', 'label': 'Put bookmark in place 🔖', 'visual_cue': 'bookmark'}, {'id': 'cur_rinse_paste', 'label': 'Rinse mouth with water 💧', 'visual_cue': 'water'}, {'id': 'nxt_spit_sink', 'label': 'Spit into sink carefully 🚰', 'visual_cue': 'sink'}], 'zones': [{'id': 'z_now', 'label': 'Current Action', 'capacity': 3}, {'id': 'z_after', 'label': 'Next Action', 'capacity': 3}], 'correct_mapping': {'cur_read_story': 'z_now', 'nxt_bookmark': 'z_after', 'cur_rinse_paste': 'z_now', 'nxt_spit_sink': 'z_after'}},
            correct_answer={'correct_mapping': {'cur_read_story': 'z_now', 'nxt_bookmark': 'z_after', 'cur_rinse_paste': 'z_now', 'nxt_spit_sink': 'z_after'}},
            explanation={'en': 'Terrific identification of next actions!', 'ar': 'تمييز رائع للأفعال التالية!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.routine.match_stages',
            objective_key='obj.life.match_activity_to_stage',
            subject_code='everyday',
            unit_code='unit.life.daily_routines',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each activity to its routine stage.', 'ar': 'طابق كل نشاط بمرحلة الروتين الخاصة به.'},
            content_payload={'prompt': 'Match each activity to its routine stage.', 'left_items': [{'id': 'act_breakfast_cereal', 'label': 'Eat Breakfast Cereal 🥣', 'visual_cue': 'cereal'}, {'id': 'act_bedtime_story', 'label': 'Listen to Bedtime Story 📖', 'visual_cue': 'story'}], 'right_items': [{'id': 'stg_morning', 'label': 'Morning Routine 🌅', 'visual_cue': 'morning'}, {'id': 'stg_night', 'label': 'Night Routine 🌙', 'visual_cue': 'night'}], 'pairs': [{'left_id': 'act_breakfast_cereal', 'right_id': 'stg_morning'}, {'left_id': 'act_bedtime_story', 'right_id': 'stg_night'}]},
            correct_answer={'pairs': [{'left_id': 'act_breakfast_cereal', 'right_id': 'stg_morning'}, {'left_id': 'act_bedtime_story', 'right_id': 'stg_night'}]},
            explanation={'en': 'Super matching of activities to routine stages!', 'ar': 'مطابقة ممتازة للأنشطة مع مراحل الروتين!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.routine.mc_bedtime_choice',
            objective_key='obj.life.match_activity_to_stage',
            subject_code='everyday',
            unit_code='unit.life.daily_routines',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which activity belongs in the Bedtime routine?', 'ar': 'أي نشاط ينتمي إلى روتين وقت النوم؟'},
            content_payload={'question': 'Which activity belongs in the Bedtime routine?', 'options': [{'id': 'ans_brush_pajamas', 'text': 'Brushing teeth and wearing pajamas 🪥👕', 'visual_cue': 'bedtime', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_school_recess', 'text': 'Playing at school playground recess ⚽', 'visual_cue': 'recess', 'is_correct': False, 'distractor_rationale': 'Recess belongs in school midday'}], 'correct_answer_id': 'ans_brush_pajamas', 'explanation': 'Correct! Bedtime includes pajamas and brushing teeth.'},
            correct_answer={'correct_answer_id': 'ans_brush_pajamas'},
            explanation={'en': 'Correct! Bedtime includes pajamas and brushing teeth.', 'ar': 'صحيح! وقت النوم يشمل ملابس النوم وتنظيف الأسنان.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.routine.vis_playtime_stage',
            objective_key='obj.life.match_activity_to_stage',
            subject_code='everyday',
            unit_code='unit.life.daily_routines',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the activity that belongs in afternoon playtime.', 'ar': 'حدد النشاط الذي ينتمي لوقت اللعب بعد الظهر.'},
            content_payload={'prompt': 'Spot the activity that belongs in afternoon playtime.', 'scene_description': 'A home living room with three activities.', 'elements': [{'id': 'ac_wake', 'label': 'Waking Up ⏰', 'category': 'activity', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'ac_play_blocks', 'label': 'Building with Toy Blocks 🧱', 'category': 'activity', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'ac_sleep_dark', 'label': 'Sleeping in Darkness 🛏️', 'category': 'activity', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'ac_play_blocks', 'feedback_clue': 'Look for the fun creative building blocks activity in the center.'},
            correct_answer={'target_id': 'ac_play_blocks'},
            explanation={'en': 'Great observation! Playing with blocks fits playtime.', 'ar': 'ملاحظة رائعة! اللعب بالمكعبات يناسب وقت اللعب.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.routine.drag.sort_school_bedtime',
            objective_key='obj.life.match_activity_to_stage',
            subject_code='everyday',
            unit_code='unit.life.daily_routines',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort daily tasks into 'School Day' and 'Bedtime'.", 'ar': "صنف المهام اليومية إلى 'يوم دراسي' و 'وقت النوم'."},
            content_payload={'prompt': "Sort daily tasks into 'School Day' and 'Bedtime'.", 'items': [{'id': 'tsk_desk_write', 'label': 'Writing at classroom desk ✏️', 'visual_cue': 'desk'}, {'id': 'tsk_listen_teacher', 'label': 'Listening to teacher 👩\u200d🏫', 'visual_cue': 'teacher'}, {'id': 'tsk_dim_lights', 'label': 'Dimming bedroom lamp 💡', 'visual_cue': 'lamp'}, {'id': 'tsk_snuggle_blanket', 'label': 'Snuggling under warm blanket 🛌', 'visual_cue': 'blanket'}], 'zones': [{'id': 'z_school', 'label': 'School Day', 'capacity': 3}, {'id': 'z_bedtime', 'label': 'Bedtime', 'capacity': 3}], 'correct_mapping': {'tsk_desk_write': 'z_school', 'tsk_listen_teacher': 'z_school', 'tsk_dim_lights': 'z_bedtime', 'tsk_snuggle_blanket': 'z_bedtime'}},
            correct_answer={'correct_mapping': {'tsk_desk_write': 'z_school', 'tsk_listen_teacher': 'z_school', 'tsk_dim_lights': 'z_bedtime', 'tsk_snuggle_blanket': 'z_bedtime'}},
            explanation={'en': 'Terrific categorization of day stages!', 'ar': 'تصنيف رائع لمراحل اليوم!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.obj.match.classroom_tools',
            objective_key='obj.life.identify_classroom_objects',
            subject_code='everyday',
            unit_code='unit.life.object_recognition',
            difficulty_level=1,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match classroom tools to their functions.', 'ar': 'طابق أدوات الفصل بوظائفها.'},
            content_payload={'prompt': 'Match classroom tools to their functions.', 'left_items': [{'id': 'tl_pencil', 'label': 'Pencil ✏️', 'visual_cue': 'pencil'}, {'id': 'tl_scissors', 'label': 'Safety Scissors ✂️', 'visual_cue': 'scissors'}], 'right_items': [{'id': 'fn_write', 'label': 'Used for drawing and writing', 'visual_cue': 'writing'}, {'id': 'fn_cut', 'label': 'Used for cutting paper shapes', 'visual_cue': 'cutting'}], 'pairs': [{'left_id': 'tl_pencil', 'right_id': 'fn_write'}, {'left_id': 'tl_scissors', 'right_id': 'fn_cut'}]},
            correct_answer={'pairs': [{'left_id': 'tl_pencil', 'right_id': 'fn_write'}, {'left_id': 'tl_scissors', 'right_id': 'fn_cut'}]},
            explanation={'en': 'Great matching! Pencil writes, scissors cut safely.', 'ar': 'مطابقة رائعة! القلم للكتابة والمقص للقص بأمان.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.obj.mc.cut_paper_tool',
            objective_key='obj.life.identify_classroom_objects',
            subject_code='everyday',
            unit_code='unit.life.object_recognition',
            difficulty_level=1,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which tool do you use to cut paper craft safely?', 'ar': 'أي أداة تستخدمها لقص الورق بأمان؟'},
            content_payload={'question': 'Which tool do you use to cut paper craft safely?', 'options': [{'id': 'ans_scissors', 'text': 'Safety Scissors ✂️', 'visual_cue': 'scissors', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_crayon', 'text': 'Crayon 🖍️', 'visual_cue': 'crayon', 'is_correct': False, 'distractor_rationale': 'Crayons color, they do not cut'}, {'id': 'ans_glue', 'text': 'Glue Stick 🧴', 'visual_cue': 'glue', 'is_correct': False, 'distractor_rationale': 'Glue sticks things together'}], 'correct_answer_id': 'ans_scissors', 'explanation': 'Correct! We use safety scissors to cut craft paper.'},
            correct_answer={'correct_answer_id': 'ans_scissors'},
            explanation={'en': 'Correct! We use safety scissors to cut craft paper.', 'ar': 'صحيح! نستخدم مقص الأمان لقص ورق الأشغال.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.obj.drag.sort_class_kitchen',
            objective_key='obj.life.identify_classroom_objects',
            subject_code='everyday',
            unit_code='unit.life.object_recognition',
            difficulty_level=1,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort items into 'Classroom Supplies' and 'Kitchen Items'.", 'ar': "صنف العناصر إلى 'أدوات الفصل' و 'أدوات المطبخ'."},
            content_payload={'prompt': "Sort items into 'Classroom Supplies' and 'Kitchen Items'.", 'items': [{'id': 'cs_ruler', 'label': 'Ruler 📏', 'visual_cue': 'ruler'}, {'id': 'cs_notebook', 'label': 'Notebook 📓', 'visual_cue': 'notebook'}, {'id': 'kt_frying_pan', 'label': 'Frying Pan 🍳', 'visual_cue': 'pan'}, {'id': 'kt_soup_ladle', 'label': 'Soup Ladle 🥣', 'visual_cue': 'ladle'}], 'zones': [{'id': 'z_classroom', 'label': 'Classroom Supplies', 'capacity': 3}, {'id': 'z_kitchen', 'label': 'Kitchen Items', 'capacity': 3}], 'correct_mapping': {'cs_ruler': 'z_classroom', 'cs_notebook': 'z_classroom', 'kt_frying_pan': 'z_kitchen', 'kt_soup_ladle': 'z_kitchen'}},
            correct_answer={'correct_mapping': {'cs_ruler': 'z_classroom', 'cs_notebook': 'z_classroom', 'kt_frying_pan': 'z_kitchen', 'kt_soup_ladle': 'z_kitchen'}},
            explanation={'en': 'Brilliant object location sorting!', 'ar': 'فرز رائع لأماكن الأشياء!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.obj.mc.sleep_object',
            objective_key='obj.life.identify_household_objects',
            subject_code='everyday',
            unit_code='unit.life.object_recognition',
            difficulty_level=1,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which household object is used for sleeping comfortably?', 'ar': 'أي شيء منزلي يستخدم للنوم المريح؟'},
            content_payload={'question': 'Which household object is used for sleeping comfortably?', 'options': [{'id': 'ans_bed', 'text': 'Bed 🛏️', 'visual_cue': 'bed', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_fridge', 'text': 'Refrigerator 🧊', 'visual_cue': 'fridge', 'is_correct': False, 'distractor_rationale': 'Keeps food cold'}, {'id': 'ans_table', 'text': 'Dining Table 🪵', 'visual_cue': 'table', 'is_correct': False, 'distractor_rationale': 'Used for dining'}], 'correct_answer_id': 'ans_bed', 'explanation': 'Correct! A bed is used for sleeping.'},
            correct_answer={'correct_answer_id': 'ans_bed'},
            explanation={'en': 'Correct! A bed is used for sleeping.', 'ar': 'صحيح! السرير يستخدم للنوم.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.obj.vis_fridge',
            objective_key='obj.life.identify_household_objects',
            subject_code='everyday',
            unit_code='unit.life.object_recognition',
            difficulty_level=1,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the refrigerator in the kitchen.', 'ar': 'حدد الثلاجة في المطبخ.'},
            content_payload={'prompt': 'Spot the refrigerator in the kitchen.', 'scene_description': 'A bright family kitchen showing a sink, refrigerator, and table.', 'elements': [{'id': 'kt_sink', 'label': 'Kitchen Sink 🚰', 'category': 'appliance', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'kt_fridge', 'label': 'Tall Refrigerator 🧊', 'category': 'appliance', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'kt_stove', 'label': 'Cooking Stove 🔥', 'category': 'appliance', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'kt_fridge', 'feedback_clue': 'Look in the center for the tall appliance that keeps food cold.'},
            correct_answer={'target_id': 'kt_fridge'},
            explanation={'en': 'Super! That is the refrigerator.', 'ar': 'ممتاز! هذه هي الثلاجة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.obj.match.room_items',
            objective_key='obj.life.identify_household_objects',
            subject_code='everyday',
            unit_code='unit.life.object_recognition',
            difficulty_level=1,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match household items to their usual rooms.', 'ar': 'طابق الأدوات المنزلية بغرفها المعتادة.'},
            content_payload={'prompt': 'Match household items to their usual rooms.', 'left_items': [{'id': 'rm_sofa', 'label': 'Sofa 🛋️', 'visual_cue': 'sofa'}, {'id': 'rm_tub', 'label': 'Bathtub 🛁', 'visual_cue': 'bathtub'}], 'right_items': [{'id': 'pl_living', 'label': 'Living Room', 'visual_cue': 'living room'}, {'id': 'pl_bath', 'label': 'Bathroom', 'visual_cue': 'bathroom'}], 'pairs': [{'left_id': 'rm_sofa', 'right_id': 'pl_living'}, {'left_id': 'rm_tub', 'right_id': 'pl_bath'}]},
            correct_answer={'pairs': [{'left_id': 'rm_sofa', 'right_id': 'pl_living'}, {'left_id': 'rm_tub', 'right_id': 'pl_bath'}]},
            explanation={'en': 'Great matching! Sofa in living room, bathtub in bathroom.', 'ar': 'مطابقة رائعة! الأريكة في غرفة الجلوس وحوض الاستحمام في الحمام.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.obj.drag.sort_kitchen_bed',
            objective_key='obj.life.identify_household_objects',
            subject_code='everyday',
            unit_code='unit.life.object_recognition',
            difficulty_level=1,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort items into 'Kitchen' and 'Bedroom'.", 'ar': "صنف العناصر إلى 'المطبخ' و 'غرفة النوم'."},
            content_payload={'prompt': "Sort items into 'Kitchen' and 'Bedroom'.", 'items': [{'id': 'h_pot', 'label': 'Cooking Pot 🍲', 'visual_cue': 'pot'}, {'id': 'h_kettle', 'label': 'Tea Kettle 🫖', 'visual_cue': 'kettle'}, {'id': 'h_pillow', 'label': 'Bed Pillow 🛏️', 'visual_cue': 'pillow'}, {'id': 'h_wardrobe', 'label': 'Clothes Wardrobe 🚪', 'visual_cue': 'wardrobe'}], 'zones': [{'id': 'z_kit', 'label': 'Kitchen', 'capacity': 3}, {'id': 'z_bed', 'label': 'Bedroom', 'capacity': 3}], 'correct_mapping': {'h_pot': 'z_kit', 'h_kettle': 'z_kit', 'h_pillow': 'z_bed', 'h_wardrobe': 'z_bed'}},
            correct_answer={'correct_mapping': {'h_pot': 'z_kit', 'h_kettle': 'z_kit', 'h_pillow': 'z_bed', 'h_wardrobe': 'z_bed'}},
            explanation={'en': 'Terrific sorting of household items by room!', 'ar': 'فرز رائع للأدوات المنزلية حسب الغرفة!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.obj.mc.eat_soup_tool',
            objective_key='obj.life.identify_household_objects',
            subject_code='everyday',
            unit_code='unit.life.object_recognition',
            difficulty_level=1,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'What kitchen utensil do you use to eat warm soup?', 'ar': 'ما هي أداة المطبخ التي تستخدمها لتناول الحساء الدافئ؟'},
            content_payload={'question': 'What kitchen utensil do you use to eat warm soup?', 'options': [{'id': 'ans_spoon', 'text': 'Spoon 🥄', 'visual_cue': 'spoon', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_fork', 'text': 'Fork 🍴', 'visual_cue': 'fork', 'is_correct': False, 'distractor_rationale': 'Soup falls through fork prongs'}, {'id': 'ans_knife', 'text': 'Butter Knife 🔪', 'visual_cue': 'knife', 'is_correct': False, 'distractor_rationale': 'Knife cuts food'}], 'correct_answer_id': 'ans_spoon', 'explanation': 'Spot on! We use a spoon to enjoy soup.'},
            correct_answer={'correct_answer_id': 'ans_spoon'},
            explanation={'en': 'Spot on! We use a spoon to enjoy soup.', 'ar': 'صحيح! نستخدم الملعقة لتناول الحساء.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.obj.match.tools_names',
            objective_key='obj.life.match_objects_to_names',
            subject_code='everyday',
            unit_code='unit.life.object_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each object picture to its correct name.', 'ar': 'طابق كل صورة شيء باسمها الصحيح.'},
            content_payload={'prompt': 'Match each object picture to its correct name.', 'left_items': [{'id': 'p_book', 'label': 'Picture 📖', 'visual_cue': 'book'}, {'id': 'p_chair', 'label': 'Picture 🪑', 'visual_cue': 'chair'}, {'id': 'p_clock', 'label': 'Picture ⏰', 'visual_cue': 'clock'}], 'right_items': [{'id': 'n_book', 'label': 'BOOK', 'visual_cue': 'BOOK'}, {'id': 'n_chair', 'label': 'CHAIR', 'visual_cue': 'CHAIR'}, {'id': 'n_clock', 'label': 'CLOCK', 'visual_cue': 'CLOCK'}], 'pairs': [{'left_id': 'p_book', 'right_id': 'n_book'}, {'left_id': 'p_chair', 'right_id': 'n_chair'}, {'left_id': 'p_clock', 'right_id': 'n_clock'}]},
            correct_answer={'pairs': [{'left_id': 'p_book', 'right_id': 'n_book'}, {'left_id': 'p_chair', 'right_id': 'n_chair'}, {'left_id': 'p_clock', 'right_id': 'n_clock'}]},
            explanation={'en': 'Perfect name-to-object matching!', 'ar': 'مطابقة مثالية بين الأسماء والأشياء!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.obj.mc.name_backpack',
            objective_key='obj.life.match_objects_to_names',
            subject_code='everyday',
            unit_code='unit.life.object_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which name matches this picture: 🎒 (Backpack)?', 'ar': 'أي اسم يطابق هذه الصورة: 🎒 (Backpack)؟'},
            content_payload={'question': 'Which name matches this picture: 🎒 (Backpack)?', 'options': [{'id': 'ans_backpack', 'text': 'BACKPACK', 'visual_cue': 'BACKPACK', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_desk', 'text': 'DESK', 'visual_cue': 'DESK', 'is_correct': False, 'distractor_rationale': 'A desk is furniture'}, {'id': 'ans_pencil', 'text': 'PENCIL', 'visual_cue': 'PENCIL', 'is_correct': False, 'distractor_rationale': 'A pencil is a writing tool'}], 'correct_answer_id': 'ans_backpack', 'explanation': 'Correct! That item is a BACKPACK.'},
            correct_answer={'correct_answer_id': 'ans_backpack'},
            explanation={'en': 'Correct! That item is a BACKPACK.', 'ar': 'صحيح! هذا الشيء هو BACKPACK (حقيبة ظهر).'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.obj.vis_find_lamp',
            objective_key='obj.life.match_objects_to_names',
            subject_code='everyday',
            unit_code='unit.life.object_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': "Find the object labeled 'LAMP' 💡.", 'ar': "حدد الشيء المسمى 'LAMP' 💡."},
            content_payload={'prompt': "Find the object labeled 'LAMP' 💡.", 'scene_description': 'A study room desk with a book, a lamp, and a pencil cup.', 'elements': [{'id': 'ob_book', 'label': 'Book 📖', 'category': 'object', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'ob_lamp', 'label': 'Desk Lamp 💡', 'category': 'object', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'ob_cup', 'label': 'Pencil Cup ✏️', 'category': 'object', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'ob_lamp', 'feedback_clue': 'Look in the center for the lamp giving off light.'},
            correct_answer={'target_id': 'ob_lamp'},
            explanation={'en': 'Awesome! You found the LAMP.', 'ar': 'رائع! لقد وجدت المصباح LAMP.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.obj.drag.labels_to_slots',
            objective_key='obj.life.match_objects_to_names',
            subject_code='everyday',
            unit_code='unit.life.object_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': 'Drag name labels to object slots: PENCIL and ERASER.', 'ar': 'اسحب بطاقات الأسماء إلى خانات الأشياء: PENCIL و ERASER.'},
            content_payload={'prompt': 'Drag name labels to object slots: PENCIL and ERASER.', 'items': [{'id': 'lbl_pencil', 'label': 'PENCIL', 'visual_cue': 'PENCIL'}, {'id': 'lbl_eraser', 'label': 'ERASER', 'visual_cue': 'ERASER'}], 'zones': [{'id': 'slt_pencil', 'label': 'Slot: Pencil ✏️', 'capacity': 1}, {'id': 'slt_eraser', 'label': 'Slot: Eraser 🧼', 'capacity': 1}], 'correct_mapping': {'lbl_pencil': 'slt_pencil', 'lbl_eraser': 'slt_eraser'}},
            correct_answer={'correct_mapping': {'lbl_pencil': 'slt_pencil', 'lbl_eraser': 'slt_eraser'}},
            explanation={'en': 'Super name labeling!', 'ar': 'تسمية ممتازة بالأسماء!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.obj.mc.pic_for_cup',
            objective_key='obj.life.match_objects_to_names',
            subject_code='everyday',
            unit_code='unit.life.object_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': "Which picture matches the name 'CUP'?", 'ar': "أي صورة تطابق الاسم 'CUP'؟"},
            content_payload={'question': "Which picture matches the name 'CUP'?", 'options': [{'id': 'ans_cup_pic', 'text': 'Cup with handle ☕', 'visual_cue': '☕', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_plate_pic', 'text': 'Flat plate 🍽️', 'visual_cue': '🍽️', 'is_correct': False, 'distractor_rationale': 'A plate is flat'}, {'id': 'ans_spoon_pic', 'text': 'Spoon 🥄', 'visual_cue': '🥄', 'is_correct': False, 'distractor_rationale': 'A spoon is a utensil'}], 'correct_answer_id': 'ans_cup_pic', 'explanation': 'Spot on! That is a CUP.'},
            correct_answer={'correct_answer_id': 'ans_cup_pic'},
            explanation={'en': 'Spot on! That is a CUP.', 'ar': 'صحيح! هذا هو الكوب CUP.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.obj.match.identical_shoes',
            objective_key='obj.life.match_identical_objects',
            subject_code='everyday',
            unit_code='unit.life.object_recognition',
            difficulty_level=1,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match identical everyday items.', 'ar': 'طابق الأشياء اليومية المتطابقة.'},
            content_payload={'prompt': 'Match identical everyday items.', 'left_items': [{'id': 'sh_red', 'label': 'Red Sneaker 👟', 'visual_cue': 'red sneaker'}, {'id': 'mug_yel', 'label': 'Yellow Mug ☕', 'visual_cue': 'yellow mug'}], 'right_items': [{'id': 'm_sh_red', 'label': 'Red Sneaker 👟', 'visual_cue': 'red sneaker'}, {'id': 'm_mug_yel', 'label': 'Yellow Mug ☕', 'visual_cue': 'yellow mug'}], 'pairs': [{'left_id': 'sh_red', 'right_id': 'm_sh_red'}, {'left_id': 'mug_yel', 'right_id': 'm_mug_yel'}]},
            correct_answer={'pairs': [{'left_id': 'sh_red', 'right_id': 'm_sh_red'}, {'left_id': 'mug_yel', 'right_id': 'm_mug_yel'}]},
            explanation={'en': 'Perfect identical item matching!', 'ar': 'مطابقة ممتازة للأشياء المتطابقة!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.obj.mc.match_umbrella',
            objective_key='obj.life.match_identical_objects',
            subject_code='everyday',
            unit_code='unit.life.object_recognition',
            difficulty_level=1,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which object is an EXACT match to the blue umbrella ☂️?', 'ar': 'أي شيء يطابق المظلة الزرقاء ☂️ تماماً؟'},
            content_payload={'question': 'Which object is an EXACT match to the blue umbrella ☂️?', 'options': [{'id': 'ans_blue_umb', 'text': 'Blue Umbrella ☂️', 'visual_cue': '☂️ (Blue)', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_yellow_umb', 'text': 'Yellow Umbrella 🌂', 'visual_cue': '🌂 (Yellow)', 'is_correct': False, 'distractor_rationale': 'Different color'}, {'id': 'ans_raincoat', 'text': 'Raincoat 🧥', 'visual_cue': 'coat', 'is_correct': False, 'distractor_rationale': 'Different item'}], 'correct_answer_id': 'ans_blue_umb', 'explanation': 'Correct! The blue umbrellas match identically.'},
            correct_answer={'correct_answer_id': 'ans_blue_umb'},
            explanation={'en': 'Correct! The blue umbrellas match identically.', 'ar': 'صحيح! المظلتان الزرقاوان متطابقتان تماماً.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.obj.vis_bottle_twin',
            objective_key='obj.life.match_identical_objects',
            subject_code='everyday',
            unit_code='unit.life.object_recognition',
            difficulty_level=1,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the twin water bottle that matches the green bottle.', 'ar': 'حدد قارورة الماء التوأم التي تطابق القارورة الخضراء.'},
            content_payload={'prompt': 'Spot the twin water bottle that matches the green bottle.', 'scene_description': 'A gym bench with three water bottles.', 'elements': [{'id': 'wb_blue', 'label': 'Blue Bottle', 'category': 'bottle', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'wb_green', 'label': 'Green Bottle 🟢', 'category': 'bottle', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'wb_red', 'label': 'Red Bottle', 'category': 'bottle', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'wb_green', 'feedback_clue': 'Look for the green bottle with the silver cap.'},
            correct_answer={'target_id': 'wb_green'},
            explanation={'en': 'Terrific spotting! The green bottles are identical.', 'ar': 'رائع! القارورتان الخضراوان متطابقتان.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.obj.drag.pair_identical_tools',
            objective_key='obj.life.match_identical_objects',
            subject_code='everyday',
            unit_code='unit.life.object_recognition',
            difficulty_level=1,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': 'Pair identical tools into matching toolboxes.', 'ar': 'زاوج الأدوات المتطابقة في صناديق الأدوات المطابقة.'},
            content_payload={'prompt': 'Pair identical tools into matching toolboxes.', 'items': [{'id': 't_hammer', 'label': 'Hammer 🔨', 'visual_cue': 'hammer'}, {'id': 't_wrench', 'label': 'Wrench 🔧', 'visual_cue': 'wrench'}], 'zones': [{'id': 'box_hammer', 'label': 'Toolbox: Hammer 🔨', 'capacity': 1}, {'id': 'box_wrench', 'label': 'Toolbox: Wrench 🔧', 'capacity': 1}], 'correct_mapping': {'t_hammer': 'box_hammer', 't_wrench': 'box_wrench'}},
            correct_answer={'correct_mapping': {'t_hammer': 'box_hammer', 't_wrench': 'box_wrench'}},
            explanation={'en': 'Super matching tool pairs!', 'ar': 'أزواج أدوات مطابقة ممتازة!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.obj.order.identical_crayons',
            objective_key='obj.life.match_identical_objects',
            subject_code='everyday',
            unit_code='unit.life.object_recognition',
            difficulty_level=1,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Arrange the colored crayons in rainbow order: Red, Yellow, Blue.', 'ar': 'رتب أقلام التلوين بترتيب ألوان قوس قزح: أحمر، أصفر، أزرق.'},
            content_payload={'prompt': 'Arrange the colored crayons in rainbow order: Red, Yellow, Blue.', 'items': [{'id': 'cr_yel', 'label': 'Yellow Crayon 🖍️', 'visual_cue': 'yellow'}, {'id': 'cr_red', 'label': 'Red Crayon 🖍️', 'visual_cue': 'red'}, {'id': 'cr_blu', 'label': 'Blue Crayon 🖍️', 'visual_cue': 'blue'}], 'correct_sequence': ['cr_red', 'cr_yel', 'cr_blu'], 'direction': 'ascending'},
            correct_answer={'correct_sequence': ['cr_red', 'cr_yel', 'cr_blu']},
            explanation={'en': 'Awesome color crayon ordering!', 'ar': 'ترتيب رائع لأقلام التلوين!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.obj.mc.desc_pillow',
            objective_key='obj.life.identify_object_by_description',
            subject_code='everyday',
            unit_code='unit.life.object_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'What is soft, sits on your bed, and you rest your head on it?', 'ar': 'ما هو الشيء الناعم الذي يوضع على سريرك وتسند رأسك عليه؟'},
            content_payload={'question': 'What is soft, sits on your bed, and you rest your head on it?', 'options': [{'id': 'ans_pillow', 'text': 'Pillow 🛏️', 'visual_cue': 'pillow', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_chair', 'text': 'Wooden Chair 🪑', 'visual_cue': 'chair', 'is_correct': False, 'distractor_rationale': 'A chair is hard and for sitting'}, {'id': 'ans_rug', 'text': 'Floor Rug 🧶', 'visual_cue': 'rug', 'is_correct': False, 'distractor_rationale': 'A rug goes on the floor'}], 'correct_answer_id': 'ans_pillow', 'explanation': 'Correct! A pillow is soft and used to rest your head.'},
            correct_answer={'correct_answer_id': 'ans_pillow'},
            explanation={'en': 'Correct! A pillow is soft and used to rest your head.', 'ar': 'صحيح! الوسادة ناعمة وتستخدم لإراحة الرأس.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.obj.vis_write_tool',
            objective_key='obj.life.identify_object_by_description',
            subject_code='everyday',
            unit_code='unit.life.object_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Find the object used to write and draw on paper.', 'ar': 'حدد الشيء المستخدم للكتابة والرسم على الورق.'},
            content_payload={'prompt': 'Find the object used to write and draw on paper.', 'scene_description': 'A desk with an apple, a pencil, and a clock.', 'elements': [{'id': 'ds_apple', 'label': 'Fresh Apple 🍎', 'category': 'object', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'ds_pencil', 'label': 'Yellow Pencil ✏️', 'category': 'object', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'ds_clock', 'label': 'Alarm Clock ⏰', 'category': 'object', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'ds_pencil', 'feedback_clue': 'Look in the center for the writing tool with graphite lead.'},
            correct_answer={'target_id': 'ds_pencil'},
            explanation={'en': 'Wonderful! A pencil is used for writing and drawing.', 'ar': 'رائع! القلم يستخدم للكتابة والرسم.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.obj.match.descriptions',
            objective_key='obj.life.identify_object_by_description',
            subject_code='everyday',
            unit_code='unit.life.object_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match descriptions to the correct object.', 'ar': 'طابق الأوصاف بالشيء الصحيح.'},
            content_payload={'prompt': 'Match descriptions to the correct object.', 'left_items': [{'id': 'd_clock', 'label': 'Tells the current time of day', 'visual_cue': 'tells time'}, {'id': 'd_fridge', 'label': 'Keeps milk and fruits cold and fresh', 'visual_cue': 'keeps cold'}], 'right_items': [{'id': 'o_clock', 'label': 'Clock ⏰', 'visual_cue': 'clock'}, {'id': 'o_fridge', 'label': 'Refrigerator 🧊', 'visual_cue': 'fridge'}], 'pairs': [{'left_id': 'd_clock', 'right_id': 'o_clock'}, {'left_id': 'd_fridge', 'right_id': 'o_fridge'}]},
            correct_answer={'pairs': [{'left_id': 'd_clock', 'right_id': 'o_clock'}, {'left_id': 'd_fridge', 'right_id': 'o_fridge'}]},
            explanation={'en': 'Terrific matching based on functional descriptions!', 'ar': 'مطابقة رائعة بناءً على الأوصاف الوظيفية!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.obj.mc.four_wheels_vehicle',
            objective_key='obj.life.identify_object_by_description',
            subject_code='everyday',
            unit_code='unit.life.object_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'What has 4 wheels, an engine, and carries families on roads?', 'ar': 'ما الذي له ٤ عجلات ومحرك وينقل العائلات على الطرق؟'},
            content_payload={'question': 'What has 4 wheels, an engine, and carries families on roads?', 'options': [{'id': 'ans_car', 'text': 'Car 🚗', 'visual_cue': 'car', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_kite', 'text': 'Kite 🪁', 'visual_cue': 'kite', 'is_correct': False, 'distractor_rationale': 'A kite flies in the sky'}, {'id': 'ans_boat', 'text': 'Sailboat ⛵', 'visual_cue': 'boat', 'is_correct': False, 'distractor_rationale': 'A boat sails on water'}], 'correct_answer_id': 'ans_car', 'explanation': 'Super! A car has 4 wheels and drives on roads.'},
            correct_answer={'correct_answer_id': 'ans_car'},
            explanation={'en': 'Super! A car has 4 wheels and drives on roads.', 'ar': 'ممتاز! السيارة لها ٤ عجلات وتسير على الطرق.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.obj.drag.worn_feet_head',
            objective_key='obj.life.identify_object_by_description',
            subject_code='everyday',
            unit_code='unit.life.object_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort clothing by description: 'Worn on Feet' and 'Worn on Head'.", 'ar': "صنف الملابس حسب الوصف: 'تلبس في القدمين' و 'تلبس على الرأس'."},
            content_payload={'prompt': "Sort clothing by description: 'Worn on Feet' and 'Worn on Head'.", 'items': [{'id': 'cl_shoes', 'label': 'Shoes 👟', 'visual_cue': 'shoes'}, {'id': 'cl_socks', 'label': 'Socks 🧦', 'visual_cue': 'socks'}, {'id': 'cl_cap', 'label': 'Baseball Cap 🧢', 'visual_cue': 'cap'}, {'id': 'cl_helmet', 'label': 'Bicycle Helmet ⛑️', 'visual_cue': 'helmet'}], 'zones': [{'id': 'z_feet', 'label': 'Worn on Feet', 'capacity': 3}, {'id': 'z_head', 'label': 'Worn on Head', 'capacity': 3}], 'correct_mapping': {'cl_shoes': 'z_feet', 'cl_socks': 'z_feet', 'cl_cap': 'z_head', 'cl_helmet': 'z_head'}},
            correct_answer={'correct_mapping': {'cl_shoes': 'z_feet', 'cl_socks': 'z_feet', 'cl_cap': 'z_head', 'cl_helmet': 'z_head'}},
            explanation={'en': 'Brilliant categorization by functional description!', 'ar': 'تصنيف رائع حسب الوصف الوظيفي!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.sort.drag.toys_tools',
            objective_key='obj.life.sort_by_type',
            subject_code='everyday',
            unit_code='unit.life.sorting_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort into 'Play Toys' and 'School Tools'.", 'ar': "صنف إلى 'ألعاب' و 'أدوات مدرسية'."},
            content_payload={'prompt': "Sort into 'Play Toys' and 'School Tools'.", 'items': [{'id': 't_teddy', 'label': 'Teddy Bear 🧸', 'visual_cue': 'teddy'}, {'id': 't_ball', 'label': 'Play Ball ⚽', 'visual_cue': 'ball'}, {'id': 's_pencil', 'label': 'Pencil ✏️', 'visual_cue': 'pencil'}, {'id': 's_notebook', 'label': 'Notebook 📓', 'visual_cue': 'notebook'}], 'zones': [{'id': 'z_toys', 'label': 'Play Toys', 'capacity': 3}, {'id': 'z_tools', 'label': 'School Tools', 'capacity': 3}], 'correct_mapping': {'t_teddy': 'z_toys', 't_ball': 'z_toys', 's_pencil': 'z_tools', 's_notebook': 'z_tools'}},
            correct_answer={'correct_mapping': {'t_teddy': 'z_toys', 't_ball': 'z_toys', 's_pencil': 'z_tools', 's_notebook': 'z_tools'}},
            explanation={'en': 'Great category type sorting!', 'ar': 'فرز رائع حسب نوع الفئة!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.sort.match.types',
            objective_key='obj.life.sort_by_type',
            subject_code='everyday',
            unit_code='unit.life.sorting_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each item to its category type.', 'ar': 'طابق كل عنصر بنوع فئته.'},
            content_payload={'prompt': 'Match each item to its category type.', 'left_items': [{'id': 'it_apple', 'label': 'Apple 🍎', 'visual_cue': 'apple'}, {'id': 'it_shirt', 'label': 'Shirt 👕', 'visual_cue': 'shirt'}], 'right_items': [{'id': 'cat_food', 'label': 'Type: Food 🍽️', 'visual_cue': 'food'}, {'id': 'cat_cloth', 'label': 'Type: Clothing 👗', 'visual_cue': 'clothing'}], 'pairs': [{'left_id': 'it_apple', 'right_id': 'cat_food'}, {'left_id': 'it_shirt', 'right_id': 'cat_cloth'}]},
            correct_answer={'pairs': [{'left_id': 'it_apple', 'right_id': 'cat_food'}, {'left_id': 'it_shirt', 'right_id': 'cat_cloth'}]},
            explanation={'en': 'Terrific matching by type!', 'ar': 'مطابقة رائعة حسب النوع!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.sort.mc.vehicle_type',
            objective_key='obj.life.sort_by_type',
            subject_code='everyday',
            unit_code='unit.life.sorting_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which item is a type of vehicle?', 'ar': 'أي عنصر يعتبر نوعاً من المركبات؟'},
            content_payload={'question': 'Which item is a type of vehicle?', 'options': [{'id': 'ans_bus', 'text': 'Bus 🚌', 'visual_cue': 'bus', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_apple', 'text': 'Apple 🍎', 'visual_cue': 'apple', 'is_correct': False, 'distractor_rationale': 'An apple is a food'}, {'id': 'ans_chair', 'text': 'Chair 🪑', 'visual_cue': 'chair', 'is_correct': False, 'distractor_rationale': 'A chair is furniture'}], 'correct_answer_id': 'ans_bus', 'explanation': 'Correct! A bus is a vehicle used for transportation.'},
            correct_answer={'correct_answer_id': 'ans_bus'},
            explanation={'en': 'Correct! A bus is a vehicle used for transportation.', 'ar': 'صحيح! الحافلة مركبة تستخدم للمواصلات.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.sort.vis.animal_among_fruits',
            objective_key='obj.life.sort_by_type',
            subject_code='everyday',
            unit_code='unit.life.sorting_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Find the animal among the grocery items.', 'ar': 'حدد الحيوان من بين عناصر البقالة.'},
            content_payload={'prompt': 'Find the animal among the grocery items.', 'scene_description': 'A picnic basket with bananas, an orange, and a kitten peek.', 'elements': [{'id': 'it_banana', 'label': 'Yellow Banana 🍌', 'category': 'food', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'it_kitten', 'label': 'Fluffy Kitten 🐱', 'category': 'animal', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'it_orange', 'label': 'Round Orange 🍊', 'category': 'food', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'it_kitten', 'feedback_clue': 'Spot the living pet sitting next to the fruit.'},
            correct_answer={'target_id': 'it_kitten'},
            explanation={'en': 'Awesome! The kitten is an animal, not a food.', 'ar': 'رائع! القطة حيوان أليف وليست طعاماً.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.sort.drag.small_large_everyday',
            objective_key='obj.life.sort_by_size',
            subject_code='everyday',
            unit_code='unit.life.sorting_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort items into 'Small Items' and 'Large Items'.", 'ar': "صنف العناصر إلى 'عناصر صغيرة' و 'عناصر كبيرة'."},
            content_payload={'prompt': "Sort items into 'Small Items' and 'Large Items'.", 'items': [{'id': 's_coin', 'label': 'Coin 🪙', 'visual_cue': 'coin'}, {'id': 's_key', 'label': 'Door Key 🔑', 'visual_cue': 'key'}, {'id': 'l_sofa', 'label': 'Living Room Sofa 🛋️', 'visual_cue': 'sofa'}, {'id': 'l_bed', 'label': 'Bedroom Bed 🛏️', 'visual_cue': 'bed'}], 'zones': [{'id': 'z_small_obj', 'label': 'Small Items', 'capacity': 3}, {'id': 'z_large_obj', 'label': 'Large Items', 'capacity': 3}], 'correct_mapping': {'s_coin': 'z_small_obj', 's_key': 'z_small_obj', 'l_sofa': 'z_large_obj', 'l_bed': 'z_large_obj'}},
            correct_answer={'correct_mapping': {'s_coin': 'z_small_obj', 's_key': 'z_small_obj', 'l_sofa': 'z_large_obj', 'l_bed': 'z_large_obj'}},
            explanation={'en': 'Super size sorting of everyday objects!', 'ar': 'فرز رائع للأشياء اليومية حسب الحجم!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.sort.mc.larger_animal',
            objective_key='obj.life.sort_by_size',
            subject_code='everyday',
            unit_code='unit.life.sorting_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which creature is LARGER?', 'ar': 'أي مخلوق أكبر حجماً؟'},
            content_payload={'question': 'Which creature is LARGER?', 'options': [{'id': 'ans_eleph', 'text': 'Elephant 🐘', 'visual_cue': 'elephant', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_butter', 'text': 'Butterfly 🦋', 'visual_cue': 'butterfly', 'is_correct': False, 'distractor_rationale': 'A butterfly is very small'}], 'correct_answer_id': 'ans_eleph', 'explanation': 'Correct! An elephant is much larger than a butterfly.'},
            correct_answer={'correct_answer_id': 'ans_eleph'},
            explanation={'en': 'Correct! An elephant is much larger than a butterfly.', 'ar': 'صحيح! الفيل أكبر بكثير من الفراشة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.sort.match.size_categories',
            objective_key='obj.life.sort_by_size',
            subject_code='everyday',
            unit_code='unit.life.sorting_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each object to its size category.', 'ar': 'طابق كل عنصر بفئة حجمه.'},
            content_payload={'prompt': 'Match each object to its size category.', 'left_items': [{'id': 'it_car', 'label': 'Family Car 🚗', 'visual_cue': 'car'}, {'id': 'it_button', 'label': 'Shirt Button 🔘', 'visual_cue': 'button'}], 'right_items': [{'id': 'sz_big', 'label': 'Large Size', 'visual_cue': 'large'}, {'id': 'sz_small', 'label': 'Small Size', 'visual_cue': 'small'}], 'pairs': [{'left_id': 'it_car', 'right_id': 'sz_big'}, {'left_id': 'it_button', 'right_id': 'sz_small'}]},
            correct_answer={'pairs': [{'left_id': 'it_car', 'right_id': 'sz_big'}, {'left_id': 'it_button', 'right_id': 'sz_small'}]},
            explanation={'en': 'Great size category matching!', 'ar': 'مطابقة ممتازة لفئات الأحجام!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.sort.order.containers',
            objective_key='obj.life.sort_by_size',
            subject_code='everyday',
            unit_code='unit.life.sorting_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Order drinking containers by capacity from smallest to largest.', 'ar': 'رتب أواني الشرب حسب السعة من الأصغر إلى الأكبر.'},
            content_payload={'prompt': 'Order drinking containers by capacity from smallest to largest.', 'items': [{'id': 'c_pitcher', 'label': 'Water Pitcher 🫖', 'visual_cue': 'pitcher'}, {'id': 'c_teacup', 'label': 'Small Teacup ☕', 'visual_cue': 'teacup'}, {'id': 'c_jug', 'label': 'Large Water Jug 🪣', 'visual_cue': 'jug'}], 'correct_sequence': ['c_teacup', 'c_pitcher', 'c_jug'], 'direction': 'ascending'},
            correct_answer={'correct_sequence': ['c_teacup', 'c_pitcher', 'c_jug']},
            explanation={'en': 'Terrific container size ordering!', 'ar': 'ترتيب رائع لأحجام الأوعية!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.sort.vis.smallest_box',
            objective_key='obj.life.sort_by_size',
            subject_code='everyday',
            unit_code='unit.life.sorting_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the SMALLEST gift box on the shelf.', 'ar': 'حدد أصغر صندوق هدايا على الرف.'},
            content_payload={'prompt': 'Spot the SMALLEST gift box on the shelf.', 'scene_description': 'A closet shelf with three wrapped boxes.', 'elements': [{'id': 'bx_large', 'label': 'Large Box 🎁', 'category': 'box', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'bx_medium', 'label': 'Medium Box 🎁', 'category': 'box', 'is_target': False, 'bounding_hint': 'center'}, {'id': 'bx_small', 'label': 'Smallest Tiny Box 🎁', 'category': 'box', 'is_target': True, 'bounding_hint': 'right'}], 'target_id': 'bx_small', 'feedback_clue': 'Look for the little box on the right.'},
            correct_answer={'target_id': 'bx_small'},
            explanation={'en': 'Spot on! That box is the smallest.', 'ar': 'صحيح! ذلك الصندوق هو الأصغر.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.sort.drag.round_square_objects',
            objective_key='obj.life.sort_by_shape',
            subject_code='everyday',
            unit_code='unit.life.sorting_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort everyday items into 'Round Items' and 'Square Items'.", 'ar': "صنف الأشياء اليومية إلى 'أشياء مستديرة' و 'أشياء مربعة'."},
            content_payload={'prompt': "Sort everyday items into 'Round Items' and 'Square Items'.", 'items': [{'id': 'rd_plate', 'label': 'Round Dinner Plate 🍽️', 'visual_cue': 'plate'}, {'id': 'rd_clock', 'label': 'Round Wall Clock ⏰', 'visual_cue': 'clock'}, {'id': 'sq_napkin', 'label': 'Square Napkin 🟫', 'visual_cue': 'napkin'}, {'id': 'sq_tile', 'label': 'Square Floor Tile 🔲', 'visual_cue': 'tile'}], 'zones': [{'id': 'z_round_items', 'label': 'Round Items ⭕', 'capacity': 3}, {'id': 'z_square_items', 'label': 'Square Items ⏹️', 'capacity': 3}], 'correct_mapping': {'rd_plate': 'z_round_items', 'rd_clock': 'z_round_items', 'sq_napkin': 'z_square_items', 'sq_tile': 'z_square_items'}},
            correct_answer={'correct_mapping': {'rd_plate': 'z_round_items', 'rd_clock': 'z_round_items', 'sq_napkin': 'z_square_items', 'sq_tile': 'z_square_items'}},
            explanation={'en': 'Super sorting of everyday objects by shape!', 'ar': 'فرز رائع للأشياء اليومية حسب الشكل!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.sort.match.object_shape_types',
            objective_key='obj.life.sort_by_shape',
            subject_code='everyday',
            unit_code='unit.life.sorting_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match everyday objects to their geometric shape.', 'ar': 'طابق الأشياء اليومية بشكلها الهندسي.'},
            content_payload={'prompt': 'Match everyday objects to their geometric shape.', 'left_items': [{'id': 'o_wheel', 'label': 'Bicycle Wheel 🛞', 'visual_cue': 'wheel'}, {'id': 'o_door', 'label': 'Classroom Door 🚪', 'visual_cue': 'door'}], 'right_items': [{'id': 's_round', 'label': 'Circular ⭕', 'visual_cue': 'circle'}, {'id': 's_rec', 'label': 'Rectangular 📄', 'visual_cue': 'rectangle'}], 'pairs': [{'left_id': 'o_wheel', 'right_id': 's_round'}, {'left_id': 'o_door', 'right_id': 's_rec'}]},
            correct_answer={'pairs': [{'left_id': 'o_wheel', 'right_id': 's_round'}, {'left_id': 'o_door', 'right_id': 's_rec'}]},
            explanation={'en': 'Great matching of objects to geometric shapes!', 'ar': 'مطابقة ممتازة للأشياء بالأشكال الهندسية!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.sort.mc.circle_food',
            objective_key='obj.life.sort_by_shape',
            subject_code='everyday',
            unit_code='unit.life.sorting_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which food has a round circular shape?', 'ar': 'أي طعام له شكل دائري مستدير؟'},
            content_payload={'question': 'Which food has a round circular shape?', 'options': [{'id': 'ans_pancake', 'text': 'Pancake 🥞', 'visual_cue': 'pancake', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_carrot', 'text': 'Carrot Stick 🥕', 'visual_cue': 'carrot', 'is_correct': False, 'distractor_rationale': 'A carrot stick is long and thin'}], 'correct_answer_id': 'ans_pancake', 'explanation': 'Correct! A pancake is cooked into a flat circle.'},
            correct_answer={'correct_answer_id': 'ans_pancake'},
            explanation={'en': 'Correct! A pancake is cooked into a flat circle.', 'ar': 'صحيح! الفطيرة تطهى على شكل دائرة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.sort.vis.triangular_watermelon',
            objective_key='obj.life.sort_by_shape',
            subject_code='everyday',
            unit_code='unit.life.sorting_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the triangular slice of watermelon 🍉 on the picnic blanket.', 'ar': 'حدد شريحة البطيخ المثلثة 🍉 على بساط النزهة.'},
            content_payload={'prompt': 'Spot the triangular slice of watermelon 🍉 on the picnic blanket.', 'scene_description': 'A picnic blanket with round grapes, an apple, and a watermelon slice.', 'elements': [{'id': 'pc_apple', 'label': 'Round Apple 🍎', 'category': 'food', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'pc_melon', 'label': 'Triangular Watermelon Slice 🍉', 'category': 'food', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'pc_grapes', 'label': 'Bunch of Grapes 🍇', 'category': 'food', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'pc_melon', 'feedback_clue': 'Look for the slice with 3 pointed sides.'},
            correct_answer={'target_id': 'pc_melon'},
            explanation={'en': 'Awesome! The watermelon slice is shaped like a triangle.', 'ar': 'رائع! شريحة البطيخ مثلثة الشكل.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.sort.mc.rec_school_item',
            objective_key='obj.life.sort_by_shape',
            subject_code='everyday',
            unit_code='unit.life.sorting_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which classroom item is rectangular with long and short sides?', 'ar': 'أي أداة بالفصل مستطيلة الشكل لها ضلعان طويلان وضلعان قصيران؟'},
            content_payload={'question': 'Which classroom item is rectangular with long and short sides?', 'options': [{'id': 'ans_book', 'text': 'Reading Textbook 📖', 'visual_cue': 'book', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_globe', 'text': 'Round World Globe 🌐', 'visual_cue': 'globe', 'is_correct': False, 'distractor_rationale': 'A globe is a round sphere'}], 'correct_answer_id': 'ans_book', 'explanation': 'Spot on! Textbooks have rectangular pages.'},
            correct_answer={'correct_answer_id': 'ans_book'},
            explanation={'en': 'Spot on! Textbooks have rectangular pages.', 'ar': 'صحيح! صفحات الكتب مستطيلة الشكل.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.sort.match.associated_pairs',
            objective_key='obj.life.match_objects_belong_together',
            subject_code='everyday',
            unit_code='unit.life.sorting_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match items that belong together in daily use.', 'ar': 'طابق الأشياء التي تستخدم معاً في الحياة اليومية.'},
            content_payload={'prompt': 'Match items that belong together in daily use.', 'left_items': [{'id': 'it_brush', 'label': 'Toothbrush 🪥', 'visual_cue': 'toothbrush'}, {'id': 'it_lock', 'label': 'Padlock 🔒', 'visual_cue': 'lock'}, {'id': 'it_shoe', 'label': 'Shoe 👟', 'visual_cue': 'shoe'}], 'right_items': [{'id': 'it_paste', 'label': 'Toothpaste 🧴', 'visual_cue': 'toothpaste'}, {'id': 'it_key', 'label': 'Key 🔑', 'visual_cue': 'key'}, {'id': 'it_sock', 'label': 'Sock 🧦', 'visual_cue': 'sock'}], 'pairs': [{'left_id': 'it_brush', 'right_id': 'it_paste'}, {'left_id': 'it_lock', 'right_id': 'it_key'}, {'left_id': 'it_shoe', 'right_id': 'it_sock'}]},
            correct_answer={'pairs': [{'left_id': 'it_brush', 'right_id': 'it_paste'}, {'left_id': 'it_lock', 'right_id': 'it_key'}, {'left_id': 'it_shoe', 'right_id': 'it_sock'}]},
            explanation={'en': 'Terrific matching! Brush goes with paste, lock with key, shoe with sock.', 'ar': 'مطابقة رائعة! الفرشاة مع المعجون، القفل مع المفتاح، الحذاء مع الجورب.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.sort.mc.belong_with_lock',
            objective_key='obj.life.match_objects_belong_together',
            subject_code='everyday',
            unit_code='unit.life.sorting_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which item belongs with a lock 🔒 to open it?', 'ar': 'أي عنصر يستخدم مع القفل 🔒 لفتحه؟'},
            content_payload={'question': 'Which item belongs with a lock 🔒 to open it?', 'options': [{'id': 'ans_key', 'text': 'Key 🔑', 'visual_cue': 'key', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_banana', 'text': 'Banana 🍌', 'visual_cue': 'banana', 'is_correct': False, 'distractor_rationale': 'A banana is food, it does not open locks'}], 'correct_answer_id': 'ans_key', 'explanation': 'Correct! A key belongs with a lock.'},
            correct_answer={'correct_answer_id': 'ans_key'},
            explanation={'en': 'Correct! A key belongs with a lock.', 'ar': 'صحيح! المفتاح يستخدم مع القفل.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.sort.vis.shoes_socks',
            objective_key='obj.life.match_objects_belong_together',
            subject_code='everyday',
            unit_code='unit.life.sorting_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the pair of socks 🧦 that belongs with shoes.', 'ar': 'حدد زوج الجوارب 🧦 الذي يرتدى مع الحذاء.'},
            content_payload={'prompt': 'Spot the pair of socks 🧦 that belongs with shoes.', 'scene_description': 'A closet shelf with sunglasses, socks, and a paintbrush.', 'elements': [{'id': 'cl_glasses', 'label': 'Sunglasses 🕶️', 'category': 'accessory', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'cl_socks', 'label': 'Pair of Socks 🧦', 'category': 'clothing', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'cl_brush', 'label': 'Paintbrush 🖌️', 'category': 'tool', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'cl_socks', 'feedback_clue': 'Look in the center for the warm socks that go inside shoes.'},
            correct_answer={'target_id': 'cl_socks'},
            explanation={'en': 'Super observation! Socks belong with shoes.', 'ar': 'ملاحظة ممتازة! الجوارب ترتدى مع الأحذية.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.sort.drag.pair_kitchen_study',
            objective_key='obj.life.match_objects_belong_together',
            subject_code='everyday',
            unit_code='unit.life.sorting_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort items into 'Eating Utensils' and 'Writing Supplies'.", 'ar': "صنف العناصر إلى 'أدوات تناول الطعام' و 'أدوات الكتابة'."},
            content_payload={'prompt': "Sort items into 'Eating Utensils' and 'Writing Supplies'.", 'items': [{'id': 'ut_fork', 'label': 'Fork 🍴', 'visual_cue': 'fork'}, {'id': 'ut_spoon', 'label': 'Spoon 🥄', 'visual_cue': 'spoon'}, {'id': 'wr_pencil', 'label': 'Pencil ✏️', 'visual_cue': 'pencil'}, {'id': 'wr_eraser', 'label': 'Eraser 🧼', 'visual_cue': 'eraser'}], 'zones': [{'id': 'z_eating', 'label': 'Eating Utensils', 'capacity': 3}, {'id': 'z_writing', 'label': 'Writing Supplies', 'capacity': 3}], 'correct_mapping': {'ut_fork': 'z_eating', 'ut_spoon': 'z_eating', 'wr_pencil': 'z_writing', 'wr_eraser': 'z_writing'}},
            correct_answer={'correct_mapping': {'ut_fork': 'z_eating', 'ut_spoon': 'z_eating', 'wr_pencil': 'z_writing', 'wr_eraser': 'z_writing'}},
            explanation={'en': 'Great functional pairing!', 'ar': 'مطابقة وظيفية رائعة!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.sort.mc.odd_toy_car',
            objective_key='obj.life.identify_does_not_belong',
            subject_code='everyday',
            unit_code='unit.life.sorting_classification',
            difficulty_level=3,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which item does NOT belong: Apple 🍎, Banana 🍌, Toy Car 🚗?', 'ar': 'أي عنصر لا ينتمي للمجموعة: تفاحة 🍎، موزة 🍌، سيارة لعبة 🚗؟'},
            content_payload={'question': 'Which item does NOT belong: Apple 🍎, Banana 🍌, Toy Car 🚗?', 'options': [{'id': 'ans_car', 'text': 'Toy Car 🚗 (Not a fruit)', 'visual_cue': 'car', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_apple', 'text': 'Apple 🍎', 'visual_cue': 'apple', 'is_correct': False, 'distractor_rationale': 'Apple is a fruit'}, {'id': 'ans_banana', 'text': 'Banana 🍌', 'visual_cue': 'banana', 'is_correct': False, 'distractor_rationale': 'Banana is a fruit'}], 'correct_answer_id': 'ans_car', 'explanation': 'Correct! A toy car is a toy, while apple and banana are fruits.'},
            correct_answer={'correct_answer_id': 'ans_car'},
            explanation={'en': 'Correct! A toy car is a toy, while apple and banana are fruits.', 'ar': 'صحيح! سيارة اللعبة لعبة، بينما التفاح والموز فواكه.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.sort.vis.odd_swimsuit',
            objective_key='obj.life.identify_does_not_belong',
            subject_code='everyday',
            unit_code='unit.life.sorting_classification',
            difficulty_level=3,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Find the item that does NOT belong on the winter coat rack: Swimsuit 🩱.', 'ar': 'حدد العنصر الذي لا ينتمي لعلاقة معاطف الشتاء: ملابس السباحة 🩱.'},
            content_payload={'prompt': 'Find the item that does NOT belong on the winter coat rack: Swimsuit 🩱.', 'scene_description': 'A winter entryway rack with a heavy coat, a swimsuit, and a warm scarf.', 'elements': [{'id': 'cl_coat', 'label': 'Heavy Winter Coat 🧥', 'category': 'winter', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'cl_swim', 'label': 'Summer Swimsuit 🩱', 'category': 'summer', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'cl_scarf', 'label': 'Warm Wool Scarf 🧣', 'category': 'winter', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'cl_swim', 'feedback_clue': 'Look in the center for the summer beach wear among winter gear.'},
            correct_answer={'target_id': 'cl_swim'},
            explanation={'en': 'Terrific! A swimsuit is for summer, not cold winter.', 'ar': 'رائع! ملابس السباحة للصيف وليست للشتاء البارد.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.sort.mc.odd_pillow',
            objective_key='obj.life.identify_does_not_belong',
            subject_code='everyday',
            unit_code='unit.life.sorting_classification',
            difficulty_level=3,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which item does NOT belong with school supplies: Pencil ✏️, Notebook 📓, Pillow 🛏️?', 'ar': 'أي عنصر لا ينتمي لأدوات المدرسة: قلم ✏️، دفتر 📓، وسادة 🛏️؟'},
            content_payload={'question': 'Which item does NOT belong with school supplies: Pencil ✏️, Notebook 📓, Pillow 🛏️?', 'options': [{'id': 'ans_pillow', 'text': 'Pillow 🛏️', 'visual_cue': 'pillow', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_pencil', 'text': 'Pencil ✏️', 'visual_cue': 'pencil', 'is_correct': False, 'distractor_rationale': 'Pencil is a school supply'}, {'id': 'ans_notebook', 'text': 'Notebook 📓', 'visual_cue': 'notebook', 'is_correct': False, 'distractor_rationale': 'Notebook is a school supply'}], 'correct_answer_id': 'ans_pillow', 'explanation': 'Super! A pillow belongs in bed, not in a school backpack.'},
            correct_answer={'correct_answer_id': 'ans_pillow'},
            explanation={'en': 'Super! A pillow belongs in bed, not in a school backpack.', 'ar': 'ممتاز! الوسادة مكانها السرير وليست في الحقيبة المدرسية.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.sort.drag.schoolbag_odd',
            objective_key='obj.life.identify_does_not_belong',
            subject_code='everyday',
            unit_code='unit.life.sorting_classification',
            difficulty_level=3,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort items into 'Belongs in Schoolbag' and 'Does Not Belong'.", 'ar': "صنف العناصر إلى 'ينتمي للحقيبة المدرسية' و 'لا ينتمي'."},
            content_payload={'prompt': "Sort items into 'Belongs in Schoolbag' and 'Does Not Belong'.", 'items': [{'id': 'bg_ruler', 'label': 'Ruler 📏', 'visual_cue': 'ruler'}, {'id': 'bg_pencil_case', 'label': 'Pencil Case 👝', 'visual_cue': 'pencil case'}, {'id': 'bg_frying_pan', 'label': 'Heavy Frying Pan 🍳', 'visual_cue': 'pan'}, {'id': 'bg_pillow', 'label': 'Bed Pillow 🛏️', 'visual_cue': 'pillow'}], 'zones': [{'id': 'z_schoolbag', 'label': 'Belongs in Schoolbag', 'capacity': 3}, {'id': 'z_not_schoolbag', 'label': 'Does Not Belong', 'capacity': 3}], 'correct_mapping': {'bg_ruler': 'z_schoolbag', 'bg_pencil_case': 'z_schoolbag', 'bg_frying_pan': 'z_not_schoolbag', 'bg_pillow': 'z_not_schoolbag'}},
            correct_answer={'correct_mapping': {'bg_ruler': 'z_schoolbag', 'bg_pencil_case': 'z_schoolbag', 'bg_frying_pan': 'z_not_schoolbag', 'bg_pillow': 'z_not_schoolbag'}},
            explanation={'en': 'Accurate odd-item exclusion!', 'ar': 'استبعاد دقيق للعناصر الشاذة!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.sort.match.odd_reason',
            objective_key='obj.life.identify_does_not_belong',
            subject_code='everyday',
            unit_code='unit.life.sorting_classification',
            difficulty_level=3,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each group to the item that does NOT belong.', 'ar': 'طابق كل مجموعة بالعنصر الذي لا ينتمي إليها.'},
            content_payload={'prompt': 'Match each group to the item that does NOT belong.', 'left_items': [{'id': 'grp_fruits', 'label': 'Apple, Banana, Toy Car', 'visual_cue': 'fruits group'}, {'id': 'grp_animals', 'label': 'Dog, Cat, Basketball', 'visual_cue': 'animals group'}], 'right_items': [{'id': 'odd_car', 'label': 'Toy Car (Vehicle)', 'visual_cue': 'car'}, {'id': 'odd_ball', 'label': 'Basketball (Sports)', 'visual_cue': 'ball'}], 'pairs': [{'left_id': 'grp_fruits', 'right_id': 'odd_car'}, {'left_id': 'grp_animals', 'right_id': 'odd_ball'}]},
            correct_answer={'pairs': [{'left_id': 'grp_fruits', 'right_id': 'odd_car'}, {'left_id': 'grp_animals', 'right_id': 'odd_ball'}]},
            explanation={'en': 'Great odd-one-out categorization!', 'ar': 'تصنيف رائع للعنصر الشاذ!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.safe.mc.spill_water',
            objective_key='obj.life.appropriate_action_everyday',
            subject_code='everyday',
            unit_code='unit.life.everyday_safety',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'You accidentally spill water on the table. What is the appropriate action?', 'ar': 'سكبت الماء بالخطأ على الطاولة. ما هو التصرف المناسب؟'},
            content_payload={'question': 'You accidentally spill water on the table. What is the appropriate action?', 'options': [{'id': 'ans_wipe', 'text': 'Wipe it up calmly with a cloth or paper towel 🧻', 'visual_cue': 'wipe', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_ignore', 'text': 'Leave it and walk away', 'visual_cue': 'walk away', 'is_correct': False, 'distractor_rationale': 'Water can drip or cause someone to slip'}], 'correct_answer_id': 'ans_wipe', 'explanation': 'Correct! We wipe up spills promptly to keep surfaces safe and clean.'},
            correct_answer={'correct_answer_id': 'ans_wipe'},
            explanation={'en': 'Correct! We wipe up spills promptly to keep surfaces safe and clean.', 'ar': 'صحيح! نمسح السوائل المسكوبة فوراً للحفاظ على السلامة والنظافة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.safe.vis.share_toys',
            objective_key='obj.life.appropriate_action_everyday',
            subject_code='everyday',
            unit_code='unit.life.everyday_safety',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the child doing the polite and kind action: sharing blocks 🧱.', 'ar': 'حدد الطفل الذي يقوم بتصرف لطيف ومؤدب: مشاركة المكعبات 🧱.'},
            content_payload={'prompt': 'Spot the child doing the polite and kind action: sharing blocks 🧱.', 'scene_description': 'A playroom with children at different activities.', 'elements': [{'id': 'ch_grab', 'label': 'Child snatching toy roughly', 'category': 'action', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'ch_share', 'label': 'Child smiling and sharing blocks nicely 🧱', 'category': 'action', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'ch_cry', 'label': 'Child sitting alone in corner', 'category': 'action', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'ch_share', 'feedback_clue': 'Look in the center for the child sharing toys nicely with a friend.'},
            correct_answer={'target_id': 'ch_share'},
            explanation={'en': 'Wonderful! Sharing toys is kind and polite.', 'ar': 'رائع! مشاركة الألعاب تصرف لطيف ومهذب.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.safe.match.situations_actions',
            objective_key='obj.life.appropriate_action_everyday',
            subject_code='everyday',
            unit_code='unit.life.everyday_safety',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match everyday situations to the responsible action.', 'ar': 'طابق المواقف اليومية بالتصرف المسؤول.'},
            content_payload={'prompt': 'Match everyday situations to the responsible action.', 'left_items': [{'id': 'sit_dirty_hands', 'label': 'Hands are sticky after snack', 'visual_cue': 'sticky hands'}, {'id': 'sit_trash', 'label': 'Empty juice box in hand', 'visual_cue': 'trash'}], 'right_items': [{'id': 'act_wash_hands', 'label': 'Wash hands with soap and water 🧼', 'visual_cue': 'wash hands'}, {'id': 'act_bin', 'label': 'Place juice box into recycling bin 🗑️', 'visual_cue': 'bin'}], 'pairs': [{'left_id': 'sit_dirty_hands', 'right_id': 'act_wash_hands'}, {'left_id': 'sit_trash', 'right_id': 'act_bin'}]},
            correct_answer={'pairs': [{'left_id': 'sit_dirty_hands', 'right_id': 'act_wash_hands'}, {'left_id': 'sit_trash', 'right_id': 'act_bin'}]},
            explanation={'en': 'Super responsible everyday decision matching!', 'ar': 'مطابقة ممتازة للقرارات اليومية المسؤولة!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.safe.mc.say_thank_you',
            objective_key='obj.life.appropriate_action_everyday',
            subject_code='everyday',
            unit_code='unit.life.everyday_safety',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'A friend shares their crayons with you. What is the polite thing to say?', 'ar': 'شارك صديق ألوانه معك. ما هو القول المهذب؟'},
            content_payload={'question': 'A friend shares their crayons with you. What is the polite thing to say?', 'options': [{'id': 'ans_thanks', 'text': "'Thank you!' with a smile 😊", 'visual_cue': 'thank you', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_nothing', 'text': 'Say nothing and take them', 'visual_cue': 'silent', 'is_correct': False, 'distractor_rationale': 'It is polite to express gratitude'}], 'correct_answer_id': 'ans_thanks', 'explanation': "Spot on! Saying 'Thank you' shows appreciation."},
            correct_answer={'correct_answer_id': 'ans_thanks'},
            explanation={'en': "Spot on! Saying 'Thank you' shows appreciation.", 'ar': "صحيح! قول 'شكراً' يعبر عن التقدير."},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.safe.drag.helpful_unhelpful',
            objective_key='obj.life.appropriate_action_everyday',
            subject_code='everyday',
            unit_code='unit.life.everyday_safety',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort actions into 'Helpful Everyday Action' and 'Unhelpful Action'.", 'ar': "صنف الأفعال إلى 'تصرف يومي مفيد' و 'تصرف غير مفيد'."},
            content_payload={'prompt': "Sort actions into 'Helpful Everyday Action' and 'Unhelpful Action'.", 'items': [{'id': 'act_put_away_coat', 'label': 'Hang coat on hook 🧥', 'visual_cue': 'coat hook'}, {'id': 'act_pick_up_book', 'label': 'Place book back on shelf 📖', 'visual_cue': 'bookshelf'}, {'id': 'act_drop_trash_floor', 'label': 'Drop candy wrapper on floor 🍬', 'visual_cue': 'litter'}, {'id': 'act_slam_door', 'label': 'Slam the door loudly 🚪', 'visual_cue': 'slam'}], 'zones': [{'id': 'z_helpful', 'label': 'Helpful Actions ✅', 'capacity': 3}, {'id': 'z_unhelpful', 'label': 'Unhelpful Actions ❌', 'capacity': 3}], 'correct_mapping': {'act_put_away_coat': 'z_helpful', 'act_pick_up_book': 'z_helpful', 'act_drop_trash_floor': 'z_unhelpful', 'act_slam_door': 'z_unhelpful'}},
            correct_answer={'correct_mapping': {'act_put_away_coat': 'z_helpful', 'act_pick_up_book': 'z_helpful', 'act_drop_trash_floor': 'z_unhelpful', 'act_slam_door': 'z_unhelpful'}},
            explanation={'en': 'Terrific sorting of responsible behavior choices!', 'ar': 'فرز رائع لخيارات السلوك المسؤول!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.safe.mc.sharp_knives',
            objective_key='obj.life.distinguish_safe_vs_unsafe',
            subject_code='everyday',
            unit_code='unit.life.everyday_safety',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Is it safe for children to play with sharp kitchen knives?', 'ar': 'هل من الآمن للأطفال اللعب بسكاكين المطبخ الحادة؟'},
            content_payload={'question': 'Is it safe for children to play with sharp kitchen knives?', 'options': [{'id': 'ans_unsafe', 'text': 'No, sharp knives are dangerous and unsafe ⚠️', 'visual_cue': '⚠️', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_safe', 'text': 'Yes, knives are fun toys', 'visual_cue': '❌', 'is_correct': False, 'distractor_rationale': 'Knives can cause severe cuts'}], 'correct_answer_id': 'ans_unsafe', 'explanation': 'Correct! Sharp knives are tools for adults, not toys.'},
            correct_answer={'correct_answer_id': 'ans_unsafe'},
            explanation={'en': 'Correct! Sharp knives are tools for adults, not toys.', 'ar': 'صحيح! السكاكين الحادة أدوات للكبار وليست ألعاباً.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.safe.vis.safe_slide',
            objective_key='obj.life.distinguish_safe_vs_unsafe',
            subject_code='everyday',
            unit_code='unit.life.everyday_safety',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the safe choice on the playground: sliding feet first.', 'ar': 'حدد الخيار الآمن في الملعب: التزحلق بالقدمين أولاً.'},
            content_payload={'prompt': 'Spot the safe choice on the playground: sliding feet first.', 'scene_description': 'A park playground with children on the slide.', 'elements': [{'id': 'sl_head', 'label': 'Sliding down head-first backwards', 'category': 'behavior', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'sl_feet', 'label': 'Sitting upright and sliding feet-first ✅', 'category': 'behavior', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'sl_stand', 'label': 'Standing up on top of the slide', 'category': 'behavior', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'sl_feet', 'feedback_clue': 'Look for the child sitting safely and sliding down feet first.'},
            correct_answer={'target_id': 'sl_feet'},
            explanation={'en': 'Super safety awareness! Sliding feet first prevents injury.', 'ar': 'وعي ممتاز بالسلامة! التزحلق بالقدمين أولاً يمنع الإصابات.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.safe.match.safe_unsafe_pairs',
            objective_key='obj.life.distinguish_safe_vs_unsafe',
            subject_code='everyday',
            unit_code='unit.life.everyday_safety',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match actions to Safe Choice vs Unsafe Choice.', 'ar': 'طابق الأفعال بخيار آمن مقابل خيار غير آمن.'},
            content_payload={'prompt': 'Match actions to Safe Choice vs Unsafe Choice.', 'left_items': [{'id': 'act_helmet', 'label': 'Wearing bicycle helmet 🚴', 'visual_cue': 'helmet'}, {'id': 'act_run_street', 'label': 'Chasing ball into busy road ⚽🚗', 'visual_cue': 'danger'}], 'right_items': [{'id': 'lbl_safe_choice', 'label': 'Safe Choice ✅', 'visual_cue': 'safe'}, {'id': 'lbl_unsafe_choice', 'label': 'Unsafe Choice ⚠️', 'visual_cue': 'unsafe'}], 'pairs': [{'left_id': 'act_helmet', 'right_id': 'lbl_safe_choice'}, {'left_id': 'act_run_street', 'right_id': 'lbl_unsafe_choice'}]},
            correct_answer={'pairs': [{'left_id': 'act_helmet', 'right_id': 'lbl_safe_choice'}, {'left_id': 'act_run_street', 'right_id': 'lbl_unsafe_choice'}]},
            explanation={'en': 'Great safety judgment! Helmets protect us; roads have traffic.', 'ar': 'حكم ممتاز على السلامة! الخوذة تحمينا والطريق خطر.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.safe.drag.home_safety_sort',
            objective_key='obj.life.distinguish_safe_vs_unsafe',
            subject_code='everyday',
            unit_code='unit.life.everyday_safety',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort home practices into 'Safe Practice' and 'Hazardous Practice'.", 'ar': "صنف الممارسات المنزلية إلى 'ممارسة آمنة' و 'ممارسة خطرة'."},
            content_payload={'prompt': "Sort home practices into 'Safe Practice' and 'Hazardous Practice'.", 'items': [{'id': 'hp_handrail', 'label': 'Holding stair handrail 🚶', 'visual_cue': 'handrail'}, {'id': 'hp_clean_spill', 'label': 'Wiping water puddle off tile 🧽', 'visual_cue': 'wipe puddle'}, {'id': 'hp_touch_iron', 'label': 'Touching hot clothes iron ⚠️', 'visual_cue': 'hot iron'}, {'id': 'hp_climb_shelf', 'label': 'Climbing up tall wobbly bookshelf 🪜', 'visual_cue': 'climb'}], 'zones': [{'id': 'z_safe_prac', 'label': 'Safe Practices ✅', 'capacity': 3}, {'id': 'z_hazard_prac', 'label': 'Hazardous Practices ⚠️', 'capacity': 3}], 'correct_mapping': {'hp_handrail': 'z_safe_prac', 'hp_clean_spill': 'z_safe_prac', 'hp_touch_iron': 'z_hazard_prac', 'hp_climb_shelf': 'z_hazard_prac'}},
            correct_answer={'correct_mapping': {'hp_handrail': 'z_safe_prac', 'hp_clean_spill': 'z_safe_prac', 'hp_touch_iron': 'z_hazard_prac', 'hp_climb_shelf': 'z_hazard_prac'}},
            explanation={'en': 'Awesome discrimination of safe vs hazardous practices!', 'ar': 'تمييز رائع للممارسات الآمنة والخطرة!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.safe.mc.curb_action',
            objective_key='obj.life.before_crossing_road',
            subject_code='everyday',
            unit_code='unit.life.everyday_safety',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'What should you do before stepping onto a road?', 'ar': 'ماذا يجب أن تفعل قبل أن تخطو على الطريق؟'},
            content_payload={'question': 'What should you do before stepping onto a road?', 'options': [{'id': 'ans_stop_look', 'text': 'Stop at the curb, look left and right, and listen 🛑👀', 'visual_cue': 'stop look listen', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_run_across', 'text': 'Run across as fast as you can without looking', 'visual_cue': 'run', 'is_correct': False, 'distractor_rationale': 'Never cross without looking for cars'}], 'correct_answer_id': 'ans_stop_look', 'explanation': 'Correct! Always stop, look both ways, and listen for traffic.'},
            correct_answer={'correct_answer_id': 'ans_stop_look'},
            explanation={'en': 'Correct! Always stop, look both ways, and listen for traffic.', 'ar': 'صحيح! توقف دائماً، وانظر في الاتجاهين، واستمع لحركة المرور.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.safe.order.cross_steps',
            objective_key='obj.life.before_crossing_road',
            subject_code='everyday',
            unit_code='unit.life.everyday_safety',
            difficulty_level=2,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Sequence the road crossing routine in order.', 'ar': 'رتب خطوات عبور الطريق بالتسلسل.'},
            content_payload={'prompt': 'Sequence the road crossing routine in order.', 'items': [{'id': 'cs_look', 'label': 'Look left, right, and left again 👀', 'visual_cue': 'look'}, {'id': 'cs_stop', 'label': 'Stop at the curb safely 🛑', 'visual_cue': 'stop'}, {'id': 'cs_walk', 'label': 'Walk calmly holding adult hand 🚶', 'visual_cue': 'walk'}], 'correct_sequence': ['cs_stop', 'cs_look', 'cs_walk'], 'direction': 'chronological'},
            correct_answer={'correct_sequence': ['cs_stop', 'cs_look', 'cs_walk']},
            explanation={'en': 'Super! Stop first, look second, walk calmly third.', 'ar': 'ممتاز! توقف أولاً، انظر ثانياً، واعبر بهدوء ثالثاً.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.safe.vis.green_walk_man',
            objective_key='obj.life.before_crossing_road',
            subject_code='everyday',
            unit_code='unit.life.everyday_safety',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the pedestrian signal that means it is safe to cross: Green Walking Figure 🚶\u200d♂️🟢.', 'ar': 'حدد إشارة المشاة التي تعني أن العبور آمن: علامة المشي الخضراء 🚶\u200d♂️🟢.'},
            content_payload={'prompt': 'Spot the pedestrian signal that means it is safe to cross: Green Walking Figure 🚶\u200d♂️🟢.', 'scene_description': 'A pedestrian street crossing with traffic signals.', 'elements': [{'id': 'sig_red_hand', 'label': "Red Hand Signal ✋🔴 (Don't Walk)", 'category': 'signal', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'sig_green_walk', 'label': 'Green Walking Figure 🚶\u200d♂️🟢 (Safe to Cross)', 'category': 'signal', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'sig_yellow_light', 'label': 'Yellow Traffic Light 🟡', 'category': 'signal', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'sig_green_walk', 'feedback_clue': 'Look in the center for the bright green walking silhouette.'},
            correct_answer={'target_id': 'sig_green_walk'},
            explanation={'en': 'Terrific observation! Green walk figure signals it is safe.', 'ar': 'ملاحظة رائعة! شكل المشي الأخضر يشير إلى أمان العبور.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.safe.match.traffic_signals',
            objective_key='obj.life.before_crossing_road',
            subject_code='everyday',
            unit_code='unit.life.everyday_safety',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match pedestrian signals to their safe actions.', 'ar': 'طابق إشارات المشاة بتصرفات الأمان الخاصة بها.'},
            content_payload={'prompt': 'Match pedestrian signals to their safe actions.', 'left_items': [{'id': 's_red_hand', 'label': 'Red Hand Signal ✋🔴', 'visual_cue': 'red hand'}, {'id': 's_green_figure', 'label': 'Green Walking Figure 🚶\u200d♂️🟢', 'visual_cue': 'green walk'}], 'right_items': [{'id': 'act_wait_curb', 'label': 'Wait on the sidewalk curb 🛑', 'visual_cue': 'wait'}, {'id': 'act_walk_cross', 'label': 'Cross calmly looking both ways 🚶', 'visual_cue': 'cross'}], 'pairs': [{'left_id': 's_red_hand', 'right_id': 'act_wait_curb'}, {'left_id': 's_green_figure', 'right_id': 'act_walk_cross'}]},
            correct_answer={'pairs': [{'left_id': 's_red_hand', 'right_id': 'act_wait_curb'}, {'left_id': 's_green_figure', 'right_id': 'act_walk_cross'}]},
            explanation={'en': 'Great road safety matching!', 'ar': 'مطابقة ممتازة لقواعد السلامة المرورية!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.safe.mc.hot_stove_action',
            objective_key='obj.life.safe_household_behavior',
            subject_code='everyday',
            unit_code='unit.life.everyday_safety',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'What should you do when the kitchen stove is turned on and hot?', 'ar': 'ماذا يجب أن تفعل عندما يكون موقد المطبخ مشتعلاً وساخناً؟'},
            content_payload={'question': 'What should you do when the kitchen stove is turned on and hot?', 'options': [{'id': 'ans_stay_back', 'text': 'Stay back and do not touch hot surfaces ⚠️', 'visual_cue': 'stay back', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_touch_pot', 'text': 'Touch the hot metal pot to feel it', 'visual_cue': 'touch', 'is_correct': False, 'distractor_rationale': 'Hot surfaces cause painful burns'}], 'correct_answer_id': 'ans_stay_back', 'explanation': 'Correct! Always keep a safe distance from hot stoves and ovens.'},
            correct_answer={'correct_answer_id': 'ans_stay_back'},
            explanation={'en': 'Correct! Always keep a safe distance from hot stoves and ovens.', 'ar': 'صحيح! حافظ دائماً على مسافة آمنة من المواقد الساخنة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.safe.vis.holding_handrail',
            objective_key='obj.life.safe_household_behavior',
            subject_code='everyday',
            unit_code='unit.life.everyday_safety',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the child holding the handrail while walking down the stairs.', 'ar': 'حدد الطفل الذي يمسك بالدرابزين أثناء النزول على الدرج.'},
            content_payload={'prompt': 'Spot the child holding the handrail while walking down the stairs.', 'scene_description': 'A staircase scene with safety features.', 'elements': [{'id': 'st_running', 'label': 'Running fast down steps', 'category': 'action', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'st_handrail', 'label': 'Walking carefully holding handrail 🚶', 'category': 'action', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'st_slide_rail', 'label': 'Sliding down banister', 'category': 'action', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'st_handrail', 'feedback_clue': 'Look for the child firmly holding the handrail on the stairs.'},
            correct_answer={'target_id': 'st_handrail'},
            explanation={'en': 'Super safety habit! Handrails prevent stair falls.', 'ar': 'عادة أمان ممتازة! الدرابزين يمنع السقوط على الدرج.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.safe.match.home_hazards',
            objective_key='obj.life.safe_household_behavior',
            subject_code='everyday',
            unit_code='unit.life.everyday_safety',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match household situations to the safe behavior.', 'ar': 'طابق المواقف المنزلية بالسلوك الآمن.'},
            content_payload={'prompt': 'Match household situations to the safe behavior.', 'left_items': [{'id': 'hz_wet_floor', 'label': 'Wet kitchen floor tile 💧', 'visual_cue': 'wet floor'}, {'id': 'hz_hot_soup', 'label': 'Bowl of steaming hot soup 🥣', 'visual_cue': 'hot soup'}], 'right_items': [{'id': 'bh_walk_slow', 'label': 'Walk slowly and carefully 🚶', 'visual_cue': 'walk slow'}, {'id': 'bh_blow_cool', 'label': 'Wait and blow gently to cool before eating 🌬️', 'visual_cue': 'cool soup'}], 'pairs': [{'left_id': 'hz_wet_floor', 'right_id': 'bh_walk_slow'}, {'left_id': 'hz_hot_soup', 'right_id': 'bh_blow_cool'}]},
            correct_answer={'pairs': [{'left_id': 'hz_wet_floor', 'right_id': 'bh_walk_slow'}, {'left_id': 'hz_hot_soup', 'right_id': 'bh_blow_cool'}]},
            explanation={'en': 'Terrific hazard safety matching!', 'ar': 'مطابقة ممتازة للأمان من المخاطر!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.safe.drag.sort_home_safety',
            objective_key='obj.life.safe_household_behavior',
            subject_code='everyday',
            unit_code='unit.life.everyday_safety',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort choices into 'Safe at Home' and 'Danger at Home'.", 'ar': "صنف الخيارات إلى 'آمن في المنزل' و 'خطر في المنزل'."},
            content_payload={'prompt': "Sort choices into 'Safe at Home' and 'Danger at Home'.", 'items': [{'id': 's_toys_away', 'label': 'Put toys in toy bin so no one trips 🧸', 'visual_cue': 'toys away'}, {'id': 's_dry_hands_plug', 'label': 'Dry hands completely before touching switches 🔌', 'visual_cue': 'dry hands'}, {'id': 'd_play_matches', 'label': 'Playing with fire matches 🔥', 'visual_cue': 'matches'}, {'id': 'd_wet_socket', 'label': 'Pouring water near electric socket ⚡', 'visual_cue': 'electric danger'}], 'zones': [{'id': 'z_safe_home', 'label': 'Safe at Home ✅', 'capacity': 3}, {'id': 'z_danger_home', 'label': 'Danger at Home ⚠️', 'capacity': 3}], 'correct_mapping': {'s_toys_away': 'z_safe_home', 's_dry_hands_plug': 'z_safe_home', 'd_play_matches': 'z_danger_home', 'd_wet_socket': 'z_danger_home'}},
            correct_answer={'correct_mapping': {'s_toys_away': 'z_safe_home', 's_dry_hands_plug': 'z_safe_home', 'd_play_matches': 'z_danger_home', 'd_wet_socket': 'z_danger_home'}},
            explanation={'en': 'Brilliant home safety sorting!', 'ar': 'فرز رائع لسلامة المنزل!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.safe.mc.cords_water',
            objective_key='obj.life.safe_household_behavior',
            subject_code='everyday',
            unit_code='unit.life.everyday_safety',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Where should electrical cords and appliances stay?', 'ar': 'أين يجب أن تبقى الأسلاك والأجهزة الكهربائية؟'},
            content_payload={'question': 'Where should electrical cords and appliances stay?', 'options': [{'id': 'ans_away_water', 'text': 'Far away from water and bathtubs 🔌💧❌', 'visual_cue': 'safe electricity', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_in_sink', 'text': 'Directly inside the filled water sink', 'visual_cue': 'in sink', 'is_correct': False, 'distractor_rationale': 'Water conducts electricity and causes severe shocks'}], 'correct_answer_id': 'ans_away_water', 'explanation': 'Spot on! Electricity and water must never mix.'},
            correct_answer={'correct_answer_id': 'ans_away_water'},
            explanation={'en': 'Spot on! Electricity and water must never mix.', 'ar': 'صحيح! الكهرباء والماء لا يجتمعان أبداً.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.safe.order.helmet_routine',
            objective_key='obj.life.sequence_safe_routine',
            subject_code='everyday',
            unit_code='unit.life.everyday_safety',
            difficulty_level=3,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Sequence putting on a bicycle helmet safely.', 'ar': 'رتب خطوات ارتداء خوذة الدراجة بأمان.'},
            content_payload={'prompt': 'Sequence putting on a bicycle helmet safely.', 'items': [{'id': 'hl_buckle', 'label': 'Click and fasten the chin buckle 🪢', 'visual_cue': 'buckle'}, {'id': 'hl_on_head', 'label': 'Place helmet level on head ⛑️', 'visual_cue': 'helmet on head'}, {'id': 'hl_check_fit', 'label': 'Check that helmet fits snug and secure 👍', 'visual_cue': 'check fit'}], 'correct_sequence': ['hl_on_head', 'hl_buckle', 'hl_check_fit'], 'direction': 'chronological'},
            correct_answer={'correct_sequence': ['hl_on_head', 'hl_buckle', 'hl_check_fit']},
            explanation={'en': 'Awesome! Helmet on head, buckle chin, check fit.', 'ar': 'رائع! الخوذة على الرأس، إغلاق الإبزيم، التأكد من الثبات.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.safe.order.rain_routine',
            objective_key='obj.life.sequence_safe_routine',
            subject_code='everyday',
            unit_code='unit.life.everyday_safety',
            difficulty_level=3,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Sequence getting dressed for rainy weather.', 'ar': 'رتب خطوات ارتداء ملابس المطر.'},
            content_payload={'prompt': 'Sequence getting dressed for rainy weather.', 'items': [{'id': 'rn_boots', 'label': 'Put on rubber rain boots 👢', 'visual_cue': 'boots'}, {'id': 'rn_coat', 'label': 'Put on hooded raincoat 🧥', 'visual_cue': 'raincoat'}, {'id': 'rn_umbrella', 'label': 'Open umbrella outside ☂️', 'visual_cue': 'umbrella'}], 'correct_sequence': ['rn_coat', 'rn_boots', 'rn_umbrella'], 'direction': 'chronological'},
            correct_answer={'correct_sequence': ['rn_coat', 'rn_boots', 'rn_umbrella']},
            explanation={'en': 'Super rainy day preparation sequence!', 'ar': 'تسلسل تحضير رائع ليوم ماطر!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.safe.mc.soap_scrub_step',
            objective_key='obj.life.sequence_safe_routine',
            subject_code='everyday',
            unit_code='unit.life.everyday_safety',
            difficulty_level=3,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'When washing hands safely, what do you do right after applying soap?', 'ar': 'عند غسل اليدين بأمان، ماذا تفعل مباشرة بعد وضع الصابون؟'},
            content_payload={'question': 'When washing hands safely, what do you do right after applying soap?', 'options': [{'id': 'ans_scrub_bubbles', 'text': 'Rub hands together for 20 seconds making bubbles 🧼🫧', 'visual_cue': 'bubbles', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_dry_immediately', 'text': 'Dry hands on shirt immediately without rubbing', 'visual_cue': 'dry', 'is_correct': False, 'distractor_rationale': 'Must scrub to remove germs'}], 'correct_answer_id': 'ans_scrub_bubbles', 'explanation': 'Correct! Rubbing with soap for 20 seconds cleans off germs.'},
            correct_answer={'correct_answer_id': 'ans_scrub_bubbles'},
            explanation={'en': 'Correct! Rubbing with soap for 20 seconds cleans off germs.', 'ar': 'صحيح! فرك اليدين بالصابون لمدة ٢٠ ثانية ينظف الجراثيم.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='life.safe.drag.prep_execution_steps',
            objective_key='obj.life.sequence_safe_routine',
            subject_code='everyday',
            unit_code='unit.life.everyday_safety',
            difficulty_level=3,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort steps into 'Preparation' and 'Safe Execution'.", 'ar': "صنف الخطوات إلى 'التحضير' و 'التنفيذ الآمن'."},
            content_payload={'prompt': "Sort steps into 'Preparation' and 'Safe Execution'.", 'items': [{'id': 'pr_check_laces', 'label': 'Tie shoelaces tightly 👟', 'visual_cue': 'shoelaces'}, {'id': 'pr_put_pads', 'label': 'Strap on knee and elbow pads 🛡️', 'visual_cue': 'pads'}, {'id': 'ex_ride_path', 'label': 'Ride bicycle on safe bike path 🚴', 'visual_cue': 'bike path'}, {'id': 'ex_watch_pedestrians', 'label': 'Watch out for pedestrians 🚶', 'visual_cue': 'watch'}], 'zones': [{'id': 'z_prep', 'label': 'Safety Preparation', 'capacity': 3}, {'id': 'z_exec', 'label': 'Safe Execution', 'capacity': 3}], 'correct_mapping': {'pr_check_laces': 'z_prep', 'pr_put_pads': 'z_prep', 'ex_ride_path': 'z_exec', 'ex_watch_pedestrians': 'z_exec'}},
            correct_answer={'correct_mapping': {'pr_check_laces': 'z_prep', 'pr_put_pads': 'z_prep', 'ex_ride_path': 'z_exec', 'ex_watch_pedestrians': 'z_exec'}},
            explanation={'en': 'Terrific sorting of safety preparation and execution!', 'ar': 'فرز رائع لإعداد وتنفيذ السلامة!'},
            hints=[],
            metadata_info={},
        )
    )
    return items
