"""GPT / Grok / Venice HTTP clients. Keys from env, never files in git.

Ollama is the unpaid local base (see azai.ollama). Tests inject hooks
so urllib is never called. Timeouts, no retry storms.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any, Callable

from azai.config import (
    GPT_MODEL,
    GPT_URL,
    GROK_MODEL,
    GROK_URL,
    PROVIDER_TIMEOUT,
    VENICE_MODEL,
    VENICE_URL,
    VENICE_URL_ALT,
)
from azai.ollama import call_chat as ollama_chat
from azai.ollama import ollama_model
from azai.ollama import status as ollama_status

Hook = Callable[[str, list[dict[str, str]], str], str]

# Tests assign callables here. Production stays empty.
TEST_HOOKS: dict[str, Hook] = {}


def clear_test_hooks() -> None:
    TEST_HOOKS.clear()


def _env_first(*names: str) -> str | None:
    for name in names:
        val = os.environ.get(name)
        if val:
            return val
    return None


def provider_status() -> dict[str, dict[str, Any]]:
    """Which keys are present — never the key values."""
    return {
        "gpt": {
            "present": bool(_env_first("OPENAI_API_KEY")),
            "env": "OPENAI_API_KEY",
            "url": GPT_URL,
            "model": os.environ.get("AZAI_GPT_MODEL") or GPT_MODEL,
        },
        "grok": {
            "present": bool(_env_first("XAI_API_KEY", "GROK_API_KEY")),
            "env": "XAI_API_KEY / GROK_API_KEY",
            "url": GROK_URL,
            "model": os.environ.get("AZAI_GROK_MODEL") or GROK_MODEL,
        },
        "venice": {
            "present": bool(_env_first("VENICE_API_KEY")),
            "env": "VENICE_API_KEY",
            "url": os.environ.get("AZAI_VENICE_URL") or VENICE_URL,
            "url_alt": VENICE_URL_ALT,
            "model": os.environ.get("AZAI_VENICE_MODEL") or VENICE_MODEL,
        },
        "local": {
            "present": True,
            "env": "AZAI_OLLAMA_URL / AZAI_OLLAMA_MODEL",
            "url": "JEEVES on Ollama base (constitution stub if Ollama is down)",
            "model": "local",
            "role": "JEEVES ethics/assistant layer",
        },
        "ollama": ollama_status(),
    }


def _post_json(url: str, headers: dict[str, str], body: dict[str, Any], timeout: float) -> dict[str, Any]:
    raw = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=raw, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:500]
        raise RuntimeError(f"provider HTTP {exc.code}: {detail}") from exc
    except Exception as exc:
        raise RuntimeError(f"provider error: {exc}") from exc


def _content_from_openai(payload: dict[str, Any]) -> str:
    choices = payload.get("choices") or []
    if not choices:
        return ""
    msg = choices[0].get("message") or {}
    return str(msg.get("content") or "")


def call_openai_compat(
    name: str,
    url: str,
    key: str,
    model: str,
    messages: list[dict[str, str]],
    timeout: float = PROVIDER_TIMEOUT,
) -> str:
    hook = TEST_HOOKS.get(name)
    if hook is not None:
        return hook(name, messages, model)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}",
    }
    body = {"model": model, "messages": messages}
    payload = _post_json(url, headers, body, timeout)
    return _content_from_openai(payload)


def call_named(name: str, messages: list[dict[str, str]]) -> str:
    """Call one provider. Raises RuntimeError on missing key or HTTP failure."""
    hook = TEST_HOOKS.get(name)
    if hook is not None:
        model = {
            "gpt": os.environ.get("AZAI_GPT_MODEL") or GPT_MODEL,
            "grok": os.environ.get("AZAI_GROK_MODEL") or GROK_MODEL,
            "venice": os.environ.get("AZAI_VENICE_MODEL") or VENICE_MODEL,
            "ollama": ollama_model(),
        }.get(name, name)
        return hook(name, messages, model)
    if name == "ollama":
        return ollama_chat(messages)
    if name == "gpt":
        key = _env_first("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("unavailable — OPENAI_API_KEY not set")
        model = os.environ.get("AZAI_GPT_MODEL") or GPT_MODEL
        return call_openai_compat("gpt", GPT_URL, key, model, messages)
    if name == "grok":
        key = _env_first("XAI_API_KEY", "GROK_API_KEY")
        if not key:
            raise RuntimeError("unavailable — XAI_API_KEY / GROK_API_KEY not set")
        model = os.environ.get("AZAI_GROK_MODEL") or GROK_MODEL
        return call_openai_compat("grok", GROK_URL, key, model, messages)
    if name == "venice":
        key = _env_first("VENICE_API_KEY")
        if not key:
            raise RuntimeError("unavailable — VENICE_API_KEY not set")
        model = os.environ.get("AZAI_VENICE_MODEL") or VENICE_MODEL
        url = os.environ.get("AZAI_VENICE_URL") or VENICE_URL
        try:
            return call_openai_compat("venice", url, key, model, messages)
        except RuntimeError:
            if url == VENICE_URL:
                # one honest fallback, not a retry storm
                return call_openai_compat("venice", VENICE_URL_ALT, key, model, messages)
            raise
    raise RuntimeError(f"unknown provider {name}")


def try_named(name: str, messages: list[dict[str, str]]) -> tuple[str, bool]:
    """Return (text, ok). Never raises. Missing keys become labeled unavailability."""
    try:
        return call_named(name, messages), True
    except RuntimeError as exc:
        return f"({exc})", False
