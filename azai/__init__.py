"""AZAI (Aziel Artificial Intelligence).

True local AI package on an Ollama base. JEEVES is the ethics/assistant
layer inside the shell and is not sovereign. OpenAI-compatible local API.
Not a hosted paid-key proxy.

Optional paid GPT/Grok/Venice blend happens on the operator's local
`azai serve` only. The hosted Worker /v1 is lamb-check ONLY.

Author: Aziel Eliab, 2026. Apache-2.0.

Standalone from AZ-OS, GodLock, ForgeReceipts.

Forks are welcome and always allowed.
"""

from __future__ import annotations

from azai.config import APP_NAME, DEFAULT_MODEL, LIMITATION, MODELS, UI_PORT

__version__ = "0.3.0"
__author__ = "Aziel Eliab"
__all__ = [
    "APP_NAME",
    "DEFAULT_MODEL",
    "LIMITATION",
    "MODELS",
    "UI_PORT",
    "__version__",
]
