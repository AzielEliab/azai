# AZAI (Aziel Artificial Intelligence)

**True local AI** on an **Ollama** base. **JEEVES** is the ethics/assistant
layer inside the shell. JEEVES is not sovereign — Lamb Lens and the
operator govern it. OpenAI-compatible local API. **Not a hosted paid-key
proxy.** Hub is a blank key: it does not interpret meaning.

**Author:** Aziel Eliab
**Date:** 2026
**Version:** 0.3.0
**License:** [Apache-2.0](LICENSE)

> Not a new foundation model, not a kernel, not a worm, not IP-blocking
> malware, not a VPN. The local base is Ollama on this machine. Optional
> paid GPT/Grok/Venice calls happen only on the operator's local
> `azai serve`. The hosted Worker `/v1` is **lamb-check ONLY**,
> never a paid-key proxy.

See the spec: [docs/whitepaper.md](docs/whitepaper.md). Source papers:
[docs/source/](docs/source/). How to contribute: [CONTRIBUTING.md](CONTRIBUTING.md).

**Forks are welcome and always allowed.**


## One-click install

```bash
curl -fsSL https://azai-download-tracker.vibelock.workers.dev/install.sh | bash
```

The script curls the **counted** tarball from this project's Worker
(`/download`, User-Agent `Mozilla/5.0`), extracts, makes a venv, and
`pip install -e .`, then `scripts/setup-ollama.sh` (installs/uses Ollama
and pulls `llama3.2` unless `AZAI_OLLAMA_MODEL` is set). Then run `azai ui`.

Or tap **Download** / **One-click install** on the Worker homepage
(a 6th-grader can tap it):
https://azai-download-tracker.vibelock.workers.dev/

## Counted download (Cloudflare Worker)

**This is the counted download.** GitHub releases exist as a mirror.
The Worker serves the gzip itself (HTTP 200, no 302 to GitHub).

# → [https://azai-download-tracker.vibelock.workers.dev/](https://azai-download-tracker.vibelock.workers.dev/) ←

