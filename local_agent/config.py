"""
Configuration for SAISA - Super AI Self-Autonomous Agent.
Loads settings from environment variables and .env file.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_WORKSPACE = PROJECT_ROOT / "workspace"

WORKSPACE_ROOT = Path(
    os.environ.get("WORKSPACE_ROOT", str(_DEFAULT_WORKSPACE))
).resolve()


def _bool_env(name: str, default: bool, truthy: tuple = ("1", "true", "yes", "on")) -> bool:
    """Parse boolean from environment variable."""
    return os.environ.get(name, str(default)).strip().lower() in truthy


def _int_env(name: str, default: int, min_val: int | None = None, max_val: int | None = None) -> int:
    """Parse integer from environment variable."""
    raw = os.environ.get(name, str(default)).strip()
    try:
        value = int(raw)
        if min_val is not None:
            value = max(min_val, value)
        if max_val is not None:
            value = min(max_val, value)
        return value
    except ValueError:
        return default


def _float_env(name: str, default: float, min_val: float = 0.0, max_val: float = 2.0) -> float:
    """Parse float from environment variable."""
    raw = os.environ.get(name)
    if raw is None or not str(raw).strip():
        return default
    try:
        value = float(str(raw).strip())
        return max(min_val, min(max_val, value))
    except ValueError:
        return default


# Backend Configuration
AGENT_BACKEND = os.environ.get("AGENT_BACKEND", "ollama").strip().lower()
AGENT_PERFORMANCE_MODE = _bool_env("AGENT_PERFORMANCE_MODE", False)


# Groq Configuration
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "").strip()
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile").strip()
GROQ_BASE_URL = os.environ.get("GROQ_BASE_URL", "https://api.groq.com/openai/v1").strip()
GROQ_REQUEST_TIMEOUT_SEC = float(
    os.environ.get("GROQ_REQUEST_TIMEOUT_SEC", "120").strip() or "120"
)
GROQ_TEMPERATURE = _float_env("GROQ_TEMPERATURE", 0.65)
GROQ_MAX_HISTORY_MESSAGES = max(4, _int_env("GROQ_MAX_HISTORY_MESSAGES", 48))
GROQ_RATE_LIMIT_MAX_RETRIES = max(0, min(20, _int_env("GROQ_RATE_LIMIT_MAX_RETRIES", 8)))
GROQ_MAX_COMPLETION_TOKENS = max(0, min(131_072, _int_env("GROQ_MAX_COMPLETION_TOKENS", 0)))


# Ollama Configuration
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434").strip()
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2").strip()
OLLAMA_CRITIC_MODEL = os.environ.get("OLLAMA_CRITIC_MODEL", "llama3.2").strip()
OLLAMA_TEMPERATURE = _float_env("OLLAMA_TEMPERATURE", 0.7)
OLLAMA_REQUEST_TIMEOUT_SEC = float(
    os.environ.get("OLLAMA_REQUEST_TIMEOUT_SEC", "600").strip() or "600"
)
OLLAMA_NUM_CTX = _int_env("OLLAMA_NUM_CTX", 0)
OLLAMA_MAX_HISTORY_MESSAGES = max(4, _int_env("OLLAMA_MAX_HISTORY_MESSAGES", 48))


# Agent Behavior
AGENT_MAX_TOOL_ROUNDS = max(4, min(32, _int_env("AGENT_MAX_TOOL_ROUNDS", 16)))
SELF_EVAL_ENABLED = _bool_env("SELF_EVAL", True)
SELF_EVAL_MIN_SCORE = max(1, min(10, _int_env("SELF_EVAL_MIN_SCORE", 7)))
AGENT_NAME = os.environ.get("AGENT_NAME", "SAISA").strip()
AGENT_OWNER_NAME = os.environ.get("AGENT_OWNER_NAME", "").strip()
AGENT_OWNER_ONLINE_HINT = os.environ.get("AGENT_OWNER_ONLINE_HINT", "").strip()


# Feature Flags
ALLOW_POWERSHELL = _bool_env("ALLOW_POWERSHELL", False)
ALLOW_FETCH_URL = _bool_env("ALLOW_FETCH_URL", False)
ALLOW_SMTP_SEND = _bool_env("ALLOW_SMTP_SEND", False)
ALLOW_OPEN_BROWSER = _bool_env("ALLOW_OPEN_BROWSER", False)
ALLOW_GIT = _bool_env("ALLOW_GIT", True)
ALLOW_DOCKER = _bool_env("ALLOW_DOCKER", False)
ALLOW_SYSTEM_MONITOR = _bool_env("ALLOW_SYSTEM_MONITOR", True)
ALLOW_SCHEDULER = _bool_env("ALLOW_SCHEDULER", False)


# Web Search
WEB_SEARCH_CACHE_TTL_SEC = _int_env(
    "WEB_SEARCH_CACHE_TTL_SEC",
    120 if AGENT_PERFORMANCE_MODE else 0,
)
WEB_SEARCH_CACHE_MAX_ENTRIES = max(8, _int_env("WEB_SEARCH_CACHE_MAX_ENTRIES", 96))


# SMTP / Email
SMTP_HOST = os.environ.get("SMTP_HOST", "").strip()
SMTP_PORT = _int_env("SMTP_PORT", 587)
SMTP_USER = os.environ.get("SMTP_USER", "").strip()
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "").strip()
SMTP_FROM = os.environ.get("SMTP_FROM", "").strip()
SMTP_USE_TLS = _bool_env("SMTP_USE_TLS", True)
MAX_EMAIL_BODY_CHARS = _int_env("MAX_EMAIL_BODY_CHARS", 200_000)


# URL Fetching
MAX_FETCH_URL_BYTES = _int_env("MAX_FETCH_URL_BYTES", 500_000)
FETCH_URL_TIMEOUT_SEC = float(
    os.environ.get("FETCH_URL_TIMEOUT_SEC", "25").strip() or "25"
)


# Memory / Storage
LOCAL_MEMORY_JOURNAL = os.environ.get(
    "LOCAL_MEMORY_JOURNAL", "memory/journal.md"
).strip().replace("\\", "/")
MAX_MEMORY_JOURNAL_BYTES = _int_env("MAX_MEMORY_JOURNAL_BYTES", 5_000_000)
MAX_MEMORY_READ_CHARS = _int_env("MAX_MEMORY_READ_CHARS", 220_000)
MAX_READ_BYTES = _int_env("MAX_READ_BYTES", 450_000)
MAX_SHELL_OUTPUT = _int_env("MAX_SHELL_OUTPUT", 28_000)
SHELL_TIMEOUT_SEC = 120


# Autonomous Mode
AUTONOMOUS_MODE = _bool_env("AUTONOMOUS_MODE", False)
AUTONOMOUS_MAX_TURNS = max(10, _int_env("AUTONOMOUS_MAX_TURNS", 100))


# Learning Mode
LEARNING_MODE = _bool_env("LEARNING_MODE", True)
LEARNING_MEMORY_FILE = os.environ.get(
    "LEARNING_MEMORY_FILE", "memory/learned.json"
).strip()
