"""Tests for the P3.11 SOC evidence-bucket synthetic fixture.

This test pins the fixture's *internal* shape, vocabulary, synthetic-range
posture, and absence of promotional/live strings. The fixture, the gap-code
vocabulary, the status vocabulary, and the evidence_confidence vocabulary
live only inside ``fixtures/soc_evidence_bucket/`` and this sibling test;
they are NOT a runtime contract and are not imported by any module runner,
report generator, scope helper, recon runtime, or other consumer.

The synthetic-range assertion is intentionally a negative test for the slice
boundary: if the fixture is ever mutated to embed a non-reserved IP such as
``8.8.8.8`` or any real public domain, ``test_network_ioc_values_are_synthetic_reserved_only``
and the related hostname assertions must fail closed. The README in the
fixture directory documents this expectation.

The test performs no network operation, no subprocess, no scanner/module
execution, and no filesystem write of any kind (test temporary directories
are not used because the test only reads the committed fixture).
"""

from __future__ import annotations

import ipaddress
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "fixtures" / "soc_evidence_bucket"
FIXTURE_PATH = FIXTURE_DIR / "sample_timeline_01.json"
README_PATH = FIXTURE_DIR / "README.md"

REQUIRED_TOP_KEYS = frozenset({"case_id", "description", "stages", "notes"})

REQUIRED_STAGE_FIELDS = (
    "stage_index",
    "stage_label",
    "timestamps",
    "assets",
    "user_account",
    "process_image",
    "command_line",
    "host_ioc",
    "network_ioc",
    "file_hashes",
    "source_uri",
    "destination_path",
    "attack_tactic",
    "attack_technique",
    "attack_subtechnique",
    "evidence_confidence",
    "description",
    "gap_codes",
    "status",
    "next_pivot_query",
)

REQUIRED_TIMESTAMP_FIELDS = ("event_observed", "event_role")

REQUIRED_ASSET_FIELDS = (
    "source_asset",
    "execution_asset",
    "target_asset",
    "affected_asset",
    "destination_asset",
)

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

ALLOWED_EVIDENCE_CONFIDENCE = frozenset({"low", "medium", "high"})

ALLOWED_IPV4_NETWORKS = (
    ipaddress.IPv4Network("192.0.2.0/24"),
    ipaddress.IPv4Network("198.51.100.0/24"),
    ipaddress.IPv4Network("203.0.113.0/24"),
)

ALLOWED_IPV6_NETWORKS = (ipaddress.IPv6Network("2001:db8::/32"),)

ALLOWED_DOMAIN_SUFFIXES = (
    ".example",
    ".invalid",
    ".test",
    ".localhost",
)

ALLOWED_DOMAIN_LITERALS = frozenset(
    {
        "example.tld",
        "example.invalid",
        "example.test",
        "example.example",
        "localhost",
    }
)

FORBIDDEN_KEY_NAMES = frozenset(
    {
        "confirmed_finding",
        "submit_ready",
        "report_ready",
        "live_target",
        "production",
        "real_target",
        "real_credential",
    }
)

FORBIDDEN_SUBSTRINGS = (
    "nuclei",
    "httpx",
    "subprocess",
    "requests.",
    "urllib",
    "socket.",
    "loot/",
    "tryhackme.com",
    "tryhackme.org",
    "trygovme.com",
    "trygovme.org",
    "<bug-bounty-platform>.com",
    "bugcrowd.com",
    "intigriti.com",
    "synack.com",
    "yeswehack.com",
    "http://",
    "https://",
    "ftp://",
)

SYNTHETIC_HASH_PREFIXES = ("0000", "dead")
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
HOSTNAME_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?$")


def _is_reserved_hostname(value: str) -> bool:
    if not isinstance(value, str) or not value:
        return False
    candidate = value.strip().lower()
    if candidate in ALLOWED_DOMAIN_LITERALS:
        return True
    if not HOSTNAME_RE.match(candidate):
        return False
    if "." not in candidate:
        return False
    return any(candidate.endswith(suffix) for suffix in ALLOWED_DOMAIN_SUFFIXES)


class SocEvidenceBucketFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture_text = FIXTURE_PATH.read_text(encoding="utf-8")
        cls.fixture = json.loads(cls.fixture_text)
        cls.stages = cls.fixture["stages"]
        cls.readme_text = README_PATH.read_text(encoding="utf-8")

    def _walk_keys(self, obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                yield k
                yield from self._walk_keys(v)
        elif isinstance(obj, list):
            for item in obj:
                yield from self._walk_keys(item)

    def test_fixture_parses_as_json_and_has_required_top_keys(self):
        self.assertIsInstance(self.fixture, dict)
        self.assertTrue(
            REQUIRED_TOP_KEYS.issubset(set(self.fixture)),
            f"missing top-level keys: {REQUIRED_TOP_KEYS - set(self.fixture)}",
        )
        self.assertIsInstance(self.stages, list)
        self.assertGreaterEqual(
            len(self.stages),
            4,
            "fixture must contain at least 4 stages to demonstrate a multi-stage timeline",
        )

    def test_each_stage_carries_every_required_field(self):
        for stage in self.stages:
            with self.subTest(stage_index=stage.get("stage_index")):
                self.assertIsInstance(stage, dict)
                for field in REQUIRED_STAGE_FIELDS:
                    self.assertIn(field, stage, f"missing field {field!r}")
                self.assertIsInstance(stage["timestamps"], dict)
                for tf in REQUIRED_TIMESTAMP_FIELDS:
                    self.assertIn(tf, stage["timestamps"])
                self.assertIsInstance(stage["assets"], dict)
                for af in REQUIRED_ASSET_FIELDS:
                    self.assertIn(af, stage["assets"])
                self.assertIsInstance(stage["host_ioc"], list)
                self.assertIsInstance(stage["network_ioc"], list)
                self.assertIsInstance(stage["file_hashes"], list)
                self.assertIsInstance(stage["gap_codes"], list)
                self.assertIsInstance(stage["stage_index"], int)
                self.assertIsInstance(stage["stage_label"], str)

    def test_gap_codes_use_only_allowed_in_fixture_vocabulary(self):
        seen_any = False
        for stage in self.stages:
            for code in stage["gap_codes"]:
                seen_any = True
                with self.subTest(stage_index=stage["stage_index"], code=code):
                    self.assertIn(code, ALLOWED_GAP_CODES)
        self.assertTrue(seen_any, "fixture must exercise at least one gap_code")

    def test_status_uses_only_non_promotional_vocabulary(self):
        for stage in self.stages:
            with self.subTest(stage_index=stage["stage_index"]):
                self.assertIn(stage["status"], ALLOWED_STATUSES)

    def test_evidence_confidence_uses_only_allowed_values(self):
        for stage in self.stages:
            with self.subTest(stage_index=stage["stage_index"]):
                self.assertIn(stage["evidence_confidence"], ALLOWED_EVIDENCE_CONFIDENCE)

    def test_network_ioc_values_are_synthetic_reserved_only(self):
        """Negative-test contract: substituting a non-reserved IP must fail.

        Every ``network_ioc`` entry must be an IPv4 address inside RFC 5737
        documentation ranges (192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24)
        or an IPv6 address inside the RFC 3849 documentation range
        (2001:db8::/32). If the fixture is mutated to include a non-reserved
        address such as 8.8.8.8 or 1.1.1.1, this test must fail closed.
        """
        for stage in self.stages:
            for raw in stage["network_ioc"]:
                with self.subTest(stage_index=stage["stage_index"], raw=raw):
                    self.assertIsInstance(raw, str)
                    addr = ipaddress.ip_address(raw)
                    if isinstance(addr, ipaddress.IPv4Address):
                        self.assertTrue(
                            any(addr in net for net in ALLOWED_IPV4_NETWORKS),
                            f"IPv4 {raw!r} is not inside RFC 5737 reserved ranges",
                        )
                    else:
                        self.assertTrue(
                            any(addr in net for net in ALLOWED_IPV6_NETWORKS),
                            f"IPv6 {raw!r} is not inside RFC 3849 reserved range",
                        )

    def test_host_ioc_hostnames_are_reserved_example_only(self):
        for stage in self.stages:
            for raw in stage["host_ioc"]:
                with self.subTest(stage_index=stage["stage_index"], raw=raw):
                    self.assertIsInstance(raw, str)
                    self.assertTrue(
                        _is_reserved_hostname(raw),
                        f"host_ioc {raw!r} is not in allowed example/reserved namespace",
                    )

    def test_asset_hostnames_are_reserved_example_only(self):
        for stage in self.stages:
            assets = stage["assets"]
            for role, value in assets.items():
                with self.subTest(stage_index=stage["stage_index"], role=role, value=value):
                    if value is None or value == "":
                        continue
                    self.assertIsInstance(value, str)
                    self.assertTrue(
                        _is_reserved_hostname(value),
                        f"asset {role!r}={value!r} is not in allowed example/reserved namespace",
                    )

    def test_source_uri_uses_only_reserved_example_hostnames(self):
        for stage in self.stages:
            raw = stage["source_uri"]
            with self.subTest(stage_index=stage["stage_index"], raw=raw):
                self.assertIsInstance(raw, str)
                if raw == "":
                    continue
                self.assertNotIn("://", raw, "source_uri must be scheme-less in this fixture")
                host = raw.split("/", 1)[0]
                self.assertTrue(
                    _is_reserved_hostname(host),
                    f"source_uri host {host!r} is not in allowed example/reserved namespace",
                )

    def test_file_hashes_are_synthetic_sha256_with_fixture_only_prefix(self):
        for stage in self.stages:
            for h in stage["file_hashes"]:
                with self.subTest(stage_index=stage["stage_index"], hash=h):
                    self.assertIsInstance(h, str)
                    self.assertRegex(h, HEX64_RE)
                    self.assertTrue(
                        any(h.startswith(prefix) for prefix in SYNTHETIC_HASH_PREFIXES),
                        f"hash {h!r} does not start with a documented fixture-only "
                        f"prefix {SYNTHETIC_HASH_PREFIXES!r}",
                    )

    def test_forbidden_promotional_or_live_keys_are_absent(self):
        seen_keys = set(self._walk_keys(self.fixture))
        for key in FORBIDDEN_KEY_NAMES:
            with self.subTest(key=key):
                self.assertNotIn(
                    key,
                    seen_keys,
                    f"fixture must not contain promotional/live key {key!r}",
                )

    def test_forbidden_live_or_action_strings_are_absent(self):
        lowered = self.fixture_text.lower()
        for needle in FORBIDDEN_SUBSTRINGS:
            with self.subTest(needle=needle):
                self.assertNotIn(
                    needle,
                    lowered,
                    f"fixture text must not contain forbidden live/action string {needle!r}",
                )

    def test_readme_states_synthetic_and_non_contract_posture(self):
        lowered = self.readme_text.lower()
        for phrase in ("synthetic", "non-promotional", "not a contract", "offline"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, lowered, f"README must state posture: {phrase!r}")
        for needle in FORBIDDEN_SUBSTRINGS:
            if needle in {"tryhackme.com", "tryhackme.org", "trygovme.com", "trygovme.org",
                          "<bug-bounty-platform>.com", "bugcrowd.com", "intigriti.com", "synack.com",
                          "yeswehack.com", "http://", "https://", "ftp://"}:
                with self.subTest(needle=needle):
                    self.assertNotIn(needle, lowered, f"README must not contain {needle!r}")


if __name__ == "__main__":
    unittest.main()
