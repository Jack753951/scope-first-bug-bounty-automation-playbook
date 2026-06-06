"""Tests for Phase 4B Wave2 benign parameter lab adapter."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "lab_modules" / "wave2_benign_params.py"


def load_module():
    spec = importlib.util.spec_from_file_location("wave2_benign_params_under_test", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


class Wave2BenignParamsTests(unittest.TestCase):
    def test_plan_uses_inert_canaries_and_health_gates(self):
        module = load_module()
        plan = module.build_plan(
            target_url="http://<lab-ip>:3000/",
            output_dir="/home/kali/codex-output/wave2_example",
            request_cap=40,
            timeout=5,
            rate_limit=2,
            lab_approved=False,
        )

        self.assertEqual(plan["status"], "ok")
        self.assertEqual(plan["schema_version"], "phase4b_wave2_benign_params/0.1-trial")
        self.assertEqual(plan["run_mode"], "plan_only")
        self.assertEqual(plan["steps"][0]["id"], "pre_health")
        self.assertEqual(plan["steps"][-1]["id"], "post_health")
        self.assertLessEqual(plan["limits"]["planned_requests"], plan["limits"]["request_cap"])
        self.assertTrue(plan["safety"]["inert_canaries_only"])
        self.assertFalse(plan["safety"]["executable_payloads"])
        self.assertFalse(plan["safety"]["crawler_execution"])
        self.assertFalse(plan["safety"]["redirect_following"])

        active_steps = [step for step in plan["steps"] if step["kind"] != "health"]
        self.assertEqual({step["method"] for step in active_steps}, {"GET"})
        self.assertEqual({step["kind"] for step in active_steps}, {"benign_parameter_probe"})
        urls = "\n".join(step["url"] for step in active_steps)
        self.assertIn("PHASE4B_REFLECT_CANARY", urls)
        self.assertIn("phase4b-canary.invalid", urls)
        self.assertNotIn("<script", urls.lower())
        self.assertNotIn("javascript:", urls.lower())

    def test_rejects_public_targets_and_unsafe_limits(self):
        module = load_module()
        public_result = module.build_plan(
            target_url="https://example.com/",
            output_dir="/tmp/out",
            request_cap=40,
            timeout=5,
            rate_limit=2,
        )
        self.assertEqual(public_result["status"], "error")
        self.assertEqual(public_result["errors"][0]["code"], "TARGET_NOT_FAST_LANE_LAB")

        fast_result = module.build_plan(
            target_url="http://<lab-ip>:3000/",
            output_dir="/tmp/out",
            request_cap=40,
            timeout=5,
            rate_limit=3,
        )
        self.assertEqual(fast_result["status"], "error")
        self.assertEqual(fast_result["errors"][0]["code"], "RATE_LIMIT_OUT_OF_RANGE")

    def test_rendered_script_has_no_scanner_payload_or_promotion_terms(self):
        module = load_module()
        plan = module.build_plan(
            target_url="http://<lab-ip>:3000/",
            output_dir="/home/kali/codex-output/wave2_example",
            request_cap=40,
            timeout=5,
            rate_limit=2,
            lab_approved=True,
        )
        script = module.render_bash(plan)
        lower = script.lower()

        self.assertIn("observations.jsonl", script)
        self.assertIn("pre_health.txt", script)
        self.assertIn("post_health.txt", script)
        self.assertIn("--max-redirs 0", script)
        self.assertIn("PHASE4B_REFLECT_CANARY", script)
        self.assertIn("phase4b-canary.invalid", script)
        self.assertIn("manual_verification_required", script)
        for forbidden in (
            "sqlmap", "hydra", "msfconsole", "metasploit", "interactsh", "oast",
            "dalfox", "kxss", "gau ", "ffuf", "gobuster", "nuclei", "--recursive",
            "<script", "javascript:", "onerror", "document.cookie", "alert(",
            "confirmed", "verified", "reportable", "ready_for_submission", "accepted",
            "etc/passwd", "shadow", "--dump", "os-shell",
        ):
            self.assertNotIn(forbidden, lower)

    def test_cli_requires_lab_approval_before_writing_script(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            script_path = Path(tmp) / "wave2_benign.sh"
            code = module.main([
                "--target-url", "http://<lab-ip>:3000/",
                "--output-dir", "/home/kali/codex-output/wave2_example",
                "--write-script", str(script_path),
            ])
            self.assertEqual(code, 2)
            self.assertFalse(script_path.exists())

            code = module.main([
                "--target-url", "http://<lab-ip>:3000/",
                "--output-dir", "/home/kali/codex-output/wave2_example",
                "--write-script", str(script_path),
                "--lab-approved",
            ])
            self.assertEqual(code, 0)
            content = script_path.read_text(encoding="utf-8")
            self.assertIn("set -euo pipefail", content)
            self.assertIn("record_probe", content)
            self.assertIn("observations.jsonl", content)


if __name__ == "__main__":
    unittest.main()
