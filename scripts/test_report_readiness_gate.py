"""Focused tests for P2.22 report readiness gate consumer."""

from __future__ import annotations

import ast
import importlib.util
import io
import json
import sys
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE_PATH = ROOT / "scripts" / "build_report_readiness_gate.py"
PLAN_PATH = ROOT / "scripts" / "build_candidate_verification_plan.py"
GAP_PATH = ROOT / "scripts" / "review_candidate_packet_gaps.py"
BUILDER_PATH = ROOT / "scripts" / "build_candidate_review_packet.py"
GATE_SCHEMA_VERSION = "report_readiness_gate/0.1-trial"
SOURCE_SCHEMA_VERSION = "candidate_verification_plan/0.1-trial"
FORBIDDEN_STATE_WORDS = {"ready", "approved", "confirmed", "verified", "accepted", "reportable"}

CHECK_CODES = (
    "CHECK_MISSING_EVIDENCE",
    "CHECK_LOW_CONFIDENCE",
    "CHECK_INFO_SEVERITY_RATIONALE",
    "CHECK_MANUAL_VERIFICATION_NOTES",
    "CHECK_NON_SCANNER_CORROBORATION",
    "CHECK_HUMAN_REMEDIATION_GUIDANCE",
    "CHECK_SAFE_MANUAL_CHECKLIST",
    "CHECK_SCOPE_REVIEW_QUESTION",
)


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


gate = _load(GATE_PATH, "build_report_readiness_gate_under_test")
planner = _load(PLAN_PATH, "build_candidate_verification_plan_for_gate_tests")
gap_consumer = _load(GAP_PATH, "review_candidate_packet_gaps_for_gate_tests")
builder = _load(BUILDER_PATH, "build_candidate_review_packet_for_gate_tests")


def _packet(*inputs: str) -> dict:
    return builder.build_packet(str(ROOT), list(inputs))


def _plan(*inputs: str) -> dict:
    return planner.build_plan(gap_consumer.review_packet(_packet(*inputs)))


def _gate(plan: dict) -> dict:
    return gate.build_gate(plan)


def _minimal_plan(plan_state="blocked", check_codes=None) -> dict:
    if check_codes is None:
        check_codes = ["CHECK_MISSING_EVIDENCE"] if plan_state == "blocked" else ["CHECK_REVIEWER_DECISION"]
    check_items = []
    for code in check_codes:
        check_items.append(
            {
                "code": code,
                "source_gap_code": None if code == "CHECK_REVIEWER_DECISION" else "MISSING_EVIDENCE",
                "action_kind": "manual",
                "prompt": "manual prompt",
            }
        )
    blocked = 1 if plan_state == "blocked" else 0
    manual = 1 if plan_state == "needs_manual_review" else 0
    return {
        "schema_version": SOURCE_SCHEMA_VERSION,
        "status": "ok",
        "source_schema_version": "candidate_review_gap_report/0.1-trial",
        "summary": {
            "finding_count": 1,
            "blocked_count": blocked,
            "needs_manual_review_count": manual,
            "check_item_count": len(check_items),
            "source_gap_code_counts": {},
        },
        "verification_plans": [
            {
                "finding_id": "finding-1",
                "target_value": "example.invalid",
                "module_id": "level1.example",
                "plan_state": plan_state,
                "check_items": check_items,
            }
        ],
        "errors": [],
    }


def _stdout_for(plan: dict, *argv: str) -> tuple[int, dict, str]:
    stdin = io.StringIO(json.dumps(plan, sort_keys=True))
    out = io.StringIO()
    err = io.StringIO()
    old_stdin = sys.stdin
    try:
        sys.stdin = stdin
        with redirect_stdout(out), redirect_stderr(err):
            code, payload = gate.main(list(argv))
    finally:
        sys.stdin = old_stdin
    rendered = out.getvalue()
    parsed = json.loads(rendered)
    self_payload = json.loads(json.dumps(payload, sort_keys=True))
    assert parsed == self_payload
    return code, parsed, err.getvalue()


