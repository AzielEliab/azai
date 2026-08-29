"""Local Jeeves stub — instrument inside AZAI, not a foundation model.

Does not pretend to be GPT, Grok, or Venice. Speaks under Lamb Lens.
Jeeves is not sovereign.
"""

from __future__ import annotations

from typing import Any

from azai.config import MOTTO

OATH = "Truth belongs to the Source; understanding belongs to service."


def local_reply(prompt: str, lamb: dict[str, Any]) -> str:
    """Constitution-bound local answer. Never claims to be GPT."""
    overall = lamb.get("overall", "PASS")
    body = (
        "[local / Jeeves]\n"
        "I am Jeeves, the instrument inside AZAI — not GPT, not Grok, not Venice, "
        "and not sovereign.\n"
        f"Lamb Lens: peace={lamb.get('peace')} clarity={lamb.get('clarity')} "
        f"service={lamb.get('service')} → {overall}\n"
        f"Oath: {OATH}\n\n"
        "I can mirror, clarify, and keep receipts. I do not invent a foundation model "
        "on this machine. Set OPENAI_API_KEY, XAI_API_KEY or GROK_API_KEY, and/or "
        "VENICE_API_KEY to blend live providers. Paid calls stay on this operator's "
        f"local `azai serve`.\n\n"
        f"You said: {prompt.strip()[:2000]}\n\n"
        f"{MOTTO}"
    )
    return body
