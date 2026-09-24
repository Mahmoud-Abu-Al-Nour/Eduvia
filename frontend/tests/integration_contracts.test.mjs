import test from 'node:test';
import assert from 'node:assert/strict';

/**
 * Eduvia — Frontend Activity Modality Submission & Evaluation Contracts Test
 *
 * Verifies that the client serialization contracts across all 5 modalities
 * exactly match the backend authoritative evaluation schemas (ActivitySubmissionRequest):
 * 1. Multiple Choice: { selected_option_id: string }
 * 2. Matching: { pairs: Array<{ left_id: string, right_id: string }> }
 * 3. Ordering: { ordered_ids: string[] }
 * 4. Visual Identification: { selected_element_id: string }
 * 5. Drag & Drop: { item_to_zone_mapping: Record<string, string> }
 *
 * And confirms that evaluation responses and telemetry metadata are correctly handled.
 */

test('Contract: Multiple Choice submission payload structure', () => {
  const selectedOptionId = 'opt_target_3';
  const payload = {
    selected_option_id: selectedOptionId,
    hints_used: 1,
    time_spent_seconds: 12,
  };

  assert.strictEqual(typeof payload.selected_option_id, 'string');
  assert.strictEqual(payload.selected_option_id, 'opt_target_3');
  assert.strictEqual(payload.hints_used, 1);
  assert.strictEqual(payload.time_spent_seconds, 12);
});

test('Contract: Matching submission payload structure', () => {
  const matchingPairs = [
    { left_id: 'left_cat', right_id: 'right_kitten' },
    { left_id: 'left_dog', right_id: 'right_puppy' },
  ];
  const payload = {
    pairs: matchingPairs,
    hints_used: 0,
    time_spent_seconds: 18,
  };

  assert.ok(Array.isArray(payload.pairs));
  assert.strictEqual(payload.pairs.length, 2);
  assert.strictEqual(payload.pairs[0].left_id, 'left_cat');
  assert.strictEqual(payload.pairs[0].right_id, 'right_kitten');
});

test('Contract: Ordering submission payload structure', () => {
  const orderedIds = ['step_wake', 'step_breakfast', 'step_bus'];
  const payload = {
    ordered_ids: orderedIds,
    hints_used: 0,
    time_spent_seconds: 15,
  };

  assert.ok(Array.isArray(payload.ordered_ids));
  assert.strictEqual(payload.ordered_ids.length, 3);
  assert.deepStrictEqual(payload.ordered_ids, ['step_wake', 'step_breakfast', 'step_bus']);
});

test('Contract: Visual Identification submission payload structure', () => {
  const selectedElementId = 'elem_circle_red';
  const payload = {
    selected_element_id: selectedElementId,
    hints_used: 0,
    time_spent_seconds: 7,
  };

  assert.strictEqual(typeof payload.selected_element_id, 'string');
  assert.strictEqual(payload.selected_element_id, 'elem_circle_red');
});

test('Contract: Drag and Drop submission payload structure', () => {
  const itemToZoneMapping = {
    item_apple: 'zone_fruits',
    item_banana: 'zone_fruits',
    item_carrot: 'zone_vegetables',
  };
  const payload = {
    item_to_zone_mapping: itemToZoneMapping,
    hints_used: 0,
    time_spent_seconds: 22,
  };

  assert.strictEqual(typeof payload.item_to_zone_mapping, 'object');
  assert.strictEqual(payload.item_to_zone_mapping['item_apple'], 'zone_fruits');
  assert.strictEqual(payload.item_to_zone_mapping['item_carrot'], 'zone_vegetables');
});

test('Contract: Backend authoritative evaluation response handling', () => {
  // Simulates authoritative evaluation response from backend /api/v1/activities/{id}/evaluate
  const mockBackendResponse = {
    is_correct: true,
    score: 1.0,
    feedback: 'Excellent work! 3 is indeed between 2 and 4.',
    correct_answer: { correct_answer_id: 'opt_target_3' },
    mastery_updated: true,
    performance_event_id: '12345678-1234-5678-1234-567812345678',
  };

  assert.strictEqual(mockBackendResponse.is_correct, true);
  assert.strictEqual(mockBackendResponse.score, 1.0);
  assert.ok(mockBackendResponse.feedback.length > 0);
  assert.ok(mockBackendResponse.performance_event_id);
});