def _all_values(obj):
    if isinstance(obj, dict):
        for value in obj.values():
            yield from _all_values(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from _all_values(value)
    else:
        yield obj


class HappyPathGateTests(unittest.TestCase):
    def test_builds_gate_from_full_p2_19_to_p2_21_chain(self):
        plan = _plan(
            "tests/fixtures/security_headers_baseline/all_headers_absent/expected_findings.json",
            "tests/fixtures/candidate_review_packet/with_evidence/expected_findings.json",
            "tests/fixtures/candidate_review_packet/low_confidence/expected_findings.json",
            "tests/fixtures/candidate_review_packet/info_severity/expected_findings.json",
        )
        report = _gate(plan)
        self.assertEqual(report["status"], "ok", report)
        self.assertEqual(report["schema_version"], GATE_SCHEMA_VERSION)
        self.assertEqual(report["source_schema_version"], SOURCE_SCHEMA_VERSION)
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["summary"]["finding_count"], len(plan["verification_plans"]))
        self.assertGreater(report["summary"]["blocked_count"], 0)
        self.assertGreater(report["summary"]["needs_manual_review_count"], 0)
        self.assertGreater(sum(report["summary"]["gate_action_counts"].values()), 0)
        keys = [(r["finding_id"], r["target_value"], r["module_id"]) for r in report["gate_results"]]
        self.assertEqual(keys, sorted(keys))
        states = {r["gate_state"] for r in report["gate_results"]}
        self.assertTrue(states.issubset({"blocked", "needs_manual_review"}))
        for r in report["gate_results"]:
            actions = r["gate_actions"]
            self.assertEqual(actions, sorted(actions, key=gate.GATE_ACTION_INDEX.get))
            reasons = r["block_reasons"]
            self.assertEqual(reasons, sorted(reasons, key=gate.BLOCK_REASON_INDEX.get))
            if r["gate_state"] == "needs_manual_review":
                self.assertEqual(reasons, [])

    def test_blocked_plan_state_remains_blocked_in_gate(self):
        plan = _minimal_plan("blocked", ["CHECK_MISSING_EVIDENCE"])
        report = _gate(plan)
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["gate_results"][0]["gate_state"], "blocked")
        self.assertEqual(report["gate_results"][0]["block_reasons"], ["BLOCK_MISSING_EVIDENCE"])
        self.assertEqual(report["gate_results"][0]["gate_actions"], ["GATE_COLLECT_EVIDENCE"])

    def test_needs_manual_review_remains_needs_manual_review_in_gate(self):
        plan = _minimal_plan("needs_manual_review", ["CHECK_REVIEWER_DECISION"])
        report = _gate(plan)
        self.assertEqual(report["status"], "ok")
        result = report["gate_results"][0]
        self.assertEqual(result["gate_state"], "needs_manual_review")
        self.assertEqual(result["block_reasons"], [])
        self.assertEqual(result["gate_actions"], ["GATE_ADD_HUMAN_REVIEW_DECISION"])

    def test_each_check_code_maps_to_stable_action_and_block_reason(self):
        expected_action = {
            "CHECK_MISSING_EVIDENCE": "GATE_COLLECT_EVIDENCE",
            "CHECK_LOW_CONFIDENCE": "GATE_COMPLETE_MANUAL_CHECKS",
            "CHECK_INFO_SEVERITY_RATIONALE": "GATE_KEEP_OUT_OF_REPORT",
            "CHECK_MANUAL_VERIFICATION_NOTES": "GATE_COMPLETE_MANUAL_CHECKS",
            "CHECK_NON_SCANNER_CORROBORATION": "GATE_COMPLETE_MANUAL_CHECKS",
            "CHECK_HUMAN_REMEDIATION_GUIDANCE": "GATE_ADD_REMEDIATION_GUIDANCE",
            "CHECK_SAFE_MANUAL_CHECKLIST": "GATE_ADD_VERIFICATION_GUIDANCE",
            "CHECK_SCOPE_REVIEW_QUESTION": "GATE_ADD_SCOPE_REVIEW",
            "CHECK_REVIEWER_DECISION": "GATE_ADD_HUMAN_REVIEW_DECISION",
        }
        expected_block = {
            "CHECK_MISSING_EVIDENCE": "BLOCK_MISSING_EVIDENCE",
            "CHECK_LOW_CONFIDENCE": "BLOCK_LOW_CONFIDENCE",
            "CHECK_INFO_SEVERITY_RATIONALE": "BLOCK_INFO_SEVERITY",
            "CHECK_MANUAL_VERIFICATION_NOTES": "BLOCK_MANUAL_VERIFICATION_REQUIRED",
            "CHECK_NON_SCANNER_CORROBORATION": "BLOCK_SCANNER_OUTPUT_ONLY",
            "CHECK_HUMAN_REMEDIATION_GUIDANCE": "BLOCK_MISSING_REMEDIATION",
            "CHECK_SAFE_MANUAL_CHECKLIST": "BLOCK_MISSING_VERIFICATION_GUIDANCE",
            "CHECK_SCOPE_REVIEW_QUESTION": "BLOCK_MISSING_SCOPE_REVIEW_QUESTION",
        }
        for code in CHECK_CODES:
            with self.subTest(code=code):
                plan = _minimal_plan("blocked", [code])
                report = _gate(plan)
                self.assertEqual(report["status"], "ok")
                result = report["gate_results"][0]
                self.assertEqual(result["gate_actions"], [expected_action[code]])
                self.assertEqual(result["block_reasons"], [expected_block[code]])

    def test_multiple_checks_dedupe_actions_and_keep_canonical_order(self):
        codes = [
            "CHECK_LOW_CONFIDENCE",
            "CHECK_MANUAL_VERIFICATION_NOTES",
            "CHECK_NON_SCANNER_CORROBORATION",
            "CHECK_MISSING_EVIDENCE",
            "CHECK_SCOPE_REVIEW_QUESTION",
        ]
        plan = _minimal_plan("blocked", codes)
        report = _gate(plan)
        result = report["gate_results"][0]
        self.assertEqual(
            result["gate_actions"],
            [
                "GATE_COLLECT_EVIDENCE",
                "GATE_COMPLETE_MANUAL_CHECKS",
                "GATE_ADD_SCOPE_REVIEW",
            ],
        )
        self.assertEqual(
            result["block_reasons"],
            [
                "BLOCK_MISSING_EVIDENCE",
                "BLOCK_LOW_CONFIDENCE",
                "BLOCK_MANUAL_VERIFICATION_REQUIRED",
                "BLOCK_SCANNER_OUTPUT_ONLY",
                "BLOCK_MISSING_SCOPE_REVIEW_QUESTION",
            ],
        )

    def test_deterministic_on_repeat(self):
        plan = _plan(
            "tests/fixtures/security_headers_baseline/weak_csp/expected_findings.json",
            "tests/fixtures/candidate_review_packet/low_confidence/expected_findings.json",
        )
        first = json.dumps(_gate(plan), sort_keys=True, separators=(",", ":"))
        second = json.dumps(_gate(plan), sort_keys=True, separators=(",", ":"))
        self.assertEqual(first, second)

    def test_output_never_contains_promoted_state_words_as_json_values(self):
        plan = _minimal_plan("blocked", list(CHECK_CODES))
        report = _gate(plan)
        for value in _all_values(report):
            if isinstance(value, str):
                self.assertNotIn(value.lower(), FORBIDDEN_STATE_WORDS)

    def test_summary_gate_action_counts_aggregate_across_findings(self):
        plan = _plan(
            "tests/fixtures/security_headers_baseline/all_headers_absent/expected_findings.json",
            "tests/fixtures/candidate_review_packet/with_evidence/expected_findings.json",
            "tests/fixtures/candidate_review_packet/low_confidence/expected_findings.json",
        )
        report = _gate(plan)
        recomputed: dict[str, int] = {}
        for result in report["gate_results"]:
            for action in result["gate_actions"]:
                recomputed[action] = recomputed.get(action, 0) + 1
        self.assertEqual(report["summary"]["gate_action_counts"], recomputed)


