---
name: AZAI
description: Use when calling AZAI hosted /v1 or installing the local true-AI package. Ask Jeeves research assistant for the public Corpus/Library. Author Aziel Eliab.
---

# AZAI

AZAI packages a **true local AI** stack on an **Ollama** base with **JEEVES**.
OpenAI-compatible local API. Not a hosted paid-key proxy. Author: **Aziel Eliab**.

**THIS IS:** true local AI. Ollama is the local model base. JEEVES is the
ethics/assistant layer inside the shell (**Ask Jeeves** research assistant).
JEEVES is not sovereign — Lamb Lens first; public Corpus posture; never the
operator.

**THIS IS NOT:** a new foundation model, a kernel, a worm, IP-blocking malware,
a VPN, a hosted paid-key proxy, GPT, or a sovereign agent.

Always send `User-Agent: Mozilla/5.0`. Cloudflare Workers may 403 an empty agent.

## Call these URLs

- Worker OpenAPI: https://azai-download-tracker.vibelock.workers.dev/openapi.json
- Catalog OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json
- MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`
- Live skill (this markdown): `GET https://azai-download-tracker.vibelock.workers.dev/v1/skill`

Ops (do **not** increment downloads or views):

- `GET /v1/health` — liveness
- `GET /v1/skill` — this file
- `GET /v1/jeeves` — Ask Jeeves research-assistant contract (not chat)
- Product POSTs listed in OpenAPI

Hosted `/v1` is **lamb-check ONLY**. It does not run Ollama and does not
spend paid keys. Jeeves chat runs on local `azai serve`.

Grok: import OpenAPI as a custom tool. ChatGPT: GPT Actions. Venice: HTTP tools.

## Ask Jeeves (Corpus / Library research assistant)

**Ask Jeeves** is the documented research-assistant mode of JEEVES for site
assistants, especially https://www.azielcorpuslibrary.net/. It is not GPT
and is not sovereign. Ollama is the local base. JEEVES is the ethics/assistant
layer. **Lamb Lens first** — public Corpus posture; never the operator.

Hard refusals (in `azai/jeeves.py` SYSTEM):

- Never reveal operator account info, credentials, admin hashes, hidden routes
- Never advise actions that risk the corpus (wipe, score forge, quarantine bypass)
- **Cannot modify scores** — research assistant only; same rights as a normal user

Adaptive learning hook: pass optional retrieved public record titles/summaries
as `site_context` so answers improve as the library grows. Persist nothing secret.

Upload is **out of band**. Jeeves may *guide* upload but files still run full
SPRE×CLCE×PhysLing + Bayesian ingest — no score shortcut.

How the Corpus/Library calls AZAI/Jeeves:

1. Search the library: `GET https://www.azielcorpuslibrary.net/v1/search?q=`
2. POST those public titles/summaries to **local** AZAI (not hosted chat):

```bash
curl -s http://127.0.0.1:8860/v1/chat/completions \
  -H 'content-type: application/json' \
  -d '{
    "model": "local",
    "messages": [{"role": "user", "content": "What does the library say about Florence?"}],
    "site_context": [
      {"title": "Florence", "summary": "Public record summary"}
    ]
  }'
```

Read the contract: `GET http://127.0.0.1:8860/v1/jeeves` (local) or
`GET https://azai-download-tracker.vibelock.workers.dev/v1/jeeves` (hosted
card only). Hosted AZAI `/v1` does **not** run Jeeves chat.

## Example

```bash
curl -s -A 'Mozilla/5.0' https://azai-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' https://azai-download-tracker.vibelock.workers.dev/v1/skill
curl -s -A 'Mozilla/5.0' https://azai-download-tracker.vibelock.workers.dev/v1/jeeves
```

## Local (after one-click install)

```bash
curl -fsSL https://azai-download-tracker.vibelock.workers.dev/install.sh | bash
azai ui
azai doctor
azai ollama
azai jeeves
```

The install path:

1. Downloads the counted tarball and `pip install -e .`
2. Runs `scripts/setup-ollama.sh` — installs or reuses Ollama, starts
   `ollama serve` if needed, pulls `llama3.2` (or `AZAI_OLLAMA_MODEL`)
3. If Ollama cannot be installed here, the script prints the exact steps
   and AZAI still runs with the JEEVES constitution stub

Then open http://127.0.0.1:8860 (loopback only). Default model is `local`
(Ollama + JEEVES / Ask Jeeves). Point other software at:

```bash
export OPENAI_BASE_URL=http://127.0.0.1:8860/v1
export OPENAI_API_KEY=dummy
```

Exact Ollama steps if doctor reports the base missing:

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
ollama pull llama3.2
azai doctor
```

Counted download (gzip HTTP 200, no 302): https://azai-download-tracker.vibelock.workers.dev/download?asset=azai-0.3.1.tar.gz
GitHub: https://github.com/AzielEliab/azai

## Catalog + local UI

Author: **Aziel Eliab**. Honest scope: true local AI on an Ollama base with
JEEVES (Ask Jeeves research assistant). Not a new foundation model. JEEVES
is not sovereign.

- Catalog product: https://aziel-runtime.vibelock.workers.dev/p/azai/
- Catalog OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json
- Catalog MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`
- This Worker skill: `GET https://azai-download-tracker.vibelock.workers.dev/v1/skill`
- This Worker OpenAPI: https://azai-download-tracker.vibelock.workers.dev/openapi.json
- Ask Jeeves card: `GET https://azai-download-tracker.vibelock.workers.dev/v1/jeeves`
- Sample payload: `GET https://azai-download-tracker.vibelock.workers.dev/v1/example`

Local UI: **Ask Jeeves** research assistant, **Import JSON file** (`type=file`)
and **Export JSON**. Then `azai doctor`.

Grok: import catalog or Worker OpenAPI as a custom tool. ChatGPT: GPT Actions. Venice: HTTP tools.
