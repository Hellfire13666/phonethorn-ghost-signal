# PHONETHORN v0.6.3 // CLEAN SIGNAL

No changes to your terminal background or appearance settings.

Use `--output clean` (default), `--verbose` for full technical terminal data,
or `--quiet` for minimal display. Full local HTML/JSON/TXT reports are retained.
Routine saved-report messages display counts and no full home paths.

## Quick test (fictional number)
```bash
cd "$HOME/PHONETHORN-v0.6.3-CLEAN-SIGNAL"
bash ./RUN.sh --phone '+14155552671' --web-intel --fusion --popup-results --out "$HOME/PhoneThornReports"
bash ./RUN.sh --phone '+14155552671' --web-intel --verbose
```

## Debian installation
Download the ZIP, then:
```bash
cd "$HOME/Downloads" &&
if [ -e "$HOME/PHONETHORN-v0.6.3-CLEAN-SIGNAL" ]; then
  echo '[STOP] Existing installation preserved'
else
  unzip -q PHONETHORN-v0.6.3-CLEAN-SIGNAL.zip -d "$HOME" &&
  cd "$HOME/PHONETHORN-v0.6.3-CLEAN-SIGNAL" &&
  bash ./INSTALL.sh && bash ./RUN.sh --version
fi
```
No sudo for normal launcher execution. Never publicly share private phone reports.
