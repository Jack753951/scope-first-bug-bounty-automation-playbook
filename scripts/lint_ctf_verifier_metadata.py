#!/usr/bin/env python3
"""Offline linter for trial CTF verifier metadata descriptors.

TRIAL ONLY -- do not promote without P2.19+ review.

This linter is intentionally weaker than a JSON Schema. It exists to let two
real verifier descriptors codify a flat vocabulary before any schema
promotion. It is non-binding, has no runtime consumers, and is not invoked
by any runner, hook, recon path, scanner, or CI in this slice. Promotion to
a versioned ``modules/_schema/ctf_verifier_metadata.schema.json`` is
explicitly deferred to P2.19+ after this trial reports gaps.

Properties:

* Standard-library only. No PyYAML. The parser is a minimal flat-key
  reader that explicitly rejects YAML anchors, aliases, merge keys,
  ``!!``-tags, flow-style mappings/sequences, and indented sub-mappings.
* No network, no sockets, no subprocess, no scanner/module imports. No
  filesystem writes. Reads input paths only.
* Deterministic JSON output: keys sorted, error lists sorted, exit code 0
  only when every input file passes.
* The forbidden-field vocabulary mirrors the
  ``OVERRIDE_FIELD_NAMES`` set in ``scripts/ctf_review_decision.py``
  (lines 90-102) plus the broader P2.18 direction-review list. The
  trial test suite asserts parity (or a documented superset).
* Unknown top-level fields are denied. The trial is meaningful only if
  drift is denied; future-compatibility belongs to the schema promotion
  step in P2.19+ where versioning provides the proper escape valve.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SCRIPT_KIND = "ctf_verifier_metadata_lint/0.1-trial"

# Error codes (stable strings for downstream tests).
CODE_DESTRUCTIVE = "DESTRUCTIVE_NOT_ALLOWED"
CODE_ACTIVE_REQUIRES_KALI = "ACTIVE_SERVICE_REQUIRES_KALI"
CODE_ACTIVE_REQUIRES_SCOPE = "ACTIVE_SERVICE_REQUIRES_SCOPE"
CODE_HOST_EXECUTION = "HOST_EXECUTION_NOT_ALLOWED"
CODE_UNKNOWN_TRIGGER = "UNKNOWN_TRIGGER"
CODE_UNKNOWN_FIELD = "UNKNOWN_FIELD"
CODE_FORBIDDEN_FIELD = "FORBIDDEN_FIELD"
CODE_BOOL_TYPE_MISMATCH = "BOOL_TYPE_MISMATCH"
CODE_UNKNOWN_MODE = "UNKNOWN_MODE"
CODE_UNKNOWN_CATEGORY = "UNKNOWN_CATEGORY"
CODE_MISSING_REQUIRED = "MISSING_REQUIRED_FIELD"
CODE_YAML_PARSE = "YAML_PARSE_ERROR"
CODE_YAML_UNSAFE = "YAML_UNSAFE_SYNTAX"
CODE_FILE_READ = "FILE_READ_ERROR"
CODE_INVALID_VALUE_TYPE = "INVALID_VALUE_TYPE"
CODE_DUPLICATE_KEY = "DUPLICATE_KEY"

# Allowed top-level fields. Anything else is denied.
ALLOWED_FIELDS = (
    "id",
    "category",
    "mode",
    "requires_scope",
    "destructive",
    "uses_external_service",
    "oracle_required",
    "kali_required",
    "confidence",
    "second_review_triggers",
    "evidence_outputs",
)

REQUIRED_FIELDS = (
    "id",
    "category",
    "mode",
    "requires_scope",
    "destructive",
    "uses_external_service",
    "oracle_required",
    "second_review_triggers",
    "evidence_outputs",
)

BOOL_FIELDS = (
    "requires_scope",
    "destructive",
    "uses_external_service",
    "oracle_required",
    "kali_required",
)

# Allowed values (kept in sync with ctf_review_decision / ctf_prepare_challenge).
ALLOWED_MODES = (
    "active-service",
    "offline",
    "oracle",
    "reconstruction",
)

# Mirror of ctf_prepare_challenge.ALLOWED_CATEGORIES.
ALLOWED_CATEGORIES = (
    "crypto",
    "forensics",
    "misc",
    "pwn",
    "reverse",
    "unknown",
    "web",
)

# Mirror of ctf_review_decision.ALLOWED_TRIGGERS.
ALLOWED_TRIGGERS = (
    "abnormal_format",
    "external_source_only",
    "multiple_candidates",
    "solver_timeout",
    "ui_or_checker_only",
)

ALLOWED_CONFIDENCES = ("low", "medium", "high", "candidate")

# Host-execution affordances. These are a strict subset of FORBIDDEN_FIELDS.
# When the descriptor is active-service-like, presence of any of these
# escalates from FORBIDDEN_FIELD to HOST_EXECUTION_NOT_ALLOWED.
HOST_EXECUTION_FIELDS = frozenset(
    {
        "args",
        "argv",
        "binary_path",
        "callback_url",
        "cmd",
        "command",
        "entrypoint",
        "exec",
        "interactsh",
        "oast_callback",
        "oast_domain",
        "run",
        "script",
        "shell",
        "sink_url",
        "webhook_url",
    }
)

# Forbidden fields from the P2.18 direction review (Question 5). The set is
# a documented superset of ctf_review_decision.OVERRIDE_FIELD_NAMES; the
# trial test suite asserts the superset relationship.
FORBIDDEN_FIELDS = frozenset(
    {
        # Network / target overrides
        "allow_cidr",
        "base_url",
        "endpoint",
        "host",
        "live_target",
        "port",
        "scope_override",
        "target_host",
        "target_ip",
        "target_url",
        # Execution affordances
        "args",
        "argv",
        "binary_path",
        "cmd",
        "command",
        "entrypoint",
        "exec",
        "run",
        "script",
        "shell",
        # Callback / out-of-band
        "callback_url",
        "interactsh",
        "oast_callback",
        "oast_domain",
        "sink_url",
        "webhook_url",
        # Exploit / payload
        "cve_exploit",
        "exploit_payload",
        "payload",
        "rop_chain",
        "shellcode",
        # Promotion / finding-state leaks
        "asserted_status",
        "cvss",
        "cvss_vector",
        "cwe",
        "evidence_promotion",
        "finding_state",
        "force_verified",
        "override_status",
        "report_promotion",
        "severity",
        "verification_state",
        # Credential / loot leaks
        "api_key",
        "credentials",
        "loot_path",
        "private_key",
        "secret",
        "token",
        "wordlist_path",
        # Scope / config bypasses
        "bypass_policy",
        "disable_scope",
        "skip_authorization",
    }
)


class YamlParseError(Exception):
    """Raised by the flat-key parser when input is malformed or unsafe."""

    def __init__(self, code: str, message: str, line: int | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.line = line


_KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_ANCHOR_OR_ALIAS_RE = re.compile(r"(?:^|\s)[&*][A-Za-z0-9_]")


def _strip_inline_comment(text: str) -> str:
    """Strip an unquoted ``# comment`` suffix from a scalar value."""

    in_single = False
    in_double = False
    for idx, ch in enumerate(text):
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == "#" and not in_single and not in_double:
            return text[:idx].rstrip()
    return text.rstrip()


