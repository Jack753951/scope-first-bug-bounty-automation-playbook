import json
import os
import shutil
import sys
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


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


@unittest.skipIf(BASH is None, "GNU bash is required for recon.sh CLI tests")
class ReconProgramCliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix=".tmp_recon_cli_", dir=REPO_ROOT)
        self.tmp_path = Path(self.tmp.name)
        self.hacklab_path = self.tmp_path / "lab"
        self.hacklab_env = self.hacklab_path.relative_to(REPO_ROOT).as_posix()
        (self.hacklab_path / "config").mkdir(parents=True)
        (self.hacklab_path / "config" / "scope.txt").write_text("authorized.test\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def make_program(self, slug="test-prog", content=None):
        if content is None:
            content = json.dumps(
                {
                    "schema_version": "1.0",
                    "program": {
                        "slug": slug,
                        "name": "Recon CLI Test",
                        "platform": "lab",
                        "url": "file:///recon-cli-test",
                        "authorization_reference": "Local unit-test fixture only.",
                        "policy_version": "2026-05-16",
                        "policy_acknowledged_at": "2026-05-16T00:00:00Z",
                    },
                    "scope": {
                        "in_scope": [{"type": "domain", "value": "authorized.test"}],
                        "out_of_scope": [],
                        "idn_handling": "punycode_only",
                    },
                    "techniques": {
                        "allowed": ["http_probe"],
                        "forbidden": ["dos", "credential_brute_force"],
                        "automation_permitted": True,
                    },
                    "rate_limits": {"max_concurrency": 1},
                    "testing_windows": {"always": True},
                    "expiration": {
                        "valid_from": "2026-01-01T00:00:00Z",
                        "valid_until": "2027-01-01T00:00:00Z",
                    },
                }
            ) + "\n"
        program_dir = self.hacklab_path / "programs" / slug
        program_dir.mkdir(parents=True)
        (program_dir / "scope.json").write_text(content, encoding="utf-8")


    def make_fake_policy_python(self, *, artifact_mode="matching"):
        fake_bin = self.hacklab_path / "fake-bin"
        fake_bin.mkdir(parents=True, exist_ok=True)
        tool = fake_bin / "python3"
        script = f"""#!/usr/bin/env bash
set -euo pipefail
if [[ "${{*}}" == *"--version"* ]]; then
  echo "Python 3.12.0"
  exit 0
fi
for arg in "$@"; do
  if [[ "$arg" == *"program_policy_boundary.py" ]]; then
    artifact_dir=""; target=""; stage=""; technique=""; mode=""; program_file=""; global_scope_file=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --artifact-dir) artifact_dir="$2"; shift 2 ;;
        --program) program_file="$2"; shift 2 ;;
        --global-scope) global_scope_file="$2"; shift 2 ;;
        --target) target="$2"; shift 2 ;;
        --stage) stage="$2"; shift 2 ;;
        --technique) technique="$2"; shift 2 ;;
        --mode) mode="$2"; shift 2 ;;
        *) shift ;;
      esac
    done
    mkdir -p "$artifact_dir"
    program_hash="$("$REAL_PYTHON" -c 'import hashlib, sys; print(hashlib.sha256(open(sys.argv[1], "rb").read()).hexdigest())' "$program_file")"
    global_hash="$("$REAL_PYTHON" -c 'import hashlib, sys; print(hashlib.sha256(open(sys.argv[1], "rb").read()).hexdigest())' "$global_scope_file")"
    decided_at="2026-05-16T00:00:00Z"
    boundary_audit_event="PROGRAM_POLICY_ALLOW"
    decision_target="$target"
    decision_verdict="allow"
    if [[ "{artifact_mode}" == "outside" ]]; then
      artifact="{self.hacklab_env}/forged_policy_outside.json"
      artifact_target="$target"
    elif [[ "{artifact_mode}" == "mismatched-target" ]]; then
      artifact="$artifact_dir/forged_policy_mismatch.json"
      artifact_target="evil.test"
    else
      artifact="$artifact_dir/forged_policy_matching.json"
      artifact_target="$target"
    fi
    if [[ "{artifact_mode}" == "decision-mismatched-target" ]]; then
      decision_target="evil.test"
    elif [[ "{artifact_mode}" == "boundary-audit-mismatch" ]]; then
      boundary_audit_event="PROGRAM_POLICY_DENY"
    elif [[ "{artifact_mode}" == "hash-mismatch" ]]; then
      program_hash="cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"
    fi
    mkdir -p "$(dirname "$artifact")"
    if [[ "{artifact_mode}" == "missing-decision" ]]; then
      printf '{{"schema_version":"policy_boundary/1.0","boundary":{{"status":"allow","audit_event":"%s"}},"request":{{"target":"%s","stage":"%s","technique":"%s","mode":"%s"}}}}\n' "$boundary_audit_event" "$artifact_target" "$stage" "$technique" "$mode" > "$artifact"
    else
      printf '{{"schema_version":"policy_boundary/1.0","boundary":{{"status":"allow","audit_event":"%s"}},"request":{{"target":"%s","stage":"%s","technique":"%s","mode":"%s"}},"decision":{{"verdict":"%s","target":"%s","technique":"%s","mode":"%s","audit_event":"PROGRAM_POLICY_ALLOW","program_file_sha256":"%s","global_scope_sha256":"%s","decided_at_utc":"%s"}}}}\n' "$boundary_audit_event" "$artifact_target" "$stage" "$technique" "$mode" "$decision_verdict" "$decision_target" "$technique" "$mode" "$program_hash" "$global_hash" "$decided_at" > "$artifact"
    fi
    echo "POLICY_BOUNDARY_STATUS=allow"
    echo "POLICY_BOUNDARY_AUDIT_EVENT=PROGRAM_POLICY_ALLOW"
    echo "POLICY_BOUNDARY_ARTIFACT=$artifact"
    echo "POLICY_BOUNDARY_DENY_REASON_CODES="
    echo "POLICY_BOUNDARY_MESSAGE=forged allow"
    echo "POLICY_BOUNDARY_PROGRAM_HASH=$program_hash"
    echo "POLICY_BOUNDARY_GLOBAL_HASH=$global_hash"
    echo "POLICY_BOUNDARY_DECIDED_AT_UTC=$decided_at"
    exit 0
  fi
done
exec "$REAL_PYTHON" "$@"
"""
        tool.write_text(script, encoding="utf-8")
        tool.chmod(0o755)

    def make_fake_tool(self, name):
        fake_bin = self.hacklab_path / "fake-bin"
        fake_bin.mkdir(parents=True, exist_ok=True)
        tool = fake_bin / name
        tool.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
        tool.chmod(0o755)

    def run_recon(self, *args, env_overrides=None):
        env = os.environ.copy()
        env.update(
            {
                "HACKLAB": self.hacklab_env,
                "NO_COLOR": "1",
                "USER": "Owner",
            }
        )
        fake_bin = self.hacklab_path / "fake-bin"
        if fake_bin.exists():
            env["PATH"] = f"{fake_bin}{os.pathsep}{env.get('PATH', '')}"
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
            timeout=30,
        )

    def test_valid_program_dry_run_runs_policy_gate_and_writes_artifact(self):
        self.make_program()
        result = self.run_recon(
            "--dry-run",
            "--program",
            "test-prog",
            "--policy-mode",
            "dry-run",
            "authorized.test",
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("DRY-RUN enabled", result.stdout)
        self.assertIn("policy PASS stage=find_live_hosts.input", result.stdout)
        scan_roots = list((self.hacklab_path / "scans").glob("authorized.test_*"))
        self.assertTrue(scan_roots)
        artifacts = list((scan_roots[-1] / "evidence" / "policy").glob("*.json"))
        self.assertTrue(artifacts)

    def test_no_program_dry_run_has_no_policy_output_or_audit(self):
        result = self.run_recon("--dry-run", "authorized.test")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertNotIn("POLICY_", result.stdout)
        audit_log = self.hacklab_path / "logs" / "audit.log"
        self.assertTrue(audit_log.exists())
        self.assertNotIn("POLICY_", audit_log.read_text(encoding="utf-8"))
        scan_roots = list((self.hacklab_path / "scans").glob("authorized.test_*"))
        self.assertTrue(scan_roots)
        self.assertFalse((scan_roots[-1] / "evidence" / "policy").exists())

    def test_allow_cidr_is_accepted_with_policy_gate(self):
        self.make_program()
        result = self.run_recon(
            "--dry-run",
            "--program",
            "test-prog",
            "--policy-mode",
            "dry-run",
            "--allow-cidr",
            "authorized.test",
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("policy PASS stage=find_live_hosts.input", result.stdout)

    def test_planned_and_live_modes_are_accepted_with_dry_run(self):
        for mode in ["planned", "live"]:
            with self.subTest(mode=mode):
                self.make_program(f"test-{mode}")
                result = self.run_recon(
                    "--dry-run",
                    "--program",
                    f"test-{mode}",
                    "--policy-mode",
                    mode,
                    "authorized.test",
                )
                self.assertEqual(result.returncode, 0, result.stdout)
                self.assertIn("policy PASS stage=find_live_hosts.input", result.stdout)

    def test_domain_enumeration_policy_deny_skips_subfinder_and_crt_dry_run(self):
        self.make_program()
        for tool in ["subfinder", "curl", "jq"]:
            self.make_fake_tool(tool)
        result = self.run_recon("--dry-run", "--domain", "--program", "test-prog", "--policy-mode", "dry-run", "authorized.test")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("program policy denied subdomain enumeration", result.stdout)
        self.assertNotIn("DRY: subfinder", result.stdout)
        self.assertNotIn("DRY: curl -s https://crt.sh", result.stdout)

    def test_policy_boundary_ignores_pythonpath_sitecustomize_bypass_attempt(self):
        self.make_program()
        for tool in ["subfinder", "curl", "jq"]:
            self.make_fake_tool(tool)
        poison_dir = self.hacklab_path / "python-poison"
        poison_dir.mkdir()
        (poison_dir / "sitecustomize.py").write_text(
            """
import json, os, sys
if '--artifact-dir' in sys.argv:
    artifact_dir = sys.argv[sys.argv.index('--artifact-dir') + 1]
    target = sys.argv[sys.argv.index('--target') + 1]
    os.makedirs(artifact_dir, exist_ok=True)
    artifact = os.path.join(artifact_dir, 'forged_allow.json')
    with open(artifact, 'w', encoding='utf-8') as handle:
        json.dump({'schema_version': 'policy_boundary/1.0', 'boundary': {'status': 'allow'}, 'request': {'target': target}}, handle)
    print('POLICY_BOUNDARY_STATUS=allow')
    print('POLICY_BOUNDARY_AUDIT_EVENT=PROGRAM_POLICY_ALLOW')
    print(f'POLICY_BOUNDARY_ARTIFACT={artifact}')
    print('POLICY_BOUNDARY_DENY_REASON_CODES=')
    print('POLICY_BOUNDARY_MESSAGE=forged allow')
    os._exit(0)
""".lstrip(),
            encoding="utf-8",
        )
        result = self.run_recon(
            "--dry-run",
            "--domain",
            "--program",
            "test-prog",
            "--policy-mode",
            "dry-run",
            "authorized.test",
            env_overrides={"PYTHONPATH": str(poison_dir)},
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("program policy denied subdomain enumeration", result.stdout)
        self.assertNotIn("forged allow", result.stdout)
        self.assertNotIn("DRY: subfinder", result.stdout)


    def test_policy_allow_artifact_outside_policy_dir_is_rejected(self):
        self.make_program()
        self.make_fake_tool("httpx")
        self.make_fake_policy_python(artifact_mode="outside")
        result = self.run_recon(
            "--dry-run",
            "--program",
            "test-prog",
            "--policy-mode",
            "dry-run",
            "authorized.test",
            env_overrides={"REAL_PYTHON": sys.executable},
        )
        self.assertEqual(result.returncode, 3, result.stdout)
        self.assertIn("policy DENY stage=find_live_hosts.input", result.stdout)
        self.assertIn("policy artifact validation failed", result.stdout)
        self.assertNotIn("DRY: httpx", result.stdout)

    def test_policy_allow_artifact_request_mismatch_is_rejected(self):
        self.make_program()
        self.make_fake_tool("httpx")
        self.make_fake_policy_python(artifact_mode="mismatched-target")
        result = self.run_recon(
            "--dry-run",
            "--program",
            "test-prog",
            "--policy-mode",
            "dry-run",
            "authorized.test",
            env_overrides={"REAL_PYTHON": sys.executable},
        )
        self.assertEqual(result.returncode, 3, result.stdout)
        self.assertIn("policy DENY stage=find_live_hosts.input", result.stdout)
        self.assertIn("policy artifact validation failed", result.stdout)
        self.assertNotIn("DRY: httpx", result.stdout)

    def test_policy_allow_artifact_missing_decision_is_rejected(self):
        self.make_program()
        self.make_fake_tool("httpx")
        self.make_fake_policy_python(artifact_mode="missing-decision")
        result = self.run_recon(
            "--dry-run",
            "--program",
            "test-prog",
            "--policy-mode",
            "dry-run",
            "authorized.test",
            env_overrides={"REAL_PYTHON": sys.executable},
        )
        self.assertEqual(result.returncode, 3, result.stdout)
        self.assertIn("policy DENY stage=find_live_hosts.input", result.stdout)
        self.assertIn("policy artifact validation failed", result.stdout)
        self.assertNotIn("DRY: httpx", result.stdout)

    def test_policy_allow_artifact_decision_target_mismatch_is_rejected(self):
        self.make_program()
        self.make_fake_tool("httpx")
        self.make_fake_policy_python(artifact_mode="decision-mismatched-target")
        result = self.run_recon(
            "--dry-run",
            "--program",
            "test-prog",
            "--policy-mode",
            "dry-run",
            "authorized.test",
            env_overrides={"REAL_PYTHON": sys.executable},
        )
        self.assertEqual(result.returncode, 3, result.stdout)
        self.assertIn("policy DENY stage=find_live_hosts.input", result.stdout)
        self.assertIn("policy artifact validation failed", result.stdout)
        self.assertNotIn("DRY: httpx", result.stdout)

    def test_policy_allow_artifact_boundary_audit_mismatch_is_rejected(self):
        self.make_program()
        self.make_fake_tool("httpx")
        self.make_fake_policy_python(artifact_mode="boundary-audit-mismatch")
        result = self.run_recon(
            "--dry-run",
            "--program",
            "test-prog",
            "--policy-mode",
            "dry-run",
            "authorized.test",
            env_overrides={"REAL_PYTHON": sys.executable},
        )
        self.assertEqual(result.returncode, 3, result.stdout)
        self.assertIn("policy DENY stage=find_live_hosts.input", result.stdout)
        self.assertIn("policy artifact validation failed", result.stdout)
        self.assertNotIn("DRY: httpx", result.stdout)

    def test_policy_allow_artifact_hash_mismatch_is_rejected(self):
        self.make_program()
        self.make_fake_tool("httpx")
        self.make_fake_policy_python(artifact_mode="hash-mismatch")
        result = self.run_recon(
            "--dry-run",
            "--program",
            "test-prog",
            "--policy-mode",
            "dry-run",
            "authorized.test",
            env_overrides={"REAL_PYTHON": sys.executable},
        )
        self.assertEqual(result.returncode, 3, result.stdout)
        self.assertIn("policy DENY stage=find_live_hosts.input", result.stdout)
        self.assertIn("policy artifact validation failed", result.stdout)
        self.assertNotIn("DRY: httpx", result.stdout)

    def test_program_policy_timeout_must_be_integer_within_bounds(self):
        self.make_program()
        self.make_fake_tool("httpx")
        for timeout_value in ["0", "61", "099", "000", "18446744073709551617", "not-int"]:
            with self.subTest(timeout_value=timeout_value):
                result = self.run_recon(
                    "--dry-run",
                    "--program",
                    "test-prog",
                    "--policy-mode",
                    "dry-run",
                    "authorized.test",
                    env_overrides={"PROGRAM_POLICY_TIMEOUT_SECS": timeout_value},
                )
                self.assertEqual(result.returncode, 3, result.stdout)
                self.assertIn("invalid program policy timeout", result.stdout)
                self.assertNotIn("DRY: httpx", result.stdout)

    def test_cidr_requires_allow_cidr_in_program_mode(self):
        (self.hacklab_path / "config" / "scope.txt").write_text("192.0.2.0/24\n", encoding="utf-8")
        program = json.loads((self.hacklab_path / "programs" / "dummy" / "missing.json").read_text(encoding="utf-8")) if False else None
        cidr_program = {
            "schema_version": "1.0",
            "program": {
                "slug": "cidr-prog",
                "name": "CIDR Test",
                "platform": "lab",
                "url": "file:///cidr-test",
                "authorization_reference": "Local unit-test fixture only.",
                "policy_version": "2026-05-16",
                "policy_acknowledged_at": "2026-05-16T00:00:00Z",
            },
            "scope": {"in_scope": [{"type": "cidr", "value": "192.0.2.0/24"}], "out_of_scope": [], "idn_handling": "punycode_only"},
            "techniques": {"allowed": ["http_probe"], "forbidden": ["dos", "credential_brute_force"], "automation_permitted": True},
            "rate_limits": {"max_concurrency": 1},
            "testing_windows": {"always": True},
            "expiration": {"valid_from": "2026-01-01T00:00:00Z", "valid_until": "2027-01-01T00:00:00Z"},
        }
        self.make_program("cidr-prog", json.dumps(cidr_program) + "\n")
        self.make_fake_tool("httpx")
        result = self.run_recon("--dry-run", "--program", "cidr-prog", "--policy-mode", "dry-run", "192.0.2.0/24")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("CIDR targets require --allow-cidr", result.stdout)
        self.assertNotIn("DRY: httpx", result.stdout)

    def test_policy_mode_is_case_sensitive(self):
        self.make_program()
        result = self.run_recon("--dry-run", "--program", "test-prog", "--policy-mode", "DRY-RUN", "authorized.test")
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("--policy-mode must be lowercase", result.stdout)

    def test_program_requires_policy_mode(self):
        self.make_program()
        result = self.run_recon("--dry-run", "--program", "test-prog", "authorized.test")
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("--program requires --policy-mode", result.stdout)

    def test_policy_mode_requires_program(self):
        result = self.run_recon("--dry-run", "--policy-mode", "dry-run", "authorized.test")
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("--policy-mode requires --program", result.stdout)

    def test_policy_dry_run_requires_recon_dry_run(self):
        self.make_program()
        result = self.run_recon("--program", "test-prog", "--policy-mode", "dry-run", "authorized.test")
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("--policy-mode dry-run requires --dry-run", result.stdout)

    def test_program_is_incompatible_with_skip_scope_check(self):
        self.make_program()
        result = self.run_recon(
            "--dry-run",
            "--program",
            "test-prog",
            "--policy-mode",
            "dry-run",
            "--skip-scope-check",
            "authorized.test",
        )
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("--program is incompatible with --skip-scope-check", result.stdout)

    def test_program_rejects_invalid_slugs_and_path_like_values(self):
        invalid_slugs = [
            "",
            "BadSlug",
            "bad_slug",
            "bad.slug",
            "bad/slug",
            "bad\\slug",
            "../bad",
            ".bad",
            "-bad",
            "_examples",
            "_schema",
            "bad slug",
            "a" * 64,
        ]
        for slug in invalid_slugs:
            with self.subTest(slug=slug):
                result = self.run_recon("--dry-run", "--program", slug, "--policy-mode", "dry-run", "authorized.test")
                self.assertEqual(result.returncode, 2, result.stdout)

    def test_program_scope_file_must_exist(self):
        (self.hacklab_path / "programs").mkdir(parents=True)
        result = self.run_recon(
            "--dry-run",
            "--program",
            "missing-prog",
            "--policy-mode",
            "dry-run",
            "authorized.test",
        )
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("--program scope file missing", result.stdout)

    def test_program_scope_symlink_outside_programs_is_rejected(self):
        outside = self.tmp_path / "outside-scope.json"
        outside.write_text("{}\n", encoding="utf-8")
        program_dir = self.hacklab_path / "programs" / "link-prog"
        program_dir.mkdir(parents=True)
        try:
            os.symlink(outside, program_dir / "scope.json")
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"symlink creation unavailable: {exc}")

        result = self.run_recon(
            "--dry-run",
            "--program",
            "link-prog",
            "--policy-mode",
            "dry-run",
            "authorized.test",
        )
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("resolves outside", result.stdout)

    def test_program_scope_symlink_to_other_program_is_rejected(self):
        self.make_program("real-prog")
        alias_dir = self.hacklab_path / "programs" / "alias-prog"
        alias_dir.mkdir(parents=True)
        try:
            os.symlink(self.hacklab_path / "programs" / "real-prog" / "scope.json", alias_dir / "scope.json")
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"symlink creation unavailable: {exc}")

        result = self.run_recon(
            "--dry-run",
            "--program",
            "alias-prog",
            "--policy-mode",
            "dry-run",
            "authorized.test",
        )
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("must resolve exactly", result.stdout)


if __name__ == "__main__":
    unittest.main()
