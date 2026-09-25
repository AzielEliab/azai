"""Command-line interface for AZAI.

    azai
    azai ui
    azai chat --message "..."
    azai doctor

Human text is the default. Add --json for the same facts as a machine payload.
Loopback UI: `azai ui` prints Open http://127.0.0.1:8860/.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Sequence

from azai import __version__
from azai.config import DEFAULT_MODEL, LAN_RISK, LIMITATION, MODELS, UI_HOST, UI_PORT
from azai.debug import dlog
from azai.runtime import LambBlocked, Runtime, SealedError, models_payload, resolve_data_dir

_MODEL_BLURB = {
    "local": "Ollama on this machine (default)",
    "ollama": "Same local Ollama base",
    "blend": "gpt, grok, and venice, each answer labeled",
    "gpt": "OpenAI on this machine when OPENAI_API_KEY is set",
    "grok": "xAI on this machine when a Grok key is set",
    "venice": "Venice on this machine when VENICE_API_KEY is set",
}


def _welcome_text() -> str:
    return (
        f"AZAI {__version__} — ask a question on this machine.\n"
        "\n"
        "Jeeves answers through Ollama on this computer. "
        "Lamb Lens reads Service, Clarity, and Peace on each turn.\n"
        "\n"
        "Next:\n"
        "  azai ui        Open the app at http://127.0.0.1:8860/\n"
        "  azai doctor    Check that this install is ready\n"
        "  azai --help    List commands\n"
        "\n"
        "Author: Aziel Eliab\n"
    )


def _welcome_payload() -> dict:
    return {
        "product": "azai",
        "version": __version__,
        "author": "Aziel Eliab",
        "summary": "Ask a question on this machine. Jeeves answers through Ollama.",
        "ui": f"http://{UI_HOST}:{UI_PORT}/",
        "next": ["azai ui", "azai doctor", "azai --help"],
    }


def _help_text() -> str:
    return (
        f"azai {__version__} — ask a question on this machine\n"
        "\n"
        "usage: azai <command> [options]\n"
        "\n"
        "Start\n"
        "  (no command)    Welcome and the next step\n"
        "  ui              Open the local app at http://127.0.0.1:8860/\n"
        "  chat            Ask one question (--message)\n"
        "  doctor          Check that this install is ready\n"
        "\n"
        "Everyday\n"
        "  models          List models\n"
        "  ollama          See whether Ollama is running\n"
        "  version         Print the version\n"
        "\n"
        "Advanced\n"
        "  jeeves          Research-assistant contract\n"
        "  integrity       Lamb Lens readings: Service, Clarity, Peace\n"
        "  receipts        Show the receipt chain\n"
        "  seal            Lock chat\n"
        "  open            Unlock a sealed runtime\n"
        "  remember        Save a session note (needs --confirm)\n"
        "  import          Import a conversation (.txt or .json)\n"
        "  export          Export chat and receipts\n"
        "  serve           Same local server, for other software\n"
        "\n"
        "Add --json on a command for machine-readable output.\n"
        "  azai --json     Welcome as JSON\n"
        "\n"
        "Examples\n"
        "  azai ui\n"
        '  azai chat --message "Explain receipts in one sentence"\n'
        "  azai doctor\n"
        "  azai models --json\n"
        "\n"
        "Author: Aziel Eliab\n"
    )


class AzaiArgumentParser(argparse.ArgumentParser):
    def format_help(self) -> str:
        if self.prog == "azai":
            return _help_text()
        return super().format_help()

    def error(self, message: str) -> None:
        self.exit(2, _plain_error(self.prog, message))


def _plain_error(prog: str, message: str) -> str:
    low = message.lower()
    choice = re.search(r"invalid choice: '([^']+)'", message)
    if choice and (prog == "azai" or "argument cmd" in low):
        name = choice.group(1)
        return f'Unknown command "{name}". Try: azai ui   or   azai --help\n'
    if "required" in low and "--message" in message:
        return 'Chat needs a message.\nTry: azai chat --message "Hello"\n'
    if "required" in low and "--text" in message:
        return (
            "Remember needs the note, and --confirm to save it.\n"
            'Try: azai remember --text "note" --confirm\n'
        )
    if "required" in low and "path" in message:
        return "Import needs a file path.\nTry: azai import chat.txt\n"
    if "required: cmd" in low:
        return _welcome_text()
    unknown = re.search(r"unrecognized arguments?: (.+)$", message)
    if unknown:
        return f"Unknown option {unknown.group(1).strip()}.\nTry: {prog} --help\n"
    if "expected one argument" in low or "expected at least one argument" in low:
        return f"That option needs a value.\nTry: {prog} --help\n"
    if choice:
        return f'Unknown value "{choice.group(1)}".\nTry: {prog} --help\n'
    return f"{message}\nTry: {prog} --help\n"


def _build_parser() -> AzaiArgumentParser:
    parser = AzaiArgumentParser(
        prog="azai",
        description="Ask a question on this machine.",
    )
    sub = parser.add_subparsers(dest="cmd", metavar="<command>", parser_class=AzaiArgumentParser)

    p_ver = sub.add_parser("version", help="Print the version.")
    p_ver.add_argument("--json", action="store_true", dest="as_json")

    p_ui = sub.add_parser("ui", help="Open the local app at http://127.0.0.1:8860/.")
    p_ui.add_argument("--host", default=UI_HOST, help="Bind host (default 127.0.0.1).")
    p_ui.add_argument("--port", type=int, default=UI_PORT, help="Port (default 8860).")
    p_ui.add_argument("--data", default=None, help="Data directory (default ./AZAI_DATA or AZAI_DATA).")

    p_serve = sub.add_parser("serve", help="Same local server, for other software.")
    p_serve.add_argument("--host", default=UI_HOST)
    p_serve.add_argument("--port", type=int, default=UI_PORT)
    p_serve.add_argument("--data", default=None)

    p_chat = sub.add_parser("chat", help="Ask one question.")
    p_chat.add_argument("--model", default=DEFAULT_MODEL, choices=list(MODELS))
    p_chat.add_argument("--message", required=True)
    p_chat.add_argument("--data", default=None)
    p_chat.add_argument("--json", action="store_true", dest="as_json")
    p_chat.add_argument("--simple", action="store_true", help="Print the short view of the answer.")
    p_chat.add_argument(
        "--site-context",
        default=None,
        help="Optional JSON file of public record titles and summaries.",
    )

    p_jv = sub.add_parser("jeeves", help="Show the research-assistant contract.")
    p_jv.add_argument("--json", action="store_true", dest="as_json")

    p_models = sub.add_parser("models", help="List models.")
    p_models.add_argument("--json", action="store_true", dest="as_json")

    p_int = sub.add_parser("integrity", help="Show Service, Clarity, and Peace, plus the receipt chain.")
    p_int.add_argument("--text", default="", help="Optional text to run Lamb Lens on.")
    p_int.add_argument("--data", default=None)
    p_int.add_argument("--json", action="store_true", dest="as_json")

    p_seal = sub.add_parser("seal", help="Lock chat. Receipts stay readable.")
    p_seal.add_argument("--data", default=None)
    p_seal.add_argument("--json", action="store_true", dest="as_json")

    p_open = sub.add_parser("open", help="Unlock a sealed runtime.")
    p_open.add_argument("--data", default=None)
    p_open.add_argument("--json", action="store_true", dest="as_json")

    p_rec = sub.add_parser("receipts", help="Show the receipt chain.")
    p_rec.add_argument("--data", default=None)
    p_rec.add_argument("--json", action="store_true", dest="as_json")

    p_mem = sub.add_parser("remember", help="Save a session note. Needs --confirm.")
    p_mem.add_argument("--text", required=True)
    p_mem.add_argument("--confirm", action="store_true")
    p_mem.add_argument("--data", default=None)
    p_mem.add_argument("--json", action="store_true", dest="as_json")

    p_doc = sub.add_parser("doctor", help="Check that this install is ready.")
    p_doc.add_argument("--data", default=None)
    p_doc.add_argument("--json", action="store_true", dest="as_json")

    p_ol = sub.add_parser("ollama", help="See whether Ollama is running.")
    p_ol.add_argument("--json", action="store_true", dest="as_json")

    p_imp = sub.add_parser("import", help="Import a .txt or JSON conversation.")
    p_imp.add_argument("path", help="Path to .txt or .json")
    p_imp.add_argument("--data", default=None)
    p_imp.add_argument("--json", action="store_true", dest="as_json")

    p_exp = sub.add_parser("export", help="Export chat and receipts as JSON or Markdown.")
    p_exp.add_argument("--format", choices=("json", "md"), default="json")
    p_exp.add_argument("--out", default=None, help="Write to this path instead of stdout.")
    p_exp.add_argument("--data", default=None)

    return parser


def _rt(args) -> Runtime:
    return Runtime(data_dir=resolve_data_dir(getattr(args, "data", None)))


def _print_models(payload: dict) -> None:
    print("Models")
    labels = _MODEL_BLURB
    for row in payload.get("data") or []:
        mid = str(row.get("id") or "")
        blurb = labels.get(mid, mid)
        print(f"  {mid:<8} {blurb}")


def main(argv: Sequence[str] | None = None) -> int:
    raw = list(sys.argv[1:] if argv is None else argv)
    if raw == ["--json"]:
        print(json.dumps(_welcome_payload(), indent=2))
        return 0
    parser = _build_parser()
    try:
        args = parser.parse_args(raw)
    except SystemExit as exc:
        code = exc.code
        if code is None:
            return 0
        return code if isinstance(code, int) else 2

    if not getattr(args, "cmd", None):
        print(_welcome_text(), end="")
        return 0

    dlog("cli", cmd=args.cmd)

    if args.cmd == "version":
        if args.as_json:
            print(json.dumps({"product": "azai", "version": __version__, "author": "Aziel Eliab"}, indent=2))
        else:
            print(f"azai {__version__}")
        return 0

    if args.cmd in ("ui", "serve"):
        from azai.ui import serve

        host = args.host or UI_HOST
        if host not in {"127.0.0.1", "localhost", "::1"}:
            print(LAN_RISK, file=sys.stderr)
        try:
            serve(
                host=host,
                port=args.port,
                data_dir=str(resolve_data_dir(args.data)),
                emphasize_api=(args.cmd == "serve"),
            )
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            print("Try: azai ui", file=sys.stderr)
            return 2
        return 0

    if args.cmd == "models":
        payload = models_payload()
        if args.as_json:
            print(json.dumps(payload, indent=2))
        else:
            _print_models(payload)
        return 0

    if args.cmd == "integrity":
        rt = _rt(args)
        payload = rt.integrity(args.text)
        if args.as_json:
            print(json.dumps(payload, indent=2))
        else:
            receipts = payload.get("receipts") or {}
            chain = "healthy" if receipts.get("ok") else "needs a look"
            print(f"Lamb Lens  {payload['overall']}")
            print(f"Service  {payload['service']}")
            print(f"Clarity  {payload['clarity']}")
            print(f"Peace  {payload['peace']}")
            print(f"Runtime  {payload['runtime']}")
            print(f"Jeeves  {payload['jeeves']}")
            print(f"Receipts  {chain} ({receipts.get('count', 0)} on the chain)")
            print(payload["honest"])
        return 0

    if args.cmd == "seal":
        rt = _rt(args)
        payload = rt.seal()
        if args.as_json:
            print(json.dumps(payload, indent=2))
        else:
            print("Runtime sealed. Chat is locked. Receipts stay readable.")
            print("Next: azai open")
        return 0

    if args.cmd == "open":
        rt = _rt(args)
        payload = rt.open()
        if args.as_json:
            print(json.dumps(payload, indent=2))
        else:
            print("Runtime open. You can chat again.")
        return 0

    if args.cmd == "receipts":
        from azai.receipts import format_rows

        rt = _rt(args)
        rows = rt.receipts.read()
        if args.as_json:
            print(json.dumps({"receipts": rows, "verify": rt.receipts.verify()}, indent=2))
        else:
            print(f"Receipts  {len(rows)}")
            if rows:
                print(format_rows(rows))
            else:
                print("No receipts yet. Ask a question and one will be written.")
        return 0

    if args.cmd == "remember":
        rt = _rt(args)
        result = rt.remember(args.text, confirm=args.confirm)
        if args.as_json:
            print(json.dumps(result, indent=2))
        elif result.get("ok"):
            print(f"Saved for this session ({result.get('count')} notes).")
        else:
            print("That note was not saved. Memory writes wait for confirmation.", file=sys.stderr)
            print('Try: azai remember --text "note" --confirm', file=sys.stderr)
        return 0 if args.confirm else 2

    if args.cmd == "ollama":
        from azai.ollama import install_steps, probe

        payload = probe()
        if args.as_json:
            print(json.dumps(payload, indent=2))
            return 0
        url = payload.get("url") or "http://127.0.0.1:11434"
        model = payload.get("model") or "llama3.2"
        if payload.get("reachable") and payload.get("model_present"):
            print(f"Ollama is ready at {url} with model {model}.")
        elif payload.get("reachable"):
            print(f"Ollama is running at {url}. Model {model} is not pulled yet.")
            print(f"Next: ollama pull {model}")
            if payload.get("steps"):
                print()
                print(payload["steps"])
        else:
            print(f"Ollama is not running at {url}.")
            if payload.get("error"):
                print(payload["error"])
            print("Next: install Ollama, then run azai doctor.")
            print()
            print(payload.get("steps") or install_steps())
        return 0

    if args.cmd == "doctor":
        from azai.doctor import format_report, run

        payload = run(data_dir=args.data)
        if args.as_json:
            print(json.dumps(payload, indent=2))
        else:
            print(format_report(payload))
        return 0 if payload.get("ok") else 1

    if args.cmd == "import":
        path = Path(args.path)
        if not path.is_file():
            print(f"No file at {path}.", file=sys.stderr)
            print("Try: azai import chat.txt", file=sys.stderr)
            return 2
        text = path.read_text(encoding="utf-8")
        rt = _rt(args)
        try:
            result = rt.import_text(text, filename=path.name)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            print("Try: azai import chat.txt   or   azai import chat.json", file=sys.stderr)
            return 2
        if args.as_json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Imported {result['count']} messages from {path.name}.")
        return 0

    if args.cmd == "export":
        rt = _rt(args)
        body = rt.export_markdown() if args.format == "md" else rt.export_json()
        if args.out:
            Path(args.out).write_text(body, encoding="utf-8")
            print(args.out)
        else:
            print(body, end="" if body.endswith("\n") else "\n")
        return 0

    if args.cmd == "jeeves":
        from azai.jeeves import MODE_LABEL, REFUSALS, UPLOAD_GUIDANCE, mode_card

        payload = mode_card()
        if args.as_json:
            print(json.dumps(payload, indent=2))
        else:
            print(MODE_LABEL)
            print("Lamb Lens first — public Corpus posture; never the operator.")
            print("Jeeves is not sovereign.")
            print(f"Site: {payload['corpus_library']}")
            print("Jeeves cannot modify scores.")
            print()
            print("Hard refusals:")
            for line in REFUSALS:
                print(f"  - {line}")
            print()
            print(UPLOAD_GUIDANCE)
            print(payload["adaptive"])
            print(payload["how_corpus_calls"])
        return 0

    if args.cmd == "chat":
        site_context = None
        if getattr(args, "site_context", None):
            path = Path(args.site_context)
            if not path.is_file():
                print(f"No site-context file at {path}.", file=sys.stderr)
                print("Try: azai chat --message \"Hello\" --site-context records.json", file=sys.stderr)
                return 2
            try:
                site_context = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                print(f"That site-context file is not valid JSON ({exc}).", file=sys.stderr)
                print("Try: a JSON array of {\"title\", \"summary\"} objects.", file=sys.stderr)
                return 2
        rt = _rt(args)
        try:
            result = rt.chat(args.message, model=args.model, site_context=site_context)
        except SealedError as exc:
            print(str(exc), file=sys.stderr)
            print("Next: azai open", file=sys.stderr)
            return 3
        except LambBlocked as exc:
            lamb = exc.lamb or {}
            print(
                f"Lamb Lens stopped this message ({exc.stage}): overall {lamb.get('overall', 'FAIL')}.",
                file=sys.stderr,
            )
            print(
                f"Service {lamb.get('service', '—')}  "
                f"Clarity {lamb.get('clarity', '—')}  "
                f"Peace {lamb.get('peace', '—')}.",
                file=sys.stderr,
            )
            print('Next: rephrase the question, or run azai integrity --text "..."', file=sys.stderr)
            return 4
        if args.as_json:
            print(json.dumps(result, indent=2))
        else:
            print(result["simple"] if args.simple else result["content"])
        return 0

    print(LIMITATION, file=sys.stderr)
    print("Try: azai --help", file=sys.stderr)
    return 2
