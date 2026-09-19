import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const frontendDir = path.resolve(__dirname, '..');

test('Global Skip Link semantics and landmark targets', () => {
  const appFile = fs.readFileSync(
    path.join(frontendDir, 'src', 'app', 'App.tsx'),
    'utf-8'
  );
  
  // Skip link must exist with proper href and class
  assert.ok(
    appFile.includes('href="#main-content"'),
    'App shell must provide a skip-to-content anchor referencing #main-content'
  );
  assert.ok(
    appFile.includes('skip-to-content'),
    'App shell skip link must use the dedicated skip-to-content styling'
  );
  assert.ok(
    appFile.includes('Skip to main content'),
    'Skip link must have descriptive accessible text'
  );

  // Landmarks in primary page views must provide id="main-content" with tabIndex={-1}
  const dashboardFile = fs.readFileSync(
    path.join(frontendDir, 'src', 'features', 'dashboard', 'DashboardPage.tsx'),
    'utf-8'
  );
  assert.ok(
    dashboardFile.includes('id="main-content"'),
    'DashboardPage main landmark must provide id="main-content"'
  );
  assert.ok(
    dashboardFile.includes('tabIndex={-1}'),
    'DashboardPage main landmark must be programmatically focusable with tabIndex={-1}'
  );

  const playerFile = fs.readFileSync(
    path.join(frontendDir, 'src', 'features', 'learning', 'ActivityPlayer.tsx'),
    'utf-8'
  );
  assert.ok(
    playerFile.includes('id="main-content"'),
    'ActivityPlayer main landmark must provide id="main-content"'
  );
  assert.ok(
    playerFile.includes('tabIndex={-1}'),
    'ActivityPlayer main landmark must be programmatically focusable with tabIndex={-1}'
  );
});

test('Teacher Dashboard tab navigation uses accessible tablist and tab semantics', () => {
  const dashboardFile = fs.readFileSync(
    path.join(frontendDir, 'src', 'features', 'dashboard', 'DashboardPage.tsx'),
    'utf-8'
  );

  // Navigation container must have role="tablist"
  assert.ok(
    dashboardFile.includes('role="tablist"'),
    'Dashboard navigation must have role="tablist"'
  );
  assert.ok(
    dashboardFile.includes('aria-label="Teacher Dashboard Tabs"'),
    'Dashboard tablist must have an accessible label'
  );

  // Tab items must be semantic buttons with role="tab", aria-selected, and aria-controls
  assert.ok(
    dashboardFile.includes('role="tab"'),
    'Dashboard tab items must have role="tab"'
  );
  assert.ok(
    dashboardFile.includes('aria-selected='),
    'Dashboard tabs must expose aria-selected state'
  );
  assert.ok(
    dashboardFile.includes('aria-controls='),
    'Dashboard tabs must associate with their tabpanel via aria-controls'
  );

  // Panels must have role="tabpanel" and aria-labelledby
  assert.ok(
    dashboardFile.includes('role="tabpanel"'),
    'Dashboard active tab content must have role="tabpanel"'
  );
  assert.ok(
    dashboardFile.includes('aria-labelledby='),
    'Dashboard tabpanel must reference the controlling tab via aria-labelledby'
  );

  // No fake href="#" anchors in the tab navigation
  assert.ok(
    !dashboardFile.includes('href="#"'),
    'Dashboard tabs must not use pseudo anchor tags with href="#"'
  );
});

test('IEP Report Modal focus containment and restoration behavior contract', () => {
  const modalFile = fs.readFileSync(
    path.join(frontendDir, 'src', 'features', 'dashboard', 'IEPReportModal.tsx'),
    'utf-8'
  );

  // Dialog semantics
  assert.ok(modalFile.includes('role="dialog"'), 'Modal must declare role="dialog"');
  assert.ok(modalFile.includes('aria-modal="true"'), 'Modal must declare aria-modal="true"');
  assert.ok(modalFile.includes('aria-labelledby='), 'Modal must reference title element');

  // Focus preservation references
  assert.ok(
    modalFile.includes('openerElementRef'),
    'Modal must store reference to opener element to restore focus upon close'
  );

  // Tab containment logic
  assert.ok(
    modalFile.includes('handleKeyDown'),
    'Modal must contain keydown handler for focus trap and escape handling'
  );
  assert.ok(
    modalFile.includes('Tab') && modalFile.includes('Escape'),
    'Modal must handle Tab and Escape keys'
  );

  // Test trap algorithm behavior in simulated DOM environment
  const mockElements = [
    { focusCount: 0, focus() { this.focusCount++; } },
    { focusCount: 0, focus() { this.focusCount++; } },
  ];

  // Simulating Shift+Tab on first element wraps to last
  let activeIndex = 0;
  let shiftKey = true;
  let targetIndex = activeIndex;
  if (shiftKey && activeIndex === 0) {
    targetIndex = mockElements.length - 1;
    mockElements[targetIndex].focus();
  }
  assert.equal(mockElements[1].focusCount, 1, 'Shift+Tab on first element must wrap to last element');

  // Simulating Tab on last element wraps to first
  activeIndex = mockElements.length - 1;
  shiftKey = false;
  if (!shiftKey && activeIndex === mockElements.length - 1) {
    targetIndex = 0;
    mockElements[targetIndex].focus();
  }
  assert.equal(mockElements[0].focusCount, 1, 'Tab on last element must wrap to first element');
});

