"""Focused tests for P2.21 candidate verification checklist consumer."""

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
PLAN_PATH = ROOT / "scripts" / "build_candidate_verification_plan.py"
GAP_PATH = ROOT / "scripts" / "review_candidate_packet_gaps.py"
BUILDER_PATH = ROOT / "scripts" / "build_candidate_review_packet.py"
PLAN_SCHEMA_VERSION = "candidate_verification_plan/0.1-trial"
GAP_SCHEMA_VERSION = "candidate_review_gap_report/0.1-trial"
FORBIDDEN_STATE_WORDS = {"ready", "approved", "confirmed", "verified", "accepted"}
GAP_CODES = (
    "MISSING_EVIDENCE",
    "LOW_CONFIDENCE",
    "INFO_SEVERITY_REPORT_BLOCKED",
    "MANUAL_VERIFICATION_REQUIRED",
    "SCANNER_OUTPUT_ONLY",
    "MISSING_REMEDIATION",
    "MISSING_VERIFICATION_GUIDANCE",
    "MISSING_SCOPE_REVIEW_QUESTION",
)


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


planner = _load(PLAN_PATH, "build_candidate_verification_plan_under_test")
gap_consumer = _load(GAP_PATH, "review_candidate_packet_gaps_for_plan_tests")
builder = _load(BUILDER_PATH, "build_candidate_review_packet_for_plan_tests")


def _packet(*inputs: str) -> dict:
    return builder.build_packet(str(ROOT), list(inputs))


def _gap_report(*inputs: str) -> dict:
    return gap_consumer.review_packet(_packet(*inputs))


def _plan(report: dict) -> dict:
    return planner.build_plan(report)


def _minimal_gap_report(gap_codes=None, review_state="not_ready") -> dict:
    if gap_codes is None:
        gap_codes = ["MISSING_EVIDENCE"]
    counts = {code: gap_codes.count(code) for code in GAP_CODES if gap_codes.count(code)}
    return {
        "schema_version": GAP_SCHEMA_VERSION,
        "status": "ok",
        "source_schema_version": "candidate_review_packet/0.1-trial",
        "summary": {
            "finding_count": 1,
            "blocked_count": 1 if gap_codes else 0,
            "not_ready_count": 1 if review_state == "not_ready" else 0,
            "reviewer_decision_required_count": 1 if review_state == "reviewer_decision_required" else 0,
            "gap_code_counts": counts,
        },
        "finding_gaps": [
            {
                "finding_id": "finding-1",
                "target_value": "example.invalid",
                "module_id": "level1.example",
                "review_state": review_state,
                "gap_codes": list(gap_codes),
            }
        ],
        "errors": [],
    }


def _stdout_for(report: dict, *argv: str) -> tuple[int, dict, str]:
    stdin = io.StringIO(json.dumps(report, sort_keys=True))
    out = io.StringIO()
    err = io.StringIO()
    old_stdin = sys.stdin
    try:
        sys.stdin = stdin
        with redirect_stdout(out), redirect_stderr(err):
            code, payload = planner.main(list(argv))
    finally:
        sys.stdin = old_stdin
    rendered = out.getvalue()
    parsed = json.loads(rendered)
    self_payload = json.loads(json.dumps(payload, sort_keys=True))
    assert parsed == self_payload
    return code, parsed, err.getvalue()


