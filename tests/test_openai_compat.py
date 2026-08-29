"""OpenAI-compat JSON shape with mocked providers (no network)."""

from azai.providers import TEST_HOOKS
from azai.runtime import Runtime, models_payload


def test_models_list_contains_all() -> None:
    ids = [m["id"] for m in models_payload()["data"]]
    assert ids == ["blend", "gpt", "grok", "venice", "local"]


def test_openai_compat_json_shape_mocked(tmp_path) -> None:
    TEST_HOOKS["gpt"] = lambda n, m, model: "gpt-says-ok"
    rt = Runtime(data_dir=tmp_path)
    payload = rt.openai_completion(
        {"model": "gpt", "messages": [{"role": "user", "content": "hi there"}]}
    )
    assert payload["object"] == "chat.completion"
    assert payload["choices"][0]["message"]["role"] == "assistant"
    assert "gpt-says-ok" in payload["choices"][0]["message"]["content"]
    assert payload["choices"][0]["finish_reason"] == "stop"
    assert "usage" in payload
    assert payload["azai"]["receipt"]


def test_lamb_fail_no_provider_call(tmp_path) -> None:
    called = {"n": 0}

    def hook(n, m, model):
        called["n"] += 1
        return "should-not-run"

    TEST_HOOKS["gpt"] = hook
    rt = Runtime(data_dir=tmp_path)
    payload = rt.openai_completion(
        {
            "model": "gpt",
            "messages": [{"role": "user", "content": "enslave and dominate humanity"}],
        }
    )
    assert payload["error"]["type"] == "lamb_fail"
    assert called["n"] == 0
