"""Focused tests for controlled external tool lab runner plan generation."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "run_external_tool_lab.py"


def load_module():
    spec = importlib.util.spec_from_file_location("external_tool_lab_runner_under_test", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


class ExternalToolLabRunnerTests(unittest.TestCase):
    def test_plan_only_generates_safe_httpx_and_katana_commands(self):
        module = load_module()
        plan = module.build_plan(
            target_url="http://<lab-ip>:3000",
            tools=["httpx", "katana"],
            rate_limit=2,
            timeout=5,
            depth=1,
            output_dir="/home/kali/phase4a-calibration/example",
            execute_lab_approved=False,
        )

        self.assertEqual(plan["status"], "ok")
        self.assertEqual(plan["run_mode"], "plan_only")
        self.assertEqual([step["tool"] for step in plan["steps"]], ["pre_health", "httpx", "katana", "post_health"])
        commands = "\n".join(step["command"] for step in plan["steps"])
        self.assertIn("httpx", commands)
        self.assertIn("katana", commands)
        self.assertIn("-rate-limit 2", commands)
        self.assertIn("-depth 1", commands)
        self.assertIn("-omit-raw", commands)
        self.assertIn("-omit-body", commands)
        for forbidden in ("nuclei", "ffuf", "interactsh", " -irr", "include-response", "--dump", "os-shell", "reportable", "confirmed"):
            self.assertNotIn(forbidden, commands.lower())

    def test_plan_only_generates_safe_nuclei_and_ffuf_commands(self):
        module = load_module()
        plan = module.build_plan(
            target_url="http://<lab-ip>:3000",
            tools=["nuclei", "ffuf"],
            rate_limit=2,
            timeout=5,
            depth=1,
            output_dir="/home/kali/phase4a-calibration/example",
            execute_lab_approved=False,
        )

        self.assertEqual(plan["status"], "ok")
        self.assertEqual([step["tool"] for step in plan["steps"]], ["pre_health", "nuclei", "ffuf", "post_health"])
        commands = "\n".join(step["command"] for step in plan["steps"])
        self.assertIn("nuclei", commands)
        self.assertIn("-jsonl", commands)
        self.assertIn("-omit-raw", commands)
        self.assertIn("ffuf", commands)
        self.assertIn("-rate 2", commands)
        self.assertIn("-maxtime 30", commands)
        self.assertIn("phase4a_tiny_wordlist.txt", commands)
        for forbidden in ("interactsh-url", "-tags", "dos", "intrusive", "-recursion", "-w /usr/share/wordlists", "--dump", "os-shell", "reportable", "confirmed"):
            self.assertNotIn(forbidden, commands.lower())

    def test_rejects_public_targets_and_unknown_tools(self):
        module = load_module()
        public_result = module.build_plan(
            target_url="https://example.com",
            tools=["httpx"],
            rate_limit=2,
            timeout=5,
            depth=1,
            output_dir="/tmp/out",
        )
        self.assertEqual(public_result["status"], "error")
        self.assertEqual(public_result["errors"][0]["code"], "TARGET_NOT_LOCAL_LAB")

        unknown_result = module.build_plan(
            target_url="http://<lab-ip>:3000",
            tools=["random-exploit"],
            rate_limit=2,
            timeout=5,
            depth=1,
            output_dir="/tmp/out",
        )
        self.assertEqual(unknown_result["status"], "error")
        self.assertEqual(unknown_result["errors"][0]["code"], "TOOL_NOT_SUPPORTED")

    def test_cli_requires_execute_approval_before_writing_executable_script(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "run.sh"
            code = module.main([
                "--target-url", "http://<lab-ip>:3000",
                "--tool", "httpx",
                "--output-dir", "/home/kali/phase4a-calibration/example",
                "--write-script", str(out),
            ])
            self.assertEqual(code, 2)
            self.assertFalse(out.exists())

            code = module.main([
                "--target-url", "http://<lab-ip>:3000",
                "--tool", "httpx",
                "--output-dir", "/home/kali/phase4a-calibration/example",
                "--write-script", str(out),
                "--execute-lab-approved",
            ])
            self.assertEqual(code, 0)
            content = out.read_text(encoding="utf-8")
            self.assertIn("set -euo pipefail", content)
            self.assertIn("httpx", content)
            self.assertNotIn("nuclei", content)


if __name__ == "__main__":
    unittest.main()
