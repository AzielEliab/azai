"""CLI smoke: version, models, integrity, chat local, memory confirm."""

from azai.cli import main


def test_cli_version(capsys) -> None:
    assert main(["version"]) == 0
    out = capsys.readouterr().out
    assert "azai 0.2.0" in out


def test_cli_models(capsys) -> None:
    assert main(["models"]) == 0
    out = capsys.readouterr().out
    for name in ("blend", "gpt", "grok", "venice", "local"):
        assert name in out


def test_cli_chat_local(capsys) -> None:
    assert main(["chat", "--model", "local", "--message", "hello"]) == 0
    out = capsys.readouterr().out
    assert "Jeeves" in out


def test_cli_integrity(capsys) -> None:
    assert main(["integrity", "--json"]) == 0
    out = capsys.readouterr().out
    assert "peace" in out.lower() or "PASS" in out


def test_cli_memory_requires_confirm(capsys) -> None:
    assert main(["remember", "--text", "note"]) == 2
    assert main(["remember", "--text", "note", "--confirm"]) == 0
