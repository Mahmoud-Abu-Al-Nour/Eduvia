"""
Eduvia — Expanded Mathematics Content Bank Items

Provides authoritative educational items for all 31 mathematics objectives,
ensuring complete coverage across all 5 activity modalities.
"""
from __future__ import annotations

from app.activities.schemas import ActivityType
from app.content.definitions import ContentItemDef

def get_expanded_math_items() -> list[ContentItemDef]:
    items: list[ContentItemDef] = []
    items.append(
        ContentItemDef(
            content_key='math.cnt610.vis.num8',
            objective_key='obj.math.count_6_10',
            subject_code='math',
            unit_code='unit.math.number_sense',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Find the numeral 8 on the chalkboard.', 'ar': 'ابحث عن الرقم ٨ على السبورة.'},
            content_payload={'prompt': 'Find the numeral 8 on the chalkboard.', 'scene_description': 'A classroom chalkboard with numerals.', 'elements': [{'id': 'c_6', 'label': 'Numeral 6', 'category': 'number', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'c_8', 'label': 'Numeral 8', 'category': 'number', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'c_10', 'label': 'Numeral 10', 'category': 'number', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'c_8', 'feedback_clue': 'Look for the number with two stacked circles.'},
            correct_answer={'target_id': 'c_8'},
            explanation={'en': 'Super! That is numeral 8.', 'ar': 'ممتاز! هذا هو الرقم ٨.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.cnt610.drag.sort_6_and_9',
            objective_key='obj.math.count_6_10',
            subject_code='math',
            unit_code='unit.math.number_sense',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort the representations into 'Group 6' and 'Group 9'.", 'ar': "صنف التمثيلات إلى 'المجموعة ٦' و 'المجموعة ٩'."},
            content_payload={'prompt': "Sort the representations into 'Group 6' and 'Group 9'.", 'items': [{'id': 'num_6', 'label': 'Numeral 6 6️⃣', 'visual_cue': '6️⃣'}, {'id': 'dots_6', 'label': '6 Dots 🔵x6', 'visual_cue': '🔵x6'}, {'id': 'num_9', 'label': 'Numeral 9 9️⃣', 'visual_cue': '9️⃣'}, {'id': 'dots_9', 'label': '9 Dots 🟡x9', 'visual_cue': '🟡x9'}], 'zones': [{'id': 'z_6', 'label': 'Group 6', 'capacity': 3}, {'id': 'z_9', 'label': 'Group 9', 'capacity': 3}], 'correct_mapping': {'num_6': 'z_6', 'dots_6': 'z_6', 'num_9': 'z_9', 'dots_9': 'z_9'}},
            correct_answer={'correct_mapping': {'num_6': 'z_6', 'dots_6': 'z_6', 'num_9': 'z_9', 'dots_9': 'z_9'}},
            explanation={'en': 'Great sorting for 6 and 9!', 'ar': 'فرز رائع للرقمين ٦ و ٩!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.cntobj05.match.toys',
            objective_key='obj.math.count_objects_0_5',
            subject_code='math',
            unit_code='unit.math.number_sense',
            difficulty_level=1,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each toy group to its correct count.', 'ar': 'طابق كل مجموعة ألعاب بعددها الصحيح.'},
            content_payload={'prompt': 'Match each toy group to its correct count.', 'left_items': [{'id': 'toys_1', 'label': '1 Toy Car 🚗', 'visual_cue': '🚗'}, {'id': 'toys_3', 'label': '3 Rubber Ducks 🦆🦆🦆', 'visual_cue': '🦆🦆🦆'}, {'id': 'toys_4', 'label': '4 Teddy Bears 🧸x4', 'visual_cue': '🧸x4'}], 'right_items': [{'id': 'c_1', 'label': '1', 'visual_cue': '1️⃣'}, {'id': 'c_3', 'label': '3', 'visual_cue': '3️⃣'}, {'id': 'c_4', 'label': '4', 'visual_cue': '4️⃣'}], 'pairs': [{'left_id': 'toys_1', 'right_id': 'c_1'}, {'left_id': 'toys_3', 'right_id': 'c_3'}, {'left_id': 'toys_4', 'right_id': 'c_4'}]},
            correct_answer={'pairs': [{'left_id': 'toys_1', 'right_id': 'c_1'}, {'left_id': 'toys_3', 'right_id': 'c_3'}, {'left_id': 'toys_4', 'right_id': 'c_4'}]},
            explanation={'en': 'Accurate matching of toys!', 'ar': 'مطابقة دقيقة للألعاب!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.cntobj05.order.dot_groups',
            objective_key='obj.math.count_objects_0_5',
            subject_code='math',
            unit_code='unit.math.number_sense',
            difficulty_level=1,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Order the dot cards from least to most dots.', 'ar': 'رتب بطاقات النقاط من الأقل إلى الأكثر نقاطاً.'},
            content_payload={'prompt': 'Order the dot cards from least to most dots.', 'items': [{'id': 'grp_2', 'label': '2 Dots ⚫⚫', 'visual_cue': '⚫⚫'}, {'id': 'grp_1', 'label': '1 Dot ⚫', 'visual_cue': '⚫'}, {'id': 'grp_3', 'label': '3 Dots ⚫⚫⚫', 'visual_cue': '⚫⚫⚫'}], 'correct_sequence': ['grp_1', 'grp_2', 'grp_3'], 'direction': 'ascending'},
            correct_answer={'correct_sequence': ['grp_1', 'grp_2', 'grp_3']},
            explanation={'en': 'Well done! 1 dot, 2 dots, 3 dots.', 'ar': 'أحسنت! نقطة واحدة، نقطتان، ٣ نقاط.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.cntobj05.drag.bin_counts',
            objective_key='obj.math.count_objects_0_5',
            subject_code='math',
            unit_code='unit.math.number_sense',
            difficulty_level=1,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort the fruit groups: put groups of 2 in 'Two' and groups of 3 in 'Three'.", 'ar': "صنف مجموعات الفواكه: ضع مجموعات ٢ في 'اثنان' ومجموعات ٣ في 'ثلاثة'."},
            content_payload={'prompt': "Sort the fruit groups: put groups of 2 in 'Two' and groups of 3 in 'Three'.", 'items': [{'id': 'f_2_bananas', 'label': '2 Bananas 🍌🍌', 'visual_cue': '🍌🍌'}, {'id': 'f_2_oranges', 'label': '2 Oranges 🍊🍊', 'visual_cue': '🍊🍊'}, {'id': 'f_3_strawberries', 'label': '3 Strawberries 🍓🍓🍓', 'visual_cue': '🍓🍓🍓'}, {'id': 'f_3_cherries', 'label': '3 Cherries 🍒🍒🍒', 'visual_cue': '🍒🍒🍒'}], 'zones': [{'id': 'zone_two', 'label': 'Basket: 2 Fruits', 'capacity': 3}, {'id': 'zone_three', 'label': 'Basket: 3 Fruits', 'capacity': 3}], 'correct_mapping': {'f_2_bananas': 'zone_two', 'f_2_oranges': 'zone_two', 'f_3_strawberries': 'zone_three', 'f_3_cherries': 'zone_three'}},
            correct_answer={'correct_mapping': {'f_2_bananas': 'zone_two', 'f_2_oranges': 'zone_two', 'f_3_strawberries': 'zone_three', 'f_3_cherries': 'zone_three'}},
            explanation={'en': 'Brilliant fruit basket sorting!', 'ar': 'فرز رائع لسلال الفواكه!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.cntobj610.match.nature',
            objective_key='obj.math.count_objects_6_10',
            subject_code='math',
            unit_code='unit.math.number_sense',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each group of objects to the correct numeral.', 'ar': 'طابق كل مجموعة أشياء بالرقم الصحيح.'},
            content_payload={'prompt': 'Match each group of objects to the correct numeral.', 'left_items': [{'id': 'leaf_6', 'label': '6 Leaves 🍃x6', 'visual_cue': '🍃x6'}, {'id': 'flower_7', 'label': '7 Flowers 🌸x7', 'visual_cue': '🌸x7'}, {'id': 'acorn_9', 'label': '9 Acorns 🌰x9', 'visual_cue': '🌰x9'}], 'right_items': [{'id': 'n_6', 'label': '6', 'visual_cue': '6️⃣'}, {'id': 'n_7', 'label': '7', 'visual_cue': '7️⃣'}, {'id': 'n_9', 'label': '9', 'visual_cue': '9️⃣'}], 'pairs': [{'left_id': 'leaf_6', 'right_id': 'n_6'}, {'left_id': 'flower_7', 'right_id': 'n_7'}, {'left_id': 'acorn_9', 'right_id': 'n_9'}]},
            correct_answer={'pairs': [{'left_id': 'leaf_6', 'right_id': 'n_6'}, {'left_id': 'flower_7', 'right_id': 'n_7'}, {'left_id': 'acorn_9', 'right_id': 'n_9'}]},
            explanation={'en': 'Great nature object counting!', 'ar': 'عد ممتاز لعناصر الطبيعة!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.cntobj610.order.quantities',
            objective_key='obj.math.count_objects_6_10',
            subject_code='math',
            unit_code='unit.math.number_sense',
            difficulty_level=2,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Order the quantities from least to greatest count.', 'ar': 'رتب الكميات من العدد الأقل إلى العدد الأكبر.'},
            content_payload={'prompt': 'Order the quantities from least to greatest count.', 'items': [{'id': 'qty_8', 'label': '8 Circles 🟢x8', 'visual_cue': '🟢x8'}, {'id': 'qty_7', 'label': '7 Circles 🟢x7', 'visual_cue': '🟢x7'}, {'id': 'qty_10', 'label': '10 Circles 🟢x10', 'visual_cue': '🟢x10'}], 'correct_sequence': ['qty_7', 'qty_8', 'qty_10'], 'direction': 'ascending'},
            correct_answer={'correct_sequence': ['qty_7', 'qty_8', 'qty_10']},
            explanation={'en': 'Well done! 7, 8, and 10 in increasing order.', 'ar': 'أحسنت! ٧، ٨، و ١٠ مرتبة تصاعدياً.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.cntobj610.vis.find_seven_birds',
            objective_key='obj.math.count_objects_6_10',
            subject_code='math',
            unit_code='unit.math.number_sense',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the tree branch that has exactly 7 birds.', 'ar': 'حدد غصن الشجرة الذي يحتوي على ٧ طيور بالضبط.'},
            content_payload={'prompt': 'Spot the tree branch that has exactly 7 birds.', 'scene_description': 'A garden tree with birds perched on branches.', 'elements': [{'id': 'branch_5', 'label': 'Branch with 5 Birds 🐦x5', 'category': 'nature', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'branch_7', 'label': 'Branch with 7 Birds 🐦x7', 'category': 'nature', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'branch_9', 'label': 'Branch with 9 Birds 🐦x9', 'category': 'nature', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'branch_7', 'feedback_clue': 'Count the birds on the middle branch.'},
            correct_answer={'target_id': 'branch_7'},
            explanation={'en': 'That branch has exactly 7 birds!', 'ar': 'ذلك الغصن يحتوي على ٧ طيور بالضبط!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.cntobj610.drag.sort_quantities',
            objective_key='obj.math.count_objects_6_10',
            subject_code='math',
            unit_code='unit.math.number_sense',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort the item cards into 'Fewer than 8' and '8 or More'.", 'ar': "صنف بطاقات العناصر إلى 'أقل من ٨' و '٨ أو أكثر'."},
            content_payload={'prompt': "Sort the item cards into 'Fewer than 8' and '8 or More'.", 'items': [{'id': 'card_6_stars', 'label': '6 Stars ⭐x6', 'visual_cue': '⭐x6'}, {'id': 'card_7_hearts', 'label': '7 Hearts ❤️x7', 'visual_cue': '❤️x7'}, {'id': 'card_8_diamonds', 'label': '8 Diamonds 💎x8', 'visual_cue': '💎x8'}, {'id': 'card_10_circles', 'label': '10 Circles 🔵x10', 'visual_cue': '🔵x10'}], 'zones': [{'id': 'zone_less8', 'label': 'Fewer than 8 Items', 'capacity': 3}, {'id': 'zone_8plus', 'label': '8 or More Items', 'capacity': 3}], 'correct_mapping': {'card_6_stars': 'zone_less8', 'card_7_hearts': 'zone_less8', 'card_8_diamonds': 'zone_8plus', 'card_10_circles': 'zone_8plus'}},
            correct_answer={'correct_mapping': {'card_6_stars': 'zone_less8', 'card_7_hearts': 'zone_less8', 'card_8_diamonds': 'zone_8plus', 'card_10_circles': 'zone_8plus'}},
            explanation={'en': 'Accurate sorting relative to 8!', 'ar': 'فرز دقيق بالنسبة للعدد ٨!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.matchqty.mc.num4',
            objective_key='obj.math.numeral_qty_match',
            subject_code='math',
            unit_code='unit.math.number_sense',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which picture shows exactly 4 apples?', 'ar': 'أي صورة تظهر ٤ تفاحات بالضبط؟'},
            content_payload={'question': 'Which picture shows exactly 4 apples?', 'options': [{'id': 'opt_2', 'text': '2 Apples 🍎🍎', 'visual_cue': '🍎🍎', 'is_correct': False, 'distractor_rationale': 'Only two'}, {'id': 'opt_4', 'text': '4 Apples 🍎🍎🍎🍎', 'visual_cue': '🍎🍎🍎🍎', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_5', 'text': '5 Apples 🍎🍎🍎🍎🍎', 'visual_cue': '🍎🍎🍎🍎🍎', 'is_correct': False, 'distractor_rationale': 'One extra apple'}], 'correct_answer_id': 'opt_4', 'explanation': 'Terrific! 4 apples match the numeral 4.'},
            correct_answer={'correct_answer_id': 'opt_4'},
            explanation={'en': 'Terrific! 4 apples match the numeral 4.', 'ar': 'رائع! ٤ تفاحات تطابق الرقم ٤.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.matchqty.match.nums_dots',
            objective_key='obj.math.numeral_qty_match',
            subject_code='math',
            unit_code='unit.math.number_sense',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each numeral card to its matching dot pattern.', 'ar': 'طابق كل بطاقة رقم بنمط النقاط المطابق لها.'},
            content_payload={'prompt': 'Match each numeral card to its matching dot pattern.', 'left_items': [{'id': 'n_2', 'label': 'Numeral 2', 'visual_cue': '2️⃣'}, {'id': 'n_5', 'label': 'Numeral 5', 'visual_cue': '5️⃣'}, {'id': 'n_8', 'label': 'Numeral 8', 'visual_cue': '8️⃣'}], 'right_items': [{'id': 'd_2', 'label': 'Two Dots 🔴🔴', 'visual_cue': '🔴🔴'}, {'id': 'd_5', 'label': 'Five Dots 🔴🔴🔴🔴🔴', 'visual_cue': '🔴🔴🔴🔴🔴'}, {'id': 'd_8', 'label': 'Eight Dots 🔴x8', 'visual_cue': '🔴x8'}], 'pairs': [{'left_id': 'n_2', 'right_id': 'd_2'}, {'left_id': 'n_5', 'right_id': 'd_5'}, {'left_id': 'n_8', 'right_id': 'd_8'}]},
            correct_answer={'pairs': [{'left_id': 'n_2', 'right_id': 'd_2'}, {'left_id': 'n_5', 'right_id': 'd_5'}, {'left_id': 'n_8', 'right_id': 'd_8'}]},
            explanation={'en': 'Great matching! Numerals and dot quantities align.', 'ar': 'مطابقة ممتازة! الأرقام والكميات متطابقة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.matchqty.order.num_qty_pairs',
            objective_key='obj.math.numeral_qty_match',
            subject_code='math',
            unit_code='unit.math.number_sense',
            difficulty_level=2,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Order the numeral-quantity cards from smallest to largest.', 'ar': 'رتب بطاقات الأرقام والكميات من الأصغر إلى الأكبر.'},
            content_payload={'prompt': 'Order the numeral-quantity cards from smallest to largest.', 'items': [{'id': 'pair_3', 'label': '3 (⭐⭐⭐)', 'visual_cue': '3 (⭐⭐⭐)'}, {'id': 'pair_1', 'label': '1 (⭐)', 'visual_cue': '1 (⭐)'}, {'id': 'pair_5', 'label': '5 (⭐⭐⭐⭐⭐)', 'visual_cue': '5 (⭐⭐⭐⭐⭐)'}], 'correct_sequence': ['pair_1', 'pair_3', 'pair_5'], 'direction': 'ascending'},
            correct_answer={'correct_sequence': ['pair_1', 'pair_3', 'pair_5']},
            explanation={'en': 'Well done! 1 star, 3 stars, 5 stars in order.', 'ar': 'أحسنت! نجمة، ٣ نجوم، ٥ نجوم بالترتيب.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.matchqty.drag.label_boxes',
            objective_key='obj.math.numeral_qty_match',
            subject_code='math',
            unit_code='unit.math.number_sense',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': 'Drag each numeral label to the box with that number of items.', 'ar': 'اسحب بطاقة الرقم إلى الصندوق الذي يحتوي على ذلك العدد من العناصر.'},
            content_payload={'prompt': 'Drag each numeral label to the box with that number of items.', 'items': [{'id': 'lbl_3', 'label': '3', 'visual_cue': '3️⃣'}, {'id': 'lbl_6', 'label': '6', 'visual_cue': '6️⃣'}], 'zones': [{'id': 'box_3', 'label': 'Box with 3 Pencils ✏️✏️✏️', 'capacity': 2}, {'id': 'box_6', 'label': 'Box with 6 Pencils ✏️x6', 'capacity': 2}], 'correct_mapping': {'lbl_3': 'box_3', 'lbl_6': 'box_6'}},
            correct_answer={'correct_mapping': {'lbl_3': 'box_3', 'lbl_6': 'box_6'}},
            explanation={'en': 'Spot on! 3 pencils have label 3, 6 pencils have label 6.', 'ar': 'صحيح! ٣ أقلام تأخذ بطاقة ٣، و ٦ أقلام تأخذ بطاقة ٦.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.cmp.mc.fewer',
            objective_key='obj.math.compare_quantities',
            subject_code='math',
            unit_code='unit.math.number_sense',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which group has FEWER items?', 'ar': 'أي مجموعة تحتوي على عناصر أقل؟'},
            content_payload={'question': 'Which group has FEWER items?', 'options': [{'id': 'opt_turtles', 'text': '3 Turtles 🐢🐢🐢', 'visual_cue': '🐢🐢🐢', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_rabbits', 'text': '6 Rabbits 🐇x6', 'visual_cue': '🐇x6', 'is_correct': False, 'distractor_rationale': '6 is greater than 3'}], 'correct_answer_id': 'opt_turtles', 'explanation': 'Correct! 3 turtles is fewer than 6 rabbits.'},
            correct_answer={'correct_answer_id': 'opt_turtles'},
            explanation={'en': 'Correct! 3 turtles is fewer than 6 rabbits.', 'ar': 'صحيح! ٣ سلاحف أقل من ٦ أرانب.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.cmp.match.terms',
            objective_key='obj.math.compare_quantities',
            subject_code='math',
            unit_code='unit.math.number_sense',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each comparison pair to the correct term.', 'ar': 'طابق كل زوج مقارنة بالمصطلح الصحيح.'},
            content_payload={'prompt': 'Match each comparison pair to the correct term.', 'left_items': [{'id': 'pair_more', 'label': '5 apples vs 2 apples', 'visual_cue': '🍎x5 vs 🍎x2'}, {'id': 'pair_fewer', 'label': '1 star vs 4 stars', 'visual_cue': '⭐x1 vs ⭐x4'}, {'id': 'pair_equal', 'label': '3 dots vs 3 dots', 'visual_cue': '🔵x3 vs 🔵x3'}], 'right_items': [{'id': 'term_more', 'label': 'First group has MORE', 'visual_cue': '➕'}, {'id': 'term_fewer', 'label': 'First group has FEWER', 'visual_cue': '➖'}, {'id': 'term_equal', 'label': 'Both groups are EQUAL', 'visual_cue': '🟰'}], 'pairs': [{'left_id': 'pair_more', 'right_id': 'term_more'}, {'left_id': 'pair_fewer', 'right_id': 'term_fewer'}, {'left_id': 'pair_equal', 'right_id': 'term_equal'}]},
            correct_answer={'pairs': [{'left_id': 'pair_more', 'right_id': 'term_more'}, {'left_id': 'pair_fewer', 'right_id': 'term_fewer'}, {'left_id': 'pair_equal', 'right_id': 'term_equal'}]},
            explanation={'en': 'Great work! You understood more, fewer, and equal quantities.', 'ar': 'عمل رائع! لقد فهمت الكميات الأكثر والأقل والمتساوية.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.cmp.vis.bowl_fewer',
            objective_key='obj.math.compare_quantities',
            subject_code='math',
            unit_code='unit.math.number_sense',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Select the bowl that contains MORE goldfish.', 'ar': 'حدد الوعاء الذي يحتوي على عدد أكبر من أسماك الزينة.'},
            content_payload={'prompt': 'Select the bowl that contains MORE goldfish.', 'scene_description': 'Two glass fishbowls on a bright blue counter.', 'elements': [{'id': 'bowl_small', 'label': 'Bowl A (2 Goldfish) 🐟🐟', 'category': 'bowl', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'bowl_large', 'label': 'Bowl B (5 Goldfish) 🐟x5', 'category': 'bowl', 'is_target': True, 'bounding_hint': 'right'}], 'target_id': 'bowl_large', 'feedback_clue': 'Look at the bowl on the right and count 5 fish.'},
            correct_answer={'target_id': 'bowl_large'},
            explanation={'en': 'Wonderful! Bowl B has 5 fish, which is more than 2 fish.', 'ar': 'رائع! الوعاء ب يحتوي على ٥ أسماك، وهو أكثر من سمكتين.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.cmp.drag.sort_more_less',
            objective_key='obj.math.compare_quantities',
            subject_code='math',
            unit_code='unit.math.number_sense',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort the statements into 'Greater Quantity' and 'Lesser Quantity' compared to 5.", 'ar': "صنف العبارات إلى 'كمية أكبر' و 'كمية أقل' مقارنة بالعدد ٥."},
            content_payload={'prompt': "Sort the statements into 'Greater Quantity' and 'Lesser Quantity' compared to 5.", 'items': [{'id': 'qty_8_items', 'label': '8 Marbles ⚪x8', 'visual_cue': '⚪x8'}, {'id': 'qty_7_items', 'label': '7 Blocks 🟩x7', 'visual_cue': '🟩x7'}, {'id': 'qty_2_items', 'label': '2 Buttons 🔘🔘', 'visual_cue': '🔘🔘'}, {'id': 'qty_4_items', 'label': '4 Cups ☕x4', 'visual_cue': '☕x4'}], 'zones': [{'id': 'zone_greater', 'label': 'More than 5 Items', 'capacity': 3}, {'id': 'zone_lesser', 'label': 'Fewer than 5 Items', 'capacity': 3}], 'correct_mapping': {'qty_8_items': 'zone_greater', 'qty_7_items': 'zone_greater', 'qty_2_items': 'zone_lesser', 'qty_4_items': 'zone_lesser'}},
            correct_answer={'correct_mapping': {'qty_8_items': 'zone_greater', 'qty_7_items': 'zone_greater', 'qty_2_items': 'zone_lesser', 'qty_4_items': 'zone_lesser'}},
            explanation={'en': 'Terrific sorting! 7 and 8 are more than 5; 2 and 4 are fewer than 5.', 'ar': 'فرز رائع! ٧ و ٨ أكثر من ٥، بينما ٢ و ٤ أقل من ٥.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.seq.mc.before_8',
            objective_key='obj.math.number_before',
            subject_code='math',
            unit_code='unit.math.number_sequence',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'What number comes immediately before 8?', 'ar': 'ما هو الرقم الذي يأتي مباشرة قبل الرقم ٨؟'},
            content_payload={'question': 'What number comes immediately before 8?', 'options': [{'id': 'opt_7', 'text': '7', 'visual_cue': '7️⃣', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_9', 'text': '9', 'visual_cue': '9️⃣', 'is_correct': False, 'distractor_rationale': '9 comes after 8'}, {'id': 'opt_6', 'text': '6', 'visual_cue': '6️⃣', 'is_correct': False, 'distractor_rationale': '6 is two before 8'}], 'correct_answer_id': 'opt_7', 'explanation': 'Correct! 7 comes immediately before 8.'},
            correct_answer={'correct_answer_id': 'opt_7'},
            explanation={'en': 'Correct! 7 comes immediately before 8.', 'ar': 'صحيح! الرقم ٧ يأتي مباشرة قبل ٨.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.seq.mc.before_3',
            objective_key='obj.math.number_before',
            subject_code='math',
            unit_code='unit.math.number_sequence',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'What number comes immediately before 3?', 'ar': 'ما هو الرقم الذي يأتي مباشرة قبل الرقم ٣؟'},
            content_payload={'question': 'What number comes immediately before 3?', 'options': [{'id': 'opt_2', 'text': '2', 'visual_cue': '2️⃣', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_4', 'text': '4', 'visual_cue': '4️⃣', 'is_correct': False, 'distractor_rationale': '4 comes after 3'}, {'id': 'opt_1', 'text': '1', 'visual_cue': '1️⃣', 'is_correct': False, 'distractor_rationale': '1 is two before 3'}], 'correct_answer_id': 'opt_2', 'explanation': 'Super! 2 comes right before 3.'},
            correct_answer={'correct_answer_id': 'opt_2'},
            explanation={'en': 'Super! 2 comes right before 3.', 'ar': 'ممتاز! الرقم ٢ يأتي مباشرة قبل ٣.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.seq.match.before_pairs',
            objective_key='obj.math.number_before',
            subject_code='math',
            unit_code='unit.math.number_sequence',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each target number to the number that comes immediately before it.', 'ar': 'طابق كل رقم مستهدف بالرقم الذي يأتي قبله مباشرة.'},
            content_payload={'prompt': 'Match each target number to the number that comes immediately before it.', 'left_items': [{'id': 'tgt_4', 'label': 'Target: 4', 'visual_cue': '4️⃣'}, {'id': 'tgt_7', 'label': 'Target: 7', 'visual_cue': '7️⃣'}, {'id': 'tgt_10', 'label': 'Target: 10', 'visual_cue': '🔟'}], 'right_items': [{'id': 'bef_3', 'label': 'Comes Before: 3', 'visual_cue': '3️⃣'}, {'id': 'bef_6', 'label': 'Comes Before: 6', 'visual_cue': '6️⃣'}, {'id': 'bef_9', 'label': 'Comes Before: 9', 'visual_cue': '9️⃣'}], 'pairs': [{'left_id': 'tgt_4', 'right_id': 'bef_3'}, {'left_id': 'tgt_7', 'right_id': 'bef_6'}, {'left_id': 'tgt_10', 'right_id': 'bef_9'}]},
            correct_answer={'pairs': [{'left_id': 'tgt_4', 'right_id': 'bef_3'}, {'left_id': 'tgt_7', 'right_id': 'bef_6'}, {'left_id': 'tgt_10', 'right_id': 'bef_9'}]},
            explanation={'en': 'Excellent matching! 3 before 4, 6 before 7, 9 before 10.', 'ar': 'مطابقة ممتازة! ٣ قبل ٤، ٦ قبل ٧، ٩ قبل ١٠.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.seq.order.before_consec',
            objective_key='obj.math.number_before',
            subject_code='math',
            unit_code='unit.math.number_sequence',
            difficulty_level=2,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Place the numbers in counting order: 3, 4, 5.', 'ar': 'ضع الأرقام بترتيب العد: ٣، ٤، ٥.'},
            content_payload={'prompt': 'Place the numbers in counting order: 3, 4, 5.', 'items': [{'id': 'n_4', 'label': '4', 'visual_cue': '4️⃣'}, {'id': 'n_3', 'label': '3', 'visual_cue': '3️⃣'}, {'id': 'n_5', 'label': '5', 'visual_cue': '5️⃣'}], 'correct_sequence': ['n_3', 'n_4', 'n_5'], 'direction': 'ascending'},
            correct_answer={'correct_sequence': ['n_3', 'n_4', 'n_5']},
            explanation={'en': 'Well done! 3 comes before 4, which comes before 5.', 'ar': 'أحسنت! ٣ تأتي قبل ٤، التي تأتي قبل ٥.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.seq.mc.after_4',
            objective_key='obj.math.number_after',
            subject_code='math',
            unit_code='unit.math.number_sequence',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'What number comes immediately after 4?', 'ar': 'ما هو الرقم الذي يأتي مباشرة بعد الرقم ٤؟'},
            content_payload={'question': 'What number comes immediately after 4?', 'options': [{'id': 'opt_5', 'text': '5', 'visual_cue': '5️⃣', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_3', 'text': '3', 'visual_cue': '3️⃣', 'is_correct': False, 'distractor_rationale': '3 comes before 4'}, {'id': 'opt_6', 'text': '6', 'visual_cue': '6️⃣', 'is_correct': False, 'distractor_rationale': '6 is two after 4'}], 'correct_answer_id': 'opt_5', 'explanation': 'Great job! 5 comes immediately after 4.'},
            correct_answer={'correct_answer_id': 'opt_5'},
            explanation={'en': 'Great job! 5 comes immediately after 4.', 'ar': 'عمل رائع! الرقم ٥ يأتي مباشرة بعد ٤.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.seq.mc.after_8',
            objective_key='obj.math.number_after',
            subject_code='math',
            unit_code='unit.math.number_sequence',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'What number comes immediately after 8?', 'ar': 'ما هو الرقم الذي يأتي مباشرة بعد الرقم ٨؟'},
            content_payload={'question': 'What number comes immediately after 8?', 'options': [{'id': 'opt_9', 'text': '9', 'visual_cue': '9️⃣', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_7', 'text': '7', 'visual_cue': '7️⃣', 'is_correct': False, 'distractor_rationale': '7 comes before 8'}, {'id': 'opt_10', 'text': '10', 'visual_cue': '🔟', 'is_correct': False, 'distractor_rationale': '10 is two after 8'}], 'correct_answer_id': 'opt_9', 'explanation': 'Spot on! 9 comes right after 8.'},
            correct_answer={'correct_answer_id': 'opt_9'},
            explanation={'en': 'Spot on! 9 comes right after 8.', 'ar': 'صحيح! الرقم ٩ يأتي مباشرة بعد ٨.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.seq.match.after_pairs',
            objective_key='obj.math.number_after',
            subject_code='math',
            unit_code='unit.math.number_sequence',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each number to the number that comes immediately after it.', 'ar': 'طابق كل رقم بالرقم الذي يأتي بعده مباشرة.'},
            content_payload={'prompt': 'Match each number to the number that comes immediately after it.', 'left_items': [{'id': 'src_3', 'label': 'Number: 3', 'visual_cue': '3️⃣'}, {'id': 'src_6', 'label': 'Number: 6', 'visual_cue': '6️⃣'}, {'id': 'src_8', 'label': 'Number: 8', 'visual_cue': '8️⃣'}], 'right_items': [{'id': 'nxt_4', 'label': 'Comes After: 4', 'visual_cue': '4️⃣'}, {'id': 'nxt_7', 'label': 'Comes After: 7', 'visual_cue': '7️⃣'}, {'id': 'nxt_9', 'label': 'Comes After: 9', 'visual_cue': '9️⃣'}], 'pairs': [{'left_id': 'src_3', 'right_id': 'nxt_4'}, {'left_id': 'src_6', 'right_id': 'nxt_7'}, {'left_id': 'src_8', 'right_id': 'nxt_9'}]},
            correct_answer={'pairs': [{'left_id': 'src_3', 'right_id': 'nxt_4'}, {'left_id': 'src_6', 'right_id': 'nxt_7'}, {'left_id': 'src_8', 'right_id': 'nxt_9'}]},
            explanation={'en': 'Terrific matching! 4 after 3, 7 after 6, 9 after 8.', 'ar': 'مطابقة رائعة! ٤ بعد ٣، ٧ بعد ٦، ٩ بعد ٨.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.seq.order.after_consec',
            objective_key='obj.math.number_after',
            subject_code='math',
            unit_code='unit.math.number_sequence',
            difficulty_level=2,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Place the numbers in consecutive order: 6, 7, 8.', 'ar': 'ضع الأرقام بالترتيب المتتالي: ٦، ٧، ٨.'},
            content_payload={'prompt': 'Place the numbers in consecutive order: 6, 7, 8.', 'items': [{'id': 'n_7', 'label': '7', 'visual_cue': '7️⃣'}, {'id': 'n_6', 'label': '6', 'visual_cue': '6️⃣'}, {'id': 'n_8', 'label': '8', 'visual_cue': '8️⃣'}], 'correct_sequence': ['n_6', 'n_7', 'n_8'], 'direction': 'ascending'},
            correct_answer={'correct_sequence': ['n_6', 'n_7', 'n_8']},
            explanation={'en': 'Awesome! 6 followed by 7 followed by 8.', 'ar': 'رائع! ٦ تليها ٧ تليها ٨.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.seq.order.asc_258',
            objective_key='obj.math.order_smallest_largest',
            subject_code='math',
            unit_code='unit.math.number_sequence',
            difficulty_level=2,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Order the numbers from smallest to largest.', 'ar': 'رتب الأرقام من الأصغر إلى الأكبر.'},
            content_payload={'prompt': 'Order the numbers from smallest to largest.', 'items': [{'id': 'ord_5', 'label': '5', 'visual_cue': '5️⃣'}, {'id': 'ord_2', 'label': '2', 'visual_cue': '2️⃣'}, {'id': 'ord_8', 'label': '8', 'visual_cue': '8️⃣'}], 'correct_sequence': ['ord_2', 'ord_5', 'ord_8'], 'direction': 'ascending'},
            correct_answer={'correct_sequence': ['ord_2', 'ord_5', 'ord_8']},
            explanation={'en': 'Perfect! 2 < 5 < 8.', 'ar': 'ممتاز! ٢ < ٥ < ٨.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.seq.order.asc_3479',
            objective_key='obj.math.order_smallest_largest',
            subject_code='math',
            unit_code='unit.math.number_sequence',
            difficulty_level=2,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Order the numbers from smallest to largest.', 'ar': 'رتب الأرقام من الأصغر إلى الأكبر.'},
            content_payload={'prompt': 'Order the numbers from smallest to largest.', 'items': [{'id': 'ord_7', 'label': '7', 'visual_cue': '7️⃣'}, {'id': 'ord_3', 'label': '3', 'visual_cue': '3️⃣'}, {'id': 'ord_9', 'label': '9', 'visual_cue': '9️⃣'}, {'id': 'ord_4', 'label': '4', 'visual_cue': '4️⃣'}], 'correct_sequence': ['ord_3', 'ord_4', 'ord_7', 'ord_9'], 'direction': 'ascending'},
            correct_answer={'correct_sequence': ['ord_3', 'ord_4', 'ord_7', 'ord_9']},
            explanation={'en': 'Brilliant ordering! 3, 4, 7, 9 are increasing.', 'ar': 'ترتيب رائع! ٣، ٤، ٧، ٩ مرتبة تصاعدياً.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.seq.mc.asc_check',
            objective_key='obj.math.order_smallest_largest',
            subject_code='math',
            unit_code='unit.math.number_sequence',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which row is correctly ordered from smallest to largest?', 'ar': 'أي صف مرتب بشكل صحيح من الأصغر إلى الأكبر؟'},
            content_payload={'question': 'Which row is correctly ordered from smallest to largest?', 'options': [{'id': 'row_correct', 'text': '1, 4, 8', 'visual_cue': '1️⃣ ➡️ 4️⃣ ➡️ 8️⃣', 'is_correct': True, 'distractor_rationale': None}, {'id': 'row_desc', 'text': '8, 4, 1', 'visual_cue': '8️⃣ ➡️ 4️⃣ ➡️ 1️⃣', 'is_correct': False, 'distractor_rationale': 'This is largest to smallest'}, {'id': 'row_mix', 'text': '4, 1, 8', 'visual_cue': '4️⃣ ➡️ 1️⃣ ➡️ 8️⃣', 'is_correct': False, 'distractor_rationale': 'Unordered sequence'}], 'correct_answer_id': 'row_correct', 'explanation': 'Correct! 1, 4, 8 increases from smallest to largest.'},
            correct_answer={'correct_answer_id': 'row_correct'},
            explanation={'en': 'Correct! 1, 4, 8 increases from smallest to largest.', 'ar': 'صحيح! ١، ٤، ٨ تزداد من الأصغر إلى الأكبر.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.seq.drag.sort_small_large',
            objective_key='obj.math.order_smallest_largest',
            subject_code='math',
            unit_code='unit.math.number_sequence',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort the numbers into 'Small Numbers (1-4)' and 'Large Numbers (6-10)'.", 'ar': "صنف الأرقام إلى 'أرقام صغيرة (١-٤)' و 'أرقام كبيرة (٦-١٠)'."},
            content_payload={'prompt': "Sort the numbers into 'Small Numbers (1-4)' and 'Large Numbers (6-10)'.", 'items': [{'id': 'd_1', 'label': '1', 'visual_cue': '1️⃣'}, {'id': 'd_3', 'label': '3', 'visual_cue': '3️⃣'}, {'id': 'd_7', 'label': '7', 'visual_cue': '7️⃣'}, {'id': 'd_9', 'label': '9', 'visual_cue': '9️⃣'}], 'zones': [{'id': 'z_small', 'label': 'Small Numbers (1 to 4)', 'capacity': 3}, {'id': 'z_large', 'label': 'Large Numbers (6 to 10)', 'capacity': 3}], 'correct_mapping': {'d_1': 'z_small', 'd_3': 'z_small', 'd_7': 'z_large', 'd_9': 'z_large'}},
            correct_answer={'correct_mapping': {'d_1': 'z_small', 'd_3': 'z_small', 'd_7': 'z_large', 'd_9': 'z_large'}},
            explanation={'en': 'Super categorization of number magnitudes!', 'ar': 'تصنيف رائع لمقادير الأرقام!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.seq.order.desc_962',
            objective_key='obj.math.order_largest_smallest',
            subject_code='math',
            unit_code='unit.math.number_sequence',
            difficulty_level=3,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Order the numbers from largest to smallest.', 'ar': 'رتب الأرقام من الأكبر إلى الأصغر.'},
            content_payload={'prompt': 'Order the numbers from largest to smallest.', 'items': [{'id': 'd_6', 'label': '6', 'visual_cue': '6️⃣'}, {'id': 'd_9', 'label': '9', 'visual_cue': '9️⃣'}, {'id': 'd_2', 'label': '2', 'visual_cue': '2️⃣'}], 'correct_sequence': ['d_9', 'd_6', 'd_2'], 'direction': 'descending'},
            correct_answer={'correct_sequence': ['d_9', 'd_6', 'd_2']},
            explanation={'en': 'Wonderful! 9 > 6 > 2.', 'ar': 'رائع! ٩ > ٦ > ٢.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.seq.order.desc_8531',
            objective_key='obj.math.order_largest_smallest',
            subject_code='math',
            unit_code='unit.math.number_sequence',
            difficulty_level=3,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Order the numbers from largest to smallest.', 'ar': 'رتب الأرقام من الأكبر إلى الأصغر.'},
            content_payload={'prompt': 'Order the numbers from largest to smallest.', 'items': [{'id': 'd_5', 'label': '5', 'visual_cue': '5️⃣'}, {'id': 'd_8', 'label': '8', 'visual_cue': '8️⃣'}, {'id': 'd_1', 'label': '1', 'visual_cue': '1️⃣'}, {'id': 'd_3', 'label': '3', 'visual_cue': '3️⃣'}], 'correct_sequence': ['d_8', 'd_5', 'd_3', 'd_1'], 'direction': 'descending'},
            correct_answer={'correct_sequence': ['d_8', 'd_5', 'd_3', 'd_1']},
            explanation={'en': 'Terrific descending order! 8, 5, 3, 1.', 'ar': 'ترتيب تنازلي رائع! ٨، ٥، ٣، ١.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.seq.order.desc_1074',
            objective_key='obj.math.order_largest_smallest',
            subject_code='math',
            unit_code='unit.math.number_sequence',
            difficulty_level=3,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Order the numbers from largest to smallest.', 'ar': 'رتب الأرقام من الأكبر إلى الأصغر.'},
            content_payload={'prompt': 'Order the numbers from largest to smallest.', 'items': [{'id': 'd_7', 'label': '7', 'visual_cue': '7️⃣'}, {'id': 'd_10', 'label': '10', 'visual_cue': '🔟'}, {'id': 'd_4', 'label': '4', 'visual_cue': '4️⃣'}], 'correct_sequence': ['d_10', 'd_7', 'd_4'], 'direction': 'descending'},
            correct_answer={'correct_sequence': ['d_10', 'd_7', 'd_4']},
            explanation={'en': 'Great! 10 > 7 > 4.', 'ar': 'ممتاز! ١٠ > ٧ > ٤.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.seq.mc.desc_check',
            objective_key='obj.math.order_largest_smallest',
            subject_code='math',
            unit_code='unit.math.number_sequence',
            difficulty_level=3,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which sequence is ordered from largest to smallest?', 'ar': 'أي تسلسل مرتب من الأكبر إلى الأصغر؟'},
            content_payload={'question': 'Which sequence is ordered from largest to smallest?', 'options': [{'id': 'opt_desc', 'text': '9, 7, 4', 'visual_cue': '9️⃣ ➡️ 7️⃣ ➡️ 4️⃣', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_asc', 'text': '4, 7, 9', 'visual_cue': '4️⃣ ➡️ 7️⃣ ➡️ 9️⃣', 'is_correct': False, 'distractor_rationale': 'Smallest to largest'}, {'id': 'opt_unordered', 'text': '7, 9, 4', 'visual_cue': '7️⃣ ➡️ 9️⃣ ➡️ 4️⃣', 'is_correct': False, 'distractor_rationale': 'Not monotonically decreasing'}], 'correct_answer_id': 'opt_desc', 'explanation': 'Spot on! 9, 7, 4 counts down from largest.'},
            correct_answer={'correct_answer_id': 'opt_desc'},
            explanation={'en': 'Spot on! 9, 7, 4 counts down from largest.', 'ar': 'صحيح! ٩، ٧، ٤ تعد تنازلياً من الأكبر.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.seq.vis.find_largest',
            objective_key='obj.math.order_largest_smallest',
            subject_code='math',
            unit_code='unit.math.number_sequence',
            difficulty_level=3,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Find the card displaying the LARGEST number.', 'ar': 'حدد البطاقة التي تعرض أكبر رقم.'},
            content_payload={'prompt': 'Find the card displaying the LARGEST number.', 'scene_description': "Three numeral cards standing on a teacher's desk.", 'elements': [{'id': 'card_3', 'label': 'Card 3', 'category': 'card', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'card_9', 'label': 'Card 9', 'category': 'card', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'card_5', 'label': 'Card 5', 'category': 'card', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'card_9', 'feedback_clue': 'Look for the greatest digit among 3, 9, and 5.'},
            correct_answer={'target_id': 'card_9'},
            explanation={'en': 'Excellent! 9 is the largest number.', 'ar': 'ممتاز! ٩ هو أكبر رقم.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.seq.mc.miss_6',
            objective_key='obj.math.complete_missing_sequence',
            subject_code='math',
            unit_code='unit.math.number_sequence',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'What number completes the sequence: 4, 5, __, 7?', 'ar': 'ما هو الرقم الذي يكمل التسلسل: ٤، ٥، __، ٧؟'},
            content_payload={'question': 'What number completes the sequence: 4, 5, __, 7?', 'options': [{'id': 'opt_6', 'text': '6', 'visual_cue': '6️⃣', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_3', 'text': '3', 'visual_cue': '3️⃣', 'is_correct': False, 'distractor_rationale': 'Precedes 4'}, {'id': 'opt_8', 'text': '8', 'visual_cue': '8️⃣', 'is_correct': False, 'distractor_rationale': 'Follows 7'}], 'correct_answer_id': 'opt_6', 'explanation': 'Correct! 4, 5, 6, 7.'},
            correct_answer={'correct_answer_id': 'opt_6'},
            explanation={'en': 'Correct! 4, 5, 6, 7.', 'ar': 'صحيح! ٤، ٥، ٦، ٧.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.seq.mc.miss_4',
            objective_key='obj.math.complete_missing_sequence',
            subject_code='math',
            unit_code='unit.math.number_sequence',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'What number completes the sequence: 1, 2, 3, __?', 'ar': 'ما هو الرقم الذي يكمل التسلسل: ١، ٢، ٣، __؟'},
            content_payload={'question': 'What number completes the sequence: 1, 2, 3, __?', 'options': [{'id': 'opt_4', 'text': '4', 'visual_cue': '4️⃣', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_5', 'text': '5', 'visual_cue': '5️⃣', 'is_correct': False, 'distractor_rationale': 'Skips 4'}, {'id': 'opt_0', 'text': '0', 'visual_cue': '0️⃣', 'is_correct': False, 'distractor_rationale': 'Comes before 1'}], 'correct_answer_id': 'opt_4', 'explanation': 'Super! 1, 2, 3, 4.'},
            correct_answer={'correct_answer_id': 'opt_4'},
            explanation={'en': 'Super! 1, 2, 3, 4.', 'ar': 'ممتاز! ١، ٢، ٣، ٤.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.seq.match.missing_pairs',
            objective_key='obj.math.complete_missing_sequence',
            subject_code='math',
            unit_code='unit.math.number_sequence',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each incomplete sequence with its missing number.', 'ar': 'طابق كل تسلسل غير مكتمل برقمه المفقود.'},
            content_payload={'prompt': 'Match each incomplete sequence with its missing number.', 'left_items': [{'id': 'seq_24', 'label': '2, __, 4', 'visual_cue': '2️⃣ ❓ 4️⃣'}, {'id': 'seq_79', 'label': '7, __, 9', 'visual_cue': '7️⃣ ❓ 9️⃣'}], 'right_items': [{'id': 'ans_3', 'label': 'Missing: 3', 'visual_cue': '3️⃣'}, {'id': 'ans_8', 'label': 'Missing: 8', 'visual_cue': '8️⃣'}], 'pairs': [{'left_id': 'seq_24', 'right_id': 'ans_3'}, {'left_id': 'seq_79', 'right_id': 'ans_8'}]},
            correct_answer={'pairs': [{'left_id': 'seq_24', 'right_id': 'ans_3'}, {'left_id': 'seq_79', 'right_id': 'ans_8'}]},
            explanation={'en': 'Great missing number completion!', 'ar': 'إكمال رائع للأرقام المفقودة!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.seq.order.fill_gap',
            objective_key='obj.math.complete_missing_sequence',
            subject_code='math',
            unit_code='unit.math.number_sequence',
            difficulty_level=2,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Place the numbers in counting order: 5, 6, 7.', 'ar': 'ضع الأرقام بترتيب العد: ٥، ٦، ٧.'},
            content_payload={'prompt': 'Place the numbers in counting order: 5, 6, 7.', 'items': [{'id': 'n_6', 'label': '6 (Middle)', 'visual_cue': '6️⃣'}, {'id': 'n_5', 'label': '5 (Start)', 'visual_cue': '5️⃣'}, {'id': 'n_7', 'label': '7 (End)', 'visual_cue': '7️⃣'}], 'correct_sequence': ['n_5', 'n_6', 'n_7'], 'direction': 'ascending'},
            correct_answer={'correct_sequence': ['n_5', 'n_6', 'n_7']},
            explanation={'en': 'Terrific! 5, 6, 7 is complete.', 'ar': 'رائع! ٥، ٦، ٧ مكتملة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.seq.mc.pat_even',
            objective_key='obj.math.recognize_numerical_patterns',
            subject_code='math',
            unit_code='unit.math.number_sequence',
            difficulty_level=3,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'What comes next in the pattern: 2, 4, 6, __?', 'ar': 'ما الذي يأتي تالياً في النمط: ٢، ٤، ٦، __؟'},
            content_payload={'question': 'What comes next in the pattern: 2, 4, 6, __?', 'options': [{'id': 'opt_8', 'text': '8', 'visual_cue': '8️⃣', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_7', 'text': '7', 'visual_cue': '7️⃣', 'is_correct': False, 'distractor_rationale': 'Only adding 1'}, {'id': 'opt_9', 'text': '9', 'visual_cue': '9️⃣', 'is_correct': False, 'distractor_rationale': 'Odd number'}], 'correct_answer_id': 'opt_8', 'explanation': 'Correct! Adding 2 each time: 2, 4, 6, 8.'},
            correct_answer={'correct_answer_id': 'opt_8'},
            explanation={'en': 'Correct! Adding 2 each time: 2, 4, 6, 8.', 'ar': 'صحيح! إضافة ٢ في كل مرة: ٢، ٤، ٦، ٨.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.seq.mc.pat_odd',
            objective_key='obj.math.recognize_numerical_patterns',
            subject_code='math',
            unit_code='unit.math.number_sequence',
            difficulty_level=3,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'What comes next in the pattern: 1, 3, 5, __?', 'ar': 'ما الذي يأتي تالياً في النمط: ١، ٣، ٥، __؟'},
            content_payload={'question': 'What comes next in the pattern: 1, 3, 5, __?', 'options': [{'id': 'opt_7', 'text': '7', 'visual_cue': '7️⃣', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_6', 'text': '6', 'visual_cue': '6️⃣', 'is_correct': False, 'distractor_rationale': 'Only adding 1'}, {'id': 'opt_8', 'text': '8', 'visual_cue': '8️⃣', 'is_correct': False, 'distractor_rationale': 'Even number'}], 'correct_answer_id': 'opt_7', 'explanation': 'Super! Skip counting odds: 1, 3, 5, 7.'},
            correct_answer={'correct_answer_id': 'opt_7'},
            explanation={'en': 'Super! Skip counting odds: 1, 3, 5, 7.', 'ar': 'ممتاز! القفز بمقدار ٢ في الأعداد الفردية: ١، ٣، ٥، ٧.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.seq.order.skip_count',
            objective_key='obj.math.recognize_numerical_patterns',
            subject_code='math',
            unit_code='unit.math.number_sequence',
            difficulty_level=3,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Arrange the skip counting by 2s pattern.', 'ar': 'رتب نمط العد القفزي بمقدار ٢.'},
            content_payload={'prompt': 'Arrange the skip counting by 2s pattern.', 'items': [{'id': 'p_4', 'label': '4', 'visual_cue': '4️⃣'}, {'id': 'p_2', 'label': '2', 'visual_cue': '2️⃣'}, {'id': 'p_6', 'label': '6', 'visual_cue': '6️⃣'}, {'id': 'p_8', 'label': '8', 'visual_cue': '8️⃣'}], 'correct_sequence': ['p_2', 'p_4', 'p_6', 'p_8'], 'direction': 'ascending'},
            correct_answer={'correct_sequence': ['p_2', 'p_4', 'p_6', 'p_8']},
            explanation={'en': 'Brilliant! 2, 4, 6, 8 pattern recognized.', 'ar': 'رائع! تم التعرف على نمط ٢، ٤، ٦، ٨.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.seq.match.pattern_rules',
            objective_key='obj.math.recognize_numerical_patterns',
            subject_code='math',
            unit_code='unit.math.number_sequence',
            difficulty_level=3,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each pattern start with its next number.', 'ar': 'طابق بداية كل نمط برقمه التالي.'},
            content_payload={'prompt': 'Match each pattern start with its next number.', 'left_items': [{'id': 'pat_24', 'label': '2, 4, 6, __', 'visual_cue': '2, 4, 6, ?'}, {'id': 'pat_13', 'label': '1, 3, 5, __', 'visual_cue': '1, 3, 5, ?'}], 'right_items': [{'id': 'nxt_8', 'label': 'Next is 8', 'visual_cue': '8️⃣'}, {'id': 'nxt_7', 'label': 'Next is 7', 'visual_cue': '7️⃣'}], 'pairs': [{'left_id': 'pat_24', 'right_id': 'nxt_8'}, {'left_id': 'pat_13', 'right_id': 'nxt_7'}]},
            correct_answer={'pairs': [{'left_id': 'pat_24', 'right_id': 'nxt_8'}, {'left_id': 'pat_13', 'right_id': 'nxt_7'}]},
            explanation={'en': 'Great pattern rule matching!', 'ar': 'مطابقة ممتازة لقواعد الأنماط!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.seq.drag.sort_even_odd',
            objective_key='obj.math.recognize_numerical_patterns',
            subject_code='math',
            unit_code='unit.math.number_sequence',
            difficulty_level=3,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort numbers into 'Even Pattern (2, 4, 6)' and 'Odd Pattern (1, 3, 5)'.", 'ar': "صنف الأرقام إلى 'نمط زوجي (٢، ٤، ٦)' و 'نمط فردي (١، ٣، ٥)'."},
            content_payload={'prompt': "Sort numbers into 'Even Pattern (2, 4, 6)' and 'Odd Pattern (1, 3, 5)'.", 'items': [{'id': 'num_e2', 'label': '2', 'visual_cue': '2️⃣'}, {'id': 'num_e4', 'label': '4', 'visual_cue': '4️⃣'}, {'id': 'num_o1', 'label': '1', 'visual_cue': '1️⃣'}, {'id': 'num_o3', 'label': '3', 'visual_cue': '3️⃣'}], 'zones': [{'id': 'z_even', 'label': 'Even Pattern', 'capacity': 3}, {'id': 'z_odd', 'label': 'Odd Pattern', 'capacity': 3}], 'correct_mapping': {'num_e2': 'z_even', 'num_e4': 'z_even', 'num_o1': 'z_odd', 'num_o3': 'z_odd'}},
            correct_answer={'correct_mapping': {'num_e2': 'z_even', 'num_e4': 'z_even', 'num_o1': 'z_odd', 'num_o3': 'z_odd'}},
            explanation={'en': 'Perfect pattern sorting!', 'ar': 'فرز مثالي للأنماط!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.mc.combine_cars',
            objective_key='obj.math.combine_two_groups',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'You have 3 blue cars and 1 red car. How many cars in total?', 'ar': 'لديك ٣ سيارات زرقاء وسيارة حمراء واحدة. كم عدد السيارات الإجمالي؟'},
            content_payload={'question': 'You have 3 blue cars and 1 red car. How many cars in total?', 'options': [{'id': 'opt_4', 'text': '4 Cars 🚗x4', 'visual_cue': '🚗x4', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_3', 'text': '3 Cars 🚗x3', 'visual_cue': '🚗x3', 'is_correct': False, 'distractor_rationale': 'Only the blue cars'}, {'id': 'opt_5', 'text': '5 Cars 🚗x5', 'visual_cue': '🚗x5', 'is_correct': False, 'distractor_rationale': 'Counted one extra'}], 'correct_answer_id': 'opt_4', 'explanation': 'Terrific! 3 blue + 1 red = 4 cars.'},
            correct_answer={'correct_answer_id': 'opt_4'},
            explanation={'en': 'Terrific! 3 blue + 1 red = 4 cars.', 'ar': 'رائع! ٣ زرقاء + ١ حمراء = ٤ سيارات.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.match.combined_counts',
            objective_key='obj.math.combine_two_groups',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each combined pair of groups to its total count.', 'ar': 'طابق كل زوج مجموعات مجمعة بعدده الإجمالي.'},
            content_payload={'prompt': 'Match each combined pair of groups to its total count.', 'left_items': [{'id': 'g_2_3', 'label': '2 Birds + 3 Birds', 'visual_cue': '🐦🐦 + 🐦🐦🐦'}, {'id': 'g_4_2', 'label': '4 Apples + 2 Apples', 'visual_cue': '🍎x4 + 🍎x2'}], 'right_items': [{'id': 't_5', 'label': 'Total: 5', 'visual_cue': '5️⃣'}, {'id': 't_6', 'label': 'Total: 6', 'visual_cue': '6️⃣'}], 'pairs': [{'left_id': 'g_2_3', 'right_id': 't_5'}, {'left_id': 'g_4_2', 'right_id': 't_6'}]},
            correct_answer={'pairs': [{'left_id': 'g_2_3', 'right_id': 't_5'}, {'left_id': 'g_4_2', 'right_id': 't_6'}]},
            explanation={'en': 'Excellent combining! 2+3=5 and 4+2=6.', 'ar': 'تجميع ممتاز! ٢+٣=٥ و ٤+٢=٦.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.vis.spot_combined',
            objective_key='obj.math.combine_two_groups',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the plate that shows 3 cookies combined with 2 cookies (5 total).', 'ar': 'حدد الطبق الذي يظهر ٣ كعكات مجمعة مع كعكتين (٥ إجمالي).'},
            content_payload={'prompt': 'Spot the plate that shows 3 cookies combined with 2 cookies (5 total).', 'scene_description': 'A table with three snack plates.', 'elements': [{'id': 'pl_4', 'label': 'Plate with 4 Cookies 🍪x4', 'category': 'plate', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'pl_5', 'label': 'Plate with 5 Cookies 🍪x5', 'category': 'plate', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'pl_6', 'label': 'Plate with 6 Cookies 🍪x6', 'category': 'plate', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'pl_5', 'feedback_clue': 'Count the cookies on the middle plate: 3 + 2 = 5.'},
            correct_answer={'target_id': 'pl_5'},
            explanation={'en': 'Great! 3 and 2 combined makes 5.', 'ar': 'رائع! ٣ و ٢ معاً يساوي ٥.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.drag.combine_to_box',
            objective_key='obj.math.combine_two_groups',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': 'Combine 2 yellow blocks and 2 blue blocks into the toy box.', 'ar': 'اجمع مكعبين أصفرين ومكعبين أزرقين في صندوق الألعاب.'},
            content_payload={'prompt': 'Combine 2 yellow blocks and 2 blue blocks into the toy box.', 'items': [{'id': 'yb_1', 'label': 'Yellow Block 1 🟨', 'visual_cue': '🟨'}, {'id': 'yb_2', 'label': 'Yellow Block 2 🟨', 'visual_cue': '🟨'}, {'id': 'bb_1', 'label': 'Blue Block 1 🟦', 'visual_cue': '🟦'}, {'id': 'bb_2', 'label': 'Blue Block 2 🟦', 'visual_cue': '🟦'}], 'zones': [{'id': 'box_combined', 'label': 'Combined Toy Box (Total 4)', 'capacity': 4}, {'id': 'box_table', 'label': 'Table Shelf', 'capacity': 2}], 'correct_mapping': {'yb_1': 'box_combined', 'yb_2': 'box_combined', 'bb_1': 'box_combined', 'bb_2': 'box_combined'}},
            correct_answer={'correct_mapping': {'yb_1': 'box_combined', 'yb_2': 'box_combined', 'bb_1': 'box_combined', 'bb_2': 'box_combined'}},
            explanation={'en': 'Super! You combined 2 + 2 = 4 blocks.', 'ar': 'ممتاز! جمعت ٢ + ٢ = ٤ مكعبات.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.mc.model_3plus2',
            objective_key='obj.math.represent_addition_objects',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which model represents adding 3 stars and 2 stars?', 'ar': 'أي نموذج يمثل جمع ٣ نجوم ونجمتين؟'},
            content_payload={'question': 'Which model represents adding 3 stars and 2 stars?', 'options': [{'id': 'opt_3plus2', 'text': '⭐⭐⭐ + ⭐⭐ = 5 Stars', 'visual_cue': '3 + 2 = 5', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_2plus2', 'text': '⭐⭐ + ⭐⭐ = 4 Stars', 'visual_cue': '2 + 2 = 4', 'is_correct': False, 'distractor_rationale': 'Only 2 plus 2'}, {'id': 'opt_4plus2', 'text': '⭐⭐⭐⭐ + ⭐⭐ = 6 Stars', 'visual_cue': '4 + 2 = 6', 'is_correct': False, 'distractor_rationale': 'Starts with 4'}], 'correct_answer_id': 'opt_3plus2', 'explanation': 'Spot on! 3 stars + 2 stars represents 3 + 2 = 5.'},
            correct_answer={'correct_answer_id': 'opt_3plus2'},
            explanation={'en': 'Spot on! 3 stars + 2 stars represents 3 + 2 = 5.', 'ar': 'صحيح! ٣ نجوم + نجمتان تمثل ٣ + ٢ = ٥.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.match.expr_objects',
            objective_key='obj.math.represent_addition_objects',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each addition expression to its object representation.', 'ar': 'طابق كل تعبير جمع بتمثيله بالأشياء.'},
            content_payload={'prompt': 'Match each addition expression to its object representation.', 'left_items': [{'id': 'exp_1_3', 'label': '1 + 3', 'visual_cue': '1️⃣ ➕ 3️⃣'}, {'id': 'exp_2_4', 'label': '2 + 4', 'visual_cue': '2️⃣ ➕ 4️⃣'}], 'right_items': [{'id': 'obj_1_3', 'label': '🔴 + 🔴🔴🔴 (4 Dots)', 'visual_cue': '1 + 3 dots'}, {'id': 'obj_2_4', 'label': '🔴🔴 + 🔴🔴🔴🔴 (6 Dots)', 'visual_cue': '2 + 4 dots'}], 'pairs': [{'left_id': 'exp_1_3', 'right_id': 'obj_1_3'}, {'left_id': 'exp_2_4', 'right_id': 'obj_2_4'}]},
            correct_answer={'pairs': [{'left_id': 'exp_1_3', 'right_id': 'obj_1_3'}, {'left_id': 'exp_2_4', 'right_id': 'obj_2_4'}]},
            explanation={'en': 'Terrific matching of expressions to objects!', 'ar': 'مطابقة رائعة للتعبيرات مع الأشياء!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.vis.bead_frame',
            objective_key='obj.math.represent_addition_objects',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Find the bead frame that represents 4 red beads plus 1 blue bead.', 'ar': 'حدد إطار الخرز الذي يمثل ٤ خرزات حمراء زائد خرزة زرقاء واحدة.'},
            content_payload={'prompt': 'Find the bead frame that represents 4 red beads plus 1 blue bead.', 'scene_description': 'Three counting abacus frames on a desk.', 'elements': [{'id': 'fr_31', 'label': '3 Red + 1 Blue (4 beads)', 'category': 'frame', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'fr_41', 'label': '4 Red + 1 Blue (5 beads)', 'category': 'frame', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'fr_42', 'label': '4 Red + 2 Blue (6 beads)', 'category': 'frame', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'fr_41', 'feedback_clue': 'Look for 4 red beads followed by 1 blue bead.'},
            correct_answer={'target_id': 'fr_41'},
            explanation={'en': 'Great observation! 4 red + 1 blue = 5 beads.', 'ar': 'ملاحظة رائعة! ٤ حمراء + ١ زرقاء = ٥ خرزات.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.order.story_steps',
            objective_key='obj.math.represent_addition_objects',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Sequence the addition story from start to finish.', 'ar': 'رتب قصة الجمع من البداية إلى النهاية.'},
            content_payload={'prompt': 'Sequence the addition story from start to finish.', 'items': [{'id': 'step_add', 'label': 'Add 2 more fish 🐟🐟', 'visual_cue': '➕ 🐟🐟'}, {'id': 'step_start', 'label': 'Start with 2 fish 🐟🐟', 'visual_cue': '🐟🐟'}, {'id': 'step_total', 'label': 'Count 4 fish in total 🐟🐟🐟🐟', 'visual_cue': '🟰 4'}], 'correct_sequence': ['step_start', 'step_add', 'step_total'], 'direction': 'chronological'},
            correct_answer={'correct_sequence': ['step_start', 'step_add', 'step_total']},
            explanation={'en': 'Wonderful story sequencing: start with 2, add 2, total 4.', 'ar': 'تسلسل قصة رائع: نبدأ بـ ٢، نضيف ٢، الإجمالي ٤.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.drag.equation_slots',
            objective_key='obj.math.represent_addition_objects',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': 'Place the counters into the addition equation template (2 + 3 = 5).', 'ar': 'ضع العدادات في قالب معادلة الجمع (٢ + ٣ = ٥).'},
            content_payload={'prompt': 'Place the counters into the addition equation template (2 + 3 = 5).', 'items': [{'id': 'two_dots', 'label': 'Group of 2 Dots 🔴🔴', 'visual_cue': '🔴🔴'}, {'id': 'three_dots', 'label': 'Group of 3 Dots 🔵🔵🔵', 'visual_cue': '🔵🔵🔵'}], 'zones': [{'id': 'slot_first', 'label': 'First Addend [ 2 ]', 'capacity': 1}, {'id': 'slot_second', 'label': 'Second Addend [ 3 ]', 'capacity': 1}], 'correct_mapping': {'two_dots': 'slot_first', 'three_dots': 'slot_second'}},
            correct_answer={'correct_mapping': {'two_dots': 'slot_first', 'three_dots': 'slot_second'}},
            explanation={'en': 'Super! You represented 2 + 3 in the equation frame.', 'ar': 'ممتاز! مثلت ٢ + ٣ في إطار المعادلة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.mc.domino_34',
            objective_key='obj.math.represent_addition_visual_groups',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which domino shows 3 dots on the left and 4 dots on the right?', 'ar': 'أي قطعة دومينو تظهر ٣ نقاط على اليسار و ٤ نقاط على اليمين؟'},
            content_payload={'question': 'Which domino shows 3 dots on the left and 4 dots on the right?', 'options': [{'id': 'dom_3_4', 'text': 'Domino [3 | 4] (Total 7)', 'visual_cue': '🁛', 'is_correct': True, 'distractor_rationale': None}, {'id': 'dom_2_4', 'text': 'Domino [2 | 4] (Total 6)', 'visual_cue': '🁚', 'is_correct': False, 'distractor_rationale': 'Only 2 on left'}, {'id': 'dom_3_3', 'text': 'Domino [3 | 3] (Total 6)', 'visual_cue': '🁙', 'is_correct': False, 'distractor_rationale': 'Double three'}], 'correct_answer_id': 'dom_3_4', 'explanation': 'Correct! The [3 | 4] domino visually groups 3 + 4 = 7.'},
            correct_answer={'correct_answer_id': 'dom_3_4'},
            explanation={'en': 'Correct! The [3 | 4] domino visually groups 3 + 4 = 7.', 'ar': 'صحيح! قطعة الدومينو [٣ | ٤] تجمع بصرياً ٣ + ٤ = ٧.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.match.visual_dominos',
            objective_key='obj.math.represent_addition_visual_groups',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each visual domino group to its total sum.', 'ar': 'طابق كل مجموعة دومينو بصرية بمجموعها الكلي.'},
            content_payload={'prompt': 'Match each visual domino group to its total sum.', 'left_items': [{'id': 'dom_23', 'label': 'Domino [2 | 3]', 'visual_cue': '2 + 3 dots'}, {'id': 'dom_44', 'label': 'Domino [4 | 4]', 'visual_cue': '4 + 4 dots'}], 'right_items': [{'id': 'sum_5', 'label': 'Sum: 5', 'visual_cue': '5️⃣'}, {'id': 'sum_8', 'label': 'Sum: 8', 'visual_cue': '8️⃣'}], 'pairs': [{'left_id': 'dom_23', 'right_id': 'sum_5'}, {'left_id': 'dom_44', 'right_id': 'sum_8'}]},
            correct_answer={'pairs': [{'left_id': 'dom_23', 'right_id': 'sum_5'}, {'left_id': 'dom_44', 'right_id': 'sum_8'}]},
            explanation={'en': 'Great domino addition matching!', 'ar': 'مطابقة ممتازة لجمع الدومينو!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.vis.balloons_32',
            objective_key='obj.math.represent_addition_visual_groups',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Find the balloon bunch showing 3 yellow balloons and 2 green balloons.', 'ar': 'حدد باقة البالونات التي تظهر ٣ بالونات صفراء وبالونين أخضرين.'},
            content_payload={'prompt': 'Find the balloon bunch showing 3 yellow balloons and 2 green balloons.', 'scene_description': 'A birthday party wall with colorful balloon bunches.', 'elements': [{'id': 'bunch_22', 'label': '2 Yellow + 2 Green (4 balloons)', 'category': 'bunch', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'bunch_32', 'label': '3 Yellow + 2 Green (5 balloons)', 'category': 'bunch', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'bunch_33', 'label': '3 Yellow + 3 Green (6 balloons)', 'category': 'bunch', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'bunch_32', 'feedback_clue': 'Look at the center bunch with 3 yellow and 2 green.'},
            correct_answer={'target_id': 'bunch_32'},
            explanation={'en': 'Wonderful! 3 + 2 = 5 balloons.', 'ar': 'رائع! ٣ + ٢ = ٥ بالونات.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.drag.sort_sum_groups',
            objective_key='obj.math.represent_addition_visual_groups',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort the visual groups into 'Sum is 5' and 'Sum is 6'.", 'ar': "صنف المجموعات البصرية إلى 'المجموع ٥' و 'المجموع ٦'."},
            content_payload={'prompt': "Sort the visual groups into 'Sum is 5' and 'Sum is 6'.", 'items': [{'id': 'grp_41', 'label': '4 Apples + 1 Apple', 'visual_cue': '🍎x4 + 🍎'}, {'id': 'grp_23', 'label': '2 Stars + 3 Stars', 'visual_cue': '⭐x2 + ⭐x3'}, {'id': 'grp_33', 'label': '3 Dots + 3 Dots', 'visual_cue': '🔵x3 + 🔵x3'}, {'id': 'grp_51', 'label': '5 Hearts + 1 Heart', 'visual_cue': '❤️x5 + ❤️'}], 'zones': [{'id': 'z_sum5', 'label': 'Sum = 5', 'capacity': 3}, {'id': 'z_sum6', 'label': 'Sum = 6', 'capacity': 3}], 'correct_mapping': {'grp_41': 'z_sum5', 'grp_23': 'z_sum5', 'grp_33': 'z_sum6', 'grp_51': 'z_sum6'}},
            correct_answer={'correct_mapping': {'grp_41': 'z_sum5', 'grp_23': 'z_sum5', 'grp_33': 'z_sum6', 'grp_51': 'z_sum6'}},
            explanation={'en': 'Accurate visual sum grouping!', 'ar': 'تصنيف دقيق للمجاميع البصرية!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.mc.ladybug_equation',
            objective_key='obj.math.represent_addition_visual_groups',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Look at 4 red ladybugs and 2 green beetles. What addition sentence does this show?', 'ar': 'انظر إلى ٤ دعسوقات حمراء وخنفساءين خضراوين. ما جملة الجمع التي يمثلها ذلك؟'},
            content_payload={'question': 'Look at 4 red ladybugs and 2 green beetles. What addition sentence does this show?', 'options': [{'id': 'sent_42', 'text': '4 + 2 = 6', 'visual_cue': '🐞x4 + 🪲x2 = 6', 'is_correct': True, 'distractor_rationale': None}, {'id': 'sent_32', 'text': '3 + 2 = 5', 'visual_cue': '🐞x3 + 🪲x2 = 5', 'is_correct': False, 'distractor_rationale': 'Only 3 ladybugs counted'}, {'id': 'sent_43', 'text': '4 + 3 = 7', 'visual_cue': '🐞x4 + 🪲x3 = 7', 'is_correct': False, 'distractor_rationale': 'Counted 3 beetles'}], 'correct_answer_id': 'sent_42', 'explanation': 'Terrific! 4 + 2 = 6 insects.'},
            correct_answer={'correct_answer_id': 'sent_42'},
            explanation={'en': 'Terrific! 4 + 2 = 6 insects.', 'ar': 'رائع! ٤ + ٢ = ٦ حشرات.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.mc.eq_5plus3',
            objective_key='obj.math.solve_addition_equations_10',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=3,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Solve: 5 + 3 = ?', 'ar': 'حل المسألة: ٥ + ٣ = ؟'},
            content_payload={'question': 'Solve: 5 + 3 = ?', 'options': [{'id': 'ans_8', 'text': '8', 'visual_cue': '8️⃣', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_7', 'text': '7', 'visual_cue': '7️⃣', 'is_correct': False, 'distractor_rationale': 'One less'}, {'id': 'ans_9', 'text': '9', 'visual_cue': '9️⃣', 'is_correct': False, 'distractor_rationale': 'One more'}], 'correct_answer_id': 'ans_8', 'explanation': 'Correct! 5 + 3 = 8.'},
            correct_answer={'correct_answer_id': 'ans_8'},
            explanation={'en': 'Correct! 5 + 3 = 8.', 'ar': 'صحيح! ٥ + ٣ = ٨.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.mc.eq_6plus4',
            objective_key='obj.math.solve_addition_equations_10',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=3,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Solve: 6 + 4 = ?', 'ar': 'حل المسألة: ٦ + ٤ = ؟'},
            content_payload={'question': 'Solve: 6 + 4 = ?', 'options': [{'id': 'ans_10', 'text': '10', 'visual_cue': '🔟', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_9', 'text': '9', 'visual_cue': '9️⃣', 'is_correct': False, 'distractor_rationale': 'Missed one'}, {'id': 'ans_8', 'text': '8', 'visual_cue': '8️⃣', 'is_correct': False, 'distractor_rationale': 'Under-calculated'}], 'correct_answer_id': 'ans_10', 'explanation': 'Super! 6 + 4 = 10.'},
            correct_answer={'correct_answer_id': 'ans_10'},
            explanation={'en': 'Super! 6 + 4 = 10.', 'ar': 'ممتاز! ٦ + ٤ = ١٠.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.match.equations_answers',
            objective_key='obj.math.solve_addition_equations_10',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=3,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each addition equation to its correct sum.', 'ar': 'طابق كل معادلة جمع بمجموعها الصحيح.'},
            content_payload={'prompt': 'Match each addition equation to its correct sum.', 'left_items': [{'id': 'eq_34', 'label': '3 + 4', 'visual_cue': '3 + 4'}, {'id': 'eq_44', 'label': '4 + 4', 'visual_cue': '4 + 4'}], 'right_items': [{'id': 's_7', 'label': '7', 'visual_cue': '7️⃣'}, {'id': 's_8', 'label': '8', 'visual_cue': '8️⃣'}], 'pairs': [{'left_id': 'eq_34', 'right_id': 's_7'}, {'left_id': 'eq_44', 'right_id': 's_8'}]},
            correct_answer={'pairs': [{'left_id': 'eq_34', 'right_id': 's_7'}, {'left_id': 'eq_44', 'right_id': 's_8'}]},
            explanation={'en': 'Great equation solving!', 'ar': 'حل ممتاز للمعادلات!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.drag.sort_by_sum',
            objective_key='obj.math.solve_addition_equations_10',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=3,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort equations into 'Sum is 7' and 'Sum is 9'.", 'ar': "صنف المعادلات إلى 'المجموع ٧' و 'المجموع ٩'."},
            content_payload={'prompt': "Sort equations into 'Sum is 7' and 'Sum is 9'.", 'items': [{'id': 'eq_52', 'label': '5 + 2', 'visual_cue': '5 + 2'}, {'id': 'eq_61', 'label': '6 + 1', 'visual_cue': '6 + 1'}, {'id': 'eq_54', 'label': '5 + 4', 'visual_cue': '5 + 4'}, {'id': 'eq_72', 'label': '7 + 2', 'visual_cue': '7 + 2'}], 'zones': [{'id': 'z_s7', 'label': 'Sum = 7', 'capacity': 3}, {'id': 'z_s9', 'label': 'Sum = 9', 'capacity': 3}], 'correct_mapping': {'eq_52': 'z_s7', 'eq_61': 'z_s7', 'eq_54': 'z_s9', 'eq_72': 'z_s9'}},
            correct_answer={'correct_mapping': {'eq_52': 'z_s7', 'eq_61': 'z_s7', 'eq_54': 'z_s9', 'eq_72': 'z_s9'}},
            explanation={'en': 'Wonderful classification of sums!', 'ar': 'تصنيف رائع للمجاميع!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.mc.plus1_4',
            objective_key='obj.math.add_plus_1',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'What is 4 + 1?', 'ar': 'ما حاصل ٤ + ١؟'},
            content_payload={'question': 'What is 4 + 1?', 'options': [{'id': 'opt_5', 'text': '5', 'visual_cue': '5️⃣', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_3', 'text': '3', 'visual_cue': '3️⃣', 'is_correct': False, 'distractor_rationale': 'Subtracted 1'}, {'id': 'opt_6', 'text': '6', 'visual_cue': '6️⃣', 'is_correct': False, 'distractor_rationale': 'Added 2'}], 'correct_answer_id': 'opt_5', 'explanation': 'Correct! Adding 1 to 4 gives 5.'},
            correct_answer={'correct_answer_id': 'opt_5'},
            explanation={'en': 'Correct! Adding 1 to 4 gives 5.', 'ar': 'صحيح! إضافة ١ إلى ٤ يعطي ٥.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.mc.plus1_7',
            objective_key='obj.math.add_plus_1',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'What is 7 + 1?', 'ar': 'ما حاصل ٧ + ١؟'},
            content_payload={'question': 'What is 7 + 1?', 'options': [{'id': 'opt_8', 'text': '8', 'visual_cue': '8️⃣', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_6', 'text': '6', 'visual_cue': '6️⃣', 'is_correct': False, 'distractor_rationale': 'Subtracted 1'}, {'id': 'opt_9', 'text': '9', 'visual_cue': '9️⃣', 'is_correct': False, 'distractor_rationale': 'Added 2'}], 'correct_answer_id': 'opt_8', 'explanation': 'Super! 7 + 1 = 8.'},
            correct_answer={'correct_answer_id': 'opt_8'},
            explanation={'en': 'Super! 7 + 1 = 8.', 'ar': 'ممتاز! ٧ + ١ = ٨.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.match.plus1_pairs',
            objective_key='obj.math.add_plus_1',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each number to the result of adding 1.', 'ar': 'طابق كل رقم بناتج إضافة ١.'},
            content_payload={'prompt': 'Match each number to the result of adding 1.', 'left_items': [{'id': 'n_3', 'label': '3 + 1', 'visual_cue': '3 + 1'}, {'id': 'n_6', 'label': '6 + 1', 'visual_cue': '6 + 1'}, {'id': 'n_8', 'label': '8 + 1', 'visual_cue': '8 + 1'}], 'right_items': [{'id': 'r_4', 'label': 'Result: 4', 'visual_cue': '4️⃣'}, {'id': 'r_7', 'label': 'Result: 7', 'visual_cue': '7️⃣'}, {'id': 'r_9', 'label': 'Result: 9', 'visual_cue': '9️⃣'}], 'pairs': [{'left_id': 'n_3', 'right_id': 'r_4'}, {'left_id': 'n_6', 'right_id': 'r_7'}, {'left_id': 'n_8', 'right_id': 'r_9'}]},
            correct_answer={'pairs': [{'left_id': 'n_3', 'right_id': 'r_4'}, {'left_id': 'n_6', 'right_id': 'r_7'}, {'left_id': 'n_8', 'right_id': 'r_9'}]},
            explanation={'en': 'Great work! Adding 1 gives the immediate next number.', 'ar': 'عمل رائع! إضافة ١ تعطي الرقم التالي مباشرة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.vis.numline_plus1',
            objective_key='obj.math.add_plus_1',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the number on the number line that is 1 more than 5.', 'ar': 'حدد الرقم على خط الأعداد الذي يزيد بمقدار ١ عن الرقم ٥.'},
            content_payload={'prompt': 'Spot the number on the number line that is 1 more than 5.', 'scene_description': 'A horizontal number line marked 1 through 10.', 'elements': [{'id': 'nl_4', 'label': 'Number 4', 'category': 'number', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'nl_6', 'label': 'Number 6', 'category': 'number', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'nl_7', 'label': 'Number 7', 'category': 'number', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'nl_6', 'feedback_clue': 'Hop 1 step forward from 5 on the number line.'},
            correct_answer={'target_id': 'nl_6'},
            explanation={'en': 'Spot on! 1 step forward from 5 lands on 6.', 'ar': 'صحيح! قفزة واحدة للأمام من ٥ تصل إلى ٦.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.order.plus1_steps',
            objective_key='obj.math.add_plus_1',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Order consecutive steps: 5, then +1 to get 6, then +1 to get 7.', 'ar': 'رتب الخطوات المتتالية: ٥، ثم +١ للحصول على ٦، ثم +١ للحصول على ٧.'},
            content_payload={'prompt': 'Order consecutive steps: 5, then +1 to get 6, then +1 to get 7.', 'items': [{'id': 'st_6', 'label': '6 (5 + 1)', 'visual_cue': '6️⃣'}, {'id': 'st_5', 'label': '5 (Start)', 'visual_cue': '5️⃣'}, {'id': 'st_7', 'label': '7 (6 + 1)', 'visual_cue': '7️⃣'}], 'correct_sequence': ['st_5', 'st_6', 'st_7'], 'direction': 'ascending'},
            correct_answer={'correct_sequence': ['st_5', 'st_6', 'st_7']},
            explanation={'en': 'Terrific! 5, 6, 7 stepping by 1.', 'ar': 'رائع! ٥، ٦، ٧ بالتقدم بمقدار ١.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.mc.plus2_3',
            objective_key='obj.math.add_plus_2_or_more',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=3,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'What is 3 + 2?', 'ar': 'ما حاصل ٣ + ٢؟'},
            content_payload={'question': 'What is 3 + 2?', 'options': [{'id': 'ans_5', 'text': '5', 'visual_cue': '5️⃣', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_4', 'text': '4', 'visual_cue': '4️⃣', 'is_correct': False, 'distractor_rationale': 'Only added 1'}, {'id': 'ans_6', 'text': '6', 'visual_cue': '6️⃣', 'is_correct': False, 'distractor_rationale': 'Added 3'}], 'correct_answer_id': 'ans_5', 'explanation': 'Correct! 3 + 2 = 5.'},
            correct_answer={'correct_answer_id': 'ans_5'},
            explanation={'en': 'Correct! 3 + 2 = 5.', 'ar': 'صحيح! ٣ + ٢ = ٥.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.mc.plus3_5',
            objective_key='obj.math.add_plus_2_or_more',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=3,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'What is 5 + 3?', 'ar': 'ما حاصل ٥ + ٣؟'},
            content_payload={'question': 'What is 5 + 3?', 'options': [{'id': 'ans_8', 'text': '8', 'visual_cue': '8️⃣', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_7', 'text': '7', 'visual_cue': '7️⃣', 'is_correct': False, 'distractor_rationale': 'Only added 2'}, {'id': 'ans_9', 'text': '9', 'visual_cue': '9️⃣', 'is_correct': False, 'distractor_rationale': 'Added 4'}], 'correct_answer_id': 'ans_8', 'explanation': 'Super! 5 + 3 = 8.'},
            correct_answer={'correct_answer_id': 'ans_8'},
            explanation={'en': 'Super! 5 + 3 = 8.', 'ar': 'ممتاز! ٥ + ٣ = ٨.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.match.plus2_pairs',
            objective_key='obj.math.add_plus_2_or_more',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=3,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each plus-2 expression to its answer.', 'ar': 'طابق كل مسألة إضافة ٢ بناتجها.'},
            content_payload={'prompt': 'Match each plus-2 expression to its answer.', 'left_items': [{'id': 'e_22', 'label': '2 + 2', 'visual_cue': '2 + 2'}, {'id': 'e_42', 'label': '4 + 2', 'visual_cue': '4 + 2'}, {'id': 'e_62', 'label': '6 + 2', 'visual_cue': '6 + 2'}], 'right_items': [{'id': 'a_4', 'label': '4', 'visual_cue': '4️⃣'}, {'id': 'a_6', 'label': '6', 'visual_cue': '6️⃣'}, {'id': 'a_8', 'label': '8', 'visual_cue': '8️⃣'}], 'pairs': [{'left_id': 'e_22', 'right_id': 'a_4'}, {'left_id': 'e_42', 'right_id': 'a_6'}, {'left_id': 'e_62', 'right_id': 'a_8'}]},
            correct_answer={'pairs': [{'left_id': 'e_22', 'right_id': 'a_4'}, {'left_id': 'e_42', 'right_id': 'a_6'}, {'left_id': 'e_62', 'right_id': 'a_8'}]},
            explanation={'en': 'Great work! 2+2=4, 4+2=6, 6+2=8.', 'ar': 'عمل رائع! ٢+٢=٤، ٤+٢=٦، ٦+٢=٨.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.vis.jump_plus2',
            objective_key='obj.math.add_plus_2_or_more',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=3,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the jumping frog landing on 6 after leaping +2 from 4.', 'ar': 'حدد الضفدع الذي يقفز ليصل إلى ٦ بعد قفزة +٢ من ٤.'},
            content_payload={'prompt': 'Spot the jumping frog landing on 6 after leaping +2 from 4.', 'scene_description': 'A pond with lily pads numbered 1 to 8.', 'elements': [{'id': 'frog_5', 'label': 'Frog on Pad 5 (Jumped 1)', 'category': 'pad', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'frog_6', 'label': 'Frog on Pad 6 (Jumped 2)', 'category': 'pad', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'frog_7', 'label': 'Frog on Pad 7 (Jumped 3)', 'category': 'pad', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'frog_6', 'feedback_clue': 'Look for the pad showing 4 + 2 = 6.'},
            correct_answer={'target_id': 'frog_6'},
            explanation={'en': 'Brilliant! 4 plus 2 jumps lands on 6.', 'ar': 'رائع! ٤ مع قفزتين تصل إلى ٦.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.add.drag.sort_plus2_plus3',
            objective_key='obj.math.add_plus_2_or_more',
            subject_code='math',
            unit_code='unit.math.addition_within_10',
            difficulty_level=3,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort expressions into 'Add 2' and 'Add 3'.", 'ar': "صنف التعبيرات إلى 'إضافة ٢' و 'إضافة ٣'."},
            content_payload={'prompt': "Sort expressions into 'Add 2' and 'Add 3'.", 'items': [{'id': 'ex_32', 'label': '3 + 2', 'visual_cue': '3 + 2'}, {'id': 'ex_52', 'label': '5 + 2', 'visual_cue': '5 + 2'}, {'id': 'ex_23', 'label': '2 + 3', 'visual_cue': '2 + 3'}, {'id': 'ex_43', 'label': '4 + 3', 'visual_cue': '4 + 3'}], 'zones': [{'id': 'z_p2', 'label': 'Adding 2', 'capacity': 3}, {'id': 'z_p3', 'label': 'Adding 3', 'capacity': 3}], 'correct_mapping': {'ex_32': 'z_p2', 'ex_52': 'z_p2', 'ex_23': 'z_p3', 'ex_43': 'z_p3'}},
            correct_answer={'correct_mapping': {'ex_32': 'z_p2', 'ex_52': 'z_p2', 'ex_23': 'z_p3', 'ex_43': 'z_p3'}},
            explanation={'en': 'Terrific sorting by added quantity!', 'ar': 'فرز رائع حسب الكمية المضافة!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.mc.birds_leave',
            objective_key='obj.math.remove_objects_group',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'There are 5 birds on a wire. 2 birds fly away. How many birds remain?', 'ar': 'هناك ٥ طيور على سلك. طار طائران. كم طائراً بقي؟'},
            content_payload={'question': 'There are 5 birds on a wire. 2 birds fly away. How many birds remain?', 'options': [{'id': 'ans_3', 'text': '3 Birds 🐦🐦🐦', 'visual_cue': '🐦🐦🐦', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_2', 'text': '2 Birds 🐦🐦', 'visual_cue': '🐦🐦', 'is_correct': False, 'distractor_rationale': 'Count of birds that flew away'}, {'id': 'ans_4', 'text': '4 Birds 🐦x4', 'visual_cue': '🐦x4', 'is_correct': False, 'distractor_rationale': 'Only subtracted 1'}], 'correct_answer_id': 'ans_3', 'explanation': 'Correct! 5 - 2 = 3 birds remain.'},
            correct_answer={'correct_answer_id': 'ans_3'},
            explanation={'en': 'Correct! 5 - 2 = 3 birds remain.', 'ar': 'صحيح! ٥ - ٢ = ٣ طيور باقية.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.mc.cookies_eat',
            objective_key='obj.math.remove_objects_group',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'There are 4 cookies. You eat 1 cookie. How many cookies are left?', 'ar': 'هناك ٤ قطع كعك. أكلت قطعة واحدة. كم قطعة كعك بقيت؟'},
            content_payload={'question': 'There are 4 cookies. You eat 1 cookie. How many cookies are left?', 'options': [{'id': 'c_3', 'text': '3 Cookies 🍪🍪🍪', 'visual_cue': '🍪🍪🍪', 'is_correct': True, 'distractor_rationale': None}, {'id': 'c_2', 'text': '2 Cookies 🍪🍪', 'visual_cue': '🍪🍪', 'is_correct': False, 'distractor_rationale': 'Subtracted 2'}, {'id': 'c_4', 'text': '4 Cookies 🍪x4', 'visual_cue': '🍪x4', 'is_correct': False, 'distractor_rationale': 'Did not subtract'}], 'correct_answer_id': 'c_3', 'explanation': 'Super! 4 - 1 = 3 cookies left.'},
            correct_answer={'correct_answer_id': 'c_3'},
            explanation={'en': 'Super! 4 - 1 = 3 cookies left.', 'ar': 'ممتاز! ٤ - ١ = ٣ قطع كعك متبقية.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.match.stories',
            objective_key='obj.math.remove_objects_group',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each removal story to the remaining count.', 'ar': 'طابق كل قصة إنقاص بالعدد المتبقي.'},
            content_payload={'prompt': 'Match each removal story to the remaining count.', 'left_items': [{'id': 'st_6_2', 'label': '6 cars, 2 drive away', 'visual_cue': '🚗x6 - 🚗x2'}, {'id': 'st_5_3', 'label': '5 apples, 3 eaten', 'visual_cue': '🍎x5 - 🍎x3'}], 'right_items': [{'id': 'rem_4', 'label': '4 Remain', 'visual_cue': '4️⃣'}, {'id': 'rem_2', 'label': '2 Remain', 'visual_cue': '2️⃣'}], 'pairs': [{'left_id': 'st_6_2', 'right_id': 'rem_4'}, {'left_id': 'st_5_3', 'right_id': 'rem_2'}]},
            correct_answer={'pairs': [{'left_id': 'st_6_2', 'right_id': 'rem_4'}, {'left_id': 'st_5_3', 'right_id': 'rem_2'}]},
            explanation={'en': 'Great removal matching!', 'ar': 'مطابقة ممتازة لعمليات الإنقاص!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.vis.tray_muffins',
            objective_key='obj.math.remove_objects_group',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the bakery tray where 2 muffins were taken from 5 (3 left).', 'ar': 'حدد صينية المخبز التي أخذ منها كعكتان من أصل ٥ (بقي ٣).'},
            content_payload={'prompt': 'Spot the bakery tray where 2 muffins were taken from 5 (3 left).', 'scene_description': 'A bakery display counter with muffin trays.', 'elements': [{'id': 'tr_2left', 'label': 'Tray with 2 Left 🧁🧁', 'category': 'tray', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'tr_3left', 'label': 'Tray with 3 Left 🧁🧁🧁', 'category': 'tray', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'tr_4left', 'label': 'Tray with 4 Left 🧁x4', 'category': 'tray', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'tr_3left', 'feedback_clue': 'Look for the tray showing 3 remaining muffins.'},
            correct_answer={'target_id': 'tr_3left'},
            explanation={'en': 'Wonderful! 5 minus 2 leaves 3 muffins.', 'ar': 'رائع! ٥ ناقص ٢ يتبقى ٣ كعكات.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.drag.remove_to_bin',
            objective_key='obj.math.remove_objects_group',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Remove 2 crossed-out items by dragging them into the 'Taken Away' box.", 'ar': "أزل العنصرين المشطوبين بسحبهما إلى صندوق 'تم أخذها'."},
            content_payload={'prompt': "Remove 2 crossed-out items by dragging them into the 'Taken Away' box.", 'items': [{'id': 'item_x1', 'label': 'Crossed Out Star ❌⭐', 'visual_cue': '❌⭐'}, {'id': 'item_x2', 'label': 'Crossed Out Star ❌⭐', 'visual_cue': '❌⭐'}], 'zones': [{'id': 'box_taken', 'label': 'Taken Away Box', 'capacity': 2}, {'id': 'box_remain', 'label': 'Remaining Items', 'capacity': 3}], 'correct_mapping': {'item_x1': 'box_taken', 'item_x2': 'box_taken'}},
            correct_answer={'correct_mapping': {'item_x1': 'box_taken', 'item_x2': 'box_taken'}},
            explanation={'en': 'Super! You separated the removed objects.', 'ar': 'ممتاز! فصلت العناصر المزالة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.mc.crossed_dots',
            objective_key='obj.math.represent_subtraction_visually',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which model represents 5 minus 2?', 'ar': 'أي نموذج يمثل ٥ ناقص ٢؟'},
            content_payload={'question': 'Which model represents 5 minus 2?', 'options': [{'id': 'opt_5m2', 'text': '🔴🔴🔴❌❌ (5 dots, 2 crossed out)', 'visual_cue': '5 - 2', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_5m1', 'text': '🔴🔴🔴🔴❌ (5 dots, 1 crossed out)', 'visual_cue': '5 - 1', 'is_correct': False, 'distractor_rationale': 'Only 1 crossed out'}, {'id': 'opt_4m2', 'text': '🔴🔴❌❌ (4 dots, 2 crossed out)', 'visual_cue': '4 - 2', 'is_correct': False, 'distractor_rationale': 'Started with only 4'}], 'correct_answer_id': 'opt_5m2', 'explanation': 'Spot on! 5 dots with 2 crossed out represents 5 - 2 = 3.'},
            correct_answer={'correct_answer_id': 'opt_5m2'},
            explanation={'en': 'Spot on! 5 dots with 2 crossed out represents 5 - 2 = 3.', 'ar': 'صحيح! ٥ نقاط مع شطب ٢ تمثل ٥ - ٢ = ٣.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.match.sub_diagrams',
            objective_key='obj.math.represent_subtraction_visually',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each subtraction sentence to its crossed-out diagram.', 'ar': 'طابق كل جملة طرح برسمها المشطوب.'},
            content_payload={'prompt': 'Match each subtraction sentence to its crossed-out diagram.', 'left_items': [{'id': 's_4_1', 'label': '4 - 1', 'visual_cue': '4 - 1'}, {'id': 's_6_3', 'label': '6 - 3', 'visual_cue': '6 - 3'}], 'right_items': [{'id': 'd_4_1', 'label': '🔵🔵🔵❌ (4 total, 1 crossed)', 'visual_cue': '4-1'}, {'id': 'd_6_3', 'label': '🔵🔵🔵❌❌❌ (6 total, 3 crossed)', 'visual_cue': '6-3'}], 'pairs': [{'left_id': 's_4_1', 'right_id': 'd_4_1'}, {'left_id': 's_6_3', 'right_id': 'd_6_3'}]},
            correct_answer={'pairs': [{'left_id': 's_4_1', 'right_id': 'd_4_1'}, {'left_id': 's_6_3', 'right_id': 'd_6_3'}]},
            explanation={'en': 'Great matching of subtraction models!', 'ar': 'مطابقة رائعة لنماذج الطرح!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.vis.tenframe_sub',
            objective_key='obj.math.represent_subtraction_visually',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Find the ten-frame showing 6 circles with 2 crossed out.', 'ar': 'حدد إطار العشرة الذي يظهر ٦ دوائر مع شطب دائرتين.'},
            content_payload={'prompt': 'Find the ten-frame showing 6 circles with 2 crossed out.', 'scene_description': 'Three ten-frame grids with counters.', 'elements': [{'id': 'tf_6_1', 'label': '6 Counters (1 crossed)', 'category': 'frame', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'tf_6_2', 'label': '6 Counters (2 crossed)', 'category': 'frame', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'tf_6_3', 'label': '6 Counters (3 crossed)', 'category': 'frame', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'tf_6_2', 'feedback_clue': 'Look at the center ten-frame with exactly two crossed circles.'},
            correct_answer={'target_id': 'tf_6_2'},
            explanation={'en': 'Excellent! 6 with 2 crossed out leaves 4.', 'ar': 'ممتاز! ٦ مع شطب ٢ يتبقى ٤.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.order.pop_balloons',
            objective_key='obj.math.represent_subtraction_visually',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Sequence the subtraction event: start with 4 balloons, 1 pops, 3 remain.', 'ar': 'رتب حدث الطرح: نبدأ بـ ٤ بالونات، ينفجر ١، يتبقى ٣.'},
            content_payload={'prompt': 'Sequence the subtraction event: start with 4 balloons, 1 pops, 3 remain.', 'items': [{'id': 'st_pop', 'label': '1 Balloon Pops 💥🎈', 'visual_cue': '💥'}, {'id': 'st_have', 'label': 'Have 4 Balloons 🎈x4', 'visual_cue': '🎈x4'}, {'id': 'st_left', 'label': '3 Balloons Remain 🎈x3', 'visual_cue': '🎈x3'}], 'correct_sequence': ['st_have', 'st_pop', 'st_left'], 'direction': 'chronological'},
            correct_answer={'correct_sequence': ['st_have', 'st_pop', 'st_left']},
            explanation={'en': 'Terrific subtraction sequence!', 'ar': 'تسلسل طرح رائع!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.drag.sort_takeaway',
            objective_key='obj.math.represent_subtraction_visually',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort diagrams into 'Take Away 1' and 'Take Away 2'.", 'ar': "صنف الرسوم إلى 'إنقاص ١' و 'إنقاص ٢'."},
            content_payload={'prompt': "Sort diagrams into 'Take Away 1' and 'Take Away 2'.", 'items': [{'id': 'dg_31', 'label': '3 Dots (1 Crossed)', 'visual_cue': '⚫⚫❌'}, {'id': 'dg_51', 'label': '5 Dots (1 Crossed)', 'visual_cue': '⚫x4 ❌'}, {'id': 'dg_42', 'label': '4 Dots (2 Crossed)', 'visual_cue': '⚫⚫❌❌'}, {'id': 'dg_62', 'label': '6 Dots (2 Crossed)', 'visual_cue': '⚫x4 ❌❌'}], 'zones': [{'id': 'z_sub1', 'label': 'Take Away 1', 'capacity': 3}, {'id': 'z_sub2', 'label': 'Take Away 2', 'capacity': 3}], 'correct_mapping': {'dg_31': 'z_sub1', 'dg_51': 'z_sub1', 'dg_42': 'z_sub2', 'dg_62': 'z_sub2'}},
            correct_answer={'correct_mapping': {'dg_31': 'z_sub1', 'dg_51': 'z_sub1', 'dg_42': 'z_sub2', 'dg_62': 'z_sub2'}},
            explanation={'en': 'Brilliant categorization of subtraction amounts!', 'ar': 'تصنيف رائع لمقادير الطرح!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.mc.remain_marbles',
            objective_key='obj.math.identify_remaining_objects',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Start with 7 marbles. Give 3 to a friend. How many marbles do you have left?', 'ar': 'بدأت بـ ٧ كرات زجاجية. أعطيت ٣ لصديق. كم كرة بقيت معك؟'},
            content_payload={'question': 'Start with 7 marbles. Give 3 to a friend. How many marbles do you have left?', 'options': [{'id': 'opt_4', 'text': '4 Marbles ⚪x4', 'visual_cue': '⚪x4', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_3', 'text': '3 Marbles ⚪x3', 'visual_cue': '⚪x3', 'is_correct': False, 'distractor_rationale': 'Number given away'}, {'id': 'opt_5', 'text': '5 Marbles ⚪x5', 'visual_cue': '⚪x5', 'is_correct': False, 'distractor_rationale': 'Only gave 2 away'}], 'correct_answer_id': 'opt_4', 'explanation': 'Correct! 7 - 3 = 4 marbles left.'},
            correct_answer={'correct_answer_id': 'opt_4'},
            explanation={'en': 'Correct! 7 - 3 = 4 marbles left.', 'ar': 'صحيح! ٧ - ٣ = ٤ كرات باقية.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.mc.remain_cupcakes',
            objective_key='obj.math.identify_remaining_objects',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Start with 8 cupcakes. 4 are eaten. How many cupcakes remain?', 'ar': 'بدأت بـ ٨ كب كيك. أكل ٤ منها. كم كب كيك بقي؟'},
            content_payload={'question': 'Start with 8 cupcakes. 4 are eaten. How many cupcakes remain?', 'options': [{'id': 'ans_4', 'text': '4 Cupcakes 🧁x4', 'visual_cue': '🧁x4', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_5', 'text': '5 Cupcakes 🧁x5', 'visual_cue': '🧁x5', 'is_correct': False, 'distractor_rationale': 'One too many'}, {'id': 'ans_3', 'text': '3 Cupcakes 🧁x3', 'visual_cue': '🧁x3', 'is_correct': False, 'distractor_rationale': 'One too few'}], 'correct_answer_id': 'ans_4', 'explanation': 'Super! 8 - 4 = 4 cupcakes remain.'},
            correct_answer={'correct_answer_id': 'ans_4'},
            explanation={'en': 'Super! 8 - 4 = 4 cupcakes remain.', 'ar': 'ممتاز! ٨ - ٤ = ٤ كب كيك متبقية.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.match.remain_pairs',
            objective_key='obj.math.identify_remaining_objects',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match starting minus taken to the remaining count.', 'ar': 'طابق العدد الأصلي مطروحاً منه المأخوذ بالعدد المتبقي.'},
            content_payload={'prompt': 'Match starting minus taken to the remaining count.', 'left_items': [{'id': 'op_9_4', 'label': 'Start 9, Take 4', 'visual_cue': '9 - 4'}, {'id': 'op_8_2', 'label': 'Start 8, Take 2', 'visual_cue': '8 - 2'}], 'right_items': [{'id': 'r_5', 'label': '5 Remain', 'visual_cue': '5️⃣'}, {'id': 'r_6', 'label': '6 Remain', 'visual_cue': '6️⃣'}], 'pairs': [{'left_id': 'op_9_4', 'right_id': 'r_5'}, {'left_id': 'op_8_2', 'right_id': 'r_6'}]},
            correct_answer={'pairs': [{'left_id': 'op_9_4', 'right_id': 'r_5'}, {'left_id': 'op_8_2', 'right_id': 'r_6'}]},
            explanation={'en': 'Accurate remaining count matching!', 'ar': 'مطابقة دقيقة للأعداد المتبقية!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.vis.uncrossed_stars',
            objective_key='obj.math.identify_remaining_objects',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Count the uncrossed stars: 7 stars total, 2 crossed out. Spot the number 5.', 'ar': 'عد النجوم غير المشطوبة: ٧ نجوم إجمالي، ٢ مشطوبتان. حدد الرقم ٥.'},
            content_payload={'prompt': 'Count the uncrossed stars: 7 stars total, 2 crossed out. Spot the number 5.', 'scene_description': 'A chalkboard with a star problem and answer choices.', 'elements': [{'id': 'ans_c4', 'label': 'Number 4', 'category': 'number', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'ans_c5', 'label': 'Number 5', 'category': 'number', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'ans_c6', 'label': 'Number 6', 'category': 'number', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'ans_c5', 'feedback_clue': 'Count the active stars: 5 uncrossed stars remain.'},
            correct_answer={'target_id': 'ans_c5'},
            explanation={'en': 'Terrific! 7 - 2 leaves 5 uncrossed stars.', 'ar': 'رائع! ٧ - ٢ يتبقى ٥ نجوم غير مشطوبة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.mc.eq_8m3',
            objective_key='obj.math.solve_subtraction_equations_10',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=3,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Solve: 8 - 3 = ?', 'ar': 'حل المسألة: ٨ - ٣ = ؟'},
            content_payload={'question': 'Solve: 8 - 3 = ?', 'options': [{'id': 'opt_5', 'text': '5', 'visual_cue': '5️⃣', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_4', 'text': '4', 'visual_cue': '4️⃣', 'is_correct': False, 'distractor_rationale': 'Subtracted 4'}, {'id': 'opt_6', 'text': '6', 'visual_cue': '6️⃣', 'is_correct': False, 'distractor_rationale': 'Subtracted 2'}], 'correct_answer_id': 'opt_5', 'explanation': 'Correct! 8 - 3 = 5.'},
            correct_answer={'correct_answer_id': 'opt_5'},
            explanation={'en': 'Correct! 8 - 3 = 5.', 'ar': 'صحيح! ٨ - ٣ = ٥.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.mc.eq_9m4',
            objective_key='obj.math.solve_subtraction_equations_10',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=3,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Solve: 9 - 4 = ?', 'ar': 'حل المسألة: ٩ - ٤ = ؟'},
            content_payload={'question': 'Solve: 9 - 4 = ?', 'options': [{'id': 'opt_5', 'text': '5', 'visual_cue': '5️⃣', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_6', 'text': '6', 'visual_cue': '6️⃣', 'is_correct': False, 'distractor_rationale': 'Subtracted 3'}, {'id': 'opt_4', 'text': '4', 'visual_cue': '4️⃣', 'is_correct': False, 'distractor_rationale': 'Subtracted 5'}], 'correct_answer_id': 'opt_5', 'explanation': 'Super! 9 - 4 = 5.'},
            correct_answer={'correct_answer_id': 'opt_5'},
            explanation={'en': 'Super! 9 - 4 = 5.', 'ar': 'ممتاز! ٩ - ٤ = ٥.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.match.eq_answers',
            objective_key='obj.math.solve_subtraction_equations_10',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=3,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each subtraction equation to its correct result.', 'ar': 'طابق كل معادلة طرح بنتيجتها الصحيحة.'},
            content_payload={'prompt': 'Match each subtraction equation to its correct result.', 'left_items': [{'id': 'sub_7_2', 'label': '7 - 2', 'visual_cue': '7 - 2'}, {'id': 'sub_8_4', 'label': '8 - 4', 'visual_cue': '8 - 4'}], 'right_items': [{'id': 'res_5', 'label': '5', 'visual_cue': '5️⃣'}, {'id': 'res_4', 'label': '4', 'visual_cue': '4️⃣'}], 'pairs': [{'left_id': 'sub_7_2', 'right_id': 'res_5'}, {'left_id': 'sub_8_4', 'right_id': 'res_4'}]},
            correct_answer={'pairs': [{'left_id': 'sub_7_2', 'right_id': 'res_5'}, {'left_id': 'sub_8_4', 'right_id': 'res_4'}]},
            explanation={'en': 'Great subtraction solving!', 'ar': 'حل ممتاز للطرح!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.drag.sort_results',
            objective_key='obj.math.solve_subtraction_equations_10',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=3,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort equations into 'Answer is 3' and 'Answer is 5'.", 'ar': "صنف المعادلات إلى 'الناتج ٣' و 'الناتج ٥'."},
            content_payload={'prompt': "Sort equations into 'Answer is 3' and 'Answer is 5'.", 'items': [{'id': 'eq_63', 'label': '6 - 3', 'visual_cue': '6 - 3'}, {'id': 'eq_74', 'label': '7 - 4', 'visual_cue': '7 - 4'}, {'id': 'eq_105', 'label': '10 - 5', 'visual_cue': '10 - 5'}, {'id': 'eq_83', 'label': '8 - 3', 'visual_cue': '8 - 3'}], 'zones': [{'id': 'z_res3', 'label': 'Answer = 3', 'capacity': 3}, {'id': 'z_res5', 'label': 'Answer = 5', 'capacity': 3}], 'correct_mapping': {'eq_63': 'z_res3', 'eq_74': 'z_res3', 'eq_105': 'z_res5', 'eq_83': 'z_res5'}},
            correct_answer={'correct_mapping': {'eq_63': 'z_res3', 'eq_74': 'z_res3', 'eq_105': 'z_res5', 'eq_83': 'z_res5'}},
            explanation={'en': 'Wonderful sorting by equation results!', 'ar': 'تصنيف رائع حسب نتائج المعادلات!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.mc.m1_5',
            objective_key='obj.math.sub_minus_1',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'What is 5 - 1?', 'ar': 'ما حاصل ٥ - ١؟'},
            content_payload={'question': 'What is 5 - 1?', 'options': [{'id': 'ans_4', 'text': '4', 'visual_cue': '4️⃣', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_3', 'text': '3', 'visual_cue': '3️⃣', 'is_correct': False, 'distractor_rationale': 'Subtracted 2'}, {'id': 'ans_5', 'text': '5', 'visual_cue': '5️⃣', 'is_correct': False, 'distractor_rationale': 'No change'}], 'correct_answer_id': 'ans_4', 'explanation': 'Correct! Subtracting 1 from 5 gives 4.'},
            correct_answer={'correct_answer_id': 'ans_4'},
            explanation={'en': 'Correct! Subtracting 1 from 5 gives 4.', 'ar': 'صحيح! طرح ١ من ٥ يعطي ٤.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.mc.m1_8',
            objective_key='obj.math.sub_minus_1',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'What is 8 - 1?', 'ar': 'ما حاصل ٨ - ١؟'},
            content_payload={'question': 'What is 8 - 1?', 'options': [{'id': 'ans_7', 'text': '7', 'visual_cue': '7️⃣', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_6', 'text': '6', 'visual_cue': '6️⃣', 'is_correct': False, 'distractor_rationale': 'Subtracted 2'}, {'id': 'ans_9', 'text': '9', 'visual_cue': '9️⃣', 'is_correct': False, 'distractor_rationale': 'Added 1'}], 'correct_answer_id': 'ans_7', 'explanation': 'Super! 8 - 1 = 7.'},
            correct_answer={'correct_answer_id': 'ans_7'},
            explanation={'en': 'Super! 8 - 1 = 7.', 'ar': 'ممتاز! ٨ - ١ = ٧.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.match.m1_pairs',
            objective_key='obj.math.sub_minus_1',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each number to the result of subtracting 1.', 'ar': 'طابق كل رقم بناتج طرح ١ منه.'},
            content_payload={'prompt': 'Match each number to the result of subtracting 1.', 'left_items': [{'id': 'num_4', 'label': '4 - 1', 'visual_cue': '4 - 1'}, {'id': 'num_7', 'label': '7 - 1', 'visual_cue': '7 - 1'}, {'id': 'num_10', 'label': '10 - 1', 'visual_cue': '10 - 1'}], 'right_items': [{'id': 'res_3', 'label': '3', 'visual_cue': '3️⃣'}, {'id': 'res_6', 'label': '6', 'visual_cue': '6️⃣'}, {'id': 'res_9', 'label': '9', 'visual_cue': '9️⃣'}], 'pairs': [{'left_id': 'num_4', 'right_id': 'res_3'}, {'left_id': 'num_7', 'right_id': 'res_6'}, {'left_id': 'num_10', 'right_id': 'res_9'}]},
            correct_answer={'pairs': [{'left_id': 'num_4', 'right_id': 'res_3'}, {'left_id': 'num_7', 'right_id': 'res_6'}, {'left_id': 'num_10', 'right_id': 'res_9'}]},
            explanation={'en': 'Great job! Subtracting 1 gives the immediate preceding number.', 'ar': 'عمل رائع! طرح ١ يعطي الرقم السابق مباشرة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.vis.numline_m1',
            objective_key='obj.math.sub_minus_1',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Identify the number that is 1 step back from 7 on the number line.', 'ar': 'حدد الرقم الذي يسبق ٧ بخطوة واحدة على خط الأعداد.'},
            content_payload={'prompt': 'Identify the number that is 1 step back from 7 on the number line.', 'scene_description': 'A number line marked 1 to 10.', 'elements': [{'id': 'nl_5', 'label': 'Number 5', 'category': 'number', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'nl_6', 'label': 'Number 6', 'category': 'number', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'nl_8', 'label': 'Number 8', 'category': 'number', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'nl_6', 'feedback_clue': 'Hop 1 step backwards from 7.'},
            correct_answer={'target_id': 'nl_6'},
            explanation={'en': 'Spot on! 1 step back from 7 lands on 6.', 'ar': 'صحيح! خطوة واحدة للخلف من ٧ تصل إلى ٦.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.order.countdown_m1',
            objective_key='obj.math.sub_minus_1',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=2,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Arrange the countdown steps by subtracting 1: 8, 7, 6.', 'ar': 'رتب خطوات العد التنازلي بطرح ١: ٨، ٧، ٦.'},
            content_payload={'prompt': 'Arrange the countdown steps by subtracting 1: 8, 7, 6.', 'items': [{'id': 'cd_7', 'label': '7 (8 - 1)', 'visual_cue': '7️⃣'}, {'id': 'cd_8', 'label': '8 (Start)', 'visual_cue': '8️⃣'}, {'id': 'cd_6', 'label': '6 (7 - 1)', 'visual_cue': '6️⃣'}], 'correct_sequence': ['cd_8', 'cd_7', 'cd_6'], 'direction': 'descending'},
            correct_answer={'correct_sequence': ['cd_8', 'cd_7', 'cd_6']},
            explanation={'en': 'Terrific countdown! 8, 7, 6.', 'ar': 'عد تنازلي رائع! ٨، ٧، ٦.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.mc.m2_6',
            objective_key='obj.math.sub_minus_2_or_more',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=3,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'What is 6 - 2?', 'ar': 'ما حاصل ٦ - ٢؟'},
            content_payload={'question': 'What is 6 - 2?', 'options': [{'id': 'ans_4', 'text': '4', 'visual_cue': '4️⃣', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_5', 'text': '5', 'visual_cue': '5️⃣', 'is_correct': False, 'distractor_rationale': 'Only subtracted 1'}, {'id': 'ans_3', 'text': '3', 'visual_cue': '3️⃣', 'is_correct': False, 'distractor_rationale': 'Subtracted 3'}], 'correct_answer_id': 'ans_4', 'explanation': 'Correct! 6 - 2 = 4.'},
            correct_answer={'correct_answer_id': 'ans_4'},
            explanation={'en': 'Correct! 6 - 2 = 4.', 'ar': 'صحيح! ٦ - ٢ = ٤.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.mc.m3_9',
            objective_key='obj.math.sub_minus_2_or_more',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=3,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'What is 9 - 3?', 'ar': 'ما حاصل ٩ - ٣؟'},
            content_payload={'question': 'What is 9 - 3?', 'options': [{'id': 'ans_6', 'text': '6', 'visual_cue': '6️⃣', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_5', 'text': '5', 'visual_cue': '5️⃣', 'is_correct': False, 'distractor_rationale': 'Subtracted 4'}, {'id': 'ans_7', 'text': '7', 'visual_cue': '7️⃣', 'is_correct': False, 'distractor_rationale': 'Only subtracted 2'}], 'correct_answer_id': 'ans_6', 'explanation': 'Super! 9 - 3 = 6.'},
            correct_answer={'correct_answer_id': 'ans_6'},
            explanation={'en': 'Super! 9 - 3 = 6.', 'ar': 'ممتاز! ٩ - ٣ = ٦.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.match.m2_pairs',
            objective_key='obj.math.sub_minus_2_or_more',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=3,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match each minus-2 expression to its result.', 'ar': 'طابق كل مسألة طرح ٢ بنتيجتها.'},
            content_payload={'prompt': 'Match each minus-2 expression to its result.', 'left_items': [{'id': 'sm_52', 'label': '5 - 2', 'visual_cue': '5 - 2'}, {'id': 'sm_72', 'label': '7 - 2', 'visual_cue': '7 - 2'}, {'id': 'sm_92', 'label': '9 - 2', 'visual_cue': '9 - 2'}], 'right_items': [{'id': 'r_3', 'label': '3', 'visual_cue': '3️⃣'}, {'id': 'r_5', 'label': '5', 'visual_cue': '5️⃣'}, {'id': 'r_7', 'label': '7', 'visual_cue': '7️⃣'}], 'pairs': [{'left_id': 'sm_52', 'right_id': 'r_3'}, {'left_id': 'sm_72', 'right_id': 'r_5'}, {'left_id': 'sm_92', 'right_id': 'r_7'}]},
            correct_answer={'pairs': [{'left_id': 'sm_52', 'right_id': 'r_3'}, {'left_id': 'sm_72', 'right_id': 'r_5'}, {'left_id': 'sm_92', 'right_id': 'r_7'}]},
            explanation={'en': 'Great job! 5-2=3, 7-2=5, 9-2=7.', 'ar': 'عمل رائع! ٥-٢=٣، ٧-٢=٥، ٩-٢=٧.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.vis.numline_m2',
            objective_key='obj.math.sub_minus_2_or_more',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=3,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the jumping frog landing on 6 after jumping backward -2 from 8.', 'ar': 'حدد الضفدع الذي يقفز للخلف خطوتين من ٨ ليصل إلى ٦.'},
            content_payload={'prompt': 'Spot the jumping frog landing on 6 after jumping backward -2 from 8.', 'scene_description': 'A number line with backward jump arrows.', 'elements': [{'id': 'frog_b7', 'label': 'Landed on 7 (-1 jump)', 'category': 'marker', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'frog_b6', 'label': 'Landed on 6 (-2 jump)', 'category': 'marker', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'frog_b5', 'label': 'Landed on 5 (-3 jump)', 'category': 'marker', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'frog_b6', 'feedback_clue': 'Look for 8 - 2 = 6.'},
            correct_answer={'target_id': 'frog_b6'},
            explanation={'en': 'Brilliant! Jumping backward 2 steps lands on 6.', 'ar': 'رائع! القفز خطوتين للخلف يصل إلى ٦.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.sub.drag.sort_m2_m3',
            objective_key='obj.math.sub_minus_2_or_more',
            subject_code='math',
            unit_code='unit.math.subtraction_within_10',
            difficulty_level=3,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort expressions into 'Minus 2' and 'Minus 3'.", 'ar': "صنف التعبيرات إلى 'طرح ٢' و 'طرح ٣'."},
            content_payload={'prompt': "Sort expressions into 'Minus 2' and 'Minus 3'.", 'items': [{'id': 'sub_42', 'label': '4 - 2', 'visual_cue': '4 - 2'}, {'id': 'sub_82', 'label': '8 - 2', 'visual_cue': '8 - 2'}, {'id': 'sub_63', 'label': '6 - 3', 'visual_cue': '6 - 3'}, {'id': 'sub_93', 'label': '9 - 3', 'visual_cue': '9 - 3'}], 'zones': [{'id': 'z_m2', 'label': 'Subtracting 2', 'capacity': 3}, {'id': 'z_m3', 'label': 'Subtracting 3', 'capacity': 3}], 'correct_mapping': {'sub_42': 'z_m2', 'sub_82': 'z_m2', 'sub_63': 'z_m3', 'sub_93': 'z_m3'}},
            correct_answer={'correct_mapping': {'sub_42': 'z_m2', 'sub_82': 'z_m2', 'sub_63': 'z_m3', 'sub_93': 'z_m3'}},
            explanation={'en': 'Terrific classification by subtracted amount!', 'ar': 'تصنيف رائع حسب المقدار المطروح!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.mc.circle_obj',
            objective_key='obj.math.identify_circle',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=1,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which everyday object has a circular shape?', 'ar': 'أي شيء من الحياة اليومية له شكل دائري؟'},
            content_payload={'question': 'Which everyday object has a circular shape?', 'options': [{'id': 'opt_clock', 'text': 'Wall Clock ⏰', 'visual_cue': '⏰', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_book', 'text': 'Book 📖', 'visual_cue': '📖', 'is_correct': False, 'distractor_rationale': 'Rectangular'}, {'id': 'opt_box', 'text': 'Shoebox 📦', 'visual_cue': '📦', 'is_correct': False, 'distractor_rationale': 'Rectangular/Cube'}], 'correct_answer_id': 'opt_clock', 'explanation': 'Correct! A wall clock is round like a circle.'},
            correct_answer={'correct_answer_id': 'opt_clock'},
            explanation={'en': 'Correct! A wall clock is round like a circle.', 'ar': 'صحيح! ساعة الحائط مستديرة كالدائرة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.vis.circle_plate',
            objective_key='obj.math.identify_circle',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=1,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the circular plate on the breakfast table.', 'ar': 'حدد الطبق الدائري على طاولة الإفطار.'},
            content_payload={'prompt': 'Spot the circular plate on the breakfast table.', 'scene_description': 'A breakfast table with a plate, a square napkin, and a rectangular juice carton.', 'elements': [{'id': 'obj_napkin', 'label': 'Square Napkin', 'category': 'tableware', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'obj_plate', 'label': 'Circular Plate', 'category': 'tableware', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'obj_carton', 'label': 'Juice Carton', 'category': 'tableware', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'obj_plate', 'feedback_clue': 'Look for the completely round object in the center.'},
            correct_answer={'target_id': 'obj_plate'},
            explanation={'en': 'Wonderful! The plate is a circle with zero corners.', 'ar': 'رائع! الطبق دائري بلا زوايا.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.match.circle_items',
            objective_key='obj.math.identify_circle',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=1,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match circular objects to the Circle shape.', 'ar': 'طابق الأشياء الدائرية بشكل الدائرة.'},
            content_payload={'prompt': 'Match circular objects to the Circle shape.', 'left_items': [{'id': 'it_wheel', 'label': 'Bicycle Wheel 🚲', 'visual_cue': 'wheel'}, {'id': 'it_coin', 'label': 'Coin 🪙', 'visual_cue': 'coin'}], 'right_items': [{'id': 'sh_circle', 'label': 'Circle Shape ⭕', 'visual_cue': '⭕'}, {'id': 'sh_other', 'label': 'Square Shape ⏹️', 'visual_cue': '⏹️'}], 'pairs': [{'left_id': 'it_wheel', 'right_id': 'sh_circle'}, {'left_id': 'it_coin', 'right_id': 'sh_circle'}]},
            correct_answer={'pairs': [{'left_id': 'it_wheel', 'right_id': 'sh_circle'}, {'left_id': 'it_coin', 'right_id': 'sh_circle'}]},
            explanation={'en': 'Great shape matching! Wheels and coins are circular.', 'ar': 'مطابقة أشكال ممتازة! العجلات والعملات دائرية.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.drag.sort_circles',
            objective_key='obj.math.identify_circle',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=1,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort items into 'Circles ⭕' and 'Other Shapes'.", 'ar': "صنف العناصر إلى 'دوائر ⭕' و 'أشكال أخرى'."},
            content_payload={'prompt': "Sort items into 'Circles ⭕' and 'Other Shapes'.", 'items': [{'id': 'sc_button', 'label': 'Round Button 🔘', 'visual_cue': '🔘'}, {'id': 'sc_pizza', 'label': 'Whole Pizza 🍕', 'visual_cue': 'round pizza'}, {'id': 'sc_door', 'label': 'Door 🚪', 'visual_cue': '🚪'}, {'id': 'sc_ruler', 'label': 'Ruler 📏', 'visual_cue': '📏'}], 'zones': [{'id': 'z_circ', 'label': 'Circles ⭕', 'capacity': 3}, {'id': 'z_notcirc', 'label': 'Other Shapes', 'capacity': 3}], 'correct_mapping': {'sc_button': 'z_circ', 'sc_pizza': 'z_circ', 'sc_door': 'z_notcirc', 'sc_ruler': 'z_notcirc'}},
            correct_answer={'correct_mapping': {'sc_button': 'z_circ', 'sc_pizza': 'z_circ', 'sc_door': 'z_notcirc', 'sc_ruler': 'z_notcirc'}},
            explanation={'en': 'Terrific circle identification!', 'ar': 'تمييز رائع للدائرة!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.mc.id_square',
            objective_key='obj.math.identify_square',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=1,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which shape has 4 equal straight sides and 4 corners?', 'ar': 'أي شكل له ٤ أضلاع مستقيمة متساوية و ٤ زوايا؟'},
            content_payload={'question': 'Which shape has 4 equal straight sides and 4 corners?', 'options': [{'id': 'opt_sq', 'text': 'Square ⏹️', 'visual_cue': '⏹️', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_ci', 'text': 'Circle ⭕', 'visual_cue': '⭕', 'is_correct': False, 'distractor_rationale': 'Round with no sides'}, {'id': 'opt_tr', 'text': 'Triangle 🔺', 'visual_cue': '🔺', 'is_correct': False, 'distractor_rationale': 'Has only 3 sides'}], 'correct_answer_id': 'opt_sq', 'explanation': 'Correct! A square has 4 equal sides and 4 corners.'},
            correct_answer={'correct_answer_id': 'opt_sq'},
            explanation={'en': 'Correct! A square has 4 equal sides and 4 corners.', 'ar': 'صحيح! المربع له ٤ أضلاع متساوية و ٤ زوايا.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.vis.square_frame',
            objective_key='obj.math.identify_square',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=1,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the square picture frame on the wall.', 'ar': 'حدد إطار الصورة المربع على الحائط.'},
            content_payload={'prompt': 'Spot the square picture frame on the wall.', 'scene_description': 'A living room wall with a clock, a square frame, and a triangular banner.', 'elements': [{'id': 'fr_clock', 'label': 'Round Clock', 'category': 'decor', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'fr_square', 'label': 'Square Frame', 'category': 'decor', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'fr_banner', 'label': 'Triangular Banner', 'category': 'decor', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'fr_square', 'feedback_clue': 'Look for the photo frame with 4 equal straight sides.'},
            correct_answer={'target_id': 'fr_square'},
            explanation={'en': 'Awesome observation! That photo frame is a square.', 'ar': 'ملاحظة رائعة! إطار الصورة مربع الشكل.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.match.square_items',
            objective_key='obj.math.identify_square',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=1,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match square objects to the Square label.', 'ar': 'طابق الأشياء المربعة ببطاقة المربع.'},
            content_payload={'prompt': 'Match square objects to the Square label.', 'left_items': [{'id': 'it_chess', 'label': 'Chessboard 🏁', 'visual_cue': 'chessboard'}, {'id': 'it_tile', 'label': 'Square Floor Tile 🔲', 'visual_cue': 'tile'}], 'right_items': [{'id': 'lbl_sq', 'label': 'Square ⏹️', 'visual_cue': '⏹️'}, {'id': 'lbl_tri', 'label': 'Triangle 🔺', 'visual_cue': '🔺'}], 'pairs': [{'left_id': 'it_chess', 'right_id': 'lbl_sq'}, {'left_id': 'it_tile', 'right_id': 'lbl_sq'}]},
            correct_answer={'pairs': [{'left_id': 'it_chess', 'right_id': 'lbl_sq'}, {'left_id': 'it_tile', 'right_id': 'lbl_sq'}]},
            explanation={'en': 'Great! Chessboards and square tiles are squares.', 'ar': 'رائع! رقعة الشطرنج والبلاط المربع أشكال مربعة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.drag.sort_squares',
            objective_key='obj.math.identify_square',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=1,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort items into 'Squares ⏹️' and 'Non-Squares'.", 'ar': "صنف العناصر إلى 'مربعات ⏹️' و 'غير مربعات'."},
            content_payload={'prompt': "Sort items into 'Squares ⏹️' and 'Non-Squares'.", 'items': [{'id': 'sq_napkin', 'label': 'Square Napkin', 'visual_cue': 'square napkin'}, {'id': 'sq_box', 'label': 'Square Gift Box', 'visual_cue': 'cube face'}, {'id': 'sq_wheel', 'label': 'Tire Wheel', 'visual_cue': 'round tire'}, {'id': 'sq_sign', 'label': 'Yield Sign', 'visual_cue': 'triangle sign'}], 'zones': [{'id': 'z_sq', 'label': 'Squares ⏹️', 'capacity': 3}, {'id': 'z_notsq', 'label': 'Non-Squares', 'capacity': 3}], 'correct_mapping': {'sq_napkin': 'z_sq', 'sq_box': 'z_sq', 'sq_wheel': 'z_notsq', 'sq_sign': 'z_notsq'}},
            correct_answer={'correct_mapping': {'sq_napkin': 'z_sq', 'sq_box': 'z_sq', 'sq_wheel': 'z_notsq', 'sq_sign': 'z_notsq'}},
            explanation={'en': 'Terrific square sorting!', 'ar': 'فرز رائع للمربعات!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.order.by_sides',
            objective_key='obj.math.identify_square',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=1,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Arrange shapes by number of sides from fewest to most.', 'ar': 'رتب الأشكال حسب عدد الأضلاع من الأقل إلى الأكثر.'},
            content_payload={'prompt': 'Arrange shapes by number of sides from fewest to most.', 'items': [{'id': 'sh_tr', 'label': 'Triangle (3 sides) 🔺', 'visual_cue': '🔺'}, {'id': 'sh_ci', 'label': 'Circle (0 sides) ⭕', 'visual_cue': '⭕'}, {'id': 'sh_sq', 'label': 'Square (4 sides) ⏹️', 'visual_cue': '⏹️'}], 'correct_sequence': ['sh_ci', 'sh_tr', 'sh_sq'], 'direction': 'ascending'},
            correct_answer={'correct_sequence': ['sh_ci', 'sh_tr', 'sh_sq']},
            explanation={'en': 'Brilliant! Circle (0), Triangle (3), Square (4).', 'ar': 'رائع! دائرة (٠)، مثلث (٣)، مربع (٤).'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.mc.id_triangle',
            objective_key='obj.math.identify_triangle',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=1,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which shape has exactly 3 straight sides and 3 corners?', 'ar': 'أي شكل له ٣ أضلاع مستقيمة و ٣ زوايا بالضبط؟'},
            content_payload={'question': 'Which shape has exactly 3 straight sides and 3 corners?', 'options': [{'id': 'opt_tr', 'text': 'Triangle 🔺', 'visual_cue': '🔺', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_sq', 'text': 'Square ⏹️', 'visual_cue': '⏹️', 'is_correct': False, 'distractor_rationale': 'Has 4 sides'}, {'id': 'opt_ci', 'text': 'Circle ⭕', 'visual_cue': '⭕', 'is_correct': False, 'distractor_rationale': 'Has 0 corners'}], 'correct_answer_id': 'opt_tr', 'explanation': 'Correct! A triangle has 3 sides and 3 corners.'},
            correct_answer={'correct_answer_id': 'opt_tr'},
            explanation={'en': 'Correct! A triangle has 3 sides and 3 corners.', 'ar': 'صحيح! المثلث له ٣ أضلاع و ٣ زوايا.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.vis.triangle_roof',
            objective_key='obj.math.identify_triangle',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=1,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the triangular roof on the birdhouse.', 'ar': 'حدد السقف المثلث لبيت الطيور.'},
            content_payload={'prompt': 'Spot the triangular roof on the birdhouse.', 'scene_description': 'A wooden birdhouse with a triangular roof, a square front, and a circular entrance hole.', 'elements': [{'id': 'bh_hole', 'label': 'Circular Entrance Hole', 'category': 'feature', 'is_target': False, 'bounding_hint': 'center'}, {'id': 'bh_roof', 'label': 'Triangular Roof', 'category': 'feature', 'is_target': True, 'bounding_hint': 'top'}, {'id': 'bh_wall', 'label': 'Square Front Wall', 'category': 'feature', 'is_target': False, 'bounding_hint': 'bottom'}], 'target_id': 'bh_roof', 'feedback_clue': 'Look at the top of the birdhouse with 3 straight sloping sides.'},
            correct_answer={'target_id': 'bh_roof'},
            explanation={'en': 'Super observation! That roof is shaped like a triangle.', 'ar': 'ملاحظة ممتازة! ذلك السقف مثلث الشكل.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.match.triangle_items',
            objective_key='obj.math.identify_triangle',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=1,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match triangle objects to the Triangle shape.', 'ar': 'طابق الأشياء المثلثة بشكل المثلث.'},
            content_payload={'prompt': 'Match triangle objects to the Triangle shape.', 'left_items': [{'id': 'tr_pizza', 'label': 'Slice of Pizza 🍕', 'visual_cue': 'pizza slice'}, {'id': 'tr_cone', 'label': 'Traffic Cone Silhouette ⚠️', 'visual_cue': 'cone'}], 'right_items': [{'id': 'sh_triangle', 'label': 'Triangle 🔺', 'visual_cue': '🔺'}, {'id': 'sh_circle', 'label': 'Circle ⭕', 'visual_cue': '⭕'}], 'pairs': [{'left_id': 'tr_pizza', 'right_id': 'sh_triangle'}, {'left_id': 'tr_cone', 'right_id': 'sh_triangle'}]},
            correct_answer={'pairs': [{'left_id': 'tr_pizza', 'right_id': 'sh_triangle'}, {'left_id': 'tr_cone', 'right_id': 'sh_triangle'}]},
            explanation={'en': 'Terrific matching! Pizza slices and traffic cones have 3 sides.', 'ar': 'مطابقة رائعة! شرائح البيتزا وأقماع المرور لها ٣ أضلاع.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.drag.sort_triangles',
            objective_key='obj.math.identify_triangle',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=1,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort shapes into 'Triangles 🔺' and 'Non-Triangles'.", 'ar': "صنف الأشكال إلى 'مثلثات 🔺' و 'غير مثلثات'."},
            content_payload={'prompt': "Sort shapes into 'Triangles 🔺' and 'Non-Triangles'.", 'items': [{'id': 'dt_pennant', 'label': 'Triangular Pennant 🚩', 'visual_cue': 'pennant'}, {'id': 'dt_pyramid', 'label': 'Pyramid Side 🔺', 'visual_cue': 'triangle side'}, {'id': 'dt_coin', 'label': 'Round Coin 🪙', 'visual_cue': 'round coin'}, {'id': 'dt_card', 'label': 'Square Card ⏹️', 'visual_cue': 'card'}], 'zones': [{'id': 'z_tri', 'label': 'Triangles 🔺', 'capacity': 3}, {'id': 'z_nottri', 'label': 'Non-Triangles', 'capacity': 3}], 'correct_mapping': {'dt_pennant': 'z_tri', 'dt_pyramid': 'z_tri', 'dt_coin': 'z_nottri', 'dt_card': 'z_nottri'}},
            correct_answer={'correct_mapping': {'dt_pennant': 'z_tri', 'dt_pyramid': 'z_tri', 'dt_coin': 'z_nottri', 'dt_card': 'z_nottri'}},
            explanation={'en': 'Great sorting of triangular objects!', 'ar': 'فرز رائع للأشكال المثلثة!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.mc.triangle_corners',
            objective_key='obj.math.identify_triangle',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=1,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'How many corners does a triangle have?', 'ar': 'كم زاوية للمثلث؟'},
            content_payload={'question': 'How many corners does a triangle have?', 'options': [{'id': 'opt_3', 'text': '3 Corners', 'visual_cue': '3️⃣', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_4', 'text': '4 Corners', 'visual_cue': '4️⃣', 'is_correct': False, 'distractor_rationale': 'A square has 4 corners'}, {'id': 'opt_2', 'text': '2 Corners', 'visual_cue': '2️⃣', 'is_correct': False, 'distractor_rationale': 'Too few'}], 'correct_answer_id': 'opt_3', 'explanation': 'Spot on! Every triangle has exactly 3 corners.'},
            correct_answer={'correct_answer_id': 'opt_3'},
            explanation={'en': 'Spot on! Every triangle has exactly 3 corners.', 'ar': 'صحيح! كل مثلث له ٣ زوايا بالضبط.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.mc.id_rectangle',
            objective_key='obj.math.identify_rectangle',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which shape has 2 long sides and 2 shorter sides?', 'ar': 'أي شكل له ضلعان طويلان وضلعان قصيران؟'},
            content_payload={'question': 'Which shape has 2 long sides and 2 shorter sides?', 'options': [{'id': 'opt_rec', 'text': 'Rectangle 📄', 'visual_cue': '📄', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_sq', 'text': 'Square ⏹️', 'visual_cue': '⏹️', 'is_correct': False, 'distractor_rationale': 'All 4 sides are equal in a square'}, {'id': 'opt_ci', 'text': 'Circle ⭕', 'visual_cue': '⭕', 'is_correct': False, 'distractor_rationale': 'No straight sides'}], 'correct_answer_id': 'opt_rec', 'explanation': 'Correct! A rectangle has opposite sides of equal length: 2 long and 2 short.'},
            correct_answer={'correct_answer_id': 'opt_rec'},
            explanation={'en': 'Correct! A rectangle has opposite sides of equal length: 2 long and 2 short.', 'ar': 'صحيح! المستطيل له ضلعان طويلان وضلعان قصيران.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.vis.rectangle_chalkboard',
            objective_key='obj.math.identify_rectangle',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the rectangular chalkboard on the classroom wall.', 'ar': 'حدد السبورة المستطيلة على حائط الفصل الدراسي.'},
            content_payload={'prompt': 'Spot the rectangular chalkboard on the classroom wall.', 'scene_description': 'A classroom with a rectangular chalkboard, a round clock, and a square window.', 'elements': [{'id': 'el_window', 'label': 'Square Window', 'category': 'wall', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'el_board', 'label': 'Rectangular Chalkboard', 'category': 'wall', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'el_clock', 'label': 'Round Clock', 'category': 'wall', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'el_board', 'feedback_clue': 'Look for the large wide board in the center with 2 long horizontal sides.'},
            correct_answer={'target_id': 'el_board'},
            explanation={'en': 'Terrific! The chalkboard is a rectangle.', 'ar': 'رائع! السبورة مستطيلة الشكل.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.match.rectangle_items',
            objective_key='obj.math.identify_rectangle',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match rectangular items to the Rectangle label.', 'ar': 'طابق العناصر المستطيلة ببطاقة المستطيل.'},
            content_payload={'prompt': 'Match rectangular items to the Rectangle label.', 'left_items': [{'id': 'ri_door', 'label': 'Door 🚪', 'visual_cue': 'door'}, {'id': 'ri_ruler', 'label': 'Ruler 📏', 'visual_cue': 'ruler'}], 'right_items': [{'id': 'lbl_rec', 'label': 'Rectangle 📄', 'visual_cue': '📄'}, {'id': 'lbl_circ', 'label': 'Circle ⭕', 'visual_cue': '⭕'}], 'pairs': [{'left_id': 'ri_door', 'right_id': 'lbl_rec'}, {'left_id': 'ri_ruler', 'right_id': 'lbl_rec'}]},
            correct_answer={'pairs': [{'left_id': 'ri_door', 'right_id': 'lbl_rec'}, {'left_id': 'ri_ruler', 'right_id': 'lbl_rec'}]},
            explanation={'en': 'Great matching! Doors and rulers have rectangular shapes.', 'ar': 'مطابقة ممتازة! الأبواب والمساطر أشكالها مستطيلة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.drag.sort_rectangles',
            objective_key='obj.math.identify_rectangle',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort shapes into 'Rectangles 📄' and 'Squares ⏹️'.", 'ar': "صنف الأشكال إلى 'مستطيلات 📄' و 'مربعات ⏹️'."},
            content_payload={'prompt': "Sort shapes into 'Rectangles 📄' and 'Squares ⏹️'.", 'items': [{'id': 'sr_door', 'label': 'Tall Door', 'visual_cue': 'door (long & short sides)'}, {'id': 'sr_phone', 'label': 'Smartphone Screen', 'visual_cue': 'phone (long & short sides)'}, {'id': 'sr_tile', 'label': 'Floor Tile (Equal sides)', 'visual_cue': 'equal square tile'}, {'id': 'sr_box', 'label': 'Square Box Face', 'visual_cue': 'equal square face'}], 'zones': [{'id': 'z_rec', 'label': 'Rectangles 📄', 'capacity': 3}, {'id': 'z_sqr', 'label': 'Squares ⏹️', 'capacity': 3}], 'correct_mapping': {'sr_door': 'z_rec', 'sr_phone': 'z_rec', 'sr_tile': 'z_sqr', 'sr_box': 'z_sqr'}},
            correct_answer={'correct_mapping': {'sr_door': 'z_rec', 'sr_phone': 'z_rec', 'sr_tile': 'z_sqr', 'sr_box': 'z_sqr'}},
            explanation={'en': 'Brilliant distinction between rectangles and squares!', 'ar': 'تمييز رائع بين المستطيلات والمربعات!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.mc.door_shape',
            objective_key='obj.math.identify_rectangle',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which everyday item is shaped like a rectangle?', 'ar': 'أي شيء من الحياة اليومية له شكل مستطيل؟'},
            content_payload={'question': 'Which everyday item is shaped like a rectangle?', 'options': [{'id': 'opt_door', 'text': 'Classroom Door 🚪', 'visual_cue': '🚪', 'is_correct': True, 'distractor_rationale': None}, {'id': 'opt_ball', 'text': 'Soccer Ball ⚽', 'visual_cue': '⚽', 'is_correct': False, 'distractor_rationale': 'A soccer ball is round'}, {'id': 'opt_donut', 'text': 'Donut 🍩', 'visual_cue': '🍩', 'is_correct': False, 'distractor_rationale': 'A donut is circular'}], 'correct_answer_id': 'opt_door', 'explanation': 'Spot on! A classroom door is tall and rectangular.'},
            correct_answer={'correct_answer_id': 'opt_door'},
            explanation={'en': 'Spot on! A classroom door is tall and rectangular.', 'ar': 'صحيح! باب الفصل طويل ومستطيل الشكل.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.match.identical_colored',
            objective_key='obj.math.match_identical_shapes',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=1,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match identical colored shapes.', 'ar': 'طابق الأشكال الملونة المتطابقة.'},
            content_payload={'prompt': 'Match identical colored shapes.', 'left_items': [{'id': 'sh_bc', 'label': 'Blue Circle 🔵', 'visual_cue': '🔵'}, {'id': 'sh_rs', 'label': 'Red Square 🟥', 'visual_cue': '🟥'}, {'id': 'sh_gt', 'label': 'Green Triangle 🔺', 'visual_cue': '🔺'}], 'right_items': [{'id': 'm_bc', 'label': 'Blue Circle 🔵', 'visual_cue': '🔵'}, {'id': 'm_rs', 'label': 'Red Square 🟥', 'visual_cue': '🟥'}, {'id': 'm_gt', 'label': 'Green Triangle 🔺', 'visual_cue': '🔺'}], 'pairs': [{'left_id': 'sh_bc', 'right_id': 'm_bc'}, {'left_id': 'sh_rs', 'right_id': 'm_rs'}, {'left_id': 'sh_gt', 'right_id': 'm_gt'}]},
            correct_answer={'pairs': [{'left_id': 'sh_bc', 'right_id': 'm_bc'}, {'left_id': 'sh_rs', 'right_id': 'm_rs'}, {'left_id': 'sh_gt', 'right_id': 'm_gt'}]},
            explanation={'en': 'Perfect identical shape matching!', 'ar': 'مطابقة مثالية للأشكال المتطابقة!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.mc.exact_match_star',
            objective_key='obj.math.match_identical_shapes',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=1,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which shape is an EXACT match to the yellow star ⭐?', 'ar': 'أي شكل يطابق النجمة الصفراء ⭐ تماماً؟'},
            content_payload={'question': 'Which shape is an EXACT match to the yellow star ⭐?', 'options': [{'id': 'ans_star', 'text': 'Yellow Star ⭐', 'visual_cue': '⭐', 'is_correct': True, 'distractor_rationale': None}, {'id': 'ans_heart', 'text': 'Red Heart ❤️', 'visual_cue': '❤️', 'is_correct': False, 'distractor_rationale': 'Different shape and color'}, {'id': 'ans_diamond', 'text': 'Blue Diamond 🔷', 'visual_cue': '🔷', 'is_correct': False, 'distractor_rationale': 'Different shape and color'}], 'correct_answer_id': 'ans_star', 'explanation': 'Super! That is the exact matching yellow star.'},
            correct_answer={'correct_answer_id': 'ans_star'},
            explanation={'en': 'Super! That is the exact matching yellow star.', 'ar': 'ممتاز! هذه هي النجمة الصفراء المطابقة تماماً.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.vis.find_twin_heart',
            objective_key='obj.math.match_identical_shapes',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=1,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the shape identical to the target red heart ❤️.', 'ar': 'حدد الشكل المتطابق مع القلب الأحمر المستهدف ❤️.'},
            content_payload={'prompt': 'Spot the shape identical to the target red heart ❤️.', 'scene_description': 'A craft table with colorful stickers.', 'elements': [{'id': 'stk_circle', 'label': 'Red Circle 🔴', 'category': 'sticker', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'stk_heart', 'label': 'Red Heart ❤️', 'category': 'sticker', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'stk_star', 'label': 'Yellow Star ⭐', 'category': 'sticker', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'stk_heart', 'feedback_clue': 'Find the heart sticker matching the sample.'},
            correct_answer={'target_id': 'stk_heart'},
            explanation={'en': 'Terrific spotting! The hearts match identically.', 'ar': 'رصد رائع! القلوب متطابقة تماماً.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.drag.identical_slots',
            objective_key='obj.math.match_identical_shapes',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=1,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': 'Drag each shape into its identical outline slot.', 'ar': 'اسحب كل شكل إلى قالبه المتطابق معه.'},
            content_payload={'prompt': 'Drag each shape into its identical outline slot.', 'items': [{'id': 'p_cir', 'label': 'Green Circle 🟢', 'visual_cue': '🟢'}, {'id': 'p_sqr', 'label': 'Purple Square 🟪', 'visual_cue': '🟪'}], 'zones': [{'id': 'slt_cir', 'label': 'Circle Outline Slot (🟢)', 'capacity': 1}, {'id': 'slt_sqr', 'label': 'Square Outline Slot (🟪)', 'capacity': 1}], 'correct_mapping': {'p_cir': 'slt_cir', 'p_sqr': 'slt_sqr'}},
            correct_answer={'correct_mapping': {'p_cir': 'slt_cir', 'p_sqr': 'slt_sqr'}},
            explanation={'en': 'Awesome! Each shape fit into its exact matching slot.', 'ar': 'رائع! استقر كل شكل في قالبه المطابق تماماً.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.drag.sort_circ_tri',
            objective_key='obj.math.sort_objects_by_shape',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort items into 'Circles' and 'Triangles'.", 'ar': "صنف العناصر إلى 'دوائر' و 'مثلثات'."},
            content_payload={'prompt': "Sort items into 'Circles' and 'Triangles'.", 'items': [{'id': 'c_clock', 'label': 'Round Clock ⏰', 'visual_cue': '⏰'}, {'id': 'c_coin', 'label': 'Gold Coin 🪙', 'visual_cue': '🪙'}, {'id': 't_slice', 'label': 'Pizza Slice 🍕', 'visual_cue': '🍕'}, {'id': 't_flag', 'label': 'Triangle Pennant 🚩', 'visual_cue': '🚩'}], 'zones': [{'id': 'z_circles', 'label': 'Circles', 'capacity': 3}, {'id': 'z_triangles', 'label': 'Triangles', 'capacity': 3}], 'correct_mapping': {'c_clock': 'z_circles', 'c_coin': 'z_circles', 't_slice': 'z_triangles', 't_flag': 'z_triangles'}},
            correct_answer={'correct_mapping': {'c_clock': 'z_circles', 'c_coin': 'z_circles', 't_slice': 'z_triangles', 't_flag': 'z_triangles'}},
            explanation={'en': 'Excellent shape sorting!', 'ar': 'فرز أشكال ممتاز!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.match.objects_categories',
            objective_key='obj.math.sort_objects_by_shape',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match everyday objects to their shape category.', 'ar': 'طابق الأشياء اليومية بفئتها الشكلية.'},
            content_payload={'prompt': 'Match everyday objects to their shape category.', 'left_items': [{'id': 'o_wheel', 'label': 'Wheel 🛞', 'visual_cue': 'wheel'}, {'id': 'o_window', 'label': 'Square Window 🪟', 'visual_cue': 'window'}], 'right_items': [{'id': 'cat_circ', 'label': 'Category: Circle', 'visual_cue': '⭕'}, {'id': 'cat_sqr', 'label': 'Category: Square', 'visual_cue': '⏹️'}], 'pairs': [{'left_id': 'o_wheel', 'right_id': 'cat_circ'}, {'left_id': 'o_window', 'right_id': 'cat_sqr'}]},
            correct_answer={'pairs': [{'left_id': 'o_wheel', 'right_id': 'cat_circ'}, {'left_id': 'o_window', 'right_id': 'cat_sqr'}]},
            explanation={'en': 'Great category matching!', 'ar': 'مطابقة فئات رائعة!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.mc.only_squares',
            objective_key='obj.math.sort_objects_by_shape',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which group contains ONLY squares?', 'ar': 'أي مجموعة تحتوي على مربعات فقط؟'},
            content_payload={'question': 'Which group contains ONLY squares?', 'options': [{'id': 'grp_sq_only', 'text': 'Square tile, square napkin, chessboard', 'visual_cue': '⏹️ ⏹️ ⏹️', 'is_correct': True, 'distractor_rationale': None}, {'id': 'grp_mix_circ', 'text': 'Square tile, round clock, coin', 'visual_cue': '⏹️ ⭕ ⭕', 'is_correct': False, 'distractor_rationale': 'Contains circles'}, {'id': 'grp_mix_tri', 'text': 'Square tile, pizza slice, banner', 'visual_cue': '⏹️ 🔺 🔺', 'is_correct': False, 'distractor_rationale': 'Contains triangles'}], 'correct_answer_id': 'grp_sq_only', 'explanation': 'Correct! That group has exclusively square objects.'},
            correct_answer={'correct_answer_id': 'grp_sq_only'},
            explanation={'en': 'Correct! That group has exclusively square objects.', 'ar': 'صحيح! تلك المجموعة تحتوي على أشياء مربعة فقط.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.vis.row_all_circles',
            objective_key='obj.math.sort_objects_by_shape',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Spot the shelf where ALL items are circular.', 'ar': 'حدد الرف الذي جميع عناصره دائرية.'},
            content_payload={'prompt': 'Spot the shelf where ALL items are circular.', 'scene_description': 'A toy shelf with three rows of items.', 'elements': [{'id': 'row_top', 'label': 'Top Shelf (Blocks and Balls)', 'category': 'shelf', 'is_target': False, 'bounding_hint': 'top'}, {'id': 'row_mid', 'label': 'Middle Shelf (All Balls ⚽🏀⚾)', 'category': 'shelf', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'row_bot', 'label': 'Bottom Shelf (Boxes and Books)', 'category': 'shelf', 'is_target': False, 'bounding_hint': 'bottom'}], 'target_id': 'row_mid', 'feedback_clue': 'Look for the shelf that contains only round spherical balls.'},
            correct_answer={'target_id': 'row_mid'},
            explanation={'en': 'Terrific observation! The middle shelf has only circular items.', 'ar': 'ملاحظة رائعة! الرف الأوسط يحتوي على عناصر دائرية فقط.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.mc.bigger_bear',
            objective_key='obj.math.identify_visual_attributes',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.MULTIPLE_CHOICE],
            prompt={'en': 'Which teddy bear is BIGGER?', 'ar': 'أي دب لعبة هو الأكبر؟'},
            content_payload={'question': 'Which teddy bear is BIGGER?', 'options': [{'id': 'bear_big', 'text': 'Big Giant Bear 🧸 (Large)', 'visual_cue': '🧸 (Large)', 'is_correct': True, 'distractor_rationale': None}, {'id': 'bear_small', 'text': 'Little Baby Bear 🧸 (Small)', 'visual_cue': '🧸 (Small)', 'is_correct': False, 'distractor_rationale': 'This bear is smaller'}], 'correct_answer_id': 'bear_big', 'explanation': 'Correct! The giant teddy bear is noticeably bigger.'},
            correct_answer={'correct_answer_id': 'bear_big'},
            explanation={'en': 'Correct! The giant teddy bear is noticeably bigger.', 'ar': 'صحيح! الدب الضخم أكبر حجماً بشكل واضح.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.vis.tallest_tree',
            objective_key='obj.math.identify_visual_attributes',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.VISUAL_IDENTIFICATION],
            prompt={'en': 'Find the TALLEST tree in the forest.', 'ar': 'حدد أطول شجرة في الغابة.'},
            content_payload={'prompt': 'Find the TALLEST tree in the forest.', 'scene_description': 'A peaceful forest illustration with trees of varying heights.', 'elements': [{'id': 'tr_short', 'label': 'Short Sapling Tree', 'category': 'tree', 'is_target': False, 'bounding_hint': 'left'}, {'id': 'tr_tall', 'label': 'Tallest Pine Tree 🌲', 'category': 'tree', 'is_target': True, 'bounding_hint': 'center'}, {'id': 'tr_med', 'label': 'Medium Oak Tree', 'category': 'tree', 'is_target': False, 'bounding_hint': 'right'}], 'target_id': 'tr_tall', 'feedback_clue': 'Look in the center for the pine tree reaching highest into the sky.'},
            correct_answer={'target_id': 'tr_tall'},
            explanation={'en': 'Wonderful! That pine tree is the tallest.', 'ar': 'رائع! شجرة الصنوبر تلك هي الأطول.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.match.opposite_attributes',
            objective_key='obj.math.identify_visual_attributes',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.MATCHING],
            prompt={'en': 'Match opposite size attributes.', 'ar': 'طابق صفات الأحجام المتعاكسة.'},
            content_payload={'prompt': 'Match opposite size attributes.', 'left_items': [{'id': 'att_big', 'label': 'Big Elephant 🐘', 'visual_cue': 'big'}, {'id': 'att_long', 'label': 'Long Pencil ✏️📏', 'visual_cue': 'long'}], 'right_items': [{'id': 'opp_small', 'label': 'Small Mouse 🐁', 'visual_cue': 'small'}, {'id': 'opp_short', 'label': 'Short Crayon 🖍️', 'visual_cue': 'short'}], 'pairs': [{'left_id': 'att_big', 'right_id': 'opp_small'}, {'left_id': 'att_long', 'right_id': 'opp_short'}]},
            correct_answer={'pairs': [{'left_id': 'att_big', 'right_id': 'opp_small'}, {'left_id': 'att_long', 'right_id': 'opp_short'}]},
            explanation={'en': 'Great work matching opposite visual attributes!', 'ar': 'عمل رائع في مطابقة الصفات البصرية المتعاكسة!'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.order.by_size',
            objective_key='obj.math.identify_visual_attributes',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.ORDERING],
            prompt={'en': 'Order balls by size from smallest to largest.', 'ar': 'رتب الكرات حسب الحجم من الأصغر إلى الأكبر.'},
            content_payload={'prompt': 'Order balls by size from smallest to largest.', 'items': [{'id': 'b_tennis', 'label': 'Tennis Ball 🎾', 'visual_cue': 'tennis ball'}, {'id': 'b_marble', 'label': 'Tiny Marble ⚪', 'visual_cue': 'marble'}, {'id': 'b_basket', 'label': 'Large Basketball 🏀', 'visual_cue': 'basketball'}], 'correct_sequence': ['b_marble', 'b_tennis', 'b_basket'], 'direction': 'ascending'},
            correct_answer={'correct_sequence': ['b_marble', 'b_tennis', 'b_basket']},
            explanation={'en': 'Super! Tiny marble, tennis ball, then large basketball.', 'ar': 'ممتاز! كرة زجاجية صغيرة، كرة تنس، ثم كرة سلة كبيرة.'},
            hints=[],
            metadata_info={},
        )
    )
    items.append(
        ContentItemDef(
            content_key='math.shape.drag.sort_size',
            objective_key='obj.math.identify_visual_attributes',
            subject_code='math',
            unit_code='unit.math.shapes_classification',
            difficulty_level=2,
            supported_modalities=[ActivityType.DRAG_DROP],
            prompt={'en': "Sort blocks into 'Small Blocks' and 'Large Blocks'.", 'ar': "صنف المكعبات إلى 'مكعبات صغيرة' و 'مكعبات كبيرة'."},
            content_payload={'prompt': "Sort blocks into 'Small Blocks' and 'Large Blocks'.", 'items': [{'id': 'blk_s1', 'label': 'Small Red Cube 🟥', 'visual_cue': 'small'}, {'id': 'blk_s2', 'label': 'Small Blue Cube 🟦', 'visual_cue': 'small'}, {'id': 'blk_l1', 'label': 'Large Red Block 🧱', 'visual_cue': 'large'}, {'id': 'blk_l2', 'label': 'Large Blue Block 🧱', 'visual_cue': 'large'}], 'zones': [{'id': 'z_small', 'label': 'Small Blocks', 'capacity': 3}, {'id': 'z_large', 'label': 'Large Blocks', 'capacity': 3}], 'correct_mapping': {'blk_s1': 'z_small', 'blk_s2': 'z_small', 'blk_l1': 'z_large', 'blk_l2': 'z_large'}},
            correct_answer={'correct_mapping': {'blk_s1': 'z_small', 'blk_s2': 'z_small', 'blk_l1': 'z_large', 'blk_l2': 'z_large'}},
            explanation={'en': 'Terrific sorting by size attribute!', 'ar': 'فرز رائع حسب صفة الحجم!'},
            hints=[],
            metadata_info={},
        )
    )
    return items
