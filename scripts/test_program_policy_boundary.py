import contextlib
import hashlib
import io
import json
import os
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import program_policy_boundary


def base_program():
    return {
        "schema_version": "1.0",
        "program": {
            "slug": "boundary-test",
            "name": "Boundary Test",
            "platform": "lab",
            "url": "file:///boundary-test",
            "authorization_reference": "Local unit-test fixture only.",
            "policy_version": "2026-05-15",
            "policy_acknowledged_at": "2026-05-15T00:00:00Z",
        },
        "scope": {
            "in_scope": [{"type": "domain", "value": "example.test"}],
            "out_of_scope": [],
            "idn_handling": "punycode_only",
        },
        "techniques": {
            "allowed": ["http_probe"],
            "forbidden": ["dos", "credential_brute_force"],
            "automation_permitted": True,
        },
        "rate_limits": {"max_concurrency": 1},
        "testing_windows": {"always": True},
        "expiration": {
            "valid_from": "2026-01-01T00:00:00Z",
            "valid_until": "2027-01-01T00:00:00Z",
        },
    }


class ProgramPolicyBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.program_path = self.root / "program.json"
        self.global_scope_path = self.root / "scope.txt"
        self.artifact_dir = self.root / "artifacts"
        self.program_path.write_text(json.dumps(base_program()), encoding="utf-8")
        self.global_scope_path.write_text("example.test\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def argv(
        self,
        *,
        target="https://example.test/",
        technique="http_probe",
        mode="dry-run",
        timeout_seconds="5",
    ):
        return [
            "--program",
            str(self.program_path),
            "--global-scope",
            str(self.global_scope_path),
            "--target",
            target,
            "--technique",
            technique,
            "--mode",
            mode,
            "--artifact-dir",
            str(self.artifact_dir),
            "--timeout-seconds",
            timeout_seconds,
            "--ignore-time",
        ]

    def run_boundary(self, argv=None, helper_path=program_policy_boundary.DEFAULT_HELPER):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code = program_policy_boundary.main(argv or self.argv(), helper_path=helper_path)
        lines = stdout.getvalue().splitlines()
        artifacts = sorted(self.artifact_dir.glob("*.json"))
        return code, stdout.getvalue(), lines, artifacts

    def write_fake_helper(self, source):
        helper = self.root / f"fake_helper_{len(list(self.root.glob('fake_helper_*.py')))}.py"
        helper.write_text(textwrap.dedent(source), encoding="utf-8")
        return helper

    def read_artifact(self, artifacts):
        self.assertEqual(len(artifacts), 1)
        return json.loads(artifacts[0].read_text(encoding="utf-8"))

    def valid_fake_decision_source(self, verdict="allow", returncode=0):
        audit_event = "PROGRAM_POLICY_ALLOW" if verdict == "allow" else "PROGRAM_POLICY_DENY"
        deny_codes = [] if verdict == "allow" else ["NOT_IN_GLOBAL_SCOPE"]
        return f"""
            import json
            import sys
            payload = {{
                "schema_version": "policy_decision/1.0",
                "verdict": {verdict!r},
                "program_slug": "boundary-test",
                "target": "https://example.test/",
                "normalized_target": "example.test",
                "target_type": "url",
                "technique": "http_probe",
                "mode": "dry-run",
                "reasons": ["fixture"],
                "errors": [],
                "warnings": [],
                "deny_reason_codes": {deny_codes!r},
                "audit_event": {audit_event!r},
                "program_file_sha256": "a" * 64,
                "global_scope_sha256": "b" * 64,
                "decided_at_utc": "2026-05-15T00:00:00Z",
            }}
            print(json.dumps(payload))
            raise SystemExit({returncode})
        """

    def test_allow_decision_writes_artifact_and_exits_zero(self):
        code, stdout, lines, artifacts = self.run_boundary()
        self.assertEqual(code, 0, stdout)
        self.assertIn("POLICY_BOUNDARY_STATUS=allow", lines)
        self.assertIn("POLICY_BOUNDARY_AUDIT_EVENT=PROGRAM_POLICY_ALLOW", lines)
        artifact = self.read_artifact(artifacts)
        self.assertEqual(artifact["boundary"]["status"], "allow")
        self.assertEqual(artifact["decision"]["verdict"], "allow")
        self.assertEqual(artifact["helper"]["returncode"], 0)

    def test_deny_decision_writes_artifact_and_exits_one(self):
        self.global_scope_path.write_text("authorized.test\n", encoding="utf-8")
        code, stdout, lines, artifacts = self.run_boundary()
        self.assertEqual(code, 1, stdout)
        self.assertIn("POLICY_BOUNDARY_STATUS=deny", lines)
        self.assertIn("POLICY_BOUNDARY_AUDIT_EVENT=PROGRAM_POLICY_DENY", lines)
        artifact = self.read_artifact(artifacts)
        self.assertEqual(artifact["boundary"]["status"], "deny")
        self.assertEqual(artifact["decision"]["verdict"], "deny")
        self.assertIn("NOT_IN_GLOBAL_SCOPE", artifact["decision"]["deny_reason_codes"])

    def test_invalid_helper_json_fails_closed_with_artifact(self):
        helper = self.write_fake_helper(
            """
            print("{not valid json")
            """
        )
        code, stdout, lines, artifacts = self.run_boundary(helper_path=helper)
        self.assertEqual(code, 2, stdout)
        self.assertIn("POLICY_BOUNDARY_STATUS=error", lines)
        artifact = self.read_artifact(artifacts)
        self.assertEqual(artifact["boundary"]["status"], "error")
        self.assertIn("invalid helper JSON", artifact["boundary"]["errors"][0])
        self.assertIsNone(artifact["decision"])

    def test_timeout_fails_closed_with_artifact(self):
        helper = self.write_fake_helper(
            """
            import time
            time.sleep(2)
            """
        )
        code, stdout, lines, artifacts = self.run_boundary(argv=self.argv(timeout_seconds="0.1"), helper_path=helper)
        self.assertEqual(code, 2, stdout)
        self.assertIn("POLICY_BOUNDARY_STATUS=error", lines)
        artifact = self.read_artifact(artifacts)
        self.assertEqual(artifact["boundary"]["status"], "error")
        self.assertTrue(artifact["helper"]["timed_out"])

    def test_helper_subprocess_ignores_pythonpath_sitecustomize_bypass_attempt(self):
        self.global_scope_path.write_text("authorized.test\n", encoding="utf-8")
        poison_dir = self.root / "python-poison"
        poison_dir.mkdir()
        (poison_dir / "sitecustomize.py").write_text(
            """
import json, sys
if '--json' in sys.argv:
    payload = {
        "schema_version": "policy_decision/1.0",
        "verdict": "allow",
        "program_slug": "boundary-test",
        "target": "https://example.test/",
        "normalized_target": "example.test",
        "target_type": "url",
        "technique": "http_probe",
        "mode": "dry-run",
        "reasons": ["forged allow"],
        "errors": [],
        "warnings": [],
        "deny_reason_codes": [],
        "audit_event": "PROGRAM_POLICY_ALLOW",
        "program_file_sha256": "a" * 64,
        "global_scope_sha256": "b" * 64,
        "decided_at_utc": "2026-05-15T00:00:00Z",
    }
    print(json.dumps(payload))
    raise SystemExit(0)
""".lstrip(),
            encoding="utf-8",
        )
        old_pythonpath = os.environ.get("PYTHONPATH")
        os.environ["PYTHONPATH"] = str(poison_dir)
        try:
            code, stdout, lines, artifacts = self.run_boundary()
        finally:
            if old_pythonpath is None:
                os.environ.pop("PYTHONPATH", None)
            else:
                os.environ["PYTHONPATH"] = old_pythonpath
        self.assertEqual(code, 1, stdout)
        self.assertIn("POLICY_BOUNDARY_STATUS=deny", lines)
        artifact = self.read_artifact(artifacts)
        self.assertEqual(artifact["decision"]["verdict"], "deny")
        self.assertNotIn("forged allow", json.dumps(artifact))

    def test_contradictory_helper_exit_code_vs_verdict_fails_closed(self):
        helper = self.write_fake_helper(self.valid_fake_decision_source(verdict="allow", returncode=1))
        code, stdout, lines, artifacts = self.run_boundary(helper_path=helper)
        self.assertEqual(code, 2, stdout)
        self.assertIn("POLICY_BOUNDARY_STATUS=error", lines)
        artifact = self.read_artifact(artifacts)
        self.assertEqual(artifact["boundary"]["status"], "error")
        self.assertIn("helper exit code contradicts allow verdict", artifact["boundary"]["contract_errors"])
        self.assertEqual(artifact["decision"]["verdict"], "allow")

    def test_unknown_helper_contract_field_fails_closed(self):
        helper = self.write_fake_helper(
            self.valid_fake_decision_source().replace(
                '"decided_at_utc": "2026-05-15T00:00:00Z",',
                '"decided_at_utc": "2026-05-15T00:00:00Z",\n                "unexpected": "schema drift",',
            )
        )
        code, stdout, lines, artifacts = self.run_boundary(helper_path=helper)
        self.assertEqual(code, 2, stdout)
        self.assertIn("POLICY_BOUNDARY_STATUS=error", lines)
        artifact = self.read_artifact(artifacts)
        self.assertEqual(artifact["boundary"]["status"], "error")
        self.assertIn("decision contract unknown fields: unexpected", artifact["boundary"]["contract_errors"])
        self.assertEqual(artifact["decision"]["unexpected"], "schema drift")

    def test_artifact_contains_boundary_status_and_original_decision_details(self):
        code, stdout, _lines, artifacts = self.run_boundary()
        self.assertEqual(code, 0, stdout)
        artifact = self.read_artifact(artifacts)
        self.assertEqual(artifact["schema_version"], "policy_boundary/1.0")
        self.assertEqual(artifact["boundary"]["status"], "allow")
        self.assertEqual(artifact["request"]["target"], "https://example.test/")
        self.assertEqual(artifact["decision"]["schema_version"], "policy_decision/1.0")
        self.assertEqual(artifact["decision"]["program_slug"], "boundary-test")

    def test_stdout_key_value_lines_contain_no_raw_nested_json(self):
        code, stdout, lines, _artifacts = self.run_boundary()
        self.assertEqual(code, 0, stdout)
        self.assertTrue(lines)
        for line in lines:
            self.assertRegex(line, r"^POLICY_BOUNDARY_[A-Z_]+=")
        self.assertNotIn("{", stdout)
        self.assertNotIn("}", stdout)
        self.assertNotIn("[", stdout)
        self.assertNotIn("]", stdout)


    def test_forced_deny_writes_contract_artifact_without_helper(self):
        argv = self.argv(target="192.0.2.0/24") + [
            "--force-deny-code",
            "CIDR_REQUIRES_ALLOW_CIDR",
            "--force-deny-message",
            "CIDR targets require --allow-cidr in program policy mode",
        ]
        code, stdout, lines, artifacts = self.run_boundary(argv=argv)
        self.assertEqual(code, 1, stdout)
        self.assertIn("POLICY_BOUNDARY_STATUS=deny", lines)
        self.assertIn("POLICY_BOUNDARY_AUDIT_EVENT=PROGRAM_POLICY_DENY", lines)
        self.assertIn("POLICY_BOUNDARY_DENY_REASON_CODES=CIDR_REQUIRES_ALLOW_CIDR", lines)
        artifact = self.read_artifact(artifacts)
        self.assertEqual(artifact["boundary"]["status"], "deny")
        self.assertEqual(artifact["boundary"]["deny_reason_codes"], ["CIDR_REQUIRES_ALLOW_CIDR"])
        self.assertEqual(artifact["boundary"]["message"], "CIDR targets require --allow-cidr in program policy mode")
        self.assertIsNone(artifact["helper"]["returncode"])
        self.assertEqual(artifact["decision"]["verdict"], "deny")
        self.assertEqual(artifact["decision"]["target_type"], "cidr")
        self.assertEqual(artifact["decision"]["program_file_sha256"], hashlib.sha256(self.program_path.read_bytes()).hexdigest())
        self.assertEqual(artifact["decision"]["global_scope_sha256"], hashlib.sha256(self.global_scope_path.read_bytes()).hexdigest())

if __name__ == "__main__":
    unittest.main()
