import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET = "http://<lab-ip>:3000/"

ADAPTERS = {
    "lab_api_docs_exposure_triage": {
        "script": ROOT / "lab_modules" / "lab_api_docs_exposure_triage.py",
        "needle": "/api-docs",
        "bundle": "lab_api_docs_exposure_triage",
    },
    "lab_metrics_exposure_triage": {
        "script": ROOT / "lab_modules" / "lab_metrics_exposure_triage.py",
        "needle": "/metrics",
        "bundle": "lab_metrics_exposure_triage",
    },
    "lab_source_map_disclosure_triage": {
        "script": ROOT / "lab_modules" / "lab_source_map_disclosure_triage.py",
        "needle": ".map",
        "bundle": "lab_source_map_disclosure_triage",
    },
    "lab_auth_surface_no_bruteforce": {
        "script": ROOT / "lab_modules" / "lab_auth_surface_no_bruteforce.py",
        "needle": "/rest/user/login",
        "bundle": "lab_auth_surface_no_bruteforce",
    },
    "lab_component_metadata_triage": {
        "script": ROOT / "lab_modules" / "lab_component_metadata_triage.py",
        "needle": "/package.json",
        "bundle": "lab_component_metadata_triage",
    },
    "lab_integrity_metadata_triage": {
        "script": ROOT / "lab_modules" / "lab_integrity_metadata_triage.py",
        "needle": "/.well-known/security.txt",
        "bundle": "lab_integrity_metadata_triage",
    },
}


class ThreeExposureBundleTests(unittest.TestCase):
    def run_json(self, script, *args, expect_ok=True):
        proc = subprocess.run([sys.executable, str(script), *args], cwd=ROOT.parent, text=True, capture_output=True)
        if expect_ok and proc.returncode != 0:
            self.fail(proc.stderr or proc.stdout)
        return proc

    def test_adapters_are_plan_only_candidate_only_and_record_oss_tools(self):
        for name, meta in ADAPTERS.items():
            with self.subTest(name=name):
                proc = self.run_json(meta["script"], "--target", TARGET)
                plan = json.loads(proc.stdout)
                self.assertEqual(plan["mode"], "plan-only")
                self.assertEqual(plan["bundle_id"], meta["bundle"])
                self.assertEqual(plan["semantics"], "candidate-only")
                self.assertIn(meta["needle"], json.dumps(plan))
                self.assertIn("oss_recon_decision", plan)
                self.assertGreaterEqual(len(plan["oss_recon_decision"]["mature_tools"]), 3)
                self.assertIn("confirmed", " ".join(plan["disallowed"]).lower())

    def test_public_targets_are_rejected_fail_closed(self):
        for meta in ADAPTERS.values():
            proc = self.run_json(meta["script"], "--target", "https://example.com/", expect_ok=False)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("refusing public target", proc.stderr.lower())

    def test_approved_generation_writes_bash_runner_and_manifest(self):
        for name, meta in ADAPTERS.items():
            with self.subTest(name=name):
                tmp_root = ROOT.parent / "setting" / "local" / "test_tmp"
                tmp_root.mkdir(parents=True, exist_ok=True)
                with tempfile.TemporaryDirectory(dir=tmp_root) as td:
                    out_script = Path(td) / f"{name}_run.sh"
                    out_dir = Path(td) / "artifacts"
                    proc = self.run_json(
                        meta["script"],
                        "--target", TARGET,
                        "--lab-approved",
                        "--out-script", str(out_script),
                        "--output-dir", str(out_dir),
                    )
                    payload = json.loads(proc.stdout)
                    self.assertEqual(payload["status"], "script_written")
                    text = out_script.read_text()
                    self.assertIn("candidate-only", text)
                    self.assertIn("possible_vulnerabilities.md", text)
                    self.assertIn("artifact_manifest.txt", text)
                    self.assertIn("python - \"$outdir\" <<'PY'", text)
                    self.assertTrue(text.startswith("#!/usr/bin/env bash\nset -euo pipefail"))


if __name__ == "__main__":
    unittest.main()
