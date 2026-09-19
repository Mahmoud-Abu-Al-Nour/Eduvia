"""
Eduvia — Application Configuration

All configuration is sourced from environment variables.
Use .env file for local development (never commit to version control).
"""
from functools import lru_cache
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    All fields with no default are REQUIRED.
    Fields with defaults can be overridden via environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # ── Application ───────────────────────────────────────────────────
    APP_ENV: Literal["development", "staging", "production"] = "development"
    APP_DEBUG: bool = False
    APP_SECRET_KEY: str

    # ── Database (PostgreSQL) ─────────────────────────────────────────
    DATABASE_URL: str

    # ── Vector Database (Qdrant) ──────────────────────────────────────
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str = ""

    # ── AI Provider (Gemini) ──────────────────────────────────────────
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.0-flash-exp"
    GEMINI_EMBEDDING_MODEL: str = "text-embedding-004"

    # ── JWT Authentication ────────────────────────────────────────────
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── CORS ──────────────────────────────────────────────────────────
    CORS_ORIGINS_RAW: str = "http://localhost:5173,http://localhost:3000"

    @property
    def CORS_ORIGINS(self) -> list[str]:
        """Parse comma-separated CORS origins into a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS_RAW.split(",") if origin.strip()]

    # ── Knowledge Base ────────────────────────────────────────────────
    QDRANT_COLLECTION_KNOWLEDGE: str = "eduvia_knowledge"
    QDRANT_COLLECTION_CURRICULUM: str = "eduvia_curriculum"
    RAG_TOP_K: int = 3
    RAG_SCORE_THRESHOLD: float = 0.5

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Ensure the database URL is not the placeholder value."""
        if not v or v.strip() == "":
            raise ValueError("DATABASE_URL must be set")
        return v

    @field_validator("GEMINI_API_KEY")
    @classmethod
    def validate_gemini_key(cls, v: str) -> str:
        """Warn if Gemini API key looks like a placeholder."""
        if v.startswith("CHANGE_ME"):
            import warnings
            warnings.warn(
                "GEMINI_API_KEY appears to be a placeholder. AI features will not work.",
                stacklevel=2,
            )
        return v

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == "development"


@lru_cache
def get_settings() -> Settings:
    """
    Return cached application settings.

    Uses lru_cache so the .env file is only parsed once.
    In tests, call get_settings.cache_clear() to reset.
    """
    return Settings()


# Convenience singleton for import
settings = get_settings()
