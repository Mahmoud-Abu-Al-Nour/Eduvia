"""
Eduvia — Activities Domain (Phase 4)
"""
from app.activities.fallbacks import create_fallback_activity
from app.activities.router import router
from app.activities.schemas import (
    Activity,
    ActivityContent,
    ActivityEvaluationResponse,
    ActivityGenerateRequest,
    ActivityGenerateResponse,
    ActivityInteractionState,
    ActivitySubmissionPayload,
    ActivitySubmissionRequest,
    ActivityType,
    DragDropContent,
    DragDropSubmission,
    MatchingContent,
    MatchingSubmission,
    MultipleChoiceContent,
    MultipleChoiceSubmission,
    OrderingContent,
    OrderingSubmission,
    VisualIdentificationContent,
    VisualIdentificationSubmission,
)
from app.activities.service import ActivityService

__all__ = [
    "Activity",
    "ActivityContent",
    "ActivityEvaluationResponse",
    "ActivityGenerateRequest",
    "ActivityGenerateResponse",
    "ActivityInteractionState",
    "ActivityService",
    "ActivitySubmissionPayload",
    "ActivitySubmissionRequest",
    "ActivityType",
    "DragDropContent",
    "DragDropSubmission",
    "MatchingContent",
    "MatchingSubmission",
    "MultipleChoiceContent",
    "MultipleChoiceSubmission",
    "OrderingContent",
    "OrderingSubmission",
    "VisualIdentificationContent",
    "VisualIdentificationSubmission",
    "create_fallback_activity",
    "router",
]

