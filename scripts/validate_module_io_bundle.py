#!/usr/bin/env python3
"""Validate P2-11 module I/O preview bundle consistency.

This helper is intentionally standard-library only. It validates an offline bundle
of an already-planned run/1.0 manifest plus parallel module_input/1.0 and
module_result/1.0 preview arrays. It performs cross-document checks only and
must not import module implementations, launch subprocesses, open network
connections, touch targets, or write findings/evidence/reports/loot.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


def _load_script_module(name: str):
    module_path = Path(__file__).resolve().with_name(f"{name}.py")
    spec = importlib.util.spec_from_file_location(name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


validate_module_io_contract = _load_script_module("validate_module_io_contract")
validate_run_manifest = _load_script_module("validate_run_manifest")

BUNDLE_DOCUMENT_INVALID = "BUNDLE_DOCUMENT_INVALID"
BUNDLE_RUN_MODULE_DUPLICATE = "BUNDLE_RUN_MODULE_DUPLICATE"
BUNDLE_DUPLICATE_PREVIEW = "BUNDLE_DUPLICATE_PREVIEW"
BUNDLE_EXTRA_PREVIEW = "BUNDLE_EXTRA_PREVIEW"
BUNDLE_MISSING_INPUT_FOR_RESULT = "BUNDLE_MISSING_INPUT_FOR_RESULT"
BUNDLE_MISSING_RESULT_FOR_INPUT = "BUNDLE_MISSING_RESULT_FOR_INPUT"
BUNDLE_RUN_ID_MISMATCH = "BUNDLE_RUN_ID_MISMATCH"
BUNDLE_MODULE_ID_MISMATCH = "BUNDLE_MODULE_ID_MISMATCH"
BUNDLE_MANIFEST_HASH_MISMATCH = "BUNDLE_MANIFEST_HASH_MISMATCH"
BUNDLE_MODE_MISMATCH = "BUNDLE_MODE_MISMATCH"
BUNDLE_DRY_RUN_MISMATCH = "BUNDLE_DRY_RUN_MISMATCH"
BUNDLE_RUNNER_MISMATCH = "BUNDLE_RUNNER_MISMATCH"
BUNDLE_PROGRAM_MISMATCH = "BUNDLE_PROGRAM_MISMATCH"
BUNDLE_TARGET_MISMATCH = "BUNDLE_TARGET_MISMATCH"
BUNDLE_POLICY_MISMATCH = "BUNDLE_POLICY_MISMATCH"
BUNDLE_PROFILE_MISMATCH = "BUNDLE_PROFILE_MISMATCH"
BUNDLE_STATUS_INVALID = "BUNDLE_STATUS_INVALID"
BUNDLE_TARGET_TOUCHING_MISMATCH = "BUNDLE_TARGET_TOUCHING_MISMATCH"
BUNDLE_FINDINGS_NOT_EMPTY = "BUNDLE_FINDINGS_NOT_EMPTY"
BUNDLE_EVIDENCE_NOT_EMPTY = "BUNDLE_EVIDENCE_NOT_EMPTY"
BUNDLE_OUTPUT_PATH_MISMATCH = "BUNDLE_OUTPUT_PATH_MISMATCH"
BUNDLE_CONSTRAINT_MISMATCH = "BUNDLE_CONSTRAINT_MISMATCH"
BUNDLE_CREATED_AT_UTC_MISMATCH = "BUNDLE_CREATED_AT_UTC_MISMATCH"

RESULT_STATUSES = {"not_executed", "planned", "skipped", "error"}


@dataclass
class BundleErrorDetail:
    code: str
    message: str
    path: str | None = None
    expected: Any = None
    observed: Any = None
    module_id: str | None = None

    def as_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "code": self.code,
            "message": self.message,
            "expected": self.expected,
            "observed": self.observed,
        }
        if self.path is not None:
            payload["path"] = self.path
        if self.module_id is not None:
            payload["module_id"] = self.module_id
        return payload


@dataclass
class BundleConsistencyResult:
    verdict: str = "deny"
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    error_codes: list[str] = field(default_factory=list)
    warning_codes: list[str] = field(default_factory=list)
    error_details: list[BundleErrorDetail] = field(default_factory=list)

    def add_error(
        self,
        code: str,
        message: str,
        *,
        path: str | None = None,
        expected: Any = None,
        observed: Any = None,
        module_id: str | None = None,
    ) -> None:
        self.errors.append(message)
        self.error_codes.append(code)
        self.error_details.append(
            BundleErrorDetail(
                code=code,
                message=message,
                path=path,
                expected=expected,
                observed=observed,
                module_id=module_id,
            )
        )

    def allow_if_clean(self) -> "BundleConsistencyResult":
        self.verdict = "deny" if self.errors else "allow"
        return self

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "module_io_bundle_consistency/1.0",
            "document_type": "module_io_bundle",
            "verdict": self.verdict,
            "errors": self.errors,
            "warnings": self.warnings,
            "error_codes": self.error_codes,
            "warning_codes": self.warning_codes,
            "error_details": [detail.as_dict() for detail in self.error_details],
        }


def _module_id_from_input(preview: Any) -> Any:
    return preview.get("module", {}).get("module_id") if isinstance(preview, dict) else None


def _module_id_from_result(preview: Any) -> Any:
    return preview.get("module_id") if isinstance(preview, dict) else None


def _add_doc_errors(result: BundleConsistencyResult, label: str, validation: Any) -> None:
    if getattr(validation, "verdict", "deny") != "allow":
        for idx, error in enumerate(getattr(validation, "errors", [])):
            result.add_error(BUNDLE_DOCUMENT_INVALID, f"{label}: {error}", path=f"{label}.errors[{idx}]")


def _same(
    actual: Any,
    expected: Any,
    code: str,
    where: str,
    result: BundleConsistencyResult,
    *,
    module_id: str | None = None,
) -> None:
    if actual != expected:
        result.add_error(
            code,
            f"{where} must match run plan",
            path=where,
            expected=expected,
            observed=actual,
            module_id=module_id,
        )


def _index_previews(
    previews: Any,
    *,
    label: str,
    id_getter,
    result: BundleConsistencyResult,
) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    if not isinstance(previews, list):
        result.add_error(
            BUNDLE_DOCUMENT_INVALID,
            f"{label} previews must be an array",
            path=label,
            expected="array",
            observed=type(previews).__name__,
        )
        return indexed
    for idx, preview in enumerate(previews):
        if not isinstance(preview, dict):
            result.add_error(
                BUNDLE_DOCUMENT_INVALID,
                f"{label}[{idx}] must be an object",
                path=f"{label}[{idx}]",
                expected="object",
                observed=type(preview).__name__,
            )
            continue
        module_id = id_getter(preview)
        if not isinstance(module_id, str) or not module_id:
            result.add_error(
                BUNDLE_MODULE_ID_MISMATCH,
                f"{label}[{idx}] module_id is missing or invalid",
                path=f"{label}[{idx}].module_id",
                observed=module_id,
            )
            continue
        if module_id in indexed:
            result.add_error(
                BUNDLE_DUPLICATE_PREVIEW,
                f"duplicate {label} preview for module_id {module_id}",
                path=f"{label}[{idx}].module_id",
                observed=module_id,
                module_id=module_id,
            )
            continue
        indexed[module_id] = preview
    return indexed


def build_bundle_consistency_report(
    run_plan: Any,
    input_previews: Any,
    result_previews: Any,
) -> BundleConsistencyResult:
    """Validate cross-document consistency for a module I/O preview bundle."""

    result = BundleConsistencyResult()
    if not isinstance(run_plan, dict):
        result.add_error(
            BUNDLE_DOCUMENT_INVALID,
            "run plan must be an object",
            path="run",
            expected="object",
            observed=type(run_plan).__name__,
        )
        return result.allow_if_clean()

    _add_doc_errors(result, "run plan", validate_run_manifest.validate_run(run_plan))
    modules = run_plan.get("modules")
    if not isinstance(modules, list):
        result.add_error(
            BUNDLE_DOCUMENT_INVALID,
            "run plan modules must be an array",
            path="run.modules",
            expected="array",
            observed=type(modules).__name__,
        )
        modules = []

    planned_modules: dict[str, dict[str, Any]] = {}
    for idx, module in enumerate(modules):
        if not isinstance(module, dict):
            result.add_error(
                BUNDLE_DOCUMENT_INVALID,
                f"run.modules[{idx}] must be an object",
                path=f"run.modules[{idx}]",
                expected="object",
                observed=type(module).__name__,
            )
            continue
        module_id = module.get("module_id")
        if not isinstance(module_id, str) or not module_id:
            result.add_error(
                BUNDLE_MODULE_ID_MISMATCH,
                f"run.modules[{idx}].module_id is missing",
                path=f"run.modules[{idx}].module_id",
                observed=module_id,
            )
            continue
        if module_id in planned_modules:
            result.add_error(
                BUNDLE_RUN_MODULE_DUPLICATE,
                f"duplicate run module_id {module_id}",
                path=f"run.modules[{idx}].module_id",
                observed=module_id,
                module_id=module_id,
            )
            continue
        planned_modules[module_id] = module

    inputs = _index_previews(input_previews, label="input", id_getter=_module_id_from_input, result=result)
    results = _index_previews(result_previews, label="result", id_getter=_module_id_from_result, result=result)

    for module_id, module_input in inputs.items():
        _add_doc_errors(result, f"module input preview {module_id}", validate_module_io_contract.validate_module_input(module_input))
        if module_id not in planned_modules:
            result.add_error(
                BUNDLE_EXTRA_PREVIEW,
                f"input preview module_id {module_id} is not present in run.modules",
                path=f"module_input[{module_id}].module.module_id",
                observed=module_id,
                module_id=module_id,
            )
        if module_id not in results:
            result.add_error(
                BUNDLE_MISSING_RESULT_FOR_INPUT,
                f"missing result preview for module_id {module_id}",
                path=f"module_result[{module_id}]",
                expected=module_id,
                module_id=module_id,
            )

    for module_id, module_result in results.items():
        _add_doc_errors(result, f"module result preview {module_id}", validate_module_io_contract.validate_module_result(module_result))
        if module_id not in planned_modules:
            result.add_error(
                BUNDLE_EXTRA_PREVIEW,
                f"result preview module_id {module_id} is not present in run.modules",
                path=f"module_result[{module_id}].module_id",
                observed=module_id,
                module_id=module_id,
            )
        if module_id not in inputs:
            result.add_error(
                BUNDLE_MISSING_INPUT_FOR_RESULT,
                f"missing input preview for module_id {module_id}",
                path=f"module_input[{module_id}]",
                expected=module_id,
                module_id=module_id,
            )

    for module_id in planned_modules:
        if module_id not in inputs:
            result.add_error(
                BUNDLE_MISSING_INPUT_FOR_RESULT,
                f"missing input preview for planned module_id {module_id}",
                path=f"module_input[{module_id}]",
                module_id=module_id,
            )
        if module_id not in results:
            result.add_error(
                BUNDLE_MISSING_RESULT_FOR_INPUT,
                f"missing result preview for planned module_id {module_id}",
                path=f"module_result[{module_id}]",
                module_id=module_id,
            )

    missing_input_ids = sorted(set(planned_modules) - set(inputs))
    extra_input_ids = sorted(set(inputs) - set(planned_modules))
    if len(missing_input_ids) == 1 and len(extra_input_ids) == 1:
        missing_id = missing_input_ids[0]
        extra_id = extra_input_ids[0]
        result.add_error(
            BUNDLE_MODULE_ID_MISMATCH,
            f"input module_id {extra_id} must match planned module_id {missing_id}",
            path=f"module_input[{extra_id}].module.module_id",
            expected=missing_id,
            observed=extra_id,
            module_id=extra_id,
        )

    missing_result_ids = sorted(set(planned_modules) - set(results))
    extra_result_ids = sorted(set(results) - set(planned_modules))
    if len(missing_result_ids) == 1 and len(extra_result_ids) == 1:
        missing_id = missing_result_ids[0]
        extra_id = extra_result_ids[0]
        result.add_error(
            BUNDLE_MODULE_ID_MISMATCH,
            f"result module_id {extra_id} must match planned module_id {missing_id}",
            path=f"module_result[{extra_id}].module_id",
            expected=missing_id,
            observed=extra_id,
            module_id=extra_id,
        )
    run_id = run_plan.get("run_id")
    expected_created_at_utc = run_plan.get("created_at_utc")
    expected_mode = run_plan.get("policy", {}).get("mode") if isinstance(run_plan.get("policy"), dict) else None
    expected_dry_run = run_plan.get("execution", {}).get("dry_run") if isinstance(run_plan.get("execution"), dict) else None
    expected_runner = run_plan.get("execution", {}).get("runner") if isinstance(run_plan.get("execution"), dict) else None
    expected_program = run_plan.get("program")
    expected_target = run_plan.get("target")
    expected_policy = run_plan.get("policy")
    expected_profile = {
        "profile_id": run_plan.get("execution", {}).get("profile_id") if isinstance(run_plan.get("execution"), dict) else None,
        "profile_sha256": run_plan.get("execution", {}).get("profile_sha256") if isinstance(run_plan.get("execution"), dict) else None,
    }

    comparable_policy = None
    if isinstance(expected_policy, dict):
        comparable_policy = {
            "decision": expected_policy.get("decision"),
            "decision_artifact_path": expected_policy.get("decision_artifact_path"),
            "decision_sha256": expected_policy.get("decision_sha256"),
            "checked_at_utc": expected_policy.get("checked_at_utc"),
        }

    for module_id in sorted(set(inputs) & set(results) & set(planned_modules)):
        module_input = inputs[module_id]
        module_result = results[module_id]
        planned_module = planned_modules[module_id]

        input_run = module_input.get("run", {}) if isinstance(module_input.get("run"), dict) else {}
        input_module = module_input.get("module", {}) if isinstance(module_input.get("module"), dict) else {}
        input_constraints = module_input.get("constraints", {}) if isinstance(module_input.get("constraints"), dict) else {}
        input_output = module_input.get("output", {}) if isinstance(module_input.get("output"), dict) else {}

        _same(input_run.get("run_id"), run_id, BUNDLE_RUN_ID_MISMATCH, f"module_input[{module_id}].run.run_id", result, module_id=module_id)
        _same(input_run.get("created_at_utc"), expected_created_at_utc, BUNDLE_CREATED_AT_UTC_MISMATCH, f"module_input[{module_id}].run.created_at_utc", result, module_id=module_id)
        _same(module_result.get("run_id"), run_id, BUNDLE_RUN_ID_MISMATCH, f"module_result[{module_id}].run_id", result, module_id=module_id)
        _same(module_result.get("run_id"), input_run.get("run_id"), BUNDLE_RUN_ID_MISMATCH, f"module_result[{module_id}].run_id", result, module_id=module_id)
        _same(input_module.get("module_id"), planned_module.get("module_id"), BUNDLE_MODULE_ID_MISMATCH, f"module_input[{module_id}].module.module_id", result, module_id=module_id)
        _same(module_result.get("module_id"), input_module.get("module_id"), BUNDLE_MODULE_ID_MISMATCH, f"module_result[{module_id}].module_id", result, module_id=module_id)
        _same(input_module.get("manifest_sha256"), planned_module.get("manifest_sha256"), BUNDLE_MANIFEST_HASH_MISMATCH, f"module_input[{module_id}].module.manifest_sha256", result, module_id=module_id)
        _same(input_run.get("mode"), expected_mode, BUNDLE_MODE_MISMATCH, f"module_input[{module_id}].run.mode", result, module_id=module_id)
        _same(input_run.get("dry_run"), expected_dry_run, BUNDLE_DRY_RUN_MISMATCH, f"module_input[{module_id}].run.dry_run", result, module_id=module_id)
        _same(input_run.get("runner"), expected_runner, BUNDLE_RUNNER_MISMATCH, f"module_input[{module_id}].run.runner", result, module_id=module_id)
        _same(module_input.get("program"), expected_program, BUNDLE_PROGRAM_MISMATCH, f"module_input[{module_id}].program", result, module_id=module_id)
        _same(module_input.get("target"), expected_target, BUNDLE_TARGET_MISMATCH, f"module_input[{module_id}].target", result, module_id=module_id)
        _same(module_input.get("policy"), comparable_policy, BUNDLE_POLICY_MISMATCH, f"module_input[{module_id}].policy", result, module_id=module_id)
        _same(module_input.get("profile"), expected_profile, BUNDLE_PROFILE_MISMATCH, f"module_input[{module_id}].profile", result, module_id=module_id)

        expected_output_dir = f"runs/{run_id}/modules/{module_id}"
        _same(input_output.get("module_output_dir"), expected_output_dir, BUNDLE_OUTPUT_PATH_MISMATCH, f"module_input[{module_id}].output.module_output_dir", result, module_id=module_id)
        if input_output.get("findings") != []:
            result.add_error(
                BUNDLE_FINDINGS_NOT_EMPTY,
                f"input {module_id} output.findings must be empty",
                path=f"module_input[{module_id}].output.findings",
                expected=[],
                observed=input_output.get("findings"),
                module_id=module_id,
            )
        if input_output.get("evidence") != []:
            result.add_error(
                BUNDLE_EVIDENCE_NOT_EMPTY,
                f"input {module_id} output.evidence must be empty",
                path=f"module_input[{module_id}].output.evidence",
                expected=[],
                observed=input_output.get("evidence"),
                module_id=module_id,
            )

        for key, expected in {
            "supports_dry_run": True,
            "requires_network": False,
            "network_access": "none",
            "target_touching": False,
            "destructive": False,
            "intrusive": False,
            "emits_findings": False,
            "emits_evidence": False,
            "manual_verification_required": True,
            "scanner_output_only": True,
            "store_redacted_evidence_only": True,
            "stores_raw_secrets": False,
            "writes_to_loot": False,
            "allows_destructive_actions": False,
            "allows_oast_callbacks": False,
        }.items():
            if input_constraints.get(key) != expected:
                result.add_error(
                    BUNDLE_CONSTRAINT_MISMATCH,
                    f"input {module_id} constraints.{key} must be {expected!r}",
                    path=f"module_input[{module_id}].constraints.{key}",
                    expected=expected,
                    observed=input_constraints.get(key),
                    module_id=module_id,
                )

        if module_result.get("status") not in RESULT_STATUSES:
            result.add_error(
                BUNDLE_STATUS_INVALID,
                f"result {module_id} status is unsupported",
                path=f"module_result[{module_id}].status",
                expected=sorted(RESULT_STATUSES),
                observed=module_result.get("status"),
                module_id=module_id,
            )
        if module_result.get("dry_run") is not True or module_result.get("dry_run") != expected_dry_run:
            result.add_error(
                BUNDLE_DRY_RUN_MISMATCH,
                f"result {module_id} dry_run must match dry-run plan",
                path=f"module_result[{module_id}].dry_run",
                expected=True,
                observed=module_result.get("dry_run"),
                module_id=module_id,
            )
        if module_result.get("target_touching") is not False:
            result.add_error(
                BUNDLE_TARGET_TOUCHING_MISMATCH,
                f"result {module_id} target_touching must be false",
                path=f"module_result[{module_id}].target_touching",
                expected=False,
                observed=module_result.get("target_touching"),
                module_id=module_id,
            )
        if module_result.get("findings") != []:
            result.add_error(
                BUNDLE_FINDINGS_NOT_EMPTY,
                f"result {module_id} findings must be empty",
                path=f"module_result[{module_id}].findings",
                expected=[],
                observed=module_result.get("findings"),
                module_id=module_id,
            )
        if module_result.get("evidence") != []:
            result.add_error(
                BUNDLE_EVIDENCE_NOT_EMPTY,
                f"result {module_id} evidence must be empty",
                path=f"module_result[{module_id}].evidence",
                expected=[],
                observed=module_result.get("evidence"),
                module_id=module_id,
            )

    return result.allow_if_clean()


def load_json(path: str | Path) -> Any:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def main(argv: list[str] | None = None) -> tuple[int, dict[str, Any]]:
    parser = argparse.ArgumentParser(description="Validate offline module I/O preview bundle consistency.")
    parser.add_argument("--run", required=True, help="Path to a run/1.0 JSON document.")
    parser.add_argument("--input", action="append", required=True, help="Path to a module_input/1.0 JSON document. Repeatable.")
    parser.add_argument("--result", action="append", required=True, help="Path to a module_result/1.0 JSON document. Repeatable.")
    parser.add_argument("--json", action="store_true", help="Print structured JSON output.")
    args = parser.parse_args(argv)

    try:
        run_plan = load_json(args.run)
        inputs = [load_json(path) for path in args.input]
        results = [load_json(path) for path in args.result]
        validation = build_bundle_consistency_report(run_plan, inputs, results)
    except (OSError, json.JSONDecodeError) as exc:
        validation = BundleConsistencyResult()
        validation.add_error(
            BUNDLE_DOCUMENT_INVALID,
            f"failed to load JSON: {exc}",
            path="bundle_input",
            expected="valid JSON document",
            observed=str(exc),
        )
        validation.allow_if_clean()

    payload = validation.as_dict()
    if args.json or validation.verdict != "allow":
        print(json.dumps(payload, indent=2, sort_keys=True))
    return (0 if validation.verdict == "allow" else 1), payload


if __name__ == "__main__":
    code, _payload = main()
    raise SystemExit(code)
