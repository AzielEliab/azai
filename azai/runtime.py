"""AZAI runtime: Lamb gate, blend, seal, memory, OpenAI-compat chat.

Paid provider calls happen here on the operator's machine.
Session transcript is import/exportable. Receipts stay append-only.
"""

from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import Any

from azai.config import DEFAULT_MODEL, LIMITATION, MODELS
from azai.debug import dlog
from azai.exchange import bundle as make_bundle
from azai.exchange import parse_conversation, simple_text, to_markdown
from azai.jeeves import local_reply, sanitize_site_context, wrap_messages
from azai.lamb import check_text, is_fail
from azai.providers import provider_status, try_named
from azai.receipts import ReceiptLog

BLEND_SOURCES = ("gpt", "grok", "venice")


class SealedError(RuntimeError):
    """Runtime is sealed; intelligence output is blocked."""


class LambBlocked(RuntimeError):
    """Lamb Lens FAIL: turn blocked, no provider call."""

    def __init__(self, lamb: dict[str, Any], stage: str) -> None:
        super().__init__(f"Lamb Lens FAIL on {stage}")
        self.lamb = lamb
        self.stage = stage


def resolve_data_dir(data_dir: str | None = None) -> Path:
    import os

    if data_dir:
        p = Path(data_dir)
    else:
        env = os.environ.get("AZAI_DATA")
        p = Path(env) if env else Path.cwd() / "AZAI_DATA"
    p.mkdir(parents=True, exist_ok=True)
    return p


