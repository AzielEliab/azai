"""AZAI constants. Honest scope lives here so the UI, CLI, and Worker agree."""

from __future__ import annotations

APP_NAME = "AZAI"
INSTRUMENT = "Jeeves"
UI_HOST = "127.0.0.1"
UI_PORT = 8860
DATA_DIR_NAME = "AZAI_DATA"
CONSTITUTION_VERSION = "1.0"

# Default core is local: constitution and guide. No weights. No Ollama probe.
# Ollama is an optional slot (AZAI_BACKEND=ollama or model=ollama).
# Optional paid blend (gpt/grok/venice) stays on the operator's machine only.
MODELS = ("local", "ollama", "blend", "gpt", "grok", "venice")
DEFAULT_MODEL = "local"

OLLAMA_URL = "http://127.0.0.1:11434"
# Suggested tag for the optional Ollama slot only. Never pulled by default.
OLLAMA_MODEL = "llama3.2"
OLLAMA_PROBE_TIMEOUT = 0.8
OLLAMA_CHAT_TIMEOUT = 120.0
OLLAMA_TAGS_PATH = "/api/tags"
OLLAMA_CHAT_PATH = "/v1/chat/completions"

OLLAMA_INSTALL_STEPS = (
    "Optional Ollama slot only. The default AZAI core does not require Ollama or any GGUF weights.\n"
    "Use this only after you opt in with AZAI_BACKEND=ollama or model=ollama.\n"
    "1. Install Ollama (Linux/macOS): curl -fsSL https://ollama.com/install.sh | sh\n"
    "   Windows: https://ollama.com/download\n"
    "   No sudo? download the binary from https://ollama.com/download, place it on PATH\n"
    "   (example: mkdir -p \"$HOME/.local/bin\" && install the ollama binary there).\n"
    "   Or run: bash scripts/setup-ollama.sh\n"
    "2. Start the local server if it is not already running: ollama serve\n"
    "   Default listen: 127.0.0.1:11434 (loopback). Override with AZAI_OLLAMA_URL.\n"
    "3. Pull a model for this slot only: ollama pull llama3.2\n"
    "   Smaller machine: AZAI_OLLAMA_MODEL=llama3.2:1b ollama pull llama3.2:1b\n"
    "4. Confirm the slot: curl -s http://127.0.0.1:11434/api/tags && azai ollama\n"
    "5. AZAI itself is already runnable: azai ui   then open http://127.0.0.1:8860\n"
    "The default model is local. No hosted paid-key proxy. No OpenAI key required."
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
    "AZAI is true local AI: a standalone local core, an OpenAI-shaped process on this machine. "
    "The default core does not require Ollama or model weights. "
    "JEEVES is the Ask Jeeves research assistant (ethics/assistant layer) "
    "and is not sovereign. "
    "Lamb Lens first — Service → Clarity → Peace; public Corpus posture; never the operator. "
    "Jeeves cannot modify scores; same rights as a normal user. "
    "Hub is a blank key: it does not interpret meaning. "
    "Default model=local is the constitution and guide, with light adaptive "
    "session notes and site_context. It never probes Ollama as the success path. "
    "Ollama is an optional slot (AZAI_BACKEND=ollama or model=ollama). "
    "Optional paid blend (gpt / grok / venice) is labeled, then a short synthesis. "
    "AZAI is not a new foundation model, not a kernel, not a worm, "
    "not IP-blocking malware, not a VPN, and not a hosted paid-key proxy. "
    "Voice is optional extra [voice]; MVP is text. Push-to-talk only; no wake word; "
    "no passive recording; voice does not execute commands. "
    "Memory writes require explicit confirm. Session-only by default. "
    "Paid GPT/Grok/Venice calls happen on the operator's local azai serve only. "
    "The hosted Cloudflare /v1 is lamb-check ONLY (plus a protocol mirror of "
    "health/models), NOT a proxy that spends the author's paid keys. "
    "Site assistants (www.azielcorpuslibrary.net) call local azai serve with "
    "optional site_context (public titles/summaries). Persist nothing secret. "
    "Lamb Lens is a constitutional gate, not a proof of ethics. "
    "Jeeves speaks inside the shell. Lamb Lens governs above the shell. "
    "Receipts witness what the shell permits."
)

LAN_RISK = (
    "Binding a non-loopback --host exposes the OpenAI-compatible API on that "
    "interface with no auth beyond a dummy key. Anyone who can reach the port "
    "can use the local core and, if you opted into the Ollama slot or set paid "
    "keys, use those too. Prefer 127.0.0.1. "
    "On-site LAN is for a trusted network only."
)

MOTTO = (
    "Jeeves speaks inside the shell. "
    "Lamb Lens governs above the shell. "
    "Receipts witness what the shell permits."
)
