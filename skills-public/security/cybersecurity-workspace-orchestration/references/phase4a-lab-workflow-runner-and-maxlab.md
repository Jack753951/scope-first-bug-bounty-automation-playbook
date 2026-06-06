> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Phase 4A Lab Workflow Runner + Max-Lab Execution Lessons

Use this reference when turning a manually orchestrated local-lab bug-bounty rehearsal into a fixed workflow runner, or when the operator asks to test the upper bound of an authorized vulnerable lab.

## Pattern

Convert the manual flow into a guarded runner before adding unattended execution:

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

Initial runner posture should be `plan_only`:

- require an explicit lab flag such as `--lab-mode`
- reject public targets even when lab mode is set
- accept only local/private/intentionally vulnerable target URLs
- consume allowlisted committed candidate fixtures or repo-local evidence fixtures
- emit deterministic artifacts under a run directory
- do not open network sockets, spawn subprocesses, execute exploit tools, submit reports, or promote statuses

Recommended artifacts:

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

## Test shape

Use TDD and prove fail-closed behavior:

1. RED: tests fail because the runner does not exist.
2. Deny without explicit lab mode.
3. Deny public targets such as `https://example.com` and public IPs such as `8.8.8.8`.
4. Happy path writes all fixed artifacts without execution.
5. Max-lab plan includes bounded active checks but no destructive/loot/callback terms.
6. Adjacent candidate/report chain still refuses promotion and reportable states.

Useful validation bundle:

```bash
python -m unittest scripts.test_phase4a_lab_workflow -v
python -m unittest scripts.test_phase4a_lab_workflow scripts.test_candidate_workflow_fixture scripts.test_candidate_review_packet scripts.test_candidate_packet_gaps scripts.test_candidate_verification_plan scripts.test_report_readiness_gate -v
HACKLAB=<user-home> USER=Owner ./bin/hermes review
```

## Bounded max-lab execution posture

If the operator explicitly asks to test lab limits, keep execution separate from the plan-only runner until a reviewed execution adapter exists.

Allowed bounded local-lab examples:

- headers/CORS audit
- bounded Nikto with a short max time
- small XSS marker/reflection triage over explicit URLs
- SQLi error/boolean/time triage over explicit URLs, but no dump
- status-only authentication bypass probe with token/body redaction

Hard stops unless a new reviewed slice approves them:

- brute force
- recursive download
- DB dump or credential/loot collection
- `sqlmap --dump`, `--os-shell`, `--risk=3`, `--level=5`
- external callbacks/OAST/interactsh
- exploit chaining or persistence
- unattended execution against real bug-bounty targets

## Critical lesson: lab availability impact is real

Even bounded local-lab runs can stress or crash an intentionally vulnerable VM/container. Treat availability loss as a valuable calibration signal, not proof that the runner is ready for unattended live execution.

If a lab target becomes unreachable:

1. Stop further offensive steps.
2. Check red-team route and host reachability.
3. Inspect victim VM state and vulnerable-app container state.
4. Restart the vulnerable app or reset the VM only because it is an owned local lab.
5. Verify recovery from both victim localhost and red-team Kali host-only IP.
6. Record the availability event, recovery action, and the fact that live execution remains manual/operator-approved.

Do not encode a transient crash as a durable claim that a tool is broken. Encode the durable lesson: live execution needs pre/post health checks, timeouts, kill/recovery controls, audit logs, and redaction before it can become an adapter.

## Next execution-adapter requirements

Before moving beyond plan-only:

- explicit `--execute-lab-approved` flag
- run ID and append-only audit log
- per-step timeout and max request count
- pre-health and post-health checks
- kill/recovery hint, not silent retry loops
- token/body redaction before writing artifacts
- artifact manifest with hashes
- candidate-only conversion for active observations
- no automatic `confirmed`, `verified`, `reportable`, or submission state
- separate review/operator approval before any real bug-bounty live automation

## Reportability stance

Keep outputs candidate-only until manual verification and report-readiness review:

- XSS reflection is not confirmed XSS.
- SQLi `ERR` triage is not confirmed SQLi.
- A status-only auth-bypass response is a strong lab candidate but must be redacted and converted into a verification plan before report drafting.
- Missing headers remain informational/blocked unless impact and program rules support a report.

For lab reports, explicitly label them as `LAB ONLY / TRAINING / NOT FOR REAL BUG BOUNTY SUBMISSION`.
