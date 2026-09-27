"""Optional Ollama slot. Default model=local never uses it. Hooks only — no live network."""

from azai import ollama as ollama_mod
from azai.jeeves import SYSTEM, wrap_messages
from azai.ollama import call_chat
from azai.runtime import Runtime


def _up_probe() -> dict:
    return {
        "ok": True,
        "reachable": True,
        "url": "http://127.0.0.1:11434",
        "model": "llama3.2",
        "model_present": True,
        "models": ["llama3.2:latest"],
        "steps": None,
    }


def test_local_does_not_use_ollama_even_when_up(tmp_path) -> None:
    seen = {"n": 0}

    def hook(name, messages, model):
        seen["n"] += 1
        seen["name"] = name
        return "from-ollama-base"

    ollama_mod.TEST_HOOKS["ollama"] = hook
    ollama_mod.TEST_PROBE = _up_probe
    rt = Runtime(data_dir=tmp_path)
    out = rt.chat("hello ollama", model="local")
    assert seen["n"] == 0
    assert "from-ollama-base" not in out["content"]
    assert "Jeeves" in out["content"] or "JEEVES" in out["content"]
    assert "not sovereign" in out["content"].lower()
    assert "does not require Ollama" in out["content"]
    assert "llama3.2" not in out["content"]
    assert "ollama pull" not in out["content"].lower()
    assert out["model"] == "local"


def test_ollama_model_same_jeeves_path(tmp_path) -> None:
    ollama_mod.TEST_HOOKS["ollama"] = lambda n, m, model: "direct-ollama"
    ollama_mod.TEST_PROBE = _up_probe
    rt = Runtime(data_dir=tmp_path)
    out = rt.chat("hi", model="ollama")
    assert "direct-ollama" in out["content"]
    assert out["model"] == "ollama"
    assert "not sovereign" in out["content"].lower()


def test_backend_env_opts_local_into_ollama(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("AZAI_BACKEND", "ollama")
    seen = {"n": 0}

    def hook(name, messages, model):
        seen["n"] += 1
        return "env-ollama"

    ollama_mod.TEST_HOOKS["ollama"] = hook
    ollama_mod.TEST_PROBE = _up_probe
    rt = Runtime(data_dir=tmp_path)
    out = rt.chat("hi", model="local")
    assert seen["n"] == 1
    assert "env-ollama" in out["content"]
    assert out["model"] == "local"


def test_wrap_messages_prepends_jeeves_once() -> None:
    rows = wrap_messages([{"role": "user", "content": "hi"}])
    assert rows[0]["role"] == "system"
    assert "JEEVES" in rows[0]["content"]
    again = wrap_messages(rows)
    assert sum(1 for m in again if m.get("role") == "system" and "JEEVES" in m["content"]) == 1
    assert "not sovereign" in SYSTEM.lower()
    assert "Service → Clarity → Peace" in SYSTEM
    assert "does not require Ollama" in SYSTEM


def test_call_chat_hook_no_network() -> None:
    ollama_mod.TEST_HOOKS["ollama"] = lambda n, m, model: f"ok-{model}"
    text = call_chat([{"role": "user", "content": "x"}])
    assert text.startswith("ok-")
