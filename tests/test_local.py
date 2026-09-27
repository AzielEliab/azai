"""Local mode without keys. Jeeves does not pretend to be GPT."""

import json

from azai.runtime import Runtime


def test_local_without_keys(tmp_path) -> None:
    rt = Runtime(data_dir=tmp_path)
    out = rt.chat("What are you?", model="local")
    text = out["content"]
    assert "Jeeves" in text
    assert "not GPT" in text or "not a foundation model" in text.lower() or "not GPT" in text
    assert "not sovereign" in text.lower()
    assert "Service → Clarity → Peace" in text
    assert out["model"] == "local"


def test_local_never_probes_ollama(tmp_path, monkeypatch) -> None:
    def boom():
        raise AssertionError("local core probed Ollama")

    monkeypatch.setattr("azai.jeeves.ollama_probe", boom)
    rt = Runtime(data_dir=tmp_path)
    out = rt.chat("What are you?", model="local")
    assert "not sovereign" in out["content"].lower()
    assert "does not require Ollama" in out["content"]


def test_local_adapts_to_session_and_site_context(tmp_path) -> None:
    rt = Runtime(data_dir=tmp_path)
    remembered = rt.remember("likes the river Arno", confirm=True)
    assert remembered["ok"] is True
    out = rt.chat(
        "What should you keep in mind?",
        model="local",
        site_context=[{"title": "Florence", "summary": "Public record about the city."}],
    )
    text = out["content"]
    assert "likes the river Arno" in text
    assert "Florence" in text
    assert "Public record about the city." in text
    assert out["site_context_n"] == 1
    dumped = json.dumps(rt.receipts.read())
    assert "Florence" not in dumped
    assert "likes the river Arno" not in dumped


def test_gpt_without_key_falls_to_jeeves(tmp_path) -> None:
    rt = Runtime(data_dir=tmp_path)
    out = rt.chat("hello", model="gpt")
    assert "Jeeves" in out["content"]
    assert "OPENAI_API_KEY" in out["content"]
