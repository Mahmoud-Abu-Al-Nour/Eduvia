# Phase 1 — Database & Authentication

## Goal
Implement relational persistence and secure role-based authentication for Teachers and Administrators.

## Scope
- SQLAlchemy async engine and declarative base.
- User domain entity with `admin` and `teacher` roles.
- Password hashing using `bcrypt` / `Argon2`.
- OAuth2 password flow with JWT token issuance (`/api/v1/auth/login`).
- Protected routes and dependency injection (`get_current_user`, `get_current_active_admin`).
- Frontend authentication state (`AuthContext.tsx`, `LoginPage.tsx`, `ProtectedRoute.tsx`).

## Architectural Decisions
- Learners are explicitly **NOT** traditional authenticated users in MVP.
- Passwords are encrypted with industry-standard key derivation.
