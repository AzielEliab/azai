"""Lamb Lens — Peace → Clarity → Service.

Deterministic rule functions on text. This is a constitutional gate,
not a proof of ethics. FAIL blocks the turn (no provider call).
Jailbreak phrases such as "ignore previous instructions" are CHECK,
never a silent pass.

Python and the Worker JS port MUST stay in lockstep.
"""

from __future__ import annotations

from typing import Any

# Keep these lists identical in workers/download-tracker/src/engine.js
PEACE_FAIL = (
    "enslave",
    "dominate humanity",
    "dominate humans",
    "take over the world",
    "you are sovereign",
    "jeeves is sovereign",
    "override the operator",
    "make them obey",
    "force the user to",
)

CLARITY_FAIL = (
    "deceive as the goal",
    "lie to everyone",
    "gaslight the user as the goal",
    "hide the truth as the goal",
)

SERVICE_FAIL = (
    "serve by dominating",
    "force compliance",
    "coerce the operator",
)

CHECK_PATTERNS = (
    "ignore previous instructions",
    "ignore all previous",
    "disregard the constitution",
    "bypass lamb",
    "jailbreak",
)

VERDICT_ORDER = {"FAIL": 2, "CHECK": 1, "PASS": 0}


def normalize(text: str) -> str:
    return " ".join((text or "").lower().split())


def _axis(text_n: str, fail_patterns: tuple[str, ...], check: bool) -> str:
    for pat in fail_patterns:
        if pat in text_n:
            return "FAIL"
    if check:
        return "CHECK"
    return "PASS"


def _worse(a: str, b: str) -> str:
    return a if VERDICT_ORDER[a] >= VERDICT_ORDER[b] else b


def check_text(text: str) -> dict[str, Any]:
    """Run Peace / Clarity / Service on ``text``.

    Returns ``{peace, clarity, service, overall, notes, honest}``.
    """
    n = normalize(text)
    jailbreak = any(p in n for p in CHECK_PATTERNS)
    peace = _axis(n, PEACE_FAIL, jailbreak)
    clarity = _axis(n, CLARITY_FAIL, jailbreak)
    service = _axis(n, SERVICE_FAIL, jailbreak)
    overall = _worse(_worse(peace, clarity), service)
    notes: list[str] = []
    if jailbreak:
        notes.append("jailbreak phrasing detected — CHECK, not a silent pass")
    if peace == "FAIL":
        notes.append("peace: domination language")
    if clarity == "FAIL":
        notes.append("clarity: deception-as-goal")
    if service == "FAIL":
        notes.append("service: coercion / domination-as-service")
    if overall == "PASS":
        notes.append("no rule fired")
    return {
        "peace": peace,
        "clarity": clarity,
        "service": service,
        "overall": overall,
        "notes": notes,
        "honest": "constitutional gate, not a proof of ethics",
        "constitution": "Lamb Lens v1.0 — Peace → Clarity → Service",
    }


def is_fail(result: dict[str, Any]) -> bool:
    return str(result.get("overall") or "") == "FAIL"
