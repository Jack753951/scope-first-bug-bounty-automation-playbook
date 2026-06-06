"""Focused tests for offline external tool observation importer."""

from __future__ import annotations

import importlib.util
import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "import_external_tool_observations.py"


def load_module():
    spec = importlib.util.spec_from_file_location("external_tool_importer_under_test", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


class ExternalToolImporterTests(unittest.TestCase):
    def test_imports_httpx_jsonl_as_non_promotional_observations(self):
        module = load_module()
        result = module.import_observations(
            REPO_ROOT,
            "httpx",
            "tests/fixtures/external_tools/httpx_sample.jsonl",
            run_id="unit-httpx",
        )

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["schema_version"], "external_tool_observations/0.1-trial")
        self.assertEqual(result["summary"]["imported_count"], 1)
        obs = result["observations"][0]
        self.assertEqual(obs["status"], "observation")
        self.assertEqual(obs["tool"]["name"], "httpx")
        self.assertEqual(obs["target"]["url"], "http://<lab-ip>:3000")
        self.assertEqual(obs["http"]["status_code"], 200)
        self.assertIn("Express", obs["technologies"])
        forbidden = {"confirmed", "verified", "reportable", "accepted"}
        self.assertFalse(forbidden.intersection(json.dumps(result).lower().split('"')))

    def test_imports_katana_jsonl_without_following_discovered_urls(self):
        module = load_module()
        with patch("subprocess.run", side_effect=AssertionError("must not execute subprocess")), patch(
            "urllib.request.urlopen", side_effect=AssertionError("must not perform network I/O")
        ):
            result = module.import_observations(
                REPO_ROOT,
                "katana",
                "tests/fixtures/external_tools/katana_sample.jsonl",
                run_id="unit-katana",
            )

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["summary"]["imported_count"], 2)
        endpoints = [obs["target"]["url"] for obs in result["observations"]]
        self.assertEqual(endpoints, ["http://<lab-ip>:3000/", "http://<lab-ip>:3000/ftp/"])
        self.assertTrue(all(obs["relationship"] == "discovered_url" for obs in result["observations"]))
        self.assertTrue(all(obs["status"] == "observation" for obs in result["observations"]))

    def test_imports_nuclei_and_ffuf_outputs_as_non_promotional_observations(self):
        module = load_module()
        nuclei = module.import_observations(
            REPO_ROOT,
            "nuclei",
            "tests/fixtures/external_tools/nuclei_sample.jsonl",
            run_id="unit-nuclei",
        )
        self.assertEqual(nuclei["status"], "ok")
        self.assertEqual(nuclei["summary"]["imported_count"], 1)
        self.assertEqual(nuclei["observations"][0]["tool"]["name"], "nuclei")
        self.assertEqual(nuclei["observations"][0]["relationship"], "template_observation")
        self.assertEqual(nuclei["observations"][0]["status"], "observation")

        ffuf = module.import_observations(
            REPO_ROOT,
            "ffuf",
            "tests/fixtures/external_tools/ffuf_sample.json",
            run_id="unit-ffuf",
        )
        self.assertEqual(ffuf["status"], "ok")
        self.assertEqual(ffuf["summary"]["imported_count"], 2)
        self.assertEqual(ffuf["observations"][0]["tool"]["name"], "ffuf")
        self.assertEqual(ffuf["observations"][0]["relationship"], "content_discovery_hit")
        forbidden = {"confirmed", "verified", "reportable", "accepted"}
        self.assertFalse(forbidden.intersection(json.dumps(ffuf).lower().split('"')))

    def test_rejects_paths_outside_committed_external_tool_fixtures(self):
        module = load_module()
        result = module.import_observations(REPO_ROOT, "httpx", "handoff/phase4a_lab_workflow_run_20260520_maxlab/workflow.json")

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["errors"][0]["code"], "INPUT_PATH_NOT_ALLOWED")
        self.assertEqual(result["observations"], [])

    def test_malformed_jsonl_fails_closed_without_partial_observations(self):
        module = load_module()
        result = module.import_observations(REPO_ROOT, "httpx", "tests/fixtures/external_tools/malformed_sample.jsonl")

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["summary"]["imported_count"], 0)
        self.assertEqual(result["observations"], [])
        self.assertEqual(result["errors"][0]["code"], "JSONL_PARSE_ERROR")

    def test_cli_outputs_json_and_rejects_unknown_tool(self):
        module = load_module()
        out = io.StringIO()
        with redirect_stdout(out):
            code = module.main([
                "--repo-root",
                str(REPO_ROOT),
                "--tool",
                "random-exploit",
                "--input",
                "tests/fixtures/external_tools/httpx_sample.jsonl",
            ])
        self.assertEqual(code, 2)
        payload = json.loads(out.getvalue())
        self.assertEqual(payload["status"], "error")
        self.assertEqual(payload["errors"][0]["code"], "TOOL_NOT_SUPPORTED")


if __name__ == "__main__":
    unittest.main()