Direct tarball (also counted):
[azai-0.3.0.tar.gz](https://azai-download-tracker.vibelock.workers.dev/download?asset=azai-0.3.0.tar.gz)

- Live count JSON: [https://azai-download-tracker.vibelock.workers.dev/stats](https://azai-download-tracker.vibelock.workers.dev/stats)
- OpenAPI: [https://azai-download-tracker.vibelock.workers.dev/openapi.json](https://azai-download-tracker.vibelock.workers.dev/openapi.json)
- Skill: [https://azai-download-tracker.vibelock.workers.dev/v1/skill](https://azai-download-tracker.vibelock.workers.dev/v1/skill)
- One-click install: [https://azai-download-tracker.vibelock.workers.dev/install.sh](https://azai-download-tracker.vibelock.workers.dev/install.sh)
- GitHub: [https://github.com/AzielEliab/azai](https://github.com/AzielEliab/azai)

Isolated counter: Worker `azai-download-tracker`, KV `AZAI_DOWNLOADS`. Not mixed with any other product. `/v1` does not increment downloads.


## Quick start (3 steps)

1. **Install**

```bash
python -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"
```

2. **Run**

```bash
azai ui
```

3. **Open** [http://127.0.0.1:8860](http://127.0.0.1:8860) — one chat box, **Send**, **Check this text**. Loopback only. No CDN, no telemetry. Default model is **local** (Ollama + JEEVES).

That is the whole start. Type a question or press **Sample prompt**. Peace / Clarity / Service chips show the Lamb Lens. Simple view is the default (6th-grader easy). Advanced view shows blend labels and receipts.

Point other software / crawlers at this machine:

```bash
export OPENAI_BASE_URL=http://127.0.0.1:8860/v1
export OPENAI_API_KEY=dummy
```

Counted download: [https://azai-download-tracker.vibelock.workers.dev/](https://azai-download-tracker.vibelock.workers.dev/)

Direct tarball (also counted): [azai-0.3.0.tar.gz](https://azai-download-tracker.vibelock.workers.dev/download?asset=azai-0.3.0.tar.gz)

GitHub: [https://github.com/AzielEliab/azai](https://github.com/AzielEliab/azai)

Self-check: `azai doctor` (loopback Ollama probe is advisory; prints exact install steps if the base is missing)

---

## Honest scope

- **True local AI on an Ollama base.** Default `model=local` talks to
  Ollama at `http://127.0.0.1:11434` through JEEVES. Default model tag:
  `llama3.2` (`AZAI_OLLAMA_MODEL`). No OpenAI key is required for local.
- **Not a new foundation model.** AZAI is a local runtime / shell.
  JEEVES is the ethics/assistant layer inside it. Without Ollama, a
  constitution stub still runs (Lamb Lens + receipts) and does **not**
  pretend to be GPT.
- **JEEVES is not sovereign.** Lamb Lens (peace, clarity, service) and
  the operator govern every turn. This is a constitutional gate, not a
  proof of ethics.
- **Hub is a blank key.** It does not interpret meaning. Removing the
  Hub leaves modules functional, only isolated.
- **Blend is visible.** When `model=blend`, responses are labeled
  `[gpt]` / `[grok]` / `[venice]` then a short `[synthesis]`. Never hide
  which model said what. Simple view shows the synthesis; Advanced shows
  the labels and receipts.
- **Voice** is optional extra `[voice]`. MVP is text. Push-to-talk only;
  no wake word; no passive recording; voice does not execute commands.
  Whisper/Piper models are **not** vendored in the tarball.
- **Memory writes require explicit confirm.** Session-only by default.
- **Do not treat Phoenix / "static block IP routing" as implemented.**
  This package does not block IPs, spread, or take over a remote OS.
- Standalone from AZ-OS, GodLock, ForgeReceipts.
- Loopback UI, no telemetry. Hosted `/v1` is lamb-check ONLY and never
  spends the author's paid keys and never proxies chat to GPT/Grok/Venice.

Motto: *Jeeves speaks inside the shell. Lamb Lens governs above the
shell. Receipts witness what the shell permits.*

## Local base (Ollama) + optional paid providers

JEEVES wraps every turn. Paid keys stay on this machine and never go
through the hosted Worker.

| id | env | URL | default model |
|----|-----|-----|----------------|
| local / ollama | `AZAI_OLLAMA_URL` / `AZAI_OLLAMA_MODEL` | `http://127.0.0.1:11434/v1/chat/completions` | `llama3.2` — **no paid key** |
| gpt | `OPENAI_API_KEY` | `https://api.openai.com/v1/chat/completions` | `gpt-4o-mini` (`AZAI_GPT_MODEL`) |
| grok | `XAI_API_KEY` or `GROK_API_KEY` | `https://api.x.ai/v1/chat/completions` | `grok-3-mini` (alt: `grok-2-latest` via `AZAI_GROK_MODEL`) |
| venice | `VENICE_API_KEY` | `https://api.venice.ai/api/v1/chat/completions` | `llama-3.3-70b` (`AZAI_VENICE_MODEL`) |

Exact Ollama steps (also printed by `azai ollama` and `azai doctor`):

```bash
curl -fsSL https://ollama.com/install.sh | sh   # or https://ollama.com/download
ollama serve                                      # 127.0.0.1:11434
ollama pull llama3.2                              # or llama3.2:1b on a small machine
azai doctor
```

Venice alt URL (if the primary 404s): `https://api.venice.ai/v1/chat/completions`
(`AZAI_VENICE_URL`). Timeouts, no retry storms. Lamb Lens runs on the
user prompt **before** any provider call and on the merged output **after**.

## Install

Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
bash scripts/setup-ollama.sh
```

`scripts/setup-ollama.sh` installs or reuses Ollama, starts `ollama serve`
if needed, and pulls `llama3.2` (override with `AZAI_OLLAMA_MODEL`).
If install cannot finish (no sudo, no network), it prints the exact
steps above and leaves AZAI usable with the JEEVES constitution stub.

Optional extra `[voice]` is a marker only — engines are not vendored.

## CLI

```bash
azai version
azai ui                 # 127.0.0.1:8860 loopback only
azai serve              # same as ui, emphasize OpenAI-compat API
azai chat --model local --message "..."
azai models
azai ollama             # local base status + exact install steps
azai integrity
azai seal
azai open
azai receipts
azai doctor             # Lamb, JEEVES, Ollama steps, loopback, no Worker keys
azai import chat.json   # or .txt
azai export --format json --out chat.json
azai export --format md --out chat.md
```

`azai ui --host 0.0.0.0` binds on-site LAN. **Risk:** anyone who can
reach the port can use the local Ollama base and, if present, spend the
operator's GPT/Grok/Venice keys. Prefer 127.0.0.1.

`AZAI_DEBUG=1` prints local stderr traces. Keys are never logged. No telemetry.

POST bodies larger than 1 MiB are rejected (413).

## UI

`azai ui` binds **127.0.0.1:8860** only by default. Black / gold.

- One chat box, **Send**, **Check this text** (Lamb only — no provider call)
- Peace / Clarity / Service chips
- Sample prompt
- Simple view (default) and Advanced view (blend labels + receipts)
- Import `.txt` / JSON conversation; export chat + receipts as JSON or Markdown
- Top status: Lamb / Integrity / Runtime / Jeeves / Ollama / Providers
  (which keys are present, never the keys)
- Seal Runtime (Advanced)

Self-contained CSS, no CDN, no telemetry.

## Backend for other software (on site)

Same loopback server. Other crawlers / local tools:

```
OPENAI_BASE_URL=http://127.0.0.1:8860/v1
OPENAI_API_KEY=dummy
```

| Method | Path | Notes |
|--------|------|--------|
| GET | `/v1/models` | local, ollama, blend, gpt, grok, venice |
| POST | `/v1/chat/completions` | `messages[]`, `model`, `stream` accepted (returned non-stream) |
| GET | `/v1/health` | runtime + which keys present |
| GET | `/openapi.json` | OpenAPI 3.1 |
| GET | `/v1/receipts` | append-only chain |
| POST | `/v1/seal` | seal runtime |
| POST | `/v1/open` | open runtime |
| POST | `/v1/lamb-check` | `{text}` — no provider call |
| POST | `/v1/import` | `{content, filename}` `.txt` or JSON |
| GET | `/v1/export?format=json\|md` | chat + receipts |
| GET | `/v1/session` | current transcript |

## Receipts

Append-only JSONL under `AZAI_DATA` (cwd/`AZAI_DATA`, or `AZAI_DATA` env).
Hash chain is TemporalLock-lite: `sha256(prev_hash + canonical payload)`.
`azai receipts`.

## iPhone & Android

Flutter sources: [`mobile/`](mobile/). Application id `com.azieeliab.azai`.
Companion only: ask / read receipts / integrity / seal / **export share**.
Constitutional edits are blocked. Dark gold. Offline against a local AZAI server.

```bash
cd mobile
flutter create --org com.azieeliab --project-name azai .
flutter pub get
flutter run
```

The `android/` and `ios/` folders in this tree are skeleton READMEs until you
run `flutter create .` (this machine has no Flutter SDK on PATH).

Counted desktop download: [https://azai-download-tracker.vibelock.workers.dev/](https://azai-download-tracker.vibelock.workers.dev/)

**Forks are welcome and always allowed.**

## Tests

```bash
pip install -e ".[dev]"
python -m pytest -q
```

Tests never call the network. pytest is the dev extra. Coverage includes
Lamb fixtures, `azai doctor`, and import/export roundtrip.

## Worker

Isolated download counter for this project only. Worker
`azai-download-tracker`, project `azai`, KV `AZAI_DOWNLOADS` bound as
`DOWNLOADS`. GET `/download` **serves** `azai-0.3.0.tar.gz` (does not 302
to GitHub) with HTTP 200 and `Content-Type: application/gzip`. See
[workers/download-tracker/README.md](workers/download-tracker/README.md).

Hosted `/v1` is **lamb-check ONLY** (plus a protocol mirror of health and
models). It is not a chat proxy and does not hold paid keys.

- `GET https://azai-download-tracker.vibelock.workers.dev/v1/health`
- `GET https://azai-download-tracker.vibelock.workers.dev/v1/models`
- `POST https://azai-download-tracker.vibelock.workers.dev/v1/lamb-check` `{text}`
- OpenAPI 3.1: https://azai-download-tracker.vibelock.workers.dev/openapi.json
- Help: https://azai-download-tracker.vibelock.workers.dev/ai

`/v1` does not increment the download counter. Lamb check does not call
GPT/Grok/Venice. POST bodies over 1 MiB return 413.

One-URL catalog: https://aziel-runtime.vibelock.workers.dev/openapi.json

## Layout

```
azai/                 library (lamb, receipts, jeeves, ollama, providers, runtime, cli, ui, doctor, exchange)
scripts/              setup-ollama.sh, pack-tarball.sh
azai/web/             loopback UI
tests/                pytest (no network) + fixtures/
docs/whitepaper.md    spec (honest scope)
docs/source/          papers
mobile/               Flutter companion (`flutter create .`)
workers/download-tracker/   Cloudflare Worker
```

## Use with Grok / ChatGPT / Venice

Catalog OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json
Catalog MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`
This Worker skill: https://azai-download-tracker.vibelock.workers.dev/v1/skill
This Worker OpenAPI: https://azai-download-tracker.vibelock.workers.dev/openapi.json

Grok: import the catalog or Worker OpenAPI as a custom tool. ChatGPT: GPT Actions (no auth). Venice: HTTP tools. Always send `User-Agent: Mozilla/5.0`.

## Cite this

Aziel Eliab. AZAI. https://github.com/AzielEliab/azai. https://azai-download-tracker.vibelock.workers.dev.

- Catalog: https://aziel-runtime.vibelock.workers.dev/
- Worker homepage: https://azai-download-tracker.vibelock.workers.dev/
- Counted download (gzip HTTP 200, no 302): https://azai-download-tracker.vibelock.workers.dev/download
- GitHub: https://github.com/AzielEliab/azai
- Citation JSON: https://azai-download-tracker.vibelock.workers.dev/cite.json

## License

Apache-2.0. See [LICENSE](LICENSE).

Forks are welcome and always allowed.