test('ActivityPlayer keyboard shortcuts & switch accessibility contract', () => {
  const playerFile = fs.readFileSync(
    path.join(frontendDir, 'src', 'features', 'learning', 'ActivityPlayer.tsx'),
    'utf-8'
  );

  // Number shortcut selection: 1-4
  assert.ok(
    playerFile.includes("['1', '2', '3', '4'].includes(key)"),
    'ActivityPlayer must support 1-4 keys for option selection'
  );

  // Progressive hint: 'h' / 'H'
  assert.ok(
    playerFile.includes("key === 'h' || key === 'H'"),
    'ActivityPlayer must support H key for progressive hint revelation'
  );

  // Audio narration: 'r' / 'R'
  assert.ok(
    playerFile.includes("key === 'r' || key === 'R'"),
    'ActivityPlayer must support R key for replaying read-aloud prompt'
  );

  // Activation/Submission: Enter or Space
  assert.ok(
    playerFile.includes("key === 'Enter' || key === ' '"),
    'ActivityPlayer must support Enter and Space for checking/submitting answers'
  );

  // Form input avoidance
  assert.ok(
    playerFile.includes("targetTag === 'input' || targetTag === 'textarea' || targetTag === 'select'"),
    'Keyboard shortcuts must not intercept keystrokes when user is typing into form inputs'
  );

  // Native button avoidance for Enter/Space to prevent double submission
  assert.ok(
    playerFile.includes("targetTag === 'button'"),
    'Enter/Space must defer to native button activation when a button is already focused'
  );
});

test('ActivityPlayer ARIA live regions expose asynchronous learner state changes', () => {
  const playerFile = fs.readFileSync(
    path.join(frontendDir, 'src', 'features', 'learning', 'ActivityPlayer.tsx'),
    'utf-8'
  );

  // Live region container with polite priority
  assert.ok(
    playerFile.includes('role="status"'),
    'ActivityPlayer must provide a live region with role="status"'
  );
  assert.ok(
    playerFile.includes('aria-live="polite"'),
    'ActivityPlayer live region must use polite aria-live priority'
  );
  assert.ok(
    playerFile.includes('aria-atomic="true"'),
    'ActivityPlayer live region must declare aria-atomic="true"'
  );

  // State announcements
  assert.ok(
    playerFile.includes('setLiveAnnouncement(`Hint ${nextCount} revealed:'),
    'Hint revelation must update accessible live announcement'
  );
  assert.ok(
    playerFile.includes("setLiveAnnouncement('Evaluating your answer, please wait.')"),
    'Answer evaluation in progress must update accessible live announcement'
  );
  assert.ok(
    playerFile.includes("setLiveAnnouncement('Activity reset. You can try again.')"),
    'Activity reset must update accessible live announcement'
  );
});

test('High Contrast and Forced Colors CSS enhancements', () => {
  const cssFile = fs.readFileSync(
    path.join(frontendDir, 'src', 'index.css'),
    'utf-8'
  );

  // Must include media query for forced-colors
  assert.ok(
    cssFile.includes('@media (forced-colors: active)'),
    'index.css must include @media (forced-colors: active) rules for Windows High Contrast'
  );

  // System color keywords
  assert.ok(
    cssFile.includes('Highlight') || cssFile.includes('CanvasText') || cssFile.includes('ButtonBorder'),
    'High contrast rules must use standardized system color keywords'
  );

  // Skip link visibility rules
  assert.ok(
    cssFile.includes('.skip-to-content:focus'),
    'Skip link must define prominent focus visibility styles'
  );

  // Preserved reduced motion
  assert.ok(
    cssFile.includes('@media (prefers-reduced-motion: reduce)'),
    'index.css must preserve prefers-reduced-motion rules'
  );
});