class ErrorContractTests(unittest.TestCase):
    def test_rejects_malformed_stdin_with_json_error(self):
        old_stdin = sys.stdin
        out = io.StringIO()
        err = io.StringIO()
        try:
            sys.stdin = io.StringIO("{not-json")
            with redirect_stdout(out), redirect_stderr(err):
                code, payload = gate.main([])
        finally:
            sys.stdin = old_stdin
        self.assertNotEqual(code, 0)
        parsed = json.loads(out.getvalue())
        self.assertEqual(parsed, payload)
        self.assertEqual(parsed["status"], "error")
        self.assertIsNone(parsed["source_schema_version"])
        self.assertEqual(parsed["gate_results"], [])
        self.assertEqual(parsed["summary"], gate._empty_summary())
        self.assertIn("INPUT_JSON_INVALID", [e["code"] for e in parsed["errors"]])
        self.assertEqual(err.getvalue(), "")

    def test_rejects_wrong_schema_status_and_source_errors(self):
        plan = _minimal_plan()
        plan["schema_version"] = "candidate_verification_plan/999"
        report = _gate(plan)
        self.assertEqual(report["status"], "error")
        self.assertIn("PLAN_SCHEMA_UNSUPPORTED", [e["code"] for e in report["errors"]])

        plan = _minimal_plan()
        plan["status"] = "error"
        report = _gate(plan)
        self.assertEqual(report["status"], "error")
        self.assertIn("PLAN_STATUS_NOT_OK", [e["code"] for e in report["errors"]])

        plan = _minimal_plan()
        plan["errors"] = [{"code": "UPSTREAM", "path": "x", "message": "bad"}]
        report = _gate(plan)
        self.assertEqual(report["status"], "error")
        self.assertIn("PLAN_ERRORS_PRESENT", [e["code"] for e in report["errors"]])

    def test_rejects_non_object_missing_verification_plans_and_bad_entries(self):
        self.assertIn("PLAN_NOT_OBJECT", [e["code"] for e in gate.build_gate([])["errors"]])

        plan = _minimal_plan()
        plan["verification_plans"] = "bad"
        report = _gate(plan)
        self.assertIn("VERIFICATION_PLANS_NOT_LIST", [e["code"] for e in report["errors"]])

        plan = _minimal_plan()
        plan["verification_plans"] = ["bad"]
        plan["summary"]["finding_count"] = 1
        plan["summary"]["blocked_count"] = 0
        plan["summary"]["needs_manual_review_count"] = 0
        report = _gate(plan)
        self.assertIn("VERIFICATION_PLAN_NOT_OBJECT", [e["code"] for e in report["errors"]])

    def test_rejects_unknown_plan_state_unknown_and_duplicate_check_codes(self):
        plan = _minimal_plan()
        plan["verification_plans"][0]["plan_state"] = "later"
        report = _gate(plan)
        self.assertIn("PLAN_STATE_UNSUPPORTED", [e["code"] for e in report["errors"]])

        for promoted in ("ready", "approved", "confirmed", "verified", "accepted", "reportable"):
            with self.subTest(state=promoted):
                plan = _minimal_plan()
                plan["verification_plans"][0]["plan_state"] = promoted
                report = _gate(plan)
                self.assertEqual(report["status"], "error")
                self.assertIn("PLAN_STATE_UNSUPPORTED", [e["code"] for e in report["errors"]])

        plan = _minimal_plan()
        plan["verification_plans"][0]["check_items"] = [
            {"code": "CHECK_DOES_NOT_EXIST", "source_gap_code": None, "action_kind": "x", "prompt": "y"}
        ]
        report = _gate(plan)
        self.assertIn("CHECK_ITEM_CODE_UNSUPPORTED", [e["code"] for e in report["errors"]])

        plan = _minimal_plan()
        plan["verification_plans"][0]["check_items"] = [
            {"code": "CHECK_MISSING_EVIDENCE", "source_gap_code": "MISSING_EVIDENCE", "action_kind": "x", "prompt": "y"},
            {"code": "CHECK_MISSING_EVIDENCE", "source_gap_code": "MISSING_EVIDENCE", "action_kind": "x", "prompt": "y"},
        ]
        report = _gate(plan)
        self.assertIn("CHECK_ITEM_CODE_DUPLICATE", [e["code"] for e in report["errors"]])

    def test_rejects_malformed_and_mismatched_summary_counts(self):
        plan = _minimal_plan()
        plan["summary"]["finding_count"] = True
        report = _gate(plan)
        self.assertIn("SUMMARY_COUNT_INVALID", [e["code"] for e in report["errors"]])

        plan = _minimal_plan()
        plan["summary"]["blocked_count"] = -1
        report = _gate(plan)
        self.assertIn("SUMMARY_COUNT_INVALID", [e["code"] for e in report["errors"]])

        plan = _minimal_plan()
        plan["summary"]["finding_count"] = 99
        report = _gate(plan)
        self.assertIn("SUMMARY_FINDING_COUNT_MISMATCH", [e["code"] for e in report["errors"]])

        plan = _minimal_plan()
        plan["summary"]["blocked_count"] = 99
        report = _gate(plan)
        self.assertIn("SUMMARY_BLOCKED_COUNT_MISMATCH", [e["code"] for e in report["errors"]])

        plan = _minimal_plan()
        plan["summary"]["needs_manual_review_count"] = 99
        report = _gate(plan)
        self.assertIn("SUMMARY_NEEDS_MANUAL_REVIEW_COUNT_MISMATCH", [e["code"] for e in report["errors"]])

    def test_rejects_non_object_summary_and_non_list_check_items(self):
        plan = _minimal_plan()
        plan["summary"] = "bad"
        report = _gate(plan)
        self.assertIn("SUMMARY_NOT_OBJECT", [e["code"] for e in report["errors"]])

        plan = _minimal_plan()
        plan["verification_plans"][0]["check_items"] = "bad"
        report = _gate(plan)
        self.assertIn("CHECK_ITEMS_NOT_LIST", [e["code"] for e in report["errors"]])

    def test_error_payload_shape_matches_contract(self):
        plan = _minimal_plan()
        plan["schema_version"] = "candidate_verification_plan/999"
        report = _gate(plan)
        self.assertEqual(report["status"], "error")
        self.assertEqual(report["schema_version"], GATE_SCHEMA_VERSION)
        self.assertIsNone(report["source_schema_version"])
        self.assertEqual(report["summary"], gate._empty_summary())
        self.assertEqual(report["gate_results"], [])
        for entry in report["errors"]:
            self.assertEqual(set(entry.keys()), {"code", "path", "message"})


