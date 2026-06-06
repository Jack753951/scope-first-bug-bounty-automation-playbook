import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.core.policy import decide_program_policy


def base_program(
    *,
    in_scope=None,
    out_of_scope=None,
    allowed=None,
    forbidden=None,
    automation_permitted=True,
    automation_profile=None,
    controlled_capabilities=None,
    a4_capabilities=None,
):
    techniques = {
        "allowed": allowed or ["http_probe"],
        "forbidden": forbidden or ["dos", "credential_brute_force"],
        "automation_permitted": automation_permitted,
    }
    if automation_profile is not None:
        techniques["automation_profile"] = automation_profile
    if controlled_capabilities is not None:
        techniques["controlled_capabilities"] = controlled_capabilities
    if a4_capabilities is not None:
        techniques["a4_capabilities"] = a4_capabilities
    return {
        "schema_version": "1.0",
        "program": {
            "slug": "policy-test",
            "name": "Policy Test",
            "platform": "lab",
            "url": "file:///policy-test",
            "authorization_reference": "Local unit-test fixture only.",
            "policy_version": "2026-05-15",
            "policy_acknowledged_at": "2026-05-15T00:00:00Z",
        },
        "scope": {
            "in_scope": in_scope or [{"type": "domain", "value": "example.test"}],
            "out_of_scope": out_of_scope or [],
            "idn_handling": "punycode_only",
        },
        "techniques": techniques,
        "rate_limits": {
            "max_concurrency": 1,
        },
        "testing_windows": {
            "always": True,
        },
        "expiration": {
            "valid_from": "2026-01-01T00:00:00Z",
            "valid_until": "2027-01-01T00:00:00Z",
        },
    }


