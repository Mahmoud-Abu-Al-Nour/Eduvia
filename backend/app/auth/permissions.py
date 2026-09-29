"""
Eduvia — Centralized Role-Based Access Control (RBAC) & Scope Matrix

Defines authoritative permission codes, role mappings, and scope resolution
to ensure server-side security boundaries:
Authentication -> Identity -> Role -> Permission -> Resource Scope -> Operation
"""
from __future__ import annotations

import enum
import uuid
from typing import Any

from app.users.models import User, UserRole


class Permission(str, enum.Enum):
    # Platform / Users
    USERS_READ_GLOBAL = "users.read.global"
    USERS_MANAGE = "users.manage"
    ROLES_MANAGE = "roles.manage"
    ADMIN_DASHBOARD = "admin.dashboard"

    # Learners
    LEARNERS_READ_GLOBAL = "learners.read.global"
    LEARNERS_READ_ASSIGNED = "learners.read.assigned"
    LEARNERS_READ_SELF = "learners.read.self"
    LEARNERS_MANAGE_ASSIGNED = "learners.manage.assigned"
    LEARNERS_CREATE = "learners.create"

    # Curriculum
    CURRICULUM_READ_GLOBAL = "curriculum.read.global"
    CURRICULUM_READ_ASSIGNED = "curriculum.read.assigned"
    CURRICULUM_READ_ENROLLED = "curriculum.read.enrolled"
    CURRICULUM_MANAGE = "curriculum.manage"

    # Content & Instructional
    CONTENT_GENERATE = "content.generate"
    CONTENT_READ_ASSIGNED = "content.read.assigned"
    CONTENT_READ_PUBLISHED = "content.read.published"
    CONTENT_APPROVE = "content.approve"
    CONTENT_PUBLISH = "content.publish"

    # Activities
    ACTIVITIES_GENERATE = "activities.generate"
    ACTIVITIES_READ_ASSIGNED = "activities.read.assigned"
    ACTIVITIES_READ_SELF = "activities.read.self"
    ACTIVITIES_EVALUATE = "activities.evaluate"

    # Assessments
    ASSESSMENTS_CREATE = "assessments.create"
    ASSESSMENTS_PUBLISH = "assessments.publish"
    ASSESSMENTS_READ_ASSIGNED = "assessments.read.assigned"
    ASSESSMENTS_READ_SELF = "assessments.read.self"

    # Analytics
    ANALYTICS_READ_GLOBAL = "analytics.read.global"
    ANALYTICS_READ_ASSIGNED = "analytics.read.assigned"
    ANALYTICS_READ_SELF = "analytics.read.self"

    # Profile
    PROFILE_READ_SELF = "profile.read.self"
    PROFILE_UPDATE_SELF = "profile.update.self"
    PROFILE_READ_ASSIGNED = "profile.read.assigned"

    # Teacher Tools
    TEACHERS_DASHBOARD = "teachers.dashboard"

    # Research Workspace & Sandbox
    RESEARCH_WORKSPACE_READ = "research.workspace.read"
    RESEARCH_PROJECT_CREATE = "research.project.create"
    RESEARCH_PROJECT_READ_OWN = "research.project.read.own"
    RESEARCH_PROJECT_UPDATE_OWN = "research.project.update.own"
    RESEARCH_PROJECT_DELETE_OWN = "research.project.delete.own"
    RESEARCH_EXPERIMENT_CREATE = "research.experiment.create"
    RESEARCH_EXPERIMENT_READ_OWN = "research.experiment.read.own"
    RESEARCH_VARIANT_CREATE = "research.variant.create"
    RESEARCH_RUN_CREATE = "research.run.create"
    RESEARCH_RUN_READ_OWN = "research.run.read.own"
    RESEARCH_ARTIFACT_READ_OWN = "research.artifact.read.own"
    RESEARCH_ARTIFACT_UPDATE_OWN = "research.artifact.update.own"
    RESEARCH_EVALUATION_CREATE = "research.evaluation.create"
    RESEARCH_COMPARE = "research.compare"
    RESEARCH_EXPORT = "research.export"
    RESEARCH_CONTEXT_CREATE = "research.context.create"
    RESEARCH_SNAPSHOT_CREATE = "research.snapshot.create"
    RESEARCH_PROMOTE = "research.promote"


# ── Authoritative Role to Permissions Mapping ──────────────────────────────

