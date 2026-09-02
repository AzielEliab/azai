"""Import / export conversations. JSON + Markdown + .txt.

Round-trippable. Does not call providers. Does not rewrite the receipt chain.
"""

from __future__ import annotations

import json
from typing import Any

from azai import __version__
from azai.config import LIMITATION
from azai.receipts import utc_now

ROLE_PREFIXES: tuple[tuple[str, str], ...] = (
    ("user:", "user"),
    ("operator:", "user"),
    ("you:", "user"),
    ("assistant:", "assistant"),
    ("jeeves:", "assistant"),
    ("azai:", "assistant"),
    ("system:", "system"),
)


def detect_format(filename: str, content: str) -> str:
    name = (filename or "").lower()
    if name.endswith(".json"):
        return "json"
    if name.endswith(".txt") or name.endswith(".md"):
        return "txt"
    stripped = (content or "").lstrip()
    if stripped.startswith("{") or stripped.startswith("["):
        return "json"
    return "txt"


def parse_txt(text: str) -> list[dict[str, str]]:
    """Parse a .txt conversation.

    Lines that start with ``user:`` / ``assistant:`` / ``jeeves:`` (etc.)
    become turns. A plain file with no prefixes becomes one user message
    (or one user message per blank-line paragraph).
    """
    raw = (text or "").replace("\r\n", "\n").replace("\r", "\n")
    if not raw.strip():
        return []
    lines = raw.split("\n")
    has_prefix = False
    for line in lines:
        low = line.lower().lstrip()
        if any(low.startswith(p) for p, _ in ROLE_PREFIXES):
            has_prefix = True
            break
    if not has_prefix:
        paras = [p.strip() for p in raw.strip().split("\n\n") if p.strip()]
        return [{"role": "user", "content": p} for p in paras]

    messages: list[dict[str, str]] = []
    role: str | None = None
    buf: list[str] = []

    def flush() -> None:
        nonlocal role, buf
        if role is None:
            buf = []
            return
        body = "\n".join(buf).strip()
        if body:
            messages.append({"role": role, "content": body})
        role = None
        buf = []

    for line in lines:
        low = line.lower().lstrip()
        matched = None
        for prefix, r in ROLE_PREFIXES:
            if low.startswith(prefix):
                stripped = line.lstrip()
                rest = stripped[len(prefix) :].lstrip()
                matched = (r, rest)
                break
        if matched:
            flush()
            role, rest = matched
            buf = [rest] if rest else []
        else:
            if role is None:
                role = "user"
            buf.append(line)
    flush()
    return messages


def parse_json(text: str) -> list[dict[str, str]]:
    """Parse AZAI export JSON, an OpenAI messages object, or a message array."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON: {exc}") from exc
    return messages_from_obj(data)


def messages_from_obj(data: Any) -> list[dict[str, str]]:
    if isinstance(data, list):
        rows = data
    elif isinstance(data, dict):
        rows = data.get("messages") or data.get("conversation") or data.get("turns") or []
        if isinstance(rows, dict):
            rows = list(rows.values())
    else:
        raise ValueError("JSON conversation must be an object or array")
    out: list[dict[str, str]] = []
    for item in rows:
        if not isinstance(item, dict):
            continue
        role = str(item.get("role") or "user")
        content = item.get("content")
        if content is None:
            continue
        if not isinstance(content, str):
            content = json.dumps(content, ensure_ascii=True)
        out.append({"role": role, "content": content})
    return out


def parse_conversation(content: str, filename: str = "") -> list[dict[str, str]]:
    kind = detect_format(filename, content)
    if kind == "json":
        return parse_json(content)
    return parse_txt(content)


def simple_text(content: str) -> str:
    """6th-grader view: hide [gpt]/[grok]/[venice] blocks; keep Jeeves + synthesis."""
    text = content or ""
    if "[synthesis]" not in text:
        return text
    synth = text.split("[synthesis]", 1)[1].strip()
    local = ""
    if "[local / Jeeves]" in text:
        local = text.split("[local / Jeeves]", 1)[1]
        local = local.split("[synthesis]", 1)[0].strip()
    if local:
        return f"{local}\n\n{synth}".strip()
    return synth


def bundle(
    messages: list[dict[str, Any]],
    receipts: list[dict[str, Any]] | None = None,
    verify: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "product": "azai",
        "version": __version__,
        "exported_at": utc_now(),
        "limitation": LIMITATION,
        "jeeves_sovereign": False,
        "hosted_v1": "lamb-check-only",
        "messages": list(messages),
        "receipts": list(receipts or []),
        "receipts_verify": verify or {},
    }


def to_markdown(bundle_obj: dict[str, Any]) -> str:
    lines: list[str] = [
        "# AZAI conversation",
        "",
        f"Exported: {bundle_obj.get('exported_at') or utc_now()}",
        f"Version: {bundle_obj.get('version') or __version__}",
        "Jeeves is not sovereign. Lamb Lens governs every turn.",
        "",
        "## Chat",
        "",
    ]
    for msg in bundle_obj.get("messages") or []:
        role = str(msg.get("role") or "user")
        who = {"user": "You", "assistant": "AZAI / Jeeves", "system": "System"}.get(role, role)
        lines.append(f"**{who}:**")
        lines.append("")
        lines.append(str(msg.get("content") or ""))
        lines.append("")
    receipts = bundle_obj.get("receipts") or []
    lines.extend(["## Receipts", ""])
    if not receipts:
        lines.append("(no receipts)")
    else:
        lines.append("| timestamp | action | result | hash |")
        lines.append("|---|---|---|---|")
        for rec in receipts:
            h = str(rec.get("hash") or "")[:16]
            lines.append(
                f"| {rec.get('timestamp', '')} | {rec.get('action', '')} | "
                f"{rec.get('result', '')} | `{h}` |"
            )
    lines.append("")
    lines.append("_Constitutional gate, not a proof of ethics. Apache-2.0, Aziel Eliab._")
    lines.append("")
    return "\n".join(lines)
