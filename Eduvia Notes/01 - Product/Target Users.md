# Target Users & Personas

Eduvia is designed for three distinct user roles with strict separation of concerns.

---

## 1. The Teacher / Special Educator
- **Role**: Primary manager of instructional planning and IEP execution.
- **Authentication**: Email/password authentication, JWT bearer token, role `teacher`.
- **Capabilities**:
  - Browse and assign standardized curricula.
  - Review learner profiles and affinity distributions.
  - Inspect activity logs, struggle points, and suggested pedagogical strategies.
  - Override system adaptations when clinical intuition dictates.

## 2. The Administrator
- **Role**: Institutional governance and system configuration.
- **Authentication**: JWT bearer token, role `admin`.
- **Capabilities**:
  - Manage user accounts (create, activate, assign roles).
  - Create and publish foundational curricula and learning standards.
  - Monitor institutional usage, uptime, and system diagnostics.

## 3. The Learner (Domain Entity)
- **Role**: The student engaging with adaptive educational activities.
- **Authentication**: **NO traditional credentials required in MVP.**
- **Rationale**: Requiring young learners or children with fine-motor or cognitive challenges to remember emails, passwords, or 2FA creates immediate accessibility barriers. Learners participate through classroom sessions managed by teachers or simplified local access.
