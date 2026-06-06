#!/usr/bin/env python3
"""Offline importer for Wave 1A metadata adapter observations.

Reads reviewed/committed JSONL output produced by scripts/lab_modules/wave1a_metadata.py
and normalizes it into non-promotional observations plus manual-review candidate
seeds. It performs no network I/O, subprocess execution, target interaction, or
report/finding promotion.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

SCHEMA_VERSION = "wave1a_metadata_observations/0.1-trial"
ALLOWED_PREFIX = ("tests", "fixtures", "wave1a_metadata")
FORBIDDEN_PROMOTIONS = {"confirmed", "verified", "reportable", "accepted"}
CANDIDATE_MODULES = {
    "level1.directory_listing_metadata": "directory_listing_candidate",
    "level1.api_docs_metadata": "api_docs_candidate",
}


def _error(code: str, message: str, *, input_path: str | None = None) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "error",
        "input_path": input_path,
        "summary": {"imported_count": 0, "dropped_count": 0, "candidate_seed_count": 0, "error_count": 1},
        "observations": [],
        "candidate_seeds": [],
        "errors": [{"code": code, "message": message}],
        "safety": _safety(),
    }


def _safety() -> dict[str, bool]:
    return {
        "network_io": False,
        "subprocess_execution": False,
        "target_touching": False,
        "promotes_findings": False,
        "report_submission": False,
        "imports_raw_bodies": False,
    }


def _is_abs_or_drive(value: str) -> bool:
    return value.startswith("/") or bool(PureWindowsPath(value).drive)


def _resolve_allowed_input(repo_root: Path, rel_path: str) -> tuple[Path | None, dict[str, Any] | None]:
    if not isinstance(rel_path, str) or not rel_path:
        return None, _error("INPUT_PATH_NOT_ALLOWED", "input path must be a non-empty repo-relative string", input_path=rel_path)
    if "\x00" in rel_path or "\\" in rel_path or "://" in rel_path or _is_abs_or_drive(rel_path):
        return None, _error("INPUT_PATH_NOT_ALLOWED", "input path must be a safe repo-relative Wave 1A JSONL fixture path", input_path=rel_path)
    pure = PurePosixPath(rel_path)
    parts = pure.parts
    if any(part in ("", ".", "..") for part in parts):
        return None, _error("INPUT_PATH_NOT_ALLOWED", "input path must not contain traversal segments", input_path=rel_path)
    if len(parts) != 4 or parts[: len(ALLOWED_PREFIX)] != ALLOWED_PREFIX or not parts[-1].endswith(".jsonl"):
        return None, _error("INPUT_PATH_NOT_ALLOWED", "input path is not in tests/fixtures/wave1a_metadata/*.jsonl", input_path=rel_path)
    root = repo_root.resolve(strict=False)
    candidate = root.joinpath(*parts).resolve(strict=False)
    try:
        candidate.relative_to(root)
    except ValueError:
        return None, _error("INPUT_PATH_NOT_ALLOWED", "input path resolves outside repo root", input_path=rel_path)
    if not candidate.exists() or not candidate.is_file():
        return None, _error("INPUT_PATH_NOT_FOUND", "input JSONL file does not exist", input_path=rel_path)
    return candidate, None


def _sha256_line(line: str) -> str:
    return hashlib.sha256(line.encode("utf-8", errors="replace")).hexdigest()


def _as_int(value: Any) -> int | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int):
        return value
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return None


def _observation(raw: dict[str, Any], *, line_no: int, line_hash: str, run_id: str) -> dict[str, Any] | None:
    if raw.get("schema_version") != "observation/0.1-trial":
        return None
    url = raw.get("url")
    if not isinstance(url, str) or not url.startswith(("http://", "https://")):
        return None
    kind = raw.get("kind") if isinstance(raw.get("kind"), str) else "metadata_observation"
    module_id = raw.get("module_id") if isinstance(raw.get("module_id"), str) else None
    path = raw.get("path") if isinstance(raw.get("path"), str) else None
    return {
        "id": f"wave1a:{line_hash[:16]}",
        "status": "observation",
        "relationship": kind,
        "run_id": run_id,
        "source_line": {"number": line_no, "sha256": line_hash},
        "module_id": module_id,
        "step_id": raw.get("step_id") if isinstance(raw.get("step_id"), str) else None,
        "target": {"url": url, "path": path},
        "http": {
            "status_code": _as_int(raw.get("http_status")),
            "content_type": raw.get("content_type") if isinstance(raw.get("content_type"), str) else None,
            "title": raw.get("title") if isinstance(raw.get("title"), str) else None,
            "body_size": _as_int(raw.get("body_size")),
            "body_sha256": raw.get("body_sha256") if isinstance(raw.get("body_sha256"), str) else None,
        },
        "cors": {
            "origin": raw.get("origin") if isinstance(raw.get("origin"), str) else None,
            "access_control_allow_origin": raw.get("access_control_allow_origin") if isinstance(raw.get("access_control_allow_origin"), str) else None,
            "access_control_allow_credentials": raw.get("access_control_allow_credentials") if isinstance(raw.get("access_control_allow_credentials"), str) else None,
        },
        "flags": {
            "directory_listing_candidate": raw.get("directory_listing_candidate") is True,
        },
        "scanner_output_only": True,
        "manual_review_required": True,
        "notes": ["Imported offline from Wave 1A metadata JSONL; observation only, not a finding."],
    }


def _candidate_seed(observation: dict[str, Any]) -> dict[str, Any] | None:
    module_id = observation.get("module_id")
    relationship = CANDIDATE_MODULES.get(module_id)
    if relationship is None:
        return None
    status_code = observation.get("http", {}).get("status_code") if isinstance(observation.get("http"), dict) else None
    if status_code != 200:
        return None
    if relationship == "directory_listing_candidate" and not observation.get("flags", {}).get("directory_listing_candidate"):
        return None
    return {
        "id": f"seed:{observation['id'].split(':', 1)[1]}",
        "status": "needs_manual_review",
        "relationship": relationship,
        "run_id": observation["run_id"],
        "source_observation_id": observation["id"],
        "module_id": module_id,
        "target": observation["target"],
        "reason": "HTTP 200 metadata lead requires manual verification before finding/report workflow.",
        "scanner_output_only": True,
        "manual_verification_required": True,
        "not_a_finding": True,
    }


def _check_no_promotional_status(payload: dict[str, Any]) -> None:
    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key == "status" and isinstance(child, str) and child.lower() in FORBIDDEN_PROMOTIONS:
                    raise ValueError(f"forbidden promotional status: {child}")
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
    walk(payload)


def import_observations(repo_root: Path | str, input_path: str, *, run_id: str = "wave1a-import") -> dict[str, Any]:
    repo_root = Path(repo_root)
    source_path, err = _resolve_allowed_input(repo_root, input_path)
    if err:
        return err
    assert source_path is not None

    observations: list[dict[str, Any]] = []
    candidate_seeds: list[dict[str, Any]] = []
    dropped = 0
    lines = source_path.read_text(encoding="utf-8").splitlines()
    for line_no, line in enumerate(lines, 1):
        if not line.strip():
            dropped += 1
            continue
        line_hash = _sha256_line(line)
        try:
            raw = json.loads(line)
        except json.JSONDecodeError as exc:
            return {
                "schema_version": SCHEMA_VERSION,
                "status": "error",
                "input_path": input_path,
                "summary": {"imported_count": 0, "dropped_count": dropped, "candidate_seed_count": 0, "error_count": 1},
                "observations": [],
                "candidate_seeds": [],
                "errors": [{"code": "JSONL_PARSE_ERROR", "line": line_no, "message": str(exc)}],
                "safety": _safety(),
            }
        if not isinstance(raw, dict):
            dropped += 1
            continue
        obs = _observation(raw, line_no=line_no, line_hash=line_hash, run_id=run_id)
        if obs is None:
            dropped += 1
            continue
        observations.append(obs)
        seed = _candidate_seed(obs)
        if seed is not None:
            candidate_seeds.append(seed)

    payload = {
        "schema_version": SCHEMA_VERSION,
        "status": "ok",
        "input_path": input_path,
        "summary": {
            "imported_count": len(observations),
            "dropped_count": dropped,
            "candidate_seed_count": len(candidate_seeds),
            "error_count": 0,
        },
        "observations": observations,
        "candidate_seeds": candidate_seeds,
        "errors": [],
        "safety": _safety(),
    }
    _check_no_promotional_status(payload)
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Import offline Wave 1A metadata JSONL into non-promotional observations/candidate seeds")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--input", required=True)
    parser.add_argument("--run-id", default="wave1a-import")
    args = parser.parse_args(argv)
    payload = import_observations(Path(args.repo_root), args.input, run_id=args.run_id)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload.get("status") == "ok" else 2


if __name__ == "__main__":
    raise SystemExit(main())
