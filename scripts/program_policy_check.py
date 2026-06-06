#!/usr/bin/env python3
"""Offline CLI for program policy allow/deny decisions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.core.policy import decide_program_policy


def _print_text(payload: dict) -> None:
    for key in (
        "verdict",
        "program_slug",
        "target",
        "normalized_target",
        "target_type",
        "technique",
        "mode",
        "audit_event",
    ):
        print(f"{key}: {payload[key]}")
    for key in ("reasons", "errors", "warnings"):
        values = payload[key]
        if values:
            print(f"{key}:")
            for item in values:
                print(f"  - {item}")
        else:
            print(f"{key}: []")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Offline default-deny program policy decision helper.",
    )
    parser.add_argument("--program", required=True, help="Path to program scope JSON.")
    parser.add_argument(
        "--global-scope",
        default="config/scope.txt",
        help="Path to global scope allowlist. Default: config/scope.txt",
    )
    parser.add_argument("--target", required=True, help="Target domain, URL, IPv4, or IPv4 CIDR.")
    parser.add_argument("--technique", required=True, help="Technique tag to evaluate.")
    parser.add_argument(
        "--mode",
        choices=("dry-run", "planned", "live"),
        default="dry-run",
        help="Decision mode. Default: dry-run",
    )
    parser.add_argument("--json", action="store_true", help="Print structured JSON output.")
    parser.add_argument(
        "--ignore-time",
        action="store_true",
        help="Forwarded to the program scope validator for stable tests/examples.",
    )
    args = parser.parse_args(argv)

    decision = decide_program_policy(
        program_path=args.program,
        global_scope_path=args.global_scope,
        target=args.target,
        technique=args.technique,
        mode=args.mode,
        ignore_time=args.ignore_time,
    )
    payload = decision.as_dict()
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        _print_text(payload)
    return 0 if decision.verdict == "allow" else 1


if __name__ == "__main__":
    raise SystemExit(main())

