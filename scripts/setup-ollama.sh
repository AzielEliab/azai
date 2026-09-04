#!/usr/bin/env bash
# AZAI — install / use the local Ollama base and pull the default model.
# Safe to re-run. Never a paid-key proxy. Author: Aziel Eliab.
#
# Env:
#   AZAI_OLLAMA_MODEL   default llama3.2  (smaller: llama3.2:1b)
#   AZAI_OLLAMA_URL     default http://127.0.0.1:11434
#   AZAI_SKIP_OLLAMA=1  print steps only, do not install
set -u

MODEL="${AZAI_OLLAMA_MODEL:-llama3.2}"
URL="${AZAI_OLLAMA_URL:-http://127.0.0.1:11434}"
BIN_DIR="${AZAI_OLLAMA_BIN:-$HOME/.local/bin}"

steps() {
  cat <<EOF
Exact Ollama steps for AZAI (true local AI, no hosted paid-key proxy):

  1. Install Ollama
     Linux/macOS:  curl -fsSL https://ollama.com/install.sh | sh
     Windows:      https://ollama.com/download
     No sudo:      download the ollama binary from https://ollama.com/download
                   and place it on PATH (example: mkdir -p "$HOME/.local/bin").

  2. Start the local server (loopback):
     ollama serve
     Default: ${URL}

  3. Pull the default model:
     ollama pull ${MODEL}
     Smaller machine: AZAI_OLLAMA_MODEL=llama3.2:1b ollama pull llama3.2:1b

  4. Confirm, then run AZAI:
     curl -s ${URL}/api/tags
     azai doctor
     azai ui
     Open http://127.0.0.1:8860
     Other software: OPENAI_BASE_URL=http://127.0.0.1:8860/v1  OPENAI_API_KEY=dummy

JEEVES is the ethics/assistant layer on this Ollama base. JEEVES is not sovereign.
EOF
}

echo "AZAI Ollama setup  model=${MODEL}  url=${URL}"
echo

if [ "${AZAI_SKIP_OLLAMA:-}" = "1" ]; then
  steps
  exit 0
fi

have_ollama() {
  command -v ollama >/dev/null 2>&1
}

if ! have_ollama; then
  echo "Ollama not on PATH. Trying install…"
  if [ -w /usr/local/bin ] || [ "$(id -u)" -eq 0 ] || command -v sudo >/dev/null 2>&1; then
    if command -v curl >/dev/null 2>&1; then
      if curl -fsSL https://ollama.com/install.sh | sh; then
        echo "Official Ollama installer finished."
      else
        echo "Official installer failed (network or privileges)."
      fi
    fi
  else
    echo "No sudo/root for the official installer. Trying a user-local binary…"
    mkdir -p "$BIN_DIR"
    ARCH="$(uname -m 2>/dev/null || echo unknown)"
    OS="$(uname -s 2>/dev/null || echo unknown)"
    TARBALL=""
    if [ "$OS" = "Linux" ]; then
      case "$ARCH" in
        x86_64|amd64) TARBALL="https://ollama.com/download/ollama-linux-amd64.tgz" ;;
        aarch64|arm64) TARBALL="https://ollama.com/download/ollama-linux-arm64.tgz" ;;
      esac
    fi
    if [ -n "$TARBALL" ] && command -v curl >/dev/null 2>&1; then
      TMP="$(mktemp -d)"
      if curl -fsSL "$TARBALL" -o "$TMP/ollama.tgz"; then
        tar -xzf "$TMP/ollama.tgz" -C "$TMP"
        if [ -f "$TMP/ollama" ]; then
          cp "$TMP/ollama" "$BIN_DIR/ollama"
          chmod +x "$BIN_DIR/ollama"
        elif [ -f "$TMP/bin/ollama" ]; then
          cp "$TMP/bin/ollama" "$BIN_DIR/ollama"
          chmod +x "$BIN_DIR/ollama"
        fi
        export PATH="$BIN_DIR:$PATH"
        echo "Installed user-local ollama at $BIN_DIR/ollama"
      else
        echo "Could not download $TARBALL"
      fi
      rm -rf "$TMP"
    fi
  fi
fi

if ! have_ollama && [ -x "$BIN_DIR/ollama" ]; then
  export PATH="$BIN_DIR:$PATH"
fi

if ! have_ollama; then
  echo
  echo "Ollama is not installed on this machine yet. AZAI itself is installed."
  echo "JEEVES will use the constitution stub until Ollama is running."
  echo
  steps
  exit 0
fi

echo "Found $(command -v ollama)"

if ! curl -fsS --max-time 2 "${URL}/api/tags" >/dev/null 2>&1; then
  echo "Starting ollama serve in the background…"
  nohup ollama serve >/tmp/azai-ollama-serve.log 2>&1 &
  sleep 2
fi

if curl -fsS --max-time 2 "${URL}/api/tags" >/dev/null 2>&1; then
  echo "Ollama is reachable at ${URL}"
  echo "Pulling default model ${MODEL} (this can take several minutes)…"
  if ollama pull "${MODEL}"; then
    echo "Model ${MODEL} is ready."
  else
    echo "ollama pull ${MODEL} failed. Retry later: ollama pull ${MODEL}"
  fi
else
  echo "Ollama binary is present but ${URL} is not reachable."
  echo "Start it yourself: ollama serve"
fi

echo
steps
echo
echo "Then: azai ui   and open http://127.0.0.1:8860"
echo "Author: Aziel Eliab."
