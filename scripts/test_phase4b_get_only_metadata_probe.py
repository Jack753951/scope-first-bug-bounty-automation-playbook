"""Tests for Phase 4B GET-only lab fast-lane adapter."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "lab_modules" / "phase4b_get_only_metadata_probe.py"


def load_module():
    spec = importlib.util.spec_from_file_location("phase4b_get_only_under_test", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


class Phase4BGetOnlyMetadataProbeTests(unittest.TestCase):
    def test_plan_uses_lab_fast_lane_get_only_paths_with_health_gates(self):
        module = load_module()
        plan = module.build_plan(
            target_url="http://<lab-ip>:3000/",
            output_dir="/home/kali/codex-output/phase4b_fast_lane_example",
            request_cap=40,
            timeout=5,
            rate_limit=2,
            lab_approved=False,
        )

        self.assertEqual(plan["status"], "ok")
        self.assertEqual(plan["schema_version"], "phase4b_get_only_metadata_probe/0.1-trial")
        self.assertEqual(plan["run_mode"], "plan_only")
        self.assertEqual(plan["steps"][0]["id"], "pre_health")
        self.assertEqual(plan["steps"][-1]["id"], "post_health")
        self.assertLessEqual(plan["limits"]["planned_requests"], plan["limits"]["request_cap"])
        self.assertIn("observations.jsonl", plan["outputs"])
        self.assertTrue(plan["safety"]["lab_fast_lane"])
        self.assertTrue(plan["safety"]["get_only"])
        self.assertFalse(plan["safety"]["head_requests"])
        self.assertFalse(plan["safety"]["raw_body_persistence"])

        step_methods = {step.get("method") for step in plan["steps"] if step["kind"] != "health"}
        self.assertEqual(step_methods, {"GET"})
        paths = [step["path"] for step in plan["steps"] if "path" in step]
        self.assertEqual(paths, [
            "/",
            "/robots.txt",
            "/.well-known/security.txt",
            "/ftp/",
            "/api-docs/",
            "/rest/products/search?q=phase4b_canary",
            "/search?q=phase4b_canary",
            "/redirect?to=https://phase4b-canary.invalid/",
        ])

    def test_rejects_public_targets_and_unsafe_fast_lane_limits(self):
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

        high_cap_result = module.build_plan(
            target_url="http://<lab-ip>:3000/",
            output_dir="/tmp/out",
            request_cap=101,
            timeout=5,
            rate_limit=2,
        )
        self.assertEqual(high_cap_result["status"], "error")
        self.assertEqual(high_cap_result["errors"][0]["code"], "REQUEST_CAP_OUT_OF_RANGE")

    def test_rendered_script_has_no_head_crawler_scanner_or_promotion_vocabulary(self):
        module = load_module()
        plan = module.build_plan(
            target_url="http://<lab-ip>:3000/",
            output_dir="/home/kali/codex-output/phase4b_fast_lane_example",
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
        self.assertIn("--max-time 5", script)
        self.assertIn("--max-filesize", script)
        self.assertIn("sleep 0.5", script)
        self.assertIn("promotes_findings", script)
        self.assertNotIn(" -i ", lower)
        self.assertNotIn("--head", lower)
        for forbidden in (
            "sqlmap", "hydra", "msfconsole", "metasploit", "interactsh", "oast",
            "dalfox", "kxss", "gau ", "ffuf", "gobuster", "nuclei", "--recursive",
            "confirmed", "verified", "reportable", "ready_for_submission", "accepted",
            "etc/passwd", "shadow", "--dump", "os-shell",
        ):
            self.assertNotIn(forbidden, lower)

    def test_cli_requires_lab_approval_before_writing_script(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            script_path = Path(tmp) / "phase4b_get_only.sh"
            code = module.main([
                "--target-url", "http://<lab-ip>:3000/",
                "--output-dir", "/home/kali/codex-output/phase4b_fast_lane_example",
                "--write-script", str(script_path),
            ])
            self.assertEqual(code, 2)
            self.assertFalse(script_path.exists())

            code = module.main([
                "--target-url", "http://<lab-ip>:3000/",
                "--output-dir", "/home/kali/codex-output/phase4b_fast_lane_example",
                "--write-script", str(script_path),
                "--lab-approved",
            ])
            self.assertEqual(code, 0)
            content = script_path.read_text(encoding="utf-8")
            self.assertIn("set -euo pipefail", content)
            self.assertIn("record_get", content)
            self.assertIn("observations.jsonl", content)


if __name__ == "__main__":
    unittest.main()
