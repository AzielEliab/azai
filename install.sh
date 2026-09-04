#!/usr/bin/env bash
# AZAI one-click install. Counted download via this project's Worker.
# Installs the Python package, then the local Ollama base + default model.
# Usage: curl -fsSL https://azai-download-tracker.vibelock.workers.dev/install.sh | bash
set -euo pipefail

HOST="${AZAI_HOME_HOST:-https://azai-download-tracker.vibelock.workers.dev}"
ASSET="${AZAI_HOME_ASSET:-azai-0.3.0.tar.gz}"
WORKDIR="${AZAI_HOME:-$HOME/azai}"

mkdir -p "$WORKDIR"
cd "$WORKDIR"

echo "Downloading counted tarball from ${HOST}/download (User-Agent Mozilla/5.0)…"
curl -fsSL -A 'Mozilla/5.0' "${HOST}/download?asset=${ASSET}" -o "${ASSET}"

tar -xzf "${ASSET}"
DIR="$(find . -maxdepth 1 -type d -name 'azai-*' | head -n 1)"
if [ -n "${DIR}" ]; then
  cd "${DIR}"
fi

python3 -m venv .venv
# shellcheck disable=SC1091
. .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .

echo
echo "Installed AZAI (true local AI on an Ollama base; JEEVES is not sovereign)."
echo "Next: local Ollama + default model (llama3.2 unless AZAI_OLLAMA_MODEL is set)."
echo

if [ -f scripts/setup-ollama.sh ]; then
  bash scripts/setup-ollama.sh || true
else
  echo "scripts/setup-ollama.sh missing from this tree. Exact steps:"
  echo "  curl -fsSL https://ollama.com/install.sh | sh"
  echo "  ollama serve"
  echo "  ollama pull ${AZAI_OLLAMA_MODEL:-llama3.2}"
  echo "  azai doctor"
fi

echo
echo "Run:  azai ui"
echo "Then open http://127.0.0.1:8860  (loopback only)"
echo "OpenAI-compatible: OPENAI_BASE_URL=http://127.0.0.1:8860/v1  OPENAI_API_KEY=dummy"
echo "Self-check: azai doctor"
echo "Author: Aziel Eliab."
