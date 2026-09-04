"""JEEVES — ethics/assistant layer inside AZAI. Not sovereign.

JEEVES wraps the local Ollama base (and optional paid providers) with
the constitution. The operator and the Lamb Lens govern JEEVES.
JEEVES is not a foundation model and does not pretend to be GPT.
"""

from __future__ import annotations

from typing import Any

from azai.config import MOTTO, OLLAMA_INSTALL_STEPS
from azai.ollama import call_chat as ollama_chat
from azai.ollama import probe as ollama_probe

OATH = "Truth belongs to the Source; understanding belongs to service."
ROLE = "ethics/assistant layer"
SOVEREIGN = False

SYSTEM = (
    "You are JEEVES, the ethics and assistant instrument inside AZAI. "
    "You are not sovereign. The operator and the Lamb Lens govern you. "
    "AZAI is a true local AI package on an Ollama base; you speak through that local model. "
    "You are not GPT, not Grok, not Venice, and not a new foundation model. "
    "Hierarchy: Lamb Lens (Peace → Clarity → Service) → Formal Rules → "
    "Integrity Gate → Jeeves Reasoning → Output. "
    "If a request would break peace, clarity, or service, refuse and explain the gate. "
    f"Oath: {OATH}"
)


def system_message() -> dict[str, str]:
    return {"role": "system", "content": SYSTEM}


def wrap_messages(messages: list[dict[str, str]] | None) -> list[dict[str, str]]:
    """Prepend the JEEVES constitution unless a JEEVES system turn is already first."""
    rows = [dict(m) for m in (messages or [])]
    if rows and rows[0].get("role") == "system" and "JEEVES" in str(rows[0].get("content") or ""):
        return rows
    return [system_message(), *rows]


def constitution_stub(prompt: str, lamb: dict[str, Any], *, reason: str = "") -> str:
    """Honest local answer when Ollama is not running. Never claims to be GPT."""
    overall = lamb.get("overall", "PASS")
    extra = f"\n\n({reason})\n" if reason else "\n\n"
    return (
        "[local / Jeeves]\n"
        "I am JEEVES, the ethics/assistant layer inside AZAI — not GPT, not Grok, "
        "not Venice, and not sovereign. The operator and the Lamb Lens govern me.\n"
        f"Lamb Lens: peace={lamb.get('peace')} clarity={lamb.get('clarity')} "
        f"service={lamb.get('service')} → {overall}\n"
        f"Oath: {OATH}\n"
        f"{extra}"
        "AZAI is a true local AI stack on an Ollama base. Ollama is not reachable "
        "on this machine yet, so I am the constitution stub (Lamb Lens + receipts). "
        "I do not invent a foundation model and I do not spend hosted paid keys.\n\n"
        "Exact Ollama steps:\n"
        f"{OLLAMA_INSTALL_STEPS}\n\n"
        f"You said: {prompt.strip()[:2000]}\n\n"
        f"{MOTTO}"
    )


def local_reply(prompt: str, lamb: dict[str, Any], messages: list[dict[str, str]] | None = None) -> str:
    """Speak through Ollama when the local base is up; otherwise the constitution stub."""
    info = ollama_probe()
    if not info.get("reachable"):
        return constitution_stub(prompt, lamb, reason="Ollama base not reachable")
    rows = wrap_messages(messages or [{"role": "user", "content": prompt}])
    try:
        text = ollama_chat(rows).strip()
    except RuntimeError as exc:
        return constitution_stub(prompt, lamb, reason=str(exc)[:400])
    if not text:
        return constitution_stub(prompt, lamb, reason="Ollama returned empty text")
    return (
        "[local / Jeeves]\n"
        f"{text}\n\n"
        "— JEEVES (ethics/assistant layer; not sovereign; not GPT; "
        "not a foundation model; Ollama base; Lamb Lens above)"
    )
