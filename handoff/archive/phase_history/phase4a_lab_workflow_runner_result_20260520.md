> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4A Lab Workflow Runner Implementation Result — 2026-05-20

Status: implemented and lab-tested
Prepared by: Hermes

## Implemented slice

Added a fixed Phase 4A lab workflow runner:

```text
scripts/phase4a_lab_workflow.py
scripts/test_phase4a_lab_workflow.py
tests/fixtures/candidate_review_packet/phase4a_juice_shop_lab/expected_findings.json
```

The runner turns the manually validated process into a deterministic artifact chain:

```text
scope_gate
-> baseline_recon
-> model_review_script_selection
-> active_script_plan
-> candidate_review_packet
-> candidate_review_gap_report
-> candidate_verification_plan
-> report_readiness_gate
-> lab_report_draft_plan
```

## Safety posture

Current runner version is plan-only:

```text
run_mode: plan_only
```

It does not perform network calls, target I/O, subprocess launches, exploit execution, report submission, or status promotion. It requires:

```text
--lab-mode
--target-url <local/private/lab URL>
--input <allowlisted committed finding fixture>
```

It rejects public targets such as `https://example.com` and public IPs such as `8.8.8.8`, even with `--lab-mode`.

## Workflow output generated for Juice Shop

Generated fixed max-lab workflow artifacts at:

```text
handoff/phase4a_lab_workflow_run_20260520_maxlab/
```

Files:

```text
workflow.json
workflow.pretty.json
script_plan.json
candidate_review_packet.json
candidate_gap_report.json
candidate_verification_plan.json
report_readiness_gate.json
lab_report_draft_plan.md
```

Summary:

```text
status: ok
run_mode: plan_only
input_count: 1
candidate_count: 2
script_step_count: 6
needs_manual_review_count: 1
blocked_count: 1
```

Max-lab planned script steps:

```text
headers_audit
cors_audit
nikto_bounded
ftp_metadata_only
xss_marker_triage
sqli_error_triage
```

## Test evidence

RED observed first:

```text
python -m unittest scripts.test_phase4a_lab_workflow -v
-> failed because scripts/phase4a_lab_workflow.py did not exist
```

GREEN / adjacent validation:

```text
python -m unittest scripts.test_phase4a_lab_workflow -v
-> 5 OK

python -m unittest scripts.test_phase4a_lab_workflow scripts.test_candidate_workflow_fixture scripts.test_candidate_review_packet scripts.test_candidate_packet_gaps scripts.test_candidate_verification_plan scripts.test_report_readiness_gate -v
-> 107 OK
```

## Lab max-capability run

Ran a bounded offensive/max-lab pass from red-team Kali against local Juice Shop:

```text
Target: http://<lab-ip>:3000
Output: /home/kali/phase4a-calibration/juice-shop-maxlab-20260520T111516Z
```

Limits enforced:

```text
local lab only
no brute force
no recursive download
no db dump
no os-shell
no external callback
```

Executed:

```text
xss_finder.sh against 3 explicitly supplied URLs
sqli_triage.sh against 3 explicitly supplied URLs, no --confirm/sqlmap dump
Nikto bounded baseline, 2-minute max time
auth-bypass status-only manual check after service recovery, token redacted
```

Observations:

```text
XSS finder: 3 reflection candidates, 0 dalfox findings
SQLi triage: 3 ERR triage hits on product search URLs
Auth bypass status-only: HTTP 200 authentication object returned with token redacted
```

Availability impact:

During/after the max-lab run, the victim became unreachable from red-team Kali and host checks. `juice-shop-lab` was later observed as exited and host-only connectivity timed out. Hermes performed a VirtualBox reset of `<victim-vm>`, restarted the container, and verified service recovery:

```text
victim eth0: <lab-ip>/24
eth1: DOWN
juice-shop-lab: Up, 0.0.0.0:3000->3000/tcp
red-team curl http://<lab-ip>:3000: HTTP/1.1 200 OK
```

Interpretation: this shows the current bounded max-lab path can stress the lab enough to cause/reveal availability failure, but it is not yet a safe unattended live-execution mode. Execution should remain manual/operator-approved until timeout/kill/recovery/audit controls are productized.

## Reportability decisions

The report-readiness gate still behaves correctly:

```text
/ftp/ directory listing: needs_manual_review
missing headers: blocked / keep out of report as standalone info finding
SQLi/auth-bypass: new lab observations only; not yet converted into committed candidate fixture/report gate artifact
XSS reflection: candidate signal only, not confirmed XSS
```

## Next recommended slice

Do not jump straight to unattended exploitation. The next implementation slice should add a controlled lab execution adapter with:

```text
explicit --execute-lab-approved flag
run ID and audit log
timeout per step
kill/recovery hints
redaction of tokens and response bodies
service health pre/post checks
no sqlmap --dump / os-shell / external callbacks
candidate-only output conversion for SQLi/auth-bypass observations
```
