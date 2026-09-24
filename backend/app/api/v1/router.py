"""
Eduvia — API v1 Router

Central router that aggregates all v1 API sub-routers.
Add new feature routers here as they are implemented.
"""
from fastapi import APIRouter

from app.activities.router import router as activities_router
from app.analytics.router import router as analytics_router
from app.api.v1 import health
from app.auth.router import router as auth_router
from app.curriculum.router import router as curriculum_router
from app.learners.router import router as learners_router
from app.recommendations.router import router as recommendations_router
from app.teachers.router import router as teachers_router
from app.users.router import router as users_router

api_router = APIRouter()

# ── System ────────────────────────────────────────────────────────────────────
api_router.include_router(
    health.router,
    prefix="/health",
    tags=["system"],
)

# ── Auth & Users ──────────────────────────────────────────────────────────────
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])

# ── Curriculum (Phase 2) ──────────────────────────────────────────────────────
api_router.include_router(curriculum_router)

# ── Learners (Phase 3) ────────────────────────────────────────────────────────
api_router.include_router(learners_router)

# ── Activities (Phase 4 & 5) ──────────────────────────────────────────────────
api_router.include_router(activities_router)

# ── Analytics & Telemetry (Phase 6 & 7) ───────────────────────────────────────
api_router.include_router(analytics_router)

# ── Recommendations & Adaptive Learning (Phase 8) ─────────────────────────────
api_router.include_router(recommendations_router)

# ── Teacher Dashboard & Insights (Phase 10) ───────────────────────────────────
api_router.include_router(teachers_router, prefix="/teachers")
api_router.include_router(teachers_router, prefix="/teacher")

