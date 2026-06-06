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
AUDIT_BASELINE_PROFILE = REPO_ROOT / "modules" / "profiles" / "audit-baseline.json"
LEVEL1_MODULE_DIRS = (
    REPO_ROOT / "modules" / "checks" / "level1" / "security_headers_baseline",
    REPO_ROOT / "modules" / "checks" / "level1" / "policy_decision_metadata_audit",
)
MODULE_RUNNER = REPO_ROOT / "scripts" / "module_runner.py"
RECON_SH = REPO_ROOT / "recon.sh"
PROGRAM_SLUG = "sample-lab"
IN_SCOPE_TARGET = "authorized.test"
SECONDARY_IN_SCOPE_TARGET = "lab.local"
TARGET_TYPE = "domain"
PROTECTED_REPO_DIRS = ("runs", "loot", "scans", "evidence", "reports")
SCANNER_EXECUTION_LEAK_MARKERS = (
    "DRY: nuclei",
    "DRY: nmap",
    "DRY: subfinder",
    "DRY: naabu",
    "DRY: feroxbuster",
    "DRY: curl -s https://crt.sh",
    "Nmap scan report",
    "[critical]",
    "[high]",
    "[medium]",
    "[low]",
    "[info] http",
    "Open: ",
    "Found ",
)
MODULE_EXECUTION_LEAK_MARKERS = (
    "\"status\": \"executed\"",
    "\"status\": \"running\"",
    "\"status\": \"completed\"",
    "\"status\": \"failed\"",
    "\"status\": \"errored\"",
    "import check",
    "check.run",
    "subprocess.Popen(",
    "socket.create_connection",
    "urllib.request",
    "urllib3.connection",
    "http.client",
)
BRIDGE_FLAG_REGRESSION_NEEDLES = (
    "--auto-bridge",
    "--from-recon",
    "--to-runner",
    "--bridge",
    "--recon-artifact",
    "--auto-locate-policy",
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
def _snapshot_repo_dir(path: Path) -> dict[str, str] | None:
    if not path.exists():
        return None
    if not path.is_dir():
        return {"": _sha256_of(path)}
    snapshot: dict[str, str] = {}
    for entry in sorted(path.rglob("*")):
        if entry.is_file():
            try:
                rel = entry.relative_to(path).as_posix()
            except ValueError:
                rel = entry.as_posix()
            snapshot[rel] = _sha256_of(entry)
    return snapshot
@unittest.skipIf(BASH is None, "GNU bash is required for recon.sh dry-run bridge tests")
class ReconRunnerBridgeDryRunTests(unittest.TestCase):
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
        cls.audit_baseline_sha256 = _sha256_of(AUDIT_BASELINE_PROFILE)
        cls.level1_manifest_sha256 = {
            module_dir.name: _sha256_of(module_dir / "module.json")
            for module_dir in LEVEL1_MODULE_DIRS
        }
        cls.protected_snapshots = {
            name: _snapshot_repo_dir(REPO_ROOT / name) for name in PROTECTED_REPO_DIRS
        }
    @classmethod
    def tearDownClass(cls):
        if cls.real_scope_txt_sha256 is not None:
            current = _sha256_of(cls.real_scope_txt)
            assert current == cls.real_scope_txt_sha256, (
                "config/scope.txt sha256 changed during the bridge test run"
            )
        assert _sha256_of(SAMPLE_LAB_SCOPE) == cls.sample_lab_scope_sha256, (
            "programs/_examples/sample-lab/scope.json must remain immutable"
        )
        assert _sha256_of(AUDIT_BASELINE_PROFILE) == cls.audit_baseline_sha256, (
            "modules/profiles/audit-baseline.json must remain immutable"
        )
        for module_dir in LEVEL1_MODULE_DIRS:
            assert (
                _sha256_of(module_dir / "module.json")
                == cls.level1_manifest_sha256[module_dir.name]
            ), f"{module_dir.name}/module.json must remain immutable"
        for name, snapshot in cls.protected_snapshots.items():
            current = _snapshot_repo_dir(REPO_ROOT / name)
            assert current == snapshot, (
                f"real-repo {name}/ tree changed during the bridge test run"
            )
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(
            prefix=".tmp_recon_runner_bridge_", dir=REPO_ROOT
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
    def install_synthetic_program(self, slug: str = PROGRAM_SLUG) -> Path:
        program_dir = self.hacklab_path / "programs" / slug
        program_dir.mkdir(parents=True, exist_ok=True)
        payload = dict(self.sample_lab_scope_payload)
        payload["program"] = dict(payload["program"])
        payload["program"]["slug"] = slug
        (program_dir / "scope.json").write_text(
            json.dumps(payload) + "\n", encoding="utf-8"
        )
        return program_dir / "scope.json"
    def install_audit_baseline_profile(self) -> Path:
        profile_path = self.hacklab_path / "modules" / "profiles" / "audit-baseline.json"
        profile_path.parent.mkdir(parents=True, exist_ok=True)
        profile_path.write_text(
            AUDIT_BASELINE_PROFILE.read_text(encoding="utf-8"), encoding="utf-8"
        )
        return profile_path
    def install_level1_module_manifests(self) -> list[Path]:
        installed: list[Path] = []
        for module_dir in LEVEL1_MODULE_DIRS:
            dest = self.hacklab_path / "modules" / "checks" / "level1" / module_dir.name
            dest.mkdir(parents=True, exist_ok=True)
            (dest / "module.json").write_text(
                (module_dir / "module.json").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            installed.append(dest / "module.json")
        return installed
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
    def latest_scan_root(self, target: str = IN_SCOPE_TARGET) -> Path:
        roots = sorted(
            (self.hacklab_path / "scans").glob(f"{target}_*"),
            key=lambda p: p.name,
        )
        self.assertTrue(roots, "no scan root produced under temp HACKLAB")
        return roots[-1]
    def select_emitted_allow_artifact(
        self, scan_root: Path, *, mode: str = "dry-run"
    ) -> tuple[Path, dict]:
        policy_dir = scan_root / "evidence" / "policy"
        self.assertTrue(policy_dir.exists(), f"missing policy artifact dir: {policy_dir}")
        artifacts = sorted(policy_dir.glob("policy_boundary_*.json"))
        self.assertTrue(artifacts, "no policy_boundary_*.json emitted by recon.sh")
        for artifact_path in artifacts:
            payload = json.loads(artifact_path.read_text(encoding="utf-8"))
            if (
                payload.get("schema_version") == "policy_boundary/1.0"
                and payload.get("boundary", {}).get("status") == "allow"
                and payload.get("request", {}).get("mode") == mode
                and payload.get("decision", {}).get("mode") == mode
            ):
                return artifact_path, payload
        self.fail(
            f"no allow artifact with mode={mode!r} found under {policy_dir}; "
            f"available: {[p.name for p in artifacts]}"
        )
    def copy_artifact_into_run_policy_dir(
        self,
        artifact_payload: dict,
        *,
        run_id: str,
        directory: str = "policy",
        filename: str = "decision.json",
    ) -> Path:
        # This is test-harness-only path translation for P3.9 dry-run coverage;
        # it must not be mirrored into runtime code or become an auto-bridge.
        run_dir = self.hacklab_path / "runs" / run_id / directory
        run_dir.mkdir(parents=True, exist_ok=True)
        target_path = run_dir / filename
        target_path.write_text(
            json.dumps(artifact_payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return target_path

    def invoke_runner(
        self,
        *,
        policy_artifact_path: Path | str,
        run_id: str,
        target: str,
        target_type: str = TARGET_TYPE,
        mode: str = "dry-run",
        include_module_io_preview: bool = False,
        extra_args: list[str] | None = None,
        cwd: Path | None = None,
        timeout: int = 30,
    ) -> tuple[subprocess.CompletedProcess, dict]:
        args = [
            sys.executable,
            str(MODULE_RUNNER),
            "--policy-artifact",
            str(policy_artifact_path),
            "--run-id",
            run_id,
            "--target",
            target,
            "--target-type",
            target_type,
            "--mode",
            mode,
            "--discover-root",
            str(self.hacklab_path),
            "--json",
        ]
        if include_module_io_preview:
            args.append("--include-module-io-preview")
        if extra_args:
            args.extend(extra_args)
        completed = subprocess.run(
            args,
            cwd=cwd or REPO_ROOT,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
        try:
            payload = json.loads(completed.stdout) if completed.stdout.strip() else {}
        except json.JSONDecodeError as exc:
            self.fail(
                f"runner JSON parse failed: {exc}\nstdout=\n{completed.stdout}\nstderr=\n{completed.stderr}"
            )
        return completed, payload
    def emit_recon_allow_artifact(
        self,
        *,
        target: str = IN_SCOPE_TARGET,
        policy_mode: str = "dry-run",
    ) -> tuple[Path, dict, subprocess.CompletedProcess]:
        self.install_synthetic_program()
        self.install_audit_baseline_profile()
        self.install_level1_module_manifests()
        result = self.run_recon(
            "--dry-run",
            "--program",
            PROGRAM_SLUG,
            "--policy-mode",
            policy_mode,
            target,
        )
        self.assertEqual(
            result.returncode,
            0,
            f"recon.sh --dry-run --policy-mode {policy_mode} did not exit 0\n{result.stdout}",
        )
        self.assertIn("DRY-RUN enabled", result.stdout)
        scan_root = self.latest_scan_root(target=target)
        artifact_path, artifact_payload = self.select_emitted_allow_artifact(
            scan_root, mode=policy_mode
        )
        return artifact_path, artifact_payload, result
    def assert_no_scanner_execution_leakage(self, *outputs: str):
        for blob in outputs:
            for marker in SCANNER_EXECUTION_LEAK_MARKERS:
                self.assertNotIn(
                    marker,
                    blob,
                    msg=f"scanner-execution marker {marker!r} surfaced in bridge output",
                )
    def assert_no_module_execution_leakage(self, *outputs: str):
        for blob in outputs:
            for marker in MODULE_EXECUTION_LEAK_MARKERS:
                self.assertNotIn(
                    marker,
                    blob,
                    msg=f"module-execution marker {marker!r} surfaced in bridge output",
                )
    def test_recon_emission_bridges_to_runner_allow_verdict(self):
        run_id = "20260519T120000Z_p3_9_bridge_positive"
        artifact_path, artifact_payload, recon_result = self.emit_recon_allow_artifact()
        copied = self.copy_artifact_into_run_policy_dir(
            artifact_payload, run_id=run_id
        )
        completed, payload = self.invoke_runner(
            policy_artifact_path=copied,
            run_id=run_id,
            target=artifact_payload["request"]["target"],
        )
        self.assertEqual(
            completed.returncode,
            0,
            f"runner exited non-zero\nstdout=\n{completed.stdout}\nstderr=\n{completed.stderr}",
        )
        self.assertEqual(payload.get("verdict"), "allow", payload)
        plan = payload.get("plan") or {}
        self.assertEqual(plan.get("schema_version"), "run/1.0")
        self.assertEqual(plan.get("run_id"), run_id)
        self.assertEqual(plan.get("status"), "planned")
        policy = plan.get("policy") or {}
        self.assertEqual(policy.get("decision"), "allow")
        self.assertEqual(policy.get("mode"), "dry-run")
        execution = plan.get("execution") or {}
        self.assertIs(execution.get("dry_run"), True)
        self.assertIs(execution.get("target_touching"), False)
        modules = plan.get("modules") or []
        self.assertTrue(modules, "runner plan must contain at least one module")
        for module in modules:
            self.assertEqual(
                module.get("status"),
                "planned",
                f"runner promoted module {module.get('module_id')!r} past planned",
            )
        self.assert_no_scanner_execution_leakage(recon_result.stdout, completed.stdout)
        self.assert_no_module_execution_leakage(completed.stdout)
    def test_runner_plan_policy_decision_sha256_matches_copied_artifact(self):
        run_id = "20260519T120001Z_p3_9_bridge_hash"
        _, artifact_payload, _ = self.emit_recon_allow_artifact()
        copied = self.copy_artifact_into_run_policy_dir(
            artifact_payload, run_id=run_id
        )
        expected_sha256 = _sha256_of(copied)
        _, payload = self.invoke_runner(
            policy_artifact_path=copied,
            run_id=run_id,
            target=artifact_payload["request"]["target"],
        )
        self.assertEqual(payload.get("verdict"), "allow", payload)
        policy = payload["plan"]["policy"]
        self.assertEqual(policy.get("decision_sha256"), expected_sha256)
        self.assertEqual(
            policy.get("decision_artifact_path"),
            f"runs/{run_id}/policy/decision.json",
        )
    def test_runner_directly_reads_explicit_recon_policy_evidence_without_copy(self):
        run_id = "20260520T091000Z_p3_10_direct_evidence"
        artifact_path, artifact_payload, recon_result = self.emit_recon_allow_artifact()
        copied_path = self.hacklab_path / "runs" / run_id / "policy" / "decision.json"
        self.assertFalse(copied_path.exists(), "precondition: no runtime bridge copy should exist")
        completed, payload = self.invoke_runner(
            policy_artifact_path=artifact_path,
            run_id=run_id,
            target=artifact_payload["request"]["target"],
        )
        self.assertEqual(
            completed.returncode,
            0,
            f"runner exited non-zero\nstdout=\n{completed.stdout}\nstderr=\n{completed.stderr}",
        )
        self.assertEqual(payload.get("verdict"), "allow", payload)
        self.assertFalse(copied_path.exists(), "direct-read bridge must not copy into runs/<run_id>/policy")
        expected_relative = artifact_path.relative_to(self.hacklab_path).as_posix()
        policy = payload["plan"]["policy"]
        self.assertEqual(policy.get("decision_artifact_path"), expected_relative)
        self.assertEqual(policy.get("decision_sha256"), _sha256_of(artifact_path))
        self.assertTrue(expected_relative.startswith("scans/"), expected_relative)
        self.assertIn("/evidence/policy/policy_boundary_", expected_relative)
        self.assert_no_scanner_execution_leakage(recon_result.stdout, completed.stdout)
        self.assert_no_module_execution_leakage(completed.stdout, completed.stderr)
    def test_runner_reads_repo_relative_recon_policy_evidence_from_non_repo_cwd(self):
        run_id = "20260520T091003Z_p3_10_relative_cwd"
        artifact_path, artifact_payload, _ = self.emit_recon_allow_artifact()
        relative_artifact = artifact_path.relative_to(self.hacklab_path).as_posix()
        completed, payload = self.invoke_runner(
            policy_artifact_path=relative_artifact,
            run_id=run_id,
            target=artifact_payload["request"]["target"],
            cwd=self.tmp_path,
        )
        self.assertEqual(
            completed.returncode,
            0,
            f"runner exited non-zero\nstdout=\n{completed.stdout}\nstderr=\n{completed.stderr}",
        )
        policy = payload["plan"]["policy"]
        self.assertEqual(policy.get("decision_artifact_path"), relative_artifact)
        self.assertEqual(policy.get("decision_sha256"), _sha256_of(artifact_path))
    def test_runner_denies_direct_recon_evidence_with_traversal_segments(self):
        run_id = "20260520T091004Z_p3_10_direct_traversal"
        artifact_path, artifact_payload, _ = self.emit_recon_allow_artifact()
        rel_parts = artifact_path.relative_to(self.hacklab_path).parts
        traversal_path = f"scans/{rel_parts[1]}/evidence/../evidence/policy/{rel_parts[4]}"
        completed, payload = self.invoke_runner(
            policy_artifact_path=traversal_path,
            run_id=run_id,
            target=artifact_payload["request"]["target"],
        )
        self.assertNotEqual(completed.returncode, 0, payload)
        self.assertEqual(payload.get("verdict"), "deny", payload)
        self.assertNotIn("plan", payload)
        self.assertTrue(
            any("traversal" in err for err in payload.get("errors", [])),
            payload.get("errors"),
        )
    def test_runner_denies_direct_recon_evidence_with_malformed_scan_dir(self):
        run_id = "20260520T091005Z_p3_10_bad_scan_dir"
        artifact_path, artifact_payload, _ = self.emit_recon_allow_artifact()
        malformed_path = self.hacklab_path / "scans" / "ab" / "evidence" / "policy" / artifact_path.name
        malformed_path.parent.mkdir(parents=True, exist_ok=True)
        malformed_path.write_text(artifact_path.read_text(encoding="utf-8"), encoding="utf-8")
        completed, payload = self.invoke_runner(
            policy_artifact_path=malformed_path,
            run_id=run_id,
            target=artifact_payload["request"]["target"],
        )
        self.assertNotEqual(completed.returncode, 0, payload)
        self.assertEqual(payload.get("verdict"), "deny", payload)
        self.assertNotIn("plan", payload)
        self.assertTrue(
            any("policy.decision_artifact_path" in err for err in payload.get("errors", [])),
            payload.get("errors"),
        )
    def test_runner_denies_direct_recon_evidence_from_wrong_filename_or_directory(self):
        run_id = "20260520T091001Z_p3_10_direct_path_shape"
        artifact_path, artifact_payload, _ = self.emit_recon_allow_artifact()

        wrong_name = artifact_path.with_name("decision.json")
        wrong_name.write_text(artifact_path.read_text(encoding="utf-8"), encoding="utf-8")
        completed, payload = self.invoke_runner(
            policy_artifact_path=wrong_name,
            run_id=run_id,
            target=artifact_payload["request"]["target"],
        )
        self.assertNotEqual(completed.returncode, 0, payload)
        self.assertEqual(payload.get("verdict"), "deny", payload)
        self.assertNotIn("plan", payload)
        self.assertTrue(
            any("policy_boundary_*.json" in err for err in payload.get("errors", [])),
            payload.get("errors"),
        )

        wrong_dir = artifact_path.parents[1] / "other" / artifact_path.name
        wrong_dir.parent.mkdir(parents=True, exist_ok=True)
        wrong_dir.write_text(artifact_path.read_text(encoding="utf-8"), encoding="utf-8")
        completed, payload = self.invoke_runner(
            policy_artifact_path=wrong_dir,
            run_id=run_id,
            target=artifact_payload["request"]["target"],
        )
        self.assertNotEqual(completed.returncode, 0, payload)
        self.assertEqual(payload.get("verdict"), "deny", payload)
        self.assertNotIn("plan", payload)
        self.assertTrue(
            any("scans/<scan-dir>/evidence/policy" in err for err in payload.get("errors", [])),
            payload.get("errors"),
        )
    def test_runner_denies_direct_recon_evidence_outside_selected_repo_root(self):
        run_id = "20260520T091002Z_p3_10_direct_outside_root"
        artifact_path, artifact_payload, _ = self.emit_recon_allow_artifact()
        outside = self.tmp_path / "outside_policy_boundary_p3_10.json"
        outside.write_text(artifact_path.read_text(encoding="utf-8"), encoding="utf-8")
        completed, payload = self.invoke_runner(
            policy_artifact_path=outside,
            run_id=run_id,
            target=artifact_payload["request"]["target"],
        )
        self.assertNotEqual(completed.returncode, 0, payload)
        self.assertEqual(payload.get("verdict"), "deny", payload)
        self.assertNotIn("plan", payload)
        self.assertTrue(
            any("selected repository root" in err for err in payload.get("errors", [])),
            payload.get("errors"),
        )
    def test_runner_denies_when_copied_artifact_bytes_drift_to_deny_verdict(self):
        run_id = "20260519T120001Z_p3_9_bridge_hash_drift"
        _, artifact_payload, _ = self.emit_recon_allow_artifact()
        copied = self.copy_artifact_into_run_policy_dir(
            artifact_payload, run_id=run_id
        )
        before_sha256 = _sha256_of(copied)
        copied.write_text(
            copied.read_text(encoding="utf-8").replace(
                '"verdict": "allow"', '"verdict": "deny"', 1
            ),
            encoding="utf-8",
        )
        after_sha256 = _sha256_of(copied)
        self.assertNotEqual(
            after_sha256,
            before_sha256,
            "test must exercise direct copied-artifact byte/hash drift",
        )
        completed, payload = self.invoke_runner(
            policy_artifact_path=copied,
            run_id=run_id,
            target=artifact_payload["request"]["target"],
        )
        self.assertNotEqual(completed.returncode, 0, payload)
        self.assertEqual(payload.get("verdict"), "deny", payload)
        self.assertNotIn("plan", payload, "tampered copied artifacts must not emit a plan")
        errors = payload.get("errors") or []
        self.assertTrue(
            any("policy decision verdict must be allow" in err for err in errors),
            f"expected a policy-decision verdict hash-drift/tamper error; got {errors!r}",
        )
        self.assert_no_module_execution_leakage(completed.stdout, completed.stderr)
    def test_bridge_copy_helper_is_marked_test_only(self):
        source = Path(__file__).read_text(encoding="utf-8")
        helper_start = source.index("    def copy_artifact_into_run_policy_dir(")
        helper_end = source.index("    def invoke_runner(")
        helper_source = source[helper_start:helper_end]
        self.assertIn("test-harness-only path translation", helper_source)
        self.assertIn("must not be mirrored into runtime code", helper_source)
    def test_runner_module_io_preview_emits_no_findings_or_evidence(self):
        run_id = "20260519T120002Z_p3_9_bridge_preview"
        _, artifact_payload, _ = self.emit_recon_allow_artifact()
        copied = self.copy_artifact_into_run_policy_dir(
            artifact_payload, run_id=run_id
        )
        _, payload = self.invoke_runner(
            policy_artifact_path=copied,
            run_id=run_id,
            target=artifact_payload["request"]["target"],
            include_module_io_preview=True,
        )
        self.assertEqual(payload.get("verdict"), "allow", payload)
        inputs = payload.get("module_input_previews") or []
        results = payload.get("module_result_previews") or []
        self.assertTrue(inputs, "expected module_input_previews to be present")
        self.assertEqual(len(inputs), len(results))
        for module_input, module_result in zip(inputs, results):
            self.assertEqual(module_input.get("schema_version"), "module_input/1.0")
            self.assertEqual(module_input["run"]["mode"], "dry-run")
            self.assertIs(module_input["run"]["dry_run"], True)
            self.assertEqual(module_input["output"]["findings"], [])
            self.assertEqual(module_input["output"]["evidence"], [])
            self.assertIs(module_input["constraints"]["target_touching"], False)
            self.assertEqual(module_result.get("schema_version"), "module_result/1.0")
            self.assertEqual(module_result.get("status"), "not_executed")
            self.assertIs(module_result.get("dry_run"), True)
            self.assertIs(module_result.get("target_touching"), False)
            self.assertEqual(module_result.get("findings"), [])
            self.assertEqual(module_result.get("evidence"), [])
    def test_runner_denies_when_target_does_not_match_artifact(self):
        run_id = "20260519T120003Z_p3_9_bridge_target_mismatch"
        _, artifact_payload, _ = self.emit_recon_allow_artifact(
            target=IN_SCOPE_TARGET
        )
        copied = self.copy_artifact_into_run_policy_dir(
            artifact_payload, run_id=run_id
        )
        completed, payload = self.invoke_runner(
            policy_artifact_path=copied,
            run_id=run_id,
            target=SECONDARY_IN_SCOPE_TARGET,  # deliberately wrong target
        )
        self.assertNotEqual(completed.returncode, 0, payload)
        self.assertEqual(payload.get("verdict"), "deny", payload)
        errors = payload.get("errors") or []
        self.assertTrue(
            any("target" in err for err in errors),
            f"expected a target-mismatch error; got {errors!r}",
        )
    def test_runner_denies_when_artifact_path_is_outside_runs_policy(self):
        run_id = "20260519T120004Z_p3_9_bridge_path_outside"
        _, artifact_payload, _ = self.emit_recon_allow_artifact()
        wrong_dir = self.copy_artifact_into_run_policy_dir(
            artifact_payload, run_id=run_id, directory="other"
        )
        completed, payload = self.invoke_runner(
            policy_artifact_path=wrong_dir,
            run_id=run_id,
            target=artifact_payload["request"]["target"],
        )
        self.assertNotEqual(completed.returncode, 0, payload)
        self.assertEqual(payload.get("verdict"), "deny", payload)
        errors = payload.get("errors") or []
        self.assertTrue(
            any(
                "policy artifact path must be under runs/<run_id>/policy/<file>" in err
                for err in errors
            ),
            f"expected the path-outside-runs/<run_id>/policy/ error; got {errors!r}",
        )
    def test_runner_denies_when_helper_returncode_is_nonzero(self):
        run_id = "20260519T120005Z_p3_9_bridge_helper_failure"
        _, artifact_payload, _ = self.emit_recon_allow_artifact()
        tampered = json.loads(json.dumps(artifact_payload))
        tampered["helper"]["returncode"] = 1
        copied = self.copy_artifact_into_run_policy_dir(
            tampered, run_id=run_id
        )
        completed, payload = self.invoke_runner(
            policy_artifact_path=copied,
            run_id=run_id,
            target=tampered["request"]["target"],
        )
        self.assertNotEqual(completed.returncode, 0, payload)
        self.assertEqual(payload.get("verdict"), "deny", payload)
        errors = payload.get("errors") or []
        self.assertTrue(
            any("helper.returncode" in err for err in errors),
            f"expected a helper.returncode error; got {errors!r}",
        )
    def test_runner_denies_when_boundary_audit_event_is_deny(self):
        run_id = "20260519T120006Z_p3_9_bridge_audit_event_mismatch"
        _, artifact_payload, _ = self.emit_recon_allow_artifact()
        tampered = json.loads(json.dumps(artifact_payload))
        tampered["boundary"]["audit_event"] = "PROGRAM_POLICY_DENY"
        copied = self.copy_artifact_into_run_policy_dir(
            tampered, run_id=run_id
        )
        completed, payload = self.invoke_runner(
            policy_artifact_path=copied,
            run_id=run_id,
            target=tampered["request"]["target"],
        )
        self.assertNotEqual(completed.returncode, 0, payload)
        self.assertEqual(payload.get("verdict"), "deny", payload)
        errors = payload.get("errors") or []
        self.assertTrue(
            any(
                "boundary.audit_event must be PROGRAM_POLICY_ALLOW" in err
                for err in errors
            ),
            f"expected a boundary.audit_event mismatch error; got {errors!r}",
        )
    def test_runner_denies_when_artifact_mode_does_not_match_requested_mode(self):
        run_id = "20260519T120007Z_p3_9_bridge_mode_mismatch"
        _, artifact_payload, _ = self.emit_recon_allow_artifact(policy_mode="planned")
        copied = self.copy_artifact_into_run_policy_dir(
            artifact_payload, run_id=run_id
        )
        completed, payload = self.invoke_runner(
            policy_artifact_path=copied,
            run_id=run_id,
            target=artifact_payload["request"]["target"],
        )
        self.assertNotEqual(completed.returncode, 0, payload)
        self.assertEqual(payload.get("verdict"), "deny", payload)
        errors = payload.get("errors") or []
        self.assertTrue(
            any("mode" in err for err in errors),
            f"expected a mode-mismatch error; got {errors!r}",
        )
    def test_recon_help_has_no_bridge_specific_flag(self):
        env = os.environ.copy()
        env.update(
            {
                "HACKLAB": self.hacklab_env,
                "NO_COLOR": "1",
                "USER": env.get("USER") or env.get("USERNAME") or "Owner",
            }
        )
        result = subprocess.run(
            [BASH, "recon.sh", "--help"],
            cwd=REPO_ROOT,
            env=env,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=10,
        )
        for needle in BRIDGE_FLAG_REGRESSION_NEEDLES:
            self.assertNotIn(
                needle,
                result.stdout,
                msg=f"recon.sh --help contains forbidden bridge flag {needle!r}",
            )
    def test_runner_help_has_no_bridge_specific_flag(self):
        result = subprocess.run(
            [sys.executable, str(MODULE_RUNNER), "--help"],
            cwd=REPO_ROOT,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=10,
        )
        for needle in BRIDGE_FLAG_REGRESSION_NEEDLES:
            self.assertNotIn(
                needle,
                result.stdout,
                msg=f"module_runner.py --help contains forbidden bridge flag {needle!r}",
            )
if __name__ == "__main__":
    unittest.main()