class CliSafetyTests(unittest.TestCase):
    def test_rejects_live_target_flags_with_json_error(self):
        plan = _minimal_plan()
        for flag in ("--target", "--target=example.invalid", "--url", "--host", "--scope", "--live"):
            with self.subTest(flag=flag):
                args = [flag] if flag in {"--live", "--target=example.invalid"} else [flag, "example.com"]
                code, parsed, err = _stdout_for(plan, *args)
                self.assertNotEqual(code, 0)
                self.assertEqual(parsed["status"], "error")
                self.assertIn("LIVE_TARGET_FLAG_NOT_ALLOWED", [e["code"] for e in parsed["errors"]])
                self.assertEqual(err, "")

    def test_rejects_positional_argument_with_json_error(self):
        plan = _minimal_plan()
        code, parsed, err = _stdout_for(plan, "unexpected-positional")
        self.assertNotEqual(code, 0)
        self.assertEqual(parsed["status"], "error")
        self.assertIn("ARGUMENT_NOT_ALLOWED", [e["code"] for e in parsed["errors"]])
        self.assertEqual(err, "")


class BoundaryTests(unittest.TestCase):
    def test_static_source_has_no_network_subprocess_file_or_runtime_primitives(self):
        source = GATE_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source)
        forbidden_import_roots = {
            "socket", "http", "urllib", "requests", "httpx", "ssl", "subprocess",
            "asyncio", "selectors", "module_runner", "recon", "pathlib", "os",
        }
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertNotIn(alias.name.split(".")[0], forbidden_import_roots)
            if isinstance(node, ast.ImportFrom) and node.module:
                self.assertNotIn(node.module.split(".")[0], forbidden_import_roots)
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Attribute):
                    self.assertNotIn(func.attr, {"read_text", "read_bytes", "write_text", "write_bytes", "system", "popen"})
                    if func.attr == "open":
                        self.fail("open calls are not allowed in the P2.22 consumer")
                if isinstance(func, ast.Name):
                    self.assertNotIn(func.id, {"open", "exec", "eval", "compile"})

    def test_no_schema_promotion_file_exists(self):
        matches = list((ROOT / "modules" / "_schema").glob("*report_readiness_gate*"))
        self.assertEqual(matches, [])

    def test_no_output_file_options_drafting_or_promotion_terms(self):
        source = GATE_PATH.read_text(encoding="utf-8").lower()
        for forbidden in (
            "--output",
            "--input",
            "--repo-root",
            "markdown",
            "html",
            "pdf",
            "platform adapter",
            "report draft",
            "submission",
            "reportable",
            "approved",
            "confirmed",
            "verified",
            "accepted",
        ):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
