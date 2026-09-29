import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const frontendDir = path.resolve(__dirname, '..');
const learnerViewFile = fs.readFileSync(path.join(frontendDir, 'src', 'features', 'learning', 'InstructionalContentView.tsx'), 'utf-8');
const teacherStudioFile = fs.readFileSync(path.join(frontendDir, 'src', 'features', 'instructional', 'TeacherInstructionalContent.tsx'), 'utf-8');

test('Instructional content data schema and non-evaluative separation', () => {
  // Non-evaluative contract: Instructional content must NOT have correctness or scoring fields
  assert.ok(!learnerViewFile.includes('score ='), 'Learner instructional page must not compute scores');
  assert.ok(!learnerViewFile.includes('is_correct:'), 'Learner instructional page must not contain correctness checks');
  assert.ok(!learnerViewFile.includes('mastery_updated'), 'Instructional content must not alter mastery directly');

  // Must have direct transition to Practice
  assert.ok(learnerViewFile.includes('Start Practice Activity'), 'Learner instructional page must provide Start Practice Activity transition');
  assert.ok(learnerViewFile.includes('/learn?objective_id='), 'Practice transition must link to activity player with objective ID');
});

test('Four valid explanation methods supported in Teacher Studio', () => {
  const methods = ['visual_explanation', 'step_by_step', 'worked_example', 'text_explanation'];

  for (const m of methods) {
    assert.ok(teacherStudioFile.includes(m), `Teacher Studio must support explanation method: ${m}`);
  }
});

test('Instructional block types rendering contract in Learner View', () => {
  const blockTypes = ['heading', 'text', 'visual_cue', 'step', 'worked_example', 'callout', 'audio_script'];

  for (const b of blockTypes) {
    assert.ok(
      learnerViewFile.includes(`block.block_type === '${b}'`) || learnerViewFile.includes(`case '${b}':`),
      `Learner view must render block type: ${b}`
    );
  }
});

test('Teacher approval workflow: review_required -> approved -> published', () => {
  assert.ok(teacherStudioFile.includes('review_required'), 'Teacher Studio must handle review_required status');
  assert.ok(teacherStudioFile.includes('approve'), 'Teacher Studio must have approval capability');
  assert.ok(teacherStudioFile.includes('publish'), 'Teacher Studio must have publishing capability');
  assert.ok(teacherStudioFile.includes('isApproving'), 'Teacher Studio must handle approving state');
  assert.ok(teacherStudioFile.includes('isPublishing'), 'Teacher Studio must handle publishing state');
});

test('Audio accessibility and Cognitive Calm in Instructional Content', () => {
  assert.ok(learnerViewFile.includes('useSpeechSynthesis'), 'Learner view must integrate useSpeechSynthesis');
  assert.ok(learnerViewFile.includes('speak'), 'Learner view must support read aloud');
  assert.ok(teacherStudioFile.includes('useSpeechSynthesis'), 'Teacher Studio must integrate useSpeechSynthesis');
});
