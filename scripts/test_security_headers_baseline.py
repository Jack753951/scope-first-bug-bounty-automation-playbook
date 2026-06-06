import ast
import copy
import importlib.util
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "modules" / "checks" / "level1" / "security_headers_baseline" / "check.py"
VALIDATOR_PATH = ROOT / "scripts" / "validate_finding_evidence.py"
FIXTURE_ROOT = ROOT / "tests" / "fixtures" / "security_headers_baseline"
TRIAGE_ROOT = ROOT / "handoff" / "p2_16_triage"
RUN_ID = "p2-16.fixture"
POLICY_DECISION_SHA256 = "0123456789abcdef" * 4

EXPECTED_SCENARIOS = {
    "all_headers_absent",
    "all_headers_present",
    "non_200_status",
    "partial_set",
    "weak_csp",
    "weak_hsts",
}


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


check = _load_module(MODULE_PATH, "security_headers_baseline_check")
finding_validator = _load_module(VALIDATOR_PATH, "validate_finding_evidence_for_headers")


def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _canonical(data) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _fixture_scenarios() -> list[Path]:
    scenarios = sorted(path for path in FIXTURE_ROOT.iterdir() if path.is_dir())
    assert {path.name for path in scenarios} == EXPECTED_SCENARIOS
    return scenarios


def _snapshot_tree(root: Path) -> dict[str, tuple[bytes, int, int]]:
    snapshot = {}
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        stat = path.stat()
        snapshot[str(path.relative_to(root))] = (path.read_bytes(), stat.st_mtime_ns, stat.st_size)
    return snapshot


