"""
Eduvia — Research Model Catalog & Canonical Configurations

Centralized catalog of AI models supported in Research Mode.
Used by backend validation, API route /models, and frontend model selectors.

Contains only active official Google Gemini API model IDs:
- Preferred current research models: gemini-3.8-flash (default), gemini-3.5-flash-lite
- Stable legacy options: gemini-2.5-flash, gemini-2.5-pro
All shut-down / experimental / obsolete IDs (gemini-2.0-flash-exp, gemini-1.5-pro) are excluded and rejected.
"""
from __future__ import annotations

from typing import Any

SUPPORTED_RESEARCH_MODELS: list[dict[str, Any]] = [
    {
        "id": "gemini-3.8-flash",
        "name": "Gemini 3.8 Flash",
        "description": "Primary high-performance research model for experimental content & assessment generation",
        "is_default": True,
    },
    {
        "id": "gemini-3.5-flash-lite",
        "name": "Gemini 3.5 Flash Lite",
        "description": "Lightweight, low-latency model for rapid high-throughput prototyping",
        "is_default": False,
    },
    {
        "id": "gemini-2.5-flash",
        "name": "Gemini 2.5 Flash",
        "description": "Stable legacy model for sandbox generation",
        "is_default": False,
    },
    {
        "id": "gemini-2.5-pro",
        "name": "Gemini 2.5 Pro",
        "description": "Stable legacy model for deep reasoning and complex curriculum design",
        "is_default": False,
    },
]

SUPPORTED_RESEARCH_MODEL_IDS: set[str] = {m["id"] for m in SUPPORTED_RESEARCH_MODELS}
DEFAULT_RESEARCH_MODEL_ID: str = "gemini-3.8-flash"
