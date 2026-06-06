"""Focused tests for the offline Wave 1A review-chain bridge."""

from __future__ import annotations

import ast
import importlib.util
import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "build_wave1a_review_chain.py"
SCHEMA_VERSION = "wave1a_review_chain/0.1-trial"
FIXTURE_INPUT = "tests/fixtures/wave1a_metadata/observations_sample.jsonl"
MALFORMED_INPUT = "tests/fixtures/wave1a_metadata/malformed_observations.jsonl"
FORBIDDEN_VALUES = {"confirmed", "verified", "reportable", "accepted", "ready_for_submission"}


def load_module():
    spec = importlib.util.spec_from_file_location("wave1a_review_chain_under_test", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def all_string_values(value):
    if isinstance(value, dict):
        for child in value.values():
            yield from all_string_values(child)
    elif isinstance(value, list):
        for child in value:
            yield from all_string_values(child)
    elif isinstance(value, str):
        yield value


class Wave1AReviewChainTests(unittest.TestCase):
    def test_builds_gap_plan_and_gate_from_wave1a_candidate_review_packet(self):
        module = load_module()

        payload = module.build_review_chain(REPO_ROOT, FIXTURE_INPUT, run_id="unit-wave1a-chain")

        self.assertEqual(payload["status"], "ok", payload)
        self.assertEqual(payload["schema_version"], SCHEMA_VERSION)
        self.assertEqual(payload["errors"], [])
        self.assertEqual(
            payload["source_schema_versions"],
            [
                "wave1a_candidate_review_bridge/0.1-trial",
                "candidate_review_packet/0.1-trial",
                "candidate_review_gap_report/0.1-trial",
                "candidate_verification_plan/0.1-trial",
                "report_readiness_gate/0.1-trial",
            ],
        )
        self.assertEqual(payload["summary"]["candidate_seed_count"], 2)
        self.assertEqual(payload["summary"]["candidate_count"], 2)
        self.assertEqual(payload["summary"]["gap_finding_count"], 2)
        self.assertEqual(payload["summary"]["verification_plan_count"], 2)
        self.assertEqual(payload["summary"]["gate_result_count"], 2)
        artifacts = payload["artifacts"]
        self.assertEqual(artifacts["candidate_review_bridge"]["status"], "ok")
        self.assertEqual(artifacts["candidate_review_packet"]["status"], "ok")
        self.assertEqual(artifacts["candidate_review_gap_report"]["status"], "ok")
        self.assertEqual(artifacts["candidate_verification_plan"]["status"], "ok")
        self.assertEqual(artifacts["report_readiness_gate"]["status"], "ok")

        packet_targets = {entry["target"]["value"]: entry for entry in artifacts["candidate_review_packet"]["findings"]}
        self.assertIn("http://<lab-ip>:3000/api-docs/", packet_targets)
        self.assertIn("http://<lab-ip>:3000/ftp/", packet_targets)
        self.assertTrue(all(entry["status"] == "candidate" for entry in packet_targets.values()))
        self.assertTrue(all(entry["report_readiness"] == "not_ready" for entry in packet_targets.values()))
        self.assertTrue(all(entry["manual_verification_required"] for entry in packet_targets.values()))
        self.assertTrue(all(entry["scanner_output_only"] for entry in packet_targets.values()))

        plan_states = {entry["plan_state"] for entry in artifacts["candidate_verification_plan"]["verification_plans"]}
        gate_states = {entry["gate_state"] for entry in artifacts["report_readiness_gate"]["gate_results"]}
        self.assertEqual(plan_states, {"blocked"})
        self.assertEqual(gate_states, {"blocked"})
        values = {value.lower() for value in all_string_values(payload)}
        self.assertFalse(FORBIDDEN_VALUES & values)

    def test_malformed_importer_input_fails_closed_before_gap_plan_or_gate(self):
        module = load_module()

        payload = module.build_review_chain(REPO_ROOT, MALFORMED_INPUT, run_id="unit-wave1a-chain-bad")

        self.assertEqual(payload["status"], "error")
        self.assertEqual(payload["summary"]["candidate_count"], 0)
        self.assertEqual(payload["errors"][0]["code"], "REVIEW_CHAIN_STAGE_FAILED")
        self.assertEqual(payload["errors"][0]["stage"], "candidate_review_bridge")
        self.assertIn("candidate_review_bridge", payload["artifacts"])
        self.assertNotIn("candidate_review_packet", payload["artifacts"])
        self.assertNotIn("candidate_review_gap_report", payload["artifacts"])
        self.assertNotIn("candidate_verification_plan", payload["artifacts"])
        self.assertNotIn("report_readiness_gate", payload["artifacts"])

    def test_packet_stage_failure_stops_before_later_review_stages(self):
        module = load_module()
        failed_bridge = {
            "schema_version": "wave1a_candidate_review_bridge/0.1-trial",
            "status": "error",
            "summary": {"candidate_seed_count": 0, "finding_fixture_count": 0, "candidate_review_packet_count": 0},
            "candidate_review_packet": {},
            "errors": [{"code": "CANDIDATE_PACKET_STAGE_FAILED", "path": "candidate_review_packet", "message": "failed"}],
            "safety": {"network_io": False, "subprocess_execution": False, "target_touching": False, "output_file_write": False},
        }
        with patch.object(module._bridge(), "build_bridge", return_value=failed_bridge):
            payload = module.build_review_chain(REPO_ROOT, FIXTURE_INPUT, run_id="unit-wave1a-chain-packet-fail")

        self.assertEqual(payload["status"], "error")
        self.assertEqual(payload["errors"][0]["stage"], "candidate_review_bridge")
        self.assertIn("candidate_review_bridge", payload["artifacts"])
        self.assertNotIn("candidate_review_packet", payload["artifacts"])
        self.assertNotIn("candidate_review_gap_report", payload["artifacts"])
        self.assertNotIn("candidate_verification_plan", payload["artifacts"])
        self.assertNotIn("report_readiness_gate", payload["artifacts"])

    def test_review_chain_does_not_perform_network_subprocess_or_file_writes(self):
        module = load_module()
        with patch("subprocess.run", side_effect=AssertionError("must not execute subprocess")), patch(
            "urllib.request.urlopen", side_effect=AssertionError("must not perform network I/O")
        ), patch("pathlib.Path.write_text", side_effect=AssertionError("default chain must not write files")):
            payload = module.build_review_chain(REPO_ROOT, FIXTURE_INPUT, run_id="unit-wave1a-chain-safety")

        self.assertEqual(payload["status"], "ok")
        self.assertFalse(payload["safety"]["network_io"])
        self.assertFalse(payload["safety"]["subprocess_execution"])
        self.assertFalse(payload["safety"]["target_touching"])
        self.assertFalse(payload["safety"]["output_file_write"])
        self.assertFalse(payload["safety"]["promotes_findings"])
        self.assertFalse(payload["safety"]["report_drafting"])
        self.assertFalse(payload["safety"]["report_submission"])

    def test_cli_emits_json_and_rejects_live_target_flags(self):
        module = load_module()
        out = io.StringIO()
        with redirect_stdout(out):
            code = module.main([
                "--repo-root", str(REPO_ROOT),
                "--input", FIXTURE_INPUT,
                "--target", "https://example.com",
            ])
        self.assertEqual(code, 2)
        payload = json.loads(out.getvalue())
        self.assertEqual(payload["status"], "error")
        self.assertEqual(payload["schema_version"], SCHEMA_VERSION)
        self.assertEqual(payload["errors"][0]["code"], "LIVE_TARGET_FLAG_NOT_ALLOWED")
        self.assertEqual(payload["artifacts"], {})


class StaticSafetyTests(unittest.TestCase):
    def test_script_has_no_network_subprocess_or_file_write_imports(self):
        tree = ast.parse(SCRIPT_PATH.read_text(encoding="utf-8"))
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
