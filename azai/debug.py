"""AZAI_DEBUG=1 — local stderr traces. Never logs secrets. No telemetry."""

from __future__ import annotations

import os
import sys
from typing import Any

from azai.config import WORKER_KEY_MARKERS

_SECRET_ENV = (
    "OPENAI_API_KEY",
    "XAI_API_KEY",
    "GROK_API_KEY",
    "VENICE_API_KEY",
)


def enabled() -> bool:
    return os.environ.get("AZAI_DEBUG", "") == "1"


def redact(text: str) -> str:
    """Strip values that look like keys. Never emit secrets to stderr."""
    out = text or ""
    for marker in WORKER_KEY_MARKERS:
        if marker.strip() and marker in out:
            out = out.replace(marker, "[redacted]")
    for name in _SECRET_ENV:
        val = os.environ.get(name) or ""
        if val and val in out:
            out = out.replace(val, f"[{name}=present]")
    return out


def dlog(msg: str, **fields: Any) -> None:
    if not enabled():
        return
    extra = ""
    if fields:
        parts = []
        for k, v in fields.items():
            if k.lower() in {"key", "token", "authorization", "secret"}:
                parts.append(f"{k}=[redacted]")
            else:
                parts.append(f"{k}={redact(str(v))}")
        extra = " " + " ".join(parts)
    sys.stderr.write(f"[azai debug] {redact(str(msg))}{extra}\n")
    sys.stderr.flush()


def status_payload() -> dict[str, Any]:
    return {
        "debug": enabled(),
        "note": "AZAI_DEBUG=1 prints local stderr traces. No telemetry. Keys are never logged.",
    }
