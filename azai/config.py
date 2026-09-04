"""AZAI constants. Honest scope lives here so the UI, CLI, and Worker agree."""

from __future__ import annotations

APP_NAME = "AZAI"
INSTRUMENT = "Jeeves"
UI_HOST = "127.0.0.1"
UI_PORT = 8860
DATA_DIR_NAME = "AZAI_DATA"
CONSTITUTION_VERSION = "1.0"

# Ollama is the true local base. JEEVES is the ethics/assistant layer on top.
# Optional paid blend (gpt/grok/venice) stays on the operator's machine only.
MODELS = ("local", "ollama", "blend", "gpt", "grok", "venice")
DEFAULT_MODEL = "local"

OLLAMA_URL = "http://127.0.0.1:11434"
OLLAMA_MODEL = "llama3.2"
OLLAMA_PROBE_TIMEOUT = 0.8
OLLAMA_CHAT_TIMEOUT = 120.0
OLLAMA_TAGS_PATH = "/api/tags"
OLLAMA_CHAT_PATH = "/v1/chat/completions"

OLLAMA_INSTALL_STEPS = (
    "1. Install Ollama (Linux/macOS): curl -fsSL https://ollama.com/install.sh | sh\n"
    "   Windows: https://ollama.com/download\n"
    "   No sudo? download the binary from https://ollama.com/download, place it on PATH\n"
    "   (example: mkdir -p \"$HOME/.local/bin\" && install the ollama binary there).\n"
    "2. Start the local server if it is not already running: ollama serve\n"
    "   Default listen: 127.0.0.1:11434 (loopback). Override with AZAI_OLLAMA_URL.\n"
    "3. Pull the default model: ollama pull llama3.2\n"
    "   Smaller machine: AZAI_OLLAMA_MODEL=llama3.2:1b ollama pull llama3.2:1b\n"
    "4. Confirm: curl -s http://127.0.0.1:11434/api/tags && azai doctor\n"
    "5. Run AZAI: azai ui   then open http://127.0.0.1:8860\n"
    "AZAI talks to Ollama on this machine. No hosted paid-key proxy. No OpenAI key required for local."
)

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
    "AZAI packages a true local AI stack on an Ollama base with JEEVES. "
    "OpenAI-compatible local API. Not a hosted paid-key proxy. "
    "AZAI is not a new foundation model, not a kernel, not a worm, "
    "not IP-blocking malware, not a VPN. "
    "JEEVES is the ethics/assistant layer inside the shell and is not sovereign. "
    "Lamb Lens (peace, clarity, service) and the operator govern every turn. "
    "Hub is a blank key: it does not interpret meaning. "
    "Default model=local uses Ollama through JEEVES. "
    "Optional paid blend (gpt / grok / venice) is labeled, then a short synthesis. "
    "Without Ollama, the JEEVES constitution stub still runs and does not pretend to be GPT. "
    "Voice is optional extra [voice]; MVP is text. Push-to-talk only; no wake word; "
    "no passive recording; voice does not execute commands. "
    "Memory writes require explicit confirm. Session-only by default. "
    "Paid GPT/Grok/Venice calls happen on the operator's local azai serve only. "
    "The hosted Cloudflare /v1 is lamb-check ONLY (plus a protocol mirror of "
    "health/models), NOT a proxy that spends the author's paid keys. "
    "Lamb Lens is a constitutional gate, not a proof of ethics. "
    "Jeeves speaks inside the shell. Lamb Lens governs above the shell. "
    "Receipts witness what the shell permits."
)

LAN_RISK = (
    "Binding a non-loopback --host exposes the OpenAI-compatible API on that "
    "interface with no auth beyond a dummy key. Anyone who can reach the port "
    "can use the local Ollama base and, if present, spend the operator's "
    "GPT/Grok/Venice keys. Prefer 127.0.0.1. "
    "On-site LAN is for a trusted network only."
)

MOTTO = (
    "Jeeves speaks inside the shell. "
    "Lamb Lens governs above the shell. "
    "Receipts witness what the shell permits."
)
