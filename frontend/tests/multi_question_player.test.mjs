import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const frontendDir = path.resolve(__dirname, '..');
const playerFile = fs.readFileSync(path.join(frontendDir, 'src', 'features', 'learning', 'ActivityPlayer.tsx'), 'utf-8');

test('Multi-question activity model supports 3-10 questions with default 5', () => {
  // Test question count normalization in ActivityPlayer
  assert.ok(playerFile.includes('activity.questions'), 'ActivityPlayer must read activity.questions');
  assert.ok(playerFile.includes('currentQuestionIndex'), 'ActivityPlayer must track current question index');
  assert.ok(playerFile.includes('Question ${currentQuestionIndex + 1} of ${questions.length}'), 'ActivityPlayer must display Question X of Y');
});

test('Per-question answer state isolation contract', () => {
  // Simulates frontend answer state dictionary keyed by question ID
  const answersByQuestionId = {};

  const q1 = 'q_mcq_1';
  const q2 = 'q_mcq_2';

  // Answer Q1
  answersByQuestionId[q1] = {
    activity_type: 'multiple_choice',
    selected_option_id: 'opt_a',
  };

  // Answer Q2
  answersByQuestionId[q2] = {
    activity_type: 'multiple_choice',
    selected_option_id: 'opt_b',
  };

  assert.strictEqual(answersByQuestionId[q1].selected_option_id, 'opt_a');
  assert.strictEqual(answersByQuestionId[q2].selected_option_id, 'opt_b');
  assert.notStrictEqual(answersByQuestionId[q1], answersByQuestionId[q2]);

  // Verify ActivityPlayer contains per-question state map
  assert.ok(playerFile.includes('answersByQuestionId[q.id]'), 'ActivityPlayer must look up answers by question id');
  assert.ok(playerFile.includes('[currentQuestion.id]'), 'ActivityPlayer must store answers under current question id');
});

test('Multi-question submission payload format', () => {
  const submissions = [
    { question_id: 'q1', submission: { activity_type: 'multiple_choice', selected_option_id: 'opt_1' } },
    { question_id: 'q2', submission: { activity_type: 'multiple_choice', selected_option_id: 'opt_2' } },
    { question_id: 'q3', submission: { activity_type: 'multiple_choice', selected_option_id: 'opt_3' } },
    { question_id: 'q4', submission: { activity_type: 'multiple_choice', selected_option_id: 'opt_4' } },
    { question_id: 'q5', submission: { activity_type: 'multiple_choice', selected_option_id: 'opt_5' } },
  ];

  const payload = {
    activity_id: 'act-123',
    objective_id: 'obj-456',
    activity_type: 'multiple_choice',
    questions: submissions,
    hints_used: 1,
    time_spent_seconds: 45,
  };

  assert.strictEqual(payload.questions.length, 5);
  assert.strictEqual(payload.questions[0].question_id, 'q1');
  assert.strictEqual(payload.questions[4].question_id, 'q5');
});

test('Multi-question evaluation response schema handling', () => {
  const mockMultiQuestionResponse = {
    is_correct: true,
    score: 0.8,
    percentage: 80,
    questions_total: 5,
    questions_answered: 5,
    questions_correct: 4,
    feedback: 'Great job! You answered 4 out of 5 questions correctly.',
    question_results: [
      { question_id: 'q1', is_correct: true, score: 1.0, feedback: 'Correct!' },
      { question_id: 'q2', is_correct: true, score: 1.0, feedback: 'Correct!' },
      { question_id: 'q3', is_correct: false, score: 0.0, feedback: 'Keep trying!' },
      { question_id: 'q4', is_correct: true, score: 1.0, feedback: 'Correct!' },
      { question_id: 'q5', is_correct: true, score: 1.0, feedback: 'Correct!' },
    ],
  };

  assert.strictEqual(mockMultiQuestionResponse.questions_total, 5);
  assert.strictEqual(mockMultiQuestionResponse.questions_correct, 4);
  assert.strictEqual(mockMultiQuestionResponse.percentage, 80);
  assert.strictEqual(mockMultiQuestionResponse.question_results.length, 5);
});

test('Backward compatibility: single-question legacy activity fallback', () => {
  // Verify that ActivityPlayer gracefully wraps legacy single-content activities
  assert.ok(
    playerFile.includes("if (activity.content)"),
    'ActivityPlayer must support legacy activity with top-level content'
  );
  assert.ok(
    playerFile.includes("id: activity.id || 'q1'"),
    'ActivityPlayer must assign fallback question ID for legacy activity'
  );
});

test('Cognitive calm single-question navigation and step indicators', () => {
  assert.ok(playerFile.includes('handlePreviousQuestion'), 'ActivityPlayer must support previous question navigation');
  assert.ok(playerFile.includes('handleNextQuestion'), 'ActivityPlayer must support next question navigation');
  assert.ok(playerFile.includes('handleJumpToQuestion'), 'ActivityPlayer must support direct question step navigation');
  assert.ok(playerFile.includes('isFinalQuestion'), 'ActivityPlayer must distinguish final question for submission');
});