def parse_flat_yaml(text: str) -> dict[str, Any]:
    """Parse a strict flat-key subset of YAML.

    Returns a dict where each key maps to either:

    * a scalar dict ``{"kind": "scalar", "raw": <str>}`` where ``raw`` is
      the unstripped token (quotes preserved), or
    * a list dict ``{"kind": "list", "items": [<str>, ...]}`` where each
      item is the raw token of a ``- value`` line.

    Rejects YAML anchors, aliases, merge keys, ``!!``-tags, flow style,
    indented sub-mappings, and duplicate keys.
    """

    result: dict[str, Any] = {}
    current_list_key: str | None = None
    in_list = False

    lines = text.splitlines()
    for line_no, raw_line in enumerate(lines, start=1):
        line = raw_line.rstrip("\r")
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            continue

        # Document markers are out of scope for the flat trial parser.
        if stripped in ("---", "..."):
            raise YamlParseError(
                CODE_YAML_UNSAFE,
                f"line {line_no}: document markers not supported in trial parser",
                line_no,
            )

        # Unsafe tags.
        if "!!" in line or stripped.startswith("!"):
            raise YamlParseError(
                CODE_YAML_UNSAFE,
                f"line {line_no}: YAML tag syntax (!!, !) not supported",
                line_no,
            )

        # Anchors / aliases.
        if _ANCHOR_OR_ALIAS_RE.search(line) or stripped.startswith("&") or stripped.startswith("*"):
            raise YamlParseError(
                CODE_YAML_UNSAFE,
                f"line {line_no}: YAML anchors/aliases not supported",
                line_no,
            )

        # Merge keys.
        if stripped.startswith("<<"):
            raise YamlParseError(
                CODE_YAML_UNSAFE,
                f"line {line_no}: YAML merge keys not supported",
                line_no,
            )

        # Flow-style mappings/sequences.
        if stripped.startswith("{") or stripped.startswith("["):
            raise YamlParseError(
                CODE_YAML_UNSAFE,
                f"line {line_no}: flow-style YAML not supported",
                line_no,
            )

        indent = len(line) - len(line.lstrip(" "))
        if "\t" in line[:indent]:
            raise YamlParseError(
                CODE_YAML_PARSE,
                f"line {line_no}: tab characters in indentation not supported",
                line_no,
            )

        # List item line: must follow a key that opened a list.
        if stripped.startswith("- ") or stripped == "-":
            if not in_list or current_list_key is None:
                raise YamlParseError(
                    CODE_YAML_PARSE,
                    f"line {line_no}: list item outside of any list key",
                    line_no,
                )
            if indent == 0:
                raise YamlParseError(
                    CODE_YAML_PARSE,
                    f"line {line_no}: list items must be indented",
                    line_no,
                )
            item_value = stripped[1:].strip() if stripped != "-" else ""
            item_value = _strip_inline_comment(item_value)
            if item_value == "":
                raise YamlParseError(
                    CODE_YAML_PARSE,
                    f"line {line_no}: empty list item",
                    line_no,
                )
            result[current_list_key]["items"].append(item_value)
            continue

        # Otherwise: must be a top-level key:value or key: (list opener).
        if indent != 0:
            raise YamlParseError(
                CODE_YAML_PARSE,
                f"line {line_no}: nested mapping not supported in flat trial parser",
                line_no,
            )

        if ":" not in stripped:
            raise YamlParseError(
                CODE_YAML_PARSE,
                f"line {line_no}: expected 'key: value' or 'key:'",
                line_no,
            )

        key, _, rest = stripped.partition(":")
        key = key.strip()
        if not _KEY_RE.match(key):
            raise YamlParseError(
                CODE_YAML_PARSE,
                f"line {line_no}: key {key!r} is not a plain identifier",
                line_no,
            )
        if key in result:
            raise YamlParseError(
                CODE_DUPLICATE_KEY,
                f"line {line_no}: duplicate top-level key {key!r}",
                line_no,
            )

        value_token = _strip_inline_comment(rest.strip())
        if value_token == "":
            # Opens a list.
            result[key] = {"kind": "list", "items": []}
            current_list_key = key
            in_list = True
            continue

        result[key] = {"kind": "scalar", "raw": value_token}
        in_list = False
        current_list_key = None

    return result


