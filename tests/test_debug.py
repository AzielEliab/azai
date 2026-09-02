"""AZAI_DEBUG=1 writes local stderr traces and never logs key values."""

from azai.debug import dlog, enabled, redact


def test_debug_off_by_default(monkeypatch) -> None:
    monkeypatch.delenv("AZAI_DEBUG", raising=False)
    assert enabled() is False


def test_debug_on_stderr(monkeypatch, capsys) -> None:
    monkeypatch.setenv("AZAI_DEBUG", "1")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-secret-test-value")
    assert enabled() is True
    dlog("hello", key="should-not-appear")
    err = capsys.readouterr().err
    assert "[azai debug]" in err
    assert "hello" in err
    assert "should-not-appear" not in err
    assert "[redacted]" in err
    assert "sk-secret-test-value" not in err


def test_redact_strips_env_key(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "sk-secret-test-value")
    assert "sk-secret-test-value" not in redact("using sk-secret-test-value")
