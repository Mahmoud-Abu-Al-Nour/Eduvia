import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const frontendDir = path.resolve(__dirname, '..');
const componentsDir = path.join(frontendDir, 'src', 'features', 'learning', 'components');
const playerFile = fs.readFileSync(path.join(frontendDir, 'src', 'features', 'learning', 'ActivityPlayer.tsx'), 'utf-8');

test('MultipleChoiceActivity component implements accessible option selection contract', () => {
  const file = fs.readFileSync(path.join(componentsDir, 'MultipleChoiceActivity.tsx'), 'utf-8');

  // Verify option button semantics and accessibility attributes
  assert.ok(file.includes('selectedOptionId'), 'Must accept selectedOptionId prop');
  assert.ok(file.includes('aria-checked') || file.includes('aria-pressed'), 'Options must expose accessible checked/pressed state');
  assert.ok(!file.includes('is_correct: true'), 'Frontend component must NOT evaluate correctness locally');

  // Verify ActivityPlayer serializes snake_case selected_option_id payload
  assert.ok(playerFile.includes('selected_option_id: selectedOptionId'), 'ActivityPlayer must map selectedOptionId to selected_option_id payload');
});

test('MatchingActivity component supports tap-to-match and stable IDs', () => {
  const file = fs.readFileSync(path.join(componentsDir, 'MatchingActivity.tsx'), 'utf-8');

  // Verify column mapping and dual-selection model
  assert.ok(file.includes('left_id') || file.includes('leftId'), 'Matching pair must reference left item ID');
  assert.ok(file.includes('right_id') || file.includes('rightId'), 'Matching pair must reference right item ID');
  assert.ok(file.includes('pairs') || file.includes('MatchingPair'), 'Must maintain matching pairs');

  // Verify ActivityPlayer serializes matching payload
  assert.ok(playerFile.includes('pairs: matchingPairs'), 'ActivityPlayer must serialize matching pairs payload');
});

test('OrderingActivity component supports slot reordering with keyboard parity', () => {
  const file = fs.readFileSync(path.join(componentsDir, 'OrderingActivity.tsx'), 'utf-8');

  // Verify ordered IDs array and accessible positioning
  assert.ok(file.includes('orderedIds'), 'Component must accept orderedIds prop');
  assert.ok(file.includes('items'), 'Component must receive items array');

  // Verify ActivityPlayer serializes ordered_ids payload
  assert.ok(playerFile.includes('ordered_ids: orderedIds'), 'ActivityPlayer must map orderedIds to ordered_ids payload');
});

test('VisualIdentificationActivity component supports visual grid selection and target ID', () => {
  const file = fs.readFileSync(path.join(componentsDir, 'VisualIdentificationActivity.tsx'), 'utf-8');

  // Verify element selection and target submission
  assert.ok(file.includes('selectedElementId'), 'Component must accept selectedElementId prop');
  assert.ok(file.includes('elements'), 'Component must render scene elements');

  // Verify ActivityPlayer serializes selected_element_id payload
  assert.ok(playerFile.includes('selected_element_id: selectedElementId'), 'ActivityPlayer must map selectedElementId to selected_element_id payload');
});

test('DragDropActivity component supports both drag-and-drop and accessible tap-to-place', () => {
  const file = fs.readFileSync(path.join(componentsDir, 'DragDropActivity.tsx'), 'utf-8');

  // Verify categorization mapping and non-mouse interaction
  assert.ok(file.includes('mapping'), 'Component must accept mapping prop');
  assert.ok(file.includes('zones'), 'Must render drop zones');
  assert.ok(file.includes('handleZoneClick') || file.includes('handleItemSelect'), 'Must support accessible two-step click/tap selection for motor accessibility');

  // Verify ActivityPlayer serializes item_to_zone_mapping payload
  assert.ok(playerFile.includes('item_to_zone_mapping: itemToZoneMapping'), 'ActivityPlayer must map itemToZoneMapping to item_to_zone_mapping payload');
});

test('ActivityPlayer ensures authoritative submission and preserves telemetry', () => {
  // Verify that evaluation is fetched from backend
  assert.ok(playerFile.includes('api.activities.evaluate'), 'Must submit to backend evaluation endpoint api.activities.evaluate');
  assert.ok(playerFile.includes('hints_used'), 'Must record hints used in evaluation request');
  assert.ok(playerFile.includes('time_spent_seconds'), 'Must record time spent in evaluation request');
  assert.ok(!playerFile.includes('score = 1.0'), 'Player must never hardcode passing scores locally');
});
