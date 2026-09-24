"""
Eduvia — Expanded Early Literacy Content Bank Items

Provides authoritative educational items for all 20 early literacy objectives,
ensuring complete coverage across all 5 activity modalities.
"""
from __future__ import annotations

from app.activities.schemas import ActivityType
from app.content.definitions import ContentItemDef

def get_expanded_literacy_items() -> list[ContentItemDef]:
    items: list[ContentItemDef] = []
    items.append(
        ContentItemDef(
            content_key='lit.letter.mc_upper_b',
            objective_key='obj.lit.identify_uppercase',
            subject_code='literacy',
            unit_code='unit.lit.letter_recognition',
            difficulty_level=1,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which letter is the uppercase B?', 'ar': 'أي حرف هو حرف B الكبير؟'},
            content_payload={'question': 'Which letter is the uppercase B?', 'options': [{'id': 'opt_B', 'text': 'B', 'visual_cue': '🅱️', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_D', 'text': 'D', 'visual_cue': 'D', 'is_correct': False, 'distractor_rationale': 'Single loop on right'}, {'id': 'opt_P', 'text': 'P', 'visual_cue': 'P', 'is_correct': False, 'distractor_rationale': 'Top loop only'}], 'correct_answer_id': 'opt_B', 'explanation': 'Correct! This is the uppercase letter B.'},
            correct_answer={'correct_answer_id': 'opt_B'},
            explanation={'en': 'Correct! This is the uppercase letter B.', 'ar': 'صحيح! هذا هو حرف B الكبير.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.letter.vis_upper_m',
            objective_key='obj.lit.identify_uppercase',
            subject_code='literacy',
            unit_code='unit.lit.letter_recognition',
            difficulty_level=1,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Find the uppercase letter M on the alphabet banner.', 'ar': 'ابحث عن حرف M الكبير على شريط الحروف.'},
            content_payload={'prompt': 'Find the uppercase letter M on the alphabet banner.', 'scene_description': 'A colorful alphabet pennant banner across the classroom.', 'elements': [{'id': 'let_c', 'label': 'Letter C', 'category': 'letter', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'let_m', 'label': 'Letter M', 'category': 'letter', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'let_s', 'label': 'Letter S', 'category': 'letter', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'let_m', 'feedback_clue': 'Look in the center for the letter with two peaks like mountains.'},
            correct_answer={'target_id': 'let_m'},
            explanation={'en': 'Wonderful! That is uppercase letter M.', 'ar': 'رائع! هذا هو حرف M الكبير.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.letter.match_upper_icons',
            objective_key='obj.lit.identify_uppercase',
            subject_code='literacy',
            unit_code='unit.lit.letter_recognition',
            difficulty_level=1,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each uppercase letter to its phonic picture.', 'ar': 'طابق كل حرف كبير بصورته الصوتية.'},
            content_payload={'prompt': 'Match each uppercase letter to its phonic picture.', 'left_items': [{'id': 'let_A', 'label': 'Letter A', 'visual_cue': '🅰️'}, {'id': 'let_B', 'label': 'Letter B', 'visual_cue': '🅱️'}, {'id': 'let_C', 'label': 'Letter C', 'visual_cue': 'C'}], 'right_items': [{'id': 'pic_apple', 'label': 'Apple 🍎', 'visual_cue': '🍎'}, {'id': 'pic_ball', 'label': 'Ball ⚽', 'visual_cue': '⚽'}, {'id': 'pic_cat', 'label': 'Cat 🐱', 'visual_cue': '🐱'}], 'pairs': [{'left_id': 'let_A', 'right_id': 'pic_apple'}, {'left_id': 'let_B', 'right_id': 'pic_ball'}, {'left_id': 'let_C', 'right_id': 'pic_cat'}]},
            correct_answer={'pairs': [{'left_id': 'let_A', 'right_id': 'pic_apple'}, {'left_id': 'let_B', 'right_id': 'pic_ball'}, {'left_id': 'let_C', 'right_id': 'pic_cat'}]},
            explanation={'en': 'Great matching! A for Apple, B for Ball, C for Cat.', 'ar': 'مطابقة رائعة! A للتفاحة، B للكرة، C للقطة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.letter.drag.sort_upper_nums',
            objective_key='obj.lit.identify_uppercase',
            subject_code='literacy',
            unit_code='unit.lit.letter_recognition',
            difficulty_level=1,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort cards into 'Uppercase Letters' and 'Numbers'.", 'ar': "صنف البطاقات إلى 'حروف كبيرة' و 'أرقام'."},
            content_payload={'prompt': "Sort cards into 'Uppercase Letters' and 'Numbers'.", 'items': [{'id': 'card_A', 'label': 'Letter A', 'visual_cue': 'A'}, {'id': 'card_K', 'label': 'Letter K', 'visual_cue': 'K'}, {'id': 'card_3', 'label': 'Number 3', 'visual_cue': '3️⃣'}, {'id': 'card_7', 'label': 'Number 7', 'visual_cue': '7️⃣'}], 'zones': [{'id': 'z_letters', 'label': 'Uppercase Letters', 'capacity': 3}, {'id': 'z_numbers', 'label': 'Numbers', 'capacity': 3}], 'correct_mapping': {'card_A': 'z_letters', 'card_K': 'z_letters', 'card_3': 'z_numbers', 'card_7': 'z_numbers'}},
            correct_answer={'correct_mapping': {'card_A': 'z_letters', 'card_K': 'z_letters', 'card_3': 'z_numbers', 'card_7': 'z_numbers'}},
            explanation={'en': 'Terrific sorting of letters and numbers!', 'ar': 'فرز رائع للحروف والأرقام!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.letter.mc_lower_a',
            objective_key='obj.lit.identify_lowercase',
            subject_code='literacy',
            unit_code='unit.lit.letter_recognition',
            difficulty_level=1,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which letter is the lowercase a?', 'ar': 'أي حرف هو حرف a الصغير؟'},
            content_payload={'question': 'Which letter is the lowercase a?', 'options': [{'id': 'ans_a', 'text': 'a', 'visual_cue': 'a', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_o', 'text': 'o', 'visual_cue': 'o', 'is_correct': False, 'distractor_rationale': 'Round circle without tail'}, {'id': 'ans_e', 'text': 'e', 'visual_cue': 'e', 'is_correct': False, 'distractor_rationale': 'Horizontal bar with loop'}], 'correct_answer_id': 'ans_a', 'explanation': 'Correct! That is lowercase letter a.'},
            correct_answer={'correct_answer_id': 'ans_a'},
            explanation={'en': 'Correct! That is lowercase letter a.', 'ar': 'صحيح! هذا هو حرف a الصغير.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.letter.mc_lower_m',
            objective_key='obj.lit.identify_lowercase',
            subject_code='literacy',
            unit_code='unit.lit.letter_recognition',
            difficulty_level=1,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which letter is the lowercase m?', 'ar': 'أي حرف هو حرف m الصغير؟'},
            content_payload={'question': 'Which letter is the lowercase m?', 'options': [{'id': 'ans_m', 'text': 'm', 'visual_cue': 'm', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_n', 'text': 'n', 'visual_cue': 'n', 'is_correct': False, 'distractor_rationale': 'Single hump only'}, {'id': 'ans_w', 'text': 'w', 'visual_cue': 'w', 'is_correct': False, 'distractor_rationale': 'Upside-down peaks'}], 'correct_answer_id': 'ans_m', 'explanation': 'Super! Lowercase m has two rounded humps.'},
            correct_answer={'correct_answer_id': 'ans_m'},
            explanation={'en': 'Super! Lowercase m has two rounded humps.', 'ar': 'ممتاز! حرف m الصغير يحتوي على انحناءين.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.letter.vis_lower_t',
            objective_key='obj.lit.identify_lowercase',
            subject_code='literacy',
            unit_code='unit.lit.letter_recognition',
            difficulty_level=1,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Find the lowercase letter t on the blackboard.', 'ar': 'ابحث عن حرف t الصغير على السبورة.'},
            content_payload={'prompt': 'Find the lowercase letter t on the blackboard.', 'scene_description': 'A reading blackboard with several lowercase letters.', 'elements': [{'id': 'let_l', 'label': 'Letter l', 'category': 'letter', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'let_t', 'label': 'Letter t', 'category': 'letter', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'let_f', 'label': 'Letter f', 'category': 'letter', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'let_t', 'feedback_clue': 'Look for the vertical letter with a crossbar.'},
            correct_answer={'target_id': 'let_t'},
            explanation={'en': 'Brilliant! You found lowercase letter t.', 'ar': 'رائع! لقد وجدت حرف t الصغير.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.letter.match_lower_icons',
            objective_key='obj.lit.identify_lowercase',
            subject_code='literacy',
            unit_code='unit.lit.letter_recognition',
            difficulty_level=1,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each lowercase letter to its phonic picture.', 'ar': 'طابق كل حرف صغير بصورته الصوتية.'},
            content_payload={'prompt': 'Match each lowercase letter to its phonic picture.', 'left_items': [{'id': 'l_d', 'label': 'Letter d', 'visual_cue': 'd'}, {'id': 'l_f', 'label': 'Letter f', 'visual_cue': 'f'}], 'right_items': [{'id': 'p_duck', 'label': 'Duck 🦆', 'visual_cue': '🦆'}, {'id': 'p_fish', 'label': 'Fish 🐟', 'visual_cue': '🐟'}], 'pairs': [{'left_id': 'l_d', 'right_id': 'p_duck'}, {'left_id': 'l_f', 'right_id': 'p_fish'}]},
            correct_answer={'pairs': [{'left_id': 'l_d', 'right_id': 'p_duck'}, {'left_id': 'l_f', 'right_id': 'p_fish'}]},
            explanation={'en': 'Great work! d for Duck, f for Fish.', 'ar': 'عمل رائع! d للبطة، f للسمكة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.letter.drag.sort_upper_lower',
            objective_key='obj.lit.identify_lowercase',
            subject_code='literacy',
            unit_code='unit.lit.letter_recognition',
            difficulty_level=1,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort letters into 'Uppercase' and 'Lowercase'.", 'ar': "صنف الحروف إلى 'كبيرة' و 'صغيرة'."},
            content_payload={'prompt': "Sort letters into 'Uppercase' and 'Lowercase'.", 'items': [{'id': 'ch_G', 'label': 'G', 'visual_cue': 'G'}, {'id': 'ch_R', 'label': 'R', 'visual_cue': 'R'}, {'id': 'ch_g', 'label': 'g', 'visual_cue': 'g'}, {'id': 'ch_r', 'label': 'r', 'visual_cue': 'r'}], 'zones': [{'id': 'z_upp', 'label': 'Uppercase Letters', 'capacity': 3}, {'id': 'z_low', 'label': 'Lowercase Letters', 'capacity': 3}], 'correct_mapping': {'ch_G': 'z_upp', 'ch_R': 'z_upp', 'ch_g': 'z_low', 'ch_r': 'z_low'}},
            correct_answer={'correct_mapping': {'ch_G': 'z_upp', 'ch_R': 'z_upp', 'ch_g': 'z_low', 'ch_r': 'z_low'}},
            explanation={'en': 'Accurate sorting of uppercase and lowercase!', 'ar': 'فرز دقيق للحروف الكبيرة والصغيرة!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.letter.mc_match_D',
            objective_key='obj.lit.match_upper_to_lower',
            subject_code='literacy',
            unit_code='unit.lit.letter_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which lowercase letter matches uppercase D?', 'ar': 'أي حرف صغير يطابق حرف D الكبير؟'},
            content_payload={'question': 'Which lowercase letter matches uppercase D?', 'options': [{'id': 'opt_d', 'text': 'd', 'visual_cue': 'd', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_b', 'text': 'b', 'visual_cue': 'b', 'is_correct': False, 'distractor_rationale': 'Loop faces right in b, left in d'}, {'id': 'opt_p', 'text': 'p', 'visual_cue': 'p', 'is_correct': False, 'distractor_rationale': 'Descender letter'}], 'correct_answer_id': 'opt_d', 'explanation': 'Correct! Uppercase D matches lowercase d.'},
            correct_answer={'correct_answer_id': 'opt_d'},
            explanation={'en': 'Correct! Uppercase D matches lowercase d.', 'ar': 'صحيح! حرف D الكبير يطابق حرف d الصغير.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.letter.match_EFG',
            objective_key='obj.lit.match_upper_to_lower',
            subject_code='literacy',
            unit_code='unit.lit.letter_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match uppercase letters to their lowercase partners.', 'ar': 'طابق الحروف الكبيرة بنظيراتها الصغيرة.'},
            content_payload={'prompt': 'Match uppercase letters to their lowercase partners.', 'left_items': [{'id': 'up_E', 'label': 'E', 'visual_cue': 'E'}, {'id': 'up_F', 'label': 'F', 'visual_cue': 'F'}, {'id': 'up_G', 'label': 'G', 'visual_cue': 'G'}], 'right_items': [{'id': 'lo_e', 'label': 'e', 'visual_cue': 'e'}, {'id': 'lo_f', 'label': 'f', 'visual_cue': 'f'}, {'id': 'lo_g', 'label': 'g', 'visual_cue': 'g'}], 'pairs': [{'left_id': 'up_E', 'right_id': 'lo_e'}, {'left_id': 'up_F', 'right_id': 'lo_f'}, {'left_id': 'up_G', 'right_id': 'lo_g'}]},
            correct_answer={'pairs': [{'left_id': 'up_E', 'right_id': 'lo_e'}, {'left_id': 'up_F', 'right_id': 'lo_f'}, {'left_id': 'up_G', 'right_id': 'lo_g'}]},
            explanation={'en': 'Terrific matching! E-e, F-f, G-g.', 'ar': 'مطابقة رائعة! E-e، F-f، G-g.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.letter.vis_find_lower_h',
            objective_key='obj.lit.match_upper_to_lower',
            subject_code='literacy',
            unit_code='unit.lit.letter_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': "Find the lowercase partner 'h' for uppercase 'H'.", 'ar': "ابحث عن الحرف الصغير 'h' المطابق لـ 'H' الكبير."},
            content_payload={'prompt': "Find the lowercase partner 'h' for uppercase 'H'.", 'scene_description': 'A reading chart showing uppercase H followed by options.', 'elements': [{'id': 'c_n', 'label': 'Letter n', 'category': 'letter', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'c_h', 'label': 'Letter h', 'category': 'letter', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'c_b', 'label': 'Letter b', 'category': 'letter', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'c_h', 'feedback_clue': 'Look for the letter with a tall stem and a rounded hump.'},
            correct_answer={'target_id': 'c_h'},
            explanation={'en': 'Super! Lowercase h matches uppercase H.', 'ar': 'ممتاز! حرف h الصغير يطابق حرف H الكبير.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.letter.drag.drop_pairs',
            objective_key='obj.lit.match_upper_to_lower',
            subject_code='literacy',
            unit_code='unit.lit.letter_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': 'Drag lowercase letters into their matching uppercase bins.', 'ar': 'اسحب الحروف الصغيرة إلى صناديق الحروف الكبيرة المطابقة لها.'},
            content_payload={'prompt': 'Drag lowercase letters into their matching uppercase bins.', 'items': [{'id': 'tile_m', 'label': "Tile 'm'", 'visual_cue': 'm'}, {'id': 'tile_t', 'label': "Tile 't'", 'visual_cue': 't'}], 'zones': [{'id': 'bin_M', 'label': "Uppercase Bin 'M'", 'capacity': 2}, {'id': 'bin_T', 'label': "Uppercase Bin 'T'", 'capacity': 2}], 'correct_mapping': {'tile_m': 'bin_M', 'tile_t': 'bin_T'}},
            correct_answer={'correct_mapping': {'tile_m': 'bin_M', 'tile_t': 'bin_T'}},
            explanation={'en': 'Spot on! m belongs with M, t belongs with T.', 'ar': 'صحيح تماماً! m تخص M، و t تخص T.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.letter.mc_find_O',
            objective_key='obj.lit.identify_letter_distractors',
            subject_code='literacy',
            unit_code='unit.lit.letter_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Identify the letter O among the similar letters.', 'ar': 'حدد الحرف O من بين الحروف المتشابهة.'},
            content_payload={'question': 'Identify the letter O among the similar letters.', 'options': [{'id': 'opt_O', 'text': 'O', 'visual_cue': 'O', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_Q', 'text': 'Q', 'visual_cue': 'Q', 'is_correct': False, 'distractor_rationale': 'Has a bottom tail'}, {'id': 'opt_C', 'text': 'C', 'visual_cue': 'C', 'is_correct': False, 'distractor_rationale': 'Open curve'}], 'correct_answer_id': 'opt_O', 'explanation': 'Correct! Letter O is a complete closed circle.'},
            correct_answer={'correct_answer_id': 'opt_O'},
            explanation={'en': 'Correct! Letter O is a complete closed circle.', 'ar': 'صحيح! الحرف O دائرة مغلقة بالكامل.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.letter.vis_find_B',
            objective_key='obj.lit.identify_letter_distractors',
            subject_code='literacy',
            unit_code='unit.lit.letter_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the target letter B among lookalike letters.', 'ar': 'حدد الحرف B المستهدف من بين الحروف المتشابهة.'},
            content_payload={'prompt': 'Spot the target letter B among lookalike letters.', 'scene_description': 'A letter puzzle board displaying P, B, and R.', 'elements': [{'id': 'el_P', 'label': 'Letter P', 'category': 'letter', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'el_B', 'label': 'Letter B', 'category': 'letter', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'el_R', 'label': 'Letter R', 'category': 'letter', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'el_B', 'feedback_clue': 'Look for the letter with two rounded loops on the right.'},
            correct_answer={'target_id': 'el_B'},
            explanation={'en': 'Great eye! You distinguished B from P and R.', 'ar': 'عين ممتازة! لقد ميزت B عن P و R.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.letter.match_twin_distractors',
            objective_key='obj.lit.identify_letter_distractors',
            subject_code='literacy',
            unit_code='unit.lit.letter_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each target letter to its identical twin.', 'ar': 'طابق كل حرف مستهدف بتوأمه المتطابق.'},
            content_payload={'prompt': 'Match each target letter to its identical twin.', 'left_items': [{'id': 't_V', 'label': 'Target: V', 'visual_cue': 'V'}, {'id': 't_W', 'label': 'Target: W', 'visual_cue': 'W'}], 'right_items': [{'id': 'm_V', 'label': 'Match: V', 'visual_cue': 'V'}, {'id': 'm_W', 'label': 'Match: W', 'visual_cue': 'W'}], 'pairs': [{'left_id': 't_V', 'right_id': 'm_V'}, {'left_id': 't_W', 'right_id': 'm_W'}]},
            correct_answer={'pairs': [{'left_id': 't_V', 'right_id': 'm_V'}, {'left_id': 't_W', 'right_id': 'm_W'}]},
            explanation={'en': 'Super matching under visual similarity!', 'ar': 'مطابقة رائعة في ظل التشابه البصري!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.letter.drag.sort_target_S',
            objective_key='obj.lit.identify_letter_distractors',
            subject_code='literacy',
            unit_code='unit.lit.letter_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort letters into 'Target S' and 'Other Distractors'.", 'ar': "صنف الحروف إلى 'الحرف المستهدف S' و 'حروف مشتتة أخرى'."},
            content_payload={'prompt': "Sort letters into 'Target S' and 'Other Distractors'.", 'items': [{'id': 's_1', 'label': 'Letter S', 'visual_cue': 'S'}, {'id': 's_2', 'label': 'Letter S', 'visual_cue': 'S'}, {'id': 'd_Z', 'label': 'Letter Z', 'visual_cue': 'Z'}, {'id': 'd_C', 'label': 'Letter C', 'visual_cue': 'C'}], 'zones': [{'id': 'z_target', 'label': 'Target S', 'capacity': 3}, {'id': 'z_distract', 'label': 'Distractor Letters', 'capacity': 3}], 'correct_mapping': {'s_1': 'z_target', 's_2': 'z_target', 'd_Z': 'z_distract', 'd_C': 'z_distract'}},
            correct_answer={'correct_mapping': {'s_1': 'z_target', 's_2': 'z_target', 'd_Z': 'z_distract', 'd_C': 'z_distract'}},
            explanation={'en': 'Terrific discrimination of the curvy letter S!', 'ar': 'تمييز رائع للحرف المنحني S!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.letter.mc_repeat_bee',
            objective_key='obj.lit.recognize_repeated_letters',
            subject_code='literacy',
            unit_code='unit.lit.letter_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': "In the word 'BEE 🐝', which letter appears twice?", 'ar': "في كلمة 'BEE 🐝'، أي حرف يظهر مرتين؟"},
            content_payload={'question': "In the word 'BEE 🐝', which letter appears twice?", 'options': [{'id': 'ans_E', 'text': 'Letter E', 'visual_cue': 'E', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_B', 'text': 'Letter B', 'visual_cue': 'B', 'is_correct': False, 'distractor_rationale': 'Only appears once'}, {'id': 'ans_T', 'text': 'Letter T', 'visual_cue': 'T', 'is_correct': False, 'distractor_rationale': 'Not in the word'}], 'correct_answer_id': 'ans_E', 'explanation': "Correct! The word BEE has two letter E's."},
            correct_answer={'correct_answer_id': 'ans_E'},
            explanation={'en': "Correct! The word BEE has two letter E's.", 'ar': 'صحيح! كلمة BEE تحتوي على حرفي E.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.letter.mc_repeat_book',
            objective_key='obj.lit.recognize_repeated_letters',
            subject_code='literacy',
            unit_code='unit.lit.letter_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': "In the word 'BOOK 📖', which letter appears twice?", 'ar': "في كلمة 'BOOK 📖'، أي حرف يظهر مرتين؟"},
            content_payload={'question': "In the word 'BOOK 📖', which letter appears twice?", 'options': [{'id': 'ans_O', 'text': 'Letter O', 'visual_cue': 'O', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_B', 'text': 'Letter B', 'visual_cue': 'B', 'is_correct': False, 'distractor_rationale': 'Appears only once'}, {'id': 'ans_K', 'text': 'Letter K', 'visual_cue': 'K', 'is_correct': False, 'distractor_rationale': 'Appears only once'}], 'correct_answer_id': 'ans_O', 'explanation': "Super! The word BOOK has double O's in the middle."},
            correct_answer={'correct_answer_id': 'ans_O'},
            explanation={'en': "Super! The word BOOK has double O's in the middle.", 'ar': 'ممتاز! كلمة BOOK تحتوي على حرفي O في المنتصف.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.letter.vis_repeat_ll',
            objective_key='obj.lit.recognize_repeated_letters',
            subject_code='literacy',
            unit_code='unit.lit.letter_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': "Spot the double repeated letter in the word 'BALL ⚽'.", 'ar': "حدد الحرف المكرر مرتين في كلمة 'BALL ⚽'."},
            content_payload={'prompt': "Spot the double repeated letter in the word 'BALL ⚽'.", 'scene_description': 'A toy building block displaying the letters B, A, L, L.', 'elements': [{'id': 'lt_b', 'label': 'Letter B', 'category': 'letter', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'lt_a', 'label': 'Letter A', 'category': 'letter', 'is_target': False, 'bounding_hint': 'center-left'}, {'id': 'lt_ll', 'label': 'Double L (LL)', 'category': 'letter', 'is_target': True, 'bounding_hint': 'right'}], 'target_id': 'lt_ll', 'feedback_clue': 'Look at the end of the word for the twin letters.'},
            correct_answer={'target_id': 'lt_ll'},
            explanation={'en': 'Awesome observation! Letter L repeats at the end of BALL.', 'ar': 'ملاحظة رائعة! الحرف L يتكرر في نهاية كلمة BALL.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.letter.match_double_letters',
            objective_key='obj.lit.recognize_repeated_letters',
            subject_code='literacy',
            unit_code='unit.lit.letter_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each word to its repeated double letter.', 'ar': 'طابق كل كلمة بحرفها المكرر.'},
            content_payload={'prompt': 'Match each word to its repeated double letter.', 'left_items': [{'id': 'w_moon', 'label': 'MOON 🌙', 'visual_cue': 'MOON'}, {'id': 'w_tree', 'label': 'TREE 🌲', 'visual_cue': 'TREE'}], 'right_items': [{'id': 'rep_oo', 'label': 'Double O (OO)', 'visual_cue': 'OO'}, {'id': 'rep_ee', 'label': 'Double E (EE)', 'visual_cue': 'EE'}], 'pairs': [{'left_id': 'w_moon', 'right_id': 'rep_oo'}, {'left_id': 'w_tree', 'right_id': 'rep_ee'}]},
            correct_answer={'pairs': [{'left_id': 'w_moon', 'right_id': 'rep_oo'}, {'left_id': 'w_tree', 'right_id': 'rep_ee'}]},
            explanation={'en': 'Great matching of repeated vowel patterns!', 'ar': 'مطابقة رائعة لأنماط الحروف المكررة!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.letter.drag.sort_repeats',
            objective_key='obj.lit.recognize_repeated_letters',
            subject_code='literacy',
            unit_code='unit.lit.letter_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort words into 'Has Repeated Letters' and 'No Repeated Letters'.", 'ar': "صنف الكلمات إلى 'تحتوي على حروف مكررة' و 'بدون حروف مكررة'."},
            content_payload={'prompt': "Sort words into 'Has Repeated Letters' and 'No Repeated Letters'.", 'items': [{'id': 'w_bee', 'label': 'BEE', 'visual_cue': 'BEE'}, {'id': 'w_zoo', 'label': 'ZOO', 'visual_cue': 'ZOO'}, {'id': 'w_cat', 'label': 'CAT', 'visual_cue': 'CAT'}, {'id': 'w_dog', 'label': 'DOG', 'visual_cue': 'DOG'}], 'zones': [{'id': 'z_rep', 'label': 'Repeated Letters', 'capacity': 3}, {'id': 'z_norep', 'label': 'No Repeated Letters', 'capacity': 3}], 'correct_mapping': {'w_bee': 'z_rep', 'w_zoo': 'z_rep', 'w_cat': 'z_norep', 'w_dog': 'z_norep'}},
            correct_answer={'correct_mapping': {'w_bee': 'z_rep', 'w_zoo': 'z_rep', 'w_cat': 'z_norep', 'w_dog': 'z_norep'}},
            explanation={'en': 'Terrific identification of repeated letters!', 'ar': 'تمييز رائع للحروف المكررة!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.letter.drag.group_AB',
            objective_key='obj.lit.group_identical_letters',
            subject_code='literacy',
            unit_code='unit.lit.letter_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Group identical letters: place all 'A's in Bin A and all 'B's in Bin B.", 'ar': "جمع الحروف المتطابقة: ضع جميع حروف 'A' في الصندوق A وجميع حروف 'B' في الصندوق B."},
            content_payload={'prompt': "Group identical letters: place all 'A's in Bin A and all 'B's in Bin B.", 'items': [{'id': 'l_a1', 'label': 'A', 'visual_cue': 'A'}, {'id': 'l_a2', 'label': 'A', 'visual_cue': 'A'}, {'id': 'l_b1', 'label': 'B', 'visual_cue': 'B'}, {'id': 'l_b2', 'label': 'B', 'visual_cue': 'B'}], 'zones': [{'id': 'bin_A', 'label': 'Bin for Letter A', 'capacity': 3}, {'id': 'bin_B', 'label': 'Bin for Letter B', 'capacity': 3}], 'correct_mapping': {'l_a1': 'bin_A', 'l_a2': 'bin_A', 'l_b1': 'bin_B', 'l_b2': 'bin_B'}},
            correct_answer={'correct_mapping': {'l_a1': 'bin_A', 'l_a2': 'bin_A', 'l_b1': 'bin_B', 'l_b2': 'bin_B'}},
            explanation={'en': 'Super grouping of identical letters!', 'ar': 'تجميع رائع للحروف المتطابقة!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.letter.match_identical_pairs',
            objective_key='obj.lit.group_identical_letters',
            subject_code='literacy',
            unit_code='unit.lit.letter_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match identical letters together.', 'ar': 'طابق الحروف المتطابقة معاً.'},
            content_payload={'prompt': 'Match identical letters together.', 'left_items': [{'id': 'src_K', 'label': 'Letter K', 'visual_cue': 'K'}, {'id': 'src_R', 'label': 'Letter R', 'visual_cue': 'R'}], 'right_items': [{'id': 'dst_K', 'label': 'Letter K', 'visual_cue': 'K'}, {'id': 'dst_R', 'label': 'Letter R', 'visual_cue': 'R'}], 'pairs': [{'left_id': 'src_K', 'right_id': 'dst_K'}, {'left_id': 'src_R', 'right_id': 'dst_R'}]},
            correct_answer={'pairs': [{'left_id': 'src_K', 'right_id': 'dst_K'}, {'left_id': 'src_R', 'right_id': 'dst_R'}]},
            explanation={'en': 'Great identical letter pairs!', 'ar': 'أزواج حروف متطابقة رائعة!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.letter.vis_find_e_twins',
            objective_key='obj.lit.group_identical_letters',
            subject_code='literacy',
            unit_code='unit.lit.letter_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': "Spot the target group showing identical green letter 'E's.", 'ar': "حدد المجموعة المستهدفة التي تظهر حروف 'E' خضراء متطابقة."},
            content_payload={'prompt': "Spot the target group showing identical green letter 'E's.", 'scene_description': 'A learning app screen with three letter clusters.', 'elements': [{'id': 'cls_mix', 'label': 'Mixed (A, B, C)', 'category': 'cluster', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'cls_e', 'label': "All Letter E's (E, E, E)", 'category': 'cluster', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'cls_num', 'label': 'Numbers (1, 2, 3)', 'category': 'cluster', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'cls_e', 'feedback_clue': 'Look for the box that contains only the letter E.'},
            correct_answer={'target_id': 'cls_e'},
            explanation={'en': "Wonderful! All letters in that group are identical E's.", 'ar': 'رائع! جميع الحروف في تلك المجموعة هي حروف E متطابقة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.letter.mc_only_T',
            objective_key='obj.lit.group_identical_letters',
            subject_code='literacy',
            unit_code='unit.lit.letter_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': "Which box contains ONLY identical letter T's?", 'ar': 'أي صندوق يحتوي على حروف T متطابقة فقط؟'},
            content_payload={'question': "Which box contains ONLY identical letter T's?", 'options': [{'id': 'box_ttt', 'text': 'T, T, T', 'visual_cue': 'T T T', 'is_correct': True, 'distractor_rationale': None}, {'id': 'box_tsf', 'text': 'T, S, F', 'visual_cue': 'T S F', 'is_correct': False, 'distractor_rationale': 'Different letters'}, {'id': 'box_bpt', 'text': 'B, P, T', 'visual_cue': 'B P T', 'is_correct': False, 'distractor_rationale': 'Different letters'}], 'correct_answer_id': 'box_ttt', 'explanation': 'Correct! Box [T, T, T] has identical letters.'},
            correct_answer={'correct_answer_id': 'box_ttt'},
            explanation={'en': 'Correct! Box [T, T, T] has identical letters.', 'ar': 'صحيح! الصندوق [T, T, T] يحتوي على حروف متطابقة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.letter.order.abc_group',
            objective_key='obj.lit.group_identical_letters',
            subject_code='literacy',
            unit_code='unit.lit.letter_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Order the grouped letter cards in alphabetical sequence: A, B, C.', 'ar': 'رتب بطاقات الحروف المجمعة بالتسلسل الأبجدي: A، B، C.'},
            content_payload={'prompt': 'Order the grouped letter cards in alphabetical sequence: A, B, C.', 'items': [{'id': 'gc_B', 'label': 'Card B', 'visual_cue': 'B'}, {'id': 'gc_A', 'label': 'Card A', 'visual_cue': 'A'}, {'id': 'gc_C', 'label': 'Card C', 'visual_cue': 'C'}], 'correct_sequence': ['gc_A', 'gc_B', 'gc_C'], 'direction': 'ascending'},
            correct_answer={'correct_sequence': ['gc_A', 'gc_B', 'gc_C']},
            explanation={'en': 'Perfect alphabet ordering!', 'ar': 'ترتيب أبجدي مثالي!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.sound.mc_initial_sun',
            objective_key='obj.lit.initial_sound_word',
            subject_code='literacy',
            unit_code='unit.lit.letter_sounds',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': "What is the initial sound of the word 'Sun ☀️'?", 'ar': "ما هو الصوت الأول لكلمة 'Sun ☀️'؟"},
            content_payload={'question': "What is the initial sound of the word 'Sun ☀️'?", 'options': [{'id': 'snd_s', 'text': 'Sound /s/', 'visual_cue': 's', 'is_correct': True, 'distractor_rationale': None}, {'id': 'snd_m', 'text': 'Sound /m/', 'visual_cue': 'm', 'is_correct': False, 'distractor_rationale': 'Different sound'}, {'id': 'snd_t', 'text': 'Sound /t/', 'visual_cue': 't', 'is_correct': False, 'distractor_rationale': 'Different sound'}], 'correct_answer_id': 'snd_s', 'explanation': "Correct! 'Sun' starts with the /s/ sound."},
            correct_answer={'correct_answer_id': 'snd_s'},
            explanation={'en': "Correct! 'Sun' starts with the /s/ sound.", 'ar': "صحيح! كلمة 'Sun' تبدأ بالصوت /s/."},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.sound.mc_initial_dog',
            objective_key='obj.lit.initial_sound_word',
            subject_code='literacy',
            unit_code='unit.lit.letter_sounds',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': "What is the initial sound of the word 'Dog 🐶'?", 'ar': "ما هو الصوت الأول لكلمة 'Dog 🐶'؟"},
            content_payload={'question': "What is the initial sound of the word 'Dog 🐶'?", 'options': [{'id': 'snd_d', 'text': 'Sound /d/', 'visual_cue': 'd', 'is_correct': True, 'distractor_rationale': None}, {'id': 'snd_b', 'text': 'Sound /b/', 'visual_cue': 'b', 'is_correct': False, 'distractor_rationale': 'Reversed letter sound'}, {'id': 'snd_g', 'text': 'Sound /g/', 'visual_cue': 'g', 'is_correct': False, 'distractor_rationale': 'Ending sound of dog'}], 'correct_answer_id': 'snd_d', 'explanation': "Super! 'Dog' begins with the /d/ sound."},
            correct_answer={'correct_answer_id': 'snd_d'},
            explanation={'en': "Super! 'Dog' begins with the /d/ sound.", 'ar': "ممتاز! كلمة 'Dog' تبدأ بالصوت /d/."},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.sound.match_word_sounds',
            objective_key='obj.lit.initial_sound_word',
            subject_code='literacy',
            unit_code='unit.lit.letter_sounds',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each word picture to its beginning sound.', 'ar': 'طابق كل صورة كلمة بصوتها الأول.'},
            content_payload={'prompt': 'Match each word picture to its beginning sound.', 'left_items': [{'id': 'wp_cat', 'label': 'Cat 🐱', 'visual_cue': 'cat'}, {'id': 'wp_fish', 'label': 'Fish 🐟', 'visual_cue': 'fish'}], 'right_items': [{'id': 'bs_k', 'label': 'Initial /k/', 'visual_cue': '/k/'}, {'id': 'bs_f', 'label': 'Initial /f/', 'visual_cue': '/f/'}], 'pairs': [{'left_id': 'wp_cat', 'right_id': 'bs_k'}, {'left_id': 'wp_fish', 'right_id': 'bs_f'}]},
            correct_answer={'pairs': [{'left_id': 'wp_cat', 'right_id': 'bs_k'}, {'left_id': 'wp_fish', 'right_id': 'bs_f'}]},
            explanation={'en': 'Great matching! Cat begins with /k/, Fish begins with /f/.', 'ar': 'مطابقة رائعة! Cat تبدأ بـ /k/، و Fish تبدأ بـ /f/.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.sound.vis_spot_sound_p',
            objective_key='obj.lit.initial_sound_word',
            subject_code='literacy',
            unit_code='unit.lit.letter_sounds',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the animal that begins with the sound /p/.', 'ar': 'حدد الحيوان الذي يبدأ اسمه بالصوت /p/.'},
            content_payload={'prompt': 'Spot the animal that begins with the sound /p/.', 'scene_description': 'A farmyard scene with a pig, a cow, and a sheep.', 'elements': [{'id': 'an_cow', 'label': 'Cow 🐮', 'category': 'animal', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'an_pig', 'label': 'Pig 🐷', 'category': 'animal', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'an_sheep', 'label': 'Sheep 🐑', 'category': 'animal', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'an_pig', 'feedback_clue': 'Look for the pink animal that says oink: Pig starts with /p/.'},
            correct_answer={'target_id': 'an_pig'},
            explanation={'en': "Terrific! 'Pig' starts with the sound /p/.", 'ar': "رائع! 'Pig' تبدأ بالصوت /p/."},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.sound.mc_sound_tiger',
            objective_key='obj.lit.match_letter_initial_sound',
            subject_code='literacy',
            unit_code='unit.lit.letter_sounds',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': "Which letter makes the sound /t/ as in 'Tiger 🐯'?", 'ar': "أي حرف يصدر الصوت /t/ كما في 'Tiger 🐯'؟"},
            content_payload={'question': "Which letter makes the sound /t/ as in 'Tiger 🐯'?", 'options': [{'id': 'lt_T', 'text': 'Letter T', 'visual_cue': 'T', 'is_correct': True, 'distractor_rationale': None}, {'id': 'lt_D', 'text': 'Letter D', 'visual_cue': 'D', 'is_correct': False, 'distractor_rationale': 'Makes /d/ sound'}, {'id': 'lt_P', 'text': 'Letter P', 'visual_cue': 'P', 'is_correct': False, 'distractor_rationale': 'Makes /p/ sound'}], 'correct_answer_id': 'lt_T', 'explanation': 'Correct! Letter T makes the /t/ sound.'},
            correct_answer={'correct_answer_id': 'lt_T'},
            explanation={'en': 'Correct! Letter T makes the /t/ sound.', 'ar': 'صحيح! الحرف T يصدر الصوت /t/.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.sound.match_letters_pictures',
            objective_key='obj.lit.match_letter_initial_sound',
            subject_code='literacy',
            unit_code='unit.lit.letter_sounds',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each letter to a picture representing its sound.', 'ar': 'طابق كل حرف بصورة تمثل صوته.'},
            content_payload={'prompt': 'Match each letter to a picture representing its sound.', 'left_items': [{'id': 'lt_s', 'label': 'Letter S', 'visual_cue': 'S'}, {'id': 'lt_m', 'label': 'Letter M', 'visual_cue': 'M'}, {'id': 'lt_r', 'label': 'Letter R', 'visual_cue': 'R'}], 'right_items': [{'id': 'pc_sun', 'label': 'Sun ☀️ (/s/)', 'visual_cue': 'sun'}, {'id': 'pc_moon', 'label': 'Moon 🌙 (/m/)', 'visual_cue': 'moon'}, {'id': 'pc_ring', 'label': 'Ring 💍 (/r/)', 'visual_cue': 'ring'}], 'pairs': [{'left_id': 'lt_s', 'right_id': 'pc_sun'}, {'left_id': 'lt_m', 'right_id': 'pc_moon'}, {'left_id': 'lt_r', 'right_id': 'pc_ring'}]},
            correct_answer={'pairs': [{'left_id': 'lt_s', 'right_id': 'pc_sun'}, {'left_id': 'lt_m', 'right_id': 'pc_moon'}, {'left_id': 'lt_r', 'right_id': 'pc_ring'}]},
            explanation={'en': 'Awesome letter-sound matching!', 'ar': 'مطابقة رائعة بين الحروف والأصوات!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.sound.drag.sort_B_P',
            objective_key='obj.lit.match_letter_initial_sound',
            subject_code='literacy',
            unit_code='unit.lit.letter_sounds',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort pictures into 'Starts with B' and 'Starts with P'.", 'ar': "صنف الصور إلى 'تبدأ بحرف B' و 'تبدأ بحرف P'."},
            content_payload={'prompt': "Sort pictures into 'Starts with B' and 'Starts with P'.", 'items': [{'id': 'it_ball', 'label': 'Ball ⚽', 'visual_cue': 'ball'}, {'id': 'it_bear', 'label': 'Bear 🐻', 'visual_cue': 'bear'}, {'id': 'it_pen', 'label': 'Pen 🖊️', 'visual_cue': 'pen'}, {'id': 'it_pot', 'label': 'Pot 🍲', 'visual_cue': 'pot'}], 'zones': [{'id': 'z_B', 'label': 'Starts with B (/b/)', 'capacity': 3}, {'id': 'z_P', 'label': 'Starts with P (/p/)', 'capacity': 3}], 'correct_mapping': {'it_ball': 'z_B', 'it_bear': 'z_B', 'it_pen': 'z_P', 'it_pot': 'z_P'}},
            correct_answer={'correct_mapping': {'it_ball': 'z_B', 'it_bear': 'z_B', 'it_pen': 'z_P', 'it_pot': 'z_P'}},
            explanation={'en': 'Brilliant phonics sorting for B and P!', 'ar': 'فرز صوتي رائع لحرفي B و P!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.sound.vis_lion_letter',
            objective_key='obj.lit.match_letter_initial_sound',
            subject_code='literacy',
            unit_code='unit.lit.letter_sounds',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Find the letter that begins the name of the Lion 🦁.', 'ar': 'حدد الحرف الذي يبدأ به اسم الأسد Lion 🦁.'},
            content_payload={'prompt': 'Find the letter that begins the name of the Lion 🦁.', 'scene_description': 'A safari alphabet board showing a lion illustration.', 'elements': [{'id': 'l_L', 'label': 'Letter L', 'category': 'letter', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'l_K', 'label': 'Letter K', 'category': 'letter', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'l_J', 'label': 'Letter J', 'category': 'letter', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'l_L', 'feedback_clue': 'Lion begins with the /l/ sound: Letter L.'},
            correct_answer={'target_id': 'l_L'},
            explanation={'en': 'Spot on! L is for Lion.', 'ar': 'صحيح! حرف L لكلمة Lion.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.sound.mc_word_starts_m',
            objective_key='obj.lit.word_starts_target_sound',
            subject_code='literacy',
            unit_code='unit.lit.letter_sounds',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which word starts with the sound /m/?', 'ar': 'أي كلمة تبدأ بالصوت /m/؟'},
            content_payload={'question': 'Which word starts with the sound /m/?', 'options': [{'id': 'w_moon', 'text': 'Moon 🌙', 'visual_cue': 'moon', 'is_correct': True, 'distractor_rationale': None}, {'id': 'w_sun', 'text': 'Sun ☀️', 'visual_cue': 'sun', 'is_correct': False, 'distractor_rationale': 'Starts with /s/'}, {'id': 'w_star', 'text': 'Star ⭐', 'visual_cue': 'star', 'is_correct': False, 'distractor_rationale': 'Starts with /st/'}], 'correct_answer_id': 'w_moon', 'explanation': "Correct! 'Moon' begins with /m/."},
            correct_answer={'correct_answer_id': 'w_moon'},
            explanation={'en': "Correct! 'Moon' begins with /m/.", 'ar': "صحيح! كلمة 'Moon' تبدأ بالصوت /m/."},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.sound.mc_word_starts_f',
            objective_key='obj.lit.word_starts_target_sound',
            subject_code='literacy',
            unit_code='unit.lit.letter_sounds',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which word starts with the sound /f/?', 'ar': 'أي كلمة تبدأ بالصوت /f/؟'},
            content_payload={'question': 'Which word starts with the sound /f/?', 'options': [{'id': 'w_fish', 'text': 'Fish 🐟', 'visual_cue': 'fish', 'is_correct': True, 'distractor_rationale': None}, {'id': 'w_bird', 'text': 'Bird 🐦', 'visual_cue': 'bird', 'is_correct': False, 'distractor_rationale': 'Starts with /b/'}, {'id': 'w_cat', 'text': 'Cat 🐱', 'visual_cue': 'cat', 'is_correct': False, 'distractor_rationale': 'Starts with /k/'}], 'correct_answer_id': 'w_fish', 'explanation': "Super! 'Fish' begins with /f/."},
            correct_answer={'correct_answer_id': 'w_fish'},
            explanation={'en': "Super! 'Fish' begins with /f/.", 'ar': "ممتاز! كلمة 'Fish' تبدأ بالصوت /f/."},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.sound.vis_fruit_apple',
            objective_key='obj.lit.word_starts_target_sound',
            subject_code='literacy',
            unit_code='unit.lit.letter_sounds',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the fruit that starts with the short /a/ sound.', 'ar': 'حدد الفاكهة التي تبدأ بالصوت /a/ القصير.'},
            content_payload={'prompt': 'Spot the fruit that starts with the short /a/ sound.', 'scene_description': 'A fruit bowl with an apple, a banana, and cherries.', 'elements': [{'id': 'fr_banana', 'label': 'Banana 🍌 (/b/)', 'category': 'fruit', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'fr_apple', 'label': 'Apple 🍎 (/a/)', 'category': 'fruit', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'fr_cherry', 'label': 'Cherries 🍒 (/ch/)', 'category': 'fruit', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'fr_apple', 'feedback_clue': 'Listen for the /a/ sound: Apple starts with /a/.'},
            correct_answer={'target_id': 'fr_apple'},
            explanation={'en': 'Wonderful observation! Apple starts with /a/.', 'ar': 'ملاحظة رائعة! Apple تبدأ بالصوت /a/.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.sound.match_sounds_words',
            objective_key='obj.lit.word_starts_target_sound',
            subject_code='literacy',
            unit_code='unit.lit.letter_sounds',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match target initial sounds to words that begin with them.', 'ar': 'طابق الأصوات الأولى المستهدفة بالكلمات التي تبدأ بها.'},
            content_payload={'prompt': 'Match target initial sounds to words that begin with them.', 'left_items': [{'id': 'snd_b', 'label': 'Sound /b/', 'visual_cue': '/b/'}, {'id': 'snd_h', 'label': 'Sound /h/', 'visual_cue': '/h/'}], 'right_items': [{'id': 'wd_ball', 'label': 'Ball ⚽', 'visual_cue': 'ball'}, {'id': 'wd_hat', 'label': 'Hat 🎩', 'visual_cue': 'hat'}], 'pairs': [{'left_id': 'snd_b', 'right_id': 'wd_ball'}, {'left_id': 'snd_h', 'right_id': 'wd_hat'}]},
            correct_answer={'pairs': [{'left_id': 'snd_b', 'right_id': 'wd_ball'}, {'left_id': 'snd_h', 'right_id': 'wd_hat'}]},
            explanation={'en': 'Terrific phonics matching!', 'ar': 'مطابقة صوتية رائعة!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.sound.drag.sort_s_t',
            objective_key='obj.lit.word_starts_target_sound',
            subject_code='literacy',
            unit_code='unit.lit.letter_sounds',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort pictures into 'Starts with /s/' and 'Starts with /t/'.", 'ar': "صنف الصور إلى 'تبدأ بـ /s/' و 'تبدأ بـ /t/'."},
            content_payload={'prompt': "Sort pictures into 'Starts with /s/' and 'Starts with /t/'.", 'items': [{'id': 'p_sock', 'label': 'Sock 🧦', 'visual_cue': 'sock'}, {'id': 'p_soap', 'label': 'Soap 🧼', 'visual_cue': 'soap'}, {'id': 'p_table', 'label': 'Table 🪵', 'visual_cue': 'table'}, {'id': 'p_tent', 'label': 'Tent ⛺', 'visual_cue': 'tent'}], 'zones': [{'id': 'z_snd_s', 'label': 'Initial /s/', 'capacity': 3}, {'id': 'z_snd_t', 'label': 'Initial /t/', 'capacity': 3}], 'correct_mapping': {'p_sock': 'z_snd_s', 'p_soap': 'z_snd_s', 'p_table': 'z_snd_t', 'p_tent': 'z_snd_t'}},
            correct_answer={'correct_mapping': {'p_sock': 'z_snd_s', 'p_soap': 'z_snd_s', 'p_table': 'z_snd_t', 'p_tent': 'z_snd_t'}},
            explanation={'en': 'Great sorting by initial phoneme!', 'ar': 'فرز رائع حسب الصوت الأول!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.sound.mc_same_sound_bat_ball',
            objective_key='obj.lit.distinguish_two_initial_sounds',
            subject_code='literacy',
            unit_code='unit.lit.letter_sounds',
            difficulty_level=3,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': "Do 'Bat 🦇' and 'Ball ⚽' start with the same sound?", 'ar': "هل تبدأ كلمتا 'Bat 🦇' و 'Ball ⚽' بنفس الصوت؟"},
            content_payload={'question': "Do 'Bat 🦇' and 'Ball ⚽' start with the same sound?", 'options': [{'id': 'ans_yes', 'text': 'Yes, both start with /b/', 'visual_cue': '✅ /b/', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_no', 'text': 'No, they start with different sounds', 'visual_cue': '❌', 'is_correct': False, 'distractor_rationale': 'Both begin with B'}], 'correct_answer_id': 'ans_yes', 'explanation': "Correct! Both 'Bat' and 'Ball' start with the sound /b/."},
            correct_answer={'correct_answer_id': 'ans_yes'},
            explanation={'en': "Correct! Both 'Bat' and 'Ball' start with the sound /b/.", 'ar': 'صحيح! كلتا الكلمتين تبدآن بالصوت /b/.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.sound.mc_two_same_initial',
            objective_key='obj.lit.distinguish_two_initial_sounds',
            subject_code='literacy',
            unit_code='unit.lit.letter_sounds',
            difficulty_level=3,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which two words start with the SAME initial sound?', 'ar': 'أي كلمتين تبدآن بنفس الصوت الأول؟'},
            content_payload={'question': 'Which two words start with the SAME initial sound?', 'options': [{'id': 'pr_sun_star', 'text': 'Sun ☀️ and Star ⭐', 'visual_cue': '☀️ ⭐', 'is_correct': True, 'distractor_rationale': None}, {'id': 'pr_cat_dog', 'text': 'Cat 🐱 and Dog 🐶', 'visual_cue': '🐱 🐶', 'is_correct': False, 'distractor_rationale': 'Starts with /k/ and /d/'}, {'id': 'pr_fish_bird', 'text': 'Fish 🐟 and Bird 🐦', 'visual_cue': '🐟 🐦', 'is_correct': False, 'distractor_rationale': 'Starts with /f/ and /b/'}], 'correct_answer_id': 'pr_sun_star', 'explanation': "Super! Both 'Sun' and 'Star' start with /s/."},
            correct_answer={'correct_answer_id': 'pr_sun_star'},
            explanation={'en': "Super! Both 'Sun' and 'Star' start with /s/.", 'ar': 'ممتاز! كلتا الكلمتين تبدآن بالصوت /s/.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.sound.match_sound_partners',
            objective_key='obj.lit.distinguish_two_initial_sounds',
            subject_code='literacy',
            unit_code='unit.lit.letter_sounds',
            difficulty_level=3,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match words that share the same initial sound.', 'ar': 'طابق الكلمات التي تشترك في نفس الصوت الأول.'},
            content_payload={'prompt': 'Match words that share the same initial sound.', 'left_items': [{'id': 'w_cat', 'label': 'Cat 🐱 (/k/)', 'visual_cue': 'cat'}, {'id': 'w_duck', 'label': 'Duck 🦆 (/d/)', 'visual_cue': 'duck'}], 'right_items': [{'id': 'w_cup', 'label': 'Cup ☕ (/k/)', 'visual_cue': 'cup'}, {'id': 'w_drum', 'label': 'Drum 🥁 (/d/)', 'visual_cue': 'drum'}], 'pairs': [{'left_id': 'w_cat', 'right_id': 'w_cup'}, {'left_id': 'w_duck', 'right_id': 'w_drum'}]},
            correct_answer={'pairs': [{'left_id': 'w_cat', 'right_id': 'w_cup'}, {'left_id': 'w_duck', 'right_id': 'w_drum'}]},
            explanation={'en': 'Terrific phoneme pairing! Cat pairs with Cup, Duck pairs with Drum.', 'ar': 'مطابقة صوتية رائعة!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.sound.drag.sort_bear_duck',
            objective_key='obj.lit.distinguish_two_initial_sounds',
            subject_code='literacy',
            unit_code='unit.lit.letter_sounds',
            difficulty_level=3,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': 'Sort items by initial sound: Sound /b/ vs Sound /d/.', 'ar': 'صنف العناصر حسب الصوت الأول: الصوت /b/ مقابل الصوت /d/.'},
            content_payload={'prompt': 'Sort items by initial sound: Sound /b/ vs Sound /d/.', 'items': [{'id': 'item_bear', 'label': 'Bear 🐻', 'visual_cue': 'bear'}, {'id': 'item_boat', 'label': 'Boat ⛵', 'visual_cue': 'boat'}, {'id': 'item_door', 'label': 'Door 🚪', 'visual_cue': 'door'}, {'id': 'item_doll', 'label': 'Doll 🪆', 'visual_cue': 'doll'}], 'zones': [{'id': 'z_b', 'label': 'Sound /b/', 'capacity': 3}, {'id': 'z_d', 'label': 'Sound /d/', 'capacity': 3}], 'correct_mapping': {'item_bear': 'z_b', 'item_boat': 'z_b', 'item_door': 'z_d', 'item_doll': 'z_d'}},
            correct_answer={'correct_mapping': {'item_bear': 'z_b', 'item_boat': 'z_b', 'item_door': 'z_d', 'item_doll': 'z_d'}},
            explanation={'en': 'Spot on distinction between /b/ and /d/!', 'ar': 'تمييز ممتاز بين /b/ و /d/!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.sound.vis_not_p',
            objective_key='obj.lit.distinguish_two_initial_sounds',
            subject_code='literacy',
            unit_code='unit.lit.letter_sounds',
            difficulty_level=3,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Find the item that does NOT start with the sound /p/.', 'ar': 'حدد العنصر الذي لا يبدأ بالصوت /p/.'},
            content_payload={'prompt': 'Find the item that does NOT start with the sound /p/.', 'scene_description': 'A desktop tray displaying a pen, a pot, and a sun.', 'elements': [{'id': 'it_pen', 'label': 'Pen 🖊️ (/p/)', 'category': 'item', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'it_sun', 'label': 'Sun ☀️ (/s/)', 'category': 'item', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'it_pot', 'label': 'Pot 🍲 (/p/)', 'category': 'item', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'it_sun', 'feedback_clue': 'Pen and Pot start with /p/; Sun starts with /s/.'},
            correct_answer={'target_id': 'it_sun'},
            explanation={'en': 'Excellent listening! Sun starts with /s/, not /p/.', 'ar': 'استماع ممتاز! Sun تبدأ بالصوت /s/ وليس /p/.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.word.mc_recognize_cat',
            objective_key='obj.lit.recognize_simple_words',
            subject_code='literacy',
            unit_code='unit.lit.word_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': "Which word says 'CAT'?", 'ar': "أي كلمة تقول 'CAT'؟"},
            content_payload={'question': "Which word says 'CAT'?", 'options': [{'id': 'ans_cat', 'text': 'CAT', 'visual_cue': 'CAT', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_dog', 'text': 'DOG', 'visual_cue': 'DOG', 'is_correct': False, 'distractor_rationale': 'Different letters'}, {'id': 'ans_car', 'text': 'CAR', 'visual_cue': 'CAR', 'is_correct': False, 'distractor_rationale': 'Ends with R'}], 'correct_answer_id': 'ans_cat', 'explanation': 'Correct! C-A-T spells CAT.'},
            correct_answer={'correct_answer_id': 'ans_cat'},
            explanation={'en': 'Correct! C-A-T spells CAT.', 'ar': 'صحيح! C-A-T تهجئة كلمة CAT.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.word.mc_recognize_red',
            objective_key='obj.lit.recognize_simple_words',
            subject_code='literacy',
            unit_code='unit.lit.word_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': "Which word says 'RED'?", 'ar': "أي كلمة تقول 'RED'؟"},
            content_payload={'question': "Which word says 'RED'?", 'options': [{'id': 'ans_red', 'text': 'RED', 'visual_cue': 'RED', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_run', 'text': 'RUN', 'visual_cue': 'RUN', 'is_correct': False, 'distractor_rationale': 'Ends with N'}, {'id': 'ans_bed', 'text': 'BED', 'visual_cue': 'BED', 'is_correct': False, 'distractor_rationale': 'Starts with B'}], 'correct_answer_id': 'ans_red', 'explanation': 'Super! R-E-D spells RED.'},
            correct_answer={'correct_answer_id': 'ans_red'},
            explanation={'en': 'Super! R-E-D spells RED.', 'ar': 'ممتاز! R-E-D تهجئة كلمة RED.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.word.vis_find_sun',
            objective_key='obj.lit.recognize_simple_words',
            subject_code='literacy',
            unit_code='unit.lit.word_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': "Find the word 'SUN' on the classroom chart.", 'ar': "ابحث عن كلمة 'SUN' على لوحة الفصل."},
            content_payload={'prompt': "Find the word 'SUN' on the classroom chart.", 'scene_description': 'A vocabulary chart showing words BIG, SUN, and RUN.', 'elements': [{'id': 'w_big', 'label': 'BIG', 'category': 'word', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'w_sun', 'label': 'SUN', 'category': 'word', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'w_run', 'label': 'RUN', 'category': 'word', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'w_sun', 'feedback_clue': 'Look for the word beginning with letter S and ending with N.'},
            correct_answer={'target_id': 'w_sun'},
            explanation={'en': 'Wonderful! You found the word SUN.', 'ar': 'رائع! لقد وجدت كلمة SUN.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.word.match_sight_words',
            objective_key='obj.lit.recognize_simple_words',
            subject_code='literacy',
            unit_code='unit.lit.word_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match sight words to their identical cards.', 'ar': 'طابق الكلمات البصرية ببطاقاتها المتطابقة.'},
            content_payload={'prompt': 'Match sight words to their identical cards.', 'left_items': [{'id': 'sw_in', 'label': 'IN', 'visual_cue': 'IN'}, {'id': 'sw_on', 'label': 'ON', 'visual_cue': 'ON'}], 'right_items': [{'id': 'sw_in_tgt', 'label': 'IN', 'visual_cue': 'IN'}, {'id': 'sw_on_tgt', 'label': 'ON', 'visual_cue': 'ON'}], 'pairs': [{'left_id': 'sw_in', 'right_id': 'sw_in_tgt'}, {'left_id': 'sw_on', 'right_id': 'sw_on_tgt'}]},
            correct_answer={'pairs': [{'left_id': 'sw_in', 'right_id': 'sw_in_tgt'}, {'left_id': 'sw_on', 'right_id': 'sw_on_tgt'}]},
            explanation={'en': 'Terrific sight word recognition!', 'ar': 'تمييز رائع للكلمات البصرية!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.word.drag.sort_cvc_colors',
            objective_key='obj.lit.recognize_simple_words',
            subject_code='literacy',
            unit_code='unit.lit.word_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort word cards into 'Animal Words' and 'Color Words'.", 'ar': "صنف بطاقات الكلمات إلى 'كلمات حيوانات' و 'كلمات ألوان'."},
            content_payload={'prompt': "Sort word cards into 'Animal Words' and 'Color Words'.", 'items': [{'id': 'wc_cat', 'label': 'CAT', 'visual_cue': 'CAT'}, {'id': 'wc_dog', 'label': 'DOG', 'visual_cue': 'DOG'}, {'id': 'wc_red', 'label': 'RED', 'visual_cue': 'RED'}, {'id': 'wc_blue', 'label': 'BLUE', 'visual_cue': 'BLUE'}], 'zones': [{'id': 'z_animals', 'label': 'Animal Words', 'capacity': 3}, {'id': 'z_colors', 'label': 'Color Words', 'capacity': 3}], 'correct_mapping': {'wc_cat': 'z_animals', 'wc_dog': 'z_animals', 'wc_red': 'z_colors', 'wc_blue': 'z_colors'}},
            correct_answer={'correct_mapping': {'wc_cat': 'z_animals', 'wc_dog': 'z_animals', 'wc_red': 'z_colors', 'wc_blue': 'z_colors'}},
            explanation={'en': 'Great categorization of familiar words!', 'ar': 'تصنيف رائع للكلمات المألوفة!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.word.match_identical_cards',
            objective_key='obj.lit.match_identical_words',
            subject_code='literacy',
            unit_code='unit.lit.word_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match identical word cards together.', 'ar': 'طابق بطاقات الكلمات المتطابقة معاً.'},
            content_payload={'prompt': 'Match identical word cards together.', 'left_items': [{'id': 'w_dog', 'label': 'DOG', 'visual_cue': 'DOG'}, {'id': 'w_run', 'label': 'RUN', 'visual_cue': 'RUN'}, {'id': 'w_big', 'label': 'BIG', 'visual_cue': 'BIG'}], 'right_items': [{'id': 'm_dog', 'label': 'DOG', 'visual_cue': 'DOG'}, {'id': 'm_run', 'label': 'RUN', 'visual_cue': 'RUN'}, {'id': 'm_big', 'label': 'BIG', 'visual_cue': 'BIG'}], 'pairs': [{'left_id': 'w_dog', 'right_id': 'm_dog'}, {'left_id': 'w_run', 'right_id': 'm_run'}, {'left_id': 'w_big', 'right_id': 'm_big'}]},
            correct_answer={'pairs': [{'left_id': 'w_dog', 'right_id': 'm_dog'}, {'left_id': 'w_run', 'right_id': 'm_run'}, {'left_id': 'w_big', 'right_id': 'm_big'}]},
            explanation={'en': 'Perfect word matching! All cards pair identically.', 'ar': 'مطابقة كلمات مثالية!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.word.mc_exact_match_book',
            objective_key='obj.lit.match_identical_words',
            subject_code='literacy',
            unit_code='unit.lit.word_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': "Which word is an EXACT match to 'BOOK'?", 'ar': "أي كلمة تطابق كلمة 'BOOK' تماماً؟"},
            content_payload={'question': "Which word is an EXACT match to 'BOOK'?", 'options': [{'id': 'ans_book', 'text': 'BOOK', 'visual_cue': 'BOOK', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_look', 'text': 'LOOK', 'visual_cue': 'LOOK', 'is_correct': False, 'distractor_rationale': 'Starts with L'}, {'id': 'ans_cook', 'text': 'COOK', 'visual_cue': 'COOK', 'is_correct': False, 'distractor_rationale': 'Starts with C'}], 'correct_answer_id': 'ans_book', 'explanation': 'Correct! B-O-O-K matches BOOK identically.'},
            correct_answer={'correct_answer_id': 'ans_book'},
            explanation={'en': 'Correct! B-O-O-K matches BOOK identically.', 'ar': 'صحيح! B-O-O-K تطابق BOOK تماماً.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.word.vis_twin_fish',
            objective_key='obj.lit.match_identical_words',
            subject_code='literacy',
            unit_code='unit.lit.word_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': "Spot the twin word card for 'FISH'.", 'ar': "حدد بطاقة الكلمة التوأم لكلمة 'FISH'."},
            content_payload={'prompt': "Spot the twin word card for 'FISH'.", 'scene_description': 'A table with three word flashcards.', 'elements': [{'id': 'card_dish', 'label': 'DISH', 'category': 'card', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'card_fish', 'label': 'FISH', 'category': 'card', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'card_wish', 'label': 'WISH', 'category': 'card', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'card_fish', 'feedback_clue': 'Look for the card beginning with letter F: F-I-S-H.'},
            correct_answer={'target_id': 'card_fish'},
            explanation={'en': 'Terrific! You spotted the matching word FISH.', 'ar': 'رائع! لقد حددت الكلمة المطابقة FISH.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.word.drag.identical_slots',
            objective_key='obj.lit.match_identical_words',
            subject_code='literacy',
            unit_code='unit.lit.word_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': 'Place word cards into their exact matching slots: CAT and DOG.', 'ar': 'ضع بطاقات الكلمات في خاناتها المطابقة تماماً: CAT و DOG.'},
            content_payload={'prompt': 'Place word cards into their exact matching slots: CAT and DOG.', 'items': [{'id': 'card_cat_1', 'label': 'CAT', 'visual_cue': 'CAT'}, {'id': 'card_dog_1', 'label': 'DOG', 'visual_cue': 'DOG'}], 'zones': [{'id': 'slot_cat', 'label': 'Slot [ CAT ]', 'capacity': 1}, {'id': 'slot_dog', 'label': 'Slot [ DOG ]', 'capacity': 1}], 'correct_mapping': {'card_cat_1': 'slot_cat', 'card_dog_1': 'slot_dog'}},
            correct_answer={'correct_mapping': {'card_cat_1': 'slot_cat', 'card_dog_1': 'slot_dog'}},
            explanation={'en': 'Spot on! Each word card is in its exact slot.', 'ar': 'صحيح! كل بطاقة في خانتها المطابقة تماماً.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.word.order.identical_pairs',
            objective_key='obj.lit.match_identical_words',
            subject_code='literacy',
            unit_code='unit.lit.word_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Order the rhyming word cards in reading sequence: CAT, HAT, MAT.', 'ar': 'رتب بطاقات الكلمات ذات القافية بتسلسل القراءة: CAT، HAT، MAT.'},
            content_payload={'prompt': 'Order the rhyming word cards in reading sequence: CAT, HAT, MAT.', 'items': [{'id': 'ord_hat', 'label': 'HAT', 'visual_cue': 'HAT'}, {'id': 'ord_cat', 'label': 'CAT', 'visual_cue': 'CAT'}, {'id': 'ord_mat', 'label': 'MAT', 'visual_cue': 'MAT'}], 'correct_sequence': ['ord_cat', 'ord_hat', 'ord_mat'], 'direction': 'ascending'},
            correct_answer={'correct_sequence': ['ord_cat', 'ord_hat', 'ord_mat']},
            explanation={'en': 'Wonderful word reading sequence!', 'ar': 'تسلسل قراءة كلمات رائع!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.word.mc_pic_car',
            objective_key='obj.lit.match_word_to_image',
            subject_code='literacy',
            unit_code='unit.lit.word_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which word matches this picture: 🚗 (Car)?', 'ar': 'أي كلمة تطابق هذه الصورة: 🚗 (Car)؟'},
            content_payload={'question': 'Which word matches this picture: 🚗 (Car)?', 'options': [{'id': 'ans_car', 'text': 'CAR', 'visual_cue': 'CAR', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_bus', 'text': 'BUS', 'visual_cue': 'BUS', 'is_correct': False, 'distractor_rationale': 'Different vehicle'}, {'id': 'ans_van', 'text': 'VAN', 'visual_cue': 'VAN', 'is_correct': False, 'distractor_rationale': 'Different vehicle'}], 'correct_answer_id': 'ans_car', 'explanation': 'Correct! The picture shows a CAR.'},
            correct_answer={'correct_answer_id': 'ans_car'},
            explanation={'en': 'Correct! The picture shows a CAR.', 'ar': 'صحيح! الصورة تظهر سيارة CAR.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.word.match_words_pictures',
            objective_key='obj.lit.match_word_to_image',
            subject_code='literacy',
            unit_code='unit.lit.word_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each word to its familiar picture.', 'ar': 'طابق كل كلمة بصورتها المألوفة.'},
            content_payload={'prompt': 'Match each word to its familiar picture.', 'left_items': [{'id': 'w_tree', 'label': 'TREE', 'visual_cue': 'TREE'}, {'id': 'w_star', 'label': 'STAR', 'visual_cue': 'STAR'}, {'id': 'w_book', 'label': 'BOOK', 'visual_cue': 'BOOK'}], 'right_items': [{'id': 'p_tree', 'label': 'Tree 🌲', 'visual_cue': 'tree'}, {'id': 'p_star', 'label': 'Star ⭐', 'visual_cue': 'star'}, {'id': 'p_book', 'label': 'Book 📖', 'visual_cue': 'book'}], 'pairs': [{'left_id': 'w_tree', 'right_id': 'p_tree'}, {'left_id': 'w_star', 'right_id': 'p_star'}, {'left_id': 'w_book', 'right_id': 'p_book'}]},
            correct_answer={'pairs': [{'left_id': 'w_tree', 'right_id': 'p_tree'}, {'left_id': 'w_star', 'right_id': 'p_star'}, {'left_id': 'w_book', 'right_id': 'p_book'}]},
            explanation={'en': 'Great matching! Words connect directly to images.', 'ar': 'مطابقة ممتازة! الكلمات ترتبط مباشرة بالصور.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.word.vis_apple_pic',
            objective_key='obj.lit.match_word_to_image',
            subject_code='literacy',
            unit_code='unit.lit.word_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': "Find the picture that matches the word 'APPLE'.", 'ar': "حدد الصورة التي تطابق كلمة 'APPLE'."},
            content_payload={'prompt': "Find the picture that matches the word 'APPLE'.", 'scene_description': 'A picture gallery showing an apple, an orange, and grapes.', 'elements': [{'id': 'im_orange', 'label': 'Orange 🍊', 'category': 'fruit', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'im_apple', 'label': 'Red Apple 🍎', 'category': 'fruit', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'im_grapes', 'label': 'Grapes 🍇', 'category': 'fruit', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'im_apple', 'feedback_clue': 'Look for the red round apple.'},
            correct_answer={'target_id': 'im_apple'},
            explanation={'en': 'Super! The red apple matches the word APPLE.', 'ar': 'ممتاز! التفاحة الحمراء تطابق كلمة APPLE.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.word.drag.label_pictures',
            objective_key='obj.lit.match_word_to_image',
            subject_code='literacy',
            unit_code='unit.lit.word_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': 'Drag word labels to their matching pictures.', 'ar': 'اسحب بطاقات الكلمات إلى صورها المطابقة.'},
            content_payload={'prompt': 'Drag word labels to their matching pictures.', 'items': [{'id': 'lbl_dog', 'label': 'DOG', 'visual_cue': 'DOG'}, {'id': 'lbl_cat', 'label': 'CAT', 'visual_cue': 'CAT'}], 'zones': [{'id': 'pic_dog_box', 'label': 'Dog Picture Box 🐶', 'capacity': 1}, {'id': 'pic_cat_box', 'label': 'Cat Picture Box 🐱', 'capacity': 1}], 'correct_mapping': {'lbl_dog': 'pic_dog_box', 'lbl_cat': 'pic_cat_box'}},
            correct_answer={'correct_mapping': {'lbl_dog': 'pic_dog_box', 'lbl_cat': 'pic_cat_box'}},
            explanation={'en': 'Awesome word-picture labeling!', 'ar': 'تسمية ممتازة للكلمات والصور!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.word.mc_find_bed',
            objective_key='obj.lit.target_word_among_distractors',
            subject_code='literacy',
            unit_code='unit.lit.word_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': "Identify the word 'BED' among the lookalikes.", 'ar': "حدد كلمة 'BED' من بين الكلمات المتشابهة."},
            content_payload={'question': "Identify the word 'BED' among the lookalikes.", 'options': [{'id': 'ans_bed', 'text': 'BED', 'visual_cue': 'BED', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_bad', 'text': 'BAD', 'visual_cue': 'BAD', 'is_correct': False, 'distractor_rationale': 'Middle letter is A'}, {'id': 'ans_red', 'text': 'RED', 'visual_cue': 'RED', 'is_correct': False, 'distractor_rationale': 'Starts with R'}], 'correct_answer_id': 'ans_bed', 'explanation': 'Correct! B-E-D spells BED.'},
            correct_answer={'correct_answer_id': 'ans_bed'},
            explanation={'en': 'Correct! B-E-D spells BED.', 'ar': 'صحيح! B-E-D تهجئة كلمة BED.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.word.vis_find_hat',
            objective_key='obj.lit.target_word_among_distractors',
            subject_code='literacy',
            unit_code='unit.lit.word_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': "Spot the target word 'HAT' among the distractor cards.", 'ar': "حدد الكلمة المستهدفة 'HAT' من بين البطاقات المشتتة."},
            content_payload={'prompt': "Spot the target word 'HAT' among the distractor cards.", 'scene_description': 'A chalkboard with cards displaying CAT, HAT, and BAT.', 'elements': [{'id': 'cd_cat', 'label': 'CAT', 'category': 'word', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'cd_hat', 'label': 'HAT', 'category': 'word', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'cd_bat', 'label': 'BAT', 'category': 'word', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'cd_hat', 'feedback_clue': 'Look for the word starting with letter H: H-A-T.'},
            correct_answer={'target_id': 'cd_hat'},
            explanation={'en': 'Great observation! You found HAT.', 'ar': 'ملاحظة رائعة! لقد وجدت كلمة HAT.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.word.match_target_distractor',
            objective_key='obj.lit.target_word_among_distractors',
            subject_code='literacy',
            unit_code='unit.lit.word_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match target words through visual similarity distractors.', 'ar': 'طابق الكلمات المستهدفة عبر مشتتات التشابه البصري.'},
            content_payload={'prompt': 'Match target words through visual similarity distractors.', 'left_items': [{'id': 'tw_sun', 'label': 'Target: SUN', 'visual_cue': 'SUN'}, {'id': 'tw_run', 'label': 'Target: RUN', 'visual_cue': 'RUN'}], 'right_items': [{'id': 'mw_sun', 'label': 'SUN', 'visual_cue': 'SUN'}, {'id': 'mw_run', 'label': 'RUN', 'visual_cue': 'RUN'}], 'pairs': [{'left_id': 'tw_sun', 'right_id': 'mw_sun'}, {'left_id': 'tw_run', 'right_id': 'mw_run'}]},
            correct_answer={'pairs': [{'left_id': 'tw_sun', 'right_id': 'mw_sun'}, {'left_id': 'tw_run', 'right_id': 'mw_run'}]},
            explanation={'en': 'Terrific matching amidst rhyming distractors!', 'ar': 'مطابقة رائعة وسط مشتتات القافية!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.word.drag.sort_target_GO',
            objective_key='obj.lit.target_word_among_distractors',
            subject_code='literacy',
            unit_code='unit.lit.word_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort cards into 'Target Word GO' and 'Other Words'.", 'ar': "صنف البطاقات إلى 'الكلمة المستهدفة GO' و 'كلمات أخرى'."},
            content_payload={'prompt': "Sort cards into 'Target Word GO' and 'Other Words'.", 'items': [{'id': 'w_go1', 'label': 'GO', 'visual_cue': 'GO'}, {'id': 'w_go2', 'label': 'GO', 'visual_cue': 'GO'}, {'id': 'w_no', 'label': 'NO', 'visual_cue': 'NO'}, {'id': 'w_so', 'label': 'SO', 'visual_cue': 'SO'}], 'zones': [{'id': 'z_target_go', 'label': 'Target: GO', 'capacity': 3}, {'id': 'z_other_words', 'label': 'Other Words', 'capacity': 3}], 'correct_mapping': {'w_go1': 'z_target_go', 'w_go2': 'z_target_go', 'w_no': 'z_other_words', 'w_so': 'z_other_words'}},
            correct_answer={'correct_mapping': {'w_go1': 'z_target_go', 'w_go2': 'z_target_go', 'w_no': 'z_other_words', 'w_so': 'z_other_words'}},
            explanation={'en': 'Accurate sorting of target sight word GO!', 'ar': 'فرز دقيق للكلمة البصرية المستهدفة GO!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.word.mc_stop_sign',
            objective_key='obj.lit.target_word_among_distractors',
            subject_code='literacy',
            unit_code='unit.lit.word_recognition',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which word appears on a red traffic stop sign?', 'ar': 'أي كلمة تظهر على إشارة التوقف المرورية الحمراء؟'},
            content_payload={'question': 'Which word appears on a red traffic stop sign?', 'options': [{'id': 'ans_stop', 'text': 'STOP 🛑', 'visual_cue': 'STOP', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_step', 'text': 'STEP', 'visual_cue': 'STEP', 'is_correct': False, 'distractor_rationale': 'Middle letter is E'}, {'id': 'ans_shop', 'text': 'SHOP', 'visual_cue': 'SHOP', 'is_correct': False, 'distractor_rationale': 'Starts with SH'}], 'correct_answer_id': 'ans_stop', 'explanation': 'Spot on! The red octagon says STOP.'},
            correct_answer={'correct_answer_id': 'ans_stop'},
            explanation={'en': 'Spot on! The red octagon says STOP.', 'ar': 'صحيح! الإشارة الحمراء مكتوب عليها STOP.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.word.mc_repeat_dog',
            objective_key='obj.lit.recognize_repeated_words',
            subject_code='literacy',
            unit_code='unit.lit.word_recognition',
            difficulty_level=3,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': "In the phrase 'A dog and a dog', which word is repeated?", 'ar': "في عبارة 'A dog and a dog'، أي كلمة تكررت؟"},
            content_payload={'question': "In the phrase 'A dog and a dog', which word is repeated?", 'options': [{'id': 'ans_dog', 'text': 'dog', 'visual_cue': 'dog', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_and', 'text': 'and', 'visual_cue': 'and', 'is_correct': False, 'distractor_rationale': 'Appears only once'}, {'id': 'ans_a', 'text': 'the', 'visual_cue': 'the', 'is_correct': False, 'distractor_rationale': 'Not in the sentence'}], 'correct_answer_id': 'ans_dog', 'explanation': "Correct! 'dog' appears twice in the phrase."},
            correct_answer={'correct_answer_id': 'ans_dog'},
            explanation={'en': "Correct! 'dog' appears twice in the phrase.", 'ar': "صحيح! كلمة 'dog' تظهر مرتين في العبارة."},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.word.vis_repeat_look',
            objective_key='obj.lit.recognize_repeated_words',
            subject_code='literacy',
            unit_code='unit.lit.word_recognition',
            difficulty_level=3,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': "Spot the repeated word 'LOOK' in the rhyme sentence: 'Look up, look down'.", 'ar': "حدد الكلمة المكررة 'LOOK' في جملة: 'Look up, look down'."},
            content_payload={'prompt': "Spot the repeated word 'LOOK' in the rhyme sentence: 'Look up, look down'.", 'scene_description': 'A nursery rhyme poster on the classroom wall.', 'elements': [{'id': 'ph_up', 'label': "Word 'up'", 'category': 'word', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'ph_look', 'label': "Repeated Word 'Look'", 'category': 'word', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'ph_down', 'label': "Word 'down'", 'category': 'word', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'ph_look', 'feedback_clue': 'Look for the action word that repeats at the start of both phrases.'},
            correct_answer={'target_id': 'ph_look'},
            explanation={'en': "Super! 'Look' repeats twice.", 'ar': "ممتاز! كلمة 'Look' تكررت مرتين."},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.word.match_repeated_phrases',
            objective_key='obj.lit.recognize_repeated_words',
            subject_code='literacy',
            unit_code='unit.lit.word_recognition',
            difficulty_level=3,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each short phrase to the word that repeats within it.', 'ar': 'طابق كل عبارة قصيرة بالكلمة التي تتكرر فيها.'},
            content_payload={'prompt': 'Match each short phrase to the word that repeats within it.', 'left_items': [{'id': 'ph_run_run', 'label': "'Run, run, fast!'", 'visual_cue': 'Run, run'}, {'id': 'ph_jump_jump', 'label': "'Jump and jump!'", 'visual_cue': 'Jump and jump'}], 'right_items': [{'id': 'rw_run', 'label': 'Repeated: RUN', 'visual_cue': 'RUN'}, {'id': 'rw_jump', 'label': 'Repeated: JUMP', 'visual_cue': 'JUMP'}], 'pairs': [{'left_id': 'ph_run_run', 'right_id': 'rw_run'}, {'left_id': 'ph_jump_jump', 'right_id': 'rw_jump'}]},
            correct_answer={'pairs': [{'left_id': 'ph_run_run', 'right_id': 'rw_run'}, {'left_id': 'ph_jump_jump', 'right_id': 'rw_jump'}]},
            explanation={'en': 'Great matching of repeated words in phrases!', 'ar': 'مطابقة رائعة للكلمات المكررة في العبارات!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.word.drag.sort_has_repeat',
            objective_key='obj.lit.recognize_repeated_words',
            subject_code='literacy',
            unit_code='unit.lit.word_recognition',
            difficulty_level=3,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort phrases into 'Has Repeated Word' and 'No Repeated Words'.", 'ar': "صنف العبارات إلى 'تحتوي على كلمة مكررة' و 'بدون كلمات مكررة'."},
            content_payload={'prompt': "Sort phrases into 'Has Repeated Word' and 'No Repeated Words'.", 'items': [{'id': 'ph_byebye', 'label': "'Bye, bye!'", 'visual_cue': 'Bye, bye'}, {'id': 'ph_gogo', 'label': "'Go, go, go!'", 'visual_cue': 'Go, go, go'}, {'id': 'ph_sunshine', 'label': "'I see sun'", 'visual_cue': 'I see sun'}, {'id': 'ph_bigcat', 'label': "'Big red cat'", 'visual_cue': 'Big red cat'}], 'zones': [{'id': 'z_has_rep', 'label': 'Has Repeated Word', 'capacity': 3}, {'id': 'z_no_rep', 'label': 'No Repeated Words', 'capacity': 3}], 'correct_mapping': {'ph_byebye': 'z_has_rep', 'ph_gogo': 'z_has_rep', 'ph_sunshine': 'z_no_rep', 'ph_bigcat': 'z_no_rep'}},
            correct_answer={'correct_mapping': {'ph_byebye': 'z_has_rep', 'ph_gogo': 'z_has_rep', 'ph_sunshine': 'z_no_rep', 'ph_bigcat': 'z_no_rep'}},
            explanation={'en': 'Terrific sorting of repetitive word patterns!', 'ar': 'فرز رائع لأنماط الكلمات المتكررة!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.word.mc_repeat_yes',
            objective_key='obj.lit.recognize_repeated_words',
            subject_code='literacy',
            unit_code='unit.lit.word_recognition',
            difficulty_level=3,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': "Which word appears twice in: 'Yes, yes, I can'?", 'ar': "أي كلمة تظهر مرتين في: 'Yes, yes, I can'؟"},
            content_payload={'question': "Which word appears twice in: 'Yes, yes, I can'?", 'options': [{'id': 'ans_yes', 'text': 'YES', 'visual_cue': 'YES', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_i', 'text': 'I', 'visual_cue': 'I', 'is_correct': False, 'distractor_rationale': 'Appears once'}, {'id': 'ans_can', 'text': 'CAN', 'visual_cue': 'CAN', 'is_correct': False, 'distractor_rationale': 'Appears once'}], 'correct_answer_id': 'ans_yes', 'explanation': "Spot on! The word 'Yes' is repeated at the start."},
            correct_answer={'correct_answer_id': 'ans_yes'},
            explanation={'en': "Spot on! The word 'Yes' is repeated at the start.", 'ar': "صحيح! كلمة 'Yes' مكررة في البداية."},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.seq.mc_socks_shoes',
            objective_key='obj.lit.order_two_events',
            subject_code='literacy',
            unit_code='unit.lit.sequencing_comprehension',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'What do you put on FIRST: your socks or your shoes?', 'ar': 'ماذا ترتدي أولاً: الجوارب أم الحذاء؟'},
            content_payload={'question': 'What do you put on FIRST: your socks or your shoes?', 'options': [{'id': 'ans_socks', 'text': 'Put on socks 🧦', 'visual_cue': '🧦', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_shoes', 'text': 'Put on shoes 👟', 'visual_cue': '👟', 'is_correct': False, 'distractor_rationale': 'Shoes go on after socks'}], 'correct_answer_id': 'ans_socks', 'explanation': 'Correct! Socks go on first, then shoes.'},
            correct_answer={'correct_answer_id': 'ans_socks'},
            explanation={'en': 'Correct! Socks go on first, then shoes.', 'ar': 'صحيح! نرتدي الجوارب أولاً ثم الحذاء.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.seq.order.wake_eat_school',
            objective_key='obj.lit.order_two_events',
            subject_code='literacy',
            unit_code='unit.lit.sequencing_comprehension',
            difficulty_level=2,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Order the morning sequence from start to finish.', 'ar': 'رتب تسلسل الصباح من البداية إلى النهاية.'},
            content_payload={'prompt': 'Order the morning sequence from start to finish.', 'items': [{'id': 'st_eat', 'label': 'Eat Breakfast 🥣', 'visual_cue': 'breakfast'}, {'id': 'st_wake', 'label': 'Wake Up ⏰', 'visual_cue': 'wake up'}, {'id': 'st_school', 'label': 'Go to School 🏫', 'visual_cue': 'school'}], 'correct_sequence': ['st_wake', 'st_eat', 'st_school'], 'direction': 'chronological'},
            correct_answer={'correct_sequence': ['st_wake', 'st_eat', 'st_school']},
            explanation={'en': 'Great morning sequence! Wake up, eat, go to school.', 'ar': 'تسلسل صباحي رائع! استيقاظ، إفطار، ذهاب للمدرسة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.seq.match.cause_effect',
            objective_key='obj.lit.order_two_events',
            subject_code='literacy',
            unit_code='unit.lit.sequencing_comprehension',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match what happens First to what happens Next.', 'ar': 'طابق ما يحدث أولاً بما يحدث تالياً.'},
            content_payload={'prompt': 'Match what happens First to what happens Next.', 'left_items': [{'id': 'f_rain', 'label': 'First: Rain falls 🌧️', 'visual_cue': 'rain'}, {'id': 'f_seed', 'label': 'First: Plant seed 🌱', 'visual_cue': 'seed'}], 'right_items': [{'id': 'n_puddle', 'label': 'Next: Water puddles form 💧', 'visual_cue': 'puddle'}, {'id': 'n_sprout', 'label': 'Next: Flower grows 🌸', 'visual_cue': 'flower'}], 'pairs': [{'left_id': 'f_rain', 'right_id': 'n_puddle'}, {'left_id': 'f_seed', 'right_id': 'n_sprout'}]},
            correct_answer={'pairs': [{'left_id': 'f_rain', 'right_id': 'n_puddle'}, {'left_id': 'f_seed', 'right_id': 'n_sprout'}]},
            explanation={'en': 'Super event sequence matching!', 'ar': 'مطابقة ممتازة لتسلسل الأحداث!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.seq.vis_first_cake_step',
            objective_key='obj.lit.order_two_events',
            subject_code='literacy',
            unit_code='unit.lit.sequencing_comprehension',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the picture showing the FIRST step of baking a cake.', 'ar': 'حدد الصورة التي تظهر الخطوة الأولى في خبز الكعكة.'},
            content_payload={'prompt': 'Spot the picture showing the FIRST step of baking a cake.', 'scene_description': 'A kitchen storyboard with three baking stages.', 'elements': [{'id': 'bk_mix', 'label': 'Mixing the Batter in Bowl 🥣', 'category': 'step', 'is_target': True, 'bounding_hint': 'left'}, {'id': 'bk_oven', 'label': 'Baking in Oven 🔥', 'category': 'step', 'is_target': False, 'bounding_hint': 'center'}, {'id': 'bk_eat', 'label': 'Eating a Slice 🍰', 'category': 'step', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'bk_mix', 'feedback_clue': 'First we mix ingredients in the bowl before baking.'},
            correct_answer={'target_id': 'bk_mix'},
            explanation={'en': 'Wonderful! Mixing ingredients is step one.', 'ar': 'رائع! خلط المكونات هو الخطوة الأولى.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.seq.drag.sort_first_next',
            objective_key='obj.lit.order_two_events',
            subject_code='literacy',
            unit_code='unit.lit.sequencing_comprehension',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort actions into 'Happens First' and 'Happens Next'.", 'ar': "صنف الأفعال إلى 'يحدث أولاً' و 'يحدث تالياً'."},
            content_payload={'prompt': "Sort actions into 'Happens First' and 'Happens Next'.", 'items': [{'id': 'act_wash', 'label': 'Wash hands with soap 🧼', 'visual_cue': 'wash hands'}, {'id': 'act_dry', 'label': 'Dry hands with clean towel 🧻', 'visual_cue': 'dry hands'}, {'id': 'act_cook', 'label': 'Cook dinner in pot 🍲', 'visual_cue': 'cook'}, {'id': 'act_eat_dinner', 'label': 'Eat the cooked dinner 🍽️', 'visual_cue': 'eat'}], 'zones': [{'id': 'z_first', 'label': 'Happens First', 'capacity': 3}, {'id': 'z_next', 'label': 'Happens Next', 'capacity': 3}], 'correct_mapping': {'act_wash': 'z_first', 'act_dry': 'z_next', 'act_cook': 'z_first', 'act_eat_dinner': 'z_next'}},
            correct_answer={'correct_mapping': {'act_wash': 'z_first', 'act_dry': 'z_next', 'act_cook': 'z_first', 'act_eat_dinner': 'z_next'}},
            explanation={'en': 'Terrific chronological sorting!', 'ar': 'فرز زمني رائع!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.seq.order.sandwich',
            objective_key='obj.lit.order_three_events',
            subject_code='literacy',
            unit_code='unit.lit.sequencing_comprehension',
            difficulty_level=3,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Order the steps to make a sandwich from start to finish.', 'ar': 'رتب خطوات صنع الشطيرة من البداية إلى النهاية.'},
            content_payload={'prompt': 'Order the steps to make a sandwich from start to finish.', 'items': [{'id': 'sw_spread', 'label': 'Spread jelly on bread 🍓', 'visual_cue': 'spread'}, {'id': 'sw_bread', 'label': 'Get two slices of bread 🍞', 'visual_cue': 'bread'}, {'id': 'sw_eat', 'label': 'Take a big bite 🥪', 'visual_cue': 'eat'}], 'correct_sequence': ['sw_bread', 'sw_spread', 'sw_eat'], 'direction': 'chronological'},
            correct_answer={'correct_sequence': ['sw_bread', 'sw_spread', 'sw_eat']},
            explanation={'en': 'Awesome! Bread first, spread next, eat last.', 'ar': 'رائع! الخبز أولاً، ثم المربى، ثم الأكل.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.seq.order.bedtime',
            objective_key='obj.lit.order_three_events',
            subject_code='literacy',
            unit_code='unit.lit.sequencing_comprehension',
            difficulty_level=3,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Sequence the bedtime routine in order.', 'ar': 'رتب روتين ما قبل النوم بالترتيب.'},
            content_payload={'prompt': 'Sequence the bedtime routine in order.', 'items': [{'id': 'bt_teeth', 'label': 'Brush teeth 🪥', 'visual_cue': 'brush teeth'}, {'id': 'bt_pajamas', 'label': 'Put on cozy pajamas 👕', 'visual_cue': 'pajamas'}, {'id': 'bt_sleep', 'label': 'Get into bed and sleep 🛏️', 'visual_cue': 'sleep'}], 'correct_sequence': ['bt_pajamas', 'bt_teeth', 'bt_sleep'], 'direction': 'chronological'},
            correct_answer={'correct_sequence': ['bt_pajamas', 'bt_teeth', 'bt_sleep']},
            explanation={'en': 'Great bedtime sequence!', 'ar': 'تسلسل وقت النوم رائع!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.seq.mc_caterpillar_middle',
            objective_key='obj.lit.order_three_events',
            subject_code='literacy',
            unit_code='unit.lit.sequencing_comprehension',
            difficulty_level=3,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'In a butterfly story (Egg -> Caterpillar -> Butterfly), what is the MIDDLE stage?', 'ar': 'في قصة الفراشة (بيضة -> يرقة -> فراشة)، ما هي المرحلة الوسطى؟'},
            content_payload={'question': 'In a butterfly story (Egg -> Caterpillar -> Butterfly), what is the MIDDLE stage?', 'options': [{'id': 'ans_catp', 'text': 'Caterpillar 🐛', 'visual_cue': '🐛', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_egg', 'text': 'Tiny Egg 🥚', 'visual_cue': '🥚', 'is_correct': False, 'distractor_rationale': 'First stage'}, {'id': 'ans_fly', 'text': 'Flying Butterfly 🦋', 'visual_cue': '🦋', 'is_correct': False, 'distractor_rationale': 'Final stage'}], 'correct_answer_id': 'ans_catp', 'explanation': 'Correct! Caterpillar is the middle stage.'},
            correct_answer={'correct_answer_id': 'ans_catp'},
            explanation={'en': 'Correct! Caterpillar is the middle stage.', 'ar': 'صحيح! اليرقة هي المرحلة الوسطى.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.seq.drag.sort_beginning_end',
            objective_key='obj.lit.order_three_events',
            subject_code='literacy',
            unit_code='unit.lit.sequencing_comprehension',
            difficulty_level=3,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort story stages into 'Beginning' and 'Ending'.", 'ar': "صنف مراحل القصة إلى 'البداية' و 'النهاية'."},
            content_payload={'prompt': "Sort story stages into 'Beginning' and 'Ending'.", 'items': [{'id': 'st_seed', 'label': 'Planting seed in pot 🌱', 'visual_cue': 'seed'}, {'id': 'st_start_run', 'label': 'Standing at starting line 🏁', 'visual_cue': 'start line'}, {'id': 'st_flower', 'label': 'Beautiful flower blooms 🌸', 'visual_cue': 'flower'}, {'id': 'st_finish_ribbon', 'label': 'Crossing finish ribbon 🏆', 'visual_cue': 'trophy'}], 'zones': [{'id': 'z_begin', 'label': 'Beginning Stage', 'capacity': 3}, {'id': 'z_ending', 'label': 'Ending Stage', 'capacity': 3}], 'correct_mapping': {'st_seed': 'z_begin', 'st_start_run': 'z_begin', 'st_flower': 'z_ending', 'st_finish_ribbon': 'z_ending'}},
            correct_answer={'correct_mapping': {'st_seed': 'z_begin', 'st_start_run': 'z_begin', 'st_flower': 'z_ending', 'st_finish_ribbon': 'z_ending'}},
            explanation={'en': 'Terrific identification of story beginnings and endings!', 'ar': 'تمييز رائع لبدايات ونهايات القصص!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.seq.mc_first_wash',
            objective_key='obj.lit.identify_first_event',
            subject_code='literacy',
            unit_code='unit.lit.sequencing_comprehension',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Before applying soap to wash hands, what do you do FIRST?', 'ar': 'قبل وضع الصابون لغسل اليدين، ماذا تفعل أولاً؟'},
            content_payload={'question': 'Before applying soap to wash hands, what do you do FIRST?', 'options': [{'id': 'ans_wet', 'text': 'Wet hands with clean water 💧', 'visual_cue': '💧', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_dry', 'text': 'Dry hands on a towel 🧻', 'visual_cue': '🧻', 'is_correct': False, 'distractor_rationale': 'Drying happens at the very end'}], 'correct_answer_id': 'ans_wet', 'explanation': 'Correct! You wet your hands with water first.'},
            correct_answer={'correct_answer_id': 'ans_wet'},
            explanation={'en': 'Correct! You wet your hands with water first.', 'ar': 'صحيح! تبلل يديك بالماء أولاً.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.seq.vis_first_garden',
            objective_key='obj.lit.identify_first_event',
            subject_code='literacy',
            unit_code='unit.lit.sequencing_comprehension',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the picture showing what you do FIRST when planting.', 'ar': 'حدد الصورة التي تظهر ما تفعله أولاً عند الزراعة.'},
            content_payload={'prompt': 'Spot the picture showing what you do FIRST when planting.', 'scene_description': 'A garden illustration showing three stages.', 'elements': [{'id': 'gd_dig', 'label': 'Digging a hole in soil 🌱', 'category': 'action', 'is_target': True, 'bounding_hint': 'left'}, {'id': 'gd_water', 'label': 'Watering with can 🚿', 'category': 'action', 'is_target': False, 'bounding_hint': 'center'}, {'id': 'gd_pick', 'label': 'Picking flowers 💐', 'category': 'action', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'gd_dig', 'feedback_clue': 'Look for preparing the ground before watering or picking.'},
            correct_answer={'target_id': 'gd_dig'},
            explanation={'en': 'Super! Digging the soil comes first.', 'ar': 'ممتاز! حفر التربة يأتي أولاً.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.seq.match.first_actions',
            objective_key='obj.lit.identify_first_event',
            subject_code='literacy',
            unit_code='unit.lit.sequencing_comprehension',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each activity to its very FIRST action.', 'ar': 'طابق كل نشاط بفعله الأول تماماً.'},
            content_payload={'prompt': 'Match each activity to its very FIRST action.', 'left_items': [{'id': 'act_book', 'label': 'Reading a Book 📖', 'visual_cue': 'reading'}, {'id': 'act_sleep', 'label': 'Going to Sleep 🛏️', 'visual_cue': 'sleeping'}], 'right_items': [{'id': 'fst_open', 'label': 'Open the front cover', 'visual_cue': 'open cover'}, {'id': 'fst_eyes', 'label': 'Close your eyes', 'visual_cue': 'close eyes'}], 'pairs': [{'left_id': 'act_book', 'right_id': 'fst_open'}, {'left_id': 'act_sleep', 'right_id': 'fst_eyes'}]},
            correct_answer={'pairs': [{'left_id': 'act_book', 'right_id': 'fst_open'}, {'left_id': 'act_sleep', 'right_id': 'fst_eyes'}]},
            explanation={'en': 'Great first event matching!', 'ar': 'مطابقة رائعة للحدث الأول!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.seq.mc_first_morning',
            objective_key='obj.lit.identify_first_event',
            subject_code='literacy',
            unit_code='unit.lit.sequencing_comprehension',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'In the morning, what happens FIRST?', 'ar': 'في الصباح، ما الذي يحدث أولاً؟'},
            content_payload={'question': 'In the morning, what happens FIRST?', 'options': [{'id': 'ans_wake', 'text': 'Opening your eyes and waking up ☀️', 'visual_cue': 'wake', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_school', 'text': 'Arriving at school 🏫', 'visual_cue': 'school', 'is_correct': False, 'distractor_rationale': 'School happens later in the day'}], 'correct_answer_id': 'ans_wake', 'explanation': 'Super! Waking up is the very first event of the morning.'},
            correct_answer={'correct_answer_id': 'ans_wake'},
            explanation={'en': 'Super! Waking up is the very first event of the morning.', 'ar': 'ممتاز! الاستيقاظ هو الحدث الأول في الصباح.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.seq.drag.sort_first_later',
            objective_key='obj.lit.identify_first_event',
            subject_code='literacy',
            unit_code='unit.lit.sequencing_comprehension',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort actions into 'Happens First' and 'Happens Later'.", 'ar': "صنف الأفعال إلى 'يحدث أولاً' و 'يحدث لاحقاً'."},
            content_payload={'prompt': "Sort actions into 'Happens First' and 'Happens Later'.", 'items': [{'id': 'e_put_coat', 'label': 'Put on winter coat 🧥', 'visual_cue': 'coat'}, {'id': 'e_zip_coat', 'label': 'Zip up the coat 🤐', 'visual_cue': 'zip'}, {'id': 'e_open_box', 'label': 'Open lunchbox 🍱', 'visual_cue': 'open box'}, {'id': 'e_eat_sandwich', 'label': 'Eat sandwich 🥪', 'visual_cue': 'eat'}], 'zones': [{'id': 'z_fst', 'label': 'Happens First', 'capacity': 3}, {'id': 'z_ltr', 'label': 'Happens Later', 'capacity': 3}], 'correct_mapping': {'e_put_coat': 'z_fst', 'e_open_box': 'z_fst', 'e_zip_coat': 'z_ltr', 'e_eat_sandwich': 'z_ltr'}},
            correct_answer={'correct_mapping': {'e_put_coat': 'z_fst', 'e_open_box': 'z_fst', 'e_zip_coat': 'z_ltr', 'e_eat_sandwich': 'z_ltr'}},
            explanation={'en': 'Terrific identification of initial events!', 'ar': 'تمييز رائع للأحداث الأولى!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.seq.mc_next_wash',
            objective_key='obj.lit.identify_next_event',
            subject_code='literacy',
            unit_code='unit.lit.sequencing_comprehension',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'You rinse the soap off your hands. What do you do NEXT?', 'ar': 'شطفت الصابون عن يديك. ماذا تفعل تالياً؟'},
            content_payload={'question': 'You rinse the soap off your hands. What do you do NEXT?', 'options': [{'id': 'ans_dry_towel', 'text': 'Dry hands with a clean towel 🧻', 'visual_cue': '🧻', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_mud', 'text': 'Put hands in mud 泥', 'visual_cue': '❌', 'is_correct': False, 'distractor_rationale': 'Hands are clean now'}], 'correct_answer_id': 'ans_dry_towel', 'explanation': 'Correct! Next, dry your clean hands with a towel.'},
            correct_answer={'correct_answer_id': 'ans_dry_towel'},
            explanation={'en': 'Correct! Next, dry your clean hands with a towel.', 'ar': 'صحيح! تالياً، جفف يديك النظيفتين بمنشفة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.seq.vis_next_winter',
            objective_key='obj.lit.identify_next_event',
            subject_code='literacy',
            unit_code='unit.lit.sequencing_comprehension',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot what comes NEXT after putting on your winter boots: putting on gloves 🧤.', 'ar': 'حدد ما يأتي تالياً بعد ارتداء حذاء الشتاء: ارتداء القفازات 🧤.'},
            content_payload={'prompt': 'Spot what comes NEXT after putting on your winter boots: putting on gloves 🧤.', 'scene_description': 'A hallway coat rack scene.', 'elements': [{'id': 'it_gloves', 'label': 'Warm Winter Gloves 🧤', 'category': 'gear', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'it_sunglasses', 'label': 'Sunglasses 🕶️', 'category': 'gear', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'it_swimsuit', 'label': 'Swimsuit 🩱', 'category': 'gear', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'it_gloves', 'feedback_clue': 'Look for the warm gloves for cold winter weather.'},
            correct_answer={'target_id': 'it_gloves'},
            explanation={'en': 'Wonderful! Next step is putting on warm gloves.', 'ar': 'رائع! الخطوة التالية هي ارتداء القفازات الدافئة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.seq.match.next_steps',
            objective_key='obj.lit.identify_next_event',
            subject_code='literacy',
            unit_code='unit.lit.sequencing_comprehension',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match current step to what happens NEXT.', 'ar': 'طابق الخطوة الحالية بما يحدث تالياً.'},
            content_payload={'prompt': 'Match current step to what happens NEXT.', 'left_items': [{'id': 'cur_turn_page', 'label': 'Finished reading page', 'visual_cue': 'finish page'}, {'id': 'cur_arrive_bus', 'label': 'School bus stops at school', 'visual_cue': 'bus stops'}], 'right_items': [{'id': 'nxt_turn', 'label': 'Turn to the next page', 'visual_cue': 'turn page'}, {'id': 'nxt_walk', 'label': 'Walk into the classroom', 'visual_cue': 'walk in'}], 'pairs': [{'left_id': 'cur_turn_page', 'right_id': 'nxt_turn'}, {'left_id': 'cur_arrive_bus', 'right_id': 'nxt_walk'}]},
            correct_answer={'pairs': [{'left_id': 'cur_turn_page', 'right_id': 'nxt_turn'}, {'left_id': 'cur_arrive_bus', 'right_id': 'nxt_walk'}]},
            explanation={'en': 'Terrific matching of logical next steps!', 'ar': 'مطابقة رائعة للخطوات التالية المنطقية!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.seq.mc_next_open_book',
            objective_key='obj.lit.identify_next_event',
            subject_code='literacy',
            unit_code='unit.lit.sequencing_comprehension',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'You sit down and open your favorite book. What do you do NEXT?', 'ar': 'جلست وفتحت كتابك المفضل. ماذا تفعل تالياً؟'},
            content_payload={'question': 'You sit down and open your favorite book. What do you do NEXT?', 'options': [{'id': 'ans_read', 'text': 'Read the story 📖', 'visual_cue': 'read', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_close', 'text': 'Close the book and put it away', 'visual_cue': 'close', 'is_correct': False, 'distractor_rationale': 'You just opened it to read'}], 'correct_answer_id': 'ans_read', 'explanation': 'Spot on! Next, you read the story.'},
            correct_answer={'correct_answer_id': 'ans_read'},
            explanation={'en': 'Spot on! Next, you read the story.', 'ar': 'صحيح! تالياً، تقرأ القصة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.seq.drag.sort_current_next',
            objective_key='obj.lit.identify_next_event',
            subject_code='literacy',
            unit_code='unit.lit.sequencing_comprehension',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort sequence cards into 'Current Step' and 'Next Step'.", 'ar': "صنف بطاقات التسلسل إلى 'الخطوة الحالية' و 'الخطوة التالية'."},
            content_payload={'prompt': "Sort sequence cards into 'Current Step' and 'Next Step'.", 'items': [{'id': 'c_put_toothpaste', 'label': 'Put paste on brush 🪥', 'visual_cue': 'paste'}, {'id': 'c_scrub_teeth', 'label': 'Brush teeth gently 😁', 'visual_cue': 'brush'}, {'id': 'c_ring_doorbell', 'label': 'Ring the doorbell 🔔', 'visual_cue': 'bell'}, {'id': 'c_open_door', 'label': 'Friend opens the door 🚪', 'visual_cue': 'door'}], 'zones': [{'id': 'z_cur', 'label': 'Current Step', 'capacity': 3}, {'id': 'z_nxt', 'label': 'Next Step', 'capacity': 3}], 'correct_mapping': {'c_put_toothpaste': 'z_cur', 'c_scrub_teeth': 'z_nxt', 'c_ring_doorbell': 'z_cur', 'c_open_door': 'z_nxt'}},
            correct_answer={'correct_mapping': {'c_put_toothpaste': 'z_cur', 'c_scrub_teeth': 'z_nxt', 'c_ring_doorbell': 'z_cur', 'c_open_door': 'z_nxt'}},
            explanation={'en': 'Super! You identified immediate next steps.', 'ar': 'ممتاز! حددت الخطوات التالية المباشرة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.seq.mc_sentence_dog_running',
            objective_key='obj.lit.match_sentence_to_image',
            subject_code='literacy',
            unit_code='unit.lit.sequencing_comprehension',
            difficulty_level=3,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which sentence matches the picture of a dog running: 🐕 🏃?', 'ar': 'أي جملة تطابق صورة الكلب الذي يجري: 🐕 🏃؟'},
            content_payload={'question': 'Which sentence matches the picture of a dog running: 🐕 🏃?', 'options': [{'id': 'sent_dog_run', 'text': 'The dog is running.', 'visual_cue': '🐕 🏃', 'is_correct': True, 'distractor_rationale': None}, {'id': 'sent_cat_sleep', 'text': 'The cat is sleeping.', 'visual_cue': '🐱 💤', 'is_correct': False, 'distractor_rationale': 'Picture shows a running dog'}, {'id': 'sent_bird_fly', 'text': 'The bird is flying.', 'visual_cue': '🐦 ☁️', 'is_correct': False, 'distractor_rationale': 'Picture shows a dog'}], 'correct_answer_id': 'sent_dog_run', 'explanation': "Correct! 'The dog is running' matches the picture."},
            correct_answer={'correct_answer_id': 'sent_dog_run'},
            explanation={'en': "Correct! 'The dog is running' matches the picture.", 'ar': "صحيح! 'The dog is running' تطابق الصورة."},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.seq.match.sentences_pictures',
            objective_key='obj.lit.match_sentence_to_image',
            subject_code='literacy',
            unit_code='unit.lit.sequencing_comprehension',
            difficulty_level=3,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each simple sentence to its picture.', 'ar': 'طابق كل جملة بسيطة بصورتها.'},
            content_payload={'prompt': 'Match each simple sentence to its picture.', 'left_items': [{'id': 's_sun', 'label': "'The sun is bright.'", 'visual_cue': 'sun sentence'}, {'id': 's_book', 'label': "'The boy reads a book.'", 'visual_cue': 'book sentence'}], 'right_items': [{'id': 'p_sun_bright', 'label': 'Shining Sun ☀️', 'visual_cue': '☀️'}, {'id': 'p_boy_reading', 'label': 'Boy Reading 👦📖', 'visual_cue': '👦📖'}], 'pairs': [{'left_id': 's_sun', 'right_id': 'p_sun_bright'}, {'left_id': 's_book', 'right_id': 'p_boy_reading'}]},
            correct_answer={'pairs': [{'left_id': 's_sun', 'right_id': 'p_sun_bright'}, {'left_id': 's_book', 'right_id': 'p_boy_reading'}]},
            explanation={'en': 'Great comprehension matching! Sentences connect to visuals.', 'ar': 'مطابقة فهم ممتازة! ترتبط الجمل بالصور.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.seq.vis_sentence_red_bird',
            objective_key='obj.lit.match_sentence_to_image',
            subject_code='literacy',
            unit_code='unit.lit.sequencing_comprehension',
            difficulty_level=3,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': "Find the illustration matching: 'The red bird sits in the tree.'", 'ar': "حدد الرسم التوضيحي المطابق لـ: 'The red bird sits in the tree.'"},
            content_payload={'prompt': "Find the illustration matching: 'The red bird sits in the tree.'", 'scene_description': 'Three garden pictures in frames.', 'elements': [{'id': 'pic_blue_fish', 'label': 'Blue fish swimming in pond', 'category': 'scene', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'pic_red_bird', 'label': 'Red bird sitting in green tree 🐦🌲', 'category': 'scene', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'pic_yellow_cat', 'label': 'Yellow cat napping on rug', 'category': 'scene', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'pic_red_bird', 'feedback_clue': 'Look for the red bird in the tree.'},
            correct_answer={'target_id': 'pic_red_bird'},
            explanation={'en': 'Wonderful reading comprehension! Red bird in the tree.', 'ar': 'فهم قرائي رائع! طائر أحمر في الشجرة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.seq.mc_girl_eats_apple',
            objective_key='obj.lit.match_sentence_to_image',
            subject_code='literacy',
            unit_code='unit.lit.sequencing_comprehension',
            difficulty_level=3,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': "Which picture matches: 'The girl is eating an apple' 👧 🍎?", 'ar': "أي صورة تطابق: 'The girl is eating an apple' 👧 🍎؟"},
            content_payload={'question': "Which picture matches: 'The girl is eating an apple' 👧 🍎?", 'options': [{'id': 'pic_girl_apple', 'text': 'Girl eating a crunchy red apple 👧🍎', 'visual_cue': '👧🍎', 'is_correct': True, 'distractor_rationale': None}, {'id': 'pic_boy_bike', 'text': 'Boy riding a blue bicycle 👦🚲', 'visual_cue': '👦🚲', 'is_correct': False, 'distractor_rationale': 'Different person and action'}, {'id': 'pic_cat_ball', 'text': 'Cat playing with yarn ball 🐱🧶', 'visual_cue': '🐱🧶', 'is_correct': False, 'distractor_rationale': 'Shows an animal playing'}], 'correct_answer_id': 'pic_girl_apple', 'explanation': 'Spot on! That picture depicts the girl eating an apple.'},
            correct_answer={'correct_answer_id': 'pic_girl_apple'},
            explanation={'en': 'Spot on! That picture depicts the girl eating an apple.', 'ar': 'صحيح! تلك الصورة تظهر الفتاة تأكل تفاحة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='lit.seq.drag.sort_sentence_pics',
            objective_key='obj.lit.match_sentence_to_image',
            subject_code='literacy',
            unit_code='unit.lit.sequencing_comprehension',
            difficulty_level=3,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': 'Drag each picture under its matching sentence caption.', 'ar': 'اسحب كل صورة تحت تعليق الجملة المطابق لها.'},
            content_payload={'prompt': 'Drag each picture under its matching sentence caption.', 'items': [{'id': 'dp_star', 'label': 'Night Star Picture ⭐🌙', 'visual_cue': 'star picture'}, {'id': 'dp_boat', 'label': 'Sea Boat Picture ⛵🌊', 'visual_cue': 'boat picture'}], 'zones': [{'id': 'cap_star', 'label': "'Stars shine in the sky.'", 'capacity': 1}, {'id': 'cap_boat', 'label': "'The boat sails on water.'", 'capacity': 1}], 'correct_mapping': {'dp_star': 'cap_star', 'dp_boat': 'cap_boat'}},
            correct_answer={'correct_mapping': {'dp_star': 'cap_star', 'dp_boat': 'cap_boat'}},
            explanation={'en': 'Terrific reading and picture comprehension!', 'ar': 'فهم قرائي وبصري رائع!'},
            hints=[],
            metadata_info={},
        )
    )
    return items