class HappyPathPlanTests(unittest.TestCase):
    def test_builds_plan_from_full_p2_19_to_p2_20_chain(self):
        gap_report = _gap_report(
            "tests/fixtures/security_headers_baseline/all_headers_absent/expected_findings.json",
            "tests/fixtures/candidate_review_packet/with_evidence/expected_findings.json",
            "tests/fixtures/candidate_review_packet/low_confidence/expected_findings.json",
            "tests/fixtures/candidate_review_packet/info_severity/expected_findings.json",
        )
        plan = _plan(gap_report)
        self.assertEqual(plan["status"], "ok", plan)
        self.assertEqual(plan["schema_version"], PLAN_SCHEMA_VERSION)
        self.assertEqual(plan["source_schema_version"], GAP_SCHEMA_VERSION)
        self.assertEqual(plan["errors"], [])
        self.assertEqual(plan["summary"]["finding_count"], len(gap_report["finding_gaps"]))
        self.assertGreater(plan["summary"]["blocked_count"], 0)
        self.assertGreater(plan["summary"]["needs_manual_review_count"], 0)
        self.assertGreater(plan["summary"]["check_item_count"], 0)
        self.assertEqual(
            sorted((item["finding_id"], item["target_value"], item["module_id"]) for item in plan["verification_plans"]),
            [(item["finding_id"], item["target_value"], item["module_id"]) for item in plan["verification_plans"]],
        )

    def test_reviewer_decision_required_without_gaps_gets_human_decision_check(self):
        gap_report = _minimal_gap_report([], "reviewer_decision_required")
        plan = _plan(gap_report)
        self.assertEqual(plan["status"], "ok")
        entry = plan["verification_plans"][0]
        self.assertEqual(entry["plan_state"], "needs_manual_review")
        self.assertEqual(entry["check_items"][0]["code"], "CHECK_REVIEWER_DECISION")
        self.assertIsNone(entry["check_items"][0]["source_gap_code"])

    def test_each_source_gap_code_maps_to_stable_check_code(self):
        expected = {
            "MISSING_EVIDENCE": "CHECK_MISSING_EVIDENCE",
            "LOW_CONFIDENCE": "CHECK_LOW_CONFIDENCE",
            "INFO_SEVERITY_REPORT_BLOCKED": "CHECK_INFO_SEVERITY_RATIONALE",
            "MANUAL_VERIFICATION_REQUIRED": "CHECK_MANUAL_VERIFICATION_NOTES",
            "SCANNER_OUTPUT_ONLY": "CHECK_NON_SCANNER_CORROBORATION",
            "MISSING_REMEDIATION": "CHECK_HUMAN_REMEDIATION_GUIDANCE",
            "MISSING_VERIFICATION_GUIDANCE": "CHECK_SAFE_MANUAL_CHECKLIST",
            "MISSING_SCOPE_REVIEW_QUESTION": "CHECK_SCOPE_REVIEW_QUESTION",
        }
        gap_report = _minimal_gap_report(list(GAP_CODES))
        plan = _plan(gap_report)
        item_codes = {item["source_gap_code"]: item["code"] for item in plan["verification_plans"][0]["check_items"]}
        self.assertEqual(item_codes, expected)
        self.assertEqual(list(item_codes.keys()), list(GAP_CODES))
        self.assertEqual(plan["summary"]["source_gap_code_counts"], {code: 1 for code in GAP_CODES})

    def test_deterministic_on_repeat(self):
        gap_report = _gap_report(
            "tests/fixtures/security_headers_baseline/weak_csp/expected_findings.json",
            "tests/fixtures/candidate_review_packet/low_confidence/expected_findings.json",
        )
        first = json.dumps(_plan(gap_report), sort_keys=True, separators=(",", ":"))
        second = json.dumps(_plan(gap_report), sort_keys=True, separators=(",", ":"))
        self.assertEqual(first, second)

    def test_output_does_not_use_promoted_state_words_as_json_values(self):
        plan = _plan(_minimal_gap_report(list(GAP_CODES)))
        for value in _all_values(plan):
            if isinstance(value, str):
                self.assertNotIn(value.lower(), FORBIDDEN_STATE_WORDS)


