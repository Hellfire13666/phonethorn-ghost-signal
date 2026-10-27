#!/usr/bin/env python3
"""Read-only source privacy checks. Never print matching content or host identity."""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH_PATTERN = re.compile(r"/(?:home|Users)/([A-Za-z0-9_.-]+)/")
TOKEN_PATTERN = re.compile(r"(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})")
KEY_PATTERN = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")
ALLOWED_NAMES = {"example", "exampleuser", "user", "username", "testuser", "runner", "demo"}
TEXT_EXT = {".py",".sh",".md",".txt",".toml",".yml",".yaml",".json",".ini",".cfg",".desktop",".html",".css",".js"}
MAX_SIZE = 1_000_000

def files():
    if (ROOT / ".git").exists():
        result = subprocess.run(["git", "-C", str(ROOT), "ls-files", "-z"], capture_output=True, check=True)
        return [ROOT / v.decode("utf-8","surrogateescape") for v in result.stdout.split(b"\0") if v]
    return [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts and ".venv" not in p.parts]

def check():
    errors = []
    for path in files():
        if not path.is_file() or path.suffix.lower() not in TEXT_EXT or path.stat().st_size > MAX_SIZE:
            continue
        try:
            contents = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError):
            continue
        for number, line in enumerate(contents.splitlines(), 1):
            bad_path = any(m.group(1).lower() not in ALLOWED_NAMES for m in PATH_PATTERN.finditer(line))
            if bad_path or TOKEN_PATTERN.search(line) or KEY_PATTERN.search(line):
                errors.append((path.relative_to(ROOT), number))
    for path, number in errors:
        print(f"[REVIEW] {path}:{number} — potentially sensitive text (content suppressed)")
    if errors:
        print(f"[STOP] {len(errors)} candidate exposures. Review locally before publishing.")
        return 1
    print("[PASS] No matching private paths, token-shaped strings or private-key headers in inspected text.")
    print("[NOTE] Working-tree check only; inspect history, files in binary formats, and release archives separately.")
    return 0

if __name__ == "__main__":
    raise SystemExit(check())
