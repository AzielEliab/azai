"""One-shot Ask Jeeves turn on the standalone local core (no Ollama required)."""

from azai.runtime import Runtime

if __name__ == "__main__":
    rt = Runtime()
    out = rt.chat("What is AZAI?", model="local")
    print(out["content"])
    print("receipt", out["receipt"])
