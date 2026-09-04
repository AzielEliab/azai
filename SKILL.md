---
name: AZAI
description: Use when calling AZAI hosted /v1 or installing the local true-AI package. Author Aziel Eliab.
---

# AZAI

AZAI packages a **true local AI** stack on an **Ollama** base with **JEEVES**.
OpenAI-compatible local API. Not a hosted paid-key proxy. Author: **Aziel Eliab**.

**THIS IS:** true local AI. Ollama is the local model base. JEEVES is the
ethics/assistant layer inside the shell. JEEVES is not sovereign — Lamb Lens
and the operator govern it.

**THIS IS NOT:** a new foundation model, a kernel, a worm, IP-blocking malware,
a VPN, or a hosted paid-key proxy.

Always send `User-Agent: Mozilla/5.0`. Cloudflare Workers may 403 an empty agent.

## Call these URLs

- Worker OpenAPI: https://azai-download-tracker.vibelock.workers.dev/openapi.json
- Catalog OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json
- MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`
- Live skill (this markdown): `GET https://azai-download-tracker.vibelock.workers.dev/v1/skill`

Ops (do **not** increment downloads or views):

- `GET /v1/health` — liveness
- `GET /v1/skill` — this file
- Product POSTs listed in OpenAPI

Hosted `/v1` is **lamb-check ONLY**. It does not run Ollama and does not
spend paid keys.

Grok: import OpenAPI as a custom tool. ChatGPT: GPT Actions. Venice: HTTP tools.

## Example

```bash
curl -s -A 'Mozilla/5.0' https://azai-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' https://azai-download-tracker.vibelock.workers.dev/v1/skill
```

## Local (after one-click install)

```bash
curl -fsSL https://azai-download-tracker.vibelock.workers.dev/install.sh | bash
azai ui
azai doctor
azai ollama
```

The install path:

1. Downloads the counted tarball and `pip install -e .`
2. Runs `scripts/setup-ollama.sh` — installs or reuses Ollama, starts
   `ollama serve` if needed, pulls `llama3.2` (or `AZAI_OLLAMA_MODEL`)
3. If Ollama cannot be installed here, the script prints the exact steps
   and AZAI still runs with the JEEVES constitution stub

Then open http://127.0.0.1:8860 (loopback only). Default model is `local`
(Ollama + JEEVES). Point other software at:

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

Counted download (gzip HTTP 200, no 302): https://azai-download-tracker.vibelock.workers.dev/download?asset=azai-0.3.0.tar.gz
GitHub: https://github.com/AzielEliab/azai

## Catalog + local UI

Author: **Aziel Eliab**. Honest scope: true local AI on an Ollama base with
JEEVES. Not a new foundation model. JEEVES is not sovereign.

- Catalog product: https://aziel-runtime.vibelock.workers.dev/p/azai/
- Catalog OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json
- Catalog MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`
- This Worker skill: `GET https://azai-download-tracker.vibelock.workers.dev/v1/skill`
- This Worker OpenAPI: https://azai-download-tracker.vibelock.workers.dev/openapi.json
- Sample payload: `GET https://azai-download-tracker.vibelock.workers.dev/v1/example`

Local UI: **Import JSON file** (`type=file`) and **Export JSON**. Then `azai doctor`.

Grok: import catalog or Worker OpenAPI as a custom tool. ChatGPT: GPT Actions. Venice: HTTP tools.
