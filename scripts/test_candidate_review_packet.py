"""Focused tests for the offline P2.19 candidate review packet builder."""

from __future__ import annotations

import ast
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILDER_PATH = ROOT / "scripts" / "build_candidate_review_packet.py"
TEST_PATH = Path(__file__).resolve()
SECURITY_HEADERS_FIXTURE_ROOT = ROOT / "tests" / "fixtures" / "security_headers_baseline"
SELF_TEST_FIXTURE_ROOT = ROOT / "tests" / "fixtures" / "candidate_review_packet"
SCHEMA_VERSION_LITERAL = "candidate_review_packet/0.1-trial"
P3_1_CURATED_INPUTS = [
    "tests/fixtures/candidate_review_packet/p3_1_curated_partial_evidence/expected_findings.json",
    "tests/fixtures/candidate_review_packet/p3_1_curated_ambiguous_scope_text/expected_findings.json",
    "tests/fixtures/candidate_review_packet/p3_1_curated_chained_precondition/expected_findings.json",
    "tests/fixtures/candidate_review_packet/p3_1_curated_low_signal_informational/expected_findings.json",
    "tests/fixtures/candidate_review_packet/p3_1_curated_duplicate_pair/expected_findings.json",
    "tests/fixtures/candidate_review_packet/p3_1_curated_non_finding_control/expected_findings.json",
]
PLATFORM_BLOCKLIST = tuple(
    "".join(parts)
    for parts in (
        ("hack", "erone"),
        ("bug", "crowd"),
        ("syn", "ack"),
        ("inti", "griti"),
        ("yes", "we", "hack"),
    )
)


