"""Focused tests for P2.20 candidate review packet gap report consumer."""

from __future__ import annotations

import ast
import importlib.util
import io
import json
import os
import sys
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONSUMER_PATH = ROOT / "scripts" / "review_candidate_packet_gaps.py"
BUILDER_PATH = ROOT / "scripts" / "build_candidate_review_packet.py"
SCHEMA_VERSION = "candidate_review_gap_report/0.1-trial"
SOURCE_SCHEMA_VERSION = "candidate_review_packet/0.1-trial"
FORBIDDEN_OUTPUT_WORDS = {"ready", "approved", "confirmed", "verified", "accepted"}


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


consumer = _load(CONSUMER_PATH, "review_candidate_packet_gaps_under_test")
builder = _load(BUILDER_PATH, "build_candidate_review_packet_for_gap_tests")


def _packet(*inputs: str) -> dict:
    return builder.build_packet(str(ROOT), list(inputs))


def _review(packet: dict) -> dict:
    return consumer.review_packet(packet)


def _stdout_for(packet: dict, *argv: str) -> tuple[int, dict, str]:
    stdin = io.StringIO(json.dumps(packet, sort_keys=True))
    out = io.StringIO()
    err = io.StringIO()
    old_stdin = sys.stdin
    try:
        sys.stdin = stdin
        with redirect_stdout(out), redirect_stderr(err):
            code, payload = consumer.main(list(argv))
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


class HappyPathGapTests(unittest.TestCase):
    def test_generates_gap_report_from_p2_19_packet(self):
        packet = _packet(
            "tests/fixtures/security_headers_baseline/all_headers_absent/expected_findings.json",
            "tests/fixtures/candidate_review_packet/with_evidence/expected_findings.json",
            "tests/fixtures/candidate_review_packet/low_confidence/expected_findings.json",
            "tests/fixtures/candidate_review_packet/info_severity/expected_findings.json",
        )
        report = _review(packet)
        self.assertEqual(report["status"], "ok", report)
        self.assertEqual(report["schema_version"], SCHEMA_VERSION)
        self.assertEqual(report["source_schema_version"], SOURCE_SCHEMA_VERSION)
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["summary"]["finding_count"], len(packet["findings"]))
        self.assertGreater(report["summary"]["not_ready_count"], 0)
        self.assertGreater(report["summary"]["reviewer_decision_required_count"], 0)
        codes = report["summary"]["gap_code_counts"]
        self.assertGreater(codes["MISSING_EVIDENCE"], 0)
        self.assertGreater(codes["LOW_CONFIDENCE"], 0)
        self.assertGreater(codes["INFO_SEVERITY_REPORT_BLOCKED"], 0)
        self.assertEqual(
            sorted((item["finding_id"], item["target_value"]) for item in report["finding_gaps"]),
            [(item["finding_id"], item["target_value"]) for item in report["finding_gaps"]],
        )

    def test_with_evidence_can_reach_reviewer_decision_required_but_never_ready(self):
        packet = _packet("tests/fixtures/candidate_review_packet/with_evidence/expected_findings.json")
        report = _review(packet)
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["summary"]["reviewer_decision_required_count"], 1)
        self.assertEqual(report["finding_gaps"][0]["review_state"], "reviewer_decision_required")
        blob = json.dumps(report, sort_keys=True).lower()
        for forbidden in FORBIDDEN_OUTPUT_WORDS:
            self.assertNotIn(f'"{forbidden}"', blob)

    def test_deterministic_on_repeat(self):
        packet = _packet(
            "tests/fixtures/security_headers_baseline/weak_csp/expected_findings.json",
            "tests/fixtures/candidate_review_packet/low_confidence/expected_findings.json",
        )
        first = json.dumps(_review(packet), sort_keys=True, separators=(",", ":"))
        second = json.dumps(_review(packet), sort_keys=True, separators=(",", ":"))
        self.assertEqual(first, second)


