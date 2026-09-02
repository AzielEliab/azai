---
name: AZAI
description: Use when calling AZAI hosted /v1 or installing the local package. Author Aziel Eliab.
---

# AZAI

AZAI is a local OpenAI-compatible runtime, not a new foundation model, not a kernel, not a worm, not IP-blocking malware, not a VPN. Jeeves is not sovereign. Hosted /v1 is lamb-check ONLY, never a paid-key proxy. Author: Aziel Eliab.

**THIS IS:** a local OpenAI-compatible runtime under the Lamb Lens. Jeeves is the instrument inside the shell.

**THIS IS NOT:** a new foundation model, a kernel, a worm, IP-blocking malware, a VPN, or a hosted paid-key proxy. Jeeves is not sovereign.

Author: **Aziel Eliab**. Forks are welcome and always allowed. Apache-2.0.

Always send `User-Agent: Mozilla/5.0`. Cloudflare Workers may 403 an empty agent.

## Call these URLs

- Worker OpenAPI: https://azai-download-tracker.vibelock.workers.dev/openapi.json
- Catalog OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json
- MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`
- Live skill (this markdown): `GET https://azai-download-tracker.vibelock.workers.dev/v1/skill`

Ops (do **not** increment downloads or views):

| Method | Path | What |
|--------|------|------|
| GET | `/v1/health` | Liveness. Does not increment downloads. |
| GET | `/v1/skill` | This markdown. Does not increment downloads. |
| GET | `/v1/models` | Local model list. Hosted is not a paid proxy. |
| POST | `/v1/lamb-check` | Lamb Lens check only. Hosted never spends paid keys. |

Grok: import OpenAPI as a custom tool. ChatGPT: GPT Actions. Venice: HTTP tools.

## Example

```bash
curl -s -A 'Mozilla/5.0' https://azai-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' https://azai-download-tracker.vibelock.workers.dev/v1/skill
curl -s -A 'Mozilla/5.0' -X POST https://azai-download-tracker.vibelock.workers.dev/v1/lamb-check \
  -H 'content-type: application/json' \
  -d '{"text":"peace clarity service"}'
```

## Local (after one-click install)

```bash
curl -fsSL https://azai-download-tracker.vibelock.workers.dev/install.sh | bash
azai ui
```

Then open http://127.0.0.1:8860 (loopback only).

Counted download (gzip HTTP 200, no 302): https://azai-download-tracker.vibelock.workers.dev/download?asset=azai-0.2.0.tar.gz
GitHub: https://github.com/AzielEliab/azai
