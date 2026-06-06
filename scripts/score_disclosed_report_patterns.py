#!/usr/bin/env python3
"""Score reusable disclosed-report patterns from sanitized offline records.

The output is candidate-only intelligence. It never authorizes live target contact,
proof testing, scanning, or report-ready promotion.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

DEFAULT_BLOCKED_BEFORE = [
    "scope_and_lane_gate_required",
    "owned_data_proof_boundary_required",
    "local_fixture_or_lab_proof_before_live_use",
    "no_customer_or_non_owned_data",
    "no_finding_promotion_from_pattern_score",
]


def _records_from_payload(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict) and isinstance(payload.get("records"), list):
        return payload["records"]
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        return [payload]
    raise ValueError("Unsupported disclosed-report pattern input shape")


def _add(counter: Counter[str], examples: dict[str, list[str]], pattern_id: str, record: dict[str, Any]) -> None:
    counter[pattern_id] += 1
    example = str(record.get("url") or record.get("title") or "unknown")
    if example not in examples[pattern_id]:
        examples[pattern_id].append(example)


def score_patterns(records: list[dict[str, Any]]) -> dict[str, Any]:
    counter: Counter[str] = Counter()
    examples: dict[str, list[str]] = defaultdict(list)
    for record in records:
        if record.get("status") != "ok" or record.get("source_visibility") != "public":
            continue
        for primitive in record.get("primitives") or []:
            _add(counter, examples, f"primitive:{primitive}", record)
        for vuln_class in record.get("vulnerability_classes") or []:
            _add(counter, examples, f"class:{vuln_class}", record)
        for surface in record.get("product_surface_keywords") or []:
            _add(counter, examples, f"surface:{surface}", record)
        for proof_shape in record.get("proof_shapes") or []:
            _add(counter, examples, f"proof:{proof_shape}", record)

    patterns = []
    for pattern_id, count in sorted(counter.items(), key=lambda item: (-item[1], item[0])):
        category, _, name = pattern_id.partition(":")
        score = min(10, 2 + count * 2 + (2 if category == "primitive" else 0))
        patterns.append({
            "pattern_id": pattern_id,
            "category": category,
            "name": name,
            "status": "candidate_pattern",
            "source_count": count,
            "score_0_10": score,
            "examples": examples[pattern_id][:5],
            "blocked_before": DEFAULT_BLOCKED_BEFORE,
            "recommended_next_step": "Use as passive lane-scoring input or build a local fixture proof before any live program action.",
        })

    return {
        "schema_version": "disclosed_report_patterns/0.1",
        "target_touching": False,
        "boundary": "No live target contact is authorized by this candidate pattern score. Scope, lane, owned-data, and local-proof gates still apply.",
        "pattern_count": len(patterns),
        "patterns": patterns,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Score reusable patterns from sanitized disclosed-report records.")
    parser.add_argument("--input", required=True, help="Normalized disclosed report batch JSON")
    parser.add_argument("--output", required=True, help="Output pattern score JSON")
    args = parser.parse_args(argv)

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = score_patterns(_records_from_payload(payload))
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out_path} patterns={result['pattern_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
