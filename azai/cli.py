"""Command-line interface for AZAI.

    azai version
    azai ui
    azai serve
    azai chat --model local --message "..."
    azai jeeves
    azai models
    azai ollama
    azai integrity
    azai seal / azai open
    azai receipts
    azai doctor
    azai import PATH
    azai export --format json|md

Loopback UI: `azai ui` at http://127.0.0.1:8860.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from azai import __version__
from azai.config import DEFAULT_MODEL, LAN_RISK, LIMITATION, MODELS, UI_HOST, UI_PORT
from azai.debug import dlog
from azai.runtime import LambBlocked, Runtime, SealedError, models_payload, resolve_data_dir


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="azai",
        description=(
            "AZAI (Aziel Artificial Intelligence) — true local AI on an Ollama base "
            "with JEEVES as the Ask Jeeves research assistant (ethics/assistant "
            "layer; not sovereign). Lamb Lens first — public Corpus posture; "
            "never the operator. OpenAI-compatible local API at "
            "http://127.0.0.1:8860/v1. Hosted /v1 is lamb-check only, never a "
            "paid-key proxy."
        ),
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("version", help="Print package version.")

    p_ui = sub.add_parser("ui", help="Serve the local AZAI UI + OpenAI-compat API on 127.0.0.1:8860.")
    p_ui.add_argument("--host", default=UI_HOST, help="Bind host (default 127.0.0.1). Non-loopback is on-site LAN risk.")
    p_ui.add_argument("--port", type=int, default=UI_PORT, help="Port (default 8860).")
    p_ui.add_argument("--data", default=None, help="Data directory (default ./AZAI_DATA or AZAI_DATA).")

    p_serve = sub.add_parser("serve", help="Same as ui; emphasize the OpenAI-compatible API.")
    p_serve.add_argument("--host", default=UI_HOST)
    p_serve.add_argument("--port", type=int, default=UI_PORT)
    p_serve.add_argument("--data", default=None)

    p_chat = sub.add_parser(
        "chat",
        help="One-shot Ask Jeeves research-assistant turn (Lamb Lens + JEEVES; not sovereign).",
    )
    p_chat.add_argument("--model", default=DEFAULT_MODEL, choices=list(MODELS))
    p_chat.add_argument("--message", required=True)
    p_chat.add_argument("--data", default=None)
    p_chat.add_argument("--json", action="store_true", dest="as_json")
    p_chat.add_argument("--simple", action="store_true", help="Print the simple (6th-grader) view of blend output.")
    p_chat.add_argument(
        "--site-context",
        default=None,
        help="Optional JSON file of retrieved public record titles/summaries (adaptive hook). Persist nothing secret.",
    )

    p_jv = sub.add_parser(
        "jeeves",
        help="Print Ask Jeeves research-assistant mode (Corpus/Library; not sovereign).",
    )
    p_jv.add_argument("--json", action="store_true", dest="as_json")

    p_models = sub.add_parser("models", help="List local, ollama, blend, gpt, grok, venice.")
    p_models.add_argument("--json", action="store_true", dest="as_json")

    p_int = sub.add_parser("integrity", help="Peace / clarity / service + receipt chain.")
    p_int.add_argument("--text", default="", help="Optional text to run Lamb Lens on.")
    p_int.add_argument("--data", default=None)
    p_int.add_argument("--json", action="store_true", dest="as_json")

    p_seal = sub.add_parser("seal", help="Seal runtime: Jeeves locked, receipts readable.")
    p_seal.add_argument("--data", default=None)
    p_open = sub.add_parser("open", help="Open a sealed runtime.")
    p_open.add_argument("--data", default=None)

    p_rec = sub.add_parser("receipts", help="Print the append-only receipt chain.")
    p_rec.add_argument("--data", default=None)
    p_rec.add_argument("--json", action="store_true", dest="as_json")

    p_mem = sub.add_parser("remember", help="Session-only memory. Requires --confirm.")
    p_mem.add_argument("--text", required=True)
    p_mem.add_argument("--confirm", action="store_true")
    p_mem.add_argument("--data", default=None)

    p_doc = sub.add_parser("doctor", help="Local self-check: Lamb, JEEVES, Ollama steps, loopback, no Worker keys.")
    p_doc.add_argument("--data", default=None)
    p_doc.add_argument("--json", action="store_true", dest="as_json")

    p_ol = sub.add_parser("ollama", help="Show local Ollama base status and exact install steps.")
    p_ol.add_argument("--json", action="store_true", dest="as_json")

    p_imp = sub.add_parser("import", help="Import a .txt or JSON conversation (replaces session transcript).")
    p_imp.add_argument("path", help="Path to .txt or .json")
    p_imp.add_argument("--data", default=None)
    p_imp.add_argument("--json", action="store_true", dest="as_json")

    p_exp = sub.add_parser("export", help="Export chat + receipts as JSON or Markdown.")
    p_exp.add_argument("--format", choices=("json", "md"), default="json")
    p_exp.add_argument("--out", default=None, help="Write to this path instead of stdout.")
    p_exp.add_argument("--data", default=None)

    return parser


def _rt(args) -> Runtime:
    return Runtime(data_dir=resolve_data_dir(getattr(args, "data", None)))


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    dlog("cli", cmd=args.cmd)

    if args.cmd == "version":
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
            return 2
        return 0

    if args.cmd == "models":
        payload = models_payload()
        if args.as_json:
            print(json.dumps(payload, indent=2))
        else:
            print(" ".join(m["id"] for m in payload["data"]))
        return 0

    if args.cmd == "integrity":
        rt = _rt(args)
        payload = rt.integrity(args.text)
        if args.as_json:
            print(json.dumps(payload, indent=2))
        else:
            print(
                f"Lamb {payload['overall']}  peace={payload['peace']}  "
                f"clarity={payload['clarity']}  service={payload['service']}"
            )
            print(f"Runtime {payload['runtime']}  Jeeves {payload['jeeves']}")
            print(f"Receipts ok={payload['receipts']['ok']} count={payload['receipts']['count']}")
            print(payload["honest"])
        return 0

    if args.cmd == "seal":
        rt = _rt(args)
        print(json.dumps(rt.seal(), indent=2))
        return 0

    if args.cmd == "open":
        rt = _rt(args)
        print(json.dumps(rt.open(), indent=2))
        return 0

    if args.cmd == "receipts":
        from azai.receipts import format_rows

        rt = _rt(args)
        rows = rt.receipts.read()
        if args.as_json:
            print(json.dumps({"receipts": rows, "verify": rt.receipts.verify()}, indent=2))
        else:
            print(format_rows(rows))
        return 0

    if args.cmd == "remember":
        rt = _rt(args)
        print(json.dumps(rt.remember(args.text, confirm=args.confirm), indent=2))
        return 0 if args.confirm else 2

    if args.cmd == "ollama":
        from azai.ollama import install_steps, probe

        payload = probe()
        if args.as_json:
            print(json.dumps(payload, indent=2))
        else:
            print(
                f"Ollama reachable={payload.get('reachable')}  "
                f"url={payload.get('url')}  model={payload.get('model')}  "
                f"model_present={payload.get('model_present')}"
            )
            if payload.get("error"):
                print(payload["error"])
            if payload.get("steps"):
                print()
                print(payload["steps"])
            elif not payload.get("reachable"):
                print()
                print(install_steps())
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
            print(f"import not found: {path}", file=sys.stderr)
            return 2
        text = path.read_text(encoding="utf-8")
        rt = _rt(args)
        try:
            result = rt.import_text(text, filename=path.name)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        if args.as_json:
            print(json.dumps(result, indent=2))
        else:
            print(f"imported {result['count']} messages from {path.name}")
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
            print(f"{MODE_LABEL}  (not sovereign; not GPT; Ollama base)")
            print("Lamb Lens first — public Corpus posture; never the operator.")
            print(f"Site: {payload['corpus_library']}")
            print("Hard refusals:")
            for line in REFUSALS:
                print(f"  - {line}")
            print(UPLOAD_GUIDANCE)
            print(payload["adaptive"])
            print(payload["how_corpus_calls"])
        return 0

    if args.cmd == "chat":
        site_context = None
        if getattr(args, "site_context", None):
            path = Path(args.site_context)
            if not path.is_file():
                print(f"site-context not found: {path}", file=sys.stderr)
                return 2
            try:
                site_context = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                print(f"site-context invalid JSON: {exc}", file=sys.stderr)
                return 2
        rt = _rt(args)
        try:
            result = rt.chat(args.message, model=args.model, site_context=site_context)
        except SealedError as exc:
            print(str(exc), file=sys.stderr)
            return 3
        except LambBlocked as exc:
            print(f"Lamb Lens FAIL ({exc.stage}): {exc.lamb}", file=sys.stderr)
            return 4
        if args.as_json:
            print(json.dumps(result, indent=2))
        else:
            print(result["simple"] if args.simple else result["content"])
        return 0

    print(LIMITATION, file=sys.stderr)
    return 2