def _load_builder():
    spec = importlib.util.spec_from_file_location(
        "build_candidate_review_packet_under_test", BUILDER_PATH
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


builder = _load_builder()


def _build(*inputs: str) -> dict:
    return builder.build_packet(str(ROOT), list(inputs))


def _snapshot_tree(root: Path) -> dict[str, tuple[int, int]]:
    snapshot: dict[str, tuple[int, int]] = {}
    if not root.exists():
        return snapshot
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        stat = path.stat()
        snapshot[str(path.relative_to(root))] = (stat.st_size, stat.st_mtime_ns)
    return snapshot


def _expected_finding_count(fixture: Path) -> int:
    return len(json.loads(fixture.read_text(encoding="utf-8")))


class HappyPathTests(unittest.TestCase):
    def test_happy_path_multiple_security_headers_fixtures(self):
        inputs = [
            "tests/fixtures/security_headers_baseline/all_headers_absent/expected_findings.json",
            "tests/fixtures/security_headers_baseline/weak_csp/expected_findings.json",
        ]
        packet = _build(*inputs)
        self.assertEqual(packet["status"], "ok", packet)
        self.assertEqual(packet["errors"], [])
        self.assertEqual(packet["schema_version"], SCHEMA_VERSION_LITERAL)
        expected_count = sum(
            _expected_finding_count(ROOT / rel) for rel in inputs
        )
        self.assertEqual(packet["summary"]["candidate_count"], expected_count)
        self.assertEqual(packet["summary"]["input_count"], len(inputs))
        self.assertEqual(packet["summary"]["modules"], ["level1.security_headers_baseline"])
        self.assertEqual(
            sorted(packet["summary"]["targets"]),
            packet["summary"]["targets"],
        )

    def test_single_file_happy_path(self):
        rel = "tests/fixtures/security_headers_baseline/weak_csp/expected_findings.json"
        packet = _build(rel)
        self.assertEqual(packet["status"], "ok")
        self.assertEqual(packet["summary"]["input_count"], 1)
        self.assertEqual(packet["summary"]["modules"], ["level1.security_headers_baseline"])
        self.assertEqual(packet["summary"]["candidate_count"], 1)
        self.assertEqual(packet["findings"][0]["id"], "security_headers_baseline.csp.unsafe_inline")

    def test_empty_inputs_zero_findings(self):
        rel = "tests/fixtures/candidate_review_packet/empty/expected_findings.json"
        packet = _build(rel)
        self.assertEqual(packet["status"], "ok")
        self.assertEqual(packet["errors"], [])
        self.assertEqual(packet["findings"], [])
        self.assertEqual(packet["summary"]["candidate_count"], 0)
        self.assertEqual(packet["summary"]["modules"], [])
        self.assertEqual(packet["summary"]["targets"], [])


class DeterminismTests(unittest.TestCase):
    INPUTS = (
        "tests/fixtures/security_headers_baseline/all_headers_absent/expected_findings.json",
        "tests/fixtures/security_headers_baseline/partial_set/expected_findings.json",
        "tests/fixtures/security_headers_baseline/weak_csp/expected_findings.json",
    )

    def test_byte_identical_on_repeat(self):
        first = json.dumps(_build(*self.INPUTS), sort_keys=True, separators=(",", ":"))
        second = json.dumps(_build(*self.INPUTS), sort_keys=True, separators=(",", ":"))
        self.assertEqual(first, second)

    def test_findings_sorted_by_id_then_target_value(self):
        packet = _build(*self.INPUTS)
        observed = [(f["id"], f["target"]["value"]) for f in packet["findings"]]
        self.assertEqual(observed, sorted(observed))

    def test_order_independent_multi_file_run(self):
        forward = _build(*self.INPUTS)
        reversed_inputs = list(reversed(self.INPUTS))
        backward = _build(*reversed_inputs)
        forward_no_input_count = dict(forward)
        backward_no_input_count = dict(backward)
        forward_no_input_count["summary"] = {
            k: v for k, v in forward["summary"].items() if k != "input_count"
        }
        backward_no_input_count["summary"] = {
            k: v for k, v in backward["summary"].items() if k != "input_count"
        }
        self.assertEqual(forward_no_input_count, backward_no_input_count)
        self.assertEqual(forward["summary"]["input_count"], backward["summary"]["input_count"])


class P31CuratedFixtureTests(unittest.TestCase):
    def test_curated_fixtures_exist_validate_and_have_synthetic_origin(self):
        missing = [rel for rel in P3_1_CURATED_INPUTS if not (ROOT / rel).exists()]
        self.assertEqual(missing, [], f"P3.1 curated fixture(s) missing: {missing}")
        for rel in P3_1_CURATED_INPUTS:
            with self.subTest(rel=rel):
                findings = json.loads((ROOT / rel).read_text(encoding="utf-8"))
                self.assertGreater(len(findings), 0)
                for finding in findings:
                    result = builder._validate_data(finding, "finding")
                    self.assertEqual(result.errors, [], f"{rel}: {result.errors}")
                    self.assertEqual(result.verdict, "allow")
                    self.assertEqual(finding["status"], "candidate")
                    self.assertTrue(
                        finding["target"]["value"].endswith((".example.test", ".invalid", ".test")),
                        finding["target"],
                    )
                    self.assertTrue(
                        finding["source"]["module_id"].startswith("p3_1_curated."),
                        finding["source"],
                    )

    def test_curated_fixtures_build_without_promoting_status(self):
        missing = [rel for rel in P3_1_CURATED_INPUTS if not (ROOT / rel).exists()]
        self.assertEqual(missing, [], f"P3.1 curated fixture(s) missing: {missing}")
        packet = _build(*P3_1_CURATED_INPUTS)
        self.assertEqual(packet["status"], "ok", packet)
        self.assertEqual(packet["summary"]["input_count"], len(P3_1_CURATED_INPUTS))
        self.assertGreaterEqual(packet["summary"]["candidate_count"], len(P3_1_CURATED_INPUTS))
        for finding in packet["findings"]:
            self.assertEqual(finding["status"], "candidate")
            self.assertNotIn(
                finding.get("report_readiness"),
                ("ready", "approved", "draft", "confirmed", "verified", "accepted"),
            )

    def test_duplicate_pair_uses_distinct_notional_sources_and_survives(self):
        rel = "tests/fixtures/candidate_review_packet/p3_1_curated_duplicate_pair/expected_findings.json"
        findings = json.loads((ROOT / rel).read_text(encoding="utf-8"))
        self.assertEqual(len(findings), 2)
        module_ids = [finding["source"]["module_id"] for finding in findings]
        self.assertEqual(len(set(module_ids)), 2)
        self.assertTrue(all(module_id.startswith("p3_1_curated.") for module_id in module_ids))

        packet = _build(rel)
        emitted = [
            finding for finding in packet["findings"] if finding["id"].startswith("p3_1_curated.duplicate_pair.")
        ]
        self.assertEqual(len(emitted), 2)
        self.assertEqual([finding["id"] for finding in emitted], sorted(finding["id"] for finding in emitted))


class ValidationReuseTests(unittest.TestCase):
    def test_invalid_finding_excluded_with_validation_failed_code(self):
        rel = "tests/fixtures/candidate_review_packet/invalid_finding/expected_findings.json"
        packet = _build(rel)
        self.assertEqual(packet["status"], "error")
        self.assertEqual(packet["findings"], [])
        codes = [e["code"] for e in packet["errors"]]
        self.assertIn("FINDING_VALIDATION_FAILED", codes)
        for finding in packet["findings"]:
            self.assertNotIn(
                "invalid_finding",
                json.dumps(finding),
            )

    def test_forbidden_status_excluded_with_dedicated_code(self):
        rel = "tests/fixtures/candidate_review_packet/forbidden_status/expected_findings.json"
        packet = _build(rel)
        self.assertEqual(packet["status"], "error")
        codes = [e["code"] for e in packet["errors"]]
        self.assertIn("FORBIDDEN_STATUS", codes)
        emitted_ids = [f["id"] for f in packet["findings"]]
        self.assertIn(
            "review_packet_self_test.forbidden_status.candidate_companion", emitted_ids
        )
        self.assertNotIn(
            "review_packet_self_test.forbidden_status.confirmed", emitted_ids
        )
        emitted_blob = json.dumps(packet["findings"])
        for forbidden in ("confirmed", "verified", "accepted"):
            for finding in packet["findings"]:
                self.assertNotEqual(finding.get("status"), forbidden)
            # report_readiness must never claim any promotion-like status
            for finding in packet["findings"]:
                self.assertNotIn(finding.get("report_readiness"), ("ready", "approved", "draft"))
        self.assertIn("candidate", emitted_blob)


class PathAllowlistTests(unittest.TestCase):
    def test_rejects_paths_outside_allowlist(self):
        for rel, expected in (
            ("runs/x/y.json", "INPUT_PATH_NOT_ALLOWED"),
            ("config/scope.txt", "INPUT_PATH_NOT_ALLOWED"),
            ("scans/output/expected_findings.json", "INPUT_PATH_NOT_ALLOWED"),
            ("loot/expected_findings.json", "INPUT_PATH_NOT_ALLOWED"),
            ("evidence/expected_findings.json", "INPUT_PATH_NOT_ALLOWED"),
            ("programs/example/expected_findings.json", "INPUT_PATH_NOT_ALLOWED"),
            (".env", "INPUT_PATH_NOT_ALLOWED"),
            ("setting/local/expected_findings.json", "INPUT_PATH_NOT_ALLOWED"),
            ("tests/fixtures/security_headers_baseline/expected_findings.json", "INPUT_PATH_NOT_ALLOWED"),
        ):
            with self.subTest(rel=rel):
                packet = _build(rel)
                self.assertEqual(packet["status"], "error")
                codes = [e["code"] for e in packet["errors"]]
                self.assertIn(expected, codes)

    def test_rejects_absolute_path(self):
        rel = (
            ROOT
            / "tests/fixtures/security_headers_baseline/all_headers_absent/expected_findings.json"
        )
        packet = _build(str(rel))
        self.assertEqual(packet["status"], "error")
        codes = [e["code"] for e in packet["errors"]]
        self.assertIn("INPUT_PATH_MUST_BE_RELATIVE", codes)

    def test_rejects_traversal(self):
        packet = _build("../etc/passwd")
        self.assertEqual(packet["status"], "error")
        codes = [e["code"] for e in packet["errors"]]
        self.assertIn("INPUT_PATH_TRAVERSAL", codes)

    def test_rejects_backslash_url_and_nul(self):
        for rel, expected in (
            (
                r"tests\fixtures\security_headers_baseline\all_headers_absent\expected_findings.json",
                "INPUT_PATH_UNSUPPORTED_CHARS",
            ),
            (
                "https://example.test/expected_findings.json",
                "INPUT_PATH_UNSUPPORTED_CHARS",
            ),
            ("tests/fixtures/security_headers_baseline/with\x00nul/expected_findings.json", "INPUT_PATH_UNSUPPORTED_CHARS"),
        ):
            with self.subTest(rel=repr(rel)):
                packet = _build(rel)
                self.assertEqual(packet["status"], "error")
                codes = [e["code"] for e in packet["errors"]]
                self.assertIn(expected, codes)

    def test_repo_root_not_containing_input(self):
        with tempfile.TemporaryDirectory() as td:
            packet = builder.build_packet(
                td,
                [
                    "tests/fixtures/security_headers_baseline/all_headers_absent/expected_findings.json"
                ],
            )
        self.assertEqual(packet["status"], "error")
        codes = [e["code"] for e in packet["errors"]]
        self.assertIn("INPUT_PATH_OUTSIDE_REPO", codes)

    def test_argparse_requires_repo_root(self):
        result = subprocess.run(
            [
                sys.executable,
                str(BUILDER_PATH),
                "--input",
                "tests/fixtures/security_headers_baseline/all_headers_absent/expected_findings.json",
            ],
            capture_output=True,
            text=True,
            check=False,
            cwd=str(ROOT),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--repo-root", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


class NoFilesystemWriteTests(unittest.TestCase):
    def test_no_writes_under_repo_root_on_happy_path(self):
        repo_snapshot = _snapshot_tree(ROOT / "tests" / "fixtures")
        with tempfile.TemporaryDirectory() as td:
            cwd_snapshot_before = _snapshot_tree(Path(td))
            old_cwd = os.getcwd()
            os.chdir(td)
            try:
                _build(
                    "tests/fixtures/security_headers_baseline/all_headers_absent/expected_findings.json",
                    "tests/fixtures/candidate_review_packet/with_evidence/expected_findings.json",
                )
            finally:
                os.chdir(old_cwd)
            cwd_snapshot_after = _snapshot_tree(Path(td))
        self.assertEqual(_snapshot_tree(ROOT / "tests" / "fixtures"), repo_snapshot)
        self.assertEqual(cwd_snapshot_before, cwd_snapshot_after)

    def test_no_writes_on_deny_path(self):
        repo_snapshot = _snapshot_tree(ROOT / "tests" / "fixtures")
        with tempfile.TemporaryDirectory() as td:
            old_cwd = os.getcwd()
            os.chdir(td)
            try:
                _build("../etc/passwd", "runs/x/expected_findings.json")
            finally:
                os.chdir(old_cwd)
            cwd_snapshot = _snapshot_tree(Path(td))
        self.assertEqual(_snapshot_tree(ROOT / "tests" / "fixtures"), repo_snapshot)
        self.assertEqual(cwd_snapshot, {})


class SchemaVersionPinTests(unittest.TestCase):
    def test_schema_version_string_appears_exactly_once_in_source(self):
        source = BUILDER_PATH.read_text(encoding="utf-8")
        occurrences = source.count(SCHEMA_VERSION_LITERAL)
        self.assertEqual(occurrences, 1, occurrences)

    def test_no_alternate_or_unsuffixed_schema_versions(self):
        source = BUILDER_PATH.read_text(encoding="utf-8")
        for bad in (
            "candidate_review_packet/0.1\"",
            "candidate_review_packet/1.0",
            "candidate_review_packet/0.2",
        ):
            with self.subTest(bad=bad):
                self.assertNotIn(bad, source)

    def test_emitted_packet_carries_pinned_version(self):
        packet = _build(
            "tests/fixtures/candidate_review_packet/empty/expected_findings.json"
        )
        self.assertEqual(packet["schema_version"], SCHEMA_VERSION_LITERAL)


class ManualVerificationFlagsTests(unittest.TestCase):
    def test_triage_flags_carry_through_unchanged(self):
        packet = _build(
            "tests/fixtures/security_headers_baseline/weak_csp/expected_findings.json"
        )
        self.assertEqual(packet["status"], "ok")
        self.assertTrue(packet["findings"])
        for finding in packet["findings"]:
            self.assertIs(finding["manual_verification_required"], True)
            self.assertIs(finding["scanner_output_only"], True)


class ReportReadinessRubricTests(unittest.TestCase):
    def test_no_evidence_is_not_ready(self):
        packet = _build(
            "tests/fixtures/security_headers_baseline/all_headers_absent/expected_findings.json"
        )
        for finding in packet["findings"]:
            self.assertEqual(finding["report_readiness"], "not_ready")

    def test_low_confidence_is_not_ready(self):
        packet = _build(
            "tests/fixtures/candidate_review_packet/low_confidence/expected_findings.json"
        )
        self.assertEqual(packet["findings"][0]["report_readiness"], "not_ready")

    def test_info_severity_is_not_ready(self):
        packet = _build(
            "tests/fixtures/candidate_review_packet/info_severity/expected_findings.json"
        )
        self.assertEqual(packet["findings"][0]["report_readiness"], "not_ready")

    def test_with_evidence_high_confidence_is_reviewer_decision_required(self):
        packet = _build(
            "tests/fixtures/candidate_review_packet/with_evidence/expected_findings.json"
        )
        self.assertEqual(
            packet["findings"][0]["report_readiness"], "reviewer_decision_required"
        )

    def test_no_promotion_like_values_anywhere(self):
        for rel in (
            "tests/fixtures/security_headers_baseline/all_headers_absent/expected_findings.json",
            "tests/fixtures/candidate_review_packet/with_evidence/expected_findings.json",
            "tests/fixtures/candidate_review_packet/low_confidence/expected_findings.json",
            "tests/fixtures/candidate_review_packet/info_severity/expected_findings.json",
        ):
            packet = _build(rel)
            blob = json.dumps(packet)
            for forbidden in ("\"ready\"", "\"approved\"", "\"draft\""):
                self.assertNotIn(forbidden, blob, rel)


class SummaryAggregationTests(unittest.TestCase):
    def test_summary_targets_and_modules_are_sorted_deduped_and_complete(self):
        inputs = [
            "tests/fixtures/security_headers_baseline/all_headers_absent/expected_findings.json",
            "tests/fixtures/security_headers_baseline/partial_set/expected_findings.json",
            "tests/fixtures/security_headers_baseline/non_200_status/expected_findings.json",
        ]
        packet = _build(*inputs)
        expected_targets = set()
        expected_modules = set()
        for rel in inputs:
            for entry in json.loads((ROOT / rel).read_text(encoding="utf-8")):
                expected_targets.add(entry["target"]["value"])
                expected_modules.add(entry["source"]["module_id"])
        self.assertEqual(packet["summary"]["targets"], sorted(expected_targets))
        self.assertEqual(packet["summary"]["modules"], sorted(expected_modules))


class ReviewQuestionsTests(unittest.TestCase):
    def test_review_questions_are_deterministic(self):
        rel = "tests/fixtures/candidate_review_packet/with_evidence/expected_findings.json"
        first = _build(rel)
        second = _build(rel)
        self.assertEqual(first["findings"][0]["review_questions"], second["findings"][0]["review_questions"])

    def test_keys_sorted_alphabetically_and_status_guardrail_last(self):
        rel = "tests/fixtures/candidate_review_packet/with_evidence/expected_findings.json"
        packet = _build(rel)
        keys = [q["key"] for q in packet["findings"][0]["review_questions"]]
        self.assertEqual(keys, sorted(keys))
        self.assertEqual(keys[-1], "status_guardrail")

    def test_no_evidence_branch_emits_no_evidence_text(self):
        rel = "tests/fixtures/security_headers_baseline/all_headers_absent/expected_findings.json"
        packet = _build(rel)
        for finding in packet["findings"]:
            evidence_q = next(q for q in finding["review_questions"] if q["key"] == "evidence_sufficiency")
            self.assertIn("No evidence refs are attached", evidence_q["text"])

    def test_with_evidence_branch_counts_refs(self):
        rel = "tests/fixtures/candidate_review_packet/with_evidence/expected_findings.json"
        packet = _build(rel)
        evidence_q = next(
            q for q in packet["findings"][0]["review_questions"] if q["key"] == "evidence_sufficiency"
        )
        self.assertIn("1 attached evidence refs", evidence_q["text"])

    def test_low_confidence_emits_confidence_floor(self):
        rel = "tests/fixtures/candidate_review_packet/low_confidence/expected_findings.json"
        packet = _build(rel)
        keys = [q["key"] for q in packet["findings"][0]["review_questions"]]
        self.assertIn("confidence_floor", keys)

    def test_non_low_confidence_omits_confidence_floor(self):
        rel = "tests/fixtures/candidate_review_packet/with_evidence/expected_findings.json"
        packet = _build(rel)
        keys = [q["key"] for q in packet["findings"][0]["review_questions"]]
        self.assertNotIn("confidence_floor", keys)

    def test_cwe_emitted_when_classifications_present(self):
        rel = "tests/fixtures/security_headers_baseline/weak_csp/expected_findings.json"
        packet = _build(rel)
        keys = [q["key"] for q in packet["findings"][0]["review_questions"]]
        self.assertIn("cwe_classification_check", keys)

    def test_review_question_templates_never_mention_platforms(self):
        rels = [
            "tests/fixtures/security_headers_baseline/weak_csp/expected_findings.json",
            "tests/fixtures/candidate_review_packet/with_evidence/expected_findings.json",
            "tests/fixtures/candidate_review_packet/low_confidence/expected_findings.json",
        ]
        for rel in rels:
            packet = _build(rel)
            blob = json.dumps(packet).lower()
            for name in PLATFORM_BLOCKLIST:
                self.assertNotIn(name, blob, rel)


class AstAndImportGuardTests(unittest.TestCase):
    FORBIDDEN_IMPORTS = frozenset(
        {
            "aiohttp",
            "asyncio",
            "asyncore",
            "ftplib",
            "http",
            "http.client",
            "httplib",
            "httpx",
            "multiprocessing",
            "requests",
            "selectors",
            "shutil",
            "smtplib",
            "socket",
            "ssl",
            "subprocess",
            "telnetlib",
            "threading",
            "urllib",
            "urllib.request",
            "urllib2",
            "urllib3",
            "xmlrpc",
        }
    )

    FORBIDDEN_RUNTIME_IMPORTS = frozenset(
        {
            "scripts.module_runner",
            "scripts.validate_module_io_bundle",
            "scripts.validate_module_io_contract",
            "scripts.program_policy_boundary",
            "scripts.module_input_contract",
            "scripts.module_result_contract",
            "module_runner",
            "validate_module_io_bundle",
            "validate_module_io_contract",
            "program_policy_boundary",
            "module_input_contract",
            "module_result_contract",
        }
    )

    def test_no_forbidden_network_or_subprocess_imports(self):
        source = BUILDER_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported.add(alias.name)
                    imported.add(alias.name.split(".", 1)[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
                imported.add(node.module.split(".", 1)[0])
        bad = imported & self.FORBIDDEN_IMPORTS
        self.assertFalse(bad, bad)

    def test_no_runtime_or_module_checks_imports(self):
        source = BUILDER_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported.add(alias.name)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
        bad = imported & self.FORBIDDEN_RUNTIME_IMPORTS
        self.assertFalse(bad, bad)
        self.assertNotIn("modules.checks", " ".join(imported))

    def test_no_forbidden_write_or_process_patterns(self):
        source = BUILDER_PATH.read_text(encoding="utf-8")
        forbidden_patterns = [
            r"\.write_text\s*\(",
            r"\.write_bytes\s*\(",
            r"\bopen\s*\([^)]*['\"][wax+]",
            r"\bos\.makedirs\s*\(",
            r"\bos\.mkdir\s*\(",
            r"\bos\.rename\s*\(",
            r"\bos\.unlink\s*\(",
            r"\bos\.remove\s*\(",
            r"\bos\.system\s*\(",
            r"\bos\.popen\s*\(",
            r"\bshutil\.",
            r"\bsubprocess\.",
            r"\basyncio\.",
            r"\bsocket\.",
        ]
        for pattern in forbidden_patterns:
            with self.subTest(pattern=pattern):
                self.assertIsNone(re.search(pattern, source))
        tree = ast.parse(source)
        calls: set[tuple[str, str]] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Name):
                    calls.add(("", func.id))
                elif isinstance(func, ast.Attribute):
                    owner = func.value.id if isinstance(func.value, ast.Name) else ""
                    calls.add((owner, func.attr))
        forbidden_attrs = {
            ("Path", "write_text"),
            ("Path", "write_bytes"),
            ("os", "system"),
            ("os", "popen"),
            ("os", "makedirs"),
            ("os", "mkdir"),
            ("os", "rename"),
            ("os", "unlink"),
            ("os", "remove"),
            ("shutil", "copy"),
            ("shutil", "move"),
            ("shutil", "rmtree"),
        }
        self.assertTrue(calls.isdisjoint(forbidden_attrs), calls & forbidden_attrs)

    def test_only_validate_data_is_consumed_from_validator(self):
        source = BUILDER_PATH.read_text(encoding="utf-8")
        for forbidden in ("validate_bundle", "_validate_finding", "_validate_evidence"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, source, forbidden)


class PlatformNameLeakTests(unittest.TestCase):
    def _scan(self, path: Path) -> None:
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for name in PLATFORM_BLOCKLIST:
            self.assertNotIn(name, text, f"{name} in {path}")

    def test_builder_source(self):
        self._scan(BUILDER_PATH)

    def test_test_source_only_blocklist_constant(self):
        text = TEST_PATH.read_text(encoding="utf-8").lower()
        # Strip our blocklist constant before scanning the rest.
        scrubbed = text.replace(
            ",".join(repr(name) for name in PLATFORM_BLOCKLIST), ""
        )
        for name in PLATFORM_BLOCKLIST:
            self.assertNotIn(name, scrubbed, name)

    def test_self_test_fixtures(self):
        for path in SELF_TEST_FIXTURE_ROOT.rglob("*.json"):
            self._scan(path)

    def test_emitted_packets_for_committed_fixtures(self):
        for fixture_dir in sorted(SECURITY_HEADERS_FIXTURE_ROOT.iterdir()):
            rel = (
                f"tests/fixtures/security_headers_baseline/{fixture_dir.name}/expected_findings.json"
            )
            packet = _build(rel)
            blob = json.dumps(packet).lower()
            for name in PLATFORM_BLOCKLIST:
                self.assertNotIn(name, blob, f"{name} in packet for {fixture_dir.name}")


class TrialHeaderTests(unittest.TestCase):
    def test_trial_only_comment_in_first_twenty_lines(self):
        source = BUILDER_PATH.read_text(encoding="utf-8").splitlines()[:20]
        joined = "\n".join(source)
        self.assertIn("# TRIAL ONLY", joined)
        self.assertIn("schema promotion deferred to P2.20+", joined)


class NoSchemaFileTests(unittest.TestCase):
    def test_no_new_schema_file_for_candidate_review_packet(self):
        schema_dir = ROOT / "modules" / "_schema"
        if not schema_dir.exists():
            return
        for path in schema_dir.iterdir():
            self.assertNotIn(
                "candidate_review_packet",
                path.name.lower(),
                path,
            )


class CliSmokeTests(unittest.TestCase):
    def test_cli_emits_single_line_json(self):
        result = subprocess.run(
            [
                sys.executable,
                str(BUILDER_PATH),
                "--repo-root",
                str(ROOT),
                "--input",
                "tests/fixtures/security_headers_baseline/weak_csp/expected_findings.json",
            ],
            capture_output=True,
            text=True,
            check=False,
            cwd=str(ROOT),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        body = result.stdout.strip()
        self.assertNotIn("\n", body)
        payload = json.loads(body)
        self.assertEqual(payload["schema_version"], SCHEMA_VERSION_LITERAL)

    def test_cli_returns_nonzero_for_disallowed_path(self):
        result = subprocess.run(
            [
                sys.executable,
                str(BUILDER_PATH),
                "--repo-root",
                str(ROOT),
                "--input",
                "runs/x/y.json",
            ],
            capture_output=True,
            text=True,
            check=False,
            cwd=str(ROOT),
        )
        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout.strip())
        self.assertEqual(payload["status"], "error")
        codes = [error["code"] for error in payload["errors"]]
        self.assertIn("INPUT_PATH_NOT_ALLOWED", codes)


if __name__ == "__main__":
    unittest.main()
