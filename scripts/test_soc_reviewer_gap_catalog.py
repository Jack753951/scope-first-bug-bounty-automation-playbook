"""Tests for the P3.12 SOC reviewer-gap catalog (offline, non-contractual).

The catalog at ``fixtures/soc_evidence_bucket/reviewer_gap_catalog.{md,json}``
is a synthetic, trial, calibration-only companion artifact to the P3.11
SOC evidence-bucket fixture. The catalog is not loaded by any runtime
consumer; the only consumer is this test, which asserts well-formedness
and vocabulary equality with the P3.11 fixture.

Negative drift contract: if a gap code is added to the catalog without
also being added to the P3.11 fixture vocabulary (or vice versa), or if
the catalog's allowed-response-postures drift from the fixture's
non-promotional status vocabulary, these tests must fail closed.

This test imports only standard library modules and deliberately does
not reference any candidate-workflow chain consumer or runtime helper.
The list of forbidden chain-consumer tokens lives in the
FORBIDDEN_CONSUMER_TOKENS_IN_TEST_SOURCE constant below, and each token
must appear only inside that constant's string-literal entries.
"""

from __future__ import annotations

import ast
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "fixtures" / "soc_evidence_bucket"
CATALOG_JSON_PATH = FIXTURE_DIR / "reviewer_gap_catalog.json"
CATALOG_MD_PATH = FIXTURE_DIR / "reviewer_gap_catalog.md"
P3_11_FIXTURE_TEST_PATH = ROOT / "scripts" / "test_soc_evidence_bucket_fixture.py"

EXPECTED_SCHEMA_MARKER = "soc_reviewer_gap_catalog_v0_trial"
EXPECTED_ENTRY_ID_PREFIX = "p3_12_prompt_"
EXPECTED_ENTRY_COUNT = 12
PROMPT_TEXT_MAX_LEN = 300

ALLOWED_GAP_CODES = frozenset(
    {
        "MISSING_HOST_IOC",
        "MISSING_NETWORK_IOC",
        "MISSING_HASH",
        "MISSING_SOURCE_URL",
        "MISSING_DESTINATION_PATH",
        "MISSING_COMMAND_LINE",
        "MISSING_FOLLOW_ON_IMPLICATION",
        "PARENT_TECHNIQUE_TOO_BROAD",
        "TACTIC_MISMATCH",
        "ASSET_ROLE_AMBIGUOUS",
        "TIMESTAMP_EVENT_ROLE_MISMATCH",
        "NEEDS_SECOND_PASS_HUNT",
    }
)

ALLOWED_STATUSES = frozenset(
    {
        "needs_more_evidence",
        "needs_mapping_review",
        "needs_asset_reconciliation",
        "needs_second_pass_hunt",
        "not_report_ready",
    }
)

SNAKE_CASE_RE = re.compile(r"^[a-z][a-z0-9_]*[a-z0-9]$")

FORBIDDEN_PROMPT_SUBSTRINGS = (
    "submit_ready",
    "report_ready",
    "confirmed_finding",
    "live_target",
    "production",
    "real_target",
    "real_credential",
    "severity",
    "cvss",
    "impact_score",
    "triaged",
    "accepted",
    "resolved",
    "informative",
    "won_t_fix",
    "not_applicable",
    "cve",
    "cwe",
    "epss",
    "nuclei",
    "httpx",
    "subfinder",
    "naabu",
    "katana",
    "ffuf",
    "dnsx",
    "subprocess",
    "requests.",
    "urllib",
    "socket.",
    "loot/",
    "http://",
    "https://",
    "ftp://",
    "elastic",
    "kibana",
    "splunk",
    "siem",
    "tryhackme",
    "trygovme",
    "<bug-bounty-platform>",
    "bugcrowd",
    "intigriti",
    "synack",
    "yeswehack",
)

# `duplicate` is a forbidden submission-lifecycle term per the §6.8 negative
# vocabulary lock; assert it does not appear as a whole word in prompt_text.
FORBIDDEN_PROMPT_WHOLE_WORDS = (
    "duplicate",
)

