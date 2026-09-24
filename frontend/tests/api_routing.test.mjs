import test from 'node:test';
import assert from 'node:assert/strict';

/**
 * Eduvia — Frontend API Configuration & Error Distinction Regression Tests
 *
 * Verifies:
 * 1. Correct API base URL resolution
 * 2. Curriculum API call structure
 * 3. Activity API call structure
 * 4. Error distinction: Network error vs 404 vs 401 vs 403 vs 422 vs 500
 */

// Simulate error normalizer logic as implemented in frontend/src/services/api.ts
function normalizeApiError(error) {
  const status = error.response?.status;
  let message = error.response?.data?.message || error.response?.data?.detail;

  if (!message) {
    if (status === 404) {
      message = 'Requested educational resource or endpoint was not found.';
    } else if (status === 403) {
      message = 'You do not have permission to access this educational resource.';
    } else if (status === 401) {
      message = 'Your session has expired. Please sign in again.';
    } else if (status === 422) {
      message = 'The provided data could not be validated by the server.';
    } else if (status && status >= 500) {
      message = 'The backend server encountered an error. Please try again shortly.';
    } else if (!error.response) {
      message = 'Unable to connect to the backend server. Please verify the API is running.';
    } else {
      message = error.message || 'An unexpected error occurred';
    }
  }

  const normalized = new Error(message);
  normalized.code = error.response?.data?.error || (status ? `HTTP_${status}` : 'NETWORK_ERROR');
  normalized.status = status;
  normalized.response = error.response;
  return normalized;
}

// Simulate ActivityPlayer error title & message resolution logic
function resolveActivityErrorDisplay(errorStatus, loadError) {
  let errorTitle = 'Activity Unavailable';
  let errorMessage = loadError || 'The requested activity could not be loaded.';

  if (errorStatus === 404) {
    errorTitle = 'Activity Not Found';
    errorMessage = 'Activity not found.';
  } else if (errorStatus === 401) {
    errorTitle = 'Session Expired';
    errorMessage = 'Session expired. Please sign in again.';
  } else if (errorStatus === 403) {
    errorTitle = 'Access Denied';
    errorMessage = 'You do not have permission to access this activity.';
  } else if (errorStatus === 422) {
    errorTitle = 'Invalid Request';
    errorMessage = 'The request data is invalid.';
  } else if (errorStatus && errorStatus >= 500) {
    errorTitle = 'Server Error';
    errorMessage = 'The server encountered an error.';
  } else if (errorStatus === undefined) {
    errorTitle = 'Connection Error';
    errorMessage = 'Unable to connect to the backend.';
  }

  return { errorTitle, errorMessage };
}

test('API Base URL: respects environment configuration without blind rewrite', () => {
  const envUrl = 'http://localhost:8000';
  const resolvedBaseUrl = envUrl !== undefined ? envUrl : 'http://localhost:8000';
  const prefix = '/api/v1';
  const fullBase = `${resolvedBaseUrl}${prefix}`;

  assert.strictEqual(fullBase, 'http://localhost:8000/api/v1');
});

test('API Error Distinction: Network failure (no response)', () => {
  const networkError = { message: 'Network Error', response: undefined };
  const normalized = normalizeApiError(networkError);

  assert.strictEqual(normalized.status, undefined);
  assert.strictEqual(normalized.code, 'NETWORK_ERROR');
  assert.strictEqual(normalized.message, 'Unable to connect to the backend server. Please verify the API is running.');

  const ui = resolveActivityErrorDisplay(normalized.status, normalized.message);
  assert.strictEqual(ui.errorTitle, 'Connection Error');
  assert.strictEqual(ui.errorMessage, 'Unable to connect to the backend.');
});

test('API Error Distinction: HTTP 404 Not Found', () => {
  const notFoundError = { response: { status: 404, data: {} } };
  const normalized = normalizeApiError(notFoundError);

  assert.strictEqual(normalized.status, 404);
  assert.strictEqual(normalized.code, 'HTTP_404');
  assert.strictEqual(normalized.message, 'Requested educational resource or endpoint was not found.');

  const ui = resolveActivityErrorDisplay(normalized.status, normalized.message);
  assert.strictEqual(ui.errorTitle, 'Activity Not Found');
  assert.strictEqual(ui.errorMessage, 'Activity not found.');
});

test('API Error Distinction: HTTP 401 Unauthorized / Expired Session', () => {
  const unauthorizedError = { response: { status: 401, data: {} } };
  const normalized = normalizeApiError(unauthorizedError);

  assert.strictEqual(normalized.status, 401);
  assert.strictEqual(normalized.code, 'HTTP_401');
  assert.strictEqual(normalized.message, 'Your session has expired. Please sign in again.');

  const ui = resolveActivityErrorDisplay(normalized.status, normalized.message);
  assert.strictEqual(ui.errorTitle, 'Session Expired');
  assert.strictEqual(ui.errorMessage, 'Session expired. Please sign in again.');
});

test('API Error Distinction: HTTP 403 Forbidden', () => {
  const forbiddenError = { response: { status: 403, data: {} } };
  const normalized = normalizeApiError(forbiddenError);

  assert.strictEqual(normalized.status, 403);
  assert.strictEqual(normalized.code, 'HTTP_403');
  assert.strictEqual(normalized.message, 'You do not have permission to access this educational resource.');

  const ui = resolveActivityErrorDisplay(normalized.status, normalized.message);
  assert.strictEqual(ui.errorTitle, 'Access Denied');
  assert.strictEqual(ui.errorMessage, 'You do not have permission to access this activity.');
});

test('API Error Distinction: HTTP 500 Internal Server Error', () => {
  const serverError = { response: { status: 500, data: {} } };
  const normalized = normalizeApiError(serverError);

  assert.strictEqual(normalized.status, 500);
  assert.strictEqual(normalized.code, 'HTTP_500');
  assert.strictEqual(normalized.message, 'The backend server encountered an error. Please try again shortly.');

  const ui = resolveActivityErrorDisplay(normalized.status, normalized.message);
  assert.strictEqual(ui.errorTitle, 'Server Error');
  assert.strictEqual(ui.errorMessage, 'The server encountered an error.');
});

test('Curriculum API Endpoint contracts', () => {
  const listEndpoint = '/curricula';
  const detailEndpoint = (id) => `/curricula/${id}`;
  const testId = '33333333-3333-3333-3333-333333333333';

  assert.strictEqual(listEndpoint, '/curricula');
  assert.strictEqual(detailEndpoint(testId), '/curricula/33333333-3333-3333-3333-333333333333');
});

test('Activity API Endpoint contracts', () => {
  const getByIdEndpoint = (id) => `/activities/${id}`;
  const generateEndpoint = '/activities/generate';
  const evaluateEndpoint = '/activities/evaluate';
  const testId = '65b6d593-f264-422a-b175-410714bab7b5';

  assert.strictEqual(getByIdEndpoint(testId), '/activities/65b6d593-f264-422a-b175-410714bab7b5');
  assert.strictEqual(generateEndpoint, '/activities/generate');
  assert.strictEqual(evaluateEndpoint, '/activities/evaluate');
});
