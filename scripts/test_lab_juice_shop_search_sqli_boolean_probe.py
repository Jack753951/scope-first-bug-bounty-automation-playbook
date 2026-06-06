import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "lab_modules" / "lab_juice_shop_search_sqli_boolean_probe.py"
TARGET = "http://<lab-ip>:3000/"


class JuiceShopSearchSqliBooleanProbeTests(unittest.TestCase):
    def run_script(self, *args, expect_ok=True):
        proc = subprocess.run([sys.executable, str(SCRIPT), *args], cwd=ROOT.parent, text=True, capture_output=True)
        if expect_ok and proc.returncode != 0:
            self.fail(proc.stderr or proc.stdout)
        return proc

    def test_plan_only_candidate_only_source_driven(self):
        proc = self.run_script("--target", TARGET)
        plan = json.loads(proc.stdout)
        self.assertEqual(plan["mode"], "plan-only")
        self.assertEqual(plan["bundle_id"], "verified_lab_flow_juice_shop_search_sqli_boolean")
        self.assertEqual(plan["semantics"], "candidate-only")
        self.assertIn("q", plan["parameters"])
        self.assertIn("boolean_true", json.dumps(plan))
        self.assertIn("boolean_false", json.dumps(plan))
        self.assertEqual(plan["source_lineage"]["primary"], "GitHub/Arjun-inspired parameter discovery")
        self.assertIn("automatic confirmed finding promotion", " ".join(plan["disallowed"]).lower())

    def test_public_targets_are_rejected_fail_closed(self):
        proc = self.run_script("--target", "https://example.com/", expect_ok=False)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("refusing public target", proc.stderr.lower())

    def test_approved_generation_writes_runner_with_controls_and_manifest(self):
        tmp_root = ROOT.parent / "setting" / "local" / "test_tmp"
        tmp_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=tmp_root) as td:
            out_script = Path(td) / "juice_q_sqli_run.sh"
            out_dir = Path(td) / "artifacts"
            proc = self.run_script(
                "--target", TARGET,
                "--lab-approved",
                "--out-script", str(out_script),
                "--output-dir", str(out_dir),
            )
            payload = json.loads(proc.stdout)
            self.assertEqual(payload["status"], "script_written")
            text = out_script.read_text()
            self.assertTrue(text.startswith("#!/usr/bin/env bash\nset -euo pipefail"))
            self.assertIn("candidate-only", text)
            self.assertIn("boolean_true", text)
            self.assertIn("boolean_false", text)
            self.assertIn("possible_vulnerabilities.md", text)
            self.assertIn("artifact_manifest.txt", text)
            bash_check = subprocess.run(["bash", "-n"], input=text, text=True, capture_output=True)
            self.assertEqual(bash_check.returncode, 0, bash_check.stderr)

    def test_classifier_uses_boolean_differential_not_noisy_keywords(self):
        proc = self.run_script(
            "--classify-fixture",
            json.dumps({
                "baseline_empty": {"status": 200, "len": 16563, "indicators": ["SELECT", "WHERE"]},
                "boolean_true": {"status": 200, "len": 21581, "indicators": ["SELECT", "WHERE"]},
                "boolean_false": {"status": 200, "len": 30, "indicators": []},
                "single_quote": {"status": 200, "len": 30, "indicators": []},
            }),
        )
        verdict = json.loads(proc.stdout)
        self.assertEqual(verdict["classification"], "verified_lab_flow_candidate_boolean_sqli")
        self.assertIn("boolean_response_differential", verdict["signals"])
        self.assertIn("sql_keyword_indicators_treated_as_noisy", verdict["controls"])
        self.assertEqual(verdict["promotion"], "needs_manual_review")


if __name__ == "__main__":
    unittest.main()