FORBIDDEN_MARKDOWN_SUBSTRINGS = (
    "http://",
    "https://",
    "ftp://",
    "nuclei",
    "httpx",
    "subfinder",
    "naabu",
    "katana",
    "ffuf",
    "dnsx",
    "tryhackme.com",
    "tryhackme.org",
    "trygovme.com",
    "trygovme.org",
    "<bug-bounty-platform>.com",
    "bugcrowd.com",
    "intigriti.com",
    "synack.com",
    "yeswehack.com",
)

FORBIDDEN_CONSUMER_TOKENS_IN_TEST_SOURCE = (
    "build_candidate_review_packet",
    "review_candidate_packet_gaps",
    "build_candidate_verification_plan",
    "build_report_readiness_gate",
    "build_candidate_workflow_fixture",
    "module_runner",
    "recon",
)

REQUIRED_MARKDOWN_PHRASES = (
    "synthetic",
    "non-promotional",
    "not a contract",
    "offline",
    "companion artifact",
)


def _literal_frozenset_assignment(source_text: str, variable_name: str) -> frozenset[str]:
    """Extract a literal ``frozenset({...})`` assignment from a test source file.

    This keeps the P3.12 drift lock symmetric without importing the P3.11
    test module. If P3.11 adds or removes a vocabulary item, this helper lets
    the catalog test compare exact sets and fail closed on either-side drift.
    """

    module = ast.parse(source_text)
    for node in module.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == variable_name for target in node.targets):
            continue

        value = node.value
        if (
            isinstance(value, ast.Call)
            and isinstance(value.func, ast.Name)
            and value.func.id == "frozenset"
            and len(value.args) == 1
        ):
            literal = ast.literal_eval(value.args[0])
        else:
            literal = ast.literal_eval(value)

        if not isinstance(literal, (set, frozenset)):
            raise AssertionError(f"{variable_name} must be a literal set/frozenset")
        if not all(isinstance(item, str) for item in literal):
            raise AssertionError(f"{variable_name} must contain only string literals")
        return frozenset(literal)

    raise AssertionError(f"{variable_name} assignment not found in P3.11 fixture test")


