import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODULE = ROOT / "lab_modules" / "lab_service_baseline_targets.py"
TARGET = "http://<lab-ip>:3000/"
EXPECTED_SERVICES = {"apache", "tomcat", "openssl", "haproxy", "envoy", "traefik"}


class ServiceBaselineTargetTests(unittest.TestCase):
    def run_module(self, *args):
        return subprocess.run(
            [sys.executable, str(MODULE), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_plan_lists_six_service_baseline_targets_candidate_only(self):
        result = self.run_module("--target", TARGET)
        self.assertEqual(result.returncode, 0, result.stderr)
        plan = json.loads(result.stdout)
        self.assertEqual(plan["mode"], "plan-only")
        self.assertEqual(plan["semantics"], "candidate-only")
        self.assertEqual(plan["bundle_id"], "lab_service_baseline_targets")
        self.assertEqual(set(plan["service_targets"]), EXPECTED_SERVICES)
        self.assertIn("local-learning-lab", plan["lane"])
        lowered = json.dumps(plan).lower()
        self.assertNotIn("confirmed finding", lowered)
        self.assertNotIn("ready_for_submission", lowered)

    def test_public_targets_are_rejected_fail_closed(self):
        result = self.run_module("--target", "https://example.com/")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("public targets are not allowed", result.stderr)

    def test_generated_runner_contains_service_specific_safe_probes_and_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            runner = Path(tmp) / "lab_service_baseline_targets_run.sh"
            result = self.run_module(
                "--target", TARGET,
                "--lab-approved",
                "--out-script", str(runner),
                "--output-dir", "/tmp/lab-service-baseline-test",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            text = runner.read_text(encoding="utf-8")
            for service in EXPECTED_SERVICES:
                self.assertIn(service, text.lower())
            self.assertIn("/server-status", text)
            self.assertIn("/manager/html", text)
            self.assertIn("openssl s_client", text)
            self.assertIn("/haproxy?stats", text)
            self.assertIn("probe_path haproxy '/;csv'", text)
            self.assertIn(":9901/server_info", text)
            self.assertIn("/dashboard/", text)
            self.assertIn("root_body.sha256", text)
            self.assertIn("generic_root_fallback", text)
            self.assertIn("cipher is (none)", text.lower())
            self.assertIn("python - \"$outdir\" <<'PY'", text)
            self.assertIn("observations.jsonl", text)
            self.assertIn("possible_vulnerabilities.md", text)
            self.assertIn("artifact_manifest.txt", text)
            self.assertIn("candidate-only", text)
            self.assertNotIn("confirmed finding", text.lower())
            self.assertNotIn("ready_for_submission", text.lower())


if __name__ == "__main__":
    unittest.main()
