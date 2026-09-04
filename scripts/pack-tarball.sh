#!/usr/bin/env bash
# Rebuild the counted Worker download tarball (sdist → public/).
# Usage: bash scripts/pack-tarball.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
VERSION="$(python3 -c "import pathlib; t=pathlib.Path('pyproject.toml').read_text();
import re; print(re.search(r'^version = \"([^\"]+)\"', t, re.M).group(1))")"
python3 -m pip install -q build
python3 -m build --sdist
mkdir -p workers/download-tracker/public
cp -f "dist/azai-${VERSION}.tar.gz" "workers/download-tracker/public/azai-${VERSION}.tar.gz"
echo "Wrote workers/download-tracker/public/azai-${VERSION}.tar.gz"
ls -lh "workers/download-tracker/public/azai-${VERSION}.tar.gz"
