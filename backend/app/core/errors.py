"""
Eduvia — Centralized Error Handling

Defines application-level exception classes and FastAPI exception handlers.
"""
from typing import Any

import structlog
from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = structlog.get_logger(__name__)


# ── Application Exception Hierarchy ───────────────────────────────────────────


class EduviaError(Exception):
    """Base exception for all Eduvia application errors."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code: str = "internal_error"
    message: str = "An internal error occurred."

    def __init__(self, message: str | None = None, **context: Any) -> None:
        self.message = message or self.__class__.message
        self.context = context
        super().__init__(self.message)


class NotFoundError(EduviaError):
    """Resource not found."""

    status_code = status.HTTP_404_NOT_FOUND
    error_code = "not_found"
    message = "The requested resource was not found."


class ValidationError(EduviaError):
    """Domain validation error."""

    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    error_code = "validation_error"
    message = "The provided data is invalid."


class AuthenticationError(EduviaError):
    """Authentication failed."""

    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "authentication_error"
    message = "Authentication is required."


class AuthorizationError(EduviaError):
    """Insufficient permissions."""

    status_code = status.HTTP_403_FORBIDDEN
    error_code = "authorization_error"
    message = "You do not have permission to perform this action."


class ConflictError(EduviaError):
    """Resource conflict (e.g. duplicate)."""

    status_code = status.HTTP_409_CONFLICT
    error_code = "conflict"
    message = "A resource conflict occurred."


class AIProviderError(EduviaError):
    """AI provider call failed."""

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    error_code = "ai_provider_error"
    message = "The AI service is temporarily unavailable. Please try again."


class DatabaseError(EduviaError):
    """Database operation failed."""

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    error_code = "database_error"
    message = "A database error occurred."


# ── Exception Handlers ────────────────────────────────────────────────────────


async def eduvia_error_handler(request: Request, exc: EduviaError) -> JSONResponse:
    """Handle all EduviaError subclass exceptions."""
    logger.warning(
        "application_error",
        error_code=exc.error_code,
        message=exc.message,
        path=str(request.url),
        context=getattr(exc, "context", {}),
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_code,
            "message": exc.message,
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle FastAPI HTTPExceptions."""
    logger.info(
        "http_exception",
        status_code=exc.status_code,
        detail=exc.detail,
        path=str(request.url),
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "http_error",
            "message": exc.detail,
        },
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle Pydantic request validation errors."""
    errors = exc.errors()
    logger.info(
        "validation_error",
        errors=errors,
        path=str(request.url),
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "error": "validation_error",
            "message": "The request contains invalid data.",
            "details": errors,
        },
    )
