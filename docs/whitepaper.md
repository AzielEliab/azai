# AZAI — true local AI, standalone local core (v0.3.1)

Aziel Artificial Intelligence. Shell: **AZAI**. Instrument: **JEEVES**.
Author: Aziel Eliab, 2026. Apache-2.0.

## What this is

A **true local AI** package. The default core is a standalone
constitution and guide. It does not require Ollama or model weights.
It adapts lightly through confirmed session notes and public
`site_context`. **JEEVES** is the ethics/assistant layer (not sovereign).
The local API is OpenAI-compatible so other software on site can point
at it. Ollama is an optional slot (`AZAI_BACKEND=ollama` or
`model=ollama`). Optional paid GPT / Grok / Venice blend stays on this
machine only.

```
OPENAI_BASE_URL=http://127.0.0.1:8860/v1
```

## What this is not

Not a new foundation model. Not a kernel. Not a worm. Not IP-blocking
malware. Not a VPN. Not a remote OS takeover. Phoenix-as-spreader and
"static block IP routing" from the research roadmap are **out of scope**
and not implemented.

Jeeves is not sovereign. The Hub is a blank key: it never interprets
meaning.

## Hierarchy

Lamb Lens → Formal Rules → Integrity Gate → Jeeves Reasoning →
Learned Patterns → Output.

Lamb Lens = Service → Clarity → Peace. FAIL blocks the turn (no
provider call) and writes a receipt. Jailbreak phrasing such as
"ignore previous instructions" is **CHECK**, not a silent pass.

Honest: this is a constitutional gate, not a proof of ethics.

## Blend

When `model=blend`, the runtime calls gpt, grok, and venice (or records
that a key is missing) and returns labeled sections plus a short
synthesis. Never hide which model said what.

Default `model=local` runs JEEVES on the constitution and guide. It
does not probe Ollama. `model=ollama` (or `AZAI_BACKEND=ollama`) is the
optional slot. The local core does not pretend to be GPT.

Paid calls happen only on local `azai serve`. The hosted Cloudflare
Worker `/v1` lists models and runs the same Lamb rules in JS. It does
not spend the author's keys.

## Voice

Optional extra `[voice]`. MVP is text. Voice is an interface, not an
authority. Push-to-talk only. No wake word. No passive recording.
Voice does not execute commands. Whisper/Piper models are not vendored.

## Memory

Session-only by default. Writes require explicit confirm.

## Receipts

Append-only JSONL under `AZAI_DATA`. Hash = sha256(prev + canonical
payload). TemporalLock-lite. Anyone can recompute.

## Papers

Copied into `docs/source/`:

- Hub & Software Tether (blank key)
- AZAI–Jeeves Constitution, UI edition
- Technical roadmap (research megalith; this package implements the
  local runtime, not the defensive-spreader items)
- AZAI Voice
- Constitution Harmonic Equilibrium

## Motto

Jeeves speaks inside the shell. Lamb Lens governs above the shell.
Receipts witness what the shell permits.


## v0.3.1

Ask Jeeves research-assistant mode for site assistants, especially
https://www.azielcorpuslibrary.net/. Lamb Lens first — public Corpus
posture; never the operator. Hard refusals live in `azai/jeeves.py`
SYSTEM: no operator account info / credentials / admin hashes / hidden
routes; no corpus-risking advice (wipe, score forge, quarantine bypass);
cannot modify scores (same rights as a normal user). Optional
`site_context` (public titles/summaries) is an adaptive hook as the
library grows; persist nothing secret. Upload guidance is out of band:
files still run full SPRE×CLCE×PhysLing + Bayesian ingest — no score
shortcut. CLI `azai jeeves`, UI copy, Worker `/v1/skill` + `/v1/jeeves`
+ OpenAPI document how the Corpus calls local AZAI. JEEVES remains not
sovereign and is not GPT.

The Worker homepage shows a suite Live Nodes strip. `/v1/mesh/*` PROXY
to aziel-runtime. Suite mesh default OFF. QNM rollup is
live|locked|isolated counts only. QNS-CD-1.0 is a hub cite / Worker mesh
cross-map only (photon QNS1 packet transfer; local qnsd in qnm-node;
runtime cites in aziel-runtime). No Node Gate. No public qnsd proxy. No
auto-heal. Not an anonymity network. Not a Softwares-tab product.
Anon-broadcast is not a publish path. AZAI remains true local AI: a
standalone local core with JEEVES. Ollama is optional. Hosted `/v1` is
still lamb-check ONLY.

## v0.3.0

At 0.3.0, Ollama was wired in and `scripts/setup-ollama.sh` could install
it and pull a model. That script is now optional and is not the install
path. The current default model `local` is the constitution and guide.
JEEVES wraps every local turn as the ethics/assistant layer and is not
sovereign. Optional paid blend remains labeled. `azai doctor` is green
without Ollama. `azai ollama` prints optional-slot steps. OpenAI-compatible
API unchanged at `/v1`. Hosted `/v1` is still lamb-check ONLY — not a
paid-key proxy.

## v0.2.0

Loopback UI at 127.0.0.1:8860 with one chat box, Send, Check this text,
Peace / Clarity / Service chips, a sample prompt, and Simple / Advanced
views. Import `.txt` / JSON conversations. Export chat + receipts as JSON
and Markdown. `azai doctor` verifies Lamb fixtures, loopback, receipts,
max body, no telemetry, and that the Worker holds no keys and is not a
paid-key proxy. `AZAI_DEBUG=1` prints local stderr traces (keys redacted).
Hosted `/v1` is lamb-check ONLY.
