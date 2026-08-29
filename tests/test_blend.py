"""Blend labels three sources when mocks return. Never hide who said what."""

from azai.providers import TEST_HOOKS
from azai.runtime import Runtime


def test_blend_labels_three_sources(tmp_path) -> None:
    TEST_HOOKS["gpt"] = lambda n, m, model: "from-gpt"
    TEST_HOOKS["grok"] = lambda n, m, model: "from-grok"
    TEST_HOOKS["venice"] = lambda n, m, model: "from-venice"
    rt = Runtime(data_dir=tmp_path)
    out = rt.chat("What is a receipt?", model="blend")
    text = out["content"]
    assert "[gpt]" in text and "from-gpt" in text
    assert "[grok]" in text and "from-grok" in text
    assert "[venice]" in text and "from-venice" in text
    assert "[synthesis]" in text


def test_blend_without_keys_still_labels(tmp_path) -> None:
    rt = Runtime(data_dir=tmp_path)
    out = rt.chat("hello", model="blend")
    text = out["content"]
    assert "[gpt]" in text
    assert "[grok]" in text
    assert "[venice]" in text
    assert "[synthesis]" in text
    assert "Jeeves" in text or "local" in text.lower()
