#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")"
echo '◆ PHONETHORN v0.5.0 • Debian-based Linux installer'
if ! command -v python3 >/dev/null; then echo 'Python 3 required'; exit 1; fi
if ! python3 -m venv .venv 2>/dev/null; then
  echo 'Install Python venv first: sudo apt install python3-venv'
  exit 1
fi
.venv/bin/python -m pip install --disable-pip-version-check --quiet -r requirements.txt
mkdir -p "$HOME/.local/bin" "$HOME/.local/share/applications"
cat > "$HOME/.local/bin/phonethorn" <<EOR
#!/usr/bin/env bash
cd "$(pwd)"
exec "$(pwd)/.venv/bin/python" -m phonethorn "\$@"
EOR
chmod +x "$HOME/.local/bin/phonethorn"
cat > "$HOME/.local/share/applications/phonethorn.desktop" <<EOR
[Desktop Entry]
Type=Application
Name=PHONETHORN Cosmic Kitties
Comment=Offline phone metadata and lost-device recovery
Exec=$HOME/.local/bin/phonethorn --rescue android
Terminal=true
Categories=Utility;System;
EOR
printf '\n✓ PHONETHORN installed successfully.\n'
echo 'Run from the project folder: ./RUN.sh --examples'
echo 'Or use the launcher: phonethorn --rescue android (when available in PATH)'
