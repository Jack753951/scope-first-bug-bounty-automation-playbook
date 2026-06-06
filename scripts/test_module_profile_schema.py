import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE_VALIDATOR_PATH = ROOT / "scripts" / "validate_module_profile.py"

spec = importlib.util.spec_from_file_location("validate_module_profile", PROFILE_VALIDATOR_PATH)
validate_module_profile = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = validate_module_profile
spec.loader.exec_module(validate_module_profile)


def audit_profile():
    return json.loads((ROOT / "modules" / "profiles" / "audit-baseline.json").read_text(encoding="utf-8"))


class ModuleProfileSchemaTests(unittest.TestCase):
    def test_committed_audit_baseline_profile_is_valid(self):
        result = validate_module_profile.validate_module_profile(audit_profile())
        self.assertEqual(result.verdict, "allow", result.errors)

    def test_unknown_schema_version_fails_closed(self):
        data = audit_profile()
        data["schema_version"] = "module_profile/9.9"
        result = validate_module_profile.validate_module_profile(data)
        self.assertEqual(result.verdict, "deny")
        self.assertTrue(any("schema_version" in error for error in result.errors), result.errors)

    def test_empty_allowlist_fails_closed(self):
        data = audit_profile()
        data["technique_tag_allowlist"] = []
        result = validate_module_profile.validate_module_profile(data)
        self.assertEqual(result.verdict, "deny")
        self.assertTrue(any("technique_tag_allowlist" in error for error in result.errors), result.errors)

    def test_unsafe_execution_constraint_fails_closed(self):
        data = audit_profile()
        data["execution_constraints"]["requires_network"] = True
        result = validate_module_profile.validate_module_profile(data)
        self.assertEqual(result.verdict, "deny")
        self.assertTrue(any("requires_network" in error for error in result.errors), result.errors)
        self.assertIn("PROFILE_SCHEMA_INVALID", result.error_codes)

    def test_unknown_profile_rule_value_fails_closed(self):
        data = audit_profile()
        data["target_type_allowlist"].append("container")
        result = validate_module_profile.validate_module_profile(data)
        self.assertEqual(result.verdict, "deny")
        self.assertTrue(any("target_type_allowlist" in error for error in result.errors), result.errors)

    def test_cli_reports_malformed_json_as_deny(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text("{", encoding="utf-8")
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                code = validate_module_profile.main([str(path), "--json"])
        self.assertNotEqual(code, 0)
        payload = json.loads(stdout.getvalue())
        self.assertIn("PROFILE_MALFORMED_JSON", payload["error_codes"])


if __name__ == "__main__":
    unittest.main()
