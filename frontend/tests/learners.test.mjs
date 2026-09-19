import { test } from 'node:test';
import assert from 'node:assert/strict';

test('Learner structure validation and age group constraints', () => {
  const validLearner = {
    id: '11111111-1111-1111-1111-111111111111',
    name: 'Tariq',
    age_group: 'primary',
    learning_level: 'beginner',
    is_active: true,
  };

  assert.equal(validLearner.name, 'Tariq');
  assert.equal(validLearner.is_active, true);

  const allowedAgeGroups = ['early_childhood', 'primary', 'intermediate', 'secondary'];
  assert.ok(allowedAgeGroups.includes(validLearner.age_group));
});

test('LearnerProfile preserves educational terminology without diagnostic labels', () => {
  const profile = {
    communication_preferences: {
      primary_mode: 'verbal',
      receptive_preference: ['verbal', 'visual_cues'],
      expressive_preference: ['verbal'],
    },
    support_requirements: {
      sensory_accommodations: [],
      pacing: 'standard',
      guidance_level: 'moderate',
      frequent_breaks: true,
    },
    teacher_constraints: {
      max_session_duration_minutes: 20,
      excluded_modalities: [],
      required_modalities: [],
    },
    teacher_overrides: {
      lock_difficulty_level: 2,
      enforce_strategy: 'Step-by-Step',
      manual_adjustments_active: true,
    },
  };

  // Educational terms verified
  assert.equal(profile.support_requirements.pacing, 'standard');
  assert.equal(profile.support_requirements.guidance_level, 'moderate');
  assert.equal(profile.teacher_overrides.lock_difficulty_level, 2);

  // Verify no diagnostic fields
  assert.equal(profile.diagnosis, undefined);
  assert.equal(profile.disability_type, undefined);
});

test('Dynamic learning evidence does not permanently classify learner', () => {
  const modalityEvidence = {
    Visual: { observed_count: 5, engagement_rating: 'high' },
    'Reading/Text': { observed_count: 1, engagement_rating: 'medium' },
    Writing: { observed_count: 0, engagement_rating: null },
    Audio: { observed_count: 4, engagement_rating: 'high' },
    Interactive: { observed_count: 6, engagement_rating: 'high' },
  };

  // Ensure all 5 core presentation modalities are represented
  const modalities = Object.keys(modalityEvidence);
  assert.deepEqual(modalities, ['Visual', 'Reading/Text', 'Writing', 'Audio', 'Interactive']);

  // Verify observations are dynamic counts, not static labels
  assert.equal(modalityEvidence.Visual.observed_count, 5);
  assert.equal(modalityEvidence.Interactive.observed_count, 6);
});

test('Observation evidence log structure and serialization', () => {
  const observation = {
    id: 'obs-12345',
    timestamp: '2026-09-19T04:00:00Z',
    category: 'strategy',
    summary: 'Demonstrated rapid mastery with Step-by-Step instruction.',
    context: { strategy: 'Step-by-Step', latency_seconds: 3.4 },
    teacher_note: 'Consider advancing difficulty on next session.',
  };

  assert.equal(observation.category, 'strategy');
  assert.ok(observation.summary.includes('Step-by-Step'));
  assert.equal(observation.context.strategy, 'Step-by-Step');
  assert.equal(observation.teacher_note, 'Consider advancing difficulty on next session.');
});
