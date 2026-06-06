import contextlib
import importlib.util
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "scripts" / "module_runner.py"

spec = importlib.util.spec_from_file_location("module_runner", RUNNER_PATH)
runner = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = runner
spec.loader.exec_module(runner)

RUN_ID = "20260516T020304Z_runner"
TARGET = "https://example.test/"
POLICY_SHA = "b" * 64
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


def active_manifest():
    data = passive_manifest("active_headers_probe")
    data["technique_tags"] = ["active.http_get"]
    data["execution"]["requires_network"] = True
    data["execution"]["network_access"] = "target-http"
    data["execution"]["target_touching"] = True
    return data


def policy_artifact(verdict="allow", *, target=TARGET, mode="dry-run"):
    return {
        "schema_version": "policy_boundary/1.0",
        "artifact_created_at_utc": "2026-05-16T02:03:00Z",
        "boundary": {
            "status": verdict,
            "exit_code": 0 if verdict == "allow" else 1,
            "audit_event": "PROGRAM_POLICY_ALLOW" if verdict == "allow" else "PROGRAM_POLICY_DENY",
            "errors": [],
        },
        "request": {
            "program": "demo-program",
            "target": target,
            "technique": "http_probe",
            "mode": mode,
            "global_scope": "config/scope.txt",
            "ignore_time": True,
        },
        "decision": {
            "schema_version": "policy_decision/1.0",
            "verdict": verdict,
            "program_slug": "demo-program",
            "target": target,
            "normalized_target": "example.test",
            "target_type": "url",
            "technique": "http_probe",
            "mode": mode,
            "reasons": ["fixture"],
            "errors": [],
            "warnings": [],
            "deny_reason_codes": [],
            "audit_event": "PROGRAM_POLICY_ALLOW" if verdict == "allow" else "PROGRAM_POLICY_DENY",
            "program_file_sha256": PROGRAM_SHA,
            "global_scope_sha256": GLOBAL_SHA,
            "decided_at_utc": "2026-05-16T02:03:01Z",
        },
        "helper": {"returncode": 0 if verdict == "allow" else 1, "timed_out": False},
    }


class ModuleRunnerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.module_path = self.root / "modules" / "passive_headers_metadata" / "module.json"
        self.module_path.parent.mkdir(parents=True)
        self.module_path.write_text(json.dumps(passive_manifest()), encoding="utf-8")
        self.profile_path = self.root / "modules" / "profiles" / "audit-baseline.json"
        self.profile_path.parent.mkdir(parents=True)
        self.profile_path.write_text(
            (ROOT / "modules" / "profiles" / "audit-baseline.json").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        self.policy_path = self.root / "runs" / RUN_ID / "policy" / "decision.json"
        self.policy_path.parent.mkdir(parents=True)
        self.policy_path.write_text(json.dumps(policy_artifact()), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def build_plan(self, **overrides):
        kwargs = {
            "manifest_paths": [self.module_path],
            "policy_artifact_path": self.policy_path,
            "run_id": RUN_ID,
            "target_type": "url",
            "target_value": TARGET,
            "mode": "dry-run",
            "profile": "audit-baseline",
            "profile_root": self.root,
        }
        kwargs.update(overrides)
        return runner.build_dry_run_plan(**kwargs)

    def copy_committed_module_manifest(self, fixture_root, module_dir_name):
        source = ROOT / "modules" / "checks" / "level1" / module_dir_name / "module.json"
        dest = fixture_root / "modules" / "checks" / "level1" / module_dir_name / "module.json"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        return dest

    def copy_committed_module_tree(self, fixture_root, module_dir_name):
        source = ROOT / "modules" / "checks" / "level1" / module_dir_name
        dest = fixture_root / "modules" / "checks" / "level1" / module_dir_name
        shutil.copytree(source, dest, dirs_exist_ok=True)
        return dest

    def copy_audit_baseline_profile(self, fixture_root):
        fixture_profile = fixture_root / "modules" / "profiles" / "audit-baseline.json"
        fixture_profile.parent.mkdir(parents=True, exist_ok=True)
        fixture_profile.write_text(
            (ROOT / "modules" / "profiles" / "audit-baseline.json").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        return fixture_profile

    def write_policy_artifact(self, fixture_root):
        policy = fixture_root / "runs" / RUN_ID / "policy" / "decision.json"
        policy.parent.mkdir(parents=True, exist_ok=True)
        policy.write_text(json.dumps(policy_artifact()), encoding="utf-8")
        return policy

    def assertIssueDetailShape(self, detail, *, code, severity, component, path=None, field=None, profile_id=None, module_id=None):
        self.assertEqual(detail["code"], code)
        self.assertIsInstance(detail["message"], str)
        self.assertTrue(detail["message"])
        self.assertEqual(detail["severity"], severity)
        self.assertEqual(detail["component"], component)
        for key, expected in {
            "path": path,
            "field": field,
            "profile_id": profile_id,
            "module_id": module_id,
        }.items():
            if expected is None:
                self.assertNotIn(key, detail)
            else:
                self.assertEqual(detail[key], str(expected))

    def test_safe_passive_module_generates_valid_dry_run_run_manifest_preview(self):
        result = self.build_plan()
        self.assertEqual(result.verdict, "allow", result.errors)
        plan = result.plan
        self.assertEqual(plan["schema_version"], "run/1.0")
        self.assertEqual(plan["run_id"], RUN_ID)
        self.assertEqual(plan["status"], "planned")
        self.assertEqual(plan["policy"]["decision"], "allow")
        self.assertEqual(plan["policy"]["decision_sha256"], runner.sha256_file(self.policy_path))
        self.assertEqual(plan["execution"]["dry_run"], True)
        self.assertEqual(plan["execution"]["profile_id"], "audit-baseline")
        self.assertTrue(plan["execution"]["profile_sha256"])
        self.assertEqual(plan["execution"]["target_touching"], False)
        self.assertEqual(plan["modules"][0]["module_id"], "passive_headers_metadata")
        self.assertEqual(plan["modules"][0]["status"], "planned")
        self.assertEqual(plan["artifacts"], {"findings": [], "evidence": []})
        self.assertEqual(plan["review"]["manual_verification_required"], True)
        self.assertEqual(result.module_input_previews, [])
        self.assertEqual(result.module_result_previews, [])

    def test_include_module_io_preview_builds_valid_non_executed_envelopes(self):
        result = self.build_plan(include_module_io_preview=True)
        self.assertEqual(result.verdict, "allow", result.errors)
        self.assertEqual(result.plan["artifacts"], {"findings": [], "evidence": []})
        self.assertEqual(len(result.module_input_previews), 1)
        self.assertEqual(len(result.module_result_previews), 1)
        module_input = result.module_input_previews[0]
        module_result = result.module_result_previews[0]
        self.assertEqual(module_input["schema_version"], "module_input/1.0")
        self.assertEqual(module_input["run"]["mode"], "dry-run")
        self.assertEqual(module_input["constraints"]["requires_network"], False)
        self.assertEqual(module_input["constraints"]["target_touching"], False)
        self.assertEqual(module_input["constraints"]["emits_findings"], False)
        self.assertEqual(module_input["constraints"]["emits_evidence"], False)
        self.assertEqual(module_input["output"], {
            "module_output_dir": f"runs/{RUN_ID}/modules/passive_headers_metadata",
            "findings": [],
            "evidence": [],
        })
        self.assertEqual(module_result["schema_version"], "module_result/1.0")
        self.assertEqual(module_result["status"], "not_executed")
        self.assertEqual(module_result["dry_run"], True)
        self.assertEqual(module_result["target_touching"], False)
        self.assertEqual(module_result["findings"], [])
        self.assertEqual(module_result["evidence"], [])
        self.assertEqual(runner.validate_module_io_contract.validate_module_input(module_input).verdict, "allow")
        self.assertEqual(runner.validate_module_io_contract.validate_module_result(module_result).verdict, "allow")
        payload = result.as_dict()
        self.assertIn("module_input_previews", payload)
        self.assertIn("module_result_previews", payload)

    def test_committed_level1_audit_fixture_is_dry_run_plannable(self):
        fixture_path = ROOT / "modules" / "checks" / "level1" / "policy_decision_metadata_audit" / "module.json"
        result = self.build_plan(manifest_paths=[fixture_path])
        self.assertEqual(result.verdict, "allow", result.errors)
        plan = result.plan
        self.assertEqual(plan["execution"]["dry_run"], True)
        self.assertEqual(plan["execution"]["profile_id"], "audit-baseline")
        self.assertTrue(plan["execution"]["profile_sha256"])
        self.assertEqual(plan["execution"]["target_touching"], False)
        self.assertEqual(plan["modules"], [
            {
                "module_id": "level1.policy_decision_metadata_audit",
                "manifest_sha256": runner.sha256_file(fixture_path),
                "status": "planned",
            }
        ])
        self.assertEqual(plan["artifacts"], {"findings": [], "evidence": []})

    def test_invalid_module_manifest_is_denied_before_plan(self):
        data = passive_manifest()
        data["execution"]["supports_dry_run"] = False
        self.module_path.write_text(json.dumps(data), encoding="utf-8")
        result = self.build_plan()
        self.assertEqual(result.verdict, "deny")
        self.assertTrue(any("module manifest" in error or "supports_dry_run" in error for error in result.errors), result.errors)
        self.assertIsNone(result.plan)

    def test_missing_or_deny_policy_artifact_default_denies(self):
        missing = self.build_plan(policy_artifact_path=self.root / "missing.json")
        self.assertEqual(missing.verdict, "deny")
        self.assertTrue(any("policy artifact" in error for error in missing.errors), missing.errors)
        self.assertEqual(missing.error_codes, [])

        self.policy_path.write_text(json.dumps(policy_artifact("deny")), encoding="utf-8")
        denied = self.build_plan()
        self.assertEqual(denied.verdict, "deny")
        self.assertTrue(any("allow" in error for error in denied.errors), denied.errors)

    def test_dry_run_refuses_target_touching_module(self):
        self.module_path.write_text(json.dumps(active_manifest()), encoding="utf-8")
        result = self.build_plan()
        self.assertEqual(result.verdict, "deny")
        self.assertTrue(any("target_touching" in error for error in result.errors), result.errors)
        self.assertIn("PROFILE_CONSTRAINT_EXECUTION", result.error_codes)
        self.assertIn("PROFILE_CONSTRAINT_TECHNIQUE_TAG", result.error_codes)
        self.assertIsNone(result.plan)

    def test_explicit_manifest_profile_membership_mismatch_has_stable_code(self):
        data = passive_manifest("other.profile.module")
        data["execution"]["default_profile"] = "other-profile"
        self.module_path.write_text(json.dumps(data), encoding="utf-8")
        result = self.build_plan()
        self.assertEqual(result.verdict, "deny")
        self.assertIn("PROFILE_MEMBERSHIP_MISMATCH", result.error_codes)
        self.assertTrue(any(detail.code == "PROFILE_MEMBERSHIP_MISMATCH" for detail in result.error_details))
        payload = result.as_dict()
        self.assertIssueDetailShape(
            payload["error_details"][0],
            code="PROFILE_MEMBERSHIP_MISMATCH",
            severity="error",
            component="module_profile_selector",
            path=self.module_path,
            field="execution.default_profile",
            profile_id="audit-baseline",
            module_id="other.profile.module",
        )

    def test_explicit_manifest_target_type_violation_has_stable_code(self):
        result = self.build_plan(target_type="domain")
        self.assertEqual(result.verdict, "deny")
        self.assertIn("PROFILE_CONSTRAINT_TARGET_TYPE", result.error_codes)

    def test_policy_artifact_must_match_target_and_mode(self):
        self.policy_path.write_text(json.dumps(policy_artifact(target="https://other.test/")), encoding="utf-8")
        bad_target = self.build_plan()
        self.assertEqual(bad_target.verdict, "deny")
        self.assertTrue(any("target" in error for error in bad_target.errors), bad_target.errors)

        self.policy_path.write_text(json.dumps(policy_artifact(mode="planned")), encoding="utf-8")
        bad_mode = self.build_plan()
        self.assertEqual(bad_mode.verdict, "deny")
        self.assertTrue(any("mode" in error for error in bad_mode.errors), bad_mode.errors)

    def test_policy_artifact_must_match_target_type_and_be_in_run_policy_directory(self):
        bad = policy_artifact()
        bad["decision"]["target_type"] = "domain"
        self.policy_path.write_text(json.dumps(bad), encoding="utf-8")
        bad_type = self.build_plan()
        self.assertEqual(bad_type.verdict, "deny")
        self.assertTrue(any("target_type" in error for error in bad_type.errors), bad_type.errors)

        outside_path = self.root / "policy_boundary.json"
        outside_path.write_text(json.dumps(policy_artifact()), encoding="utf-8")
        bad_path = self.build_plan(policy_artifact_path=outside_path)
        self.assertEqual(bad_path.verdict, "deny")
        self.assertTrue(any("policy artifact path" in error for error in bad_path.errors), bad_path.errors)

    def test_policy_artifact_boundary_contradictions_default_deny(self):
        cases = []
        with_boundary_errors = policy_artifact()
        with_boundary_errors["boundary"]["errors"] = ["helper timed out"]
        cases.append(("boundary.errors", with_boundary_errors))

        with_contract_errors = policy_artifact()
        with_contract_errors["boundary"]["contract_errors"] = ["bad contract"]
        cases.append(("boundary.contract_errors", with_contract_errors))

        with_helper_timeout = policy_artifact()
        with_helper_timeout["helper"]["timed_out"] = True
        cases.append(("helper.timed_out", with_helper_timeout))

        with_helper_nonzero = policy_artifact()
        with_helper_nonzero["helper"]["returncode"] = 1
        cases.append(("helper.returncode", with_helper_nonzero))

        with_decision_errors = policy_artifact()
        with_decision_errors["decision"]["errors"] = ["scope mismatch"]
        cases.append(("decision.errors", with_decision_errors))

        with_deny_codes = policy_artifact()
        with_deny_codes["decision"]["deny_reason_codes"] = ["NOT_IN_SCOPE"]
        cases.append(("decision.deny_reason_codes", with_deny_codes))

        with_boundary_deny_codes = policy_artifact()
        with_boundary_deny_codes["boundary"]["deny_reason_codes"] = ["NOT_IN_SCOPE"]
        cases.append(("boundary.deny_reason_codes", with_boundary_deny_codes))

        missing_helper = policy_artifact()
        del missing_helper["helper"]
        cases.append(("missing helper", missing_helper))

        malformed_helper = policy_artifact()
        malformed_helper["helper"] = {"returncode": 0}
        cases.append(("malformed helper", malformed_helper))

        for label, artifact in cases:
            self.policy_path.write_text(json.dumps(artifact), encoding="utf-8")
            with self.subTest(label=label):
                result = self.build_plan()
                self.assertEqual(result.verdict, "deny")
                self.assertTrue(result.errors)

    def test_cli_json_output_is_default_deny_without_policy_artifact(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code, payload = runner.main([
                "--manifest",
                str(self.module_path),
                "--policy-artifact",
                str(self.root / "missing.json"),
                "--run-id",
                RUN_ID,
                "--target-type",
                "url",
                "--target",
                TARGET,
                "--json",
            ])
        self.assertNotEqual(code, 0)
        self.assertEqual(payload["verdict"], "deny")
        self.assertTrue(payload["errors"])
        self.assertIn('"verdict": "deny"', stdout.getvalue())

    def test_profile_discovery_selects_committed_audit_baseline_fixture(self):
        result = runner.discover_profile_manifests(
            repo_root=ROOT,
            profile="audit-baseline",
            target_type="url",
            mode="dry-run",
        )
        self.assertEqual(result.verdict, "allow", result.errors)
        selected_ids = [module["module_id"] for module in result.modules]
        self.assertIn("level1.policy_decision_metadata_audit", selected_ids)
        selected_paths = [Path(path) for path in result.manifest_paths]
        self.assertIn(
            ROOT / "modules" / "checks" / "level1" / "policy_decision_metadata_audit" / "module.json",
            selected_paths,
        )
        for module in result.modules:
            self.assertEqual(module["profile"], "audit-baseline")
            self.assertEqual(module["requires_network"], False)
            self.assertEqual(module["network_access"], "none")
            self.assertEqual(module["target_touching"], False)

    def test_profile_discovery_fails_closed_on_duplicate_module_ids(self):
        modules_root = self.root / "modules" / "checks" / "level1"
        first = modules_root / "one" / "module.json"
        second = modules_root / "two" / "module.json"
        first.parent.mkdir(parents=True)
        second.parent.mkdir(parents=True)
        first.write_text(json.dumps(passive_manifest("duplicate.module")), encoding="utf-8")
        second.write_text(json.dumps(passive_manifest("duplicate.module")), encoding="utf-8")

        result = runner.discover_profile_manifests(
            repo_root=self.root,
            profile="audit-baseline",
            target_type="url",
            mode="dry-run",
        )
        self.assertEqual(result.verdict, "deny")
        self.assertTrue(any("duplicate module_id duplicate.module" in error for error in result.errors), result.errors)
        self.assertEqual(result.manifest_paths, [])

    def test_profile_discovery_fails_closed_on_malformed_manifest(self):
        module_path = self.root / "modules" / "checks" / "level1" / "bad" / "module.json"
        module_path.parent.mkdir(parents=True)
        module_path.write_text(json.dumps({"schema_version": "module_manifest/1.0"}), encoding="utf-8")

        result = runner.discover_profile_manifests(
            repo_root=self.root,
            profile="audit-baseline",
            target_type="url",
            mode="dry-run",
        )
        self.assertEqual(result.verdict, "deny")
        self.assertTrue(any("module manifest" in error for error in result.errors), result.errors)
        self.assertEqual(result.manifest_paths, [])

    def test_profile_discovery_fails_closed_on_path_escape(self):
        outside = self.root.parent / f"{self.root.name}_outside_module.json"
        try:
            outside.write_text(json.dumps(passive_manifest("outside.module")), encoding="utf-8")
            result = runner.discover_profile_manifests(
                repo_root=self.root,
                profile="audit-baseline",
                target_type="url",
                mode="dry-run",
                manifest_paths=[outside],
            )
            self.assertEqual(result.verdict, "deny")
            self.assertTrue(any("modules/checks" in error or "outside" in error for error in result.errors), result.errors)
            self.assertEqual(result.manifest_paths, [])
        finally:
            outside.unlink(missing_ok=True)

    def test_profile_discovery_denies_network_or_target_touching_audit_baseline_manifest(self):
        module_path = self.root / "modules" / "checks" / "level1" / "active" / "module.json"
        module_path.parent.mkdir(parents=True)
        module_path.write_text(json.dumps(active_manifest()), encoding="utf-8")

        result = runner.discover_profile_manifests(
            repo_root=self.root,
            profile="audit-baseline",
            target_type="url",
            mode="dry-run",
        )
        self.assertEqual(result.verdict, "deny")
        self.assertTrue(any("target_touching" in error or "network" in error for error in result.errors), result.errors)
        self.assertEqual(result.manifest_paths, [])

    def build_two_module_fixture_repo(self):
        fixture_root = self.root / "p3_3_two_module_repo"
        self.copy_audit_baseline_profile(fixture_root)
        self.copy_committed_module_manifest(fixture_root, "policy_decision_metadata_audit")
        self.copy_committed_module_manifest(fixture_root, "security_headers_baseline")
        policy = self.write_policy_artifact(fixture_root)
        return fixture_root, policy

    def build_two_module_tree_fixture_repo(self):
        fixture_root = self.root / "p3_4_two_module_tree_repo"
        self.copy_audit_baseline_profile(fixture_root)
        self.copy_committed_module_tree(fixture_root, "policy_decision_metadata_audit")
        self.copy_committed_module_tree(fixture_root, "security_headers_baseline")
        policy = self.write_policy_artifact(fixture_root)
        return fixture_root, policy

    def two_module_runner_preview_projection(self, fixture_root, policy):
        discovery = runner.discover_profile_manifests(
            repo_root=fixture_root,
            profile="audit-baseline",
            target_type="url",
            mode="dry-run",
        )
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code, payload = runner.main([
                "--discover-root",
                str(fixture_root),
                "--policy-artifact",
                str(policy),
                "--run-id",
                RUN_ID,
                "--target-type",
                "url",
                "--target",
                TARGET,
                "--profile",
                "audit-baseline",
                "--include-module-io-preview",
                "--json",
            ])
        self.assertEqual(discovery.verdict, "allow", discovery.errors)
        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["verdict"], "allow", payload["errors"])
        return {
            "discovered_module_ids": [module["module_id"] for module in discovery.modules],
            "discovery_error_codes": discovery.error_codes,
            "discovery_warning_codes": discovery.warning_codes,
            "payload_error_codes": payload["error_codes"],
            "payload_warning_codes": payload["warning_codes"],
            "payload_errors": payload["errors"],
            "payload_warnings": payload["warnings"],
            "plan_module_ids": [module["module_id"] for module in payload["plan"]["modules"]],
            "input_module_ids": [item["module"]["module_id"] for item in payload["module_input_previews"]],
            "result_projection": [
                {
                    "module_id": item["module_id"],
                    "status": item["status"],
                    "dry_run": item["dry_run"],
                    "target_touching": item["target_touching"],
                    "findings": item["findings"],
                    "evidence": item["evidence"],
                    "errors": item["errors"],
                    "warnings": item["warnings"],
                }
                for item in payload["module_result_previews"]
            ],
        }

    def test_cli_can_discover_profile_manifests_for_dry_run_plan(self):
        fixture_root = self.root / "fixture_repo"
        self.copy_committed_module_manifest(fixture_root, "policy_decision_metadata_audit")
        self.copy_audit_baseline_profile(fixture_root)
        policy = self.write_policy_artifact(fixture_root)

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code, payload = runner.main([
                "--discover-root",
                str(fixture_root),
                "--policy-artifact",
                str(policy),
                "--run-id",
                RUN_ID,
                "--target-type",
                "url",
                "--target",
                TARGET,
                "--profile",
                "audit-baseline",
                "--json",
            ])
        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["verdict"], "allow", payload["errors"])
        self.assertEqual(payload["plan"]["modules"][0]["module_id"], "level1.policy_decision_metadata_audit")
        self.assertIn('"profile": "audit-baseline"', stdout.getvalue())

    def test_p3_3_two_module_audit_baseline_discovery_happy_path(self):
        fixture_root, _policy = self.build_two_module_fixture_repo()

        first = runner.discover_profile_manifests(
            repo_root=fixture_root,
            profile="audit-baseline",
            target_type="url",
            mode="dry-run",
        )
        second = runner.discover_profile_manifests(
            repo_root=fixture_root,
            profile="audit-baseline",
            target_type="url",
            mode="dry-run",
        )
        self.assertEqual(first.verdict, "allow", first.errors)
        expected_ids = {"level1.policy_decision_metadata_audit", "level1.security_headers_baseline"}
        self.assertEqual({module["module_id"] for module in first.modules}, expected_ids)
        self.assertEqual(first.errors, [])
        self.assertEqual(first.error_codes, [])
        forbidden_warnings = {
            code for code in first.warning_codes
            if code == "PROFILE_MEMBERSHIP_MISMATCH" or code.startswith("PROFILE_CONSTRAINT_") or code == "PROFILE_EMPTY_SELECTION"
        }
        self.assertEqual(forbidden_warnings, set())
        self.assertEqual(first.modules, second.modules)

    def test_p3_3_two_module_cli_discovery_happy_path(self):
        fixture_root, policy = self.build_two_module_fixture_repo()

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code, payload = runner.main([
                "--discover-root",
                str(fixture_root),
                "--policy-artifact",
                str(policy),
                "--run-id",
                RUN_ID,
                "--target-type",
                "url",
                "--target",
                TARGET,
                "--profile",
                "audit-baseline",
                "--json",
            ])
        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["verdict"], "allow", payload["errors"])
        module_ids = {module["module_id"] for module in payload["plan"]["modules"]}
        self.assertEqual(module_ids, {"level1.policy_decision_metadata_audit", "level1.security_headers_baseline"})
        self.assertEqual(len(payload["plan"]["modules"]), 2)
        self.assertIn('"profile": "audit-baseline"', stdout.getvalue())

    def test_p3_3_two_module_bundle_consistency_with_module_io_preview(self):
        fixture_root, policy = self.build_two_module_fixture_repo()

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code, payload = runner.main([
                "--discover-root",
                str(fixture_root),
                "--policy-artifact",
                str(policy),
                "--run-id",
                RUN_ID,
                "--target-type",
                "url",
                "--target",
                TARGET,
                "--profile",
                "audit-baseline",
                "--include-module-io-preview",
                "--json",
            ])
        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["verdict"], "allow", payload["errors"])
        expected_ids = {"level1.policy_decision_metadata_audit", "level1.security_headers_baseline"}
        self.assertEqual({item["module"]["module_id"] for item in payload["module_input_previews"]}, expected_ids)
        self.assertEqual({item["module_id"] for item in payload["module_result_previews"]}, expected_ids)
        self.assertEqual(len(payload["module_input_previews"]), 2)
        self.assertEqual(len(payload["module_result_previews"]), 2)
        for module_result in payload["module_result_previews"]:
            self.assertEqual(module_result["status"], "not_executed")
            self.assertEqual(module_result["dry_run"], True)
            self.assertEqual(module_result["target_touching"], False)
            self.assertEqual(module_result["findings"], [])
            self.assertEqual(module_result["evidence"], [])

    def test_p3_3_live_repo_audit_baseline_includes_expected_level1_modules(self):
        result = runner.discover_profile_manifests(
            repo_root=ROOT,
            profile="audit-baseline",
            target_type="url",
            mode="dry-run",
        )
        self.assertEqual(result.verdict, "allow", result.errors)
        self.assertEqual(
            {module["module_id"] for module in result.modules},
            {
                "level1.api_docs_metadata",
                "level1.cors_metadata",
                "level1.dependency_manifest_metadata",
                "level1.directory_listing_metadata",
                "level1.policy_decision_metadata_audit",
                "level1.robots_securitytxt_metadata",
                "level1.security_headers_baseline",
            },
        )

    def test_p3_3_malformed_second_manifest_fails_closed_without_partial_selection(self):
        fixture_root, _policy = self.build_two_module_fixture_repo()
        bad_manifest = fixture_root / "modules" / "checks" / "level1" / "security_headers_baseline" / "module.json"
        bad_manifest.write_text("{", encoding="utf-8")

        result = runner.discover_profile_manifests(
            repo_root=fixture_root,
            profile="audit-baseline",
            target_type="url",
            mode="dry-run",
        )
        self.assertEqual(result.verdict, "deny")
        self.assertTrue(any("module manifest" in error or "valid JSON" in error for error in result.errors), result.errors)
        self.assertEqual(result.manifest_paths, [])
        self.assertEqual(result.modules, [])

    def test_p3_4_runner_ignores_broken_check_py_added_to_manifest_only_module(self):
        fixture_root, policy = self.build_two_module_fixture_repo()
        baseline = self.two_module_runner_preview_projection(fixture_root, policy)
        broken_check = fixture_root / "modules" / "checks" / "level1" / "policy_decision_metadata_audit" / "check.py"
        broken_check.write_text(
            "raise RuntimeError('module check should never be imported by the runner')\n",
            encoding="utf-8",
        )

        after = self.two_module_runner_preview_projection(fixture_root, policy)
        self.assertEqual(after, baseline)
        self.assertNotIn("check.py", json.dumps(after, sort_keys=True))

    def test_p3_4_runner_ignores_missing_check_py_from_evaluator_backed_module(self):
        fixture_root, policy = self.build_two_module_tree_fixture_repo()
        evaluator_check = fixture_root / "modules" / "checks" / "level1" / "security_headers_baseline" / "check.py"
        self.assertTrue(evaluator_check.exists())
        baseline = self.two_module_runner_preview_projection(fixture_root, policy)
        evaluator_check.unlink()

        after = self.two_module_runner_preview_projection(fixture_root, policy)
        self.assertEqual(after, baseline)
        self.assertNotIn("check.py", json.dumps(after, sort_keys=True))

    def test_cli_refuses_mixing_discovery_root_with_explicit_manifest(self):
        fixture_root = self.root / "fixture_repo"
        fixture_module = self.copy_committed_module_manifest(fixture_root, "policy_decision_metadata_audit")

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code, payload = runner.main([
                "--discover-root",
                str(fixture_root),
                "--manifest",
                str(fixture_module),
                "--policy-artifact",
                str(self.policy_path),
                "--run-id",
                RUN_ID,
                "--target-type",
                "url",
                "--target",
                TARGET,
                "--json",
            ])
        self.assertNotEqual(code, 0)
        self.assertEqual(payload["verdict"], "deny")
        self.assertTrue(any("cannot combine" in error for error in payload["errors"]), payload)
        self.assertIn('"verdict": "deny"', stdout.getvalue())

    def test_profile_discovery_fails_closed_on_missing_profile(self):
        self.profile_path.unlink()
        module_path = self.root / "modules" / "checks" / "level1" / "passive" / "module.json"
        module_path.parent.mkdir(parents=True)
        module_path.write_text(json.dumps(passive_manifest()), encoding="utf-8")

        result = runner.discover_profile_manifests(
            repo_root=self.root,
            profile="audit-baseline",
            target_type="url",
            mode="dry-run",
        )
        self.assertEqual(result.verdict, "deny")
        self.assertTrue(any("module profile" in error and "not found" in error for error in result.errors), result.errors)
        self.assertIn("PROFILE_NOT_FOUND", result.error_codes)
        payload = result.as_dict()
        self.assertIssueDetailShape(
            payload["error_details"][0],
            code="PROFILE_NOT_FOUND",
            severity="error",
            component="module_profile_loader",
            path=self.profile_path,
            profile_id="audit-baseline",
        )

    def test_profile_discovery_fails_closed_on_malformed_profile(self):
        self.profile_path.write_text("{", encoding="utf-8")
        module_path = self.root / "modules" / "checks" / "level1" / "passive" / "module.json"
        module_path.parent.mkdir(parents=True)
        module_path.write_text(json.dumps(passive_manifest()), encoding="utf-8")

        result = runner.discover_profile_manifests(
            repo_root=self.root,
            profile="audit-baseline",
            target_type="url",
            mode="dry-run",
        )
        self.assertEqual(result.verdict, "deny")
        self.assertTrue(any("module profile" in error and "valid JSON" in error for error in result.errors), result.errors)
        self.assertIn("PROFILE_MALFORMED_JSON", result.error_codes)

    def test_profile_discovery_fails_closed_on_schema_invalid_profile_code(self):
        data = json.loads(self.profile_path.read_text(encoding="utf-8"))
        data["execution_constraints"]["requires_network"] = True
        self.profile_path.write_text(json.dumps(data), encoding="utf-8")

        result = runner.discover_profile_manifests(
            repo_root=self.root,
            profile="audit-baseline",
            target_type="url",
            mode="dry-run",
        )
        self.assertEqual(result.verdict, "deny")
        self.assertIn("PROFILE_SCHEMA_INVALID", result.error_codes)

    def test_profile_discovery_fails_closed_on_profile_id_mismatch_code(self):
        data = json.loads(self.profile_path.read_text(encoding="utf-8"))
        data["profile_id"] = "other-profile"
        self.profile_path.write_text(json.dumps(data), encoding="utf-8")

        result = runner.discover_profile_manifests(
            repo_root=self.root,
            profile="audit-baseline",
            target_type="url",
            mode="dry-run",
        )
        self.assertEqual(result.verdict, "deny")
        self.assertIn("PROFILE_ID_MISMATCH", result.error_codes)

    def test_profile_discovery_skips_non_member_and_denies_empty_selection(self):
        module_path = self.root / "modules" / "checks" / "level1" / "other" / "module.json"
        module_path.parent.mkdir(parents=True)
        data = passive_manifest("other.profile.module")
        data["execution"]["default_profile"] = "other-profile"
        module_path.write_text(json.dumps(data), encoding="utf-8")

        result = runner.discover_profile_manifests(
            repo_root=self.root,
            profile="audit-baseline",
            target_type="url",
            mode="dry-run",
        )
        self.assertEqual(result.verdict, "deny")
        self.assertTrue(any("no module manifests selected" in error for error in result.errors), result.errors)
        self.assertIn("PROFILE_EMPTY_SELECTION", result.error_codes)
        self.assertIn("PROFILE_MEMBERSHIP_MISMATCH", result.warning_codes)
        payload = result.as_dict()
        self.assertIssueDetailShape(
            payload["warning_details"][0],
            code="PROFILE_MEMBERSHIP_MISMATCH",
            severity="warning",
            component="module_profile_selector",
            path=module_path,
            field="execution.default_profile",
            profile_id="audit-baseline",
            module_id="other.profile.module",
        )

    def test_cli_unknown_profile_fails_closed_without_hardcoded_fallback(self):
        module_path = self.root / "modules" / "checks" / "level1" / "passive" / "module.json"
        module_path.parent.mkdir(parents=True)
        module_path.write_text(json.dumps(passive_manifest()), encoding="utf-8")

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code, payload = runner.main([
                "--discover-root",
                str(self.root),
                "--policy-artifact",
                str(self.policy_path),
                "--run-id",
                RUN_ID,
                "--target-type",
                "url",
                "--target",
                TARGET,
                "--profile",
                "unknown-profile",
                "--json",
            ])
        self.assertNotEqual(code, 0)
        self.assertEqual(payload["verdict"], "deny")
        self.assertTrue(any("module profile" in error for error in payload["errors"]), payload)
        self.assertIn('"verdict": "deny"', stdout.getvalue())

    def test_persist_preview_bundle_writes_valid_repo_local_artifacts_after_allow(self):
        result = self.build_plan(
            include_module_io_preview=True,
            persist_preview_bundle_root=self.root,
        )
        self.assertEqual(result.verdict, "allow", result.errors)
        preview_dir = self.root / "runs" / RUN_ID / "preview"
        expected_files = [
            "run.json",
            "module_inputs.json",
            "module_results.json",
            "bundle_consistency.json",
            "preview_manifest.json",
        ]
        for filename in expected_files:
            self.assertTrue((preview_dir / filename).is_file(), filename)
        manifest = json.loads((preview_dir / "preview_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema_version"], "preview_manifest/1.0")
        self.assertEqual(manifest["run_id"], RUN_ID)
        self.assertEqual(manifest["producer"]["name"], "module_runner")
        self.assertRegex(manifest["producer"]["version"], r"^\d+\.\d+\.\d+")
        self.assertEqual(manifest["preview_mode"], {
            "persist_preview_bundle": True,
            "include_module_io_preview": True,
            "dry_run": True,
        })
        self.assertNotIn("target", manifest)
        self.assertNotIn("program", manifest)
        self.assertNotIn("modules", manifest)
        self.assertEqual(manifest["bundle_consistency"]["verdict"], "allow")
        self.assertEqual(manifest["bundle_consistency"]["status"], "ok")
        self.assertEqual(manifest["bundle_consistency"]["relative_path"], f"runs/{RUN_ID}/preview/bundle_consistency.json")
        self.assertEqual(result.preview_manifest["run_id"], RUN_ID)
        artifact_by_name = {item["name"]: item for item in manifest["artifacts"]}
        self.assertEqual(set(artifact_by_name), set(expected_files) - {"preview_manifest.json"})
        for filename, record in artifact_by_name.items():
            data = (preview_dir / filename).read_bytes()
            self.assertEqual(record["relative_path"], f"runs/{RUN_ID}/preview/{filename}")
            self.assertEqual(record["content_type"], "application/json")
            self.assertEqual(record["sha256"], runner.sha256(data).hexdigest(), filename)
            self.assertEqual(record["size_bytes"], len(data), filename)
        self.assertEqual(json.loads((preview_dir / "run.json").read_text(encoding="utf-8"))["run_id"], RUN_ID)
        self.assertEqual(json.loads((preview_dir / "bundle_consistency.json").read_text(encoding="utf-8"))["verdict"], "allow")

    def test_persist_preview_bundle_requires_module_io_preview_and_writes_nothing_on_deny(self):
        without_preview = self.build_plan(persist_preview_bundle_root=self.root)
        self.assertEqual(without_preview.verdict, "deny")
        self.assertTrue(any("include-module-io-preview" in error for error in without_preview.errors), without_preview.errors)
        self.assertFalse((self.root / "runs" / RUN_ID / "preview").exists())

        self.policy_path.write_text(json.dumps(policy_artifact(target="https://other.test/")), encoding="utf-8")
        denied = self.build_plan(
            include_module_io_preview=True,
            persist_preview_bundle_root=self.root,
        )
        self.assertEqual(denied.verdict, "deny")
        self.assertFalse((self.root / "runs" / RUN_ID / "preview").exists())

    def test_persist_preview_bundle_rejects_path_escape_and_existing_preview_dir(self):
        allowed = self.build_plan(include_module_io_preview=True)
        self.assertEqual(allowed.verdict, "allow", allowed.errors)
        bundle_validation = runner.validate_module_io_bundle.build_bundle_consistency_report(
            allowed.plan,
            allowed.module_input_previews,
            allowed.module_result_previews,
        )
        with self.assertRaises(ValueError):
            runner.persist_preview_bundle(
                repo_root=self.root,
                run_id="../escape",
                plan=allowed.plan,
                input_previews=allowed.module_input_previews,
                result_previews=allowed.module_result_previews,
                bundle_validation=bundle_validation,
            )
        self.assertFalse((self.root.parent / "escape").exists())

        preview_dir = self.root / "runs" / RUN_ID / "preview"
        preview_dir.mkdir(parents=True)
        with self.assertRaises(ValueError):
            runner.persist_preview_bundle(
                repo_root=self.root,
                run_id=RUN_ID,
                plan=allowed.plan,
                input_previews=allowed.module_input_previews,
                result_previews=allowed.module_result_previews,
                bundle_validation=bundle_validation,
            )

    def test_persist_preview_bundle_rejects_symlinked_runs_parent(self):
        allowed = self.build_plan(include_module_io_preview=True)
        self.assertEqual(allowed.verdict, "allow", allowed.errors)
        bundle_validation = runner.validate_module_io_bundle.build_bundle_consistency_report(
            allowed.plan,
            allowed.module_input_previews,
            allowed.module_result_previews,
        )
        symlink_repo = self.root / "symlink_repo"
        real_runs = symlink_repo / "real_runs"
        real_runs.mkdir(parents=True)
        runs_link = symlink_repo / "runs"
        try:
            runs_link.symlink_to(real_runs, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"symlink creation unavailable: {exc}")
        with self.assertRaises(ValueError):
            runner.persist_preview_bundle(
                repo_root=symlink_repo,
                run_id=RUN_ID,
                plan=allowed.plan,
                input_previews=allowed.module_input_previews,
                result_previews=allowed.module_result_previews,
                bundle_validation=bundle_validation,
            )
        self.assertFalse((real_runs / RUN_ID / "preview").exists())

    def test_persist_preview_bundle_filesystem_failure_returns_deny_without_traceback(self):
        original = runner.persist_preview_bundle
        def boom(**_kwargs):
            raise OSError("simulated write failure")
        runner.persist_preview_bundle = boom
        try:
            result = self.build_plan(
                include_module_io_preview=True,
                persist_preview_bundle_root=self.root,
            )
        finally:
            runner.persist_preview_bundle = original
        self.assertEqual(result.verdict, "deny")
        self.assertTrue(any("simulated write failure" in error for error in result.errors), result.errors)
        self.assertFalse((self.root / "runs" / RUN_ID / "preview").exists())

    def test_cli_persist_preview_bundle_requires_explicit_repo_root(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code, payload = runner.main([
                "--manifest",
                str(self.module_path),
                "--policy-artifact",
                str(self.policy_path),
                "--run-id",
                RUN_ID,
                "--target-type",
                "url",
                "--target",
                TARGET,
                "--include-module-io-preview",
                "--persist-preview-bundle",
                "--json",
            ])
        self.assertNotEqual(code, 0)
        self.assertEqual(payload["verdict"], "deny")
        self.assertTrue(any("explicit repo root" in error for error in payload["errors"]), payload)
        self.assertFalse((self.root / "runs" / RUN_ID / "preview").exists())

    def test_build_plan_fails_closed_on_profile_constraint_violation(self):
        data = passive_manifest("medium.risk.module")
        data["risk_level"] = "medium"
        self.module_path.write_text(json.dumps(data), encoding="utf-8")
        result = self.build_plan()
        self.assertEqual(result.verdict, "deny")
        self.assertTrue(any("risk_level" in error for error in result.errors), result.errors)
        self.assertIn("PROFILE_CONSTRAINT_RISK", result.error_codes)


if __name__ == "__main__":
    unittest.main()
