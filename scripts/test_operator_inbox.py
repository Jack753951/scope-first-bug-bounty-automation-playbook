from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INBOX_PATH = ROOT / "scripts" / "build_operator_inbox.py"


def _load():
    spec = importlib.util.spec_from_file_location("build_operator_inbox_for_tests", INBOX_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class OperatorInboxPendingDecisionTests(unittest.TestCase):
    def test_pending_candidate_uses_slug_program_score_and_default_safe_options(self) -> None:
        mod = _load()
        decision = mod.pending_decision(
            {
                "slug": "<program-slug>",
                "program": "<program-slug>",
                "source": "passive platform policy normalization",
                "status": "candidate_passive_intake",
                "score": {"total_0_23": 20},
                "recommended_next_step": "Review candidate assets/classes before target contact.",
                "blocked_before": [
                    "operator approval for exact live scope entries",
                    "any live target testing beyond passive policy/public-doc reading",
                ],
            }
        )

        self.assertEqual(decision["title"], "`<program-slug>` / <program-slug>")
        self.assertIn("Score: 20/23", decision["situation"])
        self.assertIn("Review candidate assets", decision["situation"])
        self.assertEqual(decision["options"][0]["label"], "KEEP_PASSIVE_TRIAGE")
        self.assertTrue(decision["options"][0]["default"])
        self.assertIn("exact scope", decision["options"][1]["description"])


if __name__ == "__main__":
    unittest.main()
