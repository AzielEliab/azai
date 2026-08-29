"""This tree is AZAI only. Not merged into AZ-OS, GodLock, or siblings."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "azai"

FORBIDDEN_ROOTS = frozenset(
    {
        "forgereceipts",
        "zionpattern",
        "zion_pattern",
        "zion_pattern_solver",
        "decisiongate",
        "azos",
        "az_os",
        "veillock",
        "vibelock",
        "godlock",
        "codelock",
        "shadowlock",
        "temporallock",
        "staticclock",
        "miragegrid",
        "glossafilter",
        "clce",
        "azclce",
        "az_clce",
        "ark",
        "chronolock",
        "postking",
    }
)


def _root_of(name: str) -> str:
    return name.split(".")[0].lower().replace("-", "_")


def test_package_never_imports_siblings() -> None:
    import azai  # noqa: F401
    import azai.cli  # noqa: F401
    import azai.ui  # noqa: F401
    import azai.runtime  # noqa: F401

    for name in list(sys.modules):
        assert _root_of(name) not in FORBIDDEN_ROOTS


def test_source_imports_isolated() -> None:
    for py in PKG.rglob("*.py"):
        tree = ast.parse(py.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert _root_of(alias.name) not in FORBIDDEN_ROOTS
            elif isinstance(node, ast.ImportFrom) and node.module:
                assert _root_of(node.module) not in FORBIDDEN_ROOTS


def test_not_inside_sibling_products() -> None:
    text = str(ROOT)
    assert text.endswith("/azai") or text.endswith("\\azai") or "/azai" in text
    assert not (ROOT / "azos").exists()
    assert not (ROOT / "godlock").exists()
    assert not (ROOT / "forgereceipts").exists()
    assert (PKG / "lamb.py").is_file()
    assert (PKG / "web" / "index.html").is_file()


def test_worker_isolated() -> None:
    toml = (ROOT / "workers" / "download-tracker" / "wrangler.toml").read_text(encoding="utf-8")
    assert 'name = "azai-download-tracker"' in toml
    assert 'account_id = "ac575a9b822bea2bed97d0ab73aed238"' in toml
    assert 'binding = "DOWNLOADS"' in toml
    assert "/download" in toml
    src = (ROOT / "workers" / "download-tracker" / "src" / "index.js").read_text(encoding="utf-8")
    assert 'const PROJECT = "azai"' in src
    assert "azai-0.1.0.tar.gz" in src
    assert "azai|__total__" in src or 'PROJECT + "|__total__"' in src
    assert "Isolated counter" in src
    assert "env.ASSETS.fetch" in src
    assert "private, no-store" in src
    assert "/v1/lamb-check" in src
    lowered = src.lower().replace("-", "").replace("_", "").replace(" ", "")
    assert "forgereceipts" not in lowered
    assert "godlock" not in lowered
    engine = (ROOT / "workers" / "download-tracker" / "src" / "engine.js").read_text(encoding="utf-8")
    assert "ignore previous instructions" in engine.lower()
    assert "not a proxy" in engine.lower() or "not a provider proxy" in engine.lower()
    assert "peace" in engine.lower() and "clarity" in engine.lower()


def test_readme_honest_scope() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    low = readme.lower()
    assert "not a new foundation model" in low
    assert "not a kernel" in low
    assert "jeeves is not sovereign" in low
    assert "blank key" in low
    assert "Forks are welcome" in readme
    assert "azai-download-tracker.vibelock.workers.dev" in readme
    assert "127.0.0.1:8860" in readme
    assert "OPENAI_BASE_URL" in readme
    assert "standalone" in low
