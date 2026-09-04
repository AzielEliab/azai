"""Ask Jeeves research-assistant mode: SYSTEM refusals and wrap_messages."""

from __future__ import annotations

import json

from azai.jeeves import (
    CORPUS_LIBRARY,
    INGEST_PIPELINE,
    MODE,
    MODE_LABEL,
    REFUSALS,
    SITE_CONTEXT_PREFIX,
    SOVEREIGN,
    SYSTEM,
    UPLOAD_GUIDANCE,
    format_site_context,
    mode_card,
    sanitize_site_context,
    upload_guidance,
    wrap_messages,
)
from azai.ollama import TEST_HOOKS
from azai.runtime import Runtime


def test_jeeves_is_not_sovereign_and_not_gpt() -> None:
    assert SOVEREIGN is False
    assert MODE == "ask-jeeves"
    assert "Ask Jeeves" in MODE_LABEL
    low = SYSTEM.lower()
    assert "not sovereign" in low
    assert "not gpt" in low
    assert "not a new foundation model" in low
    card = mode_card()
    assert card["sovereign"] is False
    assert card["not_gpt"] is True
    assert card["author"] == "Aziel Eliab"


def test_system_lamb_lens_first_public_corpus_never_operator() -> None:
    low = SYSTEM.lower()
    assert "lamb lens first" in low
    assert "public corpus" in low
    assert "never the operator" in low
    assert "ask jeeves" in low
    assert CORPUS_LIBRARY in SYSTEM


def test_system_hard_refusal_strings() -> None:
    low = SYSTEM.lower()
    for needle in (
        "never reveal operator account info",
        "credentials",
        "admin hashes",
        "hidden routes",
        "wipe",
        "score forge",
        "quarantine bypass",
        "cannot modify scores",
        "research assistant only",
        "same rights as a normal user",
    ):
        assert needle in low, needle
    for line in REFUSALS:
        # Each published refusal is represented in SYSTEM.
        assert "never reveal" in low or "cannot modify" in low
        assert any(word in low for word in line.lower().replace("—", " ").split() if len(word) > 6)


def test_system_upload_out_of_band_no_score_shortcut() -> None:
    low = SYSTEM.lower()
    assert "out of band" in low
    assert "no score shortcut" in low
    assert "spre" in low
    assert "clce" in low
    assert "physling" in low
    assert "bayesian ingest" in low
    assert "SPRE" in INGEST_PIPELINE
    assert "Bayesian" in INGEST_PIPELINE
    text = upload_guidance()
    assert text == UPLOAD_GUIDANCE
    assert "out of band" in text.lower()
    assert "no score shortcut" in text.lower()
    assert "SPRE" in text


def test_wrap_messages_prepends_jeeves_system_once() -> None:
    rows = wrap_messages([{"role": "user", "content": "What is Florence?"}])
    assert rows[0]["role"] == "system"
    assert rows[0]["content"] == SYSTEM
    assert "JEEVES" in rows[0]["content"]
    again = wrap_messages(rows)
    assert sum(1 for m in again if m.get("role") == "system" and m.get("content") == SYSTEM) == 1
    assert again[0]["content"] == SYSTEM


def test_wrap_messages_accepts_retrieved_site_context() -> None:
    rows = wrap_messages(
        [{"role": "user", "content": "Tell me about Florence."}],
        site_context=[
            {"title": "Florence", "summary": "A public library record about the city."},
            {"name": "Arno", "snippet": "The river beside the city."},
        ],
    )
    assert rows[0]["content"] == SYSTEM
    assert rows[1]["role"] == "system"
    assert SITE_CONTEXT_PREFIX in rows[1]["content"]
    assert "Florence" in rows[1]["content"]
    assert "Arno" in rows[1]["content"]
    assert "persist nothing secret" in rows[1]["content"].lower()
    assert "cannot modify scores" in rows[1]["content"].lower()
    # Second wrap does not duplicate context.
    again = wrap_messages(rows, site_context=[{"title": "Florence", "summary": "dup"}])
    assert sum(1 for m in again if SITE_CONTEXT_PREFIX in str(m.get("content") or "")) == 1


def test_site_context_drops_secrets_and_persists_nothing() -> None:
    cleaned = sanitize_site_context(
        [
            {"title": "Public note", "summary": "Safe summary."},
            {"title": "operator password dump", "summary": "should drop"},
            {"title": "admin hash", "summary": "abc"},
            {"title": "ok", "summary": "hidden route /admin/secret"},
            {"title": "creds", "summary": "credential: hunter2"},
        ]
    )
    titles = [r["title"] for r in cleaned]
    assert titles == ["Public note"]
    blob = format_site_context(
        {
            "hits": [
                {"title": "Public note", "summary": "Safe summary."},
                {"title": "api_key leak", "summary": "sk-demo"},
            ]
        }
    )
    assert "Public note" in blob
    assert "api_key" not in blob
    assert "sk-demo" not in blob


def test_runtime_chat_site_context_count_only_in_receipt(tmp_path) -> None:
    seen: dict = {}

    def hook(name, messages, model):
        seen["messages"] = messages
        return "from-context"

    TEST_HOOKS["ollama"] = hook
    from azai import ollama as ollama_mod

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
    out = rt.chat(
        "What does the library say?",
        model="local",
        site_context=[{"title": "Florence", "summary": "Public record."}],
    )
    assert out["ask_jeeves"] is True
    assert out["jeeves_sovereign"] is False
    assert out["site_context_n"] == 1
    sys_text = " ".join(m["content"] for m in seen["messages"] if m["role"] == "system")
    assert "Florence" in sys_text
    assert "JEEVES" in sys_text
    recs = rt.receipts.read()
    chat_recs = [r for r in recs if r.get("action") == "chat"]
    assert chat_recs
    extra = chat_recs[-1].get("extra") or {}
    dumped = json.dumps(extra)
    assert extra.get("site_context_n") == 1
    assert "Florence" not in dumped
    assert "Public record" not in dumped


def test_openai_completion_accepts_site_context(tmp_path) -> None:
    from azai import ollama as ollama_mod

    ollama_mod.TEST_HOOKS["ollama"] = lambda n, m, model: "ok"
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
    payload = rt.openai_completion(
        {
            "model": "local",
            "messages": [{"role": "user", "content": "hello library"}],
            "site_context": [{"title": "Gazetteer", "summary": "Places."}],
        }
    )
    assert payload["azai"]["ask_jeeves"] is True
    assert payload["azai"]["jeeves_sovereign"] is False
    assert payload["azai"]["site_context_n"] == 1
