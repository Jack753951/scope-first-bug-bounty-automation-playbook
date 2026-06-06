"""Tests for bounded/offline-safe Next.js <specific-cve-id> detector."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "nextjs_cve_2025_29927_detector.py"


def load_module():
    spec = importlib.util.spec_from_file_location("nextjs_cve_2025_29927_detector_under_test", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


class NextjsCve202529927DetectorTests(unittest.TestCase):
    def test_build_plan_is_offline_safe_bounded_and_candidate_only(self):
        module = load_module()
        plan = module.build_plan(
            base_url="https://target.example",
            paths=["/admin", "dashboard", "https://evil.example/nope"],
            method="GET",
            timeout=3.0,
        )

        self.assertEqual(plan["schema_version"], "nextjs_cve_2025_29927_detector/0.1")
        self.assertEqual(plan["run_mode"], "plan_only")
        self.assertFalse(plan["network_enabled"])
        self.assertEqual(plan["method"], "GET")
        self.assertLessEqual(plan["timeout_seconds"], 5.0)
        self.assertEqual(plan["paths"], ["/admin", "/dashboard"])
        self.assertEqual(module.normalize_paths(["C:/Program Files/Git/admin"]), ["/admin"])
        self.assertEqual(plan["requests_planned"], 4)
        self.assertEqual(plan["probe_header"], {"x-middleware-subrequest": "middleware:middleware:middleware:middleware:middleware"})
        self.assertFalse(plan["retains_response_bodies"])
        self.assertIn("candidate", json.dumps(plan).lower())
        for forbidden in ("confirmed", "verified", "exploited", "reportable", "pwned"):
            self.assertNotIn(forbidden, json.dumps(plan).lower())

    def test_detect_candidates_with_fake_fetcher_without_body_retention(self):
        module = load_module()
        calls = []

        def fake_fetch(url, *, method, headers, timeout):
            calls.append((url, method, dict(headers), timeout))
            is_probe = "x-middleware-subrequest" in headers
            if url.endswith("/admin") and not is_probe:
                return module.HttpObservation(status=307, headers={"location": "/login"}, body=b"secret login page")
            if url.endswith("/admin") and is_probe:
                return module.HttpObservation(status=200, headers={"content-type": "text/html"}, body=b"admin private content")
            return module.HttpObservation(status=404, headers={}, body=b"not found")

        result = module.detect(
            base_url="http://127.0.0.1:3000",
            paths=["/admin", "/missing"],
            method="GET",
            timeout=2.0,
            fetcher=fake_fetch,
        )

        self.assertEqual(result["run_mode"], "offline_fixture")
        self.assertEqual(result["summary"]["candidate_count"], 1)
        finding = result["findings"][0]
        self.assertEqual(finding["classification"], "candidate_middleware_bypass_indicator")
        self.assertEqual(finding["path"], "/admin")
        self.assertEqual(finding["baseline"]["status"], 307)
        self.assertEqual(finding["probe"]["status"], 200)
        rendered = json.dumps(result).lower()
        self.assertNotIn('"body":', rendered)
        self.assertNotIn("secret login page", rendered)
        self.assertNotIn("admin private content", rendered)
        self.assertIn("body_length", json.dumps(result))
        self.assertEqual(len(calls), 4)
        self.assertTrue(all(call[1] == "GET" for call in calls))
        self.assertTrue(any("x-middleware-subrequest" in call[2] for call in calls))

    def test_rejects_unsafe_methods_timeouts_and_execute_without_explicit_flags(self):
        module = load_module()
        with self.assertRaises(ValueError):
            module.build_plan("http://127.0.0.1:3000", ["/"], method="POST")
        with self.assertRaises(ValueError):
            module.build_plan("http://127.0.0.1:3000", ["/"], method="GET", timeout=30)

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "plan.json"
            code = module.main([
                "--base-url", "http://127.0.0.1:3000",
                "--path", "/admin",
                "--execute",
                "--output", str(out),
            ])
            self.assertEqual(code, 2)
            self.assertFalse(out.exists())

            code = module.main([
                "--base-url", "http://127.0.0.1:3000",
                "--path", "/admin",
                "--output", str(out),
            ])
            self.assertEqual(code, 0)
            saved = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(saved["run_mode"], "plan_only")
            self.assertFalse(saved["network_enabled"])


if __name__ == "__main__":
    unittest.main()
