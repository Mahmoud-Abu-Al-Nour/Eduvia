# Activity Evaluation

Activity Evaluation measures learner responses against explicit objective criteria.

---

## Objective Assessment Rubric

Each `LearningObjective` specifies an `assessment_criteria` payload:
```json
{
  "minimum_accuracy": 0.80,
  "maximum_assistance_level": 1,
  "required_completion": true
}
```

A learner is evaluated as having attained **Mastery** on that objective only when:
$$	ext{Accuracy} \ge 	ext{minimum\_accuracy} \quad \land \quad 	ext{Assistance} \le 	ext{maximum\_assistance\_level}$$

If a student completes an activity with 100% accuracy but required Level 3 (full demonstration), mastery is **not** confirmed; scaffolding is incrementally faded until independence is demonstrated.
