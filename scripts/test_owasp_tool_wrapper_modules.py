import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODULES = {
    "ffuf_sensitive_paths": ROOT / "lab_modules" / "lab_ffuf_sensitive_path_discovery.py",
    "nikto_server_misconfig": ROOT / "lab_modules" / "lab_nikto_server_misconfig.py",
    "nmap_http_fingerprint": ROOT / "lab_modules" / "lab_nmap_http_fingerprint.py",
}
TARGET = "http://<lab-ip>:3000/"


class OwaspToolWrapperModuleTests(unittest.TestCase):
    def run_module(self, module_name, *args):
        return subprocess.run(
            [sys.executable, str(MODULES[module_name]), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_tool_wrappers_are_plan_only_by_default_and_record_mature_tool_decision(self):
        for name in MODULES:
            with self.subTest(name=name):
                result = self.run_module(name, "--target", TARGET)
                self.assertEqual(result.returncode, 0, result.stderr)
                plan = json.loads(result.stdout)
                self.assertEqual(plan["mode"], "plan-only")
                self.assertEqual(plan["semantics"], "candidate-only")
                self.assertEqual(plan["module_granularity"], "one-vulnerability-one-module")
                self.assertEqual(len(plan["owasp_classes"]), 1)
                self.assertIn(plan["oss_recon_decision"]["decision"], {"adopt", "wrap", "adapt"})
                self.assertIn("tool", plan)
                self.assertTrue(plan["tool"]["name"])
                self.assertIn("candidate-only", json.dumps(plan))
                lowered = json.dumps(plan).lower()
                self.assertNotIn("confirmed finding", lowered)
                self.assertNotIn("ready_for_submission", lowered)

    def test_tool_wrappers_reject_public_targets_fail_closed(self):
        for name in MODULES:
            with self.subTest(name=name):
                result = self.run_module(name, "--target", "https://example.com/")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("public targets are not allowed", result.stderr)

    def test_approved_generation_writes_tool_runner_with_manifest_and_sanitized_outputs(self):
        for name in MODULES:
            with self.subTest(name=name):
                with tempfile.TemporaryDirectory() as tmp:
                    runner = Path(tmp) / f"{name}.sh"
                    result = self.run_module(
                        name,
                        "--target", TARGET,
                        "--lab-approved",
                        "--out-script", str(runner),
                        "--output-dir", f"/tmp/{name}-tool-wrapper-test",
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    text = runner.read_text(encoding="utf-8")
                    self.assertIn("tool_raw", text)
                    self.assertIn("observations.jsonl", text)
                    self.assertIn("possible_vulnerabilities.md", text)
                    self.assertIn("artifact_manifest.txt", text)
                    self.assertIn("pre_health", text)
                    self.assertIn("post_health", text)
                    self.assertIn("candidate-only", text)
                    self.assertIn("--max-time", text)
                    self.assertNotIn("confirmed finding", text.lower())
                    self.assertNotIn("ready_for_submission", text.lower())


if __name__ == "__main__":
    unittest.main()
