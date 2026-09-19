"""
Eduvia — Security Headers Middleware
Phase 11: System Hardening & Accessibility Audit

Enforces defense-in-depth HTTP security headers on all API responses.
"""
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.config import settings


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware applying strict defense-in-depth HTTP security headers.
    
    Headers applied:
    - X-Content-Type-Options: nosniff
    - X-Frame-Options: DENY
    - Referrer-Policy: strict-origin-when-cross-origin
    - X-XSS-Protection: 0
    - Content-Security-Policy: pragmatic policy safe for development & production
    - Strict-Transport-Security: production HTTPS only (omitted in local HTTP dev)
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)

        # ── Standard Defensive Headers ────────────────────────────────
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["X-XSS-Protection"] = "0"

        # ── Content Security Policy ───────────────────────────────────
        # Pragmatic policy tailored to Eduvia: allows Google Fonts and local API connections
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline'",
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
            "font-src 'self' https://fonts.gstatic.com data:",
            "img-src 'self' data: https:",
            "connect-src 'self' http://localhost:* ws://localhost:* https:",
            "frame-ancestors 'none'",
        ]
        response.headers["Content-Security-Policy"] = "; ".join(csp_directives)

        # ── Strict Transport Security (HSTS) ──────────────────────────
        # Omitted in local HTTP development; enforced in production/HTTPS
        if settings.is_production:
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )

        return response
