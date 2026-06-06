from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRAPPER = ROOT / "scripts" / "kali-browser-ops.ps1"


class KaliBrowserOpsWrapperTests(unittest.TestCase):
    def test_wrapper_exposes_cdp_click_action_without_live_url_argument(self) -> None:
        text = WRAPPER.read_text(encoding="utf-8")

        self.assertIn('"cdp-click"', text)
        self.assertIn('cdp_browser_action.py', text)
        self.assertIn('--text', text)
        self.assertIn('--selector', text)
        self.assertNotIn('--target', text)
        self.assertNotIn('--live', text)


if __name__ == "__main__":
    unittest.main()
