# AZAI download tracker (Cloudflare Worker)

Counts GitHub-release downloads for AZAI across the canonical
repository, other branches, and forks. Forks are identified by GitHub
`owner/repo`.

Homepage is an **isolated counter**: the number is on the download
button. Nobody reports a download. The click is the count.

GET `/download` **serves** the tarball via `env.ASSETS.fetch`. It does
not 302 to GitHub. `Cache-Control: private, no-store`.

`totalKey()` = `azai|__total__`. PROJECT `azai`. Worker
`azai-download-tracker`. KV namespace `AZAI_DOWNLOADS` bound as
`DOWNLOADS`.

No secrets belong in this directory.

Not a new foundation model. Jeeves is not sovereign. Hosted `/v1` is lamb-check ONLY (plus health/models). Never a paid-key proxy. Forks are welcome
and always allowed.

This worker is AZAI only. It is not mixed with AZ-OS, GodLock,
ForgeReceipts, The ARK, or any other product.

Isolated counter: Worker `azai-download-tracker`, project `azai`.

## Bindings

| Binding     | Type | Purpose |
|-------------|------|---------|
| `DOWNLOADS` | KV   | Counters keyed `project|owner|repo|branch|fork` |

KV id in `wrangler.toml`: `155f641feb8244bea7fa245133128a32`. Binding name MUST stay `DOWNLOADS` (not
`AZAI_DOWNLOADS` — that is the Cloudflare namespace title).

## Routes

| Method | Path | Behavior |
|--------|------|----------|
| GET | `/` | Isolated homepage: live count on the download button |
| GET | `/download?repo=&tag=&asset=` | Increment KV, serve the asset from `ASSETS` |
| GET | `/count` | JSON `{project, total}` |
| GET | `/stats` | JSON totals plus per-repo and per-branch breakdown |
| POST | `/event` | A fork reports a download |

Tracked asset URL:

```
https://azai-download-tracker.vibelock.workers.dev/download?asset=azai-0.2.0.tar.gz
```

## CORS

All responses include `Access-Control-Allow-Origin: *`.

## AI runtime (`/v1`)

CORS `*`. `GET /v1/health`, `GET /v1/models`, `POST /v1/lamb-check` `{text}`,
`GET /openapi.json` (OpenAPI 3.1), `GET /ai`.
Routes under `/v1` **do not** increment download KV.
Lamb check is the JS port of `azai/lamb.py`. No provider proxy.

Help page: `/ai`. Combined catalog: https://aziel-runtime.vibelock.workers.dev/

POST `/v1/lamb-check` rejects bodies larger than 1 MiB (413). No API keys live in this Worker.
