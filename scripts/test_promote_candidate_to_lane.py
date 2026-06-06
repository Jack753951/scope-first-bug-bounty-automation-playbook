from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMOTER_PATH = ROOT / "scripts" / "promote_candidate_to_lane.py"


def _load():
    spec = importlib.util.spec_from_file_location("promote_candidate_to_lane_for_tests", PROMOTER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class PromoteCandidateToLaneTests(unittest.TestCase):
    def sample_pending(self) -> dict:
        return {
            "schema_version": "1.0",
            "updated_at": "2026-05-29",
            "boundary": "candidate only",
            "candidates": [
                {
                    "slug": "<program-slug>",
                    "platform": "<bug-bounty-platform>",
                    "program": "<program-slug>",
                    "url": "https://<bug-bounty-platform>.com/<program-slug>/policy_scopes?type=team",
                    "status": "candidate_passive_intake",
                    "score": {"total_0_23": 20},
                    "candidate_assets": ["cloud.<program-redacted>.com", "app.<program-redacted>"],
                    "bundle_fit": ["auth-role-separation", "idor-bola-api-object-boundary"],
                    "blocked_before": [
                        "operator approval for exact live scope entries",
                        "account signup/login/OTP/CAPTCHA/password/phone/payment/KYC",
                    ],
                    "recommended_next_step": "Review candidate assets/classes before target contact.",
                }
            ],
        }

    def test_builds_passive_lane_draft_without_authorizing_live_action(self) -> None:
        mod = _load()
        draft = mod.build_lane_draft(self.sample_pending(), slug="<program-slug>", today="2026-05-29")

        self.assertEqual(draft["lane_state"]["program_slug"], "<program-slug>")
        self.assertEqual(draft["lane_state"]["operator_decision"], "PASSIVE_ONLY")
        self.assertEqual(draft["lane_state"]["machine_state"], "POLICY_INTAKE")
        self.assertEqual(draft["lane_state"]["authorization"]["scope_file"], "not_created_operator_gate")
        self.assertIn("testing_live_assets", draft["lane_state"]["lane_boundary"]["blocked_actions"])
        self.assertIn("auth-role-separation", draft["run_card_markdown"])
        self.assertIn("Decision: PARK until operator exact-scope approval", draft["run_card_markdown"])
        self.assertNotIn("reportable", json.dumps(draft).lower())
        self.assertNotIn("verified", json.dumps(draft).lower())

    def test_cli_writes_draft_lane_and_run_card_only(self) -> None:
        mod = _load()
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            pending_path = td_path / "pending.json"
            out_dir = td_path / "out"
            pending_path.write_text(json.dumps(self.sample_pending()), encoding="utf-8")

            exit_code = mod.main([
                "--pending", str(pending_path),
                "--slug", "<program-slug>",
                "--output-dir", str(out_dir),
                "--date", "2026-05-29",
            ])

            self.assertEqual(exit_code, 0)
            lane_path = out_dir / "<program-slug>" / "lane_state.draft.json"
            card_path = out_dir / "<program-slug>" / "run_card_20260529.md"
            self.assertTrue(lane_path.exists())
            self.assertTrue(card_path.exists())
            lane = json.loads(lane_path.read_text(encoding="utf-8"))
            self.assertEqual(lane["status"], "blocked_awaiting_scope")
            self.assertIn("No live action authorized", card_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
