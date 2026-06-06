import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "scripts" / "module_runner.py"
BUNDLE_PATH = ROOT / "scripts" / "validate_module_io_bundle.py"

runner_spec = importlib.util.spec_from_file_location("module_runner_for_bundle_tests", RUNNER_PATH)
runner = importlib.util.module_from_spec(runner_spec)
assert runner_spec.loader is not None
sys.modules[runner_spec.name] = runner
runner_spec.loader.exec_module(runner)

bundle_spec = importlib.util.spec_from_file_location("validate_module_io_bundle", BUNDLE_PATH)
bundle = importlib.util.module_from_spec(bundle_spec)
assert bundle_spec.loader is not None
sys.modules[bundle_spec.name] = bundle
bundle_spec.loader.exec_module(bundle)

RUN_ID = "20260516T020304Z_bundle"
TARGET = "https://example.test/"
PROGRAM_SHA = "c" * 64
GLOBAL_SHA = "d" * 64


def passive_manifest(module_id="passive_headers_metadata"):
    return {
        "schema_version": "module_manifest/1.0",
        "module_id": module_id,
        "version": "0.1.0",
        "name": "Passive Headers Metadata",
        "description": "Dry-run-safe passive metadata planning fixture.",
        "risk_level": "info",
        "target_types": ["url"],
        "technique_tags": ["passive.http_headers"],
        "execution": {
            "supports_dry_run": True,
            "requires_network": False,
            "network_access": "none",
            "target_touching": False,
            "destructive": False,
            "intrusive": False,
            "default_profile": "audit-baseline",
        },
        "external_tools": [
            {"name": "python-stdlib", "required": True, "version_constraint": ">=3.11"}
        ],
        "output_contracts": {
            "run_schema": "run/1.0",
            "finding_schema": "finding/1.0",
            "evidence_schema": "evidence/1.0",
            "emits_findings": False,
            "emits_evidence": False,
        },
        "safety_gates": {
            "require_policy_decision": True,
            "require_scope_match": True,
            "manual_verification_required": True,
            "scanner_output_only": True,
            "store_redacted_evidence_only": True,
            "stores_raw_secrets": False,
            "writes_to_loot": False,
            "allows_destructive_actions": False,
            "allows_oast_callbacks": False,
        },
        "references": ["https://github.com/projectdiscovery/nuclei-templates"],
    }


def policy_artifact():
    return {
        "schema_version": "policy_boundary/1.0",
        "artifact_created_at_utc": "2026-05-16T02:03:00Z",
        "boundary": {
            "status": "allow",
            "exit_code": 0,
            "audit_event": "PROGRAM_POLICY_ALLOW",
            "errors": [],
        },
        "request": {
            "program": "demo-program",
            "target": TARGET,
            "technique": "http_probe",
            "mode": "dry-run",
            "global_scope": "config/scope.txt",
            "ignore_time": True,
        },
        "decision": {
            "schema_version": "policy_decision/1.0",
            "verdict": "allow",
            "program_slug": "demo-program",
            "target": TARGET,
            "normalized_target": "example.test",
            "target_type": "url",
            "technique": "http_probe",
            "mode": "dry-run",
            "reasons": ["fixture"],
            "errors": [],
            "warnings": [],
            "deny_reason_codes": [],
            "audit_event": "PROGRAM_POLICY_ALLOW",
            "program_file_sha256": PROGRAM_SHA,
            "global_scope_sha256": GLOBAL_SHA,
            "decided_at_utc": "2026-05-16T02:03:01Z",
        },
        "helper": {"returncode": 0, "timed_out": False},
    }


class ModuleIoBundleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.profile_path = self.root / "modules" / "profiles" / "audit-baseline.json"
        self.profile_path.parent.mkdir(parents=True)
        self.profile_path.write_text(
            (ROOT / "modules" / "profiles" / "audit-baseline.json").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        self.policy_path = self.root / "runs" / RUN_ID / "policy" / "decision.json"
        self.policy_path.parent.mkdir(parents=True)
        self.policy_path.write_text(json.dumps(policy_artifact()), encoding="utf-8")
        self.manifest_path = self.write_manifest(passive_manifest())

    def tearDown(self):
        self.tmp.cleanup()

    def write_manifest(self, manifest):
        module_id = manifest["module_id"]
        path = self.root / "modules" / module_id / "module.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(manifest), encoding="utf-8")
        return path

    def build_preview_bundle(self, manifest_paths=None):
        result = runner.build_dry_run_plan(
            manifest_paths=manifest_paths or [self.manifest_path],
            policy_artifact_path=self.policy_path,
            run_id=RUN_ID,
            target_type="url",
            target_value=TARGET,
            mode="dry-run",
            profile="audit-baseline",
            profile_root=self.root,
            include_module_io_preview=True,
        )
        self.assertEqual(result.verdict, "allow", result.errors)
        return result.plan, result.module_input_previews, result.module_result_previews

    def assertDeniedWithCode(self, validation, code):
        self.assertEqual(validation.verdict, "deny", validation.as_dict())
        self.assertIn(code, validation.error_codes, validation.as_dict())

    def assertDetailForCodeContainsPath(self, validation, code, expected_path):
        details = validation.as_dict().get("error_details", [])
        matching = [detail for detail in details if detail.get("code") == code]
        self.assertTrue(matching, validation.as_dict())
        self.assertTrue(
            any(expected_path in detail.get("path", "") for detail in matching),
            {"expected_path": expected_path, "matching": matching, "payload": validation.as_dict()},
        )
        return matching

    def assertDetailForCode(self, validation, code, *, expected_path, expected=None, observed=None, module_id=None):
        matching = self.assertDetailForCodeContainsPath(validation, code, expected_path)
        for detail in matching:
            if expected_path not in detail.get("path", ""):
                continue
            if expected is not None and detail.get("expected") != expected:
                continue
            if observed is not None and detail.get("observed") != observed:
                continue
            if module_id is not None and detail.get("module_id") != module_id:
                continue
            return detail
        self.fail({"expected_path": expected_path, "expected": expected, "observed": observed, "module_id": module_id, "matching": matching})

    def test_runner_preview_bundle_happy_path_validates(self):
        plan, inputs, results = self.build_preview_bundle()
        validation = bundle.build_bundle_consistency_report(plan, inputs, results)
        self.assertEqual(validation.verdict, "allow", validation.as_dict())
        self.assertEqual(validation.error_codes, [])

    def test_two_module_bundle_is_order_independent(self):
        second_path = self.write_manifest(passive_manifest("passive_tls_metadata"))
        plan, inputs, results = self.build_preview_bundle([self.manifest_path, second_path])
        validation = bundle.build_bundle_consistency_report(plan, list(reversed(inputs)), list(reversed(results)))
        self.assertEqual(validation.verdict, "allow", validation.as_dict())

    def test_bundle_denies_result_run_id_mismatch(self):
        plan, inputs, results = self.build_preview_bundle()
        results[0]["run_id"] = "20260516T999999Z_other"
        self.assertDeniedWithCode(bundle.build_bundle_consistency_report(plan, inputs, results), bundle.BUNDLE_RUN_ID_MISMATCH)

    def test_bundle_denies_missing_extra_and_duplicate_previews(self):
        plan, inputs, results = self.build_preview_bundle()
        with self.subTest("missing result"):
            self.assertDeniedWithCode(bundle.build_bundle_consistency_report(plan, inputs, []), bundle.BUNDLE_MISSING_RESULT_FOR_INPUT)
        with self.subTest("missing input"):
            self.assertDeniedWithCode(bundle.build_bundle_consistency_report(plan, [], results), bundle.BUNDLE_MISSING_INPUT_FOR_RESULT)
        with self.subTest("duplicate input"):
            self.assertDeniedWithCode(bundle.build_bundle_consistency_report(plan, inputs + [dict(inputs[0])], results), bundle.BUNDLE_DUPLICATE_PREVIEW)
        with self.subTest("extra result"):
            extra = dict(results[0])
            extra["module_id"] = "extra.preview_module"
            self.assertDeniedWithCode(bundle.build_bundle_consistency_report(plan, inputs, results + [extra]), bundle.BUNDLE_EXTRA_PREVIEW)

    def test_bundle_denies_manifest_hash_policy_profile_program_and_target_mismatch(self):
        plan, inputs, results = self.build_preview_bundle()
        cases = [
            ("manifest", lambda: inputs[0]["module"].__setitem__("manifest_sha256", "a" * 64), bundle.BUNDLE_MANIFEST_HASH_MISMATCH),
            ("policy", lambda: inputs[0]["policy"].__setitem__("decision_sha256", "b" * 64), bundle.BUNDLE_POLICY_MISMATCH),
            ("profile", lambda: inputs[0]["profile"].__setitem__("profile_sha256", "e" * 64), bundle.BUNDLE_PROFILE_MISMATCH),
            ("program", lambda: inputs[0]["program"].__setitem__("slug", "other-program"), bundle.BUNDLE_PROGRAM_MISMATCH),
            ("target", lambda: inputs[0]["target"].__setitem__("value", "https://other.example/"), bundle.BUNDLE_TARGET_MISMATCH),
        ]
        for name, mutate, code in cases:
            with self.subTest(name):
                plan_case, inputs_case, results_case = self.build_preview_bundle()
                inputs = inputs_case
                mutate()
                self.assertDeniedWithCode(bundle.build_bundle_consistency_report(plan_case, inputs_case, results_case), code)

    def test_bundle_denies_non_empty_artifacts_and_bad_output_path(self):
        plan, inputs, results = self.build_preview_bundle()
        with self.subTest("result findings"):
            results[0]["findings"] = [{"id": "bad"}]
            validation = bundle.build_bundle_consistency_report(plan, inputs, results)
            self.assertDeniedWithCode(validation, bundle.BUNDLE_FINDINGS_NOT_EMPTY)
        with self.subTest("input evidence"):
            plan, inputs, results = self.build_preview_bundle()
            inputs[0]["output"]["evidence"] = ["bad"]
            validation = bundle.build_bundle_consistency_report(plan, inputs, results)
            self.assertDeniedWithCode(validation, bundle.BUNDLE_EVIDENCE_NOT_EMPTY)
        with self.subTest("output path"):
            plan, inputs, results = self.build_preview_bundle()
            inputs[0]["output"]["module_output_dir"] = f"runs/{RUN_ID}/modules/other"
            validation = bundle.build_bundle_consistency_report(plan, inputs, results)
            self.assertDeniedWithCode(validation, bundle.BUNDLE_OUTPUT_PATH_MISMATCH)

    def test_bundle_denies_malformed_preview_via_document_validator(self):
        plan, inputs, results = self.build_preview_bundle()
        inputs[0]["output"]["module_output_dir"] = f"runs/{RUN_ID}/modules/../bad"
        validation = bundle.build_bundle_consistency_report(plan, inputs, results)
        self.assertDeniedWithCode(validation, bundle.BUNDLE_DOCUMENT_INVALID)

    def test_bundle_denies_mode_runner_dry_run_and_created_at_mismatches_with_details(self):
        cases = [
            (
                "mode",
                lambda plan, inputs, results: inputs[0]["run"].__setitem__("mode", "planned"),
                bundle.BUNDLE_MODE_MISMATCH,
                "module_input[passive_headers_metadata].run.mode",
            ),
            (
                "runner",
                lambda plan, inputs, results: inputs[0]["run"].__setitem__("runner", "other-runner"),
                bundle.BUNDLE_RUNNER_MISMATCH,
                "module_input[passive_headers_metadata].run.runner",
            ),
            (
                "input dry_run",
                lambda plan, inputs, results: inputs[0]["run"].__setitem__("dry_run", False),
                bundle.BUNDLE_DRY_RUN_MISMATCH,
                "module_input[passive_headers_metadata].run.dry_run",
            ),
            (
                "result dry_run",
                lambda plan, inputs, results: results[0].__setitem__("dry_run", False),
                bundle.BUNDLE_DRY_RUN_MISMATCH,
                "module_result[passive_headers_metadata].dry_run",
            ),
            (
                "created_at",
                lambda plan, inputs, results: inputs[0]["run"].__setitem__("created_at_utc", "2026-05-16T99:99:99Z"),
                bundle.BUNDLE_CREATED_AT_UTC_MISMATCH,
                "module_input[passive_headers_metadata].run.created_at_utc",
            ),
        ]
        for name, mutate, code, expected_path in cases:
            with self.subTest(name):
                plan, inputs, results = self.build_preview_bundle()
                mutate(plan, inputs, results)
                validation = bundle.build_bundle_consistency_report(plan, inputs, results)
                self.assertDeniedWithCode(validation, code)
                self.assertDetailForCodeContainsPath(validation, code, expected_path)

    def test_bundle_denies_status_target_touching_constraint_and_module_id_mismatches(self):
        cases = [
            (
                "status",
                lambda plan, inputs, results: results[0].__setitem__("status", "executed"),
                bundle.BUNDLE_STATUS_INVALID,
                "module_result[passive_headers_metadata].status",
            ),
            (
                "target_touching",
                lambda plan, inputs, results: results[0].__setitem__("target_touching", True),
                bundle.BUNDLE_TARGET_TOUCHING_MISMATCH,
                "module_result[passive_headers_metadata].target_touching",
            ),
            (
                "constraint",
                lambda plan, inputs, results: inputs[0]["constraints"].__setitem__("requires_network", True),
                bundle.BUNDLE_CONSTRAINT_MISMATCH,
                "module_input[passive_headers_metadata].constraints.requires_network",
            ),
            (
                "module_id",
                lambda plan, inputs, results: results[0].__setitem__("module_id", "different_module"),
                bundle.BUNDLE_MODULE_ID_MISMATCH,
                "module_result[different_module].module_id",
            ),
        ]
        for name, mutate, code, expected_path in cases:
            with self.subTest(name):
                plan, inputs, results = self.build_preview_bundle()
                mutate(plan, inputs, results)
                validation = bundle.build_bundle_consistency_report(plan, inputs, results)
                self.assertDeniedWithCode(validation, code)
                self.assertDetailForCodeContainsPath(validation, code, expected_path)

    def test_bundle_denies_duplicate_run_module_entries_with_detail(self):
        plan, inputs, results = self.build_preview_bundle()
        plan["modules"].append(dict(plan["modules"][0]))
        validation = bundle.build_bundle_consistency_report(plan, inputs, results)
        self.assertDeniedWithCode(validation, bundle.BUNDLE_RUN_MODULE_DUPLICATE)
        self.assertDetailForCode(
            validation,
            bundle.BUNDLE_RUN_MODULE_DUPLICATE,
            expected_path="run.modules[1].module_id",
            observed="passive_headers_metadata",
            module_id="passive_headers_metadata",
        )

    def test_bundle_denies_multimodule_result_module_id_mismatch_with_detail(self):
        second_path = self.write_manifest(passive_manifest("passive_tls_metadata"))
        plan, inputs, results = self.build_preview_bundle([self.manifest_path, second_path])
        results[1]["module_id"] = "different_module"
        validation = bundle.build_bundle_consistency_report(plan, inputs, results)
        self.assertDeniedWithCode(validation, bundle.BUNDLE_MODULE_ID_MISMATCH)
        self.assertDetailForCode(
            validation,
            bundle.BUNDLE_MODULE_ID_MISMATCH,
            expected_path="module_result[different_module].module_id",
            expected="passive_tls_metadata",
            observed="different_module",
            module_id="different_module",
        )

    def test_bundle_error_details_are_populated_for_missing_and_extra_previews(self):
        plan, inputs, results = self.build_preview_bundle()
        extra = dict(results[0])
        extra["module_id"] = "extra.preview_module"
        validation = bundle.build_bundle_consistency_report(plan, inputs, results + [extra])
        for code in (bundle.BUNDLE_EXTRA_PREVIEW, bundle.BUNDLE_MISSING_INPUT_FOR_RESULT):
            matching = [detail for detail in validation.as_dict()["error_details"] if detail.get("code") == code]
            self.assertTrue(matching, validation.as_dict())
            self.assertTrue(all(detail.get("path") for detail in matching), validation.as_dict())
            self.assertTrue(all("expected" in detail and "observed" in detail for detail in matching), validation.as_dict())

    def test_cli_returns_structured_json_and_nonzero_on_inconsistency(self):
        plan, inputs, results = self.build_preview_bundle()
        results[0]["run_id"] = "20260516T999999Z_other"
        run_path = self.root / "run.json"
        input_path = self.root / "input.json"
        result_path = self.root / "result.json"
        run_path.write_text(json.dumps(plan), encoding="utf-8")
        input_path.write_text(json.dumps(inputs[0]), encoding="utf-8")
        result_path.write_text(json.dumps(results[0]), encoding="utf-8")
        completed = subprocess.run(
            [sys.executable, str(BUNDLE_PATH), "--run", str(run_path), "--input", str(input_path), "--result", str(result_path), "--json"],
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertNotEqual(completed.returncode, 0)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["verdict"], "deny")
        self.assertIn(bundle.BUNDLE_RUN_ID_MISMATCH, payload["error_codes"])


if __name__ == "__main__":
    unittest.main()
