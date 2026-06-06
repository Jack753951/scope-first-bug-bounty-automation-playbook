"""Focused tests for the offline Wave 1A candidate-review bridge."""

from __future__ import annotations

import importlib.util
import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "build_wave1a_candidate_review_fixture.py"


def load_module():
    spec = importlib.util.spec_from_file_location("wave1a_candidate_bridge_under_test", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


class Wave1ACandidateReviewBridgeTests(unittest.TestCase):
    def test_builds_non_promotional_findings_and_candidate_review_packet_from_wave1a_seeds(self):
        module = load_module()

        result = module.build_bridge(
            REPO_ROOT,
            "tests/fixtures/wave1a_metadata/observations_sample.jsonl",
            run_id="unit-wave1a-bridge",
        )

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["schema_version"], "wave1a_candidate_review_bridge/0.1-trial")
        self.assertEqual(result["summary"]["candidate_seed_count"], 2)
        self.assertEqual(result["summary"]["finding_fixture_count"], 2)
        self.assertEqual(result["summary"]["candidate_review_packet_count"], 2)
        findings = result["finding_fixture"]
        self.assertEqual({finding["status"] for finding in findings}, {"candidate"})
        self.assertTrue(all(finding["schema_version"] == "finding/1.0" for finding in findings))
        self.assertTrue(all(finding["triage"]["scanner_output_only"] for finding in findings))
        self.assertTrue(all(finding["triage"]["manual_verification_required"] for finding in findings))
        self.assertTrue(all(finding["evidence"] == [] for finding in findings))
        self.assertEqual(
            [finding["target"]["value"] for finding in findings],
            ["http://<lab-ip>:3000/api-docs/", "http://<lab-ip>:3000/ftp/"],
        )
        packet = result["candidate_review_packet"]
        self.assertEqual(packet["status"], "ok")
        self.assertEqual(packet["schema_version"], "candidate_review_packet/0.1-trial")
        self.assertEqual(packet["summary"]["candidate_count"], 2)
        self.assertTrue(all(item["report_readiness"] == "not_ready" for item in packet["findings"]))
        self.assertTrue(all(item["scanner_output_only"] for item in packet["findings"]))
        self.assertTrue(all(item["manual_verification_required"] for item in packet["findings"]))
        forbidden = {"confirmed", "verified", "reportable", "accepted"}
        self.assertFalse(forbidden.intersection(json.dumps(result).lower().split('"')))

    def test_bridge_does_not_perform_network_subprocess_or_file_writes_by_default(self):
        module = load_module()
        with patch("subprocess.run", side_effect=AssertionError("must not execute subprocess")), patch(
            "urllib.request.urlopen", side_effect=AssertionError("must not perform network I/O")
        ), patch("pathlib.Path.write_text", side_effect=AssertionError("default bridge must not write files")):
            result = module.build_bridge(
                REPO_ROOT,
                "tests/fixtures/wave1a_metadata/observations_sample.jsonl",
                run_id="unit-wave1a-bridge-safety",
            )
        self.assertEqual(result["status"], "ok")
        self.assertFalse(result["safety"]["network_io"])
        self.assertFalse(result["safety"]["subprocess_execution"])
        self.assertFalse(result["safety"]["target_touching"])
        self.assertFalse(result["safety"]["output_file_write"])
        self.assertFalse(result["safety"]["promotes_findings"])

    def test_malformed_import_input_fails_closed_without_packet_or_findings(self):
        module = load_module()
        result = module.build_bridge(
            REPO_ROOT,
            "tests/fixtures/wave1a_metadata/malformed_observations.jsonl",
            run_id="unit-wave1a-bridge-malformed",
        )
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["summary"]["finding_fixture_count"], 0)
        self.assertEqual(result["finding_fixture"], [])
        self.assertEqual(result["candidate_review_packet"], {})
        self.assertEqual(result["errors"][0]["code"], "IMPORTER_STAGE_FAILED")

    def test_cli_rejects_live_target_flags_with_json_error(self):
        module = load_module()
        out = io.StringIO()
        with redirect_stdout(out):
            code = module.main([
                "--repo-root", str(REPO_ROOT),
                "--input", "tests/fixtures/wave1a_metadata/observations_sample.jsonl",
                "--target", "https://example.com",
            ])
        self.assertEqual(code, 2)
        payload = json.loads(out.getvalue())
        self.assertEqual(payload["status"], "error")
        self.assertEqual(payload["errors"][0]["code"], "LIVE_TARGET_FLAG_NOT_ALLOWED")
        self.assertEqual(payload["finding_fixture"], [])
        self.assertEqual(payload["candidate_review_packet"], {})


if __name__ == "__main__":
    unittest.main()
