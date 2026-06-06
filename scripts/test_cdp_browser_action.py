from __future__ import annotations

import importlib.util
import io
import json
import unittest
from contextlib import redirect_stderr
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "cdp_browser_action.py"


def _load():
    spec = importlib.util.spec_from_file_location("cdp_browser_action_for_tests", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class CdpBrowserActionTests(unittest.TestCase):
    def test_click_expression_fails_closed_when_text_is_ambiguous(self) -> None:
        mod = _load()
        expression = mod.build_click_expression(text="Sign Up")

        self.assertIn("matches.length !== 1", expression)
        self.assertIn("ambiguous", expression)
        self.assertIn(json.dumps("Sign Up"), expression)
        self.assertIn("el.click()", expression)

    def test_click_expression_uses_selector_without_reading_secrets_or_storage(self) -> None:
        mod = _load()
        expression = mod.build_click_expression(selector='button[type="submit"]')

        forbidden = ["document.cookie", "localStorage", "sessionStorage", "Network.", "getAllCookies", ".value"]
        for token in forbidden:
            self.assertNotIn(token, expression)
        self.assertIn(json.dumps('button[type="submit"]'), expression)
        self.assertIn("scrollIntoView", expression)

    def test_extract_action_result_redacts_url_query_and_has_no_input_values(self) -> None:
        mod = _load()
        raw = {
            "result": {
                "result": {
                    "value": {
                        "ok": True,
                        "action": "click",
                        "url": "https://signin.example/u/signup?state=secret-state-token&x=abc",
                        "label": "Sign Up",
                        "tag": "A",
                    }
                }
            }
        }
        result = mod.extract_action_result(raw)

        self.assertEqual(result["url"], "https://signin.example/u/signup")
        self.assertNotIn("state", json.dumps(result).lower())
        self.assertNotIn("secret-state-token", json.dumps(result))
        self.assertNotIn("value", result)

    def test_fill_expression_does_not_return_field_value(self) -> None:
        mod = _load()
        expression = mod.build_fill_expression(selector='input[name="name"]', value="<researcher-alias> <program-slug>")

        self.assertIn(json.dumps('input[name="name"]'), expression)
        self.assertIn("value_length", expression)
        self.assertNotIn("document.cookie", expression)
        self.assertNotIn("localStorage", expression)
        self.assertNotIn("return {ok:true, action:'fill', value", expression)

    def test_cli_decodes_base64_text_argument(self) -> None:
        mod = _load()
        args = mod.parse_args(["--text-b64", "U2lnbiBVcA=="])

        self.assertEqual(args.text, "Sign Up")
        self.assertIsNone(args.selector)

    def test_cli_rejects_live_target_arguments(self) -> None:
        mod = _load()
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as ctx:
                mod.parse_args(["--target", "https://example.com", "--text", "Sign Up"])
        self.assertNotEqual(ctx.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
