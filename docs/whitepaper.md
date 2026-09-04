# AZAI — true local AI on an Ollama base (v0.3.0)

Aziel Artificial Intelligence. Shell: **AZAI**. Instrument: **JEEVES**.
Author: Aziel Eliab, 2026. Apache-2.0.

## What this is

A **true local AI** package. **Ollama** is the local model base.
**JEEVES** is the ethics/assistant layer (not sovereign). The local
API is OpenAI-compatible so other software on site can point at it.
Optional paid GPT / Grok / Venice blend stays on this machine only.

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

Lamb Lens = Peace → Clarity → Service. FAIL blocks the turn (no
provider call) and writes a receipt. Jailbreak phrasing such as
"ignore previous instructions" is **CHECK**, not a silent pass.

Honest: this is a constitutional gate, not a proof of ethics.

## Blend

When `model=blend`, the runtime calls gpt, grok, and venice (or records
that a key is missing) and returns labeled sections plus a short
synthesis. Never hide which model said what.

Default `model=local` (and `model=ollama`) runs JEEVES on the Ollama
base. Without Ollama, the constitution stub still answers and does not
pretend to be GPT.

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


## v0.3.0

Ollama is the true local base. `scripts/setup-ollama.sh` installs or
reuses Ollama and pulls `llama3.2` (or `AZAI_OLLAMA_MODEL`). JEEVES wraps
every local turn as the ethics/assistant layer and is not sovereign.
Default model is `local`. Optional paid blend remains labeled.
`azai ollama` and `azai doctor` print exact Ollama steps when the base
is missing. OpenAI-compatible API unchanged at `/v1`. Hosted `/v1` is
still lamb-check ONLY — not a paid-key proxy.

## v0.2.0

Loopback UI at 127.0.0.1:8860 with one chat box, Send, Check this text,
Peace / Clarity / Service chips, a sample prompt, and Simple / Advanced
views. Import `.txt` / JSON conversations. Export chat + receipts as JSON
and Markdown. `azai doctor` verifies Lamb fixtures, loopback, receipts,
max body, no telemetry, and that the Worker holds no keys and is not a
paid-key proxy. `AZAI_DEBUG=1` prints local stderr traces (keys redacted).
Hosted `/v1` is lamb-check ONLY.
