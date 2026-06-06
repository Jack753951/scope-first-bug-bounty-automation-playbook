#!/usr/bin/env python3
"""Validate an already-persisted dry-run preview bundle manifest.

This helper is standard-library only and read-only. It reads
preview_manifest.json plus the four fixed preview artifacts, validates their
closed data contract, recomputes size/SHA-256, and exits nonzero on denial.
It never creates, writes, repairs, renames, deletes, executes modules, opens
network clients, or touches targets.
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


SCHEMA_VERSION = "preview_manifest/1.0"
VALIDATION_SCHEMA_VERSION = "preview_manifest_validation/1.0"
PRODUCER_NAME = "module_runner"
ALLOWED_ARTIFACTS = {
    "run.json",
    "module_inputs.json",
    "module_results.json",
    "bundle_consistency.json",
}
RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{2,127}$")
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][A-Za-z0-9._-]+)?$")


@dataclass
class ManifestError:
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
class PreviewManifestValidation:
    verdict: str = "deny"
    errors: list[ManifestError] = field(default_factory=list)
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
        self.errors.append(ManifestError(code, path, message, expected, observed))

    def allow_if_clean(self) -> "PreviewManifestValidation":
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
            raise ValueError(f"duplicate key: {key}")
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


def _is_safe_run_id(value: Any) -> bool:
    return isinstance(value, str) and RUN_ID_RE.fullmatch(value) is not None and ".." not in value


def _is_abs_or_drive_path(value: str) -> bool:
    return value.startswith("/") or PureWindowsPath(value).drive != ""


def _safe_relative_path(value: Any, run_id: str, artifact_name: str) -> bool:
    if not isinstance(value, str):
        return False
    if "\\" in value or _is_abs_or_drive_path(value):
        return False
    if "//" in value or "/./" in value or value.endswith("/.") or value.startswith("./"):
        return False
    pure = PurePosixPath(value)
    if any(part in ("", ".", "..") for part in pure.parts):
        return False
    expected = PurePosixPath("runs") / run_id / "preview" / artifact_name
    return pure == expected


def _chain_has_symlink(path: Path) -> bool:
    absolute = path.absolute()
    for candidate in (absolute, *absolute.parents):
        try:
            if candidate.exists() and candidate.is_symlink():
                return True
        except OSError:
            return True
    return False


def _read_artifact_bytes(path: Path, validation: PreviewManifestValidation, field_path: str) -> bytes | None:
    if _chain_has_symlink(path):
        validation.add("PREVIEW_MANIFEST_SYMLINK_DENIED", field_path, "symlinks are not allowed in artifact paths")
        return None
    try:
        if not path.exists():
            validation.add("PREVIEW_MANIFEST_ARTIFACT_MISSING", field_path, "artifact file is missing")
            return None
        if not path.is_file():
            validation.add("PREVIEW_MANIFEST_ARTIFACT_NOT_FILE", field_path, "artifact path must be a regular file")
            return None
        return path.read_bytes()
    except OSError:
        validation.add("PREVIEW_MANIFEST_READ_ERROR", field_path, "artifact could not be read")
        return None


def _require_object(
    value: Any,
    required: set[str],
    allowed: set[str],
    path: str,
    validation: PreviewManifestValidation,
) -> bool:
    if not isinstance(value, dict):
        validation.add("PREVIEW_MANIFEST_TYPE_INVALID", path, "field must be an object", expected="object", observed=_type_name(value))
        return False
    for key in sorted(required - set(value)):
        validation.add("PREVIEW_MANIFEST_REQUIRED_MISSING", f"{path}.{key}", "required field is missing")
    for key in sorted(set(value) - allowed):
        validation.add("PREVIEW_MANIFEST_UNKNOWN_FIELD", f"{path}.{key}", "unknown field is not allowed")
    return not (required - set(value) or set(value) - allowed)


def _validate_manifest_shape(manifest: Any, validation: PreviewManifestValidation) -> None:
    top_keys = {
        "schema_version",
        "run_id",
        "created_at_utc",
        "producer",
        "preview_mode",
        "bundle_consistency",
        "artifacts",
    }
    if not _require_object(manifest, top_keys, top_keys, "manifest", validation):
        if not isinstance(manifest, dict):
            return

    if manifest.get("schema_version") != SCHEMA_VERSION:
        validation.add("PREVIEW_MANIFEST_SCHEMA_VERSION_INVALID", "schema_version", "schema_version must be preview_manifest/1.0", expected=SCHEMA_VERSION, observed=_type_name(manifest.get("schema_version")))
    if not _is_safe_run_id(manifest.get("run_id")):
        validation.add("PREVIEW_MANIFEST_RUN_ID_INVALID", "run_id", "run_id must be a single safe path segment")
    if _parse_utc(manifest.get("created_at_utc")) is None:
        validation.add("PREVIEW_MANIFEST_TIMESTAMP_INVALID", "created_at_utc", "created_at_utc must be a Z-suffixed UTC timestamp")

    producer = manifest.get("producer")
    if _require_object(producer, {"name", "version"}, {"name", "version"}, "producer", validation):
        if producer.get("name") != PRODUCER_NAME:
            validation.add("PREVIEW_MANIFEST_PRODUCER_INVALID", "producer.name", "producer.name must identify module_runner", expected=PRODUCER_NAME, observed=_type_name(producer.get("name")))
        if not isinstance(producer.get("version"), str) or not SEMVER_RE.fullmatch(producer["version"]):
            validation.add("PREVIEW_MANIFEST_PRODUCER_VERSION_INVALID", "producer.version", "producer.version must be semver")

    preview_mode = manifest.get("preview_mode")
    preview_keys = {"persist_preview_bundle", "include_module_io_preview", "dry_run"}
    if _require_object(preview_mode, preview_keys, preview_keys, "preview_mode", validation):
        for key in sorted(preview_keys):
            if preview_mode.get(key) is not True:
                validation.add("PREVIEW_MANIFEST_PREVIEW_MODE_INVALID", f"preview_mode.{key}", "preview mode flag must be true", expected=True, observed=_type_name(preview_mode.get(key)))

    consistency = manifest.get("bundle_consistency")
    consistency_keys = {"status", "verdict", "relative_path", "sha256"}
    if _require_object(consistency, consistency_keys, consistency_keys, "bundle_consistency", validation):
        if consistency.get("status") != "ok":
            validation.add("PREVIEW_MANIFEST_BUNDLE_STATUS_INVALID", "bundle_consistency.status", "bundle consistency status must be ok", expected="ok", observed=_type_name(consistency.get("status")))
        if consistency.get("verdict") != "allow":
            validation.add("PREVIEW_MANIFEST_BUNDLE_VERDICT_INVALID", "bundle_consistency.verdict", "bundle consistency verdict must be allow", expected="allow", observed=_type_name(consistency.get("verdict")))
        if not isinstance(consistency.get("sha256"), str) or not HASH_RE.fullmatch(consistency["sha256"]):
            validation.add("PREVIEW_MANIFEST_HASH_INVALID", "bundle_consistency.sha256", "sha256 must be lowercase hex")

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        validation.add("PREVIEW_MANIFEST_TYPE_INVALID", "artifacts", "artifacts must be an array", expected="array", observed=_type_name(artifacts))
        return
    seen: set[str] = set()
    for index, artifact in enumerate(artifacts):
        artifact_path = f"artifacts[{index}]"
        keys = {"name", "relative_path", "sha256", "size_bytes", "content_type"}
        if not _require_object(artifact, keys, keys, artifact_path, validation):
            continue
        name = artifact.get("name")
        if name == "preview_manifest.json":
            validation.add("PREVIEW_MANIFEST_SELF_LISTED", f"{artifact_path}.name", "preview_manifest.json must not be listed as an artifact")
        elif name not in ALLOWED_ARTIFACTS:
            validation.add("PREVIEW_MANIFEST_ARTIFACT_NAME_INVALID", f"{artifact_path}.name", "artifact name is not in the fixed allowlist", expected=sorted(ALLOWED_ARTIFACTS), observed=_type_name(name))
        elif name in seen:
            validation.add("PREVIEW_MANIFEST_ARTIFACT_DUPLICATE", f"{artifact_path}.name", "artifact name is duplicated")
        else:
            seen.add(name)
        if not isinstance(artifact.get("sha256"), str) or not HASH_RE.fullmatch(artifact["sha256"]):
            validation.add("PREVIEW_MANIFEST_HASH_INVALID", f"{artifact_path}.sha256", "sha256 must be lowercase hex")
        if not isinstance(artifact.get("size_bytes"), int) or isinstance(artifact.get("size_bytes"), bool) or artifact["size_bytes"] < 0:
            validation.add("PREVIEW_MANIFEST_SIZE_INVALID", f"{artifact_path}.size_bytes", "size_bytes must be a non-negative integer")
        if artifact.get("content_type") != "application/json":
            validation.add("PREVIEW_MANIFEST_CONTENT_TYPE_INVALID", f"{artifact_path}.content_type", "content_type must be application/json", expected="application/json", observed=_type_name(artifact.get("content_type")))

    missing = ALLOWED_ARTIFACTS - seen
    extra = seen - ALLOWED_ARTIFACTS
    for name in sorted(missing):
        validation.add("PREVIEW_MANIFEST_ARTIFACT_MISSING", f"artifacts.{name}", "required artifact is missing")
    for name in sorted(extra):
        validation.add("PREVIEW_MANIFEST_ARTIFACT_EXTRA", f"artifacts.{name}", "unexpected artifact is listed")


def _validate_artifacts(
    bundle_dir: Path,
    manifest: dict[str, Any],
    validation: PreviewManifestValidation,
) -> dict[str, Any]:
    parsed_artifacts: dict[str, Any] = {}
    run_id = manifest.get("run_id")
    if not _is_safe_run_id(run_id):
        return parsed_artifacts

    consistency_block = manifest.get("bundle_consistency") if isinstance(manifest.get("bundle_consistency"), dict) else {}
    if consistency_block:
        expected_path = f"runs/{run_id}/preview/bundle_consistency.json"
        if consistency_block.get("relative_path") != expected_path:
            validation.add("PREVIEW_MANIFEST_PATH_INVALID", "bundle_consistency.relative_path", "bundle consistency path must match the run preview artifact path", expected=expected_path, observed=_type_name(consistency_block.get("relative_path")))

    artifact_entries = manifest.get("artifacts") if isinstance(manifest.get("artifacts"), list) else []
    for index, artifact in enumerate(artifact_entries):
        if not isinstance(artifact, dict):
            continue
        name = artifact.get("name")
        field_path = f"artifacts[{index}]"
        if not isinstance(name, str) or name not in ALLOWED_ARTIFACTS:
            continue
        relative_path = artifact.get("relative_path")
        if not _safe_relative_path(relative_path, run_id, name):
            validation.add("PREVIEW_MANIFEST_PATH_INVALID", f"{field_path}.relative_path", "relative_path must be a safe runs/<run_id>/preview artifact path")
            continue
        artifact_path = bundle_dir / name
        data = _read_artifact_bytes(artifact_path, validation, field_path)
        if data is None:
            continue
        digest = sha256(data).hexdigest()
        if digest != artifact.get("sha256"):
            validation.add("PREVIEW_MANIFEST_HASH_MISMATCH", f"{field_path}.sha256", "artifact sha256 does not match file contents")
        if len(data) != artifact.get("size_bytes"):
            validation.add("PREVIEW_MANIFEST_SIZE_MISMATCH", f"{field_path}.size_bytes", "artifact size_bytes does not match file contents")
        if name == "bundle_consistency.json" and consistency_block:
            if digest != consistency_block.get("sha256"):
                validation.add("PREVIEW_MANIFEST_BUNDLE_HASH_MISMATCH", "bundle_consistency.sha256", "bundle_consistency sha256 must match artifact contents")
        try:
            parsed_artifacts[name] = json.loads(data.decode("utf-8"), object_pairs_hook=_reject_duplicate_keys)
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
            validation.add("PREVIEW_MANIFEST_ARTIFACT_JSON_INVALID", field_path, "artifact must be valid UTF-8 JSON without duplicate keys")
    return parsed_artifacts


def _validate_semantics(
    manifest: dict[str, Any],
    artifacts: dict[str, Any],
    validation: PreviewManifestValidation,
) -> None:
    run_id = manifest.get("run_id")
    run_doc = artifacts.get("run.json")
    if isinstance(run_doc, dict) and run_doc.get("run_id") != run_id:
        validation.add("PREVIEW_MANIFEST_RUN_ID_MISMATCH", "run.run_id", "run artifact run_id must match preview manifest")

    manifest_created = _parse_utc(manifest.get("created_at_utc"))
    if manifest_created is not None:
        if manifest_created > datetime.now(timezone.utc):
            validation.add("PREVIEW_MANIFEST_TIMESTAMP_FUTURE", "created_at_utc", "created_at_utc must not be in the future")
        if isinstance(run_doc, dict):
            run_created = _parse_utc(run_doc.get("created_at_utc"))
            if run_created is not None and manifest_created < run_created:
                validation.add("PREVIEW_MANIFEST_TIMESTAMP_ORDER_INVALID", "created_at_utc", "created_at_utc must not be earlier than run.created_at_utc")

    consistency = artifacts.get("bundle_consistency.json")
    if not isinstance(consistency, dict):
        return
    status = consistency.get("status")
    verdict = consistency.get("verdict")
    if status is None and verdict is None:
        validation.add("PREVIEW_MANIFEST_BUNDLE_STATUS_INVALID", "bundle_consistency_artifact", "bundle consistency artifact must contain status ok or verdict allow")
    if status is not None and status != "ok":
        validation.add("PREVIEW_MANIFEST_BUNDLE_STATUS_INVALID", "bundle_consistency_artifact.status", "bundle consistency artifact status must be ok")
    if verdict is not None and verdict != "allow":
        validation.add("PREVIEW_MANIFEST_BUNDLE_VERDICT_INVALID", "bundle_consistency_artifact.verdict", "bundle consistency artifact verdict must be allow")


def validate_preview_bundle(bundle_dir: str | Path) -> PreviewManifestValidation:
    validation = PreviewManifestValidation()
    preview_dir = Path(bundle_dir)
    manifest_path = preview_dir / "preview_manifest.json"

    if _chain_has_symlink(preview_dir):
        validation.add("PREVIEW_MANIFEST_SYMLINK_DENIED", "bundle_dir", "symlinks are not allowed in the bundle path")
        return validation.allow_if_clean()
    if not preview_dir.exists() or not preview_dir.is_dir():
        validation.add("PREVIEW_MANIFEST_BUNDLE_DIR_INVALID", "bundle_dir", "bundle directory must exist and be a directory")
        return validation.allow_if_clean()
    if _chain_has_symlink(manifest_path):
        validation.add("PREVIEW_MANIFEST_SYMLINK_DENIED", "preview_manifest.json", "symlinks are not allowed for preview_manifest.json")
        return validation.allow_if_clean()

    try:
        manifest = load_json_strict(manifest_path)
    except FileNotFoundError:
        validation.add("PREVIEW_MANIFEST_NOT_FOUND", "preview_manifest.json", "preview_manifest.json is missing")
        return validation.allow_if_clean()
    except UnicodeDecodeError:
        validation.add("PREVIEW_MANIFEST_JSON_INVALID", "preview_manifest.json", "preview_manifest.json must be UTF-8 JSON")
        return validation.allow_if_clean()
    except json.JSONDecodeError:
        validation.add("PREVIEW_MANIFEST_JSON_INVALID", "preview_manifest.json", "preview_manifest.json is malformed")
        return validation.allow_if_clean()
    except ValueError as exc:
        code = "PREVIEW_MANIFEST_DUPLICATE_KEY" if "duplicate key" in str(exc) else "PREVIEW_MANIFEST_JSON_INVALID"
        validation.add(code, "preview_manifest.json", "preview_manifest.json is malformed")
        return validation.allow_if_clean()
    except OSError:
        validation.add("PREVIEW_MANIFEST_READ_ERROR", "preview_manifest.json", "preview_manifest.json could not be read")
        return validation.allow_if_clean()

    _validate_manifest_shape(manifest, validation)
    if isinstance(manifest, dict):
        artifacts = _validate_artifacts(preview_dir, manifest, validation)
        _validate_semantics(manifest, artifacts, validation)
    return validation.allow_if_clean()


def main(argv: list[str] | None = None) -> tuple[int, dict[str, Any]]:
    parser = argparse.ArgumentParser(description="Validate an offline persisted preview bundle manifest.")
    parser.add_argument("bundle_dir", help="Path to runs/<run_id>/preview containing preview_manifest.json.")
    parser.add_argument("--json", action="store_true", help="Accepted for compatibility; output is always JSON.")
    args = parser.parse_args(argv)

    validation = validate_preview_bundle(args.bundle_dir)
    payload = validation.as_dict()
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    return (0 if validation.verdict == "allow" else 1), payload


if __name__ == "__main__":
    code, _payload = main()
    raise SystemExit(code)
