"""Focused tests for P2.23 offline candidate workflow fixture."""

from __future__ import annotations

import ast
import importlib.util
import io
import json
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ROOT / "scripts" / "build_candidate_workflow_fixture.py"
WORKFLOW_SCHEMA_VERSION = "candidate_workflow_fixture/0.1-trial"
FORBIDDEN_PROMOTION_VALUES = {"ready", "approved", "confirmed", "verified", "accepted", "reportable"}
P3_1_CURATED_INPUTS = [
    "tests/fixtures/candidate_review_packet/p3_1_curated_partial_evidence/expected_findings.json",
    "tests/fixtures/candidate_review_packet/p3_1_curated_ambiguous_scope_text/expected_findings.json",
    "tests/fixtures/candidate_review_packet/p3_1_curated_chained_precondition/expected_findings.json",
    "tests/fixtures/candidate_review_packet/p3_1_curated_low_signal_informational/expected_findings.json",
    "tests/fixtures/candidate_review_packet/p3_1_curated_duplicate_pair/expected_findings.json",
    "tests/fixtures/candidate_review_packet/p3_1_curated_non_finding_control/expected_findings.json",
]
P3_2_EXPECTED_TERMINAL_STATES = {
    "p3_1_curated.partial_evidence.candidate": {
        "packet_readiness": "not_ready",
        "gap_review_state": "not_ready",
        "plan_state": "blocked",
        "gate_state": "blocked",
        "required_gap_codes": {"LOW_CONFIDENCE", "MANUAL_VERIFICATION_REQUIRED", "SCANNER_OUTPUT_ONLY"},
    },
    "p3_1_curated.ambiguous_scope_text.candidate": {
        "packet_readiness": "reviewer_decision_required",
        "gap_review_state": "reviewer_decision_required",
        "plan_state": "needs_manual_review",
        "gate_state": "needs_manual_review",
        "required_gap_codes": {"MANUAL_VERIFICATION_REQUIRED", "SCANNER_OUTPUT_ONLY"},
    },
    "p3_1_curated.chained_precondition.browser_condition": {
        "packet_readiness": "reviewer_decision_required",
        "gap_review_state": "reviewer_decision_required",
        "plan_state": "needs_manual_review",
        "gate_state": "needs_manual_review",
        "required_gap_codes": {"MANUAL_VERIFICATION_REQUIRED", "SCANNER_OUTPUT_ONLY"},
    },
    "p3_1_curated.chained_precondition.missing_header": {
        "packet_readiness": "reviewer_decision_required",
        "gap_review_state": "reviewer_decision_required",
        "plan_state": "needs_manual_review",
        "gate_state": "needs_manual_review",
        "required_gap_codes": {"MANUAL_VERIFICATION_REQUIRED", "SCANNER_OUTPUT_ONLY"},
    },
    "p3_1_curated.low_signal_informational.candidate": {
        "packet_readiness": "not_ready",
        "gap_review_state": "not_ready",
        "plan_state": "blocked",
        "gate_state": "blocked",
        "required_gap_codes": {"INFO_SEVERITY_REPORT_BLOCKED", "MANUAL_VERIFICATION_REQUIRED", "SCANNER_OUTPUT_ONLY"},
    },
    "p3_1_curated.duplicate_pair.source_a": {
        "packet_readiness": "reviewer_decision_required",
        "gap_review_state": "reviewer_decision_required",
        "plan_state": "needs_manual_review",
        "gate_state": "needs_manual_review",
        "required_gap_codes": {"MANUAL_VERIFICATION_REQUIRED", "SCANNER_OUTPUT_ONLY"},
    },
    "p3_1_curated.duplicate_pair.source_b": {
        "packet_readiness": "reviewer_decision_required",
        "gap_review_state": "reviewer_decision_required",
        "plan_state": "needs_manual_review",
        "gate_state": "needs_manual_review",
        "required_gap_codes": {"MANUAL_VERIFICATION_REQUIRED", "SCANNER_OUTPUT_ONLY"},
    },
    "p3_1_curated.non_finding_control.candidate": {
        "packet_readiness": "not_ready",
        "gap_review_state": "not_ready",
        "plan_state": "blocked",
        "gate_state": "blocked",
        "required_gap_codes": {"LOW_CONFIDENCE", "MANUAL_VERIFICATION_REQUIRED", "SCANNER_OUTPUT_ONLY"},
    },
}


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


workflow = _load(WORKFLOW_PATH, "build_candidate_workflow_fixture_under_test")


