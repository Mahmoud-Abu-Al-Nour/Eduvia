"""
Eduvia — API v1 Router

Central router that aggregates all v1 API sub-routers.
Add new feature routers here as they are implemented.
"""
from fastapi import APIRouter

from app.api.v1 import health

from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.curriculum.router import router as curriculum_router

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

# ── Future routers (Phase 2+) ─────────────────────────────────────────────────
# api_router.include_router(learners.router, prefix="/learners", tags=["learners"])
# api_router.include_router(curriculum.router, prefix="/curriculum", tags=["curriculum"])
# api_router.include_router(activities.router, prefix="/activities", tags=["activities"])
# api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
# api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
