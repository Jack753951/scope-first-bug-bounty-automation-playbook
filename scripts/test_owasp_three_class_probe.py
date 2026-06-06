import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "lab_modules" / "owasp_three_class_probe.py"


class OwaspThreeClassProbeTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def test_plan_only_default_outputs_three_classes_without_script_write(self):
        with tempfile.TemporaryDirectory() as td:
            out_script = Path(td) / "run.sh"
            proc = self.run_cli("--target", "http://<lab-ip>:3000/", "--out-script", str(out_script))
            self.assertEqual(proc.returncode, 0, proc.stderr)
            plan = json.loads(proc.stdout)
            self.assertEqual(plan["mode"], "plan-only")
            self.assertFalse(out_script.exists())
            self.assertEqual(
                [wave["owasp_class"] for wave in plan["waves"]],
                ["A01:2021 Broken Access Control", "A02:2021 Cryptographic Failures", "A10:2025 Mishandling of Exceptional Conditions"],
            )
            self.assertEqual(plan["semantics"], "candidate-only")
            self.assertNotIn('"status": "confirmed"', json.dumps(plan).lower())

    def test_public_target_rejected_fail_closed(self):
        proc = self.run_cli("--target", "https://example.com/", "--lab-approved")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("public targets are not allowed", proc.stderr.lower())

    def test_lab_approved_writes_bounded_runnable(self):
        with tempfile.TemporaryDirectory() as td:
            out_script = Path(td) / "run.sh"
            proc = self.run_cli(
                "--target", "http://<lab-ip>:3000/",
                "--lab-approved",
                "--out-script", str(out_script),
                "--output-dir", "/tmp/owasp-three-class",
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue(out_script.exists())
            text = out_script.read_text(encoding="utf-8")
            self.assertIn("request_cap=16", text)
            self.assertIn("/rest/admin/application-configuration", text)
            self.assertIn("/rest/user/whoami", text)
            self.assertIn("/rest/products/search?q=%25", text)
            self.assertIn("spa_fallback_control", text)
            self.assertIn("unauth_identity_metadata", text)
            self.assertIn("observations.jsonl", text)
            self.assertNotIn("sqlmap", text)
            self.assertNotIn("hydra", text)
            self.assertNotIn("-L=false", text)
            self.assertNotIn("confirmed", text.lower())


if __name__ == "__main__":
    unittest.main()
