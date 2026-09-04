"""One-shot local JEEVES turn (Ollama base, constitution stub if Ollama is down)."""

from azai.runtime import Runtime

if __name__ == "__main__":
    rt = Runtime()
    out = rt.chat("What is AZAI?", model="local")
    print(out["content"])
    print("receipt", out["receipt"])
