> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Claude/Cowork Independent Review — Phase 1 P1-4 Runtime Integration

Generated: 2026-05-16 12:24:00

## Verdict

ACCEPT / PASS

## Scope Reviewed

- `recon.sh` per-stage program policy runtime wiring
- `scripts/program_policy_boundary.py` boundary/helper subprocess hardening
- `scripts/test_program_policy_boundary.py` boundary contract and isolation regressions
- `scripts/test_recon_program_cli.py` recon CLI/runtime policy regressions
- `bin/hermes` Git-Bash/Windows review environment hardening

## Blocking Issues

None remaining after the final fix.

## Blocking Issues Found And Resolved During Review

1. Environment override bypass
   - Finding: `PROGRAM_POLICY_BOUNDARY` / `PROGRAM_POLICY_PYTHON` could replace the policy boundary/interpreter and forge allow decisions.
   - Resolution: `recon.sh` now fixes the boundary path to the repo-owned `scripts/program_policy_boundary.py` and only selects `python3`/`python`.

2. Boundary Python startup bypass
   - Finding: `PYTHONPATH/sitecustomize.py` could run before the boundary script and forge allow stdout/artifacts.
   - Resolution: `recon.sh` now invokes the boundary with Python isolated mode (`python -I`).
   - Regression: `test_policy_boundary_ignores_pythonpath_sitecustomize_bypass_attempt`.

3. Child helper Python startup bypass
   - Finding: boundary used isolated Python, but its child helper subprocess still inherited Python startup/import environment and could be poisoned by `PYTHONPATH/sitecustomize.py`.
   - Resolution: `_build_helper_command()` now invokes the helper as `[sys.executable, "-I", helper_path, ...]`.
   - Regression: `test_helper_subprocess_ignores_pythonpath_sitecustomize_bypass_attempt`.

## Safety / Security Observations

- Global `safe_target` remains the first authorization gate; program policy is an additional second gate, not a replacement.
- Program policy decisions are fail-closed: deny/error/missing artifact prevents stage consumption.
- Domain enumeration policy is evaluated before `subfinder`/`crt.sh` dry-run/live command construction.
- Live probe, port scan, service fingerprint, web URL generation, directory brute force, and nuclei inputs are gated before target-touching execution paths.
- CIDR targets in program policy mode require explicit `--allow-cidr`; otherwise a local forced-deny artifact is generated and target-touching tools are not invoked.
- Boundary and helper subprocesses use Python isolated mode to block `PYTHONPATH`/user-site `sitecustomize.py` allow-forgery attempts.

## Validation Evidence

- PASS: `bash -n recon.sh bin/hermes`
- PASS: `env -u PYTHONIOENCODING -u PYTHONUTF8 python -m py_compile scripts/program_policy_boundary.py scripts/test_program_policy_boundary.py scripts/test_recon_program_cli.py`
- PASS: `env -u PYTHONIOENCODING -u PYTHONUTF8 python -m pytest scripts/test_program_policy_boundary.py scripts/test_recon_program_cli.py scripts/test_program_policy_check.py -q`
  - Result: `40 passed, 2 skipped, 15 subtests passed`
- PASS: `HACKLAB="$PWD" ./bin/hermes review`
  - Python Compile OK
  - Shell scripts bash-n OK
  - Lock clear
- PASS: static added-line scans found no hardcoded secrets, shell=True/os.system, eval/exec, pickle, or SQL string-formatting patterns.

## Non-Blocking Recommendations

- Defense-in-depth: have `recon.sh` validate that returned policy artifacts resolve under `$POLICY_ARTIFACT_DIR` and that artifact request fields match the current stage/target/technique/mode before accepting allow.
- Consider bounding and validating `PROGRAM_POLICY_TIMEOUT_SECS` if kept as an environment/configurable value.
- Consider policy-gating `web_probe` post-httpx output for evidence consistency, even though later target-touching consumers already re-gate URLs.
- Long term: move repeated Bash policy plumbing into clearer `gate_stage_targets` / `gate_single_target` helpers or Python core modules as the platform modularizes.

## Final Reviewer Verdict

PASS. The previously identified program policy bypasses have been resolved. No remaining blocking target-touching safety defect was found in the reviewed diff.
