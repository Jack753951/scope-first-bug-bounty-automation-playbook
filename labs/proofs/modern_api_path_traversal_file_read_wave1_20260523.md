> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# modern_vuln_api path traversal file-read safe-marker wave 1

Date: 2026-05-23
Status: `verified_file_read_safe_marker_lab_only`
Lane: second file read / path traversal safe-marker target

## Route / tool

- Control plane: Windows Hermes, repo `<private-workspace>`.
- Attacker / tester: `<attacker-vm>`, host-only `<lab-ip>`.
- Victim / Docker target host: `<victim-vm>`, host-only `<lab-ip>`.
- Runner: `scripts/labs/modern_api_path_traversal_file_read_wave1.sh`.
- Target: `http://<lab-ip>:18083/file-read?name=`.
- Runtime: victim-side Docker `python:3-alpine`, container `modern-api-pathread-18083`.
- Artifact root: `<artifact-output-dir>/modern_api_path_traversal_file_read_20260523T094352Z/`.
- Preview: `handoff/modern_api_path_traversal_file_read_preview_20260523.md`.
- Review: `handoff/claude_review_modern_api_path_traversal_file_read_20260523.md`.

## Source / OSS / target decision

Existing project references and prior waves covered the path traversal family:

- WebGoat upload-write and Zip Slip verified bundles.
- WebGoat direct random-picture retrieval attempt: `attempted-not-verified` because app/Tomcat rejected traversal before marker content was read.
- `owasp-single-vuln-lab-wave` reference: `webgoat-path-traversal-zipslip-proofs.md`.

Decision: `write-custom` bounded local target expansion.

Reason: this lane needed a clean second file-read proof using lab-owned marker files only. A small source-controlled target route is more deterministic and safer than forcing WebGoat's direct-read endpoint or touching sensitive system files.

## Target change

Updated `labs/modern_vuln_api/modern_vuln_api.py` with a deliberately vulnerable local-lab route:

```text
GET /file-read?name=<name>
```

The route creates these lab-owned fixtures at startup:

- public control: `/tmp/hermes_modern_api_public_files/public.txt`
- marker file: `/tmp/hermes_modern_api_file_read_marker.txt`

The route naively joins `FILE_READ_PUBLIC_DIR / name`, so `../hermes_modern_api_file_read_marker.txt` reads the marker file.

## Execution summary

Command run from Windows control plane via project Kali wrapper:

```text
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ./scripts/kali-run.ps1 -Command 'cd /mnt/hacking && bash scripts/labs/modern_api_path_traversal_file_read_wave1.sh'
```

Result:

```text
RUN_ID=modern_api_path_traversal_file_read_20260523T094352Z
pre_health=200
public_control_status=200
missing_control_status=404
traversal_positive_status=200
post_health=200
public_marker_found=yes
missing_control_ok=yes
traversal_marker_found=yes
VERDICT=verified_file_read_safe_marker_lab_only
```

## Evidence

Summary artifact:

```text
<artifact-output-dir>/modern_api_path_traversal_file_read_20260523T094352Z/summary.md
```

Positive traversal artifact:

```text
<artifact-output-dir>/modern_api_path_traversal_file_read_20260523T094352Z/http/traversal_positive.json
```

Positive content:

```json
{
  "name": "../hermes_modern_api_file_read_marker.txt",
  "resolved": "/tmp/hermes_modern_api_public_files/../hermes_modern_api_file_read_marker.txt",
  "content": "FILE_READ_SAFE_MARKER_HERMES_LOCAL_LAB\n",
  "bytes": 39
}
```

Control artifact:

```text
<artifact-output-dir>/modern_api_path_traversal_file_read_20260523T094352Z/http/public_control.json
```

Control content:

```json
{
  "name": "public.txt",
  "resolved": "/tmp/hermes_modern_api_public_files/public.txt",
  "content": "PUBLIC_FILE_CONTROL_HERMES_LOCAL_LAB\n",
  "bytes": 37
}
```

Negative control:

```text
missing_control_status=404
<artifact-output-dir>/modern_api_path_traversal_file_read_20260523T094352Z/http/missing_control.json
```

Cleanup / network posture:

- `cleanup/attacker_internet.txt`: `internet_closed`
- `victim_pulled/cleanup/victim_internet.txt`: `internet_closed`
- `victim_pulled/cleanup/target_cleanup.txt`: target container removed

## Review result

Read-only review route/tool: Hermes `delegate_task` evidence review with file/terminal toolsets.
Visible model/runtime: delegate reported `gpt-5.5`; exact hosted runtime otherwise not exposed.
Usage artifact path: current Hermes transcript; review saved to `handoff/claude_review_modern_api_path_traversal_file_read_20260523.md`.

Reviewer classification: `verified_file_read_safe_marker_lab_only`.

Reviewer caution:

- Do not claim real-target exploitability or a production finding.
- Do not claim arbitrary sensitive file read.
- The proof supports only lab-owned marker file read through a source-controlled intentionally vulnerable local target.
- Packet-grade raw headers / Docker inspect metadata would be optional hardening, not required for this local-lab classification.

## Boundary

Local authorized lab only. Lab-owned marker files only. No public targets, sensitive system files, credentials, secrets, shell, persistence, exfiltration, automatic finding promotion, or report submission.

## 對專案有什麼幫助

- 補上先前 WebGoat direct file-read attempt 缺少的「實際 marker content read」證據。
- 讓 proof library 的 file-read/path traversal 類別不只停在 upload-write、Zip Slip overwrite、XXE safe-marker，而有一個乾淨的 path traversal read primitive。
- 強化 `script-first + context-driven + one-vuln max-impact proof`：從 WebGoat 不適合的 direct-read surface，切到 source-controlled disposable target，而不是硬把不乾淨的結果說成成功。
- 提供未來 bug bounty / pentest 的安全證據習慣：用 lab-owned marker、positive/control/negative/post-health，而不是讀敏感系統檔。

## 新增/更新了什麼

- Updated target: `labs/modern_vuln_api/modern_vuln_api.py`
- Added runner: `scripts/labs/modern_api_path_traversal_file_read_wave1.sh`
- Added preview: `handoff/modern_api_path_traversal_file_read_preview_20260523.md`
- Added review: `handoff/claude_review_modern_api_path_traversal_file_read_20260523.md`
- Added handoff: `handoff/modern_api_path_traversal_file_read_wave1_20260523.md`
- Added bundle: `modules/bundles/verified_lab_flow_modern_api_path_traversal_file_read.md`
- Added artifacts: `<artifact-output-dir>/modern_api_path_traversal_file_read_20260523T094352Z/`

## Recommended next step

Stop this lane and update navigation/proof-library records. If packetizing later, add optional raw headers / curl verbose transcript / Docker inspect metadata, but do not rerun just for the base proof.
