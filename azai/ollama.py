"""Ollama — true local AI base for AZAI.

Loopback by default (127.0.0.1:11434). No paid keys. Not a hosted proxy.
Tests inject TEST_HOOKS so urllib is never called.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any, Callable

from azai.config import (
    OLLAMA_CHAT_PATH,
    OLLAMA_CHAT_TIMEOUT,
    OLLAMA_INSTALL_STEPS,
    OLLAMA_MODEL,
    OLLAMA_PROBE_TIMEOUT,
    OLLAMA_TAGS_PATH,
    OLLAMA_URL,
)

Hook = Callable[[str, list[dict[str, str]], str], str]
ProbeHook = Callable[[], dict[str, Any]]

TEST_HOOKS: dict[str, Hook] = {}
TEST_PROBE: ProbeHook | None = None


def clear_test_hooks() -> None:
    TEST_HOOKS.clear()
    global TEST_PROBE
    TEST_PROBE = None


def ollama_url() -> str:
    return (os.environ.get("AZAI_OLLAMA_URL") or OLLAMA_URL).rstrip("/")


def ollama_model() -> str:
    return os.environ.get("AZAI_OLLAMA_MODEL") or OLLAMA_MODEL


def install_steps() -> str:
    return OLLAMA_INSTALL_STEPS


def _model_listed(names: list[str], wanted: str) -> bool:
    want = (wanted or "").lower().strip()
    if not want:
        return False
    for name in names:
        n = (name or "").lower()
        if n == want or n.startswith(want + ":") or want in n:
            return True
    return False


def probe() -> dict[str, Any]:
    """Local liveness. Never hits paid APIs. Short timeout."""
    if TEST_PROBE is not None:
        return TEST_PROBE()
    url = ollama_url()
    model = ollama_model()
    tags_url = url + OLLAMA_TAGS_PATH
    try:
        req = urllib.request.Request(tags_url, headers={"Accept": "application/json"}, method="GET")
        with urllib.request.urlopen(req, timeout=OLLAMA_PROBE_TIMEOUT) as resp:
            payload = json.loads(resp.read().decode("utf-8") or "{}")
        names = []
        for row in payload.get("models") or []:
            if isinstance(row, dict):
                names.append(str(row.get("name") or row.get("model") or ""))
        present = _model_listed(names, model)
        return {
            "ok": True,
            "reachable": True,
            "url": url,
            "model": model,
            "model_present": present,
            "models": [n for n in names if n],
            "steps": None if present else (
                f"Ollama is up at {url} but {model} is not pulled.\n"
                f"Run: ollama pull {model}\n" + OLLAMA_INSTALL_STEPS
            ),
        }
    except Exception as exc:
        return {
            "ok": False,
            "reachable": False,
            "url": url,
            "model": model,
            "model_present": False,
            "models": [],
            "error": str(exc)[:300],
            "steps": OLLAMA_INSTALL_STEPS,
        }


def status() -> dict[str, Any]:
    info = probe()
    return {
        "present": bool(info.get("reachable")),
        "model_present": bool(info.get("model_present")),
        "env": "AZAI_OLLAMA_URL / AZAI_OLLAMA_MODEL",
        "url": info.get("url") or ollama_url(),
        "model": info.get("model") or ollama_model(),
        "role": "local Ollama base",
        "paid_key": False,
    }


def call_chat(messages: list[dict[str, str]], model: str | None = None) -> str:
    """OpenAI-compatible chat against local Ollama. Raises RuntimeError on failure."""
    use_model = model or ollama_model()
    hook = TEST_HOOKS.get("ollama")
    if hook is not None:
        return hook("ollama", messages, use_model)
    url = ollama_url() + OLLAMA_CHAT_PATH
    headers = {"Content-Type": "application/json"}
    body = {"model": use_model, "messages": messages, "stream": False}
    raw = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=raw, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=OLLAMA_CHAT_TIMEOUT) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:500]
        raise RuntimeError(f"ollama HTTP {exc.code}: {detail}") from exc
    except Exception as exc:
        raise RuntimeError(
            f"ollama unavailable at {ollama_url()}: {exc}. {OLLAMA_INSTALL_STEPS}"
        ) from exc
    choices = payload.get("choices") or []
    if choices:
        msg = choices[0].get("message") or {}
        content = str(msg.get("content") or "")
        if content:
            return content
    # Some Ollama builds answer via /api/chat shape even on /v1
    if payload.get("message") and payload["message"].get("content"):
        return str(payload["message"]["content"])
    raise RuntimeError("ollama returned an empty completion")
