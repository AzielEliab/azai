"""Import .txt/JSON and export JSON + Markdown. Roundtrip."""

from pathlib import Path

from azai.cli import main
from azai.exchange import parse_conversation, parse_txt, simple_text, to_markdown
from azai.runtime import Runtime

ROOT = Path(__file__).resolve().parent
FIX = ROOT / "fixtures"


def test_parse_txt_prefixed() -> None:
    msgs = parse_txt((FIX / "conversation.txt").read_text(encoding="utf-8"))
    assert msgs[0]["role"] == "user"
    assert "receipt" in msgs[0]["content"].lower()
    assert msgs[1]["role"] == "assistant"


def test_parse_json_azai_export() -> None:
    msgs = parse_conversation((FIX / "conversation.json").read_text(encoding="utf-8"), "chat.json")
    assert msgs[0]["content"] == "hello from json"
    assert msgs[1]["role"] == "assistant"


def test_parse_plain_txt_paragraphs() -> None:
    msgs = parse_txt("Hello there.\n\nSecond thought.")
    assert len(msgs) == 2
    assert msgs[0]["role"] == "user"
    assert msgs[1]["content"] == "Second thought."


def test_runtime_import_export_json_roundtrip(tmp_path) -> None:
    a = Runtime(data_dir=tmp_path / "a")
    a.chat("hello roundtrip", model="local")
    blob = a.export_json()
    b = Runtime(data_dir=tmp_path / "b")
    b.import_text(blob, filename="chat.json")
    again = b.export_bundle()
    user_msgs = [m["content"] for m in again["messages"] if m["role"] == "user"]
    assert "hello roundtrip" in user_msgs
    assert again["product"] == "azai"
    assert again["jeeves_sovereign"] is False
    md = b.export_markdown()
    assert "# AZAI conversation" in md
    assert "hello roundtrip" in md
    assert "## Receipts" in md


def test_txt_import_then_json_export_roundtrip(tmp_path) -> None:
    rt = Runtime(data_dir=tmp_path)
    raw = (FIX / "conversation.txt").read_text(encoding="utf-8")
    result = rt.import_text(raw, filename="conversation.txt")
    assert result["ok"] is True
    assert result["count"] >= 2
    bundle = rt.export_bundle()
    assert any("receipt" in m["content"].lower() for m in bundle["messages"])
    md = to_markdown(bundle)
    assert "You" in md or "you" in md.lower()


def test_cli_import_export_roundtrip(tmp_path, capsys) -> None:
    src = FIX / "conversation.json"
    data = str(tmp_path / "data")
    assert main(["import", str(src), "--data", data]) == 0
    out_json = tmp_path / "out.json"
    out_md = tmp_path / "out.md"
    assert main(["export", "--format", "json", "--out", str(out_json), "--data", data]) == 0
    assert main(["export", "--format", "md", "--out", str(out_md), "--data", data]) == 0
    body = out_json.read_text(encoding="utf-8")
    assert "hello from json" in body
    assert "Jeeves" in out_md.read_text(encoding="utf-8")


def test_simple_text_hides_blend_labels() -> None:
    raw = "[gpt]\nfrom-gpt\n\n[grok]\nfrom-grok\n\n[venice]\nfrom-venice\n\n[synthesis]\nThree-source blend."
    simple = simple_text(raw)
    assert "[gpt]" not in simple
    assert "Three-source blend." in simple
