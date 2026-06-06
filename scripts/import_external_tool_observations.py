#!/usr/bin/env python3
"""Offline importer for mature external web-recon tool observations.

Trial-only Phase 4A adapter. This script reads committed JSONL fixtures or
reviewed local tool-output captures and normalizes selected safe fields into
observation records. It does not execute tools, open network connections,
follow URLs, import response bodies, or promote scanner output to findings.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

SCHEMA_VERSION = "external_tool_observations/0.1-trial"
SUPPORTED_TOOLS = {"httpx", "katana", "nuclei", "ffuf"}
ALLOWED_PREFIX = ("tests", "fixtures", "external_tools")
ALLOWED_SUFFIXES = (".jsonl", ".json")
FORBIDDEN_PROMOTIONS = {"confirmed", "verified", "reportable", "accepted"}


def _error(code: str, message: str, *, tool: str | None = None, input_path: str | None = None) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "error",
        "tool": tool,
        "input_path": input_path,
        "summary": {"imported_count": 0, "dropped_count": 0, "error_count": 1},
        "observations": [],
        "errors": [{"code": code, "message": message}],
    }


def _is_abs_or_drive(value: str) -> bool:
    return value.startswith("/") or bool(PureWindowsPath(value).drive)


def _resolve_allowed_input(repo_root: Path, rel_path: str) -> tuple[Path | None, dict[str, Any] | None]:
    if not isinstance(rel_path, str) or not rel_path:
        return None, _error("INPUT_PATH_NOT_ALLOWED", "input path must be a non-empty repo-relative string", input_path=rel_path)
    if "\x00" in rel_path or "\\" in rel_path or "://" in rel_path or _is_abs_or_drive(rel_path):
        return None, _error("INPUT_PATH_NOT_ALLOWED", "input path must be a safe repo-relative JSONL fixture path", input_path=rel_path)
    pure = PurePosixPath(rel_path)
    parts = pure.parts
    if any(part in ("", ".", "..") for part in parts):
        return None, _error("INPUT_PATH_NOT_ALLOWED", "input path must not contain traversal segments", input_path=rel_path)
    if len(parts) < 4 or parts[: len(ALLOWED_PREFIX)] != ALLOWED_PREFIX or not parts[-1].endswith(ALLOWED_SUFFIXES):
        return None, _error("INPUT_PATH_NOT_ALLOWED", "input path is not in tests/fixtures/external_tools/*.jsonl or *.json", input_path=rel_path)
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


def _httpx_observation(raw: dict[str, Any], *, line_no: int, line_hash: str, run_id: str) -> dict[str, Any] | None:
    url = raw.get("url") or raw.get("input")
    if not isinstance(url, str) or not url.startswith(("http://", "https://")):
        return None
    technologies = raw.get("tech")
    if not isinstance(technologies, list):
        technologies = []
    return {
        "id": f"httpx:{line_hash[:16]}",
        "status": "observation",
        "relationship": "http_service_metadata",
        "run_id": run_id,
        "tool": {"name": "httpx", "version": raw.get("version")},
        "source_line": {"number": line_no, "sha256": line_hash},
        "target": {"url": url, "host": raw.get("host"), "port": raw.get("port"), "scheme": raw.get("scheme")},
        "http": {
            "status_code": _as_int(raw.get("status_code")),
            "title": raw.get("title") if isinstance(raw.get("title"), str) else None,
            "webserver": raw.get("webserver") if isinstance(raw.get("webserver"), str) else None,
            "content_length": _as_int(raw.get("content_length")),
            "response_time": raw.get("response_time") if isinstance(raw.get("response_time"), str) else None,
        },
        "technologies": [str(item) for item in technologies[:20]],
        "scanner_output_only": True,
        "manual_review_required": True,
        "notes": ["Imported offline from httpx JSONL; not a finding and not reportable by itself."],
    }


def _katana_observation(raw: dict[str, Any], *, line_no: int, line_hash: str, run_id: str) -> dict[str, Any] | None:
    request = raw.get("request") if isinstance(raw.get("request"), dict) else {}
    response = raw.get("response") if isinstance(raw.get("response"), dict) else {}
    url = request.get("endpoint") or raw.get("url") or raw.get("endpoint")
    if not isinstance(url, str) or not url.startswith(("http://", "https://")):
        return None
    return {
        "id": f"katana:{line_hash[:16]}",
        "status": "observation",
        "relationship": "discovered_url",
        "run_id": run_id,
        "tool": {"name": "katana", "version": raw.get("version")},
        "source_line": {"number": line_no, "sha256": line_hash},
        "target": {"url": url},
        "source": {"url": raw.get("source") if isinstance(raw.get("source"), str) else None},
        "http": {
            "method": request.get("method") if isinstance(request.get("method"), str) else None,
            "status_code": _as_int(response.get("status_code") or raw.get("status_code")),
            "content_length": _as_int(response.get("content_length") or raw.get("content_length")),
        },
        "scanner_output_only": True,
        "manual_review_required": True,
        "notes": ["Imported offline from katana JSONL; importer does not follow discovered URLs."],
    }


def _nuclei_observation(raw: dict[str, Any], *, line_no: int, line_hash: str, run_id: str) -> dict[str, Any] | None:
    url = raw.get("matched-at") or raw.get("host") or raw.get("url")
    if not isinstance(url, str) or not url.startswith(("http://", "https://")):
        return None
    info = raw.get("info") if isinstance(raw.get("info"), dict) else {}
    severity = info.get("severity") if isinstance(info.get("severity"), str) else raw.get("severity")
    return {
        "id": f"nuclei:{line_hash[:16]}",
        "status": "observation",
        "relationship": "template_observation",
        "run_id": run_id,
        "tool": {"name": "nuclei", "version": raw.get("version")},
        "source_line": {"number": line_no, "sha256": line_hash},
        "target": {"url": url},
        "template": {
            "id": raw.get("template-id") if isinstance(raw.get("template-id"), str) else None,
            "name": info.get("name") if isinstance(info.get("name"), str) else None,
            "severity": severity if isinstance(severity, str) else None,
            "tags": info.get("tags") if isinstance(info.get("tags"), list) else [],
        },
        "scanner_output_only": True,
        "manual_review_required": True,
        "notes": ["Imported offline from bounded nuclei JSONL; template output is an observation, not a finding."],
    }


def _ffuf_observation(raw: dict[str, Any], *, line_no: int, line_hash: str, run_id: str) -> dict[str, Any] | None:
    url = raw.get("url")
    if not isinstance(url, str) or not url.startswith(("http://", "https://")):
        return None
    return {
        "id": f"ffuf:{line_hash[:16]}",
        "status": "observation",
        "relationship": "content_discovery_hit",
        "run_id": run_id,
        "tool": {"name": "ffuf", "version": raw.get("version")},
        "source_line": {"number": line_no, "sha256": line_hash},
        "target": {"url": url},
        "http": {
            "status_code": _as_int(raw.get("status")),
            "content_length": _as_int(raw.get("length")),
            "words": _as_int(raw.get("words")),
            "lines": _as_int(raw.get("lines")),
            "redirect_location": raw.get("redirectlocation") if isinstance(raw.get("redirectlocation"), str) else None,
        },
        "fuzz_input": raw.get("input") if isinstance(raw.get("input"), dict) else {},
        "scanner_output_only": True,
        "manual_review_required": True,
        "notes": ["Imported offline from tiny bounded ffuf JSON; discovered paths require manual review."],
    }


def _observation_for_tool(tool: str, raw: dict[str, Any], *, line_no: int, line_hash: str, run_id: str) -> dict[str, Any] | None:
    if tool == "httpx":
        return _httpx_observation(raw, line_no=line_no, line_hash=line_hash, run_id=run_id)
    if tool == "katana":
        return _katana_observation(raw, line_no=line_no, line_hash=line_hash, run_id=run_id)
    if tool == "nuclei":
        return _nuclei_observation(raw, line_no=line_no, line_hash=line_hash, run_id=run_id)
    if tool == "ffuf":
        return _ffuf_observation(raw, line_no=line_no, line_hash=line_hash, run_id=run_id)
    return None


def _ffuf_records(source_path: Path) -> tuple[list[tuple[int, str, dict[str, Any]]], dict[str, Any] | None]:
    text = source_path.read_text(encoding="utf-8")
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        return [], {"code": "JSON_PARSE_ERROR", "line": 1, "message": str(exc)}
    results = payload.get("results") if isinstance(payload, dict) else None
    if not isinstance(results, list):
        return [], {"code": "FFUF_RESULTS_NOT_LIST", "line": 1, "message": "ffuf JSON must contain results list"}
    records: list[tuple[int, str, dict[str, Any]]] = []
    for idx, item in enumerate(results, 1):
        if isinstance(item, dict):
            line = json.dumps(item, sort_keys=True, separators=(",", ":"))
            records.append((idx, line, item))
    return records, None


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


def import_observations(repo_root: Path | str, tool: str, input_path: str, *, run_id: str = "external-tool-import") -> dict[str, Any]:
    repo_root = Path(repo_root)
    if tool not in SUPPORTED_TOOLS:
        return _error("TOOL_NOT_SUPPORTED", f"tool must be one of: {', '.join(sorted(SUPPORTED_TOOLS))}", tool=tool, input_path=input_path)
    source_path, err = _resolve_allowed_input(repo_root, input_path)
    if err:
        err["tool"] = tool
        return err

    observations: list[dict[str, Any]] = []
    dropped = 0
    errors: list[dict[str, Any]] = []
    assert source_path is not None

    if tool == "ffuf":
        records, parse_error = _ffuf_records(source_path)
        if parse_error:
            return {
                "schema_version": SCHEMA_VERSION,
                "status": "error",
                "tool": tool,
                "input_path": input_path,
                "summary": {"imported_count": 0, "dropped_count": 0, "error_count": 1},
                "observations": [],
                "errors": [parse_error],
            }
        for line_no, line, raw in records:
            line_hash = _sha256_line(line)
            observation = _observation_for_tool(tool, raw, line_no=line_no, line_hash=line_hash, run_id=run_id)
            if observation is None:
                dropped += 1
            else:
                observations.append(observation)
    else:
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
                    "tool": tool,
                    "input_path": input_path,
                    "summary": {"imported_count": 0, "dropped_count": dropped, "error_count": 1},
                    "observations": [],
                    "errors": [{"code": "JSONL_PARSE_ERROR", "line": line_no, "message": str(exc)}],
                }
            if not isinstance(raw, dict):
                errors.append({"code": "JSONL_RECORD_NOT_OBJECT", "line": line_no, "message": "line must decode to object"})
                dropped += 1
                continue
            observation = _observation_for_tool(tool, raw, line_no=line_no, line_hash=line_hash, run_id=run_id)
            if observation is None:
                dropped += 1
            else:
                observations.append(observation)

    payload = {
        "schema_version": SCHEMA_VERSION,
        "status": "ok" if not errors else "error",
        "tool": tool,
        "input_path": input_path,
        "summary": {"imported_count": len(observations), "dropped_count": dropped, "error_count": len(errors)},
        "observations": observations,
        "errors": errors,
        "safety": {
            "network_io": False,
            "subprocess_execution": False,
            "promotes_findings": False,
            "imports_response_bodies": False,
        },
    }
    _check_no_promotional_status(payload)
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Import offline httpx/katana/nuclei/ffuf outputs into non-promotional observations")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--tool", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--run-id", default="external-tool-import")
    args = parser.parse_args(argv)
    payload = import_observations(Path(args.repo_root), args.tool, args.input, run_id=args.run_id)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload.get("status") == "ok" else 2


if __name__ == "__main__":
    raise SystemExit(main())
