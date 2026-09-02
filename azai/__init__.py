"""AZAI (Aziel Artificial Intelligence).

Local OpenAI-compatible runtime that blends GPT, Grok, and Venice
under the Lamb Lens. Jeeves is the instrument inside the shell.
Jeeves is not sovereign. Hub is a blank key: it does not interpret meaning.

Not a new foundation model, not a kernel, not a worm, not IP-blocking
malware, not a VPN. Paid GPT/Grok/Venice calls happen on the operator's
local `azai serve`. The hosted Worker /v1 is lamb-check ONLY,
not a proxy that spends the author's keys.

Author: Aziel Eliab, 2026. Apache-2.0.

Standalone from AZ-OS, GodLock, ForgeReceipts.

Forks are welcome and always allowed.
"""

from __future__ import annotations

from azai.config import APP_NAME, LIMITATION, MODELS, UI_PORT

__version__ = "0.2.0"
__author__ = "Aziel Eliab"
__all__ = [
    "APP_NAME",
    "LIMITATION",
    "MODELS",
    "UI_PORT",
    "__version__",
]
