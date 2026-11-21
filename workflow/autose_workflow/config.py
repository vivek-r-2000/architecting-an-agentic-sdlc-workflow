"""Configuration settings for AutoSE Workflow Engine."""

import os
from pathlib import Path

# Paths
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
AUTOSE_DIR = WORKSPACE_ROOT / ".autose"
ARCHITECTURE_FILE = WORKSPACE_ROOT / "ARCHITECTURE.md"

# LLM Models
DEFAULT_FAST_MODEL = "gemini-3.5-flash-lite"
DEFAULT_REASONING_MODEL = "gemini-3.5-flash"
DEFAULT_REVIEWER_MODEL = "gemini-3.5-flash"

# Resource & Budget Limits
MAX_TEST_RETRIES = 3
MAX_REVIEW_ROUNDS = 2
MAX_TOKEN_BUDGET = 200_000
STAGE_TIMEOUT_SECONDS = 180

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MOCK_LLM_MODE = os.getenv("AUTOSE_MOCK_LLM", "false").lower() in ("true", "1", "yes")
