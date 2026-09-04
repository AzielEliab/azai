"""CLI smoke: version, models, integrity, chat local, memory confirm."""

from azai.cli import main


def test_cli_version(capsys) -> None:
    assert main(["version"]) == 0
    out = capsys.readouterr().out
    assert "azai 0.3.1" in out


def test_cli_jeeves(capsys) -> None:
    assert main(["jeeves"]) == 0
    out = capsys.readouterr().out
    assert "Ask Jeeves" in out
    assert "not sovereign" in out.lower()
    assert "Lamb Lens first" in out
    assert "cannot modify scores" in out.lower() or "Cannot modify scores" in out
    assert "SPRE" in out
    assert "azielcorpuslibrary.net" in out
    assert main(["jeeves", "--json"]) == 0
    jout = capsys.readouterr().out
    assert '"mode": "ask-jeeves"' in jout or '"mode":"ask-jeeves"' in jout.replace(" ", "")


def test_cli_models(capsys) -> None:
    assert main(["models"]) == 0
    out = capsys.readouterr().out
    for name in ("local", "ollama", "blend", "gpt", "grok", "venice"):
        assert name in out


def test_cli_chat_local(capsys) -> None:
    assert main(["chat", "--model", "local", "--message", "hello"]) == 0
    out = capsys.readouterr().out
    assert "Jeeves" in out


def test_cli_integrity(capsys) -> None:
    assert main(["integrity", "--json"]) == 0
    out = capsys.readouterr().out
    assert "peace" in out.lower() or "PASS" in out


def test_cli_ollama_status(capsys) -> None:
    assert main(["ollama"]) == 0
    out = capsys.readouterr().out
    assert "Ollama" in out
    assert "127.0.0.1:11434" in out


def test_cli_memory_requires_confirm(capsys) -> None:
    assert main(["remember", "--text", "note"]) == 2
    assert main(["remember", "--text", "note", "--confirm"]) == 0