ROLE_PERMISSIONS: dict[UserRole, set[Permission]] = {
    UserRole.admin: set(Permission),  # Admins possess platform-wide permissions
    UserRole.teacher: {
        Permission.LEARNERS_READ_ASSIGNED,
        Permission.LEARNERS_MANAGE_ASSIGNED,
        Permission.LEARNERS_CREATE,
        Permission.CURRICULUM_READ_GLOBAL,
        Permission.CURRICULUM_READ_ASSIGNED,
        Permission.CONTENT_GENERATE,
        Permission.CONTENT_READ_ASSIGNED,
        Permission.CONTENT_READ_PUBLISHED,
        Permission.CONTENT_APPROVE,
        Permission.CONTENT_PUBLISH,
        Permission.ACTIVITIES_GENERATE,
        Permission.ACTIVITIES_READ_ASSIGNED,
        Permission.ACTIVITIES_READ_SELF,
        Permission.ACTIVITIES_EVALUATE,
        Permission.ASSESSMENTS_CREATE,
        Permission.ASSESSMENTS_PUBLISH,
        Permission.ASSESSMENTS_READ_ASSIGNED,
        Permission.ANALYTICS_READ_ASSIGNED,
        Permission.PROFILE_READ_SELF,
        Permission.PROFILE_UPDATE_SELF,
        Permission.PROFILE_READ_ASSIGNED,
        Permission.TEACHERS_DASHBOARD,
    },
    UserRole.learner: {
        Permission.LEARNERS_READ_SELF,
        Permission.CURRICULUM_READ_ENROLLED,
        Permission.CONTENT_READ_PUBLISHED,
        Permission.ACTIVITIES_READ_SELF,
        Permission.ACTIVITIES_EVALUATE,
        Permission.ASSESSMENTS_READ_SELF,
        Permission.ANALYTICS_READ_SELF,
        Permission.PROFILE_READ_SELF,
        Permission.PROFILE_UPDATE_SELF,
    },
    UserRole.researcher: {
        Permission.RESEARCH_WORKSPACE_READ,
        Permission.RESEARCH_PROJECT_CREATE,
        Permission.RESEARCH_PROJECT_READ_OWN,
        Permission.RESEARCH_PROJECT_UPDATE_OWN,
        Permission.RESEARCH_PROJECT_DELETE_OWN,
        Permission.RESEARCH_EXPERIMENT_CREATE,
        Permission.RESEARCH_EXPERIMENT_READ_OWN,
        Permission.RESEARCH_VARIANT_CREATE,
        Permission.RESEARCH_RUN_CREATE,
        Permission.RESEARCH_RUN_READ_OWN,
        Permission.RESEARCH_ARTIFACT_READ_OWN,
        Permission.RESEARCH_ARTIFACT_UPDATE_OWN,
        Permission.RESEARCH_EVALUATION_CREATE,
        Permission.RESEARCH_COMPARE,
        Permission.RESEARCH_EXPORT,
        Permission.RESEARCH_CONTEXT_CREATE,
        Permission.RESEARCH_SNAPSHOT_CREATE,
        Permission.PROFILE_READ_SELF,
        Permission.PROFILE_UPDATE_SELF,
    },
}


def get_user_role(user: User | None) -> UserRole | None:
    """Normalize user role to UserRole enum."""
    if not user or not user.role:
        return None
    if isinstance(user.role, UserRole):
        return user.role
    try:
        return UserRole(str(user.role))
    except ValueError:
        return None


def has_permission(user: User | None, permission: Permission | str) -> bool:
    """
    Check whether a user possesses a specific permission based on their role.
    """
    if not user or not user.is_active:
        return False
    role = get_user_role(user)
    if not role:
        return False
    if role == UserRole.admin:
        return True
    perm_enum = Permission(permission) if isinstance(permission, str) else permission
    return perm_enum in ROLE_PERMISSIONS.get(role, set())


def check_resource_scope(
    user: User,
    *,
    owner_teacher_id: uuid.UUID | None = None,
    owner_user_id: uuid.UUID | None = None,
    target_learner_id: uuid.UUID | None = None,
    user_learner_id: uuid.UUID | None = None,
) -> bool:
    """
    Authoritatively verify resource ownership/scope.
    - Admin: Full platform scope (always authorized).
    - Teacher: Authorized if owner_teacher_id matches teacher's user ID.
    - Learner: Authorized only if owner_user_id matches learner's user ID
               or target_learner_id matches user_learner_id.
    """
    role = get_user_role(user)
    if not role:
        return False

    if role == UserRole.admin:
        return True

    if role == UserRole.teacher:
        if owner_teacher_id is not None:
            return owner_teacher_id == user.id
        return False

    if role == UserRole.learner:
        if owner_user_id is not None and owner_user_id == user.id:
            return True
        if (
            target_learner_id is not None
            and user_learner_id is not None
            and target_learner_id == user_learner_id
        ):
            return True
        return False

    if role == UserRole.researcher:
        if owner_user_id is not None:
            return owner_user_id == user.id
        return False

    return False
