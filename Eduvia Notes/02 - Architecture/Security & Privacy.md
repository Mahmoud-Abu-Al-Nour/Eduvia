# Security & Privacy

Security and student data privacy are central to Eduvia's engineering principles.

---

## Core Security Controls

1. **Authentication**:
   - Cryptographic hashing: `bcrypt` (or `Argon2`) for all stored user passwords.
   - Stateless JWT tokens signed with `HS256` using `JWT_SECRET` loaded strictly from environment variables.
   - Configurable access token expiry (`JWT_ACCESS_TOKEN_EXPIRE_MINUTES`).

2. **Role-Based Access Control (RBAC)**:
   - FastAPI dependencies: `get_current_user`, `get_current_active_admin`, `get_current_active_teacher`.
   - Admin-only routes (e.g., `POST /curricula`) strictly reject non-admin users with HTTP 403 Forbidden.

3. **Zero Hardcoded Secrets Policy**:
   - Tracked repository files are scanned and verified to contain zero API keys, passwords, or JWT secrets.
   - `.env` is ignored by `.gitignore`.
   - `.env.example` provides safe placeholder values only.

4. **Student Privacy**:
   - In accordance with COPPA, FERPA, and GDPR principles, no unnecessary personally identifiable information (PII) is required for learner activity participation in MVP.
