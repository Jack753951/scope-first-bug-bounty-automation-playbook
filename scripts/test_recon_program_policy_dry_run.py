"""Offline regression for ``recon.sh --dry-run --program <slug> --policy-mode planned|live``.

This test was added by the P3.7 slice (see ``handoff/cowork_p3_7_direction_review.md``)
and hardened by P3.8 for malformed-scope exit-code semantics. It exercises the
program-policy gate end-to-end against a synthetic program scope shipped at
``programs/_examples/sample-lab/scope.json``. The intent is regression coverage
only; every invocation remains ``--dry-run`` and non-target-touching.

What this test does NOT cover (deliberately, to keep the slice T2 / tests-only):

* Live mode against a real target. ``--policy-mode live`` is exercised only as an
  offline regression path under ``--dry-run``; no scanner, exploit, fuzzer, callback,
  brute force, proxy/pivot/transport, OAST, or DNS resolution path is executed.
* Recon-to-runner artifact coupling (the deferred Option 4 from the P3.7 direction
  review). The test never invokes ``scripts/module_runner.py`` against artifacts
  produced by ``recon.sh``.
* Per-program ``scope.json`` schema validation (covered separately by
  ``scripts/test_validate_program_scope.py``).
* Scanner binary integration (subfinder, httpx, nuclei, nmap, naabu). The test asserts
  these are not invoked during dry-run.
* DNS resolution edge cases when ``getaddrinfo`` is hooked at the OS level. The test
  only inspects ``recon.sh`` stdout/audit-log markers, not low-level resolver state.
* Stale artifact / target-mode-technique-mismatch boundaries beyond what the test can
  observe through existing recon.sh behavior without runtime edits. Where an
  assertion would require runtime changes, it is recorded as a deferred assertion in
  ``handoff/claude_code_result_p3_7.md`` rather than smuggled into a runtime patch.

Boundary recap:

* P3.8 permits only a narrow ``recon.sh`` exit-code hardening for policy-boundary
  error outcomes. No edits are permitted to ``scripts/program_policy_check.py``,
  ``scripts/program_policy_boundary.py``, ``scripts/module_runner.py``,
  ``scripts/build_*``, ``scripts/review_*``, ``scripts/core/**``, ``modules/**``,
  ``modules/_schema/**``, ``config/scope.txt``, ``config/recon.conf``,
  ``bin/hermes``, or ``run_hermes_worker.ps1``.
* The boundary helper continues to run under Python isolated mode (``python -I``);
  this test does not exercise that path directly but expects it to remain in place.
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_LAB_SCOPE = REPO_ROOT / "programs" / "_examples" / "sample-lab" / "scope.json"
PROGRAM_SLUG = "sample-lab"
IN_SCOPE_TARGET = "authorized.test"
SECONDARY_IN_SCOPE_TARGET = "lab.local"

# Markers that recon.sh emits for the techniques NOT allowed by the synthetic
# sample-lab program (which only allows ``http_probe``). The dry-run flow must
# never even *plan* these scanner invocations, because the program-policy gate
# denies the corresponding stage first. ``DRY: httpx`` is intentionally NOT in
# this set: it is the expected dry-run marker for the allowed ``http_probe``
# stage and its presence is proof that ``--dry-run`` short-circuited real
# execution.
DENIED_TECHNIQUE_DRY_RUN_MARKERS = (
    "DRY: subfinder",
    "DRY: nuclei",
    "DRY: nmap",
    "DRY: naabu",
    "DRY: feroxbuster",
    "DRY: curl -s https://crt.sh",
)

# Output fragments that would suggest a scanner actually ran instead of being
# planned via ``DRY: ...``. None of these should appear under ``--dry-run`` on a
# host without the tools installed; the test asserts their absence regardless.
SCANNER_EXECUTION_LEAK_MARKERS = (
    "[critical]",
    "[high]",
    "[medium]",
    "[low]",
    "[info] http",
    "Found ",
    "Open: ",
    "Nmap scan report",
)


def find_usable_bash():
    candidates = []
    if shutil.which("bash"):
        candidates.append(shutil.which("bash"))
    try:
        where = subprocess.run(
            ["where.exe", "bash"],
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=5,
        )
        if where.returncode == 0:
            candidates.extend(line.strip() for line in where.stdout.splitlines() if line.strip())
    except (OSError, subprocess.SubprocessError):
        pass

    seen = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        try:
            version = subprocess.run(
                [candidate, "--version"],
                text=True,
                encoding="utf-8",
                errors="replace",
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=5,
            )
        except (OSError, subprocess.SubprocessError):
            continue
        if version.returncode == 0 and "GNU bash" in version.stdout:
            return candidate
    return None


BASH = find_usable_bash()


def _sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@unittest.skipIf(BASH is None, "GNU bash is required for recon.sh dry-run policy tests")
class ReconProgramPolicyDryRunTests(unittest.TestCase):
    """End-to-end offline regression for the program-policy dry-run gate."""

    @classmethod
    def setUpClass(cls):
        cls.real_scope_txt = REPO_ROOT / "config" / "scope.txt"
        cls.real_scope_txt_sha256 = (
            _sha256_of(cls.real_scope_txt) if cls.real_scope_txt.is_file() else None
        )
        cls.sample_lab_scope_sha256 = _sha256_of(SAMPLE_LAB_SCOPE)
        cls.sample_lab_scope_payload = json.loads(
            SAMPLE_LAB_SCOPE.read_text(encoding="utf-8")
        )

    @classmethod
    def tearDownClass(cls):
        if cls.real_scope_txt_sha256 is not None:
            current = _sha256_of(cls.real_scope_txt)
            assert current == cls.real_scope_txt_sha256, (
                "config/scope.txt sha256 changed during the test run; tests must not "
                "edit the real scope file."
            )
        current_sample_sha = _sha256_of(SAMPLE_LAB_SCOPE)
        assert current_sample_sha == cls.sample_lab_scope_sha256, (
            "programs/_examples/sample-lab/scope.json sha256 changed during the test "
            "run; the synthetic fixture must remain immutable inside the suite."
        )

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(
            prefix=".tmp_recon_policy_", dir=REPO_ROOT
        )
        self.tmp_path = Path(self.tmp.name)
        self.hacklab_path = self.tmp_path / "lab"
        self.hacklab_env = self.hacklab_path.relative_to(REPO_ROOT).as_posix()
        (self.hacklab_path / "config").mkdir(parents=True)
        (self.hacklab_path / "config" / "scope.txt").write_text(
            f"{IN_SCOPE_TARGET}\n{SECONDARY_IN_SCOPE_TARGET}\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.tmp.cleanup()

    def install_synthetic_program(self, *, slug=PROGRAM_SLUG, payload=None):
        """Copy the synthetic sample-lab scope into the temporary HACKLAB.

        ``recon.sh`` resolves ``--program <slug>`` to
        ``$HACKLAB/programs/<slug>/scope.json``, so the synthetic fixture must be
        installed into the temp HACKLAB. Using a temp copy keeps the committed
        fixture at ``programs/_examples/sample-lab/scope.json`` untouched.
        """
        program_dir = self.hacklab_path / "programs" / slug
        program_dir.mkdir(parents=True, exist_ok=True)
        content = payload if payload is not None else self.sample_lab_scope_payload
        if isinstance(content, dict):
            data = dict(content)
            data.setdefault("program", {})
            data["program"] = dict(data["program"])
            data["program"]["slug"] = slug
            text = json.dumps(data)
        else:
            text = str(content)
        (program_dir / "scope.json").write_text(text + "\n", encoding="utf-8")

    def run_recon(self, *args, env_overrides=None, timeout=30):
        env = os.environ.copy()
        env.update(
            {
                "HACKLAB": self.hacklab_env,
                "NO_COLOR": "1",
                "USER": env.get("USER") or env.get("USERNAME") or "Owner",
            }
        )
        if env_overrides:
            env.update(env_overrides)
        return subprocess.run(
            [BASH, "recon.sh", *args],
            cwd=REPO_ROOT,
            env=env,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
        )

    def latest_scan_root(self, target=IN_SCOPE_TARGET):
        roots = sorted(
            (self.hacklab_path / "scans").glob(f"{target}_*"),
            key=lambda p: p.name,
        )
        self.assertTrue(roots, "no scan root produced under temp HACKLAB")
        return roots[-1]

    def policy_artifacts_for(self, scan_root):
        policy_dir = scan_root / "evidence" / "policy"
        if not policy_dir.exists():
            return []
        return sorted(p for p in policy_dir.glob("*.json"))

    def load_policy_artifacts(self, scan_root):
        return [
            json.loads(p.read_text(encoding="utf-8"))
            for p in self.policy_artifacts_for(scan_root)
        ]

    def assert_no_denied_technique_dry_run_markers(self, stdout):
        for marker in DENIED_TECHNIQUE_DRY_RUN_MARKERS:
            self.assertNotIn(
                marker,
                stdout,
                msg=(
                    f"denied-technique dry-run marker {marker!r} surfaced; "
                    "program policy should have skipped this stage entirely"
                ),
            )

    def assert_no_scanner_execution_leakage(self, stdout):
        for marker in SCANNER_EXECUTION_LEAK_MARKERS:
            self.assertNotIn(
                marker,
                stdout,
                msg=f"scanner-execution marker {marker!r} surfaced in dry-run output",
            )

    # --- assertions ---------------------------------------------------------

    def _select_allow_artifact_for_mode(self, scan_root, mode):
        for artifact in self.load_policy_artifacts(scan_root):
            if (
                artifact.get("schema_version") == "policy_boundary/1.0"
                and artifact.get("boundary", {}).get("status") == "allow"
                and artifact.get("request", {}).get("mode") == mode
                and artifact.get("decision", {}).get("mode") == mode
            ):
                return artifact
        self.fail(
            f"no allow artifact for mode={mode} found under {scan_root}/evidence/policy"
        )

    def test_synthetic_program_dry_run_planned_mode_allows_and_emits_artifact(self):
        self.install_synthetic_program()
        result = self.run_recon(
            "--dry-run",
            "--program",
            PROGRAM_SLUG,
            "--policy-mode",
            "planned",
            IN_SCOPE_TARGET,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("DRY-RUN enabled", result.stdout)
        self.assertIn("policy PASS stage=find_live_hosts.input", result.stdout)
        scan_root = self.latest_scan_root()
        artifact = self._select_allow_artifact_for_mode(scan_root, "planned")
        self.assertEqual(
            artifact.get("boundary", {}).get("audit_event"), "PROGRAM_POLICY_ALLOW"
        )
        self.assertEqual(artifact.get("decision", {}).get("verdict"), "allow")
        self.assertEqual(
            artifact.get("decision", {}).get("audit_event"), "PROGRAM_POLICY_ALLOW"
        )
        self.assertEqual(artifact.get("decision", {}).get("technique"), "http_probe")
        self.assertEqual(artifact.get("request", {}).get("technique"), "http_probe")
        self.assertIn("find_live_hosts", artifact.get("request", {}).get("stage", ""))
        self.assert_no_denied_technique_dry_run_markers(result.stdout)
        self.assert_no_scanner_execution_leakage(result.stdout)

    def test_synthetic_program_dry_run_live_mode_remains_offline_regression_only(self):
        self.install_synthetic_program()
        result = self.run_recon(
            "--dry-run",
            "--program",
            PROGRAM_SLUG,
            "--policy-mode",
            "live",
            IN_SCOPE_TARGET,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("DRY-RUN enabled", result.stdout)
        self.assertIn("policy PASS stage=find_live_hosts.input", result.stdout)
        scan_root = self.latest_scan_root()
        artifact = self._select_allow_artifact_for_mode(scan_root, "live")
        self.assertEqual(
            artifact.get("boundary", {}).get("audit_event"), "PROGRAM_POLICY_ALLOW"
        )
        self.assertEqual(artifact.get("decision", {}).get("verdict"), "allow")
        self.assert_no_denied_technique_dry_run_markers(result.stdout)
        self.assert_no_scanner_execution_leakage(result.stdout)

    def test_secondary_in_scope_target_is_also_allowed_under_planned_mode(self):
        self.install_synthetic_program()
        result = self.run_recon(
            "--dry-run",
            "--program",
            PROGRAM_SLUG,
            "--policy-mode",
            "planned",
            SECONDARY_IN_SCOPE_TARGET,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("policy PASS stage=find_live_hosts.input", result.stdout)
        scan_root = self.latest_scan_root(target=SECONDARY_IN_SCOPE_TARGET)
        artifact = self._select_allow_artifact_for_mode(scan_root, "planned")
        self.assertEqual(artifact.get("decision", {}).get("normalized_target"), SECONDARY_IN_SCOPE_TARGET)
        self.assert_no_denied_technique_dry_run_markers(result.stdout)
        self.assert_no_scanner_execution_leakage(result.stdout)

    def test_audit_log_records_program_policy_allow_event(self):
        self.install_synthetic_program()
        result = self.run_recon(
            "--dry-run",
            "--program",
            PROGRAM_SLUG,
            "--policy-mode",
            "planned",
            IN_SCOPE_TARGET,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        audit_log = self.hacklab_path / "logs" / "audit.log"
        self.assertTrue(audit_log.exists(), "audit log not produced")
        audit_text = audit_log.read_text(encoding="utf-8")
        self.assertIn("PROGRAM_POLICY_ALLOW", audit_text)
        self.assertIn(f"target={IN_SCOPE_TARGET}", audit_text)
        self.assertIn("mode=planned", audit_text)

    def test_missing_program_scope_file_fails_closed(self):
        (self.hacklab_path / "programs").mkdir(parents=True, exist_ok=True)
        result = self.run_recon(
            "--dry-run",
            "--program",
            "does-not-exist",
            "--policy-mode",
            "planned",
            IN_SCOPE_TARGET,
        )
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("--program scope file missing", result.stdout)

    def test_malformed_program_scope_fails_closed_at_policy_gate(self):
        program_dir = self.hacklab_path / "programs" / PROGRAM_SLUG
        program_dir.mkdir(parents=True, exist_ok=True)
        (program_dir / "scope.json").write_text("{ not valid json", encoding="utf-8")
        result = self.run_recon(
            "--dry-run",
            "--program",
            PROGRAM_SLUG,
            "--policy-mode",
            "planned",
            IN_SCOPE_TARGET,
        )
        self.assertEqual(
            result.returncode,
            3,
            "malformed program scope is a policy-boundary error and must fail CI/preflight",
        )
        self.assertIn("policy DENY stage=find_live_hosts.input", result.stdout)
        self.assertIn("VALIDATOR_DENY", result.stdout)
        self.assertNotIn(
            "policy PASS stage=find_live_hosts.input",
            result.stdout,
            "malformed scope must not yield a PASS",
        )
        self.assert_no_denied_technique_dry_run_markers(result.stdout)
        self.assert_no_scanner_execution_leakage(result.stdout)

    def test_valid_policy_deny_for_out_of_scope_target_exits_zero(self):
        outside_target = "outside.test"
        (self.hacklab_path / "config" / "scope.txt").write_text(
            f"{IN_SCOPE_TARGET}\n{SECONDARY_IN_SCOPE_TARGET}\n{outside_target}\n",
            encoding="utf-8",
        )
        self.install_synthetic_program()
        result = self.run_recon(
            "--dry-run",
            "--program",
            PROGRAM_SLUG,
            "--policy-mode",
            "planned",
            outside_target,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("policy DENY stage=find_live_hosts.input", result.stdout)
        self.assertIn("NOT_IN_PROGRAM_SCOPE", result.stdout)
        self.assertNotIn("status=error", result.stdout)
        self.assertNotIn("VALIDATOR_DENY", result.stdout)
        self.assertNotIn("policy PASS stage=find_live_hosts.input", result.stdout)
        self.assert_no_denied_technique_dry_run_markers(result.stdout)
        self.assert_no_scanner_execution_leakage(result.stdout)

    def install_cidr_program(self):
        (self.hacklab_path / "config" / "scope.txt").write_text(
            "192.0.2.0/24\n", encoding="utf-8"
        )
        cidr_payload = json.loads(SAMPLE_LAB_SCOPE.read_text(encoding="utf-8"))
        cidr_payload["program"]["slug"] = "sample-lab-cidr"
        cidr_payload["scope"]["in_scope"] = [
            {
                "type": "cidr",
                "value": "192.0.2.0/24",
                "notes": "RFC 5737 documentation range; synthetic CIDR dry-run test.",
            }
        ]
        self.install_synthetic_program(slug="sample-lab-cidr", payload=cidr_payload)

    def test_cidr_target_without_allow_cidr_is_forced_deny_end_to_end(self):
        self.install_cidr_program()
        result = self.run_recon(
            "--dry-run",
            "--program",
            "sample-lab-cidr",
            "--policy-mode",
            "planned",
            "192.0.2.0/24",
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("safe_target PASS context=initial_target target=192.0.2.0/24", result.stdout)
        self.assertIn("safe_target PASS context=find_live_hosts.input target=192.0.2.0/24", result.stdout)
        self.assertIn("policy DENY stage=find_live_hosts.input", result.stdout)
        self.assertIn("CIDR_REQUIRES_ALLOW_CIDR", result.stdout)
        self.assertNotIn("policy PASS stage=find_live_hosts.input", result.stdout)
        self.assertNotIn("DRY: httpx", result.stdout)
        scan_root = self.latest_scan_root(target="192.0.2.0_24")
        artifacts = self.load_policy_artifacts(scan_root)
        self.assertTrue(artifacts, "CIDR forced-deny should emit a policy artifact")
        self.assertTrue(
            any(
                artifact.get("boundary", {}).get("status") == "deny"
                and artifact.get("decision", {}).get("verdict") == "deny"
                and artifact.get("request", {}).get("target") == "192.0.2.0/24"
                and "CIDR_REQUIRES_ALLOW_CIDR"
                in artifact.get("decision", {}).get("deny_reason_codes", [])
                for artifact in artifacts
            ),
            "no policy artifact recorded the literal CIDR forced-deny decision",
        )
        self.assert_no_denied_technique_dry_run_markers(result.stdout)
        self.assert_no_scanner_execution_leakage(result.stdout)

    def test_cidr_target_with_allow_cidr_stays_dry_run_and_policy_limited(self):
        self.install_cidr_program()
        result = self.run_recon(
            "--dry-run",
            "--program",
            "sample-lab-cidr",
            "--policy-mode",
            "planned",
            "--allow-cidr",
            "192.0.2.0/24",
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("policy PASS stage=find_live_hosts.input", result.stdout)
        self.assertIn("policy DENY stage=port_scan.input", result.stdout)
        self.assertIn("TECHNIQUE_NOT_ALLOWED", result.stdout)
        self.assert_no_denied_technique_dry_run_markers(result.stdout)
        self.assert_no_scanner_execution_leakage(result.stdout)

    def test_reserved_examples_slug_is_rejected_by_recon(self):
        result = self.run_recon(
            "--dry-run",
            "--program",
            "_examples",
            "--policy-mode",
            "planned",
            IN_SCOPE_TARGET,
        )
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("--program", result.stdout)

    def test_program_requires_policy_mode_for_synthetic_slug(self):
        self.install_synthetic_program()
        result = self.run_recon(
            "--dry-run", "--program", PROGRAM_SLUG, IN_SCOPE_TARGET
        )
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("--program requires --policy-mode", result.stdout)

    def test_dry_run_output_does_not_indicate_scanner_execution(self):
        self.install_synthetic_program()
        result = self.run_recon(
            "--dry-run",
            "--program",
            PROGRAM_SLUG,
            "--policy-mode",
            "planned",
            IN_SCOPE_TARGET,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assert_no_denied_technique_dry_run_markers(result.stdout)
        self.assert_no_scanner_execution_leakage(result.stdout)

    def test_global_scope_file_in_real_repo_is_unchanged_by_dry_run(self):
        """recon.sh must never touch the real config/scope.txt during a test."""

        if self.real_scope_txt_sha256 is None:
            self.skipTest("real config/scope.txt does not exist; nothing to compare")
        self.install_synthetic_program()
        self.run_recon(
            "--dry-run",
            "--program",
            PROGRAM_SLUG,
            "--policy-mode",
            "planned",
            IN_SCOPE_TARGET,
        )
        self.assertEqual(_sha256_of(self.real_scope_txt), self.real_scope_txt_sha256)

    def test_synthetic_fixture_file_is_unchanged_by_dry_run(self):
        self.install_synthetic_program()
        self.run_recon(
            "--dry-run",
            "--program",
            PROGRAM_SLUG,
            "--policy-mode",
            "planned",
            IN_SCOPE_TARGET,
        )
        self.assertEqual(_sha256_of(SAMPLE_LAB_SCOPE), self.sample_lab_scope_sha256)


if __name__ == "__main__":
    unittest.main()
