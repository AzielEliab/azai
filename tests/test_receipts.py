"""Receipt hash chain (TemporalLock-lite)."""

from azai.receipts import GENESIS_PREV, ReceiptLog, chain_hash


def test_receipts_chain(tmp_path) -> None:
    log = ReceiptLog(tmp_path)
    a = log.append("boot", "PASS")
    b = log.append("chat", "PASS")
    assert a["prev_hash"] == GENESIS_PREV
    assert b["prev_hash"] == a["hash"]
    assert b["hash"] == chain_hash(a["hash"], b["payload"])
    v = log.verify()
    assert v["ok"] is True
    assert v["count"] == 2


def test_receipts_tamper_detected(tmp_path) -> None:
    log = ReceiptLog(tmp_path)
    log.append("boot", "PASS")
    log.append("chat", "PASS")
    rows = log.read()
    rows[-1]["hash"] = "0" * 64
    log.path.write_text("".join(__import__("json").dumps(r, sort_keys=True) + "\n" for r in rows), encoding="utf-8")
    v = log.verify()
    assert v["ok"] is False
