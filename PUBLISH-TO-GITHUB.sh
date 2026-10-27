#!/usr/bin/env bash
set -euo pipefail
SOURCE_DIR="$(dirname "$(readlink -f "$0")")"
cd "$SOURCE_DIR"
REPO='Hellfire13666/phonethorn-ghost-signal'
BRANCH='release/phonethorn-v0.6.3-clean-signal'
printf '%s\n' '=== PHONETHORN v0.6.3 // PRIVATE-INFO GUARD + GITHUB PUBLICATION ==='
command -v git >/dev/null || { echo '[STOP] Git is required.'; exit 1; }
command -v python3 >/dev/null || { echo '[STOP] Python 3 is required.'; exit 1; }
python3 -B -m unittest discover -s tests -v
python3 -B - <<'PY'
import pathlib,re,sys
root=pathlib.Path('.')
paths=[p for p in root.rglob('*') if p.is_file() and not any(x in p.parts for x in ('.git','.venv','__pycache__')) and p.suffix.lower() in ('.py','.md','.sh','.txt','.json','.yml','.yaml','.toml','.ini','.desktop')]
fail=[]
for p in paths:
    data=p.read_text(encoding='utf-8', errors='replace')
    if re.search(r'/(?:home|Users)/(?!example(?:user)?/|runner/|testuser/|user/)[A-Za-z0-9._-]+/',data): fail.append(p)
    if re.search(r'(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----)',data): fail.append(p)
    if ('MX ' + 'Linux') in data: fail.append(p)
if fail:
    print('[STOP] Potential privacy/branding findings in:', ', '.join(sorted({p.name for p in fail})))
    sys.exit(1)
print('[PASS] No matching local-account paths, token patterns, or old distro wording in source text.')
PY
if [ -d .git ]; then
  echo '[STOP] This package directory already contains a git repository. Review its git status manually.'
  exit 1
fi
if [ -e "$HOME/phonethorn-publish-v063" ]; then
  echo '[STOP] A publication staging folder already exists; nothing overwritten.'
  exit 1
fi
STAGE="$HOME/phonethorn-publish-v063"
git clone "https://github.com/$REPO.git" "$STAGE"
cd "$STAGE"
git switch -c "$BRANCH"
# Copy known release contents, retaining GitHub-specific workflow and history.
for item in INSTALL.sh RUN.sh README.md README-CLEAN-OUTPUT.md README-UPGRADE.md COSMIC_KITTIES_EXAMPLES.md EXAMPLES.md GITHUB_PUBLISH.md PORTABLE_README.md LICENSE requirements.txt PHONETHORN-COVER.png; do
  cp "$SOURCE_DIR/$item" "$STAGE/$item"
done
cp -R "$SOURCE_DIR/phonethorn/." "$STAGE/phonethorn/"
cp -R "$SOURCE_DIR/tests/." "$STAGE/tests/"
cp "$SOURCE_DIR/PUBLISH-TO-GITHUB.sh" "$STAGE/PUBLISH-TO-GITHUB.sh"
chmod u+x "$STAGE/RUN.sh" "$STAGE/INSTALL.sh"
git add -A
if git diff --cached --quiet; then
  echo '[INFO] No release changes to publish.'
  exit 0
fi
printf '\n[REVIEW] Files staged for release:\n'
git diff --cached --name-status
printf '\n[REVIEW] Repository: %s\n[REVIEW] Branch: %s\n' "$REPO" "$BRANCH"
read -r -p 'Publish this branch to GitHub now? Type PUBLISH: ' approval
if [ "$approval" != PUBLISH ]; then echo '[STOP] User did not approve publication.'; exit 0; fi
git commit -m 'Release PHONETHORN v0.6.3 Clean Signal with privacy-reviewed examples'
git push -u origin "$BRANCH"
echo '[PASS] Release branch pushed. Review CI and create a pull request before merging to main.'
echo "https://github.com/$REPO/compare/main...$BRANCH?expand=1"
