#!/usr/bin/env python3
"""Fail-closed public export scanner.

This is intentionally conservative. Review any hit before publishing.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

PATTERNS = {
    "private_host_path": re.compile(r"C:\\\\Users\\\\|/home/[^/]+|/Users/[^/]+"),
    "lab_ip": re.compile(r"\b10\.\d+\.\d+\.\d+\b|\b172\.(1[6-9]|2\d|3[0-1])\.\d+\.\d+\b|\b192\.168\.\d+\.\d+\b"),
    "private_key": re.compile(r"BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY"),
    "github_token": re.compile(r"gh[pousr]_[A-Za-z0-9_]+"),
    "openai_like_key": re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    "secret_words": re.compile(r"\b(refresh_token|access_token|client_secret|token\.json|cookie|password|otp)\b", re.I),
    "specific_advisory": re.compile(r"\bCVE-20\d{2}-\d{4,7}\b|\bGHSA-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}\b", re.I),
    "private_program_placeholder_missed": re.compile(r"\b(hackerone|intigriti|bugcrowd)\b", re.I),
}
ALLOWLIST = {
    "scripts/public_safety_scan.py": {"private_host_path", "github_token", "openai_like_key", "secret_words", "specific_advisory", "private_program_placeholder_missed", "lab_ip"},
    "README.md": {"secret_words"},
    "docs/01-safety-contract.md": {"secret_words"},
    "docs/02-agent-operating-model.md": {"secret_words"},
    "docs/03-memory-and-handoff-governance.md": {"secret_words"},
    "docs/05-authorized-live-target-dry-run.md": {"secret_words"},
    "docs/06-evidence-redaction-and-report-readiness.md": {"secret_words"},
    "docs/08-public-export-safety.md": {"secret_words", "private_program_placeholder_missed"},
    "templates/operator_gate_card.template.md": {"secret_words"},
    "templates/evidence_packet.template.md": {"secret_words"},
}
TEXT_SUFFIXES = {".md", ".py", ".json", ".yml", ".yaml", ".txt"}

def main(root: str = ".") -> int:
    base = Path(root)
    hits = []
    for path in sorted(base.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if ".git" in path.parts:
            continue
        rel = path.relative_to(base).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        allowed = ALLOWLIST.get(rel, set())
        for lineno, line in enumerate(text.splitlines(), 1):
            for name, rx in PATTERNS.items():
                if name in allowed:
                    continue
                if rx.search(line):
                    hits.append((rel, lineno, name, line.strip()[:180]))
    if hits:
        print("PUBLIC SAFETY SCAN FAILED")
        for rel, lineno, name, snippet in hits:
            print(f"{rel}:{lineno}: {name}: {snippet}")
        return 1
    print("PUBLIC SAFETY SCAN PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
