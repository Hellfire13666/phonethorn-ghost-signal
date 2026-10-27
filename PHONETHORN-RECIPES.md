# PHONETHORN // GHOST SIGNAL v0.5.0
## Safe download and beginner recipes · Debian-based Linux

Standalone source: https://github.com/Hellfire13666/phonethorn-ghost-signal

### New installation (copy one block)
```bash
if command -v git >/dev/null && command -v python3 >/dev/null; then
  if [ ! -e "$HOME/phonethorn-ghost-signal" ]; then
    git clone https://github.com/Hellfire13666/phonethorn-ghost-signal.git "$HOME/phonethorn-ghost-signal"
  else
    printf '[INFO] Existing folder preserved; no clone attempted.\n'
  fi
  if [ -f "$HOME/phonethorn-ghost-signal/INSTALL.sh" ]; then
    ( cd "$HOME/phonethorn-ghost-signal" && bash ./INSTALL.sh && ./RUN.sh --examples )
  else
    printf '[STOP] Expected source missing; inspect the existing folder.\n'
  fi
else
  printf '[NEEDED] Debian packages: git python3 python3-venv\n'
fi
```

### Already installed? Verify without changing project files
```bash
( cd "$HOME/phonethorn-ghost-signal" &&
  python3 -B -m unittest discover -s tests -v &&
  ./RUN.sh --version &&
  ./RUN.sh --examples )
```

### Safe example recipes
```bash
cd "$HOME/phonethorn-ghost-signal"
./RUN.sh --phone "+14155552671" --region US
./RUN.sh --phone "+14155552671" --web-intel
./RUN.sh --phone "+14155552671" --fusion --out ./PhoneThornReports
./RUN.sh --coords 40.7128 -74.0060
./RUN.sh --rescue android
./RUN.sh --rescue iphone
./RUN.sh --devices
```

### Optional modes
Use `--geo-ip 8.8.8.8 --live-geo` for approximate **IP** geography, not a phone's GPS.
Use `--photo-gps ./your-owned-photo.jpg` only for an image you own.
Use `--web-url https://example.org/contact` only for public business pages you are permitted to inspect.
Twilio carrier lookup needs privately configured credentials and may incur fees.

### Easy-save reports
```bash
( cd "$HOME/phonethorn-ghost-signal" &&
  ./RUN.sh --phone "+14155552671" --fusion --out ./PhoneThornReports )
```
The `--out` option is the published PHONETHORN report-directory option for supported report modes.
Do not commit real phone reports, photographs, credentials, or `.env` files.

### Privacy requirements
Use only fictional account names, hostnames, file paths, numbers and domains in public documentation.
Inspect the **real** repository and generated release artifacts before publishing.
The included `privacy_publication_guard.py` is a preventative text check, not a complete secrets audit.
