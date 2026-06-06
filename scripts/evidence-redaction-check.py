#!/usr/bin/env python3
"""Fail-closed redaction check for live-bounty evidence artifacts.

The checker is intentionally lightweight and local-only: it scans files for common
secret/PII/token patterns before artifacts are promoted into handoff memory.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

PATTERNS = [
    ("authorization_header", re.compile(r"(?im)^\s*authorization\s*:\s*\S+")),
    ("set_cookie", re.compile(r"(?im)^\s*set-cookie\s*:\s*.+")),
    ("bearer_token", re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{16,}")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{2,}\b")),
    ("api_key_like", re.compile(r"(?i)\b(api[_-]?key|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{16,}")),
    ("email_address", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)),
    ("phone_like", re.compile(r"(?<![\d-])(?:\+?\d[\d .()]{8,}\d)(?![\d-])")),
    ("otp_like", re.compile(r"(?i)\b(otp|verification code|2fa|mfa)\b[^\n\r]{0,40}\b\d{4,8}\b")),
]


def iter_text_files(paths: Iterable[Path]) -> Iterable[Path]:
    for path in paths:
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.is_file():
                    yield child
        elif path.is_file():
            yield path
        else:
            raise FileNotFoundError(str(path))


def redact_line(line: str) -> str:
    redacted = line
    redacted = re.sub(r"(?im)^\s*authorization\s*:\s*.*$", "Authorization: <REDACTED_AUTHORIZATION>", redacted)
    redacted = re.sub(r"(?im)^\s*set-cookie\s*:\s*.*$", "Set-Cookie: <REDACTED_COOKIE>", redacted)
    redacted = re.sub(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{6,}", "Bearer <REDACTED_BEARER>", redacted)
    redacted = re.sub(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{2,}\b", "<REDACTED_JWT>", redacted)
    redacted = re.sub(r"(?i)(\b(?:api[_-]?key|secret|token)\s*[:=]\s*)['\"]?[A-Za-z0-9_./+=-]{6,}", r"\1<REDACTED_SECRET>", redacted)
    redacted = re.sub(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", "<REDACTED_EMAIL>", redacted, flags=re.I)
    redacted = re.sub(r"(?<![\d-])(?:\+?\d[\d .()]{8,}\d)(?![\d-])", "<REDACTED_PHONE>", redacted)
    redacted = re.sub(r"(?i)(\b(?:otp|verification code|2fa|mfa)\b[^\n\r]{0,40})\b\d{4,8}\b", r"\1<REDACTED_OTP>", redacted)
    cleaned = re.sub(r"\s+", " ", redacted.strip())
    return cleaned[:160]


def scan_file(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8", errors="replace")
    findings = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for kind, pattern in PATTERNS:
            if pattern.search(line):
                excerpt = redact_line(line)
                findings.append({
                    "file": str(path),
                    "line": line_no,
                    "kind": kind,
                    "excerpt": excerpt,
                })
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check evidence files for secrets/PII before promotion")
    parser.add_argument("paths", nargs="+", help="Files or directories to scan")
    parser.add_argument("--json", action="store_true", help="Emit JSON result")
    args = parser.parse_args(argv)

    all_findings: list[dict] = []
    try:
        for file_path in iter_text_files(Path(p) for p in args.paths):
            all_findings.extend(scan_file(file_path))
    except Exception as exc:  # fail closed
        result = {"status": "error", "error": str(exc), "findings": all_findings}
        print(json.dumps(result, indent=2, ensure_ascii=False) if args.json else result)
        return 2

    status = "blocked" if all_findings else "clean"
    result = {"status": status, "findings": all_findings}
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"status={status} findings={len(all_findings)}")
        for finding in all_findings:
            print(f"{finding['file']}:{finding['line']} {finding['kind']}: {finding['excerpt']}")
    return 1 if all_findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
