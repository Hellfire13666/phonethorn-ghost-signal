#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")"
if [[ -x .venv/bin/python ]]; then exec .venv/bin/python -m phonethorn "$@"; fi
exec python3 -m phonethorn "$@"
