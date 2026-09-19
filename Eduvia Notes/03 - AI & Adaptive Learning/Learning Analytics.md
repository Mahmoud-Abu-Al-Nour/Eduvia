# Learning Analytics

Learning Analytics processes raw interaction events into actionable pedagogical metrics.

---

## Telemetry Captured Per Activity
- **Timestamp & Duration**: Total time engaged and latency to first interaction.
- **Attempt Count**: Number of tries before correct completion.
- **Assistance Level**: 
  - Level 0: Independent mastery (no hints).
  - Level 1: Subtle prompt / reminder.
  - Level 2: Substantial hint / eliminated distractors.
  - Level 3: Full worked demonstration.
- **Error Types**: Categorized slip, misconception, or attention lapse.

---

## Metric Aggregation
These telemetry points feed the update algorithms:
- **Mastery Probability**: Bayesian or exponential moving average of objective completion.
- **Strategy Gain**: Delta in accuracy achieved when Strategy $S$ was applied versus baseline.