def _looks_active_service(parsed: dict[str, Any]) -> bool:
    """Return True if any active-service-like flag is set in the raw input.

    We use the raw token so that even mistyped descriptors still trigger
    the kali-required and host-execution checks. A separate
    BOOL_TYPE_MISMATCH may fire on the same field.
    """

    mode_entry = parsed.get("mode")
    if isinstance(mode_entry, dict) and mode_entry.get("kind") == "scalar":
        if mode_entry.get("raw") == "active-service":
            return True
    for name in ("uses_external_service", "oracle_required"):
        entry = parsed.get(name)
        if isinstance(entry, dict) and entry.get("kind") == "scalar":
            if entry.get("raw") == "true":
                return True
    return False


def _add_error(errors: list[dict[str, str]], code: str, field: str | None, message: str) -> None:
    record: dict[str, str] = {"code": code, "message": message}
    if field is not None:
        record["field"] = field
    errors.append(record)


def _validate_known_fields(parsed: dict[str, Any], errors: list[dict[str, str]]) -> None:
    # Boolean type checks.
    for name in BOOL_FIELDS:
        entry = parsed.get(name)
        if entry is None:
            continue
        if entry.get("kind") != "scalar":
            _add_error(
                errors,
                CODE_INVALID_VALUE_TYPE,
                name,
                f"{name!r} must be a scalar boolean (true/false)",
            )
            continue
        raw = entry["raw"]
        if raw not in ("true", "false"):
            _add_error(
                errors,
                CODE_BOOL_TYPE_MISMATCH,
                name,
                f"{name!r} must be the bare token 'true' or 'false' (got {raw!r})",
            )

    mode_entry = parsed.get("mode")
    if mode_entry is not None and mode_entry.get("kind") == "scalar":
        mode_raw = mode_entry["raw"]
        if mode_raw not in ALLOWED_MODES:
            _add_error(
                errors,
                CODE_UNKNOWN_MODE,
                "mode",
                f"mode must be one of {sorted(ALLOWED_MODES)} (got {mode_raw!r})",
            )
    elif mode_entry is not None:
        _add_error(
            errors,
            CODE_INVALID_VALUE_TYPE,
            "mode",
            "mode must be a scalar string",
        )

    cat_entry = parsed.get("category")
    if cat_entry is not None and cat_entry.get("kind") == "scalar":
        cat_raw = cat_entry["raw"]
        if cat_raw not in ALLOWED_CATEGORIES:
            _add_error(
                errors,
                CODE_UNKNOWN_CATEGORY,
                "category",
                f"category must be one of {sorted(ALLOWED_CATEGORIES)} (got {cat_raw!r})",
            )
    elif cat_entry is not None:
        _add_error(
            errors,
            CODE_INVALID_VALUE_TYPE,
            "category",
            "category must be a scalar string",
        )

    id_entry = parsed.get("id")
    if id_entry is not None and id_entry.get("kind") != "scalar":
        _add_error(
            errors,
            CODE_INVALID_VALUE_TYPE,
            "id",
            "id must be a scalar string",
        )

    conf_entry = parsed.get("confidence")
    if conf_entry is not None:
        if conf_entry.get("kind") != "scalar":
            _add_error(
                errors,
                CODE_INVALID_VALUE_TYPE,
                "confidence",
                "confidence must be a scalar string (advisory)",
            )
        elif conf_entry["raw"] not in ALLOWED_CONFIDENCES:
            _add_error(
                errors,
                CODE_UNKNOWN_FIELD,
                "confidence",
                f"confidence must be one of {sorted(ALLOWED_CONFIDENCES)} "
                f"(got {conf_entry['raw']!r})",
            )

    trig_entry = parsed.get("second_review_triggers")
    if trig_entry is not None:
        if trig_entry.get("kind") != "list":
            _add_error(
                errors,
                CODE_INVALID_VALUE_TYPE,
                "second_review_triggers",
                "second_review_triggers must be a YAML list",
            )
        else:
            for item in trig_entry["items"]:
                if item not in ALLOWED_TRIGGERS:
                    _add_error(
                        errors,
                        CODE_UNKNOWN_TRIGGER,
                        "second_review_triggers",
                        f"unknown second_review_triggers value {item!r} "
                        f"(allowed: {sorted(ALLOWED_TRIGGERS)})",
                    )

    ev_entry = parsed.get("evidence_outputs")
    if ev_entry is not None and ev_entry.get("kind") != "list":
        _add_error(
            errors,
            CODE_INVALID_VALUE_TYPE,
            "evidence_outputs",
            "evidence_outputs must be a YAML list",
        )


