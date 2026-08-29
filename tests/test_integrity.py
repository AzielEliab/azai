"""Integrity screen fields and memory confirm."""

from azai.runtime import Runtime


def test_integrity_fields(tmp_path) -> None:
    rt = Runtime(data_dir=tmp_path)
    integ = rt.integrity()
    assert integ["peace"] in {"PASS", "CHECK", "FAIL"}
    assert integ["clarity"] in {"PASS", "CHECK", "FAIL"}
    assert integ["service"] in {"PASS", "CHECK", "FAIL"}
    assert integ["runtime"] == "OPEN"
    assert integ["jeeves"] == "READY"
    assert "local" in integ["providers"]


def test_memory_requires_confirm(tmp_path) -> None:
    rt = Runtime(data_dir=tmp_path)
    denied = rt.remember("secret note", confirm=False)
    assert denied["ok"] is False
    ok = rt.remember("secret note", confirm=True)
    assert ok["ok"] is True
    assert ok["mode"] == "session-only"
