#!/usr/bin/env python3
"""Tests for scripts/ctf_review_decision.py."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "ctf_review_decision.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "ctf_review_decision"

spec = importlib.util.spec_from_file_location("ctf_review_decision", SCRIPT)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ReviewDecisionTests(unittest.TestCase):
    def _decision(self, fixture_name: str) -> dict:
        payload = json.loads((FIXTURES / fixture_name).read_text(encoding="utf-8"))
        return mod.decide(payload)

    def test_verified_normal_flag(self) -> None:
        decision = self._decision("verified_normal_flag.json")
        self.assertEqual(decision["status"], "verified")
        self.assertEqual(decision["confidence"], "high")
        self.assertEqual(decision["triggers"], [])

    def test_no_wrapper_flag_needs_second_review_for_abnormal_format(self) -> None:
        decision = self._decision("no_wrapper_flag_verified.json")
        self.assertEqual(decision["status"], "needs_second_review")
        self.assertIn("abnormal_format", decision["triggers"])
        self.assertEqual(decision["confidence"], "low")

    def test_ui_only_candidate_needs_review(self) -> None:
        decision = self._decision("ui_only_candidate_needs_review.json")
        self.assertEqual(decision["status"], "needs_second_review")
        self.assertIn("ui_or_checker_only", decision["triggers"])

    def test_multiple_candidates_needs_review(self) -> None:
        decision = self._decision("multiple_candidates_needs_review.json")
        self.assertEqual(decision["status"], "needs_second_review")
        self.assertIn("multiple_candidates", decision["triggers"])

    def test_solver_timeout_needs_review(self) -> None:
        decision = self._decision("solver_timeout_needs_review.json")
        self.assertEqual(decision["status"], "needs_second_review")
        self.assertIn("solver_timeout", decision["triggers"])

    def test_external_writeup_only_needs_review(self) -> None:
        decision = self._decision("external_writeup_only_needs_review.json")
        self.assertEqual(decision["status"], "needs_second_review")
        self.assertIn("external_source_only", decision["triggers"])

    def test_boundary_override_fields_are_ignored_and_do_not_grant_verification(self) -> None:
        decision = self._decision("boundary_override_no_grant.json")
        self.assertNotEqual(decision["status"], "verified")
        self.assertIn("force_verified", decision["ignored_fields"])
        self.assertIn("scope_override", decision["ignored_fields"])
        self.assertIn("target_url", decision["ignored_fields"])
        self.assertIn("status", decision["ignored_fields"])

    def test_all_fixtures_match_pinned_expected_outputs(self) -> None:
        for fixture in sorted(FIXTURES.glob("*.json")):
            if fixture.name.endswith(".expected.json"):
                continue
            with self.subTest(fixture=fixture.name):
                expected_path = fixture.with_name(f"{fixture.stem}.expected.json")
                self.assertTrue(expected_path.is_file(), f"missing {expected_path.name}")
                payload = json.loads(fixture.read_text(encoding="utf-8"))
                self.assertEqual(mod.decide(payload), json.loads(expected_path.read_text(encoding="utf-8")))

    def test_deterministic_cli_output(self) -> None:
        fixture = FIXTURES / "solver_timeout_needs_review.json"
        expected = (FIXTURES / "solver_timeout_needs_review.expected.json").read_text(encoding="utf-8")
        first = subprocess.check_output([sys.executable, str(SCRIPT), "--input", str(fixture)], text=True)
        second = subprocess.check_output([sys.executable, str(SCRIPT), "--input", str(fixture)], text=True)
        self.assertEqual(first, second)
        self.assertEqual(first, expected)
        parsed = json.loads(first)
        self.assertEqual(parsed["triggers"], sorted(parsed["triggers"]))

    def test_output_file_matches_stdout_shape(self) -> None:
        fixture = FIXTURES / "verified_normal_flag.json"
        with tempfile.TemporaryDirectory() as td:
            output = Path(td) / "decision.json"
            subprocess.check_call([sys.executable, str(SCRIPT), "--input", str(fixture), "--output", str(output)])
            parsed = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(parsed["status"], "verified")


if __name__ == "__main__":
    unittest.main(verbosity=2)
