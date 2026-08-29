# AZAI — local OpenAI-compatible runtime (v0.1.0)

Aziel Artificial Intelligence. Shell: **AZAI**. Instrument: **Jeeves**.
Author: Aziel Eliab, 2026. Apache-2.0.

## What this is

A **standard local AI** that blends GPT, Grok, and Venice on the
operator's machine, gated by the Lamb Lens, with an OpenAI-compatible
HTTP surface so other software on site can point at it.

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

Without keys, `model=local` (and blend fallback) runs the Jeeves stub.
The stub does not pretend to be GPT.

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