def _all_values(obj):
    if isinstance(obj, dict):
        for value in obj.values():
            yield from _all_values(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from _all_values(value)
    else:
        yield obj


def _stdout_for(*argv: str) -> tuple[int, dict, str]:
    out = io.StringIO()
    err = io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code, payload = workflow.main(list(argv))
    rendered = out.getvalue()
    parsed = json.loads(rendered)
    self_payload = json.loads(json.dumps(payload, sort_keys=True))
    assert parsed == self_payload
    return code, parsed, err.getvalue()


class CandidateWorkflowFixtureTests(unittest.TestCase):
    def test_builds_complete_offline_chain_from_committed_fixtures(self):
        payload = workflow.build_workflow_fixture(
            str(ROOT),
            [
                "tests/fixtures/security_headers_baseline/all_headers_absent/expected_findings.json",
                "tests/fixtures/candidate_review_packet/with_evidence/expected_findings.json",
                "tests/fixtures/candidate_review_packet/low_confidence/expected_findings.json",
                "tests/fixtures/candidate_review_packet/info_severity/expected_findings.json",
            ],
        )
        self.assertEqual(payload["status"], "ok", payload)
        self.assertEqual(payload["schema_version"], WORKFLOW_SCHEMA_VERSION)
        self.assertEqual(payload["errors"], [])
        self.assertEqual(
            payload["source_schema_versions"],
            [
                "candidate_review_packet/0.1-trial",
                "candidate_review_gap_report/0.1-trial",
                "candidate_verification_plan/0.1-trial",
                "report_readiness_gate/0.1-trial",
            ],
        )
        artifacts = payload["artifacts"]
        self.assertEqual(artifacts["candidate_review_packet"]["status"], "ok")
        self.assertEqual(artifacts["candidate_review_gap_report"]["status"], "ok")
        self.assertEqual(artifacts["candidate_verification_plan"]["status"], "ok")
        self.assertEqual(artifacts["report_readiness_gate"]["status"], "ok")
        self.assertEqual(
            payload["summary"],
            {
                "input_count": 4,
                "candidate_count": artifacts["candidate_review_packet"]["summary"]["candidate_count"],
                "gap_finding_count": artifacts["candidate_review_gap_report"]["summary"]["finding_count"],
                "verification_plan_count": artifacts["candidate_verification_plan"]["summary"]["finding_count"],
                "gate_result_count": artifacts["report_readiness_gate"]["summary"]["finding_count"],
                "blocked_count": artifacts["report_readiness_gate"]["summary"]["blocked_count"],
                "needs_manual_review_count": artifacts["report_readiness_gate"]["summary"]["needs_manual_review_count"],
            },
        )
        self.assertGreater(payload["summary"]["blocked_count"], 0)
        self.assertGreater(payload["summary"]["needs_manual_review_count"], 0)

    def test_workflow_preserves_only_non_promotional_gate_states(self):
        payload = workflow.build_workflow_fixture(
            str(ROOT),
            [
                "tests/fixtures/candidate_review_packet/with_evidence/expected_findings.json",
                "tests/fixtures/candidate_review_packet/low_confidence/expected_findings.json",
            ],
        )
        self.assertEqual(payload["status"], "ok", payload)
        states = {
            entry["gate_state"]
            for entry in payload["artifacts"]["report_readiness_gate"]["gate_results"]
        }
        self.assertTrue(states.issubset({"blocked", "needs_manual_review"}))
        string_values = {value for value in _all_values(payload) if isinstance(value, str)}
        self.assertFalse(FORBIDDEN_PROMOTION_VALUES & string_values)

    def test_upstream_error_fails_closed_without_running_later_stages(self):
        payload = workflow.build_workflow_fixture(
            str(ROOT),
            ["tests/fixtures/candidate_review_packet/forbidden_status/expected_findings.json"],
        )
        self.assertEqual(payload["status"], "error")
        self.assertEqual(payload["summary"]["candidate_count"], 0)
        self.assertEqual(payload["artifacts"]["candidate_review_packet"]["status"], "error")
        self.assertNotIn("candidate_review_gap_report", payload["artifacts"])
        self.assertEqual(payload["errors"][0]["code"], "WORKFLOW_STAGE_FAILED")
        self.assertEqual(payload["errors"][0]["stage"], "candidate_review_packet")

    def test_cli_emits_compact_json_and_rejects_live_target_flags(self):
        for argv in (
            ("--target", "example.invalid"),
            ("--target=example.invalid",),
            ("--url", "https://example.invalid"),
            ("--host", "example.invalid"),
            ("--scope", "program"),
            ("--live",),
            ("tests/fixtures/candidate_review_packet/with_evidence/expected_findings.json",),
        ):
            with self.subTest(argv=argv):
                code, payload, stderr = _stdout_for(*argv)
                self.assertEqual(code, 2)
                self.assertEqual(stderr, "")
                self.assertEqual(payload["schema_version"], WORKFLOW_SCHEMA_VERSION)
                self.assertEqual(payload["status"], "error")
                self.assertEqual(payload["artifacts"], {})
                self.assertIn(
                    payload["errors"][0]["code"],
                    {"LIVE_TARGET_FLAG_NOT_ALLOWED", "ARGUMENT_NOT_ALLOWED", "REQUIRED_ARGUMENT_MISSING"},
                )

    def test_cli_happy_path_uses_repo_root_and_repeatable_input(self):
        code, payload, stderr = _stdout_for(
            "--repo-root",
            str(ROOT),
            "--input",
            "tests/fixtures/candidate_review_packet/with_evidence/expected_findings.json",
            "--input",
            "tests/fixtures/candidate_review_packet/low_confidence/expected_findings.json",
        )
        self.assertEqual(code, 0, payload)
        self.assertEqual(stderr, "")
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["summary"]["input_count"], 2)

    def test_p3_1_curated_cases_cover_non_promotional_vocabulary(self):
        missing = [rel for rel in P3_1_CURATED_INPUTS if not (ROOT / rel).exists()]
        self.assertEqual(missing, [], f"P3.1 curated fixture(s) missing: {missing}")
        payload = workflow.build_workflow_fixture(str(ROOT), P3_1_CURATED_INPUTS)
        self.assertEqual(payload["status"], "ok", payload)
        gap_summary = payload["artifacts"]["candidate_review_gap_report"]["summary"]
        self.assertGreaterEqual(gap_summary["not_ready_count"], 1)
        self.assertGreaterEqual(gap_summary["reviewer_decision_required_count"], 1)
        self.assertGreaterEqual(gap_summary["blocked_count"], 1)

        plan_states = {
            entry["plan_state"]
            for entry in payload["artifacts"]["candidate_verification_plan"]["verification_plans"]
        }
        gate_states = {
            entry["gate_state"]
            for entry in payload["artifacts"]["report_readiness_gate"]["gate_results"]
        }
        self.assertGreaterEqual(plan_states, {"blocked", "needs_manual_review"})
        self.assertGreaterEqual(gate_states, {"blocked", "needs_manual_review"})

    def test_p3_1_curated_cases_are_byte_identical_and_non_promotional(self):
        missing = [rel for rel in P3_1_CURATED_INPUTS if not (ROOT / rel).exists()]
        self.assertEqual(missing, [], f"P3.1 curated fixture(s) missing: {missing}")
        first = workflow.build_workflow_fixture(str(ROOT), P3_1_CURATED_INPUTS)
        second = workflow.build_workflow_fixture(str(ROOT), P3_1_CURATED_INPUTS)
        first_json = json.dumps(first, sort_keys=True, separators=(",", ":"))
        second_json = json.dumps(second, sort_keys=True, separators=(",", ":"))
        self.assertEqual(first_json, second_json)

        forbidden = {"confirmed", "verified", "accepted", "ready_for_submission", "fail", "pass"}
        values = {value for value in _all_values(first) if isinstance(value, str)}
        self.assertFalse(forbidden & values)

    def test_p3_2_curated_cases_match_terminal_state_expectation_matrix(self):
        payload = workflow.build_workflow_fixture(str(ROOT), P3_1_CURATED_INPUTS)
        self.assertEqual(payload["status"], "ok", payload)
        artifacts = payload["artifacts"]
        packet_by_id = {finding["id"]: finding for finding in artifacts["candidate_review_packet"]["findings"]}
        gaps_by_id = {
            finding_gap["finding_id"]: finding_gap
            for finding_gap in artifacts["candidate_review_gap_report"]["finding_gaps"]
        }
        plans_by_id = {
            plan["finding_id"]: plan
            for plan in artifacts["candidate_verification_plan"]["verification_plans"]
        }
        gates_by_id = {
            gate["finding_id"]: gate
            for gate in artifacts["report_readiness_gate"]["gate_results"]
        }
        expected_ids = set(P3_2_EXPECTED_TERMINAL_STATES)
        self.assertEqual(expected_ids, set(packet_by_id))
        self.assertEqual(expected_ids, set(gaps_by_id))
        self.assertEqual(expected_ids, set(plans_by_id))
        self.assertEqual(expected_ids, set(gates_by_id))

        for finding_id, expected in P3_2_EXPECTED_TERMINAL_STATES.items():
            with self.subTest(finding_id=finding_id):
                self.assertEqual(packet_by_id[finding_id]["report_readiness"], expected["packet_readiness"])
                self.assertEqual(gaps_by_id[finding_id]["review_state"], expected["gap_review_state"])
                self.assertTrue(expected["required_gap_codes"].issubset(set(gaps_by_id[finding_id]["gap_codes"])))
                self.assertEqual(plans_by_id[finding_id]["plan_state"], expected["plan_state"])
                self.assertEqual(gates_by_id[finding_id]["gate_state"], expected["gate_state"])


class StaticSafetyTests(unittest.TestCase):
    def test_script_has_no_network_subprocess_or_file_write_imports(self):
        tree = ast.parse(WORKFLOW_PATH.read_text(encoding="utf-8"))
        forbidden_imports = {"socket", "subprocess", "requests", "urllib", "http", "ftplib", "smtplib"}
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
        self.assertFalse(forbidden_imports & imports)
        forbidden_calls = {"open", "write_text", "write_bytes", "replace", "rename", "unlink", "mkdir"}
        calls = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Name):
                    calls.add(func.id)
                elif isinstance(func, ast.Attribute):
                    calls.add(func.attr)
        self.assertFalse(forbidden_calls & calls)


if __name__ == "__main__":
    unittest.main()
