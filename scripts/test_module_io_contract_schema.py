import copy
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
VALIDATOR_PATH = ROOT / "scripts" / "validate_module_io_contract.py"
SCHEMA_DIR = ROOT / "modules" / "_schema"

spec = importlib.util.spec_from_file_location("validate_module_io_contract", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = validator
spec.loader.exec_module(validator)

RUN_ID = "20260516T020304Z_runner"
MODULE_ID = "level1.policy_decision_metadata_audit"
SHA = "a" * 64


def valid_module_input():
    return {
        "schema_version": "module_input/1.0",
        "run": {
            "run_id": RUN_ID,
            "mode": "dry-run",
            "dry_run": True,
            "runner": "hacklab-module-runner",
            "created_at_utc": "2026-05-16T02:03:04Z",
        },
        "program": {
            "slug": "demo-program",
            "scope_file_sha256": "b" * 64,
            "global_scope_file_sha256": "c" * 64,
        },
        "target": {"type": "url", "value": "https://example.test/"},
        "policy": {
            "decision": "allow",
            "decision_artifact_path": f"runs/{RUN_ID}/policy/decision.json",
            "decision_sha256": "d" * 64,
            "checked_at_utc": "2026-05-16T02:03:01Z",
        },
        "profile": {"profile_id": "audit-baseline", "profile_sha256": "e" * 64},
        "module": {
            "module_id": MODULE_ID,
            "module_version": "0.1.0",
            "manifest_sha256": SHA,
            "risk_level": "info",
            "target_types": ["url"],
            "technique_tags": ["passive.http_headers"],
        },
        "constraints": {
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
        },
        "output": {
            "module_output_dir": f"runs/{RUN_ID}/modules/{MODULE_ID}",
            "findings": [],
            "evidence": [],
        },
    }


def valid_module_result():
    return {
        "schema_version": "module_result/1.0",
        "run_id": RUN_ID,
        "module_id": MODULE_ID,
        "status": "not_executed",
        "dry_run": True,
        "target_touching": False,
        "summary": "Dry-run contract preview only; module code was not executed.",
        "findings": [],
        "evidence": [],
        "errors": [],
        "warnings": [],
    }


class ModuleIoContractTests(unittest.TestCase):
    def assertValidatorAllows(self, document, kind):
        if kind == "input":
            result = validator.validate_module_input(document)
        else:
            result = validator.validate_module_result(document)
        self.assertEqual(result.verdict, "allow", result.errors)
        return result

    def assertValidatorDenies(self, document, kind, expected):
        if kind == "input":
            result = validator.validate_module_input(document)
        else:
            result = validator.validate_module_result(document)
        self.assertEqual(result.verdict, "deny")
        self.assertTrue(any(expected in error for error in result.errors), result.errors)
        return result

    def assertSchemaAllows(self, schema_name, document):
        if jsonschema is None:
            return
        schema = json.loads((SCHEMA_DIR / schema_name).read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator(schema).validate(document)

    def assertSchemaDenies(self, schema_name, document):
        if jsonschema is None:
            return
        schema = json.loads((SCHEMA_DIR / schema_name).read_text(encoding="utf-8"))
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft202012Validator(schema).validate(document)

    def test_valid_module_input_and_result_are_allowed_by_schema_and_validator(self):
        module_input = valid_module_input()
        module_result = valid_module_result()
        self.assertSchemaAllows("module_input.schema.json", module_input)
        self.assertSchemaAllows("module_result.schema.json", module_result)
        self.assertValidatorAllows(module_input, "input")
        self.assertValidatorAllows(module_result, "result")

    def test_module_input_denies_non_dry_run_modes_and_dry_run_false(self):
        data = valid_module_input()
        data["run"]["mode"] = "live"
        self.assertSchemaDenies("module_input.schema.json", data)
        self.assertValidatorDenies(data, "input", "run.mode")

        data = valid_module_input()
        data["run"]["dry_run"] = False
        self.assertSchemaDenies("module_input.schema.json", data)
        self.assertValidatorDenies(data, "input", "run.dry_run")

    def test_module_input_denies_network_target_touching_and_intrusive_constraints(self):
        cases = [
            ("requires_network", True),
            ("network_access", "target-http"),
            ("target_touching", True),
            ("destructive", True),
            ("intrusive", True),
            ("emits_findings", True),
            ("emits_evidence", True),
            ("stores_raw_secrets", True),
            ("writes_to_loot", True),
            ("allows_destructive_actions", True),
            ("allows_oast_callbacks", True),
        ]
        for key, value in cases:
            with self.subTest(key=key):
                data = valid_module_input()
                data["constraints"][key] = value
                self.assertSchemaDenies("module_input.schema.json", data)
                self.assertValidatorDenies(data, "input", f"constraints.{key}")

    def test_module_input_denies_non_empty_outputs_and_path_traversal(self):
        data = valid_module_input()
        data["output"]["findings"] = [{"id": "finding-1"}]
        self.assertSchemaDenies("module_input.schema.json", data)
        self.assertValidatorDenies(data, "input", "output.findings")

        data = valid_module_input()
        data["output"]["module_output_dir"] = f"runs/{RUN_ID}/modules/../loot"
        self.assertSchemaDenies("module_input.schema.json", data)
        self.assertValidatorDenies(data, "input", "traversal")

        data = valid_module_input()
        data["policy"]["decision_artifact_path"] = f"runs/{RUN_ID}/../policy/decision.json"
        self.assertSchemaDenies("module_input.schema.json", data)
        self.assertValidatorDenies(data, "input", "traversal")

    def test_module_input_denies_non_canonical_dot_and_duplicate_slash_paths(self):
        cases = [
            ("policy", "decision_artifact_path", f"runs/{RUN_ID}/policy/./decision.json"),
            ("policy", "decision_artifact_path", f"runs/{RUN_ID}/policy//decision.json"),
            ("output", "module_output_dir", f"runs/{RUN_ID}/modules/./{MODULE_ID}"),
            ("output", "module_output_dir", f"runs/{RUN_ID}/modules//{MODULE_ID}"),
        ]
        for section, key, value in cases:
            with self.subTest(value=value):
                data = valid_module_input()
                data[section][key] = value
                self.assertSchemaDenies("module_input.schema.json", data)
                self.assertValidatorDenies(data, "input", "canonical POSIX path")

    def test_module_input_denies_unknown_nested_keys_and_bad_hash_timestamp(self):
        data = valid_module_input()
        data["constraints"]["future_exec"] = True
        self.assertSchemaDenies("module_input.schema.json", data)
        self.assertValidatorDenies(data, "input", "not allowed")

        data = valid_module_input()
        data["policy"]["decision_sha256"] = "ABC"
        self.assertSchemaDenies("module_input.schema.json", data)
        self.assertValidatorDenies(data, "input", "sha256")

        data = valid_module_input()
        data["run"]["created_at_utc"] = "2026-05-16 02:03:04"
        self.assertSchemaDenies("module_input.schema.json", data)
        self.assertValidatorDenies(data, "input", "UTC timestamp")

    def test_module_result_denies_completed_execution_and_non_empty_artifacts(self):
        data = valid_module_result()
        data["status"] = "completed"
        self.assertSchemaDenies("module_result.schema.json", data)
        self.assertValidatorDenies(data, "result", "status")

        data = valid_module_result()
        data["findings"] = [{"id": "finding-1"}]
        self.assertSchemaDenies("module_result.schema.json", data)
        self.assertValidatorDenies(data, "result", "findings")

        data = valid_module_result()
        data["evidence"] = [{"id": "ev-1"}]
        self.assertSchemaDenies("module_result.schema.json", data)
        self.assertValidatorDenies(data, "result", "evidence")

    def test_module_result_denies_execution_claims_and_sensitive_terms(self):
        data = valid_module_result()
        data["summary"] = "Module executed and captured HTTP response."
        # Schema does not encode every unsafe semantic term; strict validator must.
        self.assertValidatorDenies(data, "result", "must not imply module execution")

        data = valid_module_result()
        data["target_touching"] = True
        self.assertSchemaDenies("module_result.schema.json", data)
        self.assertValidatorDenies(data, "result", "target_touching")

    def test_cli_validates_input_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "module_input.json"
            path.write_text(json.dumps(valid_module_input()), encoding="utf-8")
            code, payload = validator.main(["--input", str(path), "--json"])
        self.assertEqual(code, 0)
        self.assertEqual(payload["verdict"], "allow")
        self.assertEqual(payload["schema_version"], "module_io_contract_validation/1.0")


if __name__ == "__main__":
    unittest.main()
