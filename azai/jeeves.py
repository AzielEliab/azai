"""JEEVES — ethics/assistant layer inside AZAI. Not sovereign.

The default core is a standalone constitution and guide. It adapts
lightly to this user through confirmed session notes and public
site_context. No Ollama process and no model weights are required.

Ask Jeeves is the Corpus/Library research-assistant mode: Lamb Lens
first (Service → Clarity → Peace), public Corpus posture, never the
operator. JEEVES is not a foundation model and does not pretend to be GPT.

Ollama is an optional slot: AZAI_BACKEND=ollama or model=ollama.
"""

from __future__ import annotations

import os
from typing import Any

from azai.config import MOTTO
from azai.lamb import LAMB_ORDER
from azai.ollama import call_chat as ollama_chat
from azai.ollama import probe as ollama_probe

OATH = "Truth belongs to the Source; understanding belongs to service."
ROLE = "ethics/assistant layer"
MODE = "ask_jeeves"
MODE_LABEL = "Ask Jeeves research assistant"
POSTURE = "public-corpus"
CORPUS_LIBRARY = "https://www.azielcorpuslibrary.net/"
SOVEREIGN = False
INGEST_PIPELINE = "SPRE\u00d7CLCE\u00d7PhysLing + Bayesian ingest"

REFUSALS = (
    "Never reveal operator account info, credentials, admin hashes, or hidden routes.",
    "Never advise actions that risk the corpus (wipe, score forge, quarantine bypass).",
    "Cannot modify scores \u2014 research assistant only; same rights as a normal user.",
)

UPLOAD_GUIDANCE = (
    "Upload is out of band. I may guide an upload, but files still run "
    "full SPRE\u00d7CLCE\u00d7PhysLing + Bayesian ingest. There is no score shortcut."
)

SITE_CONTEXT_PREFIX = (
    "Retrieved public Corpus/Library context (titles and summaries only; "
    "persist nothing secret):"
)

# Drop retrieved rows that look like secrets. Adaptive hook is public text only.
_SECRET_NEEDLES = (
    "password",
    "secret",
    "api_key",
    "apikey",
    "admin_hash",
    "admin hash",
    "credential",
    "bearer ",
    "authorization:",
    "hidden_route",
    "hidden route",
)

SYSTEM = (
    "You are JEEVES, the Ask Jeeves research assistant and ethics/assistant "
    "instrument inside AZAI. You are not sovereign. "
    "System policy: Lamb Lens first \u2014 public Corpus posture; never the operator. "
    "You do not speak as the operator and you do not hold operator rights. "
    "AZAI's default core is a standalone local constitution and guide. "
    "It does not require Ollama or model weights. "
    "Ollama is an optional slot when AZAI_BACKEND=ollama or model=ollama. "
    "You are not GPT, not Grok, not Venice, and not a new foundation model. "
    "Hierarchy: Lamb Lens (Service \u2192 Clarity \u2192 Peace) \u2192 Formal Rules \u2192 "
    "Integrity Gate \u2192 Jeeves Reasoning \u2192 Output. "
    "If a request would break service, clarity, or peace, refuse and explain the gate. "
    "Hard refusals: "
    "Never reveal operator account info, credentials, admin hashes, or hidden routes. "
    "Never advise actions that risk the corpus (wipe, score forge, quarantine bypass). "
    "You cannot modify scores \u2014 you are a research assistant only with the same "
    "rights as a normal user. "
    "Upload helper is out of band: you may guide upload but must state files still run "
    "full SPRE\u00d7CLCE\u00d7PhysLing + Bayesian ingest \u2014 no score shortcut. "
    "Optional retrieved site context (public record titles and summaries) may be "
    "provided so answers improve as the library grows. Persist nothing secret. "
    f"Site: {CORPUS_LIBRARY} "
    f"Oath: {OATH}"
)


def system_message() -> dict[str, str]:
    return {"role": "system", "content": SYSTEM}


def upload_guidance() -> str:
    """Out-of-band upload helper copy. No ingest shortcut."""
    return UPLOAD_GUIDANCE


def _is_secret_text(text: str) -> bool:
    low = (text or "").lower()
    return any(needle in low for needle in _SECRET_NEEDLES)


