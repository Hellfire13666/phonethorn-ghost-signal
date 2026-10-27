# PHONETHORN // GHOST SIGNAL v0.6.3
Cosmic Kitty Clean Signal edition. Debian-based Linux.

## Install without ZIP (once v0.6.3 is merged into GitHub main)

```bash
sudo apt update && sudo apt install -y git python3 python3-venv &&
git clone https://github.com/Hellfire13666/phonethorn-ghost-signal.git "$HOME/phonethorn-ghost-signal" &&
cd "$HOME/phonethorn-ghost-signal" &&
bash ./INSTALL.sh && bash ./RUN.sh --version
```
If the destination already exists, do not clone over it. Preserve existing files and follow upgrade instructions.

## Output styles
```bash
bash ./RUN.sh --phone '+14155552671' --web-intel --fusion --output clean --popup-results --out "$HOME/PhoneThornReports"
bash ./RUN.sh --phone '+14155552671' --web-intel --fusion --verbose --popup-results --out "$HOME/PhoneThornReports"
```
Clean is the default; verbose shows technical details. Saved reports retain full information.
The illustrative number above is not a real-person identity claim. Number metadata
does not provide subscriber identity or real-time GPS. Web research links are not retrieved matches.

## Publication
`PUBLISH-TO-GITHUB.sh` stages the release on a **new branch**, checks for private
paths and token-shaped strings, runs tests, and requests explicit approval before
pushing. It never force-pushes and never rewrites history. Review the pull request
and passing workflows before merging.

Run local tests:
```bash
python3 -B -m unittest discover -s tests -v
```
