"""Sealed runtime blocks chat; receipts remain readable."""

import pytest

from azai.runtime import Runtime, SealedError


def test_sealed_blocks_chat(tmp_path) -> None:
    rt = Runtime(data_dir=tmp_path)
    rt.seal(reason="test")
    with pytest.raises(SealedError):
        rt.chat("hello")
    rows = rt.receipts.read()
    assert any(r["action"] == "seal" for r in rows)
    assert any(r["action"] == "chat_blocked" for r in rows)


def test_open_allows_chat_again(tmp_path) -> None:
    rt = Runtime(data_dir=tmp_path)
    rt.seal()
    rt.open()
    out = rt.chat("hello", model="local")
    assert "Jeeves" in out["content"]
    assert out["model"] == "local"


def test_openai_sealed_json_shape(tmp_path) -> None:
    rt = Runtime(data_dir=tmp_path)
    rt.seal()
    payload = rt.openai_completion({"model": "local", "messages": [{"role": "user", "content": "hi"}]})
    assert "error" in payload
    assert payload["error"]["type"] == "sealed"
