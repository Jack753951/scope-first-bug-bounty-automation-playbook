"""Tests for bounded /ftp/ filename content-class verifier."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "lab_modules" / "ftp_filename_content_class_verifier.py"


def load_module():
    spec = importlib.util.spec_from_file_location("ftp_filename_content_class_verifier_under_test", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


class FtpFilenameContentClassVerifierTests(unittest.TestCase):
    def test_plan_is_ftp_only_bounded_and_health_gated(self):
        module = load_module()
        plan = module.build_plan(
            target_url="http://<lab-ip>:3000/",
            output_dir="/home/kali/codex-output/ftp_filename_example",
            candidate_path="/ftp/",
            request_cap=20,
            timeout=5,
            rate_limit=2,
            lab_approved=False,
        )

        self.assertEqual(plan["status"], "ok")
        self.assertEqual(plan["schema_version"], "ftp_filename_content_class_verifier/0.1-trial")
        self.assertEqual(plan["run_mode"], "plan_only")
        self.assertEqual(plan["steps"][0]["id"], "pre_health")
        self.assertEqual(plan["steps"][-1]["id"], "post_health")
        self.assertEqual([s["path"] for s in plan["steps"] if "path" in s], ["/ftp/"])
        self.assertLessEqual(plan["limits"]["planned_requests"], 3)
        self.assertTrue(plan["safety"]["directory_listing_only"])
        self.assertFalse(plan["safety"]["bulk_download"])
        self.assertFalse(plan["safety"]["recursive_crawl"])
        self.assertFalse(plan["safety"]["raw_body_persistence"])

    def test_rejects_public_targets_bad_paths_and_unsafe_limits(self):
        module = load_module()
        public_result = module.build_plan(
            target_url="https://example.com/",
            output_dir="/tmp/out",
            candidate_path="/ftp/",
            request_cap=20,
            timeout=5,
            rate_limit=2,
        )
        self.assertEqual(public_result["status"], "error")
        self.assertEqual(public_result["errors"][0]["code"], "TARGET_NOT_FAST_LANE_LAB")

        bad_path = module.build_plan(
            target_url="http://<lab-ip>:3000/",
            output_dir="/tmp/out",
            candidate_path="/",
            request_cap=20,
            timeout=5,
            rate_limit=2,
        )
        self.assertEqual(bad_path["status"], "error")
        self.assertEqual(bad_path["errors"][0]["code"], "UNSUPPORTED_CANDIDATE_PATH")

        bad_rate = module.build_plan(
            target_url="http://<lab-ip>:3000/",
            output_dir="/tmp/out",
            candidate_path="/ftp/",
            request_cap=20,
            timeout=5,
            rate_limit=3,
        )
        self.assertEqual(bad_rate["status"], "error")
        self.assertEqual(bad_rate["errors"][0]["code"], "RATE_LIMIT_OUT_OF_RANGE")

    def test_extracts_and_classifies_filenames_without_file_content(self):
        module = load_module()
        html = """
        <html><title>listing directory /ftp/</title><body>
          <a href="incident-support.kdbx">incident-support.kdbx</a> 12 KB
          <a href="coupons_2013.md.bak">coupons_2013.md.bak</a>
          <a href="/ftp/legal.md">legal.md</a>
          <a href="../">parent</a>
          <a href="https://example.com/x">external</a>
        </body></html>
        """
        entries = module.extract_ftp_entries(html, "http://<lab-ip>:3000/ftp/")
        names = [entry["filename"] for entry in entries]
        self.assertEqual(names, ["incident-support.kdbx", "coupons_2013.md.bak", "legal.md"])
        classes = {entry["filename"]: entry["content_class"] for entry in entries}
        self.assertEqual(classes["incident-support.kdbx"], "password_database_candidate")
        self.assertEqual(classes["coupons_2013.md.bak"], "backup_or_temporary_candidate")
        self.assertEqual(classes["legal.md"], "text_or_markdown")
        self.assertTrue(all("content" not in entry for entry in entries))
        self.assertTrue(all(entry["status"] == "needs_manual_review" for entry in entries))

    def test_rendered_script_has_no_bulk_download_or_promotion_terms(self):
        module = load_module()
        plan = module.build_plan(
            target_url="http://<lab-ip>:3000/",
            output_dir="/home/kali/codex-output/ftp_filename_example",
            candidate_path="/ftp/",
            request_cap=20,
            timeout=5,
            rate_limit=2,
            lab_approved=True,
        )
        script = module.render_bash(plan)
        lower = script.lower()
        self.assertIn("observations.jsonl", script)
        self.assertIn("pre_health.txt", script)
        self.assertIn("post_health.txt", script)
        self.assertIn("extract_ftp_entries", script)
        self.assertIn("--max-redirs 0", script)
        for forbidden in (
            "wget", "aria2c", "curl -o", "curl -O", "--recursive", "--mirror",
            "sqlmap", "hydra", "msfconsole", "metasploit", "interactsh", "oast",
            "confirmed", "verified", "reportable", "ready_for_submission", "accepted",
            "etc/passwd", "shadow", "--dump", "os-shell",
        ):
            self.assertNotIn(forbidden, lower)

    def test_cli_requires_lab_approval_before_writing_script(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            script_path = Path(tmp) / "ftp_filename_verifier.sh"
            code = module.main([
                "--target-url", "http://<lab-ip>:3000/",
                "--output-dir", "/home/kali/codex-output/ftp_filename_example",
                "--write-script", str(script_path),
            ])
            self.assertEqual(code, 2)
            self.assertFalse(script_path.exists())

            code = module.main([
                "--target-url", "http://<lab-ip>:3000/",
                "--output-dir", "/home/kali/codex-output/ftp_filename_example",
                "--write-script", str(script_path),
                "--lab-approved",
            ])
            self.assertEqual(code, 0)
            content = script_path.read_text(encoding="utf-8")
            self.assertIn("set -euo pipefail", content)
            self.assertIn("record_ftp_listing", content)
            self.assertIn("observations.jsonl", content)


if __name__ == "__main__":
    unittest.main()
