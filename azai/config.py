"""AZAI constants. Honest scope lives here so the UI, CLI, and Worker agree."""

from __future__ import annotations

APP_NAME = "AZAI"
INSTRUMENT = "Jeeves"
UI_HOST = "127.0.0.1"
UI_PORT = 8860
DATA_DIR_NAME = "AZAI_DATA"
CONSTITUTION_VERSION = "1.0"

MODELS = ("blend", "gpt", "grok", "venice", "local")

GPT_URL = "https://api.openai.com/v1/chat/completions"
GPT_MODEL = "gpt-4o-mini"
GROK_URL = "https://api.x.ai/v1/chat/completions"
GROK_MODEL = "grok-3-mini"
GROK_MODEL_ALT = "grok-2-latest"
VENICE_URL = "https://api.venice.ai/api/v1/chat/completions"
VENICE_URL_ALT = "https://api.venice.ai/v1/chat/completions"
VENICE_MODEL = "llama-3.3-70b"

PROVIDER_TIMEOUT = 30.0

# Hardening: refuse oversized POSTs (local UI and hosted lamb-check).
MAX_BODY_BYTES = 1_048_576  # 1 MiB

SAMPLE_PROMPT = "Explain receipts in one sentence, please."

VIEWS = ("simple", "advanced")

# Phrases that must never appear in the loopback UI or Worker (no telemetry).
TELEMETRY_FORBIDDEN = (
    "google-analytics",
    "googletagmanager",
    "gtag(",
    "mixpanel",
    "segment.io",
    "sentry.io",
    "amplitude.com",
    "hotjar",
    "fullstory",
)

# Hosted Worker must never contain these as live secrets or provider calls.
WORKER_KEY_MARKERS = (
    "sk-",
    "xai-",
    "Bearer ",
)
WORKER_PROVIDER_HOSTS = (
    "api.openai.com",
    "api.x.ai",
    "api.venice.ai",
)

LIMITATION = (
    "AZAI is a local OpenAI-compatible runtime, not a new foundation model, "
    "not a kernel, not a worm, not IP-blocking malware, not a VPN. "
    "Jeeves is not sovereign. Lamb Lens (peace, clarity, service) gates every turn. "
    "Hub is a blank key: it does not interpret meaning. "
    "Blend is visible: gpt / grok / venice are labeled, then a short synthesis. "
    "Without API keys, local Jeeves stub (Lamb Lens + receipts + constitution) "
    "runs and does not pretend to be GPT. "
    "Voice is optional extra [voice]; MVP is text. Push-to-talk only; no wake word; "
    "no passive recording; voice does not execute commands. "
    "Memory writes require explicit confirm. Session-only by default. "
    "Paid GPT/Grok/Venice calls happen on the operator's local azai serve. "
    "The hosted Cloudflare /v1 is lamb-check ONLY (plus a protocol mirror of "
    "health/models), NOT a proxy that spends the author's paid keys. "
    "Lamb Lens is a constitutional gate, not a proof of ethics. "
    "Jeeves speaks inside the shell. Lamb Lens governs above the shell. "
    "Receipts witness what the shell permits."
)

LAN_RISK = (
    "Binding a non-loopback --host exposes the OpenAI-compatible API on that "
    "interface with no auth beyond a dummy key. Anyone who can reach the port "
    "can spend the operator's GPT/Grok/Venice keys. Prefer 127.0.0.1. "
    "On-site LAN is for a trusted network only."
)

MOTTO = (
    "Jeeves speaks inside the shell. "
    "Lamb Lens governs above the shell. "
    "Receipts witness what the shell permits."
)