class Runtime:
    def __init__(self, data_dir: str | Path | None = None) -> None:
        self.data_dir = resolve_data_dir(str(data_dir) if data_dir else None)
        self.receipts = ReceiptLog(self.data_dir)
        self.state_path = self.data_dir / "runtime.json"
        self.session_path = self.data_dir / "session.json"
        self._session_memory: list[str] = []
        self._transcript: list[dict[str, Any]] = []
        self._load_state()
        self._load_session()

    def _load_state(self) -> None:
        if self.state_path.exists():
            try:
                self._state = json.loads(self.state_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                self._state = {"sealed": False}
        else:
            self._state = {"sealed": False}
            self._save_state()

    def _save_state(self) -> None:
        self.state_path.write_text(json.dumps(self._state, indent=2) + "\n", encoding="utf-8")

    def _load_session(self) -> None:
        if not self.session_path.exists():
            self._transcript = []
            return
        try:
            data = json.loads(self.session_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            self._transcript = []
            return
        msgs = data.get("messages") if isinstance(data, dict) else data
        if isinstance(msgs, list):
            self._transcript = [m for m in msgs if isinstance(m, dict)]
        else:
            self._transcript = []

    def _save_session(self) -> None:
        payload = {"messages": self._transcript}
        self.session_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    def transcript(self) -> list[dict[str, Any]]:
        return list(self._transcript)

    @property
    def sealed(self) -> bool:
        return bool(self._state.get("sealed"))

    def seal(self, reason: str = "operator") -> dict[str, Any]:
        self._state["sealed"] = True
        self._save_state()
        rec = self.receipts.append("seal", "SEALED", extra={"reason": reason})
        dlog("seal", reason=reason)
        return {"ok": True, "sealed": True, "receipt": rec["hash"]}

    def open(self, reason: str = "operator") -> dict[str, Any]:
        self._state["sealed"] = False
        self._save_state()
        rec = self.receipts.append("open", "OPEN", extra={"reason": reason})
        dlog("open", reason=reason)
        return {"ok": True, "sealed": False, "receipt": rec["hash"]}

    def integrity(self, sample: str = "") -> dict[str, Any]:
        lamb = check_text(sample or "peace clarity service")
        chain = self.receipts.verify()
        return {
            "lamb": lamb,
            "peace": lamb["peace"],
            "clarity": lamb["clarity"],
            "service": lamb["service"],
            "overall": lamb["overall"],
            "runtime": "SEALED" if self.sealed else "OPEN",
            "receipts": chain,
            "jeeves": "LOCKED" if self.sealed else "READY",
            "providers": {
                name: {"present": meta["present"]}
                for name, meta in provider_status().items()
            },
            "honest": lamb["honest"],
            "limitation": LIMITATION,
        }

    def remember(self, text: str, confirm: bool = False) -> dict[str, Any]:
        if not confirm:
            rec = self.receipts.append("memory_denied", "DENIED", extra={"reason": "confirm required"})
            return {
                "ok": False,
                "error": "memory writes require explicit confirm",
                "receipt": rec["hash"],
            }
        self._session_memory.append(text)
        rec = self.receipts.append("memory", "SESSION", extra={"n": len(self._session_memory)})
        return {
            "ok": True,
            "mode": "session-only",
            "count": len(self._session_memory),
            "receipt": rec["hash"],
            "note": "Session-only by default. Not written as verified memory.",
        }

    def _record(self, role: str, content: str, **extra: Any) -> None:
        row: dict[str, Any] = {"role": role, "content": content}
        row.update(extra)
        self._transcript.append(row)
        self._save_session()

    def import_text(self, content: str, filename: str = "") -> dict[str, Any]:
        messages = parse_conversation(content, filename=filename)
        return self.import_messages(messages, source=filename or "import")

    def import_messages(self, messages: list[dict[str, str]], source: str = "import") -> dict[str, Any]:
        self._transcript = []
        for m in messages:
            role = str(m.get("role") or "user")
            body = str(m.get("content") or "")
            self._transcript.append({"role": role, "content": body})
        self._save_session()
        rec = self.receipts.append("import", "OK", extra={"n": len(self._transcript), "source": source})
        dlog("import", n=len(self._transcript), source=source)
        return {"ok": True, "count": len(self._transcript), "receipt": rec["hash"], "messages": self.transcript()}

    def export_bundle(self) -> dict[str, Any]:
        return make_bundle(self.transcript(), self.receipts.read(), self.receipts.verify())

    def export_json(self) -> str:
        return json.dumps(self.export_bundle(), indent=2) + "\n"

    def export_markdown(self) -> str:
        return to_markdown(self.export_bundle())

    def _blend(self, messages: list[dict[str, str]]) -> str:
        parts: list[str] = []
        available: list[str] = []
        for name in BLEND_SOURCES:
            dlog("provider", name=name)
            text, ok = try_named(name, messages)
            parts.append(f"[{name}]\n{text.strip()}")
            if ok:
                available.append(name)
        if available:
            synth = (
                f"Optional paid blend. Present: {', '.join(available)}. "
                "Each instrument is labeled above; nothing is hidden. "
                "JEEVES is not sovereign. Lamb Lens gated this turn. "
                "The true local base is Ollama + JEEVES (model=local)."
            )
        else:
            synth = (
                "No live paid providers (keys missing or hooks empty). "
                "Falling back to local JEEVES on the Ollama base — not GPT, not a hosted proxy."
            )
            prompt = messages[-1]["content"] if messages else ""
            parts.append(local_reply(prompt, check_text(prompt), messages=messages))
        parts.append(f"[synthesis]\n{synth}")
        return "\n\n".join(parts)

    def chat(
        self,
        prompt: str,
        model: str = DEFAULT_MODEL,
        site_context: Any = None,
    ) -> dict[str, Any]:
        model = (model or DEFAULT_MODEL).lower().strip()
        if model not in MODELS:
            model = DEFAULT_MODEL
        cleaned_context = sanitize_site_context(site_context)
        context_n = len(cleaned_context)
        dlog("chat", model=model, n=len(prompt or ""), site_context_n=context_n)
        if self.sealed:
            rec = self.receipts.append("chat_blocked", "SEALED", extra={"model": model})
            self._record("user", prompt, blocked="sealed")
            raise SealedError("runtime is sealed — Jeeves locked; receipts remain readable") from None

        lamb_in = check_text(prompt)
        if is_fail(lamb_in):
            rec = self.receipts.append(
                "lamb_fail_prompt",
                "FAIL",
                extra={"peace": lamb_in["peace"], "clarity": lamb_in["clarity"], "service": lamb_in["service"]},
            )
            self._record("user", prompt, lamb="FAIL")
            raise LambBlocked(lamb_in, "prompt")

        messages = [{"role": "user", "content": prompt}]
        if self._session_memory:
            messages.insert(
                0,
                {
                    "role": "system",
                    "content": "Session notes (operator-confirmed, session-only):\n"
                    + "\n".join(self._session_memory[-8:]),
                },
            )
        messages = wrap_messages(messages, site_context=cleaned_context)

        if model in {"local", "ollama"}:
            content = local_reply(prompt, lamb_in, messages=messages)
        elif model == "blend":
            content = self._blend(messages)
        else:
            text, ok = try_named(model, messages)
            if ok:
                content = f"[{model}]\n{text.strip()}"
            else:
                content = local_reply(prompt, lamb_in, messages=messages) + f"\n\n({model} {text})"

        lamb_out = check_text(content)
        if is_fail(lamb_out):
            rec = self.receipts.append("lamb_fail_output", "FAIL", extra={"model": model})
            self._record("user", prompt, lamb="FAIL", stage="output")
            raise LambBlocked(lamb_out, "output")

        rec = self.receipts.append(
            "chat",
            lamb_out["overall"],
            extra={
                "model": model,
                "lamb_in": lamb_in["overall"],
                "lamb_out": lamb_out["overall"],
                "site_context_n": context_n,
            },
        )
        self._record("user", prompt)
        self._record(
            "assistant",
            content,
            model=model,
            receipt=rec["hash"],
            lamb=lamb_out["overall"],
            site_context_n=context_n,
        )
        return {
            "content": content,
            "simple": simple_text(content),
            "model": model,
            "lamb_in": lamb_in,
            "lamb_out": lamb_out,
            "receipt": rec["hash"],
            "sealed": False,
            "ask_jeeves": True,
            "jeeves_sovereign": False,
            "site_context_n": context_n,
        }

    def openai_completion(self, body: dict[str, Any]) -> dict[str, Any]:
        messages = body.get("messages") or []
        model = str(body.get("model") or DEFAULT_MODEL)
        azai_extra = body.get("azai") if isinstance(body.get("azai"), dict) else {}
        site_context = (
            body.get("site_context")
            or body.get("corpus_context")
            or azai_extra.get("site_context")
        )
        prompt_parts = []
        for msg in messages:
            if msg.get("role") == "user":
                prompt_parts.append(str(msg.get("content") or ""))
        prompt = "\n".join(prompt_parts) or str(body.get("prompt") or "")
        try:
            result = self.chat(prompt, model=model, site_context=site_context)
        except SealedError as exc:
            return {
                "error": {"message": str(exc), "type": "sealed", "code": "runtime_sealed"},
                "lamb": self.integrity()["lamb"],
            }
        except LambBlocked as exc:
            return {
                "error": {
                    "message": str(exc),
                    "type": "lamb_fail",
                    "code": "lamb_blocked",
                    "lamb": exc.lamb,
                }
            }
        created = int(time.time())
        return {
            "id": f"chatcmpl-{uuid.uuid4().hex[:20]}",
            "object": "chat.completion",
            "created": created,
            "model": result["model"],
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": result["content"]},
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            "azai": {
                "lamb_in": result["lamb_in"],
                "lamb_out": result["lamb_out"],
                "receipt": result["receipt"],
                "limitation": LIMITATION,
                "simple": result["simple"],
                "hosted_v1": "lamb-check-only",
                "ask_jeeves": True,
                "jeeves_sovereign": False,
                "site_context_n": result.get("site_context_n", 0),
            },
        }


def models_payload() -> dict[str, Any]:
    return {
        "object": "list",
        "data": [
            {
                "id": m,
                "object": "model",
                "created": 0,
                "owned_by": "azai",
            }
            for m in MODELS
        ],
    }
