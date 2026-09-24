# Eduvia — Expanded Foundational Curriculum Catalog

## 1. Overview
The Eduvia MVP curriculum is organized into a clean, 4-tier pedagogical hierarchy:
`Curriculum` -> `Subject` -> `Unit` -> `Lesson` -> `LearningObjective`

This structure provides standardized learning progression for inclusive learners with disabilities and special educational needs without claiming false governmental accreditation.

---

## 2. Subjects and Units Summary

### Subject 1: Foundational Mathematics (`subj.foundational_math`)
Focuses on numerical reasoning, quantity-numeral correspondence, early arithmetic, and spatial classification.
- **Unit 1**: Number Sense & Counting (Objectives: Recognize 0-5, Recognize 6-10, Count 0-5, Count 6-10, Match Numeral to Quantity, Compare Quantities).
- **Unit 2**: Number Sequence (Objectives: Number Before, Number After, Order Smallest to Largest, Order Largest to Smallest, Complete Missing Sequence, Number Patterns).
- **Unit 3**: Addition Within 10 (Objectives: Combine Groups, Represent Addition Visually, Solve Addition Equations, Add 1, Add 2 or More).
- **Unit 4**: Subtraction Within 10 (Objectives: Take Away from Group, Represent Subtraction Visually, How Many Remain, Solve Subtraction Equations, Subtract 1, Subtract 2 or More).
- **Unit 5**: Basic Shapes & Classification (Objectives: Identify Circle, Square, Triangle, Rectangle, Match Identical Shapes, Sort by Shape, Visual Attributes).

### Subject 2: Early Literacy (`subj.early_literacy`)
Focuses on phonemic awareness, orthographic recognition, vocabulary mapping, and narrative sequencing.
- **Unit 1**: Letter Recognition (Objectives: Uppercase Letters, Lowercase Letters, Match Upper to Lower, Target Letter Discrimination, Repeated Letters, Group Identical Letters).
- **Unit 2**: Letter Sounds (Objectives: Initial Sound Identification, Letter-Sound Matching, Target Initial Sound Word, Distinguish Initial Sounds).
- **Unit 3**: Word Recognition (Objectives: High-Frequency Words, Match Identical Words, Word to Picture Matching, Target Word Discrimination, Repeated Word Recognition).
- **Unit 4**: Simple Sequencing & Comprehension (Objectives: Order 2 Events, Order 3 Events, What Happens First, What Happens Next, Match Sentence to Picture).

### Subject 3: Everyday Learning Skills (`subj.everyday_learning`)
Focuses on non-clinical, practical independence, routine sequencing, perceptual categorization, and safe everyday behavior.
- **Unit 1**: Daily Routines (Objectives: Identify Daily Activities, Order Morning Routines, Next Step in Routine, Routine Stage Matching).
- **Unit 2**: Object Recognition (Objectives: Classroom Objects, Household Objects, Object to Name Matching, Match Identical Objects, Identify by Description).
- **Unit 3**: Sorting & Classification (Objectives: Sort by Type, Sort by Size, Sort by Shape, Belongs Together Matching, Odd One Out).
- **Unit 4**: Everyday Decisions & Basic Safety (Objectives: Appropriate Daily Action, Safe vs Unsafe Scenarios, Road Crossing Preparation, Household Situations, Sequence Safe Routine).

---

## 3. Prerequisite Graph Design
Prerequisites form a directed acyclic graph (DAG) enforced deterministically:
1. `Recognize numbers 0-5` -> `Count objects 0-5`
2. `Recognize numbers 6-10` -> `Count objects 6-10`
3. `Count objects 0-5` -> `Match numeral to quantity`
4. `Match numeral to quantity` -> `Order smallest to largest`
5. `Order smallest to largest` -> `Complete missing sequence`
6. `Count objects 0-10` -> `Combine two groups` (Addition)
7. `Combine two groups` -> `Solve addition equations`
8. `Addition within 10` -> `Subtraction within 10`
9. `Uppercase letters` -> `Match uppercase to lowercase`
10. `Letter recognition` -> `Letter sounds`
11. `Letter sounds` -> `Word recognition`
12. `Word recognition` -> `Story sequencing & comprehension`
13. `Identify daily activities` -> `Order morning routines`
14. `Object recognition` -> `Sort by type` -> `Odd one out`