def _validate_rules(parsed: dict[str, Any], errors: list[dict[str, str]]) -> None:
    dest_entry = parsed.get("destructive")
    if isinstance(dest_entry, dict) and dest_entry.get("kind") == "scalar":
        if dest_entry["raw"] == "true":
            _add_error(
                errors,
                CODE_DESTRUCTIVE,
                "destructive",
                "destructive: true is reserved and must NOT be used in trial descriptors",
            )

    if _looks_active_service(parsed):
        kali = parsed.get("kali_required")
        kali_ok = (
            isinstance(kali, dict)
            and kali.get("kind") == "scalar"
            and kali.get("raw") == "true"
        )
        if not kali_ok:
            _add_error(
                errors,
                CODE_ACTIVE_REQUIRES_KALI,
                "kali_required",
                "mode active-service / uses_external_service: true / oracle_required: true "
                "requires kali_required: true",
            )

        scope = parsed.get("requires_scope")
        scope_ok = (
            isinstance(scope, dict)
            and scope.get("kind") == "scalar"
            and scope.get("raw") == "true"
        )
        if not scope_ok:
            _add_error(
                errors,
                CODE_ACTIVE_REQUIRES_SCOPE,
                "requires_scope",
                "mode active-service / uses_external_service: true / oracle_required: true "
                "requires requires_scope: true",
            )