class SecurityHeadersBaselineTests(unittest.TestCase):
    def test_fixture_golden_equality_and_finding_validation(self):
        for scenario in _fixture_scenarios():
            with self.subTest(scenario=scenario.name):
                fixture = _json(scenario / "input.json")
                expected = _json(scenario / "expected_findings.json")
                observed = check.evaluate(
                    fixture,
                    run_id=RUN_ID,
                    policy_decision_sha256=POLICY_DECISION_SHA256,
                )
                self.assertEqual(_canonical(observed), _canonical(expected))
                for finding in expected:
                    result = finding_validator.validate_data(finding, document_type="finding")
                    self.assertEqual(result.verdict, "allow", result.errors)

    def test_candidate_triage_source_and_redaction_fields(self):
        rendered_fields = ("title", "summary", "remediation", "verification_guidance")
        for scenario in _fixture_scenarios():
            fixture = _json(scenario / "input.json")
            expected = _json(scenario / "expected_findings.json")
            forbidden_literals = [fixture["target"]["value"]]
            forbidden_literals.extend(header["value"] for header in fixture["headers"] if header["value"])
            for finding in expected:
                with self.subTest(scenario=scenario.name, finding=finding["id"]):
                    self.assertEqual(finding["status"], "candidate")
                    self.assertTrue(finding["triage"]["scanner_output_only"])
                    self.assertTrue(finding["triage"]["manual_verification_required"])
                    self.assertEqual(finding["source"]["module_id"], "level1.security_headers_baseline")
                    self.assertEqual(finding["source"]["run_id"], RUN_ID)
                    self.assertEqual(finding["source"]["policy_decision_sha256"], POLICY_DECISION_SHA256)
                    self.assertEqual(finding["evidence"], [])
                    rendered = "\n".join(finding[field] for field in rendered_fields)
                    for literal in forbidden_literals:
                        self.assertNotIn(literal, rendered)

    def test_missing_required_fixture_keys_fail_closed_with_field_path(self):
        base = _json(FIXTURE_ROOT / "all_headers_present" / "input.json")
        for key in ("fixture_version", "target", "status_code", "headers"):
            with self.subTest(key=key):
                data = copy.deepcopy(base)
                del data[key]
                with self.assertRaisesRegex(check.FixtureShapeError, rf"fixture\.{key}"):
                    check.evaluate(data, run_id=RUN_ID, policy_decision_sha256=POLICY_DECISION_SHA256)

    def test_unknown_top_level_and_nested_fixture_keys_fail_closed(self):
        base = _json(FIXTURE_ROOT / "all_headers_present" / "input.json")

        data = copy.deepcopy(base)
        data["unexpected"] = True
        with self.assertRaisesRegex(check.FixtureShapeError, r"fixture\.unexpected"):
            check.evaluate(data, run_id=RUN_ID, policy_decision_sha256=POLICY_DECISION_SHA256)

        data = copy.deepcopy(base)
        data["target"]["unexpected"] = True
        with self.assertRaisesRegex(check.FixtureShapeError, r"fixture\.target\.unexpected"):
            check.evaluate(data, run_id=RUN_ID, policy_decision_sha256=POLICY_DECISION_SHA256)

        data = copy.deepcopy(base)
        data["headers"][0]["unexpected"] = True
        with self.assertRaisesRegex(check.FixtureShapeError, r"fixture\.headers\[0\]\.unexpected"):
            check.evaluate(data, run_id=RUN_ID, policy_decision_sha256=POLICY_DECISION_SHA256)

    def test_fixture_version_drift_fails_closed(self):
        base = _json(FIXTURE_ROOT / "all_headers_present" / "input.json")
        for version in ("security_headers_baseline_input/1.0", "security_headers_baseline_input/2", None):
            with self.subTest(version=version):
                data = copy.deepcopy(base)
                data["fixture_version"] = version
                with self.assertRaisesRegex(check.FixtureShapeError, r"fixture\.fixture_version"):
                    check.evaluate(data, run_id=RUN_ID, policy_decision_sha256=POLICY_DECISION_SHA256)

    def test_target_type_and_header_name_denials(self):
        base = _json(FIXTURE_ROOT / "all_headers_present" / "input.json")

        data = copy.deepcopy(base)
        data["target"]["type"] = "ip"
        with self.assertRaisesRegex(check.FixtureShapeError, r"fixture\.target\.type"):
            check.evaluate(data, run_id=RUN_ID, policy_decision_sha256=POLICY_DECISION_SHA256)

        data = copy.deepcopy(base)
        data["headers"][0]["name"] = "Bad Header"
        with self.assertRaisesRegex(check.FixtureShapeError, r"fixture\.headers\[0\]\.name"):
            check.evaluate(data, run_id=RUN_ID, policy_decision_sha256=POLICY_DECISION_SHA256)

    def test_determinism_and_no_fixture_mutation_or_writes(self):
        fixture = _json(FIXTURE_ROOT / "weak_hsts" / "input.json")
        original = copy.deepcopy(fixture)
        before = _snapshot_tree(FIXTURE_ROOT)
        first = check.evaluate(fixture, run_id=RUN_ID, policy_decision_sha256=POLICY_DECISION_SHA256)
        second = check.evaluate(fixture, run_id=RUN_ID, policy_decision_sha256=POLICY_DECISION_SHA256)
        after = _snapshot_tree(FIXTURE_ROOT)
        self.assertEqual(fixture, original)
        self.assertEqual(_canonical(first), _canonical(second))
        self.assertEqual(after, before)

    def test_check_module_has_no_forbidden_imports(self):
        source = MODULE_PATH.read_text(encoding="utf-8")
        forbidden = {
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
            "urllib2",
            "urllib3",
            "xmlrpc",
        }
        tree = ast.parse(source)
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported.add(alias.name)
                    imported.add(alias.name.split(".", 1)[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
                imported.add(node.module.split(".", 1)[0])
        self.assertTrue(imported.isdisjoint(forbidden), imported & forbidden)

    def test_check_module_has_no_forbidden_write_patterns(self):
        source = MODULE_PATH.read_text(encoding="utf-8")
        forbidden_patterns = [
            r"\.write_text\s*\(",
            r"\.write_bytes\s*\(",
            r"\bopen\s*\([^)]*['\"][wax+]",
            r"\bos\.makedirs\s*\(",
            r"\bos\.mkdir\s*\(",
            r"\bos\.rename\s*\(",
            r"\bos\.unlink\s*\(",
            r"\bos\.remove\s*\(",
            r"\bshutil\.",
        ]
        for pattern in forbidden_patterns:
            with self.subTest(pattern=pattern):
                self.assertIsNone(re.search(pattern, source))

        tree = ast.parse(source)
        forbidden_attrs = {
            ("Path", "write_text"),
            ("Path", "write_bytes"),
            ("os", "makedirs"),
            ("os", "mkdir"),
            ("os", "rename"),
            ("os", "unlink"),
            ("os", "remove"),
            ("shutil", "copy"),
            ("shutil", "move"),
            ("shutil", "rmtree"),
        }
        calls = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Name):
                    calls.add(("", func.id))
                elif isinstance(func, ast.Attribute):
                    owner = func.value.id if isinstance(func.value, ast.Name) else ""
                    calls.add((owner, func.attr))
        self.assertNotIn(("", "open"), calls)
        self.assertTrue(calls.isdisjoint(forbidden_attrs), calls & forbidden_attrs)

    def test_cli_smoke_success_and_failure(self):
        fixture_path = FIXTURE_ROOT / "weak_csp" / "input.json"
        expected = _json(FIXTURE_ROOT / "weak_csp" / "expected_findings.json")

        missing_run = subprocess.run(
            [sys.executable, str(MODULE_PATH), "--fixture", str(fixture_path), "--policy-decision-sha256", POLICY_DECISION_SHA256],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(missing_run.returncode, 0)
        self.assertIn("--run-id", missing_run.stderr)

        bad_hash = subprocess.run(
            [
                sys.executable,
                str(MODULE_PATH),
                "--fixture",
                str(fixture_path),
                "--run-id",
                RUN_ID,
                "--policy-decision-sha256",
                "not-a-sha",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(bad_hash.returncode, 0)
        self.assertIn("policy_decision_sha256", bad_hash.stderr)

        ok = subprocess.run(
            [
                sys.executable,
                str(MODULE_PATH),
                "--fixture",
                str(fixture_path),
                "--run-id",
                RUN_ID,
                "--policy-decision-sha256",
                POLICY_DECISION_SHA256,
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(ok.returncode, 0, ok.stderr)
        self.assertEqual(ok.stderr, "")
        self.assertNotIn("\n", ok.stdout.strip())
        self.assertEqual(_canonical(json.loads(ok.stdout)), _canonical(expected))

    def test_cli_rejects_live_target_flags(self):
        fixture_path = FIXTURE_ROOT / "weak_csp" / "input.json"
        for flag in ("--target", "--url", "--host", "--scope", "--live"):
            with self.subTest(flag=flag):
                result = subprocess.run(
                    [
                        sys.executable,
                        str(MODULE_PATH),
                        "--fixture",
                        str(fixture_path),
                        "--run-id",
                        RUN_ID,
                        "--policy-decision-sha256",
                        POLICY_DECISION_SHA256,
                        flag,
                        "https://example.test/",
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("unrecognized arguments", result.stderr)
                self.assertIn(flag, result.stderr)

    def test_header_name_case_insensitivity(self):
        fixture = {
            "fixture_version": "security_headers_baseline_input/1",
            "target": {"type": "domain", "value": "lab.local"},
            "status_code": 200,
            "headers": [
                {"name": "content-security-policy", "value": "default-src 'self'"},
                {"name": "x-frame-options", "value": "DENY"},
                {"name": "x-content-type-options", "value": "nosniff"},
                {"name": "strict-transport-security", "value": "max-age=15552000; includeSubDomains"},
                {"name": "referrer-policy", "value": "no-referrer"},
            ],
        }
        self.assertEqual(
            check.evaluate(fixture, run_id=RUN_ID, policy_decision_sha256=POLICY_DECISION_SHA256),
            [],
        )

    def test_value_comparison_behavior_is_verbatim_for_v1(self):
        fixture = {
            "fixture_version": "security_headers_baseline_input/1",
            "target": {"type": "domain", "value": "invalid."},
            "status_code": 200,
            "headers": [
                {"name": "Content-Security-Policy", "value": "DEFAULT-SRC 'SELF'; SCRIPT-SRC 'UNSAFE-INLINE'"},
                {"name": "X-Frame-Options", "value": "sameorigin"},
                {"name": "X-Content-Type-Options", "value": "NoSniff"},
                {"name": "Strict-Transport-Security", "value": "max-age=15552000; includesubdomains"},
                {"name": "Referrer-Policy", "value": "NO-REFERRER"},
            ],
        }
        observed_ids = [
            finding["id"]
            for finding in check.evaluate(
                fixture,
                run_id=RUN_ID,
                policy_decision_sha256=POLICY_DECISION_SHA256,
            )
        ]
        self.assertEqual(
            observed_ids,
            [
                "security_headers_baseline.x_frame_options.invalid_value",
                "security_headers_baseline.x_content_type_options.invalid_value",
                "security_headers_baseline.hsts.include_subdomains_missing",
                "security_headers_baseline.referrer_policy.invalid_value",
            ],
        )

    def test_committed_fixture_targets_are_reserved_names_only(self):
        allowed_domain = re.compile(r"^(?:lab\.local|invalid\.|\*\.example\.test|(?:[a-z0-9-]+\.)*example\.test)$")
        allowed_url = re.compile(r"^https://(?:lab\.local|(?:[a-z0-9-]+\.)*example\.test)(?:/[a-z0-9_./-]*)?$")
        for scenario in _fixture_scenarios():
            fixture = _json(scenario / "input.json")
            value = fixture["target"]["value"]
            with self.subTest(scenario=scenario.name, value=value):
                self.assertTrue(allowed_domain.fullmatch(value) or allowed_url.fullmatch(value))

    def test_triage_drafts_match_golden_rule_ids_and_redaction_boundary(self):
        self.assertTrue((TRIAGE_ROOT / "README.md").is_file())
        for scenario in _fixture_scenarios():
            fixture = _json(scenario / "input.json")
            expected = _json(scenario / "expected_findings.json")
            draft_path = TRIAGE_ROOT / f"{scenario.name}.md"
            self.assertTrue(draft_path.is_file(), draft_path)
            draft = draft_path.read_text(encoding="utf-8")
            expected_ids = {finding["id"] for finding in expected}
            observed_ids = set(re.findall(r"security_headers_baseline\.[a-z0-9_.]+", draft))
            with self.subTest(scenario=scenario.name):
                self.assertEqual(observed_ids, expected_ids)
                self.assertNotIn(fixture["target"]["value"], draft)
                for header in fixture["headers"]:
                    if header["value"]:
                        self.assertNotIn(header["value"], draft)


if __name__ == "__main__":
    unittest.main()
