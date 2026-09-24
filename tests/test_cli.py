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
    assert '"mode": "ask_jeeves"' in jout or '"mode":"ask_jeeves"' in jout.replace(" ", "")


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
    err = capsys.readouterr().err
    assert "confirm" in err.lower()
    assert main(["remember", "--text", "note", "--confirm"]) == 0


def test_cli_welcome_and_help(capsys) -> None:
    assert main([]) == 0
    out = capsys.readouterr().out
    assert "azai ui" in out
    assert "Aziel Eliab" in out
    assert "following arguments are required" not in out
    assert main(["--help"]) == 0
    help_out = capsys.readouterr().out
    assert "azai ui" in help_out
    assert "Advanced" in help_out
    assert "following arguments are required" not in help_out
    assert main(["--json"]) == 0
    payload = capsys.readouterr().out
    assert '"product": "azai"' in payload
    assert '"version": "0.3.1"' in payload


def test_cli_unknown_command_has_next_step(capsys) -> None:
    assert main(["bogus"]) == 2
    err = capsys.readouterr().err
    assert 'Unknown command "bogus"' in err
    assert "azai --help" in err
    assert main(["chat"]) == 2
    chat_err = capsys.readouterr().err
    assert "azai chat --message" in chat_err


def test_cli_seal_json_shape(capsys, tmp_path) -> None:
    assert main(["seal", "--json", "--data", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert '"sealed": true' in out
    assert '"ok": true' in out
