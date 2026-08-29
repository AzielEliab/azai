"""Local mode without keys. Jeeves does not pretend to be GPT."""

from azai.runtime import Runtime


def test_local_without_keys(tmp_path) -> None:
    rt = Runtime(data_dir=tmp_path)
    out = rt.chat("What are you?", model="local")
    text = out["content"]
    assert "Jeeves" in text
    assert "not GPT" in text or "not a foundation model" in text.lower() or "not GPT" in text
    assert "not sovereign" in text.lower()
    assert out["model"] == "local"


def test_gpt_without_key_falls_to_jeeves(tmp_path) -> None:
    rt = Runtime(data_dir=tmp_path)
    out = rt.chat("hello", model="gpt")
    assert "Jeeves" in out["content"]
    assert "OPENAI_API_KEY" in out["content"]
