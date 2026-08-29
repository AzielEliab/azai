"""Isolate AZAI tests: tmp data dir, no network keys, no provider hooks leftover."""

from __future__ import annotations

import os

import pytest

from azai.providers import clear_test_hooks


@pytest.fixture(autouse=True)
def _isolate(tmp_path, monkeypatch):
    monkeypatch.setenv("AZAI_DATA", str(tmp_path / "AZAI_DATA"))
    monkeypatch.chdir(tmp_path)
    for key in ("OPENAI_API_KEY", "XAI_API_KEY", "GROK_API_KEY", "VENICE_API_KEY"):
        monkeypatch.delenv(key, raising=False)
    clear_test_hooks()
    yield
    clear_test_hooks()
