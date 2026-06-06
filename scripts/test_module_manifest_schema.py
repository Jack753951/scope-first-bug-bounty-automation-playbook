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
VALIDATOR_PATH = ROOT / "scripts" / "validate_module_manifest.py"
SCHEMA_DIR = ROOT / "modules" / "_schema"

spec = importlib.util.spec_from_file_location("validate_module_manifest", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = validator
spec.loader.exec_module(validator)


VALID_MODULE = {
    "schema_version": "module_manifest/1.0",
    "module_id": "security_headers_baseline",
    "version": "0.1.0",
    "name": "Security Headers Baseline",
    "description": "Offline-safe manifest for a policy-gated HTTP header observation module.",
    "risk_level": "low",
    "target_types": ["url"],
    "technique_tags": ["active.http_get", "passive.http_headers"],
    "execution": {
        "supports_dry_run": True,
        "requires_network": True,
        "network_access": "target-http",
        "target_touching": True,
        "destructive": False,
        "intrusive": False,
        "default_profile": "audit-baseline",
    },
    "external_tools": [
        {
            "name": "python-stdlib",
            "required": True,
            "version_constraint": ">=3.11",
        }
    ],
    "output_contracts": {
        "run_schema": "run/1.0",
        "finding_schema": "finding/1.0",
        "evidence_schema": "evidence/1.0",
        "emits_findings": True,
        "emits_evidence": True,
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
    "references": [
        "https://github.com/projectdiscovery/nuclei-templates",
        "https://github.com/zaproxy/zap-extensions",
        "https://github.com/usnistgov/OSCAL",
    ],
}


class ModuleManifestSchemaTests(unittest.TestCase):
    def test_committed_level1_audit_module_fixture_validates(self):
        fixture_path = ROOT / "modules" / "checks" / "level1" / "policy_decision_metadata_audit" / "module.json"
        data = json.loads(fixture_path.read_text(encoding="utf-8"))
        result = validator.validate_module_manifest(data)
        self.assertEqual(result.verdict, "allow", result.errors)
        self.assertEqual(data["module_id"], "level1.policy_decision_metadata_audit")
        self.assertEqual(data["risk_level"], "info")
        self.assertEqual(data["technique_tags"], ["passive.content_metadata"])
        self.assertEqual(data["execution"]["supports_dry_run"], True)
        self.assertEqual(data["execution"]["requires_network"], False)
        self.assertEqual(data["execution"]["network_access"], "none")
        self.assertEqual(data["execution"]["target_touching"], False)
        self.assertEqual(data["execution"]["destructive"], False)
        self.assertEqual(data["execution"]["intrusive"], False)
        self.assertEqual(data["output_contracts"]["emits_findings"], False)
        self.assertEqual(data["output_contracts"]["emits_evidence"], False)
        self.assertEqual(data["safety_gates"]["stores_raw_secrets"], False)
        self.assertEqual(data["safety_gates"]["writes_to_loot"], False)
        self.assertEqual(data["safety_gates"]["allows_destructive_actions"], False)
        self.assertEqual(data["safety_gates"]["allows_oast_callbacks"], False)

    def test_module_manifest_schema_file_is_valid_json_and_versioned(self):
        data = json.loads((SCHEMA_DIR / "module_manifest.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(data["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(data["title"], "Hacklab Module Manifest")
        self.assertFalse(data.get("additionalProperties", True))

    @unittest.skipIf(jsonschema is None, "jsonschema is optional for schema-level regression tests")
    def test_module_manifest_schema_rejects_missing_dry_run_and_unsafe_gates(self):
        schema = json.loads((SCHEMA_DIR / "module_manifest.schema.json").read_text(encoding="utf-8"))
        missing_dry_run = json.loads(json.dumps(VALID_MODULE))
        del missing_dry_run["execution"]["supports_dry_run"]
        unsafe_gate = json.loads(json.dumps(VALID_MODULE))
        unsafe_gate["safety_gates"]["require_policy_decision"] = False
        for doc in (missing_dry_run, unsafe_gate):
            with self.subTest(doc=doc):
                with self.assertRaises(jsonschema.ValidationError):
                    jsonschema.validate(doc, schema)

    def test_valid_module_manifest_passes(self):
        result = validator.validate_module_manifest(VALID_MODULE)
        self.assertEqual(result.verdict, "allow", result.errors)

    def test_unknown_technique_tags_default_deny(self):
        data = json.loads(json.dumps(VALID_MODULE))
        data["technique_tags"].append("exploit.unknown_magic")
        result = validator.validate_module_manifest(data)
        self.assertEqual(result.verdict, "deny")
        self.assertTrue(any("technique_tags" in error for error in result.errors), result.errors)

    def test_missing_dry_run_support_default_deny(self):
        for mutation in ("missing", "false"):
            data = json.loads(json.dumps(VALID_MODULE))
            if mutation == "missing":
                del data["execution"]["supports_dry_run"]
            else:
                data["execution"]["supports_dry_run"] = False
            with self.subTest(mutation=mutation):
                result = validator.validate_module_manifest(data)
                self.assertEqual(result.verdict, "deny")
                self.assertTrue(any("supports_dry_run" in error for error in result.errors), result.errors)

    def test_ambiguous_network_posture_default_deny(self):
        bad_values = [None, "", "internet", "callback"]
        for value in bad_values:
            data = json.loads(json.dumps(VALID_MODULE))
            if value is None:
                del data["execution"]["network_access"]
            else:
                data["execution"]["network_access"] = value
            with self.subTest(value=value):
                result = validator.validate_module_manifest(data)
                self.assertEqual(result.verdict, "deny")
                self.assertTrue(any("network_access" in error for error in result.errors), result.errors)

    def test_known_techniques_must_match_declared_network_posture(self):
        cases = [
            (["active.http_get"], "dns", False),
            (["active.http_get"], "target-http", False),
            (["active.web_content_check"], "target-tcp", True),
            (["active.tcp_connect"], "target-http", True),
            (["active.dns_lookup"], "target-http", True),
            (["passive.http_headers"], "target-http", True),
        ]
        for tags, network_access, target_touching in cases:
            data = json.loads(json.dumps(VALID_MODULE))
            data["technique_tags"] = tags
            data["execution"]["network_access"] = network_access
            data["execution"]["target_touching"] = target_touching
            with self.subTest(tags=tags, network_access=network_access, target_touching=target_touching):
                result = validator.validate_module_manifest(data)
                self.assertEqual(result.verdict, "deny")
                self.assertTrue(any("network posture" in error for error in result.errors), result.errors)

    @unittest.skipIf(jsonschema is None, "jsonschema is optional for schema-level regression tests")
    def test_schema_rejects_known_technique_network_mismatch(self):
        schema = json.loads((SCHEMA_DIR / "module_manifest.schema.json").read_text(encoding="utf-8"))
        data = json.loads(json.dumps(VALID_MODULE))
        data["technique_tags"] = ["active.http_get"]
        data["execution"]["network_access"] = "dns"
        data["execution"]["target_touching"] = False
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(data, schema)

        passive_only = json.loads(json.dumps(VALID_MODULE))
        passive_only["technique_tags"] = ["passive.http_headers"]
        passive_only["execution"]["network_access"] = "dns"
        passive_only["execution"]["target_touching"] = True
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(passive_only, schema)

    def test_unsupported_output_schema_default_deny(self):
        for field in ("run_schema", "finding_schema", "evidence_schema"):
            data = json.loads(json.dumps(VALID_MODULE))
            data["output_contracts"][field] = "sarif/2.1.0"
            with self.subTest(field=field):
                result = validator.validate_module_manifest(data)
                self.assertEqual(result.verdict, "deny")
                self.assertTrue(any(field in error for error in result.errors), result.errors)

    def test_safety_gates_must_keep_triage_and_policy_boundaries(self):
        unsafe = {
            "require_policy_decision": False,
            "require_scope_match": False,
            "manual_verification_required": False,
            "scanner_output_only": False,
            "store_redacted_evidence_only": False,
            "stores_raw_secrets": True,
            "writes_to_loot": True,
            "allows_destructive_actions": True,
            "allows_oast_callbacks": True,
        }
        for field, value in unsafe.items():
            data = json.loads(json.dumps(VALID_MODULE))
            data["safety_gates"][field] = value
            with self.subTest(field=field):
                result = validator.validate_module_manifest(data)
                self.assertEqual(result.verdict, "deny")
                self.assertTrue(any(field in error for error in result.errors), result.errors)

    def test_duplicate_lists_are_rejected(self):
        for field in ("target_types", "technique_tags"):
            data = json.loads(json.dumps(VALID_MODULE))
            data[field].append(data[field][0])
            with self.subTest(field=field):
                result = validator.validate_module_manifest(data)
                self.assertEqual(result.verdict, "deny")
                self.assertTrue(any("duplicate" in error for error in result.errors), result.errors)

    def test_cli_json_output_is_default_deny_on_invalid_manifest(self):
        data = json.loads(json.dumps(VALID_MODULE))
        data["execution"]["supports_dry_run"] = False
        with tempfile.TemporaryDirectory() as tmp:
            manifest_path = Path(tmp) / "module.json"
            manifest_path.write_text(json.dumps(data), encoding="utf-8")
            code, payload = validator.main(["--manifest", str(manifest_path), "--json"])
        self.assertNotEqual(code, 0)
        self.assertEqual(payload["verdict"], "deny")
        self.assertTrue(payload["errors"])


if __name__ == "__main__":
    unittest.main()
