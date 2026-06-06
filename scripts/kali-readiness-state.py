#!/usr/bin/env python3
"""Seed, validate, and summarize local Kali readiness state artifacts.

V1 is file-only. It does not SSH, start VMs, change NAT, browse, or probe targets.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "kali_readiness_state.schema.json"
FORBIDDEN_ARGS = {"--target", "--url", "--host", "--scope", "--live"}


def reject_target_like_args(argv: list[str]) -> None:
    seen = []
    for arg in argv:
        if arg in FORBIDDEN_ARGS:
            seen.append(arg)
        elif any(arg.startswith(flag + "=") for flag in FORBIDDEN_ARGS):
            seen.append(arg.split("=", 1)[0])
    seen = sorted(set(seen))
    if seen:
        print(json.dumps({"status": "error", "target_touching_allowed": False, "exit_code": 30, "errors": [f"forbidden target-like argument: {arg}" for arg in seen]}, indent=2))
        raise SystemExit(30)


def load_schema() -> dict[str, Any]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def load_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def schema_errors(data: Any, label: str) -> list[str]:
    errors = []
    for error in sorted(Draft202012Validator(load_schema()).iter_errors(data), key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in error.path) or "<root>"
        errors.append(f"{label}:{where}: {error.message}")
    return errors


def semantic_errors(data: dict[str, Any], label: str) -> list[str]:
    errors: list[str] = []
    checks = {c["name"]: c for c in data.get("checks", [])}
    if data.get("readiness") == "ready":
        for required in ["host_only_network", "nat_closed", "project_mount"]:
            if checks.get(required, {}).get("status") != "pass":
                errors.append(f"{label}: readiness=ready requires {required}=pass")
        failed = [c["name"] for c in data.get("checks", []) if c.get("status") == "fail"]
        if failed:
            errors.append(f"{label}: readiness=ready cannot include failed checks: {', '.join(failed)}")
    if data.get("target_touching_allowed") is not False:
        errors.append(f"{label}: target_touching_allowed must remain false")
    return errors


def cmd_validate(args: argparse.Namespace) -> int:
    data = load_json(args.input)
    errors = schema_errors(data, args.input)
    if not errors:
        errors.extend(semantic_errors(data, args.input))
    print(json.dumps({"status": "error" if errors else "ok", "target_touching_allowed": False, "errors": errors}, indent=2, ensure_ascii=False))
    return 1 if errors else 0


def cmd_summarize(args: argparse.Namespace) -> int:
    data = load_json(args.input)
    errors = schema_errors(data, args.input)
    if not errors:
        errors.extend(semantic_errors(data, args.input))
    if errors:
        print(json.dumps({"status": "error", "target_touching_allowed": False, "errors": errors}, indent=2, ensure_ascii=False))
        return 1
    print(json.dumps({"status": "ok", "profile": data["profile"], "readiness": data["readiness"], "blockers": data["blockers"], "warnings": data["warnings"], "next_action": data["next_action"], "target_touching_allowed": False}, indent=2, ensure_ascii=False))
    return 0


def cmd_seed(args: argparse.Namespace) -> int:
    now = date.today().isoformat()
    data = {
        "schema_version": "1.0",
        "profile": args.profile,
        "checked_at": now,
        "readiness": "unknown",
        "target_touching_allowed": False,
        "checks": [
            {"name": "project_mount", "status": "unknown", "evidence": "seeded placeholder; no VM/SSH/browser probe executed", "command_safe_to_rerun": True},
            {"name": "nat_closed", "status": "unknown", "evidence": "seeded placeholder; no VirtualBox or network command executed", "command_safe_to_rerun": True}
        ],
        "conditions": [{"type": "KaliReady", "status": "Unknown", "reason": "SeedOnly", "message": "Placeholder state created without probing VM or network", "last_transition_time": now}],
        "blockers": ["readiness state is seed-only; run an approved local precheck before any live work"],
        "warnings": [],
        "next_action": "local_precheck"
    }
    errors = schema_errors(data, "seed") + semantic_errors(data, "seed")
    if errors:
        print(json.dumps({"status": "error", "target_touching_allowed": False, "errors": errors}, indent=2, ensure_ascii=False))
        return 1
    if args.out:
        Path(args.out).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    reject_target_like_args(argv)
    parser = argparse.ArgumentParser(description="Offline Kali readiness state helper")
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate")
    validate.add_argument("--input", required=True)
    validate.set_defaults(func=cmd_validate)
    summarize = sub.add_parser("summarize")
    summarize.add_argument("--input", required=True)
    summarize.set_defaults(func=cmd_summarize)
    seed = sub.add_parser("seed")
    seed.add_argument("--profile", choices=["windows-control", "<attacker-vm>", "<victim-vm>", "other"], required=True)
    seed.add_argument("--out")
    seed.set_defaults(func=cmd_seed)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