class ErrorContractTests(unittest.TestCase):
    def test_rejects_malformed_stdin_with_json_error(self):
        old_stdin = sys.stdin
        out = io.StringIO()
        err = io.StringIO()
        try:
            sys.stdin = io.StringIO("{not-json")
            with redirect_stdout(out), redirect_stderr(err):
                code, payload = planner.main([])
        finally:
            sys.stdin = old_stdin
        self.assertNotEqual(code, 0)
        parsed = json.loads(out.getvalue())
        self.assertEqual(parsed, payload)
        self.assertEqual(parsed["status"], "error")
        self.assertIn("INPUT_JSON_INVALID", [e["code"] for e in parsed["errors"]])
        self.assertEqual(err.getvalue(), "")

    def test_rejects_wrong_schema_status_and_source_errors(self):
        report = _minimal_gap_report()
        report["schema_version"] = "candidate_review_gap_report/999"
        plan = _plan(report)
        self.assertEqual(plan["status"], "error")
        self.assertIn("GAP_REPORT_SCHEMA_UNSUPPORTED", [e["code"] for e in plan["errors"]])

        report = _minimal_gap_report()
        report["status"] = "error"
        plan = _plan(report)
        self.assertEqual(plan["status"], "error")
        self.assertIn("GAP_REPORT_STATUS_NOT_OK", [e["code"] for e in plan["errors"]])

        report = _minimal_gap_report()
        report["errors"] = [{"code": "UPSTREAM", "path": "x", "message": "bad"}]
        plan = _plan(report)
        self.assertEqual(plan["status"], "error")
        self.assertIn("GAP_REPORT_ERRORS_PRESENT", [e["code"] for e in plan["errors"]])

    def test_rejects_non_object_missing_finding_gaps_and_bad_entries(self):
        self.assertIn("GAP_REPORT_NOT_OBJECT", [e["code"] for e in planner.build_plan([])["errors"]])

        report = _minimal_gap_report()
        report["finding_gaps"] = "bad"
        plan = _plan(report)
        self.assertIn("FINDING_GAPS_NOT_LIST", [e["code"] for e in plan["errors"]])

        report = _minimal_gap_report()
        report["finding_gaps"] = ["bad"]
        report["summary"]["gap_code_counts"] = {}
        plan = _plan(report)
        self.assertIn("FINDING_GAP_NOT_OBJECT", [e["code"] for e in plan["errors"]])

    def test_rejects_unknown_review_state_unknown_gap_duplicate_gap_and_mismatched_counts(self):
        report = _minimal_gap_report(["MISSING_EVIDENCE"], "later")
        plan = _plan(report)
        self.assertIn("REVIEW_STATE_UNSUPPORTED", [e["code"] for e in plan["errors"]])

        report = _minimal_gap_report(["MISSING_EVIDENCE"])
        report["finding_gaps"][0]["gap_codes"] = ["NEW_GAP"]
        report["summary"]["gap_code_counts"] = {}
        plan = _plan(report)
        self.assertIn("GAP_CODE_UNSUPPORTED", [e["code"] for e in plan["errors"]])

        report = _minimal_gap_report(["MISSING_EVIDENCE"])
        report["finding_gaps"][0]["gap_codes"] = ["MISSING_EVIDENCE", "MISSING_EVIDENCE"]
        report["summary"]["gap_code_counts"] = {"MISSING_EVIDENCE": 2}
        plan = _plan(report)
        self.assertIn("GAP_CODE_DUPLICATE", [e["code"] for e in plan["errors"]])

        report = _minimal_gap_report(["MISSING_EVIDENCE"])
        report["summary"]["gap_code_counts"] = {"MISSING_EVIDENCE": True}
        plan = _plan(report)
        self.assertIn("GAP_CODE_COUNT_INVALID", [e["code"] for e in plan["errors"]])

        report = _minimal_gap_report(["MISSING_EVIDENCE"])
        report["summary"]["gap_code_counts"] = {"MISSING_EVIDENCE": 2}
        plan = _plan(report)
        self.assertIn("GAP_CODE_COUNTS_MISMATCH", [e["code"] for e in plan["errors"]])

    def test_rejects_live_target_flags_and_positional_args(self):
        report = _minimal_gap_report()
        for flag in ("--target", "--target=example.invalid", "--url", "--host", "--scope", "--live"):
            with self.subTest(flag=flag):
                args = [flag] if flag in {"--live", "--target=example.invalid"} else [flag, "example.com"]
                code, parsed, err = _stdout_for(report, *args)
                self.assertNotEqual(code, 0)
                self.assertEqual(parsed["status"], "error")
                self.assertIn("LIVE_TARGET_FLAG_NOT_ALLOWED", [e["code"] for e in parsed["errors"]])
                self.assertEqual(err, "")

        code, parsed, err = _stdout_for(report, "unexpected-positional")
        self.assertNotEqual(code, 0)
        self.assertEqual(parsed["status"], "error")
        self.assertIn("ARGUMENT_NOT_ALLOWED", [e["code"] for e in parsed["errors"]])
        self.assertEqual(err, "")


class BoundaryTests(unittest.TestCase):
    def test_static_source_has_no_network_subprocess_file_or_runtime_primitives(self):
        source = PLAN_PATH.read_text(encoding="utf-8")
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
                        self.fail("open calls are not allowed in the P2.21 consumer")
                if isinstance(func, ast.Name):
                    self.assertNotIn(func.id, {"open", "exec", "eval", "compile"})

    def test_no_schema_promotion_file_exists(self):
        matches = list((ROOT / "modules" / "_schema").glob("*candidate_verification_plan*"))
        self.assertEqual(matches, [])

    def test_no_output_file_option_or_platform_drafting_terms(self):
        source = PLAN_PATH.read_text(encoding="utf-8").lower()
        for forbidden in ("--output", "--input", "--repo-root", "markdown", "html", "pdf", "platform adapter", "report draft"):
            self.assertNotIn(forbidden, source)


def _all_values(obj):
    if isinstance(obj, dict):
        for value in obj.values():
            yield from _all_values(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from _all_values(value)
    else:
        yield obj


if __name__ == "__main__":
    unittest.main()
