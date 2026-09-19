# Eduvia Security & Privacy Engineering

> **Multi-Tenant Protection, Defensive Authentication, and Privacy Preservation for Special Education Data**

---

## The Threat Model in Special Education

Educational records, cognitive profiles, and behavioral telemetry for minors—particularly students receiving special education services under Individualized Education Programs (IEPs)—represent extremely sensitive personal data. Unauthorized disclosure, data cross-contamination between schools, or adversarial tampering with evaluation records can directly harm students and violate strict legal standards (such as FERPA and GDPR).

Eduvia is engineered with defense-in-depth principles:
* **Zero Trust for Client Claims**: The server evaluates all responses and logs all events independently.
* **Multi-Tenant Scoping**: Teachers cannot observe, modify, or infer data belonging to students outside their authorized classroom cohorts.
* **Defense Against Automated Abuse**: Sensitive endpoints (authentication and generative AI execution) are throttled via in-memory sliding-window rate limiters.
* **Zero Hardcoded Secrets**: Secrets are injected strictly via environment variables in local development and Google Cloud Secret Manager in production.

---

## 1. Authentication & Role-Based Access Control (RBAC)

### Cryptographic Identity & Session Management
* **Password Hashing**: Passwords are never stored in plaintext. They are salted and hashed using **Bcrypt** (`passlib[bcrypt]`), with support for Argon2 verification.
* **Stateless Bearer Tokens**: Sessions are authenticated using cryptographic **JSON Web Tokens (JWT)** signed with `HS256`. Tokens encode the subject `user_id`, role, and strict expiration (`exp`) timestamps.
* **Role Hierarchy**:
  * `admin`: Platform administration, system health monitoring, curriculum creation/modification.
  * `teacher`: Creation of learner profiles, classroom assignment, curriculum viewing, activity generation, telemetry inspection, cohort analytics, and IEP progress reporting for assigned students.
  * `learner`: Access to active learning activities and submission endpoints without administrative capabilities.

---

## 2. Multi-Tenant Teacher Scoping & Cohort Isolation

Eduvia enforces strict relational tenant scoping at the service layer:
* In the database, every `Learner` is linked to a `User` (the supervising teacher or classroom educator).
* When a teacher requests learner profiles, telemetry history, mastery summaries, or IEP reports, the `TeacherDashboardService` and `LearnerService` enforce an explicit ownership check:
  ```python
  if learner.teacher_id != current_user.id and current_user.role != "admin":
      raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN,
          detail="Not authorized to access this learner's records"
      )
  ```
* Cross-cohort inspection is rejected with an immediate `403 Forbidden`. No learner metadata, progress percentages, or sensory accommodations are leaked across tenant boundaries.

---

## 3. Rate Limiting & Resource Protection

Generative AI invocations and authentication endpoints are prime targets for resource exhaustion, denial-of-service, or brute-force credential stuffing.

Eduvia implements a **bounded in-memory sliding-window rate limiter** with zero external dependencies, protecting key endpoints:

| Protected Endpoint | Rate Limit Tier | Rejection Behavior |
| :--- | :--- | :--- |
| `POST /api/v1/auth/login` | Bounded brute-force threshold (e.g., 5 req / min / IP) | `429 Too Many Requests` with `Retry-After` header |
| `POST /api/v1/activities/generate` | Generative throughput guard (e.g., 20 req / min / user) | `429 Too Many Requests` with `Retry-After` header |
| `POST /api/v1/activities/evaluate` | Interaction spam guard (e.g., 60 req / min / user) | `429 Too Many Requests` with `Retry-After` header |

*Note: In the current modular monolith, rate limiting is maintained in memory. For horizontal scaling across multiple Cloud Run instances, this is designed to transition to a shared Redis instance.*

---

## 4. HTTP Transport Security & Hardening Headers

Eduvia's ASGI middleware applies enterprise security headers to every outbound HTTP response:

```text
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; font-src 'self' data:;
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Strict-Transport-Security: max-age=31536000; includeSubDomains
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

### Production API Documentation Protection
In development environments, `/docs` (Swagger UI) and `/redoc` provide interactive exploration. In production deployments, these endpoints are **disabled by default** via application configuration (`ENVIRONMENT=production`) to prevent unauthorized schema reconnaissance.

### Cross-Origin Resource Sharing (CORS)
CORS is locked down via `CORSMiddleware`. Allowed origins must be explicitly enumerated in `CORS_ALLOWED_ORIGINS` (e.g., `https://eduvia.app`). Wildcard origins (`*`) are strictly blocked in production.

---

## 5. Secrets Management & Credential Hygiene

* **Zero Repository Secrets**: All passwords, JWT secret keys, and Google Gemini API keys are excluded from Git tracking via `.gitignore`.
* **Automated Scanner Verification**: A dedicated security scanner verifies that no `.env`, `.pem`, `.key`, or plain API tokens exist within the version-controlled codebase.
* **Production Secret Manager**: In Google Cloud environments (Phase 12), configuration values are retrieved at container startup from **Google Cloud Secret Manager**, mounting secrets as secure environment variables inside the Cloud Run container runtime.

---

## Related Documentation

* Master Overview: [[Eduvia Project Overview & Technical Abstract|Eduvia Project Overview & Technical Abstract]]
* System Architecture: [[Eduvia Architecture & System Design|Eduvia Architecture & System Design]]
* Database Security: [[02 - Architecture/Database Architecture|Database Architecture]]
* Security Architecture Overview: [[02 - Architecture/Security & Privacy|Security & Privacy]]
* Production Deployment: [[Eduvia Production & Cloud Deployment|Eduvia Production & Cloud Deployment]]
