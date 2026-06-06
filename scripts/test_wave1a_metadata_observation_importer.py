"""Focused tests for offline Wave 1A metadata observation importer."""

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
SCRIPT_PATH = REPO_ROOT / "scripts" / "import_wave1a_metadata_observations.py"


def load_module():
    spec = importlib.util.spec_from_file_location("wave1a_importer_under_test", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


class Wave1AMetadataObservationImporterTests(unittest.TestCase):
    def test_imports_wave1a_jsonl_as_non_promotional_observations_and_candidate_seeds(self):
        module = load_module()
        result = module.import_observations(
            REPO_ROOT,
            "tests/fixtures/wave1a_metadata/observations_sample.jsonl",
            run_id="unit-wave1a",
        )

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["schema_version"], "wave1a_metadata_observations/0.1-trial")
        self.assertEqual(result["summary"]["imported_count"], 5)
        self.assertEqual(result["summary"]["candidate_seed_count"], 2)
        self.assertTrue(all(obs["status"] == "observation" for obs in result["observations"]))
        self.assertTrue(all(obs["scanner_output_only"] for obs in result["observations"]))
        relationships = [seed["relationship"] for seed in result["candidate_seeds"]]
        self.assertEqual(relationships, ["directory_listing_candidate", "api_docs_candidate"])
        self.assertTrue(all(seed["status"] == "needs_manual_review" for seed in result["candidate_seeds"]))
        forbidden = {"confirmed", "verified", "reportable", "accepted"}
        self.assertFalse(forbidden.intersection(json.dumps(result).lower().split('"')))

    def test_importer_does_not_perform_network_or_subprocess(self):
        module = load_module()
        with patch("subprocess.run", side_effect=AssertionError("must not execute subprocess")), patch(
            "urllib.request.urlopen", side_effect=AssertionError("must not perform network I/O")
        ):
            result = module.import_observations(
                REPO_ROOT,
                "tests/fixtures/wave1a_metadata/observations_sample.jsonl",
                run_id="unit-wave1a-safety",
            )
        self.assertEqual(result["status"], "ok")
        self.assertFalse(result["safety"]["network_io"])
        self.assertFalse(result["safety"]["subprocess_execution"])
        self.assertFalse(result["safety"]["promotes_findings"])

    def test_rejects_paths_outside_wave1a_fixture_allowlist(self):
        module = load_module()
        result = module.import_observations(
            REPO_ROOT,
            "tests/fixtures/external_tools/httpx_sample.jsonl",
            run_id="unit-wave1a-badpath",
        )
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["errors"][0]["code"], "INPUT_PATH_NOT_ALLOWED")
        self.assertEqual(result["observations"], [])
        self.assertEqual(result["candidate_seeds"], [])

    def test_malformed_jsonl_fails_closed_without_partial_observations(self):
        module = load_module()
        result = module.import_observations(
            REPO_ROOT,
            "tests/fixtures/wave1a_metadata/malformed_observations.jsonl",
            run_id="unit-wave1a-malformed",
        )
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["summary"]["imported_count"], 0)
        self.assertEqual(result["observations"], [])
        self.assertEqual(result["candidate_seeds"], [])
        self.assertEqual(result["errors"][0]["code"], "JSONL_PARSE_ERROR")

    def test_cli_outputs_json_and_nonzero_for_public_promotional_status(self):
        module = load_module()
        out = io.StringIO()
        with redirect_stdout(out):
            code = module.main([
                "--repo-root", str(REPO_ROOT),
                "--input", "tests/fixtures/external_tools/httpx_sample.jsonl",
            ])
        self.assertEqual(code, 2)
        payload = json.loads(out.getvalue())
        self.assertEqual(payload["status"], "error")
        self.assertEqual(payload["errors"][0]["code"], "INPUT_PATH_NOT_ALLOWED")


if __name__ == "__main__":
    unittest.main()
