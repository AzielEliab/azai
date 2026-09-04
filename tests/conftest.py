"""Isolate AZAI tests: tmp data dir, no network keys, no provider hooks leftover."""

from __future__ import annotations

import os

import pytest

from azai import ollama as ollama_mod
from azai.ollama import clear_test_hooks as clear_ollama_hooks
from azai.providers import clear_test_hooks


def _isolated_ollama_probe() -> dict:
    return {
        "ok": False,
        "reachable": False,
        "url": "http://127.0.0.1:11434",
        "model": "llama3.2",
        "model_present": False,
        "models": [],
        "error": "test isolation",
        "steps": None,
    }


@pytest.fixture(autouse=True)
def _isolate(tmp_path, monkeypatch):
    monkeypatch.setenv("AZAI_DATA", str(tmp_path / "AZAI_DATA"))
    monkeypatch.chdir(tmp_path)
    for key in ("OPENAI_API_KEY", "XAI_API_KEY", "GROK_API_KEY", "VENICE_API_KEY"):
        monkeypatch.delenv(key, raising=False)
    clear_test_hooks()
    clear_ollama_hooks()
    ollama_mod.TEST_PROBE = _isolated_ollama_probe
    yield
    clear_test_hooks()
    clear_ollama_hooks()
