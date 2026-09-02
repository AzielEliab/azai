"""Local AZAI UI + OpenAI-compatible HTTP.

Default bind 127.0.0.1:8860 (loopback). Optional --host for on-site LAN
(documented risk: spends the operator's keys). Self-contained CSS, no CDN,
no telemetry. Max POST body 1 MiB.
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import files
from typing import Any
from urllib.parse import parse_qs, urlparse

from azai import __version__
from azai.config import LAN_RISK, LIMITATION, MAX_BODY_BYTES, MODELS, MOTTO, SAMPLE_PROMPT, UI_HOST, UI_PORT
from azai.debug import dlog, enabled as debug_enabled, status_payload
from azai.lamb import check_text
from azai.providers import provider_status
from azai.runtime import Runtime, models_payload

LOOPBACK = frozenset({"127.0.0.1", "localhost", "::1"})
WEB = files("azai") / "web"
MIME = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
}


def openapi_spec(origin: str = "http://127.0.0.1:8860") -> dict[str, Any]:
    return {
        "openapi": "3.1.0",
        "info": {
            "title": "AZAI local runtime",
            "version": __version__,
            "summary": "OpenAI-compatible local blend of GPT, Grok, and Venice under Lamb Lens.",
            "description": LIMITATION + " Point other software at OPENAI_BASE_URL=" + origin + "/v1 with a dummy key.",
            "license": {"name": "Apache-2.0", "identifier": "Apache-2.0"},
            "contact": {"name": "Aziel Eliab", "url": "https://github.com/AzielEliab/azai"},
        },
        "servers": [{"url": origin}],
        "paths": {
            "/v1/health": {
                "get": {
                    "operationId": "azai_health",
                    "summary": "Liveness. Providers present (never keys). Runtime OPEN/SEALED.",
                    "responses": {"200": {"description": "ok"}},
                }
            },
            "/v1/models": {
                "get": {
                    "operationId": "azai_models",
                    "summary": "Lists blend, gpt, grok, venice, local.",
                    "responses": {"200": {"description": "OpenAI-compat model list"}},
                }
            },
            "/v1/chat/completions": {
                "post": {
                    "operationId": "azai_chat",
                    "summary": "OpenAI-compat chat. Stream is accepted and returned as non-stream.",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "model": {"type": "string", "enum": list(MODELS)},
                                        "messages": {"type": "array"},
                                        "stream": {"type": "boolean"},
                                    },
                                }
                            }
                        },
                    },
                    "responses": {"200": {"description": "chat.completion"}},
                }
            },
            "/v1/receipts": {
                "get": {
                    "operationId": "azai_receipts",
                    "summary": "Append-only receipt chain.",
                    "responses": {"200": {"description": "receipts"}},
                }
            },
            "/v1/seal": {
                "post": {
                    "operationId": "azai_seal",
                    "summary": "Seal runtime. Jeeves locked.",
                    "responses": {"200": {"description": "sealed"}},
                }
            },
            "/v1/open": {
                "post": {
                    "operationId": "azai_open",
                    "summary": "Open a sealed runtime.",
                    "responses": {"200": {"description": "open"}},
                }
            },
            "/v1/integrity": {
                "get": {
                    "operationId": "azai_integrity",
                    "summary": "Peace / clarity / service + receipt chain health.",
                    "responses": {"200": {"description": "integrity"}},
                }
            },
            "/v1/lamb-check": {
                "post": {
                    "operationId": "azai_lamb_check",
                    "summary": "Run Lamb Lens on {text}. No provider call.",
                    "requestBody": {
                        "required": True,
                        "content": {"application/json": {"schema": {"type": "object"}}},
                    },
                    "responses": {"200": {"description": "lamb"}},
                }
            },
            "/v1/import": {
                "post": {
                    "operationId": "azai_import",
                    "summary": "Import a .txt or JSON conversation. Replaces session transcript.",
                    "responses": {"200": {"description": "imported"}},
                }
            },
            "/v1/export": {
                "get": {
                    "operationId": "azai_export",
                    "summary": "Export chat + receipts as JSON or Markdown (?format=json|md).",
                    "responses": {"200": {"description": "export"}},
                }
            },
            "/v1/session": {
                "get": {
                    "operationId": "azai_session",
                    "summary": "Current session transcript.",
                    "responses": {"200": {"description": "session"}},
                }
            },
        },
    }


class _State:
    def __init__(self, data_dir: str) -> None:
        self.runtime = Runtime(data_dir=data_dir)


def _web_bytes(name: str) -> bytes:
    return (WEB / name).read_bytes()


def make_server(
    host: str = UI_HOST,
    port: int = UI_PORT,
    data_dir: str | None = None,
) -> ThreadingHTTPServer:
    from azai.runtime import resolve_data_dir

    state = _State(str(resolve_data_dir(data_dir)))

    class Bound(Handler):
        pass

    Bound.state = state
    Bound.bind_host = host
    return ThreadingHTTPServer((host, port), Bound)


def serve(
    host: str = UI_HOST,
    port: int = UI_PORT,
    data_dir: str | None = None,
    emphasize_api: bool = False,
) -> None:
    httpd = make_server(host, port, data_dir=data_dir)
    bound_host, bound_port = httpd.server_address[:2]
    extra = "OpenAI-compat at /v1 (OPENAI_BASE_URL=http://%s:%s/v1)." % (bound_host, bound_port)
    if host not in LOOPBACK:
        extra += " " + LAN_RISK
    kind = "AZAI serve" if emphasize_api else "AZAI UI"
    print(
        f"{kind} http://{bound_host}:{bound_port} "
        f"(Jeeves inside the shell; Lamb Lens above; {extra} no telemetry)"
    )
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        httpd.server_close()


class Handler(BaseHTTPRequestHandler):
    state: _State
    bind_host: str = UI_HOST

    def log_message(self, fmt: str, *args) -> None:  # noqa: A003
        if debug_enabled():
            dlog("http", msg=(fmt % args))
        return

    def _send(self, status: int, body: bytes, content_type: str, extra: dict[str, str] | None = None) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Filename")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        if extra:
            for k, v in extra.items():
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status: int, payload: Any) -> None:
        raw = json.dumps(payload, indent=2).encode("utf-8")
        self._send(status, raw, "application/json; charset=utf-8")

    def _read_raw(self) -> bytes | None:
        try:
            n = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            n = 0
        if n > MAX_BODY_BYTES:
            self._json(413, {"error": "payload too large", "max": MAX_BODY_BYTES})
            return None
        raw = self.rfile.read(n) if n else b""
        if len(raw) > MAX_BODY_BYTES:
            self._json(413, {"error": "payload too large", "max": MAX_BODY_BYTES})
            return None
        return raw

    def _read_json(self) -> dict[str, Any] | None:
        raw = self._read_raw()
        if raw is None:
            return None
        if not raw:
            return {}
        try:
            data = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self._json(400, {"error": "invalid json"})
            return None
        return data if isinstance(data, dict) else {}

    def do_OPTIONS(self) -> None:  # noqa: N802
        self._send(204, b"", "text/plain")

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)
        dlog("GET", path=path)
        if path in ("/", "/index.html"):
            self._send(200, _web_bytes("index.html"), MIME[".html"])
            return
        if path == "/style.css":
            self._send(200, _web_bytes("style.css"), MIME[".css"])
            return
        if path == "/app.js":
            self._send(200, _web_bytes("app.js"), MIME[".js"])
            return
        if path == "/openapi.json":
            host, port = self.server.server_address[:2]
            self._json(200, openapi_spec(f"http://{host}:{port}"))
            return
        if path == "/v1/health" or path == "/api/status":
            integ = self.state.runtime.integrity()
            status = provider_status()
            payload = {
                "ok": True,
                "product": "azai",
                "version": __version__,
                "instrument": "Jeeves",
                "runtime": integ["runtime"],
                "jeeves": integ["jeeves"],
                "lamb": integ["lamb"],
                "integrity": integ["overall"],
                "providers": {k: {"present": v["present"]} for k, v in status.items()},
                "limitation": LIMITATION,
                "motto": MOTTO,
                "sample_prompt": SAMPLE_PROMPT,
                "max_body": MAX_BODY_BYTES,
                "hosted_v1": "lamb-check-only",
                "openai_base_url": f"http://{self.server.server_address[0]}:{self.server.server_address[1]}/v1",
            }
            payload.update(status_payload())
            self._json(200, payload)
            return
        if path == "/v1/models":
            self._json(200, models_payload())
            return
        if path == "/v1/receipts" or path == "/api/receipts":
            self._json(
                200,
                {
                    "receipts": self.state.runtime.receipts.read(),
                    "verify": self.state.runtime.receipts.verify(),
                },
            )
            return
        if path == "/v1/integrity" or path == "/api/integrity":
            self._json(200, self.state.runtime.integrity())
            return
        if path in ("/v1/session", "/api/session"):
            self._json(200, {"messages": self.state.runtime.transcript()})
            return
        if path in ("/v1/export", "/api/export"):
            fmt = (qs.get("format") or ["json"])[0].lower()
            if fmt in ("md", "markdown"):
                body = self.state.runtime.export_markdown().encode("utf-8")
                self._send(
                    200,
                    body,
                    "text/markdown; charset=utf-8",
                    extra={"Content-Disposition": 'attachment; filename="azai-chat.md"'},
                )
                return
            body = self.state.runtime.export_json().encode("utf-8")
            self._send(
                200,
                body,
                "application/json; charset=utf-8",
                extra={"Content-Disposition": 'attachment; filename="azai-chat.json"'},
            )
            return
        self._json(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        dlog("POST", path=path)
        body = self._read_json()
        if body is None:
            return
        if path in ("/v1/chat/completions", "/api/chat"):
            if path == "/api/chat" and "messages" not in body:
                body = {
                    "model": body.get("model") or "blend",
                    "messages": [{"role": "user", "content": body.get("message") or body.get("prompt") or ""}],
                }
            payload = self.state.runtime.openai_completion(body)
            status = 200
            if payload.get("error") and payload["error"].get("type") == "sealed":
                status = 423
            elif payload.get("error") and payload["error"].get("type") == "lamb_fail":
                status = 400
            self._json(status, payload)
            return
        if path in ("/v1/seal", "/api/seal"):
            self._json(200, self.state.runtime.seal(reason=str(body.get("reason") or "ui")))
            return
        if path in ("/v1/open", "/api/open"):
            self._json(200, self.state.runtime.open(reason=str(body.get("reason") or "ui")))
            return
        if path in ("/v1/lamb-check", "/v1/lamb_check", "/api/lamb-check"):
            text = str(body.get("text") or body.get("prompt") or "")
            self._json(200, check_text(text))
            return
        if path in ("/v1/import", "/api/import"):
            content = str(body.get("content") or body.get("text") or "")
            filename = str(body.get("filename") or body.get("name") or "import.txt")
            try:
                result = self.state.runtime.import_text(content, filename=filename)
            except ValueError as exc:
                self._json(400, {"ok": False, "error": str(exc)})
                return
            self._json(200, result)
            return
        if path in ("/v1/memory", "/api/memory"):
            self._json(
                200,
                self.state.runtime.remember(
                    str(body.get("text") or ""),
                    confirm=bool(body.get("confirm")),
                ),
            )
            return
        self._json(404, {"error": "not found"})