class ProgramPolicyCheckTests(unittest.TestCase):
    def write_fixture(self, program, global_scope):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        program_path = root / "program.json"
        global_path = root / "scope.txt"
        program_path.write_text(json.dumps(program), encoding="utf-8")
        global_path.write_text(global_scope, encoding="utf-8")
        self.addCleanup(temp.cleanup)
        return program_path, global_path

    def decide(
        self,
        program,
        global_scope,
        target="https://example.test/",
        technique="http_probe",
        mode="dry-run",
        now=None,
    ):
        program_path, global_path = self.write_fixture(program, global_scope)
        decision = decide_program_policy(
            program_path=program_path,
            global_scope_path=global_path,
            target=target,
            technique=technique,
            mode=mode,
            ignore_time=True,
            now=now,
        )
        return decision, program_path, global_path

    def test_safe_example_target_allowed_by_program_and_global_scope(self):
        now = datetime(2026, 5, 15, 12, 34, 56, tzinfo=timezone.utc)
        decision, program_path, global_path = self.decide(base_program(), "example.test\n", now=now)
        self.assertEqual(decision.verdict, "allow", decision.errors)
        self.assertEqual(decision.normalized_target, "example.test")
        self.assertEqual(decision.target_type, "url")
        self.assertEqual(decision.audit_event, "PROGRAM_POLICY_ALLOW")
        payload = decision.as_dict()
        self.assertEqual(payload["schema_version"], "policy_decision/1.0")
        self.assertEqual(payload["deny_reason_codes"], [])
        self.assertTrue(payload["reasons"])
        self.assertEqual(payload["program_file_sha256"], sha256(program_path.read_bytes()).hexdigest())
        self.assertEqual(payload["global_scope_sha256"], sha256(global_path.read_bytes()).hexdigest())
        self.assertEqual(payload["decided_at_utc"], "2026-05-15T12:34:56Z")

    def test_deny_when_program_scope_allows_but_global_scope_does_not(self):
        decision, _, _ = self.decide(base_program(), "other.test\n")
        self.assertEqual(decision.verdict, "deny")
        self.assertIn("target does not match global scope", decision.errors)
        self.assertIn("NOT_IN_GLOBAL_SCOPE", decision.as_dict()["deny_reason_codes"])

    def test_deny_when_global_scope_allows_but_program_scope_does_not(self):
        program = base_program(in_scope=[{"type": "domain", "value": "other.test"}])
        decision, _, _ = self.decide(program, "example.test\n")
        self.assertEqual(decision.verdict, "deny")
        self.assertIn("target does not match program in_scope", decision.errors)
        self.assertIn("NOT_IN_PROGRAM_SCOPE", decision.as_dict()["deny_reason_codes"])

    def test_deny_when_out_of_scope_overlaps_in_scope(self):
        program = base_program(
            in_scope=[{"type": "wildcard", "value": "*.example.test"}],
            out_of_scope=[{"type": "domain", "value": "blocked.example.test"}],
        )
        decision, _, _ = self.decide(program, "*.example.test\n", target="https://blocked.example.test/")
        self.assertEqual(decision.verdict, "deny")
        self.assertIn("target matches program out_of_scope", decision.errors)
        self.assertIn("PROGRAM_OUT_OF_SCOPE", decision.as_dict()["deny_reason_codes"])

    def test_deny_forbidden_technique(self):
        program = base_program(
            allowed=["http_probe"],
            forbidden=["port_scan", "dos", "credential_brute_force"],
        )
        decision, _, _ = self.decide(program, "example.test\n", technique="port_scan")
        self.assertEqual(decision.verdict, "deny")
        self.assertTrue(any("forbidden" in error for error in decision.errors))
        self.assertIn("FORBIDDEN_TECHNIQUE", decision.as_dict()["deny_reason_codes"])
        self.assertNotIn("TECHNIQUE_NOT_ALLOWED", decision.as_dict()["deny_reason_codes"])

    def test_deny_allowed_but_automation_disabled_live_mode(self):
        program = base_program(automation_permitted=False)
        decision, _, _ = self.decide(program, "example.test\n", mode="live")
        self.assertEqual(decision.verdict, "deny")
        self.assertTrue(any("automation_permitted" in error for error in decision.errors))
        self.assertIn("AUTOMATION_DISABLED", decision.as_dict()["deny_reason_codes"])

    def test_allow_dry_run_when_automation_disabled(self):
        program = base_program(automation_permitted=False)
        decision, _, _ = self.decide(program, "example.test\n", mode="dry-run")
        self.assertEqual(decision.verdict, "allow", decision.errors)
        self.assertTrue(any("dry-run" in reason for reason in decision.as_dict()["reasons"]))

    def test_allow_a3_api_token_when_profile_is_lane_approved(self):
        program = base_program(
            allowed=["api_token_min_scope_owned_account"],
            automation_profile="A3_BOUNDED_PROOF_ACTIONS",
        )
        decision, _, _ = self.decide(
            program,
            "example.test\n",
            technique="api_token_min_scope_owned_account",
            mode="planned",
        )
        self.assertEqual(decision.verdict, "allow", decision.errors)
        self.assertTrue(any("A3 technique permitted" in reason for reason in decision.reasons))

    def test_deny_a3_without_profile(self):
        program = base_program(allowed=["api_token_min_scope_owned_account"])
        decision, _, _ = self.decide(
            program,
            "example.test\n",
            technique="api_token_min_scope_owned_account",
            mode="planned",
        )
        self.assertEqual(decision.verdict, "deny")
        self.assertIn("VALIDATOR_DENY", decision.as_dict()["deny_reason_codes"])

    def test_allow_a3_bounded_owned_impact_exploit_chain_with_approved_capability(self):
        program = base_program(
            allowed=["exploit_chain_bounded_owned_impact"],
            automation_profile="A3_BOUNDED_PROOF_ACTIONS",
            controlled_capabilities=[
                {
                    "name": "exploit_chain_bounded_owned_impact",
                    "status": "operator_approved",
                    "max_steps": 2,
                    "max_requests_per_run": 6,
                    "allowed_impact": "owned_state_change_recoverable",
                    "cleanup_required": True,
                    "stop_before": [
                        "non_owned_data",
                        "secret_capture",
                        "credential_extraction",
                        "persistence",
                        "final_submission",
                        "uncontrolled_internal_enumeration",
                        "destructive_impact_outside_owned_state",
                    ],
                }
            ],
        )
        decision, _, _ = self.decide(
            program,
            "example.test\n",
            technique="exploit_chain_bounded_owned_impact",
            mode="planned",
        )
        self.assertEqual(decision.verdict, "allow", decision.errors)
        self.assertTrue(any("A3 controlled capability" in reason for reason in decision.reasons))

    def test_deny_a3_ssrf_when_capability_not_operator_approved(self):
        program = base_program(
            allowed=["ssrf_marker_callback"],
            automation_profile="A3_BOUNDED_PROOF_ACTIONS",
            controlled_capabilities=[
                {
                    "name": "ssrf_marker_callback",
                    "status": "not_approved",
                    "max_requests_per_run": 1,
                    "allowed_impact": "marker_only",
                    "cleanup_required": True,
                    "stop_before": [
                        "non_owned_data",
                        "secret_capture",
                        "credential_extraction",
                        "persistence",
                        "final_submission",
                        "uncontrolled_internal_enumeration",
                    ],
                }
            ],
        )
        decision, _, _ = self.decide(program, "example.test\n", technique="ssrf_marker_callback", mode="planned")
        self.assertEqual(decision.verdict, "deny")
        self.assertIn("A3_CAPABILITY_NOT_APPROVED", decision.as_dict()["deny_reason_codes"])

    def test_deny_a3_ssrf_without_operator_controlled_receiver_and_cloud_stop(self):
        program = base_program(
            allowed=["ssrf_marker_callback"],
            automation_profile="A3_BOUNDED_PROOF_ACTIONS",
            controlled_capabilities=[
                {
                    "name": "ssrf_marker_callback",
                    "status": "operator_approved",
                    "max_requests_per_run": 1,
                    "allowed_impact": "marker_only",
                    "cleanup_required": True,
                    "callback_receiver": "third_party_receiver",
                    "stop_before": [
                        "non_owned_data",
                        "secret_capture",
                        "credential_extraction",
                        "persistence",
                        "final_submission",
                        "uncontrolled_internal_enumeration",
                    ],
                }
            ],
        )
        decision, _, _ = self.decide(program, "example.test\n", technique="ssrf_marker_callback", mode="planned")
        self.assertEqual(decision.verdict, "deny")
        self.assertIn("VALIDATOR_DENY", decision.as_dict()["deny_reason_codes"])

    def test_deny_a3_exploit_chain_without_step_cap(self):
        program = base_program(
            allowed=["exploit_chain_bounded_owned_impact"],
            automation_profile="A3_BOUNDED_PROOF_ACTIONS",
            controlled_capabilities=[
                {
                    "name": "exploit_chain_bounded_owned_impact",
                    "status": "operator_approved",
                    "max_requests_per_run": 6,
                    "allowed_impact": "owned_state_change_recoverable",
                    "cleanup_required": True,
                    "stop_before": [
                        "non_owned_data",
                        "secret_capture",
                        "credential_extraction",
                        "persistence",
                        "final_submission",
                        "uncontrolled_internal_enumeration",
                        "destructive_impact_outside_owned_state",
                    ],
                }
            ],
        )
        decision, _, _ = self.decide(
            program,
            "example.test\n",
            technique="exploit_chain_bounded_owned_impact",
            mode="planned",
        )
        self.assertEqual(decision.verdict, "deny")
        self.assertIn("VALIDATOR_DENY", decision.as_dict()["deny_reason_codes"])

    def test_deny_raw_unicode_idn_target(self):
        program = base_program(
            in_scope=[{"type": "domain", "value": "xn--bcher-kva.example"}],
        )
        decision, _, _ = self.decide(
            program,
            "xn--bcher-kva.example\n",
            target="b\u00fccher.example",
        )
        self.assertEqual(decision.verdict, "deny")
        self.assertTrue(any("ASCII" in error for error in decision.errors))
        self.assertIn("INVALID_TARGET", decision.as_dict()["deny_reason_codes"])

    def test_deny_ipv6_target_with_clear_code(self):
        decision, _, _ = self.decide(base_program(), "example.test\n", target="2001:db8::1")
        self.assertEqual(decision.verdict, "deny")
        self.assertIn("IPV6_UNSUPPORTED", decision.as_dict()["deny_reason_codes"])

    def test_allow_wildcard_semantics_include_apex_and_subdomain(self):
        program = base_program(in_scope=[{"type": "wildcard", "value": "*.example.test"}])
        apex, _, _ = self.decide(program, "*.example.test\n", target="example.test")
        subdomain, _, _ = self.decide(program, "*.example.test\n", target="app.example.test")
        self.assertEqual(apex.verdict, "allow", apex.errors)
        self.assertEqual(subdomain.verdict, "allow", subdomain.errors)

    def test_allow_url_prefix_entry(self):
        program = base_program(in_scope=[{"type": "url_prefix", "value": "https://api.example.test/v1/"}])
        decision, _, _ = self.decide(
            program,
            "https://api.example.test/v1/\n",
            target="https://api.example.test/v1/status",
        )
        self.assertEqual(decision.verdict, "allow", decision.errors)

    def test_empty_or_comments_only_global_scope_denies_with_code(self):
        decision, _, _ = self.decide(base_program(), "# comment only\n\n")
        self.assertEqual(decision.verdict, "deny")
        self.assertIn("GLOBAL_SCOPE_ERROR", decision.as_dict()["deny_reason_codes"])

    def test_malformed_global_scope_line_is_warning_only_when_valid_entry_exists(self):
        decision, _, _ = self.decide(base_program(), "bad host\nexample.test\n")
        self.assertEqual(decision.verdict, "allow", decision.errors)
        self.assertTrue(decision.warnings)
        self.assertEqual(decision.as_dict()["deny_reason_codes"], [])

    def test_ipv4_cidr_target_requires_program_and_global_scope_intersection(self):
        program = base_program(in_scope=[{"type": "cidr", "value": "10.10.0.0/16"}])
        allowed, _, _ = self.decide(program, "10.0.0.0/8\n", target="10.10.20.0/24")
        denied_by_program, _, _ = self.decide(program, "10.0.0.0/8\n", target="10.11.20.0/24")
        denied_by_global, _, _ = self.decide(program, "10.11.0.0/16\n", target="10.10.20.0/24")
        self.assertEqual(allowed.verdict, "allow", allowed.errors)
        self.assertEqual(denied_by_program.verdict, "deny")
        self.assertIn("NOT_IN_PROGRAM_SCOPE", denied_by_program.as_dict()["deny_reason_codes"])
        self.assertEqual(denied_by_global.verdict, "deny")
        self.assertIn("NOT_IN_GLOBAL_SCOPE", denied_by_global.as_dict()["deny_reason_codes"])

    def test_url_prefix_explicit_port_must_match(self):
        program = base_program(in_scope=[{"type": "url_prefix", "value": "https://api.example.test:8443/v1/"}])
        matching, _, _ = self.decide(
            program,
            "https://api.example.test:8443/v1/\n",
            target="https://api.example.test:8443/v1/status",
        )
        mismatch, _, _ = self.decide(
            program,
            "https://api.example.test:8443/v1/\n",
            target="https://api.example.test/v1/status",
        )
        self.assertEqual(matching.verdict, "allow", matching.errors)
        self.assertEqual(mismatch.verdict, "deny")
        self.assertIn("NOT_IN_PROGRAM_SCOPE", mismatch.as_dict()["deny_reason_codes"])

    def test_blackout_denial_emits_code(self):
        program = base_program()
        program["testing_windows"] = {
            "always": True,
            "blackouts": [
                {"from": "2026-05-15T12:00:00Z", "to": "2026-05-15T13:00:00Z", "reason": "unit test"}
            ],
        }
        decision, _, _ = self.decide(
            program,
            "example.test\n",
            mode="planned",
            now=datetime(2026, 5, 15, 12, 30, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(decision.verdict, "deny")
        self.assertIn("BLACKOUT", decision.as_dict()["deny_reason_codes"])

    def test_cli_json_shape(self):
        program_path, global_path = self.write_fixture(base_program(), "example.test\n")
        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "program_policy_check.py"),
                "--program",
                str(program_path),
                "--global-scope",
                str(global_path),
                "--target",
                "https://example.test/",
                "--technique",
                "http_probe",
                "--mode",
                "dry-run",
                "--ignore-time",
                "--json",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["verdict"], "allow")
        self.assertEqual(payload["program_slug"], "policy-test")
        self.assertEqual(payload["target"], "https://example.test/")
        self.assertEqual(payload["normalized_target"], "example.test")
        self.assertEqual(payload["target_type"], "url")
        self.assertEqual(payload["technique"], "http_probe")
        self.assertEqual(payload["mode"], "dry-run")
        self.assertIsInstance(payload["reasons"], list)
        self.assertTrue(payload["reasons"])
        self.assertIsInstance(payload["errors"], list)
        self.assertIsInstance(payload["warnings"], list)
        self.assertEqual(payload["schema_version"], "policy_decision/1.0")
        self.assertEqual(payload["deny_reason_codes"], [])
        self.assertRegex(payload["program_file_sha256"], r"^[0-9a-f]{64}$")
        self.assertRegex(payload["global_scope_sha256"], r"^[0-9a-f]{64}$")
        self.assertRegex(payload["decided_at_utc"], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
        self.assertEqual(payload["audit_event"], "PROGRAM_POLICY_ALLOW")


if __name__ == "__main__":
    unittest.main()
