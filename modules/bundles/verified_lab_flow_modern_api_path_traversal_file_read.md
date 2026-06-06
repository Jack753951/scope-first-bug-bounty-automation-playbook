> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Verified lab flow: modern_vuln_api path traversal file-read safe-marker

Status: `verified_file_read_safe_marker_lab_only`
Last verified: 2026-05-23
OWASP mapping: A01 Broken Access Control / path traversal family; 2025 migration track: file-read boundary proof
Target lane: `local-learning-lab`

## When to use

Use this bundle when the project needs a clean, source-controlled, recoverable local-lab proof that path traversal can read a lab-owned marker file without touching sensitive system files or public targets.

This bundle complements:

- WebGoat upload-field path traversal file write.
- WebGoat Zip Slip bounded profile overwrite.
- WebGoat direct random-picture file-read attempt (`attempted-not-verified`).
- `modern_vuln_api` XXE safe-marker file read.

## Target surface

`labs/modern_vuln_api/modern_vuln_api.py` exposes:

```text
GET /file-read?name=<name>
```

The route intentionally joins a user-controlled `name` under a lab-owned public temp directory. A traversal value such as:

```text
../hermes_modern_api_file_read_marker.txt
```

can reach a lab-owned marker file created by the disposable target at startup.

## Runner

```text
scripts/labs/modern_api_path_traversal_file_read_wave1.sh
```

Default route:

- Attacker / tester: `<attacker-vm>`, host-only IP `<lab-ip>`.
- Victim / Docker target host: `<victim-vm>`, host-only IP `<lab-ip>`.
- Target port: `18083`.
- Runtime: victim-side Docker `python:3-alpine` container named `modern-api-pathread-18083`.

The runner:

1. verifies attacker/victim Internet posture;
2. copies current source-controlled target to victim;
3. starts the disposable target container;
4. waits for attacker-to-victim `/health`;
5. checks public-file control;
6. checks missing-file negative control;
7. performs one traversal request for the lab marker;
8. checks post-health;
9. cleans the target container;
10. preserves artifacts under `<artifact-output-dir>/<run_id>/`.

## Latest verified artifacts

```text
<artifact-output-dir>/modern_api_path_traversal_file_read_20260523T094352Z/
```

Key evidence:

- `summary.md`
- `run.log`
- `http/pre_health.json`
- `http/public_control.json`
- `http/missing_control.json`
- `http/traversal_positive.json`
- `http/post_health.json`
- `victim_pulled/cleanup/target_cleanup.txt`
- `victim_pulled/cleanup/victim_internet.txt`
- `cleanup/attacker_internet.txt`

Verified values from latest run:

```text
pre_health: 200
public_control_status: 200
public_control_marker_found: yes
missing_control_status: 404
missing_control_ok: yes
traversal_positive_status: 200
traversal_marker_found: yes
post_health: 200
VERDICT=verified_file_read_safe_marker_lab_only
```

Positive artifact:

```json
{
  "name": "../hermes_modern_api_file_read_marker.txt",
  "resolved": "/tmp/hermes_modern_api_public_files/../hermes_modern_api_file_read_marker.txt",
  "content": "FILE_READ_SAFE_MARKER_HERMES_LOCAL_LAB\n",
  "bytes": 39
}
```

## Success criteria

A run may be classified as `verified_file_read_safe_marker_lab_only` only when all are true:

- pre-health is `200`;
- public control returns `PUBLIC_FILE_CONTROL_HERMES_LOCAL_LAB`;
- missing-file control returns `404` or equivalent negative proof;
- traversal positive returns `FILE_READ_SAFE_MARKER_HERMES_LOCAL_LAB`;
- post-health is `200`;
- cleanup removes the target container or records why it could not;
- attacker/victim Internet posture remains closed for host-only lab execution.

## Boundary and false-positive rules

Allowed:

- lab-owned marker file read;
- lab-owned public control file read;
- one bounded traversal request against the disposable target;
- source-level explanation of the vulnerable join.

Not allowed / not claimed:

- reading `/etc/passwd`, cloud metadata, tokens, config secrets, SSH keys, or real user data;
- public/third-party targets;
- shell execution, persistence, or webshell writes;
- credential theft, exfiltration, or automatic report submission;
- claiming arbitrary sensitive file-read impact from this lab-only marker proof.

## Review / report-readiness

Latest read-only review:

```text
handoff/claude_review_modern_api_path_traversal_file_read_20260523.md
```

Reviewer classification: `verified_file_read_safe_marker_lab_only`.

Report-readiness: `reusable_methodology` / local-learning only. For a real authorized assessment, this pattern must be rerun under scope/rules/rate/evidence gates and with only program-approved, non-sensitive marker files.
