"""Command-line interface for AZAI.

    azai version
    azai ui
    azai serve
    azai chat --model blend --message "..."
    azai models
    azai integrity
    azai seal / azai open
    azai receipts

Loopback UI: `azai ui` at http://127.0.0.1:8860.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Sequence

from azai import __version__
from azai.config import LAN_RISK, LIMITATION, MODELS, UI_HOST, UI_PORT
from azai.runtime import LambBlocked, Runtime, SealedError, models_payload, resolve_data_dir


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="azai",
        description=(
            "AZAI (Aziel Artificial Intelligence) — local OpenAI-compatible runtime "
            "that blends GPT, Grok, and Venice under the Lamb Lens. "
            "Jeeves is the instrument inside the shell and is not sovereign. "
            "Loopback UI: `azai ui` at http://127.0.0.1:8860."
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

    p_chat = sub.add_parser("chat", help="One-shot chat through Lamb Lens.")
    p_chat.add_argument("--model", default="blend", choices=list(MODELS))
    p_chat.add_argument("--message", required=True)
    p_chat.add_argument("--data", default=None)
    p_chat.add_argument("--json", action="store_true", dest="as_json")

    p_models = sub.add_parser("models", help="List blend, gpt, grok, venice, local.")
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

    return parser


def _rt(args) -> Runtime:
    return Runtime(data_dir=resolve_data_dir(getattr(args, "data", None)))


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

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

    if args.cmd == "chat":
        rt = _rt(args)
        try:
            result = rt.chat(args.message, model=args.model)
        except SealedError as exc:
            print(str(exc), file=sys.stderr)
            return 3
        except LambBlocked as exc:
            print(f"Lamb Lens FAIL ({exc.stage}): {exc.lamb}", file=sys.stderr)
            return 4
        if args.as_json:
            print(json.dumps(result, indent=2))
        else:
            print(result["content"])
        return 0

    print(LIMITATION, file=sys.stderr)
    return 2
