"""Append-only JSONL receipt chain (TemporalLock-lite).

Hash = sha256(prev_hash + canonical payload). Genesis prev is 64 zeros.
Stored under AZAI_DATA/receipts.jsonl. Anyone can recompute.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

GENESIS_PREV = "0" * 64


def utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def canonical(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def chain_hash(prev_hash: str, payload: dict[str, Any]) -> str:
    body = (prev_hash or GENESIS_PREV) + canonical(payload)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


class ReceiptLog:
    def __init__(self, data_dir: str | Path) -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.data_dir / "receipts.jsonl"
        if not self.path.exists():
            self.path.write_text("", encoding="utf-8")

    def _last_hash(self) -> str:
        last = GENESIS_PREV
        if not self.path.exists() or self.path.stat().st_size == 0:
            return last
        with self.path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                last = rec.get("hash") or last
        return last

    def append(
        self,
        action: str,
        result: str,
        extra: dict[str, Any] | None = None,
        timestamp: str | None = None,
    ) -> dict[str, Any]:
        prev = self._last_hash()
        payload: dict[str, Any] = {
            "action": action,
            "result": result,
            "timestamp": timestamp or utc_now(),
        }
        if extra:
            payload["extra"] = extra
        rec = {
            "timestamp": payload["timestamp"],
            "action": action,
            "result": result,
            "prev_hash": prev,
            "hash": chain_hash(prev, payload),
            "payload": payload,
        }
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, sort_keys=True) + "\n")
        return rec

    def read(self) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        if not self.path.exists():
            return out
        with self.path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    out.append(json.loads(line))
        return out

    def verify(self) -> dict[str, Any]:
        rows = self.read()
        prev = GENESIS_PREV
        for i, rec in enumerate(rows):
            payload = rec.get("payload") or {}
            expected_prev = prev
            expected_hash = chain_hash(expected_prev, payload)
            if rec.get("prev_hash") != expected_prev or rec.get("hash") != expected_hash:
                return {
                    "ok": False,
                    "broken_at": i,
                    "count": len(rows),
                    "expected_hash": expected_hash,
                    "got_hash": rec.get("hash"),
                }
            prev = rec["hash"]
        return {"ok": True, "count": len(rows), "tip": prev if rows else GENESIS_PREV}


def format_rows(rows: Iterable[dict[str, Any]]) -> str:
    lines = []
    for rec in rows:
        lines.append(
            f"{rec.get('timestamp')} | {rec.get('action')} | {rec.get('result')} | "
            f"prev={str(rec.get('prev_hash') or '')[:12]}… hash={str(rec.get('hash') or '')[:12]}…"
        )
    return "\n".join(lines) if lines else "(no receipts)"
