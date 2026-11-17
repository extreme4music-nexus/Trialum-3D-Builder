#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if [[ ! -f vendor/three.module.js || ! -f assets/models/f01-marble-cream-full.glb ]]; then
  echo "Preparing local Three.js modules and original Trialum GLBs ..."
  python3 scripts/setup.py
fi
( xdg-open http://127.0.0.1:8765/ >/dev/null 2>&1 || true ) &
if command -v python3 >/dev/null; then
  exec python3 scripts/server.py
elif command -v node >/dev/null; then
  exec node scripts/server.mjs
else
  echo "Requires Python 3 or Node.js 20+" >&2
  exit 1
fi
