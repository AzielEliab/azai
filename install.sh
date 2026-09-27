#!/usr/bin/env bash
# AZAI one-click install. Counted download via this project's Worker.
# Installs the Python package only. The default core does not require Ollama
# or model weights. scripts/setup-ollama.sh is optional.
# Usage: curl -fsSL https://azai-download-tracker.vibelock.workers.dev/install.sh | bash
set -euo pipefail

HOST="${AZAI_HOME_HOST:-https://azai-download-tracker.vibelock.workers.dev}"
ASSET="${AZAI_HOME_ASSET:-azai-0.3.1.tar.gz}"
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
echo "Installed AZAI."
echo "The default core does not require Ollama or model weights."
echo "Next:"
echo "  azai ui"
echo "Then open http://127.0.0.1:8860/"
echo "Self-check: azai doctor   (green without Ollama)"
echo
echo "Optional Ollama slot: scripts/setup-ollama.sh"
echo "  Then set AZAI_BACKEND=ollama or call model=ollama."
echo "  The installer does not run that script."
echo "Author: Aziel Eliab."
