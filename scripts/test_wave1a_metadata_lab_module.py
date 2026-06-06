"""Focused tests for the reusable Wave 1A metadata lab module adapter."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "lab_modules" / "wave1a_metadata.py"


def load_module():
    spec = importlib.util.spec_from_file_location("wave1a_metadata_under_test", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


class Wave1AMetadataLabModuleTests(unittest.TestCase):
    def test_plan_only_selects_bounded_metadata_modules_with_health_gates(self):
        module = load_module()
        plan = module.build_plan(
            target_url="http://<lab-ip>:3000/",
            output_dir="/home/kali/wave1a/example",
            request_cap=24,
            timeout=5,
            rate_limit=2,
            lab_approved=False,
        )

        self.assertEqual(plan["status"], "ok")
        self.assertEqual(plan["run_mode"], "plan_only")
        self.assertEqual(plan["schema_version"], "wave1a_metadata_lab_plan/0.1-trial")
        self.assertEqual(plan["module_ids"], [
            "level1.directory_listing_metadata",
            "level1.robots_securitytxt_metadata",
            "level1.api_docs_metadata",
            "level1.dependency_manifest_metadata",
            "level1.cors_metadata",
        ])
        self.assertLessEqual(plan["limits"]["request_cap"], 24)
        self.assertEqual(plan["steps"][0]["id"], "pre_health")
        self.assertEqual(plan["steps"][-1]["id"], "post_health")
        self.assertIn("observations.jsonl", plan["outputs"])

    def test_rendered_script_uses_known_paths_jsonl_and_no_exploit_or_download_behavior(self):
        module = load_module()
        plan = module.build_plan(
            target_url="http://<lab-ip>:3000/",
            output_dir="/home/kali/wave1a/example",
            request_cap=24,
            timeout=5,
            rate_limit=2,
            lab_approved=True,
        )
        script = module.render_bash(plan)
        lower = script.lower()

        for expected in ("/robots.txt", "/.well-known/security.txt", "/ftp/", "/api-docs/", "/rest/products/search"):
            self.assertIn(expected, script)
        self.assertIn("observations.jsonl", script)
        self.assertIn("pre_health.txt", script)
        self.assertIn("post_health.txt", script)
        self.assertIn("origin: https://example.invalid", lower)
        self.assertIn("--max-time 5", script)
        self.assertIn("sleep 0.5", script)
        for forbidden in (
            "sqlmap", "hydra", "metasploit", "msfconsole", "interactsh", "oast",
            "--recursive", "-recursion", "wget", "curl -o", "curl --output", "download",
            "confirmed", "verified", "reportable", "accepted",
        ):
            self.assertNotIn(forbidden, lower)

    def test_rejects_public_targets_and_unsafe_limits(self):
        module = load_module()
        public_result = module.build_plan(
            target_url="https://example.com/",
            output_dir="/tmp/out",
            request_cap=24,
            timeout=5,
            rate_limit=2,
        )
        self.assertEqual(public_result["status"], "error")
        self.assertEqual(public_result["errors"][0]["code"], "TARGET_NOT_LOCAL_LAB")

        high_cap_result = module.build_plan(
            target_url="http://<lab-ip>:3000/",
            output_dir="/tmp/out",
            request_cap=100,
            timeout=5,
            rate_limit=2,
        )
        self.assertEqual(high_cap_result["status"], "error")
        self.assertEqual(high_cap_result["errors"][0]["code"], "REQUEST_CAP_OUT_OF_RANGE")

    def test_cli_requires_lab_approval_before_writing_script(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            script_path = Path(tmp) / "wave1a.sh"
            code = module.main([
                "--target-url", "http://<lab-ip>:3000/",
                "--output-dir", "/home/kali/wave1a/example",
                "--write-script", str(script_path),
            ])
            self.assertEqual(code, 2)
            self.assertFalse(script_path.exists())

            code = module.main([
                "--target-url", "http://<lab-ip>:3000/",
                "--output-dir", "/home/kali/wave1a/example",
                "--write-script", str(script_path),
                "--lab-approved",
            ])
            self.assertEqual(code, 0)
            self.assertTrue(script_path.exists())
            content = script_path.read_text(encoding="utf-8")
            self.assertIn("set -euo pipefail", content)
            self.assertIn("observations.jsonl", content)


if __name__ == "__main__":
    unittest.main()