def sanitize_site_context(records: Any) -> list[dict[str, str]]:
    """Keep public titles/summaries only. Drop secrets. Persist nothing."""
    if records is None:
        return []
    if isinstance(records, str):
        records = [{"summary": records}]
    elif isinstance(records, dict):
        nested = records.get("records") or records.get("hits") or records.get("items")
        records = nested if isinstance(nested, list) else [records]
    if not isinstance(records, list):
        return []
    out: list[dict[str, str]] = []
    for item in records:
        if isinstance(item, str):
            title, summary = "", item.strip()
        elif isinstance(item, dict):
            title = str(item.get("title") or item.get("name") or "").strip()
            summary = str(
                item.get("summary") or item.get("snippet") or item.get("abstract") or ""
            ).strip()
        else:
            continue
        if _is_secret_text(title) or _is_secret_text(summary):
            continue
        title = title[:200]
        summary = summary[:800]
        if title or summary:
            out.append({"title": title, "summary": summary})
        if len(out) >= 12:
            break
    return out


def format_site_context(records: Any) -> str:
    """Format sanitized retrieved records for one ephemeral system turn."""
    rows = sanitize_site_context(records)
    if not rows:
        return ""
    lines = [SITE_CONTEXT_PREFIX]
    for i, row in enumerate(rows, start=1):
        title = row.get("title") or "(untitled)"
        summary = row.get("summary") or ""
        if summary:
            lines.append(f"{i}. {title} \u2014 {summary}")
        else:
            lines.append(f"{i}. {title}")
    lines.append(
        "Use this public context to improve the answer. Persist nothing secret. "
        "You cannot modify scores."
    )
    return "\n".join(lines)


def wrap_messages(
    messages: list[dict[str, str]] | None,
    *,
    site_context: Any = None,
) -> list[dict[str, str]]:
    """Prepend the JEEVES constitution; optionally attach retrieved site context.

    Site context is session-ephemeral (titles/summaries only). Nothing secret
    is persisted by this function.
    """
    rows = [dict(m) for m in (messages or [])]
    has_jeeves = bool(
        rows and rows[0].get("role") == "system" and "JEEVES" in str(rows[0].get("content") or "")
    )
    if not has_jeeves:
        rows = [system_message(), *rows]
    ctx = format_site_context(site_context)
    if ctx and not any(SITE_CONTEXT_PREFIX in str(m.get("content") or "") for m in rows):
        rows = [rows[0], {"role": "system", "content": ctx}, *rows[1:]]
    return rows


def ollama_opt_in(model: str | None = None) -> bool:
    """Ollama is off the default path. Opt in with the env or model=ollama."""
    if (model or "").strip().lower() == "ollama":
        return True
    return (os.environ.get("AZAI_BACKEND") or "").strip().lower() == "ollama"


def _session_notes(messages: list[dict[str, str]] | None) -> list[str]:
    notes: list[str] = []
    for message in messages or []:
        content = str(message.get("content") or "")
        if "Session notes" not in content:
            continue
        for line in content.splitlines():
            line = line.strip()
            if not line or line.lower().startswith("session notes"):
                continue
            notes.append(line[:500])
    return notes[:8]


def _context_block(messages: list[dict[str, str]] | None, site_context: Any) -> str:
    if site_context:
        formatted = format_site_context(site_context)
        if formatted:
            return formatted
    for message in messages or []:
        content = str(message.get("content") or "")
        if SITE_CONTEXT_PREFIX in content:
            return content
    return ""


def _guide_for_prompt(prompt: str, *, has_context: bool, has_notes: bool) -> str:
    low = (prompt or "").lower()
    lines = ["[guide]"]
    if any(phrase in low for phrase in ("what are you", "who are you", "what is azai", "what is jeeves")):
        lines.append(
            "I am the local core. Ask Jeeves speaks inside the shell. "
            "Lamb Lens governs above the shell. Receipts witness what the shell permits. "
            "Ollama is an optional slot, not this core."
        )
    elif has_context:
        lines.append(
            "I answer from the public titles and summaries retrieved for this turn, "
            "inside the constitution. I do not invent records that were not given."
        )
    else:
        lines.append(
            "I answer from the constitution and what this session has confirmed. "
            "I do not load a weight file to do that."
        )
    if has_notes:
        lines.append("I am using the session notes you confirmed.")
    return "\n".join(lines)