class SocReviewerGapCatalogTests(unittest.TestCase):
    """P3.12 catalog well-formedness and cross-file vocabulary lock.

    Negative drift contract: adding a gap_code to the catalog without
    also adding it to the P3.11 fixture vocabulary, or vice versa, must
    fail closed under these tests. The same is true for any drift in
    the allowed non-promotional status vocabulary.
    """

    @classmethod
    def setUpClass(cls):
        cls.catalog_text = CATALOG_JSON_PATH.read_text(encoding="utf-8")
        cls.catalog = json.loads(cls.catalog_text)
        cls.entries = cls.catalog["entries"]
        cls.markdown_text = CATALOG_MD_PATH.read_text(encoding="utf-8")
        cls.p3_11_test_text = P3_11_FIXTURE_TEST_PATH.read_text(encoding="utf-8")
        cls.p3_11_gap_codes = _literal_frozenset_assignment(cls.p3_11_test_text, "ALLOWED_GAP_CODES")
        cls.p3_11_statuses = _literal_frozenset_assignment(cls.p3_11_test_text, "ALLOWED_STATUSES")
        cls.test_source_text = Path(__file__).read_text(encoding="utf-8")

    def test_catalog_parses_and_has_required_top_shape(self):
        self.assertIsInstance(self.catalog, dict)
        self.assertEqual(
            set(self.catalog),
            {"schema_marker", "version", "entries"},
            "top-level must be exactly schema_marker / version / entries",
        )
        self.assertIsInstance(self.entries, list)
        self.assertEqual(
            len(self.entries),
            EXPECTED_ENTRY_COUNT,
            f"catalog must contain exactly {EXPECTED_ENTRY_COUNT} entries",
        )

    def test_schema_marker_is_flat_trial_marker(self):
        marker = self.catalog["schema_marker"]
        self.assertIsInstance(marker, str)
        self.assertEqual(marker, EXPECTED_SCHEMA_MARKER)
        self.assertIn("trial", marker)
        self.assertNotIn("/", marker, "schema_marker must be flat, not slash-shaped")

    def test_version_is_zero(self):
        version = self.catalog["version"]
        self.assertEqual(version, 0, "version must be 0 (integer)")
        self.assertIsInstance(version, int)
        self.assertNotIsInstance(version, bool)

    def test_entry_ids_unique_sorted_snake_case_prefixed(self):
        ids = [entry["id"] for entry in self.entries]
        self.assertEqual(len(ids), len(set(ids)), "entry ids must be unique")
        self.assertEqual(ids, sorted(ids), "entries must be sorted by id")
        for entry_id in ids:
            with self.subTest(entry_id=entry_id):
                self.assertIsInstance(entry_id, str)
                self.assertTrue(
                    entry_id.startswith(EXPECTED_ENTRY_ID_PREFIX),
                    f"id {entry_id!r} must start with {EXPECTED_ENTRY_ID_PREFIX!r}",
                )
                self.assertRegex(entry_id, SNAKE_CASE_RE)

    def test_entry_gap_codes_cover_allowed_vocabulary_exactly_once(self):
        gap_codes = [entry["gap_code"] for entry in self.entries]
        self.assertEqual(
            len(gap_codes),
            len(set(gap_codes)),
            "each gap_code must appear in exactly one catalog entry",
        )
        self.assertEqual(
            set(gap_codes),
            set(ALLOWED_GAP_CODES),
            "catalog gap_code set must equal the P3.11 allowed vocabulary exactly",
        )

    def test_gap_code_vocabulary_is_exactly_equal_to_p3_11_test_source(self):
        """Symmetric drift lock between the P3.11 fixture test and catalog.

        Adding a gap code on either side without updating the other side must
        fail closed; substring presence alone is not sufficient.
        """
        self.assertEqual(
            ALLOWED_GAP_CODES,
            self.p3_11_gap_codes,
            "P3.12 local gap-code vocabulary must exactly equal P3.11 fixture-test vocabulary",
        )
        catalog_gap_codes = frozenset(entry["gap_code"] for entry in self.entries)
        self.assertEqual(
            catalog_gap_codes,
            self.p3_11_gap_codes,
            "catalog gap_code set must exactly equal P3.11 fixture-test vocabulary",
        )

    def test_status_vocabulary_is_exactly_equal_to_p3_11_test_source(self):
        self.assertEqual(
            ALLOWED_STATUSES,
            self.p3_11_statuses,
            "P3.12 local status vocabulary must exactly equal P3.11 fixture-test vocabulary",
        )
        catalog_postures = frozenset(
            posture for entry in self.entries for posture in entry["allowed_response_postures"]
        )
        self.assertTrue(
            catalog_postures.issubset(self.p3_11_statuses),
            "catalog postures must stay within P3.11 non-promotional status vocabulary",
        )
        self.assertEqual(
            catalog_postures,
            self.p3_11_statuses,
            "catalog should exercise every P3.11 non-promotional status at least once",
        )

    def test_entry_allowed_response_postures_are_non_empty_subset(self):
        for entry in self.entries:
            with self.subTest(entry_id=entry["id"]):
                postures = entry["allowed_response_postures"]
                self.assertIsInstance(postures, list)
                self.assertGreater(len(postures), 0, "must be non-empty")
                self.assertEqual(
                    len(postures),
                    len(set(postures)),
                    "postures within one entry must not repeat",
                )
                for posture in postures:
                    self.assertIsInstance(posture, str)
                    self.assertIn(
                        posture,
                        ALLOWED_STATUSES,
                        f"posture {posture!r} not in allowed non-promotional vocabulary",
                    )

    def test_entry_keys_are_closed_and_minimal(self):
        allowed_required = {"id", "gap_code", "prompt_text", "allowed_response_postures"}
        allowed_optional = {"metadata"}
        for entry in self.entries:
            with self.subTest(entry_id=entry.get("id")):
                keys = set(entry)
                self.assertTrue(
                    allowed_required.issubset(keys),
                    f"entry missing required keys: {allowed_required - keys}",
                )
                extra = keys - allowed_required - allowed_optional
                self.assertFalse(
                    extra,
                    f"entry has unexpected keys: {extra}",
                )
                if "metadata" in entry:
                    self.assertIsInstance(entry["metadata"], dict)
                    for k, v in entry["metadata"].items():
                        self.assertIsInstance(k, str)
                        self.assertNotIsInstance(
                            v,
                            (dict, list),
                            "metadata must be a flat map (no nested dict/list)",
                        )

    def test_prompt_text_is_short_neutral_evidence_completeness_question(self):
        for entry in self.entries:
            with self.subTest(entry_id=entry["id"]):
                prompt = entry["prompt_text"]
                self.assertIsInstance(prompt, str)
                self.assertGreater(len(prompt.strip()), 0, "prompt_text must be non-empty")
                self.assertLessEqual(
                    len(prompt),
                    PROMPT_TEXT_MAX_LEN,
                    f"prompt_text must be <= {PROMPT_TEXT_MAX_LEN} chars",
                )
                lowered = prompt.lower()
                for needle in FORBIDDEN_PROMPT_SUBSTRINGS:
                    self.assertNotIn(
                        needle,
                        lowered,
                        f"prompt_text contains forbidden substring {needle!r}",
                    )
                for word in FORBIDDEN_PROMPT_WHOLE_WORDS:
                    pattern = re.compile(rf"\b{re.escape(word)}\b", re.IGNORECASE)
                    self.assertIsNone(
                        pattern.search(prompt),
                        f"prompt_text contains forbidden whole word {word!r}",
                    )

    def test_json_round_trip_is_stable(self):
        reloaded = json.loads(self.catalog_text)
        canonical = json.dumps(reloaded, sort_keys=True, indent=2) + "\n"
        self.assertEqual(
            canonical,
            self.catalog_text,
            "catalog JSON must equal json.dumps(..., sort_keys=True, indent=2) + LF",
        )

    def test_catalog_has_no_byte_order_mark(self):
        with CATALOG_JSON_PATH.open("rb") as fh:
            head = fh.read(3)
        self.assertNotEqual(head, b"\xef\xbb\xbf", "JSON must be UTF-8 without BOM")

    def test_test_source_imports_only_stdlib_and_avoids_chain_consumers(self):
        """Stand-alone consumer property: the test must not import any
        chain consumer, runtime helper, or non-stdlib module.
        """
        import_lines = [
            line.strip()
            for line in self.test_source_text.splitlines()
            if line.strip().startswith(("import ", "from "))
        ]
        allowed_modules = {"ast", "json", "re", "unittest", "pathlib", "__future__"}
        for line in import_lines:
            with self.subTest(line=line):
                if line.startswith("from "):
                    module = line.split()[1]
                else:
                    module = line.split()[1].split(".")[0]
                self.assertIn(
                    module.split(".")[0],
                    allowed_modules,
                    f"test must import only stdlib modules, found {module!r}",
                )
        for forbidden in FORBIDDEN_CONSUMER_TOKENS_IN_TEST_SOURCE:
            with self.subTest(forbidden=forbidden):
                whole_word = re.compile(rf"\b{re.escape(forbidden)}\b")
                whole_word_matches = whole_word.findall(self.test_source_text)
                quoted_in_tuple = self.test_source_text.count(f'"{forbidden}"')
                self.assertEqual(
                    len(whole_word_matches),
                    quoted_in_tuple,
                    f"test source must not reference chain consumer {forbidden!r} "
                    f"outside the forbidden-token constant declaration",
                )

    def test_markdown_sibling_states_required_posture(self):
        lowered = self.markdown_text.lower()
        for phrase in REQUIRED_MARKDOWN_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertIn(
                    phrase,
                    lowered,
                    f"Markdown sibling must state posture phrase {phrase!r}",
                )
        self.assertIn(
            "templates/report_readiness_reviewer_prompts.json",
            self.markdown_text,
            "Markdown must cross-link to report_readiness_reviewer_prompts.json",
        )
        self.assertIn(
            "parallel pattern reference",
            lowered,
            "Markdown must declare report-readiness catalog as a parallel pattern reference",
        )

    def test_markdown_has_no_url_scheme_or_real_platform_reference(self):
        lowered = self.markdown_text.lower()
        for needle in FORBIDDEN_MARKDOWN_SUBSTRINGS:
            with self.subTest(needle=needle):
                self.assertNotIn(
                    needle,
                    lowered,
                    f"Markdown sibling must not contain {needle!r}",
                )


if __name__ == "__main__":
    unittest.main()
