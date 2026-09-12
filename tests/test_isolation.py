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
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'name = "azai"' in pyproject
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
    assert "azai-0.3.1.tar.gz" in src
    assert "true local AI" in src or "true local ai" in src.lower()
    assert "ollama" in src.lower()
    assert "azai|__total__" in src or 'PROJECT + "|__total__"' in src
    assert "Isolated counter" in src
    assert "env.ASSETS.fetch" in src
    assert "private, no-store" in src
    assert "/v1/lamb-check" in src
    assert "/v1/jeeves" in src
    assert "Ask Jeeves" in src
    assert "azielcorpuslibrary.net" in src
    idx = src.find('url.pathname === "/count"')
    assert idx != -1
    count_block = src[idx : idx + 500]
    assert "project:" in count_block or "project :" in count_block
    assert "views" in count_block
    assert "downloads" in count_block
    assert "total" in count_block
    worker_readme = (ROOT / "workers" / "download-tracker" / "README.md").read_text(
        encoding="utf-8"
    )
    assert "{project, views, downloads, total}" in worker_readme
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
    assert "ollama" in low
    assert "true local" in low
    assert "blank key" in low
    assert "Forks are welcome" in readme
    assert "azai-download-tracker.vibelock.workers.dev" in readme
    assert "127.0.0.1:8860" in readme
    assert "OPENAI_BASE_URL" in readme
    assert "standalone" in low
    assert "ask jeeves" in low
    assert "azielcorpuslibrary.net" in low
    assert "cannot modify scores" in low or "cannot modify scores" in readme.lower()
    assert "## Use with Grok / ChatGPT / Venice" not in readme
    assert "## Use with AI clients" in readme
    for name in PUBLIC_ENGINE_CLIENTS:
        assert name in readme, name
    assert "paid GPT/Grok/Venice" in readme
    assert "Lamb check does not call" in readme
    assert "GPT/Grok/Venice" in readme


BRAND_MARK = (
    '<div class="brandrow"><img class="brandmark" src="/sigil.png" '
    'width="40" height="40" alt="" decoding="async"></div>'
)


def test_worker_brand_mark_is_wordless_rose_star() -> None:
    src = (ROOT / "workers" / "download-tracker" / "src" / "index.js").read_text(
        encoding="utf-8"
    )
    assert src.count(BRAND_MARK) == 2
    assert ".brandrow" in src and ".brandmark" in src
    sigil = ROOT / "workers" / "download-tracker" / "public" / "sigil.png"
    assert sigil.is_file()
    size = sigil.stat().st_size
    assert 70_000 <= size <= 80_000, size
    assert sigil.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
    # Public mark has no words (empty alt). Do not scrub verify
    # contracts that require Everblooming header/skill strings.
    mark_alts = [
        line for line in src.splitlines() if "class=\"brandmark\"" in line
    ]
    assert mark_alts
    for line in mark_alts:
        assert 'alt=""' in line
        assert "everblooming sigil" not in line.lower()
        assert "Everblooming" not in line


PUBLIC_ENGINE_CLIENTS = (
    "ChatGPT (GPT Actions / OpenAI)",
    "Grok (xAI)",
    "Claude (Anthropic)",
    "Cursor (MCP)",
    "Glama (MCP)",
    "Perplexity",
    "Microsoft Copilot / Bing",
    "Google Gemini / Vertex",
    "Mistral",
    "Meta AI",
    "Apple Intelligence",
    "Amazon Q",
    "DuckAssist",
    "You.com",
    "Cohere",
    "MCP/OpenAPI-capable",
)


def test_skill_and_worker_full_client_list() -> None:
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    worker = (ROOT / "workers" / "download-tracker" / "src" / "index.js").read_text(
        encoding="utf-8"
    )
    for text in (skill, worker):
        assert "Author: **Aziel Eliab**" in text or "Author Aziel Eliab" in text
        for name in PUBLIC_ENGINE_CLIENTS:
            assert name in text, name
        assert "Grok: import OpenAPI as a custom tool. ChatGPT: GPT Actions. Venice: HTTP tools." not in text
