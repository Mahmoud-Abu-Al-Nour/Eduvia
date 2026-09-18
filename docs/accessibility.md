# Eduvia — API Design

## Base URL

/api/v1

## Authentication

All teacher/admin endpoints require Bearer JWT token.
Learner endpoints use session-based access (no login required in MVP).

## Endpoints (Planned)

### System
- GET /health — Basic health check
- GET /health/detailed — Full dependency status

### Auth (Phase 1)
- POST /auth/login
- POST /auth/refresh
- POST /auth/logout

### Users (Phase 1)
- GET /users/me
- PUT /users/me

### Learners (Phase 3)
- GET /learners
- POST /learners
- GET /learners/{id}
- PUT /learners/{id}
- GET /learners/{id}/profile
- GET /learners/{id}/performance
- GET /learners/{id}/recommendations

### Curriculum (Phase 2)
- GET /curriculum
- POST /curriculum
- GET /curriculum/{id}
- GET /curriculum/{id}/subjects
- GET /subjects/{id}/units
- GET /units/{id}/lessons
- GET /lessons/{id}/objectives

### Activities (Phase 4)
- POST /activities/generate
- GET /activities/{id}
- POST /activities/{id}/attempt

### Analytics (Phase 7)
- GET /analytics/learners/{id}
- POST /analytics/events

## Response Format

Success:
\\\json
{ "data": { ... } }
\\\

Error:
\\\json
{ "error": "error_code", "message": "Human readable message" }
\\\
"@ | Set-Content "d:\test-vibe-codeing\Eduvia\docs\api-design.md" -Encoding UTF8

@"
# Eduvia — Accessibility

## Core Requirement

Accessibility is a fundamental design requirement for the learner interface.
The learner interface must serve users with intellectual disabilities and special educational needs.

## WCAG Compliance Target

WCAG 2.1 Level AA minimum for learner interface.

## Requirements

### Visual
- Minimum 16px body text
- Color contrast ratio ≥ 4.5:1 for normal text
- Color contrast ratio ≥ 3:1 for large text and UI components
- Never use color alone to convey information

### Interaction
- Minimum 44×44px touch targets (WCAG 2.5.5)
- Keyboard navigable interface
- Focus-visible outlines on all interactive elements
- No time limits on interactions

### Motion
- Respect prefers-reduced-motion media query
- No autoplay animations
- Provide alternatives to motion-based interactions

### Screen Reader
- Semantic HTML (nav, main, section, article, etc.)
- ARIA labels on icon buttons
- Role and state attributes on custom components
- Meaningful alt text on all images
- Skip navigation link at page top

### Language
- Simple, clear language in learner interface
- Avoid jargon in learner-facing content
- Optional audio instructions for activities

## Learner Interface Specific

- Extra-large buttons (minimum 3rem height)
- Clear visual feedback for all interactions
- Success/error states with icons + text (not color only)
- Minimal cognitive load — one task at a time
- Predictable navigation patterns
- No pop-ups without user initiation
