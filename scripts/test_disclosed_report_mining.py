#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INGEST_PATH = ROOT / "scripts" / "ingest_disclosed_reports.py"
SCORE_PATH = ROOT / "scripts" / "score_disclosed_report_patterns.py"
SCHEMA_PATH = ROOT / "schemas" / "disclosed_report.schema.json"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


PUBLIC_REPORT_TEXT = """
<bug-bounty-platform> Report #12345: IDOR in organization invite role allowed a low-privilege user
from owned Account A to access an owned Account B workspace object via /api/v1/organizations/42/invites.
The researcher used two owned test accounts, screenshots, and a minimal STR. Impact was tenant boundary bypass.
Remediation: check object ownership and role before returning invite details. Severity: high.
Contact: researcher@example.com. Example token: h1_api_token_abc1234567890. OTP: 123456.
"""

PRIVATE_OR_LOGIN_TEXT = """
Please sign in to continue. Cloudflare CAPTCHA required. This page may include private program details,
bounty-only endpoint /admin/internal, and private rule text that must not be stored.
"""


class DisclosedReportIngestTests(unittest.TestCase):
    def test_schema_exists_with_offline_public_only_boundary(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.assertEqual(schema["title"], "Disclosed report normalized record")
        self.assertFalse(schema["properties"]["target_touching"]["const"])
        self.assertEqual(schema["properties"]["source_visibility"]["enum"], ["public", "needs_operator_or_browser_review"])

    def test_normalizes_public_report_with_sanitization_and_candidate_only_language(self) -> None:
        ingest = _load(INGEST_PATH, "ingest_disclosed_reports_for_tests")

        record = ingest.normalize_report_text(
            PUBLIC_REPORT_TEXT,
            source="<bug-bounty-platform>",
            url="https://<bug-bounty-platform>.com/reports/12345",
            title="IDOR in organization invite role",
        )

        self.assertEqual(record["schema_version"], "disclosed_report/0.1")
        self.assertEqual(record["source_visibility"], "public")
        self.assertFalse(record["target_touching"])
        self.assertEqual(record["status"], "ok")
        self.assertIn("idor", record["vulnerability_classes"])
        self.assertIn("org_role_invite_authz", record["primitives"])
        self.assertIn("owned_account_a_b", record["proof_shapes"])
        self.assertIn("tenant_boundary", record["impact_shapes"])
        self.assertIn("organization", record["product_surface_keywords"])
        self.assertIn("/api/v1/organizations/42/invites", record["route_patterns"])
        self.assertIn("clear_str", record["report_quality_signals"])
        self.assertIn("target-touching required", record["safety_tags"])
        rendered = json.dumps(record, ensure_ascii=False).lower()
        self.assertIn("[redacted_email]", rendered)
        self.assertIn("[redacted_secret]", rendered)
        self.assertNotIn("researcher@example.com", rendered)
        self.assertNotIn("h1_api_token_abc1234567890", rendered)
        self.assertNotIn("verified", rendered)
        self.assertNotIn("reportable", rendered)

    def test_login_or_private_page_fails_closed_for_operator_review(self) -> None:
        ingest = _load(INGEST_PATH, "ingest_disclosed_reports_private_for_tests")

        record = ingest.normalize_report_text(
            PRIVATE_OR_LOGIN_TEXT,
            source="intigriti",
            url="https://app.intigriti.com/researcher/programs/example/disclosed-reports/1",
            title="Private page",
        )

        self.assertEqual(record["status"], "needs_operator_or_browser_review")
        self.assertEqual(record["source_visibility"], "needs_operator_or_browser_review")
        self.assertFalse(record["target_touching"])
        self.assertEqual(record["vulnerability_classes"], [])
        rendered = json.dumps(record, ensure_ascii=False).lower()
        self.assertNotIn("private program details", rendered)
        self.assertNotIn("/admin/internal", rendered)
        self.assertNotIn("private rule text", rendered)
        self.assertIn("[private_or_login_gated_content_not_ingested]", record["summary"])
        self.assertIn("login_or_captcha_or_private_source", record["safety_tags"])
        self.assertIn("do_not_ingest_private_logged_in_content", record["blocked_actions"])

    def test_cli_ingests_jsonl_and_writes_normalized_json(self) -> None:
        ingest = _load(INGEST_PATH, "ingest_disclosed_reports_cli_for_tests")
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            source_path = td_path / "reports.jsonl"
            out_path = td_path / "normalized.json"
            source_path.write_text(
                "\n".join([
                    json.dumps({"source": "<bug-bounty-platform>", "url": "https://<bug-bounty-platform>.com/reports/12345", "title": "IDOR", "text": PUBLIC_REPORT_TEXT}),
                    json.dumps({"source": "intigriti", "url": "https://app.intigriti.com/private", "title": "Private", "text": PRIVATE_OR_LOGIN_TEXT}),
                ]),
                encoding="utf-8",
            )

            exit_code = ingest.main(["--input", str(source_path), "--output", str(out_path)])

            self.assertEqual(exit_code, 0)
            payload = json.loads(out_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["schema_version"], "disclosed_report_batch/0.1")
            self.assertFalse(payload["target_touching"])
            self.assertEqual(payload["record_count"], 2)
            self.assertEqual(payload["records"][0]["status"], "ok")
            self.assertEqual(payload["records"][1]["status"], "needs_operator_or_browser_review")


class DisclosedReportPatternScoreTests(unittest.TestCase):
    def test_scores_reusable_patterns_without_authorizing_live_actions(self) -> None:
        ingest = _load(INGEST_PATH, "ingest_disclosed_reports_for_score_tests")
        scorer = _load(SCORE_PATH, "score_disclosed_report_patterns_for_tests")
        records = [
            ingest.normalize_report_text(PUBLIC_REPORT_TEXT, source="<bug-bounty-platform>", url="https://<bug-bounty-platform>.com/reports/12345", title="IDOR"),
            ingest.normalize_report_text(
                "SSRF through webhook callback to collaborator used only an operator-controlled callback marker and no customer data.",
                source="bugcrowd",
                url="https://bugcrowd.com/disclosures/example",
                title="SSRF webhook callback",
            ),
        ]

        result = scorer.score_patterns(records)

        self.assertEqual(result["schema_version"], "disclosed_report_patterns/0.1")
        self.assertFalse(result["target_touching"])
        self.assertIn("No live target contact is authorized", result["boundary"])
        pattern_ids = {row["pattern_id"] for row in result["patterns"]}
        self.assertIn("primitive:org_role_invite_authz", pattern_ids)
        self.assertIn("primitive:ssrf_callback_marker", pattern_ids)
        for pattern in result["patterns"]:
            self.assertEqual(pattern["status"], "candidate_pattern")
            self.assertIn("scope_and_lane_gate_required", pattern["blocked_before"])
        rendered = json.dumps(result, ensure_ascii=False).lower()
        self.assertNotIn("verified", rendered)
        self.assertNotIn("reportable", rendered)

    def test_scorer_cli_accepts_ingest_batch_output(self) -> None:
        ingest = _load(INGEST_PATH, "ingest_disclosed_reports_for_scorer_cli_ingest")
        scorer = _load(SCORE_PATH, "score_disclosed_report_patterns_cli_for_tests")
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            batch_path = td_path / "batch.json"
            out_path = td_path / "patterns.json"
            batch = {
                "schema_version": "disclosed_report_batch/0.1",
                "target_touching": False,
                "record_count": 1,
                "records": [ingest.normalize_report_text(PUBLIC_REPORT_TEXT, source="<bug-bounty-platform>", url="https://<bug-bounty-platform>.com/reports/12345", title="IDOR")],
            }
            batch_path.write_text(json.dumps(batch), encoding="utf-8")

            exit_code = scorer.main(["--input", str(batch_path), "--output", str(out_path)])

            self.assertEqual(exit_code, 0)
            payload = json.loads(out_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["pattern_count"], len(payload["patterns"]))
            self.assertGreaterEqual(payload["pattern_count"], 1)


if __name__ == "__main__":
    unittest.main()
