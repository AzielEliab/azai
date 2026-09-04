"""Ollama base + JEEVES wrap. Hooks only — no live network."""

from azai import ollama as ollama_mod
from azai.jeeves import SYSTEM, wrap_messages
from azai.ollama import call_chat
from azai.runtime import Runtime


def test_local_uses_ollama_via_jeeves(tmp_path) -> None:
    seen: dict = {}

    def hook(name, messages, model):
        seen["name"] = name
        seen["messages"] = messages
        seen["model"] = model
        return "from-ollama-base"

    ollama_mod.TEST_HOOKS["ollama"] = hook
    ollama_mod.TEST_PROBE = lambda: {
        "ok": True,
        "reachable": True,
        "url": "http://127.0.0.1:11434",
        "model": "llama3.2",
        "model_present": True,
        "models": ["llama3.2:latest"],
        "steps": None,
    }
    rt = Runtime(data_dir=tmp_path)
    out = rt.chat("hello ollama", model="local")
    assert "from-ollama-base" in out["content"]
    assert "Jeeves" in out["content"] or "JEEVES" in out["content"]
    assert "not sovereign" in out["content"].lower()
    assert seen["name"] == "ollama"
    sys_text = " ".join(m["content"] for m in seen["messages"] if m["role"] == "system")
    assert "JEEVES" in sys_text
    assert "not sovereign" in sys_text.lower()


def test_ollama_model_same_jeeves_path(tmp_path) -> None:
    ollama_mod.TEST_HOOKS["ollama"] = lambda n, m, model: "direct-ollama"
    ollama_mod.TEST_PROBE = lambda: {
        "ok": True,
        "reachable": True,
        "url": "http://127.0.0.1:11434",
        "model": "llama3.2",
        "model_present": True,
        "models": ["llama3.2"],
        "steps": None,
    }
    rt = Runtime(data_dir=tmp_path)
    out = rt.chat("hi", model="ollama")
    assert "direct-ollama" in out["content"]
    assert out["model"] == "ollama"


def test_wrap_messages_prepends_jeeves_once() -> None:
    rows = wrap_messages([{"role": "user", "content": "hi"}])
    assert rows[0]["role"] == "system"
    assert "JEEVES" in rows[0]["content"]
    again = wrap_messages(rows)
    assert sum(1 for m in again if m.get("role") == "system" and "JEEVES" in m["content"]) == 1
    assert "not sovereign" in SYSTEM.lower()


def test_call_chat_hook_no_network() -> None:
    ollama_mod.TEST_HOOKS["ollama"] = lambda n, m, model: f"ok-{model}"
    text = call_chat([{"role": "user", "content": "x"}])
    assert text.startswith("ok-")
