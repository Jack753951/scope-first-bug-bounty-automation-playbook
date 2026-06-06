import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

try:
    import jsonschema
except Exception:  # pragma: no cover - optional local dependency
    jsonschema = None


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_run_manifest.py"
FINDING_VALIDATOR_PATH = ROOT / "scripts" / "validate_finding_evidence.py"
SCHEMA_DIR = ROOT / "modules" / "_schema"

spec = importlib.util.spec_from_file_location("validate_run_manifest", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = validator
spec.loader.exec_module(validator)

finding_spec = importlib.util.spec_from_file_location("validate_finding_evidence", FINDING_VALIDATOR_PATH)
finding_validator = importlib.util.module_from_spec(finding_spec)
assert finding_spec.loader is not None
sys.modules[finding_spec.name] = finding_validator
finding_spec.loader.exec_module(finding_validator)

RUN_ID = "20260516T010203Z_test"
POLICY_SHA = "b" * 64
EVIDENCE_SHA = "a" * 64
FINDING_SHA = "c" * 64

VALID_RUN = {
    "schema_version": "run/1.0",
    "run_id": RUN_ID,
    "created_at_utc": "2026-05-16T01:02:03Z",
    "completed_at_utc": "2026-05-16T01:03:03Z",
    "status": "completed",
    "program": {
        "slug": "demo-program",
        "scope_file_sha256": "d" * 64,
        "global_scope_file_sha256": "e" * 64,
    },
    "target": {
        "type": "url",
        "value": "https://authorized.test/",
    },
    "policy": {
        "mode": "dry-run",
        "decision": "allow",
        "decision_artifact_path": f"runs/{RUN_ID}/policy/decision.json",
        "decision_sha256": POLICY_SHA,
        "checked_at_utc": "2026-05-16T01:02:04Z",
    },
    "execution": {
        "runner": "hacklab-runner",
        "profile": "audit-baseline",
        "profile_id": "audit-baseline",
        "profile_sha256": "f" * 64,
        "dry_run": True,
        "target_touching": False,
    },
    "modules": [
        {
            "module_id": "security_headers_baseline",
            "manifest_sha256": "f" * 64,
            "status": "completed",
        }
    ],
    "artifacts": {
        "findings": [
            {
                "id": "finding-security-headers-001",
                "path": f"runs/{RUN_ID}/findings/finding-security-headers-001.json",
                "sha256": FINDING_SHA,
            }
        ],
        "evidence": [
            {
                "id": "ev-http-headers-001",
                "path": f"runs/{RUN_ID}/evidence/ev-http-headers-001.json",
                "sha256": EVIDENCE_SHA,
                "redacted": True,
            }
        ],
    },
    "review": {
        "manual_verification_required": True,
        "scanner_output_only": True,
        "agent_review_status": "not_started",
    },
}

VALID_EVIDENCE = {
    "schema_version": "evidence/1.0",
    "id": "ev-http-headers-001",
    "finding_id": "finding-security-headers-001",
    "kind": "http_exchange",
    "captured_at_utc": "2026-05-16T01:02:30Z",
    "source": {
        "tool": "headers_audit",
        "module_id": "security_headers_baseline",
        "run_id": RUN_ID,
    },
    "target": {
        "type": "url",
        "value": "https://authorized.test/",
    },
    "storage": {
        "path": f"runs/{RUN_ID}/evidence/ev-http-headers-001.txt",
        "sha256": EVIDENCE_SHA,
        "redacted": True,
    },
    "summary": "Response headers captured for authorized dry-run fixture.",
    "metadata": {"content_type": "text/plain"},
}

VALID_FINDING = {
    "schema_version": "finding/1.0",
    "id": "finding-security-headers-001",
    "status": "candidate",
    "title": "Missing baseline security headers",
    "summary": "Authorized dry-run fixture observed missing defensive headers.",
    "target": {
        "type": "url",
        "value": "https://authorized.test/",
    },
    "source": {
        "module_id": "security_headers_baseline",
        "run_id": RUN_ID,
        "policy_decision_sha256": POLICY_SHA,
    },
    "severity_hint": "low",
    "confidence": "low",
    "triage": {
        "scanner_output_only": True,
        "manual_verification_required": True,
    },
    "evidence": [
        {
            "id": "ev-http-headers-001",
            "kind": "http_exchange",
            "sha256": EVIDENCE_SHA,
            "redacted": True,
        }
    ],
    "references": ["https://owasp.org/www-project-secure-headers/"],
    "classifications": {"cwe": ["CWE-693"]},
    "remediation": "Review required headers and deploy only those appropriate for the application.",
    "verification_guidance": "Manually verify header behavior in an authorized testing window before reporting.",
}


class RunManifestSchemaTests(unittest.TestCase):
    def test_run_schema_file_is_valid_json_and_versioned(self):
        data = json.loads((SCHEMA_DIR / "run.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(data["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(data["title"], "Hacklab Run Manifest")
        self.assertFalse(data.get("additionalProperties", True))

    @unittest.skipIf(jsonschema is None, "jsonschema is optional for schema-level regression tests")
    def test_run_schema_rejects_traversal_paths_and_live_touching_dry_run(self):
        schema = json.loads((SCHEMA_DIR / "run.schema.json").read_text(encoding="utf-8"))
        bad_path_doc = json.loads(json.dumps(VALID_RUN))
        bad_path_doc["artifacts"]["findings"][0]["path"] = f"runs/{RUN_ID}/findings/../../config/scope.txt"
        live_dry_run_doc = json.loads(json.dumps(VALID_RUN))
        live_dry_run_doc["execution"]["target_touching"] = True
        for doc in (bad_path_doc, live_dry_run_doc):
            with self.subTest(doc=doc):
                with self.assertRaises(jsonschema.ValidationError):
                    jsonschema.validate(doc, schema)

    def test_valid_run_manifest_passes(self):
        result = validator.validate_run(VALID_RUN)
        self.assertEqual(result.verdict, "allow", result.errors)

    def test_run_manifest_requires_policy_allow_and_triage_only_review(self):
        for field, value in (
            ("policy.decision", "deny"),
            ("review.manual_verification_required", False),
            ("review.scanner_output_only", False),
        ):
            data = json.loads(json.dumps(VALID_RUN))
            section, key = field.split(".")
            data[section][key] = value
            with self.subTest(field=field):
                result = validator.validate_run(data)
                self.assertEqual(result.verdict, "deny")
                self.assertTrue(any(key in error for error in result.errors), result.errors)

    def test_run_manifest_paths_must_stay_under_matching_run_directory(self):
        bad_paths = [
            f"runs/{RUN_ID}/findings/../../config/scope.txt",
            f"/runs/{RUN_ID}/findings/finding.json",
            f"runs\\{RUN_ID}\\findings\\finding.json",
            f"https://example.com/finding.json",
            "runs/other-run/findings/finding.json",
            f"runs/{RUN_ID}/loot/finding.json",
        ]
        for bad_path in bad_paths:
            data = json.loads(json.dumps(VALID_RUN))
            data["artifacts"]["findings"][0]["path"] = bad_path
            with self.subTest(path=bad_path):
                result = validator.validate_run(data)
                self.assertEqual(result.verdict, "deny")
                self.assertTrue(any("path" in error for error in result.errors), result.errors)

    def test_run_manifest_accepts_recon_policy_evidence_decision_artifact_path(self):
        data = json.loads(json.dumps(VALID_RUN))
        data["policy"]["decision_artifact_path"] = (
            "scans/authorized.test_20260520_091000/evidence/policy/"
            "policy_boundary_20260520_091000.json"
        )
        result = validator.validate_run(data)
        self.assertEqual(result.verdict, "allow", result.errors)

    def test_run_manifest_rejects_malformed_recon_policy_evidence_path(self):
        bad_paths = [
            "scans/authorized.test_20260520_091000/evidence/other/policy_boundary_20260520_091000.json",
            "scans/authorized.test_20260520_091000/evidence/policy/decision.json",
            "scans/../evidence/policy/policy_boundary_20260520_091000.json",
        ]
        for bad_path in bad_paths:
            data = json.loads(json.dumps(VALID_RUN))
            data["policy"]["decision_artifact_path"] = bad_path
            with self.subTest(path=bad_path):
                result = validator.validate_run(data)
                self.assertEqual(result.verdict, "deny")
                self.assertTrue(any("policy.decision_artifact_path" in error for error in result.errors), result.errors)

    def test_run_bundle_cross_checks_finding_evidence_policy_and_target(self):
        result = validator.validate_run_bundle(VALID_RUN, [VALID_FINDING], [VALID_EVIDENCE])
        self.assertEqual(result.verdict, "allow", result.errors)

        bad_finding = json.loads(json.dumps(VALID_FINDING))
        bad_finding["source"]["policy_decision_sha256"] = "9" * 64
        result = validator.validate_run_bundle(VALID_RUN, [bad_finding], [VALID_EVIDENCE])
        self.assertEqual(result.verdict, "deny")
        self.assertTrue(any("policy_decision_sha256" in error for error in result.errors), result.errors)

    def test_run_bundle_rejects_artifacts_not_declared_in_manifest(self):
        data = json.loads(json.dumps(VALID_RUN))
        data["artifacts"]["evidence"] = []
        result = validator.validate_run_bundle(data, [VALID_FINDING], [VALID_EVIDENCE])
        self.assertEqual(result.verdict, "deny")
        self.assertTrue(any("not declared" in error for error in result.errors), result.errors)

    def test_run_bundle_cross_checks_every_finding_not_only_first(self):
        second_finding = json.loads(json.dumps(VALID_FINDING))
        second_finding["id"] = "finding-second-001"
        second_finding["evidence"] = [
            {
                "id": "ev-missing-002",
                "kind": "http_exchange",
                "sha256": "9" * 64,
                "redacted": True,
            }
        ]
        data = json.loads(json.dumps(VALID_RUN))
        data["artifacts"]["findings"].append(
            {
                "id": "finding-second-001",
                "path": f"runs/{RUN_ID}/findings/finding-second-001.json",
                "sha256": "8" * 64,
            }
        )
        result = validator.validate_run_bundle(data, [VALID_FINDING, second_finding], [VALID_EVIDENCE])
        self.assertEqual(result.verdict, "deny")
        self.assertTrue(any("ev-missing-002" in error for error in result.errors), result.errors)

    def test_run_manifest_rejects_duplicate_module_and_artifact_ids(self):
        duplicate_module = json.loads(json.dumps(VALID_RUN))
        duplicate_module["modules"].append(json.loads(json.dumps(duplicate_module["modules"][0])))
        duplicate_finding = json.loads(json.dumps(VALID_RUN))
        duplicate_finding["artifacts"]["findings"].append(
            {
                "id": "finding-security-headers-001",
                "path": f"runs/{RUN_ID}/findings/other.json",
                "sha256": "8" * 64,
            }
        )
        duplicate_evidence = json.loads(json.dumps(VALID_RUN))
        duplicate_evidence["artifacts"]["evidence"].append(
            {
                "id": "ev-http-headers-001",
                "path": f"runs/{RUN_ID}/evidence/other.json",
                "sha256": "7" * 64,
                "redacted": True,
            }
        )
        for data in (duplicate_module, duplicate_finding, duplicate_evidence):
            with self.subTest(data=data):
                result = validator.validate_run(data)
                self.assertEqual(result.verdict, "deny")
                self.assertTrue(any("duplicate" in error for error in result.errors), result.errors)

    def test_cli_json_output_is_default_deny_on_invalid_run(self):
        data = json.loads(json.dumps(VALID_RUN))
        data["policy"]["decision"] = "deny"
        with tempfile.TemporaryDirectory() as tmp:
            run_path = Path(tmp) / "run.json"
            run_path.write_text(json.dumps(data), encoding="utf-8")
            code, payload = validator.main(["--run", str(run_path), "--json"])
        self.assertNotEqual(code, 0)
        self.assertEqual(payload["verdict"], "deny")
        self.assertTrue(payload["errors"])


if __name__ == "__main__":
    unittest.main()
