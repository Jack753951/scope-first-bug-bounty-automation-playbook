> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Verified Lab Flow — tmp npm path traversal arbitrary file creation safe-marker

Status: `verified_tmp_path_traversal_arbitrary_file_creation_lab_only`
Last verified: 2026-05-27
Source advisory: `<specific-ghsa-id>`
Package under test: `tmp@0.2.5` (`<0.2.6` vulnerable; `0.2.6` patched per GitHub Advisory)
OWASP mapping: A01 Broken Access Control / path traversal family; A06 Vulnerable and Outdated Components context
Target lane: `local-learning-lab`

## When to use

Use this bundle when the project needs a source-controlled, recoverable local-lab proof pattern for dependency-level path traversal where user-controlled temporary-file naming options escape the intended base directory.

This bundle is a marker-only proof. It demonstrates arbitrary file creation only within a lab-owned artifact directory and does not claim code execution, sensitive file read, web-root write, persistence, overwrite of existing files, or container escape.

## Candidate selection

The candidate was selected from the 2026-05-27 vuln-intel refresh:

- ID: `<specific-ghsa-id>`
- Title: `tmp has Path Traversal via unsanitized prefix/postfix that enables directory escape`
- Class: `file-read/path-traversal`, `auth/access-control`
- Safe proof reason: npm package behavior can be verified entirely in a disposable Kali victim-lab artifact directory with synthetic marker files.

This was chosen over heavier/product-specific candidates because it required no live target, no account, no scanner/fuzzer/DAST, no callback/OAST, no secrets, and no privileged host Docker socket.

## Runner

```text
scripts/labs/tmp_path_traversal_safe_marker_wave1.sh
```

The runner:

1. rejects target-like/live flags (`--target`, `--url`, `--host`, `--scope`, `--live`, `--scan`, `--exploit`) with structured JSON and exit 30;
2. requires exact local-lab approval phrase `RUN_TMP_PATH_TRAVERSAL_ON_LOCAL_LAB`;
3. installs `tmp@0.2.5` inside the victim-lab run artifact app directory;
4. creates a lab-owned `safe-base/` and sibling `escape-zone/`;
5. creates a control temp file that must stay inside `safe-base/`;
6. creates a marker-only escaped temp file using `prefix: '../escape-zone/TMP_PATH_TRAVERSAL_MARKER_'`;
7. emits JSON and Markdown evidence under the run artifact directory.

## Latest verified artifacts

```text
<artifact-output-dir>/tmp_path_traversal_ghsa_ph9p_20260527T1238Z/
```

Key evidence:

- `proof.json`
- `summary.md`
- `proof_stdout.json`
- victim-side app directory and lab-owned target directory under the same run artifact root

Verified values from latest run:

```text
status: ok
verdict: verified_tmp_path_traversal_arbitrary_file_creation_lab_only
package_version: 0.2.5
control_inside_safe_base: true
escaped_inside_safe_base: false
escaped_relative_to_safe_base: ../escape-zone/TMP_PATH_TRAVERSAL_MARKER_-4092-0tS7B4yhMz4X
escaped_marker_found: true
control_marker_found: true
```

Relevant sanitized artifact excerpt:

```json
{
  "status": "ok",
  "verdict": "verified_tmp_path_traversal_arbitrary_file_creation_lab_only",
  "advisory": "<specific-ghsa-id>",
  "package": "tmp",
  "package_version": "0.2.5",
  "control_inside_safe_base": true,
  "escaped_inside_safe_base": false,
  "escaped_marker_found": true,
  "control_marker_found": true
}
```

## Lab posture and recovery

- Attacker/control plane: Windows Hermes -> Kali SSH bridge.
- Victim: `<victim-vm>`, host-only IP `<lab-ip>`.
- Temporary NAT was enabled only long enough for npm package acquisition on the victim VM, then disabled and cable state closed.
- Final victim route check showed only host-only/docker routes and `INTERNET_CLOSED_EXPECTED`.
- No Docker socket was mounted or used by this proof.
- The proof writes only inside the run artifact directory under `/home/kali/codex-output/<artifact-output-dir>/<run_id>/`.

## Success criteria

A run may be classified as `verified_tmp_path_traversal_arbitrary_file_creation_lab_only` only when all are true:

- the runner was invoked with exact local-lab approval;
- target-like/live flags were not supplied and regression rejects them;
- package under test is the intentionally vulnerable `tmp@0.2.5`;
- control temp file remains inside the configured `safe-base/`;
- escaped temp file resolves outside `safe-base/` but still inside lab-owned artifact `target/`;
- escaped marker content is present;
- no secret/system file is read or written;
- final posture records that temporary NAT was closed after package acquisition.

## Boundary and false-positive rules

Allowed:

- creating synthetic marker files inside a lab-owned artifact directory;
- proving path containment failure with `path.relative()`/realpath evidence;
- comparing positive escape with a control inside the safe base.

Not allowed / not claimed:

- public/third-party target testing;
- reading `/etc/passwd`, cloud metadata, tokens, configs, SSH keys, or user data;
- writing web roots, cron paths, shell profiles, app config, or existing files;
- code execution, persistence, credential access, container escape, or host compromise;
- scanner/fuzzer/DAST/OAST/callback behavior;
- report-ready live finding status.

## Live-target prerequisite mapping

For live bounty, this proof pattern is usable only when all are true:

- program scope/rules explicitly permit file/path behavior testing and dependency-behavior evidence;
- the app exposes user-controlled input that flows into `tmp` `prefix`, `postfix`, or `dir` options;
- the proof can be constrained to operator-owned synthetic paths/files and a non-sensitive marker;
- testing stops before overwrite, sensitive file access, web-root writes, persistence, or non-owned data;
- evidence is redacted and manually reviewed before any report packet.

This bundle is a local proof pattern, not live authorization.

## 2026-05-28 re-verification with patched control

Latest verified artifacts:

```text
<artifact-output-dir>/three_latest_npm_vulns_20260528T110251Z/evidence/
```

Updated values:

```text
status: verified
vulnerable_version: 0.2.5
patched_control_version: 0.2.6
vulnerable escaped: true
vulnerable marker wrote: true
patched marker wrote: false
patched error: Relative value not allowed
```

This re-run strengthened the original 2026-05-27 proof by adding an explicit `tmp@0.2.6` patched negative control. The boundary remains local lab only and not live authorization.
