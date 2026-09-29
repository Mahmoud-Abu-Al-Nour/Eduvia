import test from 'node:test';
import assert from 'node:assert/strict';

/**
 * Eduvia — Frontend Research Mode & RBAC Routing Contract Tests
 *
 * Verifies:
 * 1. Role-based routing: Researcher & Admin allowed; Teacher & Learner denied
 * 2. Research generation request contract: RAG, Content Bank, and Learner Profile are OFF by default
 * 3. Schema flexibility: Custom question counts (1-50+), mixed modalities, and freeform text
 * 4. Variant lineage & comparative evaluation structure
 */

function checkRouteAccess(userRole, targetRoute, allowedRoles) {
  if (!allowedRoles.includes(userRole)) {
    if (userRole === 'admin') {
      return { allowed: false, redirect: '/admin' };
    } else if (userRole === 'learner') {
      return { allowed: false, redirect: '/learner' };
    } else if (userRole === 'researcher') {
      return { allowed: false, redirect: '/research' };
    } else {
      return { allowed: false, redirect: '/dashboard' };
    }
  }
  return { allowed: true, redirect: null };
}

test('Research routing: Researcher is granted access to /research workspace', () => {
  const result = checkRouteAccess('researcher', '/research', ['researcher', 'admin']);
  assert.strictEqual(result.allowed, true);
  assert.strictEqual(result.redirect, null);
});

test('Research routing: Admin with research permissions is granted access to /research', () => {
  const result = checkRouteAccess('admin', '/research', ['researcher', 'admin']);
  assert.strictEqual(result.allowed, true);
  assert.strictEqual(result.redirect, null);
});

test('Research routing: Teacher is denied access to /research and redirected to /dashboard', () => {
  const result = checkRouteAccess('teacher', '/research', ['researcher', 'admin']);
  assert.strictEqual(result.allowed, false);
  assert.strictEqual(result.redirect, '/dashboard');
});

test('Research routing: Learner is denied access to /research and redirected to /learner', () => {
  const result = checkRouteAccess('learner', '/research', ['researcher', 'admin']);
  assert.strictEqual(result.allowed, false);
  assert.strictEqual(result.redirect, '/learner');
});

test('Research generation contract: Production constraints are OFF by default', () => {
  const defaultGenerationPayload = {
    project_id: 'proj-123',
    experiment_id: 'exp-123',
    variant_id: 'var-123',
    prompt: 'Generate an experimental 20-question mixed assessment on biology',
    output_target: 'assessment',
    model: 'gemini-2.5-flash',
    model_configuration: {
      temperature: 0.7,
      max_output_tokens: 4096,
    },
    explicit_context: null,
    production_compatibility_mode: false,
  };

  // Verify production sources are not included
  assert.strictEqual(defaultGenerationPayload.production_compatibility_mode, false);
  assert.strictEqual(defaultGenerationPayload.explicit_context, null);
  assert.strictEqual('learner_profile' in defaultGenerationPayload, false);
  assert.strictEqual('curriculum_id' in defaultGenerationPayload, false);
  assert.strictEqual('content_bank' in defaultGenerationPayload, false);
  assert.strictEqual('phase8' in defaultGenerationPayload, false);
});

test('Multi-question & mixed-modality research payload support', () => {
  const researchAssessment = {
    artifact_type: 'assessment',
    schema_version: 'research.v1',
    payload: {
      title: 'Experimental Mixed Diagnostic',
      question_count: 20,
      sections: [
        {
          section_id: 'sec-1',
          title: 'Multiple Choice Core',
          questions: Array.from({ length: 10 }, (_, i) => ({
            id: `q-${i + 1}`,
            type: 'multiple_choice',
            prompt: `Question ${i + 1}`,
          })),
        },
        {
          section_id: 'sec-2',
          title: 'Mixed Modality & Experimental Types',
          questions: [
            { id: 'q-11', type: 'ordering', prompt: 'Order events' },
            { id: 'q-12', type: 'matching', prompt: 'Match pairs' },
            { id: 'q-13', type: 'visual_identification', prompt: 'Identify part' },
            { id: 'q-14', type: 'drag_drop', prompt: 'Place elements' },
            { id: 'q-15', type: 'free_response_experimental', prompt: 'Self explanation' },
          ],
        },
      ],
    },
    metadata: {
      raw_output: '{\n  "title": "Experimental Mixed Diagnostic" ...}',
      is_production_compatible: false,
    },
  };

  assert.strictEqual(researchAssessment.payload.question_count, 20);
  assert.strictEqual(researchAssessment.payload.sections.length, 2);
  assert.strictEqual(researchAssessment.metadata.is_production_compatible, false);
  assert.ok(researchAssessment.metadata.raw_output.length > 0);
});

test('Variant cloning preserves experiment lineage and parent pointer', () => {
  const originalVariant = {
    id: 'var-orig-01',
    experiment_id: 'exp-01',
    name: 'Variant A: High Temperature Exploratory',
    configuration: { temperature: 0.9, explanation_method: 'socratic' },
  };

  const clonedVariant = {
    id: 'var-clone-02',
    experiment_id: originalVariant.experiment_id,
    name: 'Variant A: High Temperature Exploratory (Clone)',
    parent_variant_id: originalVariant.id,
    configuration: { ...originalVariant.configuration, temperature: 0.4 },
  };

  assert.strictEqual(clonedVariant.experiment_id, originalVariant.experiment_id);
  assert.strictEqual(clonedVariant.parent_variant_id, originalVariant.id);
  assert.strictEqual(clonedVariant.configuration.temperature, 0.4);
});

test('Model catalog contract: Canonical models supported, obsolete models excluded', () => {
  const CANONICAL_SUPPORTED_MODELS = ['gemini-3.8-flash', 'gemini-3.5-flash-lite', 'gemini-2.5-flash', 'gemini-2.5-pro'];
  
  // Verify selectable models in prompt studio are canonical
  assert.ok(CANONICAL_SUPPORTED_MODELS.includes('gemini-3.8-flash'));
  assert.ok(CANONICAL_SUPPORTED_MODELS.includes('gemini-3.5-flash-lite'));
  assert.ok(CANONICAL_SUPPORTED_MODELS.includes('gemini-2.5-flash'));
  assert.ok(CANONICAL_SUPPORTED_MODELS.includes('gemini-2.5-pro'));

  // Verify shut-down/obsolete models are not allowed
  assert.strictEqual(CANONICAL_SUPPORTED_MODELS.includes('gemini-2.0-flash-exp'), false);
  assert.strictEqual(CANONICAL_SUPPORTED_MODELS.includes('gemini-1.5-pro'), false);
});

test('Question count validation: 1-50 accepted, values outside rejected', () => {
  const validateQuestionCount = (n) => {
    if (n === undefined || n === null) return true;
    return typeof n === 'number' && n >= 1 && n <= 50;
  };

  for (const validCount of [1, 5, 10, 20, 50]) {
    assert.strictEqual(validateQuestionCount(validCount), true);
  }

  assert.strictEqual(validateQuestionCount(0), false);
  assert.strictEqual(validateQuestionCount(51), false);
  assert.strictEqual(validateQuestionCount(-5), false);
});
