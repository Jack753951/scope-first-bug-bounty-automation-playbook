#!/usr/bin/env python3
"""Validate an offline preview manifest ledger.

This helper is standard-library only and read-only. It reads a
preview_ledger/1.0 JSON document and hashes only the referenced
preview_manifest.json files. It never creates, writes, repairs, renames,
deletes, executes modules, opens network clients, invokes scanners, follows
callbacks, or touches targets.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import sys
from typing import Any


SCHEMA_VERSION = "preview_ledger/1.0"
VALIDATION_SCHEMA_VERSION = "preview_ledger_validation/1.0"
PREVIEW_MANIFEST_SCHEMA_VERSION = "preview_manifest/1.0"
PRODUCER_NAME = "preview_ledger"

SAFE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{2,127}$")
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][A-Za-z0-9._-]+)?$")
NOTE_TEXT_RE = re.compile(r"^[A-Za-z0-9 .,;:_()\[\]+='\"!?-]*$")
NOTE_IP_RE = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")
NOTE_HOST_RE = re.compile(r"\b[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+\b")


@dataclass
class LedgerError:
    code: str
    path: str
    message: str
    expected: Any | None = None
    observed: Any | None = None

    def as_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "code": self.code,
            "path": self.path,
            "message": self.message,
        }
        if self.expected is not None:
            payload["expected"] = self.expected
        if self.observed is not None:
            payload["observed"] = self.observed
        return payload


@dataclass
class PreviewLedgerValidation:
    verdict: str = "deny"
    errors: list[LedgerError] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add(
        self,
        code: str,
        path: str,
        message: str,
        *,
        expected: Any | None = None,
        observed: Any | None = None,
    ) -> None:
        self.errors.append(LedgerError(code, path, message, expected, observed))

    def allow_if_clean(self) -> "PreviewLedgerValidation":
        self.verdict = "deny" if self.errors else "allow"
        return self

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": VALIDATION_SCHEMA_VERSION,
            "validated_schema_version": SCHEMA_VERSION,
            "verdict": self.verdict,
            "errors": [error.as_dict() for error in self.errors],
            "error_codes": [error.code for error in self.errors],
            "warnings": self.warnings,
        }


def _type_name(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, list):
        return "array"
    if isinstance(value, str):
        return "string"
    if isinstance(value, int):
        return "integer"
    return type(value).__name__


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    seen: set[str] = set()
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError("duplicate key")
        seen.add(key)
        result[key] = value
    return result


def load_json_strict(path: Path) -> Any:
    data = path.read_bytes()
    text = data.decode("utf-8")
    decoder = json.JSONDecoder(object_pairs_hook=_reject_duplicate_keys)
    value, end = decoder.raw_decode(text)
    if text[end:].strip():
        raise ValueError("trailing data after JSON document")
    return value


def _parse_utc(value: Any) -> datetime | None:
    if not isinstance(value, str) or not UTC_RE.fullmatch(value):
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _is_safe_id(value: Any) -> bool:
    return isinstance(value, str) and SAFE_ID_RE.fullmatch(value) is not None and ".." not in value


def _is_abs_or_drive_path(value: str) -> bool:
    return value.startswith("/") or PureWindowsPath(value).drive != ""


def _safe_preview_manifest_path(value: Any, run_id: str) -> bool:
    if not isinstance(value, str):
        return False
    if "\\" in value or _is_abs_or_drive_path(value):
        return False
    if "//" in value or "/./" in value or value.endswith("/.") or value.startswith("./"):
        return False
    pure = PurePosixPath(value)
    if any(part in ("", ".", "..") for part in pure.parts):
        return False
    expected = PurePosixPath("runs") / run_id / "preview" / "preview_manifest.json"
    return pure == expected


def _chain_has_symlink(path: Path) -> bool | None:
    try:
        absolute = path.absolute()
        candidates = (absolute, *absolute.parents)
    except OSError:
        return None
    for candidate in candidates:
        try:
            if candidate.exists() and candidate.is_symlink():
                return True
        except OSError:
            return None
    return False


def _is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base)
        return True
    except ValueError:
        return False


def _require_object(
    value: Any,
    required: set[str],
    allowed: set[str],
    path: str,
    validation: PreviewLedgerValidation,
) -> bool:
    if not isinstance(value, dict):
        validation.add("PREVIEW_LEDGER_TYPE_INVALID", path, "field must be an object", expected="object", observed=_type_name(value))
        return False
    for key in sorted(required - set(value)):
        validation.add("PREVIEW_LEDGER_REQUIRED_MISSING", f"{path}.{key}", "required field is missing")
    for key in sorted(set(value) - allowed):
        validation.add("PREVIEW_LEDGER_UNKNOWN_FIELD", f"{path}.{key}", "unknown field is not allowed")
    return not (required - set(value) or set(value) - allowed)


def _validate_notes(value: Any, path: str, validation: PreviewLedgerValidation) -> None:
    if not isinstance(value, str):
        validation.add("PREVIEW_LEDGER_NOTES_INVALID", path, "notes must be a redaction-safe string", observed=_type_name(value))
        return
    if len(value) > 256:
        validation.add("PREVIEW_LEDGER_NOTES_INVALID", path, "notes must be no more than 256 characters")
        return
    if (
        "/" in value
        or "\\" in value
        or "@" in value
        or "http://" in value.lower()
        or "https://" in value.lower()
        or NOTE_IP_RE.search(value)
        or NOTE_HOST_RE.search(value)
        or NOTE_TEXT_RE.fullmatch(value) is None
    ):
        validation.add("PREVIEW_LEDGER_NOTES_INVALID", path, "notes must avoid paths, URLs, host indicators, and contact-like tokens")


def _validate_ledger_shape(ledger: Any, validation: PreviewLedgerValidation) -> tuple[datetime | None, list[dict[str, Any]]]:
    top_keys = {"schema_version", "ledger_id", "created_at_utc", "producer", "entry_count", "entries"}
    if not _require_object(ledger, top_keys, top_keys, "ledger", validation):
        if not isinstance(ledger, dict):
            return None, []

    if ledger.get("schema_version") != SCHEMA_VERSION:
        validation.add("PREVIEW_LEDGER_SCHEMA_VERSION_INVALID", "schema_version", "schema_version must be preview_ledger/1.0", expected=SCHEMA_VERSION, observed=_type_name(ledger.get("schema_version")))
    if not _is_safe_id(ledger.get("ledger_id")):
        validation.add("PREVIEW_LEDGER_ID_INVALID", "ledger_id", "ledger_id must be a single safe identifier segment")

    created_at = _parse_utc(ledger.get("created_at_utc"))
    if created_at is None:
        validation.add("PREVIEW_LEDGER_TIMESTAMP_INVALID", "created_at_utc", "created_at_utc must be a Z-suffixed UTC timestamp")
    elif created_at > datetime.now(timezone.utc):
        validation.add("PREVIEW_LEDGER_TIMESTAMP_FUTURE", "created_at_utc", "created_at_utc must not be in the future")

    producer = ledger.get("producer")
    if _require_object(producer, {"name", "version"}, {"name", "version"}, "producer", validation):
        if producer.get("name") != PRODUCER_NAME:
            validation.add("PREVIEW_LEDGER_PRODUCER_INVALID", "producer.name", "producer.name must identify preview_ledger", expected=PRODUCER_NAME, observed=_type_name(producer.get("name")))
        if not isinstance(producer.get("version"), str) or not SEMVER_RE.fullmatch(producer["version"]):
            validation.add("PREVIEW_LEDGER_PRODUCER_VERSION_INVALID", "producer.version", "producer.version must be semver")

    entry_count = ledger.get("entry_count")
    if not isinstance(entry_count, int) or isinstance(entry_count, bool) or entry_count < 0:
        validation.add("PREVIEW_LEDGER_ENTRY_COUNT_INVALID", "entry_count", "entry_count must be a non-negative integer", expected="non-negative integer", observed=_type_name(entry_count))

    entries = ledger.get("entries")
    if not isinstance(entries, list):
        validation.add("PREVIEW_LEDGER_TYPE_INVALID", "entries", "entries must be an array", expected="array", observed=_type_name(entries))
        return created_at, []
    if isinstance(entry_count, int) and not isinstance(entry_count, bool) and entry_count != len(entries):
        validation.add("PREVIEW_LEDGER_ENTRY_COUNT_MISMATCH", "entry_count", "entry_count must equal the number of entries", expected="len(entries)", observed="integer")

    parsed_entries: list[dict[str, Any]] = []
    seen_runs: dict[str, int] = {}
    entry_keys = {
        "run_id",
        "preview_manifest_relative_path",
        "preview_manifest_sha256",
        "preview_manifest_size_bytes",
        "schema_version_observed",
        "observed_at_utc",
        "notes",
    }
    required_entry_keys = entry_keys - {"notes"}
    now = datetime.now(timezone.utc)

    for index, entry in enumerate(entries):
        entry_path = f"entries[{index}]"
        if not _require_object(entry, required_entry_keys, entry_keys, entry_path, validation):
            if not isinstance(entry, dict):
                continue

        run_id = entry.get("run_id")
        if not _is_safe_id(run_id):
            validation.add("PREVIEW_LEDGER_RUN_ID_INVALID", f"{entry_path}.run_id", "run_id must be a single safe identifier segment")
        elif run_id in seen_runs:
            validation.add(
                "PREVIEW_LEDGER_DUPLICATE_RUN_ID",
                f"{entry_path}.run_id",
                "run_id must be unique across entries",
                expected=f"unique run_id; first seen at entries[{seen_runs[run_id]}]",
                observed=f"duplicate at entries[{index}]",
            )
        else:
            seen_runs[run_id] = index

        if entry.get("schema_version_observed") != PREVIEW_MANIFEST_SCHEMA_VERSION:
            validation.add(
                "PREVIEW_LEDGER_OBSERVED_SCHEMA_VERSION_INVALID",
                f"{entry_path}.schema_version_observed",
                "schema_version_observed must be preview_manifest/1.0",
                expected=PREVIEW_MANIFEST_SCHEMA_VERSION,
                observed=_type_name(entry.get("schema_version_observed")),
            )
        if not isinstance(entry.get("preview_manifest_sha256"), str) or not HASH_RE.fullmatch(entry["preview_manifest_sha256"]):
            validation.add("PREVIEW_LEDGER_HASH_INVALID", f"{entry_path}.preview_manifest_sha256", "preview_manifest_sha256 must be lowercase hex")
        size_bytes = entry.get("preview_manifest_size_bytes")
        if not isinstance(size_bytes, int) or isinstance(size_bytes, bool) or size_bytes < 0:
            validation.add("PREVIEW_LEDGER_SIZE_INVALID", f"{entry_path}.preview_manifest_size_bytes", "preview_manifest_size_bytes must be a non-negative integer", expected="non-negative integer", observed=_type_name(size_bytes))
        if isinstance(run_id, str) and not _safe_preview_manifest_path(entry.get("preview_manifest_relative_path"), run_id):
            validation.add("PREVIEW_LEDGER_PATH_INVALID", f"{entry_path}.preview_manifest_relative_path", "path must equal runs/<run_id>/preview/preview_manifest.json and stay relative")

        observed_at = _parse_utc(entry.get("observed_at_utc"))
        if observed_at is None:
            validation.add("PREVIEW_LEDGER_TIMESTAMP_INVALID", f"{entry_path}.observed_at_utc", "observed_at_utc must be a Z-suffixed UTC timestamp")
        else:
            if observed_at > now:
                validation.add("PREVIEW_LEDGER_TIMESTAMP_FUTURE", f"{entry_path}.observed_at_utc", "observed_at_utc must not be in the future")
            if created_at is not None and observed_at > created_at:
                validation.add("PREVIEW_LEDGER_TIMESTAMP_ORDER_INVALID", f"{entry_path}.observed_at_utc", "observed_at_utc must not be later than ledger.created_at_utc")

        if "notes" in entry:
            _validate_notes(entry.get("notes"), f"{entry_path}.notes", validation)

        if isinstance(entry, dict):
            parsed_entries.append(entry)

    return created_at, parsed_entries


def _read_bound_manifest(
    repo_root: Path,
    entry: dict[str, Any],
    index: int,
    validation: PreviewLedgerValidation,
) -> None:
    run_id = entry.get("run_id")
    relative_path = entry.get("preview_manifest_relative_path")
    if not isinstance(run_id, str) or not _safe_preview_manifest_path(relative_path, run_id):
        return

    manifest_path = repo_root / relative_path
    symlink_state = _chain_has_symlink(manifest_path)
    if symlink_state is None or symlink_state:
        validation.add("PREVIEW_LEDGER_SYMLINK_DENIED", f"entries[{index}].preview_manifest_relative_path", "symlinks are not allowed in preview manifest paths")
        return

    try:
        runs_root = (repo_root / "runs").resolve(strict=False)
        resolved_manifest = manifest_path.resolve(strict=False)
    except OSError:
        validation.add("PREVIEW_LEDGER_PATH_RESOLUTION_FAILED", f"entries[{index}].preview_manifest_relative_path", "preview manifest path could not be resolved")
        return
    if not _is_relative_to(resolved_manifest, runs_root):
        validation.add("PREVIEW_LEDGER_PATH_ESCAPE", f"entries[{index}].preview_manifest_relative_path", "preview manifest path must resolve under repo_root/runs")
        return

    try:
        if not manifest_path.exists():
            validation.add("PREVIEW_LEDGER_PREVIEW_MANIFEST_MISSING", f"entries[{index}].preview_manifest_relative_path", "referenced preview_manifest.json is missing")
            return
        if not manifest_path.is_file():
            validation.add("PREVIEW_LEDGER_PREVIEW_MANIFEST_NOT_FILE", f"entries[{index}].preview_manifest_relative_path", "referenced preview_manifest.json must be a regular file")
            return
        data = manifest_path.read_bytes()
    except OSError:
        validation.add("PREVIEW_LEDGER_READ_ERROR", f"entries[{index}].preview_manifest_relative_path", "referenced preview_manifest.json could not be read")
        return

    if sha256(data).hexdigest() != entry.get("preview_manifest_sha256"):
        validation.add("PREVIEW_LEDGER_HASH_MISMATCH", f"entries[{index}].preview_manifest_sha256", "preview_manifest_sha256 does not match file contents")
    if len(data) != entry.get("preview_manifest_size_bytes"):
        validation.add("PREVIEW_LEDGER_SIZE_MISMATCH", f"entries[{index}].preview_manifest_size_bytes", "preview_manifest_size_bytes does not match file contents")


def validate_preview_ledger(ledger_file: str | Path, repo_root: str | Path) -> PreviewLedgerValidation:
    validation = PreviewLedgerValidation()
    ledger_path = Path(ledger_file)

    ledger_symlink_state = _chain_has_symlink(ledger_path)
    if ledger_symlink_state is None or ledger_symlink_state:
        validation.add("PREVIEW_LEDGER_SYMLINK_DENIED", "ledger_file", "symlinks are not allowed in the ledger path")
        return validation.allow_if_clean()

    try:
        repo_root_path = Path(repo_root).resolve(strict=False)
    except OSError:
        validation.add("PREVIEW_LEDGER_REPO_ROOT_INVALID", "repo_root", "repo root could not be resolved")
        return validation.allow_if_clean()

    try:
        ledger = load_json_strict(ledger_path)
    except FileNotFoundError:
        validation.add("PREVIEW_LEDGER_NOT_FOUND", "ledger_file", "preview ledger is missing")
        return validation.allow_if_clean()
    except UnicodeDecodeError:
        validation.add("PREVIEW_LEDGER_JSON_INVALID", "ledger_file", "preview ledger must be UTF-8 JSON")
        return validation.allow_if_clean()
    except json.JSONDecodeError:
        validation.add("PREVIEW_LEDGER_JSON_INVALID", "ledger_file", "preview ledger is malformed")
        return validation.allow_if_clean()
    except ValueError as exc:
        code = "PREVIEW_LEDGER_DUPLICATE_KEY" if "duplicate key" in str(exc) else "PREVIEW_LEDGER_JSON_INVALID"
        validation.add(code, "ledger_file", "preview ledger is malformed")
        return validation.allow_if_clean()
    except OSError:
        validation.add("PREVIEW_LEDGER_READ_ERROR", "ledger_file", "preview ledger could not be read")
        return validation.allow_if_clean()

    _created_at, entries = _validate_ledger_shape(ledger, validation)
    for index, entry in enumerate(entries):
        _read_bound_manifest(repo_root_path, entry, index, validation)
    return validation.allow_if_clean()


def main(argv: list[str] | None = None) -> tuple[int, dict[str, Any]]:
    parser = argparse.ArgumentParser(description="Validate an offline preview_manifest/1.0 ledger.")
    parser.add_argument("ledger_file", help="Path to a preview_ledger/1.0 JSON document.")
    parser.add_argument("--repo-root", required=True, help="Repository root used to resolve runs/<run_id>/preview/preview_manifest.json entries.")
    parser.add_argument("--json", action="store_true", help="Accepted for compatibility; output is always JSON.")
    args = parser.parse_args(argv)

    validation = validate_preview_ledger(args.ledger_file, args.repo_root)
    payload = validation.as_dict()
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    return (0 if validation.verdict == "allow" else 1), payload


if __name__ == "__main__":
    code, _payload = main()
    raise SystemExit(code)
