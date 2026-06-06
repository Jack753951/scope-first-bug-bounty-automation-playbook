"""Tests for the P3.5 report-readiness reviewer prompt catalog."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "templates" / "report_readiness_reviewer_prompts.json"
GATE_PATH = ROOT / "scripts" / "build_report_readiness_gate.py"
GAP_PATH = ROOT / "scripts" / "review_candidate_packet_gaps.py"

GATE_ACTION_ORDER = (
    "GATE_COLLECT_EVIDENCE",
    "GATE_COMPLETE_MANUAL_CHECKS",
    "GATE_ADD_SCOPE_REVIEW",
    "GATE_ADD_REMEDIATION_GUIDANCE",
    "GATE_ADD_VERIFICATION_GUIDANCE",
    "GATE_ADD_HUMAN_REVIEW_DECISION",
    "GATE_KEEP_OUT_OF_REPORT",
)

BLOCK_REASON_ORDER = (
    "BLOCK_MISSING_EVIDENCE",
    "BLOCK_LOW_CONFIDENCE",
    "BLOCK_INFO_SEVERITY",
    "BLOCK_MANUAL_VERIFICATION_REQUIRED",
    "BLOCK_SCANNER_OUTPUT_ONLY",
    "BLOCK_MISSING_REMEDIATION",
    "BLOCK_MISSING_VERIFICATION_GUIDANCE",
    "BLOCK_MISSING_SCOPE_REVIEW_QUESTION",
)

CHECK_CODES = (
    "CHECK_MISSING_EVIDENCE",
    "CHECK_LOW_CONFIDENCE",
    "CHECK_INFO_SEVERITY_RATIONALE",
    "CHECK_MANUAL_VERIFICATION_NOTES",
    "CHECK_NON_SCANNER_CORROBORATION",
    "CHECK_HUMAN_REMEDIATION_GUIDANCE",
    "CHECK_SAFE_MANUAL_CHECKLIST",
    "CHECK_SCOPE_REVIEW_QUESTION",
    "CHECK_REVIEWER_DECISION",
)

ALLOWED_RESPONSE_POSTURES = frozenset(
    {
        "still_blocked",
        "still_needs_manual_review",
        "needs_more_evidence",
        "defer",
    }
)

FORBIDDEN_WHOLE_WORDS = (
    "confirmed",
    "verified",
    "valid",
    "validated",
    "ready_for_submission",
    "accepted",
    "duplicate_confirmed",
    "false_positive",
    "risk_accepted",
    "mitigated",
    "triaged",
    "resolved",
    "disclosed",
    "submitted",
    "published",
    "reportable",
    "weaponizable",
    "fail",
    "pass",
    "informative",
    "not_applicable",
    "won_t_fix",
)

FORBIDDEN_KEY_NAMES = {
    "title",
    "summary",
    "impact_narrative",
    "steps_to_reproduce",
    "remediation_prose",
    "submission_text",
    "report_body",
    "report_draft",
    "program_handle",
    "engagement",
    "bounty_amount",
    "disclosed_at",
    "triage_state",
    "submission_id",
    "cve_assignment",
    "vrt_category",
    "vrt_id",
    "dedupe_hash",
    "template_id",
    "matched_at",
    "matcher_name",
    "template_path",
    "tool_name",
    "scanner_name",
    "rule_id",
    "severity",
    "level",
    "risk",
    "confidence_score",
    "cvss",
    "epss",
}

FORBIDDEN_SUBSTRINGS = (
    "<bug-bounty-platform>",
    "bugcrowd",
    "defectdojo",
    "intigriti",
    "synack",
    "yeswehack",
    "http://",
    "https://",
    "ftp://",
    "://",
    "oast.",
    "interactsh.",
    "burpcollaborator.",
    "ngrok.",
    "webhook.",
    "requestbin.",
    "--target",
    "--url",
    "--host",
    "--scope",
    "--live",
)


class ReportReadinessReviewerPromptCatalogTests(unittest.TestCase):
    def _catalog_text(self) -> str:
        return CATALOG_PATH.read_text(encoding="utf-8")

    def _catalog(self) -> dict:
        return json.loads(self._catalog_text())

    def _entries(self) -> list[dict]:
        entries = self._catalog()["entries"]
        self.assertIsInstance(entries, list)
        return entries

    def test_catalog_parses_and_uses_canonical_json_format(self):
        text = self._catalog_text()
        catalog = json.loads(text)
        self.assertIsInstance(catalog, dict)
        self.assertEqual(set(catalog), {"schema_marker", "version", "notes", "entries"})
        canonical = json.dumps(catalog, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
        self.assertEqual(text, canonical)

    def test_schema_marker_is_flat_trial_marker_not_slash_schema_version(self):
        catalog = self._catalog()
        self.assertEqual(catalog["schema_marker"], "report_readiness_reviewer_prompts_v0_trial")
        self.assertIn("trial", catalog["schema_marker"])
        self.assertNotIn("/", catalog["schema_marker"])
        self.assertEqual(catalog["version"], 0)

    def test_entries_cover_existing_gate_block_and_check_codes(self):
        gate_actions = set()
        block_reasons = set()
        check_codes = set()
        for entry in self._entries():
            applies_to = entry["applies_to"]
            gate_actions.update(applies_to["gate_actions"])
            block_reasons.update(applies_to["block_reasons"])
            check_codes.update(applies_to["check_codes"])
        self.assertEqual(gate_actions, set(GATE_ACTION_ORDER))
        self.assertEqual(block_reasons, set(BLOCK_REASON_ORDER))
        self.assertEqual(check_codes, set(CHECK_CODES))

    def test_allowed_response_postures_are_closed_non_promotional_set(self):
        for entry in self._entries():
            with self.subTest(entry=entry["id"]):
                postures = entry["allowed_response_postures"]
                self.assertIsInstance(postures, list)
                self.assertGreater(len(postures), 0)
                self.assertEqual(len(postures), len(set(postures)))
                self.assertTrue(set(postures).issubset(ALLOWED_RESPONSE_POSTURES))

    def test_entry_ids_are_unique_stable_and_sorted(self):
        ids = [entry["id"] for entry in self._entries()]
        self.assertEqual(ids, sorted(ids))
        self.assertEqual(len(ids), len(set(ids)))
        for entry_id in ids:
            self.assertRegex(entry_id, r"^p3_5_prompt_[a-z0-9_]+$")

    def test_catalog_rejects_forbidden_vocabulary_fields_urls_and_live_flags(self):
        text = self._catalog_text().lower()
        for word in FORBIDDEN_WHOLE_WORDS:
            with self.subTest(word=word):
                self.assertIsNone(re.search(rf"\b{re.escape(word)}\b", text))
        for substring in FORBIDDEN_SUBSTRINGS:
            with self.subTest(substring=substring):
                self.assertNotIn(substring, text)

    def test_catalog_rejects_drafting_platform_scanner_and_severity_axis_keys(self):
        def walk_keys(value):
            if isinstance(value, dict):
                for key, child in value.items():
                    yield key
                    yield from walk_keys(child)
            elif isinstance(value, list):
                for child in value:
                    yield from walk_keys(child)

        keys = {key.lower() for key in walk_keys(self._catalog())}
        self.assertTrue(keys.isdisjoint(FORBIDDEN_KEY_NAMES), keys & FORBIDDEN_KEY_NAMES)

    def test_chain_vocabulary_sources_still_expose_expected_constants(self):
        gate_text = GATE_PATH.read_text(encoding="utf-8")
        gap_text = GAP_PATH.read_text(encoding="utf-8")
        self.assertIn("GATE_ACTION_ORDER = (", gate_text)
        self.assertIn("BLOCK_REASON_ORDER = (", gate_text)
        self.assertIn("CHECK_TO_ACTION = {", gate_text)
        self.assertIn("LIVE_TARGET_FLAGS = frozenset", gate_text)
        self.assertIn("LIVE_TARGET_FLAGS = frozenset", gap_text)


if __name__ == "__main__":
    unittest.main()
