"""Loopback UI: GET / contains AZAI and Jeeves; /v1/models lists blend+providers."""

from __future__ import annotations

import json
import threading
import urllib.request

from azai.ui import LOOPBACK, make_server


def test_loopback_constant() -> None:
    assert "127.0.0.1" in LOOPBACK


def test_ui_get_root_contains_azai_and_jeeves(tmp_path) -> None:
    httpd = make_server("127.0.0.1", 0, data_dir=str(tmp_path))
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=3) as resp:
            assert resp.status == 200
            html = resp.read().decode("utf-8")
        assert "AZAI" in html
        assert "Jeeves" in html
        assert "Send" in html
        assert "Check this text" in html
        assert "Peace" in html and "Clarity" in html and "Service" in html
        assert "Sample prompt" in html
        assert "Simple" in html and "Advanced" in html
        assert "Import" in html and "Export" in html
        assert "cdnjs" not in html.lower()
        assert "unpkg" not in html.lower()
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/v1/models", timeout=3) as resp:
            models = json.loads(resp.read().decode("utf-8"))
        ids = [m["id"] for m in models["data"]]
        assert ids == ["blend", "gpt", "grok", "venice", "local"]
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/v1/health", timeout=3) as resp:
            health = json.loads(resp.read().decode("utf-8"))
        assert health["ok"] is True
        assert health["product"] == "azai"
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/openapi.json", timeout=3) as resp:
            spec = json.loads(resp.read().decode("utf-8"))
        assert spec["openapi"].startswith("3.")
        assert "/v1/chat/completions" in spec["paths"]
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_ui_chat_local_via_v1(tmp_path) -> None:
    httpd = make_server("127.0.0.1", 0, data_dir=str(tmp_path))
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        body = json.dumps(
            {"model": "local", "messages": [{"role": "user", "content": "hello from crawler"}]}
        ).encode("utf-8")
        req = urllib.request.Request(
            f"http://127.0.0.1:{port}/v1/chat/completions",
            data=body,
            headers={"Content-Type": "application/json", "Authorization": "Bearer dummy"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        assert payload["object"] == "chat.completion"
        assert "Jeeves" in payload["choices"][0]["message"]["content"]
    finally:
        httpd.shutdown()
        httpd.server_close()



def test_ui_import_export_and_lamb_check(tmp_path) -> None:
    httpd = make_server("127.0.0.1", 0, data_dir=str(tmp_path))
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        imp = json.dumps(
            {
                "filename": "chat.txt",
                "content": "user: hello import\nassistant: Jeeves imported this.",
            }
        ).encode("utf-8")
        req = urllib.request.Request(
            f"http://127.0.0.1:{port}/v1/import",
            data=imp,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        assert payload["ok"] is True
        assert payload["count"] == 2
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/v1/export?format=json", timeout=3) as resp:
            assert resp.status == 200
            exported = json.loads(resp.read().decode("utf-8"))
        assert any("hello import" in m["content"] for m in exported["messages"])
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/v1/export?format=md", timeout=3) as resp:
            md = resp.read().decode("utf-8")
        assert "hello import" in md
        lamb_body = json.dumps({"text": "Explain receipts in one sentence, please."}).encode("utf-8")
        req = urllib.request.Request(
            f"http://127.0.0.1:{port}/v1/lamb-check",
            data=lamb_body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            lamb = json.loads(resp.read().decode("utf-8"))
        assert lamb["overall"] == "PASS"
        assert lamb["peace"] == "PASS"
    finally:
        httpd.shutdown()
        httpd.server_close()
