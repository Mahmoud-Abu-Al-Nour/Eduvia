# Curriculum Progression

Learning objectives do not exist in isolation; they form a directed acyclic graph (DAG) of prerequisite mastery.

---

## Prerequisite Modeling

The association table `objective_prerequisites` creates a self-referential graph on `learning_objectives`:
- `objective_id` (The advanced objective)
- `prerequisite_id` (The prerequisite objective that must be mastered first)

### Example:
- Objective A: "Recognize numbers 1–5" (Difficulty 1)
- Objective B: "Recognize numbers 6–10" (Difficulty 2)
  - `prerequisites = [Objective A]`

If a learner consistently fails activities on Objective B, the adaptation engine detects that prerequisite Objective A may require diagnostic review or reinforcement.
