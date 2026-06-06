import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODULES = {
    "access": ROOT / "lab_modules" / "lab_access_control_unauth_route_metadata.py",
    "crypto": ROOT / "lab_modules" / "lab_crypto_transport_metadata.py",
    "exception": ROOT / "lab_modules" / "lab_exceptional_condition_metadata.py",
}
TARGET = "http://<lab-ip>:3000/"


class OwaspSingleVulnModuleTests(unittest.TestCase):
    def run_module(self, module_name, *args):
        return subprocess.run(
            [sys.executable, str(MODULES[module_name]), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_each_module_is_plan_only_by_default_and_one_vulnerability_scope(self):
        for name in MODULES:
            with self.subTest(name=name):
                result = self.run_module(name, "--target", TARGET)
                self.assertEqual(result.returncode, 0, result.stderr)
                plan = json.loads(result.stdout)
                self.assertEqual(plan["mode"], "plan-only")
                self.assertEqual(plan["semantics"], "candidate-only")
                self.assertEqual(plan["module_granularity"], "one-vulnerability-one-module")
                self.assertEqual(len(plan["owasp_classes"]), 1)
                self.assertIn(plan["oss_recon_decision"]["decision"], {"adopt", "wrap", "adapt", "reference-only", "write-custom"})
                self.assertNotIn("confirmed", json.dumps(plan).lower())
                self.assertNotIn("reportable", json.dumps(plan).lower())

    def test_modules_reject_public_targets_fail_closed(self):
        for name in MODULES:
            with self.subTest(name=name):
                result = self.run_module(name, "--target", "https://example.com/")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("public targets are not allowed", result.stderr)

    def test_approved_generation_writes_bounded_runner_with_possible_vulnerabilities(self):
        for name in MODULES:
            with self.subTest(name=name):
                with tempfile.TemporaryDirectory() as tmp:
                    runner = Path(tmp) / f"{name}.sh"
                    result = self.run_module(
                        name,
                        "--target", TARGET,
                        "--lab-approved",
                        "--out-script", str(runner),
                        "--output-dir", f"/tmp/{name}-single-vuln-test",
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertTrue(runner.exists())
                    text = runner.read_text(encoding="utf-8")
                    self.assertIn("observations.jsonl", text)
                    self.assertIn("possible_vulnerabilities.md", text)
                    self.assertIn("artifact_manifest.txt", text)
                    self.assertIn("pre_health", text)
                    self.assertIn("post_health", text)
                    self.assertNotIn("-L=false", text)
                    self.assertNotIn("sqlmap", text.lower())
                    self.assertNotIn("hydra", text.lower())
                    self.assertNotIn("confirmed", text.lower())
                    self.assertNotIn("reportable", text.lower())


if __name__ == "__main__":
    unittest.main()
