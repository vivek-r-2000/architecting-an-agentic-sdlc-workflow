"""Robust Gemini LLM Client with IPv4 routing, budget tracking, and mock fallback."""

import json
import logging
import os
import socket
import urllib.request
import urllib.error
from typing import Optional, Dict, Any

from .config import (
    GEMINI_API_KEY,
    DEFAULT_FAST_MODEL,
    DEFAULT_REASONING_MODEL,
    MAX_TOKEN_BUDGET,
    MOCK_LLM_MODE,
)

logger = logging.getLogger("autose.llm_client")

# Force IPv4 resolution to prevent Windows dual-stack socket connect timeouts
_real_getaddrinfo = socket.getaddrinfo

def _ipv4_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    return _real_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)

socket.getaddrinfo = _ipv4_getaddrinfo


class TokenBudgetTracker:
    def __init__(self, max_tokens: int = MAX_TOKEN_BUDGET):
        self.max_tokens = max_tokens
        self.total_tokens_used = 0
        self.calls_count = 0

    def record_usage(self, prompt_tokens: int, candidate_tokens: int):
        self.total_tokens_used += (prompt_tokens + candidate_tokens)
        self.calls_count += 1
        if self.total_tokens_used > self.max_tokens:
            raise RuntimeError(
                f"Token budget exhausted! Used {self.total_tokens_used} tokens > {self.max_tokens} limit."
            )

global_tracker = TokenBudgetTracker()


def generate(
    prompt: str,
    system_instruction: str = "",
    model: str = DEFAULT_FAST_MODEL,
    temperature: float = 0.2,
    api_key: Optional[str] = None,
    mock_response: Optional[str] = None
) -> str:
    """Generate content using Gemini API with timeout, IPv4 binding, and budget tracking."""
    if MOCK_LLM_MODE or mock_response:
        global_tracker.record_usage(len(prompt.split()), 100)
        return mock_response or "MOCK_LLM_OUTPUT"

    key = api_key or GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")
    if not key:
        logger.warning("No GEMINI_API_KEY provided; falling back to heuristic mock response.")
        return mock_response or f"Generated response for {prompt[:60]}..."

    # Sanitize model name
    clean_model = model.replace("models/", "")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{clean_model}:generateContent?key={key}"

    contents = []
    if system_instruction:
        contents.append({"role": "user", "parts": [{"text": f"System Directive: {system_instruction}"}]})
        contents.append({"role": "model", "parts": [{"text": "Understood. I will strictly follow this directive."}]})
    contents.append({"role": "user", "parts": [{"text": prompt}]})

    payload = {
        "contents": contents,
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": 4096,
        }
    }

    req_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=req_data,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            candidates = data.get("candidates", [])
            if not candidates:
                raise RuntimeError("No candidates returned from Gemini API")
            parts = candidates[0].get("content", {}).get("parts", [])
            text = "".join(part.get("text", "") for part in parts)
            
            usage = data.get("usageMetadata", {})
            p_tokens = usage.get("promptTokenCount", len(prompt.split()))
            c_tokens = usage.get("candidatesTokenCount", len(text.split()))
            global_tracker.record_usage(p_tokens, c_tokens)
            return text
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        logger.error(f"Gemini API HTTP {e.code}: {err_body}")
        raise RuntimeError(f"Gemini API HTTP {e.code}: {err_body}") from e
    except Exception as e:
        logger.error(f"Gemini request failed: {e}")
        raise