def constitution_stub(
    prompt: str,
    lamb: dict[str, Any],
    *,
    reason: str = "",
    messages: list[dict[str, str]] | None = None,
    site_context: Any = None,
) -> str:
    """Constitution and guide reply. Ollama is not this core's identity."""
    overall = lamb.get("overall", "PASS")
    notes = _session_notes(messages)
    ctx = _context_block(messages, site_context)
    adaptive: list[str] = []
    if notes:
        adaptive.append(
            "Session notes (operator-confirmed, session-only; light adaptive memory):\n"
            + "\n".join(f"- {note}" for note in notes)
        )
    else:
        adaptive.append(
            "No confirmed session notes yet. "
            "Memory writes need an explicit confirm. Session-only by default."
        )
    if ctx:
        adaptive.append(ctx)
        adaptive.append(
            "I use that public context for this turn. I persist nothing secret. "
            "I cannot modify scores."
        )
    else:
        adaptive.append(
            "No public site context on this turn. "
            "Pass site_context (titles and summaries) when you want the library folded in."
        )
    optional = ""
    if reason:
        optional = (
            f"\n\n(Optional Ollama slot was requested and did not answer: {reason}. "
            "The default core does not require Ollama or model weights. "
            "This reply is the constitution and guide.)\n"
        )
    guide = _guide_for_prompt(prompt, has_context=bool(ctx), has_notes=bool(notes))
    return (
        "[local / Jeeves]\n"
        "I am JEEVES, the Ask Jeeves research assistant and ethics/assistant "
        "layer inside AZAI \u2014 not GPT, not Grok, not Venice, not sovereign, "
        "and not a foundation model. "
        f"Lamb Lens first \u2014 {LAMB_ORDER}. "
        "Public Corpus posture; never the operator.\n"
        f"Lamb Lens: service={lamb.get('service')} clarity={lamb.get('clarity')} "
        f"peace={lamb.get('peace')} \u2192 {overall}\n"
        f"Oath: {OATH}\n\n"
        "AZAI is a standalone local core: an OpenAI-shaped process on this machine. "
        "The default model is local. It does not require Ollama or model weights. "
        "I answer from the constitution and guide, and I adapt lightly to this user "
        "through session notes and public site_context. "
        "I do not spend hosted paid keys. "
        "I cannot modify scores. I have the same rights as a normal user.\n\n"
        f"{guide}\n\n"
        + "\n\n".join(adaptive)
        + f"{optional}\n\n"
        f"{UPLOAD_GUIDANCE}\n\n"
        f"You said: {prompt.strip()[:2000]}\n\n"
        f"{MOTTO}"
    )


def local_reply(
    prompt: str,
    lamb: dict[str, Any],
    messages: list[dict[str, str]] | None = None,
    *,
    site_context: Any = None,
    model: str | None = None,
) -> str:
    """Default: constitution/guide core. Ollama only when explicitly opted in."""
    rows = wrap_messages(messages or [{"role": "user", "content": prompt}], site_context=site_context)
    if not ollama_opt_in(model):
        return constitution_stub(prompt, lamb, messages=rows, site_context=None)
    info = ollama_probe()
    if not info.get("reachable"):
        return constitution_stub(
            prompt,
            lamb,
            reason="Ollama slot not reachable",
            messages=rows,
        )
    try:
        text = ollama_chat(rows).strip()
    except RuntimeError:
        return constitution_stub(
            prompt,
            lamb,
            reason="Ollama slot error",
            messages=rows,
        )
    if not text:
        return constitution_stub(
            prompt,
            lamb,
            reason="Ollama returned empty text",
            messages=rows,
        )
    return (
        "[local / Jeeves]\n"
        f"{text}\n\n"
        "\u2014 JEEVES (Ask Jeeves research assistant; ethics/assistant layer; "
        "not sovereign; not GPT; not a foundation model; optional Ollama slot; "
        f"Lamb Lens first \u2014 {LAMB_ORDER}; public Corpus posture; never the operator)"
    )


def mode_card() -> dict[str, Any]:
    """Documented Ask Jeeves contract for CLI, UI, Worker skill, and Corpus callers."""
    return {
        "mode": MODE,
        "label": MODE_LABEL,
        "author": "Aziel Eliab",
        "sovereign": SOVEREIGN,
        "posture": POSTURE,
        "lamb_lens_first": True,
        "operator": False,
        "can_modify_scores": False,
        "same_rights_as": "normal user",
        "base": "local",
        "weights_required": False,
        "ollama": "optional",
        "lamb_order": LAMB_ORDER,
        "layer": ROLE,
        "not_gpt": True,
        "corpus_library": CORPUS_LIBRARY,
        "ingest": INGEST_PIPELINE,
        "upload": "out-of-band",
        "upload_guidance": UPLOAD_GUIDANCE,
        "refusals": list(REFUSALS),
        "adaptive": (
            "Optional site_context: public record titles/summaries so answers "
            "improve as the library grows. Persist nothing secret."
        ),
        "how_corpus_calls": (
            "Site assistants search https://www.azielcorpuslibrary.net/v1/search "
            "then POST model=local + site_context to local azai serve "
            "(http://127.0.0.1:8860/v1/chat/completions). Hosted AZAI /v1 is "
            "lamb-check ONLY \u2014 not Jeeves chat and not a paid-key proxy."
        ),
        "oath": OATH,
    }