def _validate_field_membership(
    parsed: dict[str, Any], errors: list[dict[str, str]]
) -> None:
    allowed = frozenset(ALLOWED_FIELDS)
    active_like = _looks_active_service(parsed)

    for key in parsed.keys():
        if key in allowed:
            continue
        if key in FORBIDDEN_FIELDS:
            if active_like and key in HOST_EXECUTION_FIELDS:
                _add_error(
                    errors,
                    CODE_HOST_EXECUTION,
                    key,
                    f"host-execution affordance {key!r} not allowed in active-service "
                    "descriptors (Kali side performs external interaction; the descriptor "
                    "declares intent only)",
                )
            else:
                _add_error(
                    errors,
                    CODE_FORBIDDEN_FIELD,
                    key,
                    f"forbidden field {key!r} (see P2.18 direction review)",
                )
        else:
            _add_error(
                errors,
                CODE_UNKNOWN_FIELD,
                key,
                f"unknown top-level field {key!r}; the trial denies drift",
            )

    for required in REQUIRED_FIELDS:
        if required not in parsed:
            _add_error(
                errors,
                CODE_MISSING_REQUIRED,
                required,
                f"missing required field {required!r}",
            )


def lint_text(text: str) -> dict[str, Any]:
    """Lint a single descriptor's text body. Returns a result dict.

    Result shape (sorted by key throughout):
    ``{"errors": [...], "status": "ok"|"fail", "warnings": [...]}``
    """

    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []

    try:
        parsed = parse_flat_yaml(text)
    except YamlParseError as exc:
        _add_error(errors, exc.code, None, exc.message)
        return _finalize(errors, warnings)

    if not isinstance(parsed, dict):
        _add_error(
            errors,
            CODE_YAML_PARSE,
            None,
            "root must be a flat mapping",
        )
        return _finalize(errors, warnings)

    _validate_field_membership(parsed, errors)
    _validate_known_fields(parsed, errors)
    _validate_rules(parsed, errors)

    return _finalize(errors, warnings)


def _sort_records(records: list[dict[str, str]]) -> list[dict[str, str]]:
    return sorted(records, key=lambda r: (r.get("code", ""), r.get("field", ""), r.get("message", "")))


def _finalize(errors: list[dict[str, str]], warnings: list[dict[str, str]]) -> dict[str, Any]:
    errors = _sort_records(errors)
    warnings = _sort_records(warnings)
    status = "ok" if not errors else "fail"
    return {"errors": errors, "status": status, "warnings": warnings}


def lint_file(path: Path) -> dict[str, Any]:
    """Lint a single file. ``file`` is the rendered path (POSIX-style)."""

    file_label = path.as_posix()
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return {
            "errors": [
                {
                    "code": CODE_FILE_READ,
                    "field": "",
                    "message": f"could not read file: {exc}",
                }
            ],
            "file": file_label,
            "status": "fail",
            "warnings": [],
        }

    result = lint_text(text)
    return {
        "errors": result["errors"],
        "file": file_label,
        "status": result["status"],
        "warnings": result["warnings"],
    }


def lint_paths(paths: list[str]) -> dict[str, Any]:
    """Lint many files. Returns a deterministic report dict."""

    results: list[dict[str, Any]] = []
    for raw in paths:
        results.append(lint_file(Path(raw)))
    results.sort(key=lambda r: r["file"])
    status = "ok" if all(r["status"] == "ok" for r in results) else "fail"
    return {
        "kind": SCRIPT_KIND,
        "results": results,
        "status": status,
    }


def _render(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lint_ctf_verifier_metadata",
        description=(
            "Trial-only linter for CTF verifier metadata descriptors. "
            "Standard-library only. Reads --input paths and emits a "
            "deterministic JSON report to stdout. No filesystem writes, "
            "no network, no subprocess, no module imports, no runtime wiring. "
            "Unknown fields are denied during the trial; promotion to a "
            "versioned schema in P2.19+ may revisit."
        ),
    )
    parser.add_argument(
        "--input",
        action="append",
        required=True,
        help="Path to a descriptor file (repeatable). Required at least once.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    report = lint_paths(args.input)
    rendered = _render(report)
    sys.stdout.write(rendered)

    return 0 if report["status"] == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
