> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Offline Workflow Validation Sprint

Use this pattern when a cybersecurity automation platform has accumulated several safe offline contracts (schemas, validators, preview manifests, ledgers, profile gates) but has not yet proven that the workflow produces useful triage artifacts. The goal is to prevent a "contract museum": safe and elegant platform layers that do not yet improve authorized testing or reporting.

## Trigger

- The repo already has scope/policy gates, module/run/finding/evidence contracts, dry-run previews, or preview manifests.
- The next tempting task is another schema, ledger, archive index, registry, generic builder, or runner abstraction.
- The user asks whether the project direction is right, or explicitly invites candid objections.
- A reviewer flags over-engineering or lack of end-to-end workflow proof.

## Direction Review Prompt Shape

Ask Claude/Cowork for a design-only review before implementation. Require it to challenge the plan, not rubber-stamp it:

- Should we pause platform abstraction and validate workflow value now?
- What is the lowest-risk Level 1 module that proves the path from fixture to candidate finding to triage draft?
- What must remain out of scope: live target flags, runner/recon wiring, runtime evidence writes, schema bumps, scheduler/CI integration, reports marked as confirmed?
- Which OSS concepts are relevant but should not be copied into unsafe defaults?
- What evidence would prove the sprint was useful enough to continue?

Expected verdicts: `PROCEED`, `PROCEED_WITH_LIMITS`, or `ROUTE_BACK`.

## Recommended Slice

A good first slice is `level1.security_headers_baseline`:

- Offline fixture-only input, e.g. sanitized HTTP response header snapshots.
- Standard-library-only Python module.
- Pure function such as `evaluate(fixture, *, run_id, policy_decision_sha256)`.
- CLI accepts only fixture/provenance fields; it does not accept `--target`, `--url`, `--host`, `--scope`, or `--live`.
- Emits candidate-only finding objects to stdout for tests/fixtures; does not write runtime artifacts.
- Findings carry triage-only posture: `candidate`, `scanner_output_only=true`, `manual_verification_required=true`, empty evidence, and no `confirmed` state.
- Include redacted human triage draft fixtures to exercise reviewer/reporting workflow.

## Implementation Boundaries

Do not include in this sprint:

- Network, DNS, socket, HTTP client, callback, subprocess, thread/process, async worker, scanner, or browser automation.
- Live target support or target-discovery flags.
- Runtime writes under `runs/`, `evidence/`, `reports/`, `loot/`, or scan directories.
- Runner/recon/profile/CI/hook/scheduler wiring.
- Schema version bumps or new generic archive/ledger contracts.
- Claims of confirmed vulnerabilities.

Treat any of the above as a new T3+ phase with fresh direction review and safety gates.

## Test Requirements

At minimum, add tests for:

1. Golden fixture equality for several cases.
2. Candidate finding schema validation where available.
3. Fixture version drift and unknown fields failing closed.
4. Reserved/lab placeholder targets only in committed fixtures.
5. No fixture mutation and deterministic output.
6. Explicit argparse rejection of live-target flags: `--target`, `--url`, `--host`, `--scope`, `--live`.
7. AST-backed static import checks for forbidden modules such as `socket`, `ssl`, `http`, `urllib`, `requests`, `httpx`, `aiohttp`, `subprocess`, `multiprocessing`, `threading`, `asyncio`, and `shutil`.
8. AST-backed call checks for writes such as `open(...)`, `Path.write_text`, `Path.write_bytes`, `os.remove`, `os.unlink`, `os.rename`, `os.makedirs`, and `shutil.*`.
9. Redaction boundary checks for triage drafts and rendered finding fields.

Regex checks may supplement AST checks, but should not be the only safety test.

## Review and Verification

Suggested sequence:

1. Hermes writes a P2-style direction prompt and requests independent Claude/Cowork direction review.
2. Codex implements only the approved fixture-only module, fixtures, tests, docs, and triage drafts.
3. Hermes runs focused tests, module manifest validation, full offline tests, `git diff --check`, and the project review wrapper.
4. Claude/Cowork implementation review checks target-touching/network/writes/schema/wiring boundaries and asks whether the workflow actually has value.
5. Hermes arbitrates recommendations. Address small safety-test recommendations immediately; defer runtime/runner/schema/live support to a separate phase.

## Acceptance Criteria

Accept the sprint when:

- Focused and full offline tests pass.
- Independent implementation review has no blockers.
- Review artifacts explicitly state no target touching, no network/DNS, no runtime writes, no schema bumps, and no runner/recon wiring.
- The output demonstrates a useful human/agent triage path, not only validator correctness.

## Next Step After Acceptance

Prefer a scoped CTF/training/local-lab validation only after the fixture workflow is accepted. Confirm the scope first (PortSwigger Academy, HTB/THM, local Juice Shop/DVWA, or another authorized lab), and keep findings candidate-only until manual verification, evidence, impact, remediation, and retest notes exist.
