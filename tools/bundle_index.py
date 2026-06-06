#!/usr/bin/env python3
"""Index Cybersec Lab proof bundles for metadata-only freshness checks.

This tool is intentionally offline-only. It reads local Markdown bundle docs,
extracts lightweight coverage metadata, and never touches targets, scanners,
browsers, noVNC, recon, or external networks.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BUNDLE_DIR = ROOT / "modules" / "bundles"

CLASS_PATTERNS: list[tuple[str, str]] = [
    (r"\bssrf\b|server-side request forgery", "ssrf"),
    (r"\bxxe\b|xml external entity", "xxe"),
    (r"path traversal|directory traversal|file[- ]?read|arbitrary file", "file-read/path-traversal"),
    (r"deseriali[sz]ation|pickle|unserialize", "deserialization"),
    (r"command injection|remote code execution|\brce\b|code execution", "rce/command-execution"),
    (r"sql injection|\bsqli\b", "sqli"),
    (r"cross-site scripting|\bxss\b", "xss"),
    (r"idor|bola|object ownership|authorization bypass|authentication bypass|access control|role separation|privilege escalation", "auth/access-control"),
    (r"open redirect|redirect", "redirect"),
    (r"upload|zip slip|archive extraction", "upload/archive"),
    (r"api docs|metrics|headers|cors|directory listing|metadata|fingerprint", "exposure/metadata"),
]

FIELD_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_ -]*):\s*(.*?)\s*$")
CVE_RE = re.compile(r"\bCVE-\d{4}-\d{4,}\b", re.I)
GHSA_RE = re.compile(r"\bGHSA-[0-9A-Za-z]{4}-[0-9A-Za-z]{4}-[0-9A-Za-z]{4}\b")
DATE_RE = re.compile(r"\b(20\d{2}-\d{2}-\d{2}|20\d{6}(?:T\d{6}Z)?)\b")


def _split_list(value: str) -> list[str]:
    value = value.strip()
    if not value:
        return []
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    parts = [part.strip().strip("'\"") for part in re.split(r"[,;]", value)]
    return [part for part in parts if part]


def _unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out


def _fields_from_text(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.splitlines()[:80]:
        match = FIELD_RE.match(line.strip())
        if not match:
            continue
        key = match.group(1).strip().lower().replace(" ", "_").replace("-", "_")
        fields[key] = match.group(2).strip()
    return fields


def _title_from_text(path: Path, text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip() or path.stem
    return path.stem.replace("_", " ")


def infer_classes(path: Path, text: str, fields: dict[str, str]) -> list[str]:
    explicit = fields.get("vuln_classes") or fields.get("vuln_class")
    if explicit:
        return _unique(_split_list(explicit))
    haystack = f"{path.stem} {text[:4000]}"
    labels = [label for pattern, label in CLASS_PATTERNS if re.search(pattern, haystack, re.I)]
    return _unique(labels) or ["unknown/review"]


def infer_maturity(path: Path, text: str, fields: dict[str, str]) -> str:
    status = fields.get("status", "").lower()
    stem = path.stem.lower()
    title = _title_from_text(path, text).lower()
    raw = " ".join([stem, status, title])
    if "attempted_not_verified" in raw or "attempted-not-verified" in raw:
        return "attempted_not_verified"
    if "verified_lab_flow" in raw or raw.startswith("verified") or " verified " in f" {raw} ":
        return "verified"
    if "valuable_candidate" in raw or "candidate" in raw:
        return "candidate"
    if "triage" in raw or "baseline" in raw or "metadata" in raw:
        return "triage"
    return "unknown"


def index_bundle(path: Path, root: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    fields = _fields_from_text(text)
    cve_refs = _unique([ref.upper() for ref in CVE_RE.findall(text)])
    ghsa_refs = _unique(GHSA_RE.findall(text))
    dates = DATE_RE.findall(text)
    item: dict[str, Any] = {
        "path": path.relative_to(root).as_posix() if path.is_relative_to(root) else path.as_posix(),
        "title": _title_from_text(path, text),
        "maturity": infer_maturity(path, text, fields),
        "vuln_classes": infer_classes(path, text, fields),
        "cve_refs": _unique(_split_list(fields.get("cve_refs", "")) + cve_refs),
        "ghsa_refs": _unique(_split_list(fields.get("ghsa_refs", "")) + ghsa_refs),
        "product_refs": _unique(_split_list(fields.get("product_refs", ""))),
        "last_verified": fields.get("last_verified", "") or (max(dates) if dates else ""),
        "safe_proof_posture": fields.get("safe_proof_posture", ""),
        "live_target_policy": fields.get("live_target_policy", ""),
        "coverage_terms": _unique(_split_list(fields.get("coverage_terms", "")) + [path.stem.replace("_", " ")]),
    }
    return item


def build_index(bundle_dir: Path) -> list[dict[str, Any]]:
    if not bundle_dir.exists():
        raise FileNotFoundError(f"bundle directory not found: {bundle_dir}")
    items = []
    for path in sorted(bundle_dir.glob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        items.append(index_bundle(path, ROOT))
    return items


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build offline proof bundle metadata index")
    parser.add_argument("--bundle-dir", type=Path, default=DEFAULT_BUNDLE_DIR)
    parser.add_argument("--out", type=Path, default=None, help="write JSON to path instead of stdout")
    args = parser.parse_args(argv)

    items = build_index(args.bundle_dir)
    payload = json.dumps(items, indent=2, ensure_ascii=False)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
