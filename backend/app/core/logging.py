"""
Eduvia — Structured Logging Configuration

Uses structlog for JSON-structured logging.
Human-readable in development, JSON in production.
"""
import logging
import sys

import structlog


def configure_logging() -> None:
    """
    Configure structlog for the application.

    - Development: pretty-printed colored console output
    - Production: JSON lines for log aggregation
    """
    from app.core.config import settings

    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    if settings.is_development:
        # Human-friendly output in development
        processors: list[structlog.types.Processor] = [
            *shared_processors,
            structlog.dev.ConsoleRenderer(colors=True),
        ]
    else:
        # JSON lines for production log aggregation (Cloud Logging etc.)
        processors = [
            *shared_processors,
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.DEBUG if settings.APP_DEBUG else logging.INFO
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(sys.stdout),
        cache_logger_on_first_use=True,
    )

    # Also configure stdlib logging to go through structlog
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.DEBUG if settings.APP_DEBUG else logging.INFO,
    )
