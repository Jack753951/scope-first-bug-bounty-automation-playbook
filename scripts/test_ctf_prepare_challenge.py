#!/usr/bin/env python3
"""Tests for scripts/ctf_prepare_challenge.py."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "ctf_prepare_challenge.py"

spec = importlib.util.spec_from_file_location("ctf_prepare_challenge", SCRIPT)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class PrepareChallengeTests(unittest.TestCase):
    def test_prepare_writes_challenge_and_notes(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            code, report = mod.prepare_challenge(
                repo_root=Path(td),
                slug="clouds-nimbus",
                category="crypto",
                source="picoCTF local drill",
                kali_required=True,
                force=False,
            )
            self.assertEqual(code, 0, report)
            slug_dir = Path(td) / "setting" / "local" / "ctf" / "clouds-nimbus"
            challenge = json.loads((slug_dir / "challenge.json").read_text(encoding="utf-8"))
            self.assertEqual(challenge["slug"], "clouds-nimbus")
            self.assertEqual(challenge["category"], "crypto")
            self.assertTrue(challenge["kali_required"])
            notes = (slug_dir / "solve_notes.md").read_text(encoding="utf-8")
            self.assertIn("Output-side review checklist", notes)
            self.assertIn("external writeups/PoCs", notes)

    def test_idempotency_refuses_existing_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            kwargs = dict(
                repo_root=Path(td),
                slug="repeat-test",
                category="misc",
                source="lab",
                kali_required=False,
            )
            code, _ = mod.prepare_challenge(force=False, **kwargs)
            self.assertEqual(code, 0)
            challenge_path = Path(td) / "setting" / "local" / "ctf" / "repeat-test" / "challenge.json"
            original = challenge_path.read_text(encoding="utf-8")
            code, report = mod.prepare_challenge(force=False, **kwargs)
            self.assertEqual(code, 1)
            self.assertEqual(report["error_code"], "ALREADY_EXISTS")
            self.assertEqual(challenge_path.read_text(encoding="utf-8"), original)
            code, _ = mod.prepare_challenge(force=True, **kwargs)
            self.assertEqual(code, 0)

    def test_invalid_slug_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            code, report = mod.prepare_challenge(
                repo_root=Path(td),
                slug="../evil",
                category="misc",
                source="lab",
                kali_required=False,
                force=False,
            )
            self.assertEqual(code, 2)
            self.assertEqual(report["error_code"], "INVALID_SLUG")
            self.assertFalse((Path(td) / "setting").exists())

    def test_cli_outputs_json(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = subprocess.check_output([
                sys.executable,
                str(SCRIPT),
                "--repo-root", td,
                "--slug", "cli-test",
                "--category", "crypto",
                "--source", "unit",
            ], text=True)
            parsed = json.loads(out)
            self.assertEqual(parsed["status"], "ok")
            self.assertTrue((Path(td) / "setting" / "local" / "ctf" / "cli-test" / "solve_notes.md").is_file())


if __name__ == "__main__":
    unittest.main(verbosity=2)
