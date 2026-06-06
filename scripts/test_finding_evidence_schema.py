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
VALIDATOR_PATH = ROOT / "scripts" / "validate_finding_evidence.py"
SCHEMA_DIR = ROOT / "modules" / "_schema"

spec = importlib.util.spec_from_file_location("validate_finding_evidence", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = validator
spec.loader.exec_module(validator)


VALID_EVIDENCE = {
    "schema_version": "evidence/1.0",
    "id": "ev-http-headers-001",
    "finding_id": "finding-security-headers-001",
    "kind": "http_exchange",
    "captured_at_utc": "2026-05-16T00:00:00Z",
    "source": {
        "tool": "headers_audit",
        "module_id": "security_headers_baseline",
        "run_id": "20260516T000000Z_test"
    },
    "target": {
        "type": "url",
        "value": "https://authorized.test/"
    },
    "storage": {
        "path": "runs/20260516T000000Z_test/evidence/ev-http-headers-001.txt",
        "sha256": "a" * 64,
        "redacted": True
    },
    "summary": "Response headers captured for authorized dry-run fixture.",
    "metadata": {
        "content_type": "text/plain"
    }
}

VALID_FINDING = {
    "schema_version": "finding/1.0",
    "id": "finding-security-headers-001",
    "status": "candidate",
    "title": "Missing baseline security headers",
    "summary": "Authorized dry-run fixture observed missing defensive headers.",
    "target": {
        "type": "url",
        "value": "https://authorized.test/"
    },
    "source": {
        "module_id": "security_headers_baseline",
        "run_id": "20260516T000000Z_test",
        "policy_decision_sha256": "b" * 64
    },
    "severity_hint": "low",
    "confidence": "low",
    "triage": {
        "scanner_output_only": True,
        "manual_verification_required": True
    },
    "evidence": [
        {
            "id": "ev-http-headers-001",
            "kind": "http_exchange",
            "sha256": "a" * 64,
            "redacted": True
        }
    ],
    "references": [
        "https://owasp.org/www-project-secure-headers/"
    ],
    "classifications": {
        "cwe": ["CWE-693"],
        "owasp": ["A05 Security Misconfiguration"]
    },
    "remediation": "Review required headers and deploy only those appropriate for the application.",
    "verification_guidance": "Manually verify header behavior in an authorized testing window before reporting."
}


class FindingEvidenceSchemaTests(unittest.TestCase):
    def test_schema_files_are_valid_json_and_versioned(self):
        for filename, expected_title in (
            ("finding.schema.json", "Hacklab Candidate Finding"),
            ("evidence.schema.json", "Hacklab Evidence Artifact"),
        ):
            with self.subTest(filename=filename):
                data = json.loads((SCHEMA_DIR / filename).read_text(encoding="utf-8"))
                self.assertEqual(data["$schema"], "https://json-schema.org/draft/2020-12/schema")
                self.assertEqual(data["title"], expected_title)
                self.assertFalse(data.get("additionalProperties", True))

    @unittest.skipIf(jsonschema is None, "jsonschema is optional for schema-level regression tests")
    def test_evidence_schema_rejects_case_variant_sensitive_metadata(self):
        schema = json.loads((SCHEMA_DIR / "evidence.schema.json").read_text(encoding="utf-8"))
        bad_documents = []
        for key, value in (
            ("Authorization", "redacted"),
            ("HEADER", "redacted"),
            ("notes", "authorization: redacted"),
            ("sample", "bearer redacted"),
        ):
            doc = json.loads(json.dumps(VALID_EVIDENCE))
            doc["metadata"] = {key: value}
            bad_documents.append(doc)
        for doc in bad_documents:
            with self.subTest(metadata=doc["metadata"]):
                with self.assertRaises(jsonschema.ValidationError):
                    jsonschema.validate(doc, schema)

    def test_valid_finding_and_evidence_pass(self):
        evidence = validator.validate_data(VALID_EVIDENCE, document_type="evidence")
        finding = validator.validate_data(VALID_FINDING, document_type="finding")
        self.assertEqual(evidence.verdict, "allow", evidence.errors)
        self.assertEqual(finding.verdict, "allow", finding.errors)

    def test_finding_confirmed_status_is_rejected(self):
        data = dict(VALID_FINDING)
        data["status"] = "confirmed"
        result = validator.validate_data(data, document_type="finding")
        self.assertEqual(result.verdict, "deny")
        self.assertTrue(any("confirmed" in error for error in result.errors))

    def test_finding_requires_manual_verification_flag(self):
        data = json.loads(json.dumps(VALID_FINDING))
        data["triage"]["manual_verification_required"] = False
        result = validator.validate_data(data, document_type="finding")
        self.assertEqual(result.verdict, "deny")
        self.assertTrue(any("manual_verification_required" in error for error in result.errors))

    def test_evidence_requires_redaction_and_canonical_hash(self):
        data = json.loads(json.dumps(VALID_EVIDENCE))
        data["storage"]["redacted"] = False
        data["storage"]["sha256"] = "A" * 64
        result = validator.validate_data(data, document_type="evidence")
        self.assertEqual(result.verdict, "deny")
        self.assertTrue(any("redacted" in error for error in result.errors))
        self.assertTrue(any("sha256" in error for error in result.errors))

    def test_finding_requires_scanner_output_only_flag(self):
        data = json.loads(json.dumps(VALID_FINDING))
        data["triage"]["scanner_output_only"] = False
        result = validator.validate_data(data, document_type="finding")
        self.assertEqual(result.verdict, "deny")
        self.assertTrue(any("scanner_output_only" in error for error in result.errors))

    def test_evidence_storage_path_rejects_traversal_and_requires_run_evidence_path(self):
        bad_paths = [
            "runs/20260516T000000Z_test/../../config/scope.txt",
            "/runs/20260516T000000Z_test/evidence/ev.txt",
            "runs/20260516T000000Z_test/../evidence/ev.txt",
            "runs/20260516T000000Z_test/findings/ev.txt",
            "https://example.com/evidence.txt",
            "runs\\20260516T000000Z_test\\evidence\\ev.txt",
        ]
        for bad_path in bad_paths:
            with self.subTest(path=bad_path):
                data = json.loads(json.dumps(VALID_EVIDENCE))
                data["storage"]["path"] = bad_path
                result = validator.validate_data(data, document_type="evidence")
                self.assertEqual(result.verdict, "deny")
                self.assertTrue(any("storage.path" in error for error in result.errors), result.errors)

    def test_evidence_metadata_rejects_sensitive_raw_fields(self):
        sensitive_metadata = {
            "authorization": "Bearer SECRET_TOKEN",
            "cookie": "session=abc",
            "raw_response_body": "secret body",
            "headers": {"set-cookie": "session=abc"},
            "notes": "Authorization: Bearer SECRET_TOKEN",
            "sample": "Set-Cookie: session=abc",
            "description": "password=abc123",
        }
        for key, value in sensitive_metadata.items():
            with self.subTest(key=key):
                data = json.loads(json.dumps(VALID_EVIDENCE))
                data["metadata"] = {key: value}
                result = validator.validate_data(data, document_type="evidence")
                self.assertEqual(result.verdict, "deny")
                self.assertTrue(any("metadata" in error for error in result.errors), result.errors)

    def test_evidence_metadata_is_flat_repository_safe_scalars_only(self):
        bad_values = {
            "nested": {"content_type": "text/plain"},
            "list_value": ["text/plain"],
            "long_value": "x" * 501,
        }
        for key, value in bad_values.items():
            with self.subTest(key=key):
                data = json.loads(json.dumps(VALID_EVIDENCE))
                data["metadata"] = {key: value}
                result = validator.validate_data(data, document_type="evidence")
                self.assertEqual(result.verdict, "deny")
                self.assertTrue(any("metadata" in error for error in result.errors), result.errors)

    def test_cross_document_evidence_ids_must_match(self):
        finding = json.loads(json.dumps(VALID_FINDING))
        evidence = json.loads(json.dumps(VALID_EVIDENCE))
        evidence["id"] = "ev-other"
        result = validator.validate_bundle(finding, [evidence])
        self.assertEqual(result.verdict, "deny")
        self.assertTrue(any("evidence id" in error for error in result.errors))

    def test_cli_json_output_is_default_deny_on_invalid_bundle(self):
        finding = json.loads(json.dumps(VALID_FINDING))
        finding["status"] = "confirmed"
        with tempfile.TemporaryDirectory() as tmp:
            finding_path = Path(tmp) / "finding.json"
            evidence_path = Path(tmp) / "evidence.json"
            finding_path.write_text(json.dumps(finding), encoding="utf-8")
            evidence_path.write_text(json.dumps(VALID_EVIDENCE), encoding="utf-8")
            code, payload = validator.main([
                "--finding", str(finding_path),
                "--evidence", str(evidence_path),
                "--json",
            ])
        self.assertNotEqual(code, 0)
        self.assertEqual(payload["verdict"], "deny")
        self.assertTrue(payload["errors"])


if __name__ == "__main__":
    unittest.main()
