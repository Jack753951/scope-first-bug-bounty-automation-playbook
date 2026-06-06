#!/usr/bin/env python3
"""Render dry-run candidate batches into a compact operator inbox summary."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except Exception:  # pragma: no cover
    Draft202012Validator = None  # type: ignore[assignment]

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SCHEMA = ROOT / "schemas" / "operator_inbox_candidate.schema.json"


def load_json(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def make_error(errors: list[str]) -> dict[str, Any]:
    return {
        "status": "error",
        "target_touching": False,
        "candidate_count": 0,
        "errors": errors,
    }


def validate_batch(batch: dict[str, Any], schema_path: Path) -> list[str]:
    errors: list[str] = []
    if Draft202012Validator is not None:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        for err in sorted(validator.iter_errors(batch), key=lambda e: list(e.path)):
            where = "/".join(str(p) for p in err.path) or "<root>"
            errors.append(f"{where}: {err.message}")
    if batch.get("target_touching") is not False:
        errors.append("batch target_touching must be false")
    if batch.get("mode") != "dry_run_no_target":
        errors.append("batch mode must be dry_run_no_target")
    return errors


def render_markdown(batch: dict[str, Any]) -> str:
    lines = [
        "# Operator Inbox",
        "",
        "Status: dry-run candidate summary",
        "Target touching: false",
        "Live activation allowed: false",
        "",
        f"Candidate count: {batch.get('candidate_count', 0)}",
        "",
    ]
    for idx, candidate in enumerate(batch.get("candidates", []), start=1):
        safety = candidate.get("safety", {})
        lines.extend([
            f"## {idx}. {candidate.get('title')}",
            "",
            f"Decision: {candidate.get('operator_decision')}",
            f"Machine state: {candidate.get('machine_state')}",
            f"Source: {candidate.get('source_kind')} / {candidate.get('source_id')}",
            f"Technology: {candidate.get('affected_technology', 'unknown')}",
            "",
            str(candidate.get("summary", "")),
            "",
            f"Recommended next step: {candidate.get('recommended_next_step')}",
            "",
            "Safety:",
            f"- Target touching: {str(safety.get('target_touching')).lower()}",
            f"- Live activation allowed: {str(safety.get('live_activation_allowed')).lower()}",
            f"- Requires policy/scope gate: {str(safety.get('requires_policy_scope_gate')).lower()}",
            f"- Blocked actions: {', '.join(safety.get('blocked_actions', []))}",
            "",
            "References:",
        ])
        refs = candidate.get("references") or []
        if refs:
            lines.extend(f"- {ref}" for ref in refs)
        else:
            lines.append("- none")
        lines.append("")
    lines.append("Boundary: This inbox is generated from offline/passive dry-run input and does not authorize live target contact, scans, proof execution, account mutation, report promotion, or submission.")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render operator inbox summary from candidate batch")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--schema", default=str(DEFAULT_SCHEMA))
    args = parser.parse_args(argv)

    try:
        batch = load_json(args.input)
        errors = validate_batch(batch, Path(args.schema))
        if errors:
            result = make_error(errors)
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return 1
        md = render_markdown(batch)
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(md, encoding="utf-8")
        result = {
            "status": "ok",
            "target_touching": False,
            "candidate_count": len(batch.get("candidates", [])),
            "out": str(out_path),
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except Exception as exc:
        result = make_error([f"input error: {exc}"])
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
