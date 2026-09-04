"""Hardening: loopback, max body, no telemetry, no keys in Worker, not a proxy."""

from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request
from pathlib import Path

from azai.config import MAX_BODY_BYTES, TELEMETRY_FORBIDDEN, UI_HOST
from azai.ui import LOOPBACK, make_server

ROOT = Path(__file__).resolve().parents[1]


def test_default_bind_is_loopback() -> None:
    assert UI_HOST == "127.0.0.1"
    assert "127.0.0.1" in LOOPBACK


def test_web_has_no_telemetry_and_no_cdn() -> None:
    web = ROOT / "azai" / "web"
    blob = ""
    for p in web.iterdir():
        blob += p.read_text(encoding="utf-8").lower() + "\n"
    for needle in TELEMETRY_FORBIDDEN:
        assert needle.lower() not in blob
    assert "cdnjs" not in blob
    assert "unpkg" not in blob
    assert "googleapis" not in blob


def test_max_body_413(tmp_path) -> None:
    httpd = make_server("127.0.0.1", 0, data_dir=str(tmp_path))
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        huge = b'{"text":"' + (b"x" * (MAX_BODY_BYTES + 50)) + b'"}'
        req = urllib.request.Request(
            f"http://127.0.0.1:{port}/v1/lamb-check",
            data=huge,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            urllib.request.urlopen(req, timeout=5)
            raise AssertionError("expected 413")
        except urllib.error.HTTPError as exc:
            assert exc.code == 413
            payload = json.loads(exc.read().decode("utf-8"))
            assert payload["error"] == "payload too large"
            assert payload["max"] == MAX_BODY_BYTES
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_worker_has_no_keys_and_is_not_a_proxy() -> None:
    src = ""
    for p in (ROOT / "workers" / "download-tracker" / "src").glob("*.js"):
        src += p.read_text(encoding="utf-8") + "\n"
    low = src.lower()
    assert "env.OPENAI_API_KEY" not in src
    assert "env.XAI_API_KEY" not in src
    assert "env.VENICE_API_KEY" not in src
    assert "api.openai.com" not in low
    assert "api.x.ai" not in low
    assert "api.venice.ai" not in low
    assert "sk-" not in src
    assert "lamb-check" in low
    assert "not a proxy" in low or "lamb-check only" in low
    assert "azai-0.3.1.tar.gz" in src
    assert "1048576" in src or "MAX_BODY" in src
    assert "provider_proxy: false" in src or "provider_proxy:false" in src.replace(" ", "")
