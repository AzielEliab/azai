# AZAI

Ask a question on this machine. Jeeves answers from the local core. No Ollama and no model weights are required. Lamb Lens reads Service, Clarity, and Peace.

**Author:** Aziel Eliab
**Version:** 0.3.1
**License:** [Apache-2.0](LICENSE)

## Start

1. **Install**

```bash
python -m venv .venv && source .venv/bin/activate && pip install -e .
```

2. **Open the app**

```bash
azai ui
```

3. **Go to** [http://127.0.0.1:8860](http://127.0.0.1:8860) and press **Send**.

`azai` with no command prints this same next step. `azai doctor` checks the install. `azai --help` lists commands. Add `--json` when another program needs machine output.

See [RUN.txt](RUN.txt) for the same three steps. Spec: [docs/whitepaper.md](docs/whitepaper.md). Contribute: [CONTRIBUTING.md](CONTRIBUTING.md).

**Forks are welcome and always allowed.**

## Counted download

```bash
curl -fsSL https://azai-download-tracker.vibelock.workers.dev/install.sh | bash
```

The script downloads the counted tarball (User-Agent `Mozilla/5.0`), creates a virtualenv, and runs `pip install -e .`. It does not require Ollama and does not pull model weights. `scripts/setup-ollama.sh` is optional. Then run `azai ui`. `azai doctor` is green without Ollama.

- Home: [https://azai-download-tracker.vibelock.workers.dev/](https://azai-download-tracker.vibelock.workers.dev/)
- Tarball: [azai-0.3.1.tar.gz](https://azai-download-tracker.vibelock.workers.dev/download?asset=azai-0.3.1.tar.gz)
- Live count JSON: [https://azai-download-tracker.vibelock.workers.dev/stats](https://azai-download-tracker.vibelock.workers.dev/stats)
- OpenAPI: [https://azai-download-tracker.vibelock.workers.dev/openapi.json](https://azai-download-tracker.vibelock.workers.dev/openapi.json)
- Skill: [https://azai-download-tracker.vibelock.workers.dev/v1/skill](https://azai-download-tracker.vibelock.workers.dev/v1/skill)
- Suite mesh proxy: [https://azai-download-tracker.vibelock.workers.dev/v1/mesh](https://azai-download-tracker.vibelock.workers.dev/v1/mesh) — default OFF; QNM live / locked / isolated; QNS-CD-1.0 hub cite (photon QNS1 packet transfer; not a public qnsd proxy)
- One-click install: [https://azai-download-tracker.vibelock.workers.dev/install.sh](https://azai-download-tracker.vibelock.workers.dev/install.sh)
- GitHub: [https://github.com/AzielEliab/azai](https://github.com/AzielEliab/azai)

Isolated counter: Worker `azai-download-tracker`, KV `AZAI_DOWNLOADS`. The Worker serves the gzip itself (HTTP 200, no 302 to GitHub). `/v1` does not increment downloads.

Other software on this machine:

```bash
export OPENAI_BASE_URL=http://127.0.0.1:8860/v1
export OPENAI_API_KEY=dummy
```

---

## Honest scope

- **True local AI, standalone local core.** Default `model=local` is the
  constitution and guide plus light adaptive session notes and `site_context`.
  It does not require Ollama or model weights, and it does not probe Ollama
  as the success path. No OpenAI key is required for local.
- **Ollama is an optional slot.** Use it only with `AZAI_BACKEND=ollama` or
  `model=ollama`. `scripts/setup-ollama.sh` is optional and is not part of
  install. It may pull a GGUF only when you run it on purpose.
- **Not a new foundation model.** AZAI is a local runtime / shell,
  not a kernel. JEEVES is the ethics/assistant layer inside it and does
  **not** pretend to be GPT.
- **JEEVES is not sovereign.** **Ask Jeeves** is the research-assistant
  mode for the public Corpus/Library. Lamb Lens first — Service → Clarity →
  Peace; public Corpus posture; never the operator. Jeeves cannot modify
  scores (same rights as a normal user). This is a constitutional gate,
  not a proof of ethics.
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
- Loopback UI, no telemetry. Optional paid GPT/Grok/Venice calls happen
  on the operator's local `azai serve`. Hosted `/v1` is lamb-check ONLY
  and never spends the author's paid keys and never proxies chat to
  GPT/Grok/Venice.

Motto: *Jeeves speaks inside the shell. Lamb Lens governs above the
shell. Receipts witness what the shell permits.*

## Local core + optional Ollama slot + optional paid providers

JEEVES wraps every turn. Paid keys stay on this machine and never go
through the hosted Worker. The default core does not require Ollama.

| id | env | URL | what it is |
|----|-----|-----|----------------|
| local | none | constitution and guide in-process | **default** — no weights, no Ollama probe |
| ollama | `AZAI_BACKEND=ollama` or `model=ollama`; `AZAI_OLLAMA_URL` / `AZAI_OLLAMA_MODEL` | `http://127.0.0.1:11434/v1/chat/completions` | optional slot — **no paid key** |
| gpt | `OPENAI_API_KEY` | `https://api.openai.com/v1/chat/completions` | `gpt-4o-mini` (`AZAI_GPT_MODEL`) |
| grok | `XAI_API_KEY` or `GROK_API_KEY` | `https://api.x.ai/v1/chat/completions` | `grok-3-mini` (alt: `grok-2-latest` via `AZAI_GROK_MODEL`) |
| venice | `VENICE_API_KEY` | `https://api.venice.ai/api/v1/chat/completions` | `llama-3.3-70b` (`AZAI_VENICE_MODEL`) |

Optional Ollama slot (not printed as a doctor failure; `azai ollama` prints the steps):

```bash
bash scripts/setup-ollama.sh    # optional; may pull a model only because you ran it
# then: AZAI_BACKEND=ollama   or   model=ollama
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
azai doctor
```

`azai doctor` is green without Ollama. `scripts/setup-ollama.sh` is optional
and is not part of install. Run it only when you want the Ollama slot.

Optional extra `[voice]` is a marker only — engines are not vendored.

## CLI

People get short text. Add `--json` on a command when a program needs the machine payload. HTTP JSON paths are unchanged.

```bash
azai                    # welcome and the next step
azai ui                 # prints: Open http://127.0.0.1:8860/
azai chat --message "Explain receipts in one sentence"
azai doctor
azai models
azai ollama
azai version

azai jeeves             # research-assistant contract
azai integrity
azai receipts
azai seal
azai open
azai remember --text "note" --confirm
azai import chat.json   # or .txt
azai export --format json --out chat.json
azai export --format md --out chat.md
azai serve              # same server, for other software
azai doctor --json
```

`azai ui --host 0.0.0.0` binds on-site LAN. **Risk:** anyone who can
reach the port can use the local core and, if present, the optional Ollama slot or spend the
operator's GPT/Grok/Venice keys. Prefer 127.0.0.1.

`AZAI_DEBUG=1` prints local stderr traces. Keys are never logged. No telemetry.

POST bodies larger than 1 MiB are rejected (413).

## UI

`azai ui` prints `Open http://127.0.0.1:8860/` and binds **127.0.0.1:8860** by default.

The first screen has one message box and **Send**. **Check this text** runs Lamb Lens and does not call a model. **Sample prompt** fills an example. Service, Clarity, and Peace show as a short status line.

**Advanced** stays collapsed. It holds the model list, Simple and full answers, seal / open, receipts, import, export, and About. Light and dark follow the system. Focus uses a gold ring. The page fits a 390px-wide screen.

Self-contained CSS, no CDN, no telemetry. Keys are never shown.

## Backend for other software (on site)

Same loopback server. Other crawlers / local tools:

```
OPENAI_BASE_URL=http://127.0.0.1:8860/v1
OPENAI_API_KEY=dummy
```

| Method | Path | Notes |
|--------|------|--------|
| GET | `/v1/models` | local, ollama, blend, gpt, grok, venice |
| POST | `/v1/chat/completions` | `messages[]`, `model`, optional `site_context` (public titles/summaries) |
| GET | `/v1/jeeves` | Ask Jeeves research-assistant contract |
| GET | `/v1/health` | runtime + which keys present |
| GET | `/openapi.json` | OpenAPI 3.1 |
| GET | `/v1/receipts` | append-only chain |
| POST | `/v1/seal` | seal runtime |
| POST | `/v1/open` | open runtime |
| POST | `/v1/lamb-check` | `{text}` — no provider call |
| POST | `/v1/import` | `{content, filename}` `.txt` or JSON |
| GET | `/v1/export?format=json\|md` | chat + receipts |
| GET | `/v1/session` | current transcript |

## Ask Jeeves (Corpus / Library)

Site assistants — especially [www.azielcorpuslibrary.net](https://www.azielcorpuslibrary.net/) —
call **local** AZAI. Hosted Worker `/v1` is lamb-check ONLY (plus
`GET /v1/jeeves` for the contract). Jeeves is not GPT and is not sovereign.

1. Search the library: `GET https://www.azielcorpuslibrary.net/v1/search?q=`
2. POST public titles/summaries to local Ask Jeeves:

```bash
azai jeeves
curl -s http://127.0.0.1:8860/v1/chat/completions \
  -H 'content-type: application/json' \
  -d '{"model":"local","messages":[{"role":"user","content":"What does the library say?"}],"site_context":[{"title":"Florence","summary":"Public record summary"}]}'
```

`site_context` is an adaptive hook as the library grows. Persist nothing
secret. Jeeves cannot modify scores. Upload is out of band: files still
run full SPRE×CLCE×PhysLing + Bayesian ingest — no score shortcut.

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
`DOWNLOADS`. GET `/download` **serves** `azai-0.3.1.tar.gz` (does not 302
to GitHub) with HTTP 200 and `Content-Type: application/gzip`. See
[workers/download-tracker/README.md](workers/download-tracker/README.md).

Hosted `/v1` is **lamb-check ONLY** (plus a protocol mirror of health and
models). It is not a chat proxy and does not hold paid keys.

- `GET https://azai-download-tracker.vibelock.workers.dev/v1/health`
- `GET https://azai-download-tracker.vibelock.workers.dev/v1/models`
- `GET https://azai-download-tracker.vibelock.workers.dev/v1/skill`
- `GET https://azai-download-tracker.vibelock.workers.dev/v1/jeeves` (Ask Jeeves contract; not chat)
- `GET https://azai-download-tracker.vibelock.workers.dev/v1/mesh` (suite mesh PROXY; default OFF; QNM live|locked|isolated; QNS-CD-1.0 hub cite — not a Softwares-tab product, not a public qnsd proxy)
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

## Use with AI clients

Public engines accept any MCP/OpenAPI-capable assistant, including ChatGPT (GPT Actions / OpenAI), Grok (xAI), Venice, Claude (Anthropic), Cursor (MCP), Glama (MCP), Perplexity, Microsoft Copilot / Bing, Google Gemini / Vertex, Mistral, Meta AI, Apple Intelligence surfaces, Amazon Q tooling, DuckAssist, You.com, Cohere, and other MCP/OpenAPI-capable assistants.

Catalog OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json
Catalog MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`. Suite mesh `/v1/mesh/*` PROXY via `AZIEL_RUNTIME` (default OFF; QNM-BUILD-1.0 live|locked|isolated; no Node Gate). QNS-CD-1.0 is a hub cite / Worker mesh cross-map only (photon QNS1 packet transfer; local qnsd in [qnm-node](https://github.com/AzielEliab/qnm-node); runtime cites in [aziel-runtime](https://github.com/AzielEliab/aziel-runtime)). Not a Softwares-tab product. Not a public qnsd proxy. Catalog MCP `mesh_*` + FragGate `slug=mesh`.
This Worker skill: https://azai-download-tracker.vibelock.workers.dev/v1/skill
This Worker OpenAPI: https://azai-download-tracker.vibelock.workers.dev/openapi.json

ChatGPT: GPT Actions (no auth). Grok: import the catalog or Worker OpenAPI as a custom tool. Venice: HTTP tools. Claude, Cursor, Glama, and other MCP clients: catalog MCP. Always send `User-Agent: Mozilla/5.0`.

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
