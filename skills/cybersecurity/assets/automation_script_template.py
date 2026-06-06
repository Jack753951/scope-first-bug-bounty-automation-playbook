#!/usr/bin/env python3
"""
{TOOL_NAME} — one-line description

Scaffold for new security automation tools. Copy this file, rename, and
fill in the four numbered sections below. Standard library only by default.

Conventions
===========
* Legality banner before any active operation.
* argparse with --yes for non-interactive use.
* Output to JSON + Markdown in the same directory.
* Subprocess calls always pass list (never shell=True).
* Timeouts on every subprocess and network call.
* Errors aggregate into result.errors instead of raising.

Usage
=====
    python3 {tool}.py <target> -o ./out
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path


# ------------------------------------------------------------------
# 1. Result data model — define what your tool produces
# ------------------------------------------------------------------

@dataclass
class Result:
    target: str
    timestamp: str
    findings: list = field(default_factory=list)
    errors: list = field(default_factory=list)


# ------------------------------------------------------------------
# Helpers (do not edit unless you have a reason)
# ------------------------------------------------------------------

def have(tool: str) -> bool:
    return shutil.which(tool) is not None


def run(cmd: list[str], timeout: int = 600) -> tuple[int, str, str]:
    """Subprocess wrapper that never raises on subprocess errors."""
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, check=False
        )
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return -1, "", f"Timeout after {timeout}s: {' '.join(cmd)}"
    except FileNotFoundError as e:
        return -1, "", f"Not found: {e}"


# ------------------------------------------------------------------
# 2. Core logic — implement the actual scanning / parsing here
# ------------------------------------------------------------------

def collect(target: str, result: Result) -> None:
    """Fill in your collection logic.

    Example pattern:
        if not have("some-tool"):
            result.errors.append("some-tool not installed")
            return
        rc, out, err = run(["some-tool", "-flag", target], timeout=300)
        if rc != 0:
            result.errors.append(f"some-tool rc={rc}: {err.strip()[:200]}")
            return
        for line in out.splitlines():
            # parse line into a finding
            result.findings.append({"raw": line.strip()})
    """
    raise NotImplementedError("Fill in collect() before running.")


# ------------------------------------------------------------------
# 3. Output formatters
# ------------------------------------------------------------------

def to_markdown(r: Result) -> str:
    lines = [
        f"# {r.target} — Report",
        f"_Generated: {r.timestamp}_\n",
        f"## Findings ({len(r.findings)})\n",
    ]
    for i, f in enumerate(r.findings, 1):
        lines.append(f"{i}. `{f}`")
    if r.errors:
        lines += ["\n## Errors / warnings\n", *(f"- {e}" for e in r.errors)]
    lines.append("\n---\n_Reminder: only run on authorized targets._")
    return "\n".join(lines)


# ------------------------------------------------------------------
# 4. CLI
# ------------------------------------------------------------------

LEGAL_NOTICE = """\
================ LEGAL NOTICE ================
This tool may send active probes. Use only against:
  (a) systems you own,
  (b) targets under written authorization, or
  (c) legal practice ranges.
==============================================
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="{TOOL_NAME}")
    ap.add_argument("target", help="Target IP / domain / URL")
    ap.add_argument("-o", "--out", default="./out", help="Output directory")
    ap.add_argument("--yes", action="store_true", help="Skip interactive legality check")
    args = ap.parse_args()

    print(LEGAL_NOTICE)
    if not args.yes:
        ans = input("Proceed? (yes/N) ").strip().lower()
        if ans != "yes":
            print("Aborted.")
            return 1

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    result = Result(
        target=args.target,
        timestamp=dt.datetime.utcnow().isoformat() + "Z",
    )

    print(f"[*] Scanning {args.target} ...")
    try:
        collect(args.target, result)
    except NotImplementedError as e:
        print(f"[!] {e}")
        return 2

    json_path = out_dir / f"{args.target.replace('/', '_')}.json"
    md_path = out_dir / f"{args.target.replace('/', '_')}.md"
    json_path.write_text(json.dumps(asdict(result), indent=2, ensure_ascii=False))
    md_path.write_text(to_markdown(result))

    print(f"[+] Done.")
    print(f"    JSON     : {json_path}")
    print(f"    Markdown : {md_path}")
    print(f"    Findings : {len(result.findings)}, Errors: {len(result.errors)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