class ErrorContractTests(unittest.TestCase):
    def test_rejects_malformed_stdin_with_json_error(self):
        old_stdin = sys.stdin
        out = io.StringIO()
        err = io.StringIO()
        try:
            sys.stdin = io.StringIO("{not-json")
            with redirect_stdout(out), redirect_stderr(err):
                code, payload = consumer.main([])
        finally:
            sys.stdin = old_stdin
        self.assertNotEqual(code, 0)
        parsed = json.loads(out.getvalue())
        self.assertEqual(parsed, payload)
        self.assertEqual(parsed["status"], "error")
        self.assertIn("INPUT_JSON_INVALID", [e["code"] for e in parsed["errors"]])
        self.assertEqual(err.getvalue(), "")

    def test_rejects_wrong_schema_and_packet_errors(self):
        packet = _packet("tests/fixtures/security_headers_baseline/weak_csp/expected_findings.json")
        packet["schema_version"] = "candidate_review_packet/999"
        report = _review(packet)
        self.assertEqual(report["status"], "error")
        self.assertIn("PACKET_SCHEMA_UNSUPPORTED", [e["code"] for e in report["errors"]])

        packet = _packet("tests/fixtures/security_headers_baseline/weak_csp/expected_findings.json")
        packet["errors"] = [{"code": "UPSTREAM", "path": "x", "message": "bad"}]
        report = _review(packet)
        self.assertEqual(report["status"], "error")
        self.assertIn("PACKET_ERRORS_PRESENT", [e["code"] for e in report["errors"]])

    def test_rejects_packet_status_not_ok_and_forbidden_finding_status(self):
        packet = _packet("tests/fixtures/security_headers_baseline/weak_csp/expected_findings.json")
        packet["status"] = "error"
        report = _review(packet)
        self.assertEqual(report["status"], "error")
        self.assertIn("PACKET_STATUS_NOT_OK", [e["code"] for e in report["errors"]])

        packet = _packet("tests/fixtures/security_headers_baseline/weak_csp/expected_findings.json")
        packet["findings"][0]["status"] = "verified"
        report = _review(packet)
        self.assertEqual(report["status"], "error")
        self.assertIn("FINDING_STATUS_PROMOTED", [e["code"] for e in report["errors"]])

    def test_rejects_live_target_flags_with_json_error(self):
        packet = _packet("tests/fixtures/security_headers_baseline/weak_csp/expected_findings.json")
        for flag in ("--target", "--url", "--host", "--scope", "--live"):
            with self.subTest(flag=flag):
                args = [flag] if flag == "--live" else [flag, "example.com"]
                code, parsed, err = _stdout_for(packet, *args)
                self.assertNotEqual(code, 0)
                self.assertEqual(parsed["status"], "error")
                self.assertIn("LIVE_TARGET_FLAG_NOT_ALLOWED", [e["code"] for e in parsed["errors"]])
                self.assertEqual(err, "")

    def test_rejects_positional_argument_with_json_error(self):
        packet = _packet("tests/fixtures/security_headers_baseline/weak_csp/expected_findings.json")
        code, parsed, err = _stdout_for(packet, "unexpected-positional")
        self.assertNotEqual(code, 0)
        self.assertEqual(parsed["status"], "error")
        self.assertIn("ARGUMENT_NOT_ALLOWED", [e["code"] for e in parsed["errors"]])
        self.assertEqual(err, "")


class BoundaryTests(unittest.TestCase):
    def test_static_source_has_no_network_subprocess_or_write_primitives(self):
        source = CONSUMER_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source)
        forbidden_import_roots = {
            "socket", "http", "urllib", "requests", "httpx", "ssl", "subprocess",
            "asyncio", "selectors", "module_runner", "recon",
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
                    self.assertNotIn(func.attr, {"write_text", "write_bytes", "system", "popen"})
                    if func.attr == "open":
                        self.fail("open calls are not allowed in the P2.20 consumer")
                if isinstance(func, ast.Name):
                    self.assertNotIn(func.id, {"open", "exec", "eval", "compile"})

    def test_no_schema_promotion_file_exists(self):
        matches = list((ROOT / "modules" / "_schema").glob("*candidate_review_gap_report*"))
        self.assertEqual(matches, [])

    def test_no_output_file_option_or_report_draft_terms(self):
        source = CONSUMER_PATH.read_text(encoding="utf-8").lower()
        for forbidden in ("--output", "--input", "--repo-root", "markdown", "submission", "report draft", "approved"):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
