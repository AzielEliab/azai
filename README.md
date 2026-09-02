# AZAI (Aziel Artificial Intelligence)

**Local OpenAI-compatible runtime** that blends GPT, Grok, and Venice
under the Lamb Lens. **Jeeves** is the instrument inside the shell.
Jeeves is not sovereign. Hub is a blank key: it does not interpret meaning.

**Author:** Aziel Eliab
**Date:** 2026
**Version:** 0.2.0
**License:** [Apache-2.0](LICENSE)

> Not a new foundation model, not a kernel, not a worm, not IP-blocking
> malware, not a VPN. Paid GPT/Grok/Venice calls happen on the operator's
> local `azai serve`. The hosted Worker `/v1` is **lamb-check ONLY**,
> never a paid-key proxy.

See the spec: [docs/whitepaper.md](docs/whitepaper.md). Source papers:
[docs/source/](docs/source/). How to contribute: [CONTRIBUTING.md](CONTRIBUTING.md).

**Forks are welcome and always allowed.**

## Quick start (3 steps)

1. **Install**

```bash
python -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"
```

2. **Run**

```bash
azai ui
```

3. **Open** [http://127.0.0.1:8860](http://127.0.0.1:8860) — one chat box, **Send**, **Check this text**. Loopback only. No CDN, no telemetry.

That is the whole start. Type a question or press **Sample prompt**. Peace / Clarity / Service chips show the Lamb Lens. Simple view is the default (6th-grader easy). Advanced view shows blend labels and receipts.

Point other software / crawlers at this machine:

```bash
export OPENAI_BASE_URL=http://127.0.0.1:8860/v1
export OPENAI_API_KEY=dummy
```

Counted download: [https://azai-download-tracker.vibelock.workers.dev/](https://azai-download-tracker.vibelock.workers.dev/)

Direct tarball (also counted): [azai-0.2.0.tar.gz](https://azai-download-tracker.vibelock.workers.dev/download?asset=azai-0.2.0.tar.gz)

GitHub: [https://github.com/AzielEliab/azai](https://github.com/AzielEliab/azai)

Self-check (no network): `azai doctor`

---

## Honest scope

- **Not a new foundation model.** AZAI is a local runtime / shell.
  Jeeves is the instrument inside it. Without API keys, a local stub
  still runs (Lamb Lens + receipts + constitution) and does **not**
  pretend to be GPT.
- **Jeeves is not sovereign.** Lamb Lens (peace, clarity, service)
  gates every turn. This is a constitutional gate, not a proof of ethics.
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

## Providers (keys from env, never files in git)

| id | env | URL | default model |
|----|-----|-----|----------------|
| gpt | `OPENAI_API_KEY` | `https://api.openai.com/v1/chat/completions` | `gpt-4o-mini` (`AZAI_GPT_MODEL`) |
| grok | `XAI_API_KEY` or `GROK_API_KEY` | `https://api.x.ai/v1/chat/completions` | `grok-3-mini` (alt: `grok-2-latest` via `AZAI_GROK_MODEL`) |
| venice | `VENICE_API_KEY` | `https://api.venice.ai/api/v1/chat/completions` | `llama-3.3-70b` (`AZAI_VENICE_MODEL`) |

Venice alt URL (if the primary 404s): `https://api.venice.ai/v1/chat/completions`
(`AZAI_VENICE_URL`). Timeouts, no retry storms. Lamb Lens runs on the
user prompt **before** any provider call and on the merged output **after**.

## Install

Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Optional extra `[voice]` is a marker only — engines are not vendored.

## CLI

```bash
azai version
azai ui                 # 127.0.0.1:8860 loopback only
azai serve              # same as ui, emphasize OpenAI-compat API
azai chat --model blend --message "..."
azai models
azai integrity
azai seal
azai open
azai receipts
azai doctor             # local self-check (Lamb fixtures, loopback, no Worker keys)
azai import chat.json   # or .txt
azai export --format json --out chat.json
azai export --format md --out chat.md
```

`azai ui --host 0.0.0.0` binds on-site LAN. **Risk:** anyone who can
reach the port can spend the operator's GPT/Grok/Venice keys. Prefer
127.0.0.1.

`AZAI_DEBUG=1` prints local stderr traces. Keys are never logged. No telemetry.

POST bodies larger than 1 MiB are rejected (413).

## UI

`azai ui` binds **127.0.0.1:8860** only by default. Black / gold.

- One chat box, **Send**, **Check this text** (Lamb only — no provider call)
- Peace / Clarity / Service chips
- Sample prompt
- Simple view (default) and Advanced view (blend labels + receipts)
- Import `.txt` / JSON conversation; export chat + receipts as JSON or Markdown
- Top status: Lamb / Integrity / Runtime / Jeeves / Providers (which
  keys are present, never the keys)
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
| GET | `/v1/models` | blend, gpt, grok, venice, local |
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
`DOWNLOADS`. GET `/download` **serves** `azai-0.2.0.tar.gz` (does not 302
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
azai/                 library (lamb, receipts, jeeves, providers, runtime, cli, ui, doctor, exchange)
azai/web/             loopback UI
tests/                pytest (no network) + fixtures/
docs/whitepaper.md    spec (honest scope)
docs/source/          papers
mobile/               Flutter companion (`flutter create .`)
workers/download-tracker/   Cloudflare Worker
```

## License

Apache-2.0. See [LICENSE](LICENSE).

Forks are welcome and always allowed.
