"""Focused tests for Phase 4A lab workflow runner."""

from __future__ import annotations

import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "scripts" / "phase4a_lab_workflow.py"
SCHEMA_VERSION = "phase4a_lab_workflow/0.1-trial"


def _load_runner():
    spec = importlib.util.spec_from_file_location("phase4a_lab_workflow_under_test", RUNNER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


runner = _load_runner()


def _stdout_for(*argv: str) -> tuple[int, dict, str]:
    out = io.StringIO()
    err = io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code, payload = runner.main(list(argv))
    rendered = out.getvalue()
    parsed = json.loads(rendered)
    self_payload = json.loads(json.dumps(payload, sort_keys=True))
    assert parsed == self_payload
    return code, parsed, err.getvalue()


class Phase4ALabWorkflowTests(unittest.TestCase):
    def test_fails_closed_without_explicit_lab_mode(self):
        code, payload, stderr = _stdout_for(
            "--repo-root",
            str(ROOT),
            "--target-url",
            "http://<lab-ip>:3000",
            "--input",
            "tests/fixtures/candidate_review_packet/with_evidence/expected_findings.json",
        )
        self.assertEqual(code, 2)
        self.assertEqual(stderr, "")
        self.assertEqual(payload["schema_version"], SCHEMA_VERSION)
        self.assertEqual(payload["status"], "error")
        self.assertEqual(payload["artifacts"], {})
        self.assertEqual(payload["errors"][0]["code"], "LAB_MODE_REQUIRED")

    def test_rejects_public_targets_even_with_lab_mode(self):
        for target in ("https://example.com", "http://8.8.8.8:3000"):
            with self.subTest(target=target):
                code, payload, stderr = _stdout_for(
                    "--repo-root",
                    str(ROOT),
                    "--lab-mode",
                    "--target-url",
                    target,
                    "--input",
                    "tests/fixtures/candidate_review_packet/with_evidence/expected_findings.json",
                )
                self.assertEqual(code, 2)
                self.assertEqual(stderr, "")
                self.assertEqual(payload["errors"][0]["code"], "TARGET_NOT_LOCAL_LAB")
                self.assertEqual(payload["artifacts"], {})

    def test_builds_fixed_recon_review_script_selection_candidate_gate_chain(self):
        payload = runner.build_lab_workflow(
            repo_root=ROOT,
            target_url="http://<lab-ip>:3000",
            inputs=[
                "tests/fixtures/candidate_review_packet/with_evidence/expected_findings.json",
                "tests/fixtures/candidate_review_packet/info_severity/expected_findings.json",
            ],
            intensity="active",
        )
        self.assertEqual(payload["status"], "ok", payload)
        self.assertEqual(payload["schema_version"], SCHEMA_VERSION)
        self.assertEqual(payload["target"]["url"], "http://<lab-ip>:3000")
        self.assertEqual(payload["run_mode"], "plan_only")
        self.assertEqual(payload["summary"]["input_count"], 2)
        self.assertEqual(
            payload["stage_order"],
            [
                "scope_gate",
                "baseline_recon",
                "model_review_script_selection",
                "active_script_plan",
                "candidate_review_packet",
                "candidate_review_gap_report",
                "candidate_verification_plan",
                "report_readiness_gate",
                "lab_report_draft_plan",
            ],
        )
        plan_ids = [entry["id"] for entry in payload["artifacts"]["active_script_plan"]["steps"]]
        self.assertIn("headers_audit", plan_ids)
        self.assertIn("cors_audit", plan_ids)
        self.assertIn("nikto_bounded", plan_ids)
        self.assertIn("ftp_metadata_only", plan_ids)
        self.assertEqual(payload["artifacts"]["candidate_review_packet"]["status"], "ok")
        self.assertEqual(payload["artifacts"]["report_readiness_gate"]["status"], "ok")
        gate_states = {
            item["gate_state"] for item in payload["artifacts"]["report_readiness_gate"]["gate_results"]
        }
        self.assertTrue(gate_states.issubset({"blocked", "needs_manual_review"}))

    def test_max_lab_plan_contains_bounded_offensive_steps_but_no_destructive_or_loot_actions(self):
        payload = runner.build_lab_workflow(
            repo_root=ROOT,
            target_url="http://<lab-ip>:3000",
            inputs=["tests/fixtures/candidate_review_packet/with_evidence/expected_findings.json"],
            intensity="max-lab",
        )
        self.assertEqual(payload["status"], "ok", payload)
        plan = payload["artifacts"]["active_script_plan"]
        plan_ids = [entry["id"] for entry in plan["steps"]]
        self.assertIn("xss_marker_triage", plan_ids)
        self.assertIn("sqli_error_triage", plan_ids)
        self.assertEqual(plan["execution_default"], "plan_only")
        rendered_commands = "\n".join(entry["command"] for entry in plan["steps"]).lower()
        for forbidden in ("--dump", "os-shell", "--risk=3", "--level=5", "bruteforce", "recursive download", "interactsh", "oast"):
            self.assertNotIn(forbidden, rendered_commands)
        self.assertIn("no recursive download", "\n".join(plan["safety_limits"]).lower())

    def test_cli_can_write_all_artifacts_to_explicit_output_dir_without_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, payload, stderr = _stdout_for(
                "--repo-root",
                str(ROOT),
                "--lab-mode",
                "--target-url",
                "http://<lab-ip>:3000",
                "--intensity",
                "max-lab",
                "--input",
                "tests/fixtures/candidate_review_packet/with_evidence/expected_findings.json",
                "--output-dir",
                tmp,
            )
            self.assertEqual(code, 0, payload)
            self.assertEqual(stderr, "")
            out_dir = Path(tmp)
            for name in (
                "workflow.json",
                "script_plan.json",
                "candidate_review_packet.json",
                "candidate_gap_report.json",
                "candidate_verification_plan.json",
                "report_readiness_gate.json",
                "lab_report_draft_plan.md",
            ):
                self.assertTrue((out_dir / name).is_file(), name)
            self.assertEqual(payload["run_mode"], "plan_only")


if __name__ == "__main__":
    unittest.main()
