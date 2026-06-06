> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P3.10 Direction Review Prompt — Dry-Run Recon-to-Runner Runtime Bridge

Status: requested
Date: 2026-05-20
Requested by: operator via Hermes
Prepared by: Hermes

## Reviewer identity requirement

At the top of your response, state:

- Reviewer route/tool
- Visible model/runtime if exposed; if not exposed, state that the exact runtime is not exposed
- Review tier you believe applies
- Whether Hermes may decide directly, conditionally, or must escalate to operator

## Context

The cybersec lab is building an authorized bug-bounty automation platform with strict safety gates. Current P3.9 work proved, in tests only, that a recon.sh dry-run policy boundary artifact can be consumed by the existing module runner preview path after the test harness copies the artifact into a temporary `runs/<run_id>/policy/decision.json` location.

P3.9 intentionally did not authorize runtime bridge implementation. The bridge-copy helper is explicitly marked test-harness-only.

The operator now authorized this sequence: complete review and safety work first; if there are no blocking issues, proceed into implementation.

## Proposed P3.10 question

Should we implement a narrow dry-run-only runtime bridge that lets `scripts/module_runner.py` consume an explicit recon-emitted `policy_boundary/1.0` artifact directly, without test-harness copying, auto-discovery, scanner execution, or module execution?

Candidate implementation boundary if approved:

- `scripts/module_runner.py` only, plus focused tests and handoff docs.
- Keep `recon.sh` unchanged for this slice.
- Keep `config/scope.txt`, real program scopes, schemas, modules, reports, scheduler, credentials, deployment, and production settings unchanged.
- Continue to require explicit `--policy-artifact <path>`; no `--auto-bridge`, no `--from-recon`, no run-directory auto-discovery, no scheduler linkage.
- Permit the explicit artifact path to be either:
  - existing runner path: `runs/<run_id>/policy/<file>`; or
  - recon dry-run evidence path: `scans/<target>_<timestamp>/evidence/policy/policy_boundary_*.json`.
- When using a recon evidence path, do not copy or move the file. Read only, validate fail-closed, and represent `decision_artifact_path` in the plan as the repo-relative evidence path.
- Require all existing artifact checks: schema_version, boundary.status allow, audit event allow, helper returncode/timed_out, decision verdict/audit event/target/target_type/mode, empty errors/deny codes, canonical hashes, UTC timestamp.
- Add additional fail-closed path checks for recon evidence artifacts: path must resolve under the selected repo root, no symlink parent, no path traversal, filename must match `policy_boundary_*.json`, parent must be `evidence/policy`, and path should include a `scans/<scan-dir>/` ancestor.
- Add tests proving recon artifact direct read works only in dry-run preview and does not create/copy files, does not execute scanners/modules, rejects target/mode/helper/audit mismatches, rejects path escapes/wrong directories/symlinks, and does not mutate real repo protected directories.

## Out of scope / still blocked

- No live target behavior.
- No scanner/module execution.
- No fuzzing, brute force, exploit attempts, callbacks, OAST, proxy/pivot/tunnel, beacon/relay behavior.
- No `recon.sh` bridge flags or auto-discovery.
- No automatic copying from scans to runs.
- No scheduler/CI integration.
- No schema promotion.
- No report drafting/submission.
- No credentials/OAuth/tokens/private keys, deployment, billing, production settings, or repo-setting changes.
- No `config/scope.txt` or real program scope activation changes.

## Required OSS Recon Gate

Add an OSS Recon Gate comparison before recommending implementation.

Do not run scans, contact targets, trigger callbacks, or suggest live target interaction. This is a design-only review.

Compare the proposed change with 2-5 relevant open-source projects, tools, or interchange formats. Prefer relevant patterns such as SARIF artifact provenance, ProjectDiscovery JSONL/pipeline ergonomics, Nuclei metadata/unsafe-active defaults, DefectDojo lifecycle/dedup separation, OWASP ZAP alert risk/confidence/evidence, or Recon-ng/SpiderFoot workspace/module boundaries.

For each reference, state:

- Useful pattern
- Adopt / adapt / ignore decision
- Safety concern or reason not to copy directly
- Impact on our contracts: program scope, policy decision, finding/evidence schema, run manifest, module manifest, module profile, dry-run runner, module I/O preview

## Review questions

1. Decision: APPROVE / APPROVE_WITH_CHANGES / DEFER / BLOCK?
2. Is the proposed direct-read-only bridge T3, T4, or higher? Explain.
3. Is operator approval already sufficient for this dry-run-only implementation if all activation remains blocked?
4. Should the runner accept explicit recon evidence paths, or should it continue requiring copied `runs/<run_id>/policy/decision.json` artifacts?
5. Is reading an explicit recon evidence artifact without copying safer than runtime copying? Why?
6. What exact fail-closed path and artifact identity checks are required?
7. Should `decision_artifact_path` in the run plan remain `runs/<run_id>/policy/decision.json`, or reflect the real explicit recon evidence path?
8. What tests/safety assertions are mandatory before implementation acceptance?
9. What must remain blocked until T4/T5 approval?
10. What is the minimal Codex/implementation scope if approved?

## Expected output

Write the direction review to:

`handoff/cowork_p3_10_direction_review.md`

Use this template:

```text
# P3.10 Direction Review — Dry-Run Recon-to-Runner Runtime Bridge

Reviewer identity:
- Reviewer route/tool:
- Visible model/runtime:
- Tier:
- Hermes authority:

Decision:
- APPROVE / APPROVE_WITH_CHANGES / DEFER / BLOCK

OSS Recon Gate:
- references considered
- adopt/adapt/ignore decisions
- rejected unsafe patterns

Approved implementation boundary:
- in scope
- out of scope
- required fail-closed checks
- required tests

Codex/implementation guidance:
- files allowed
- files forbidden
- acceptance checks

Safety boundary:
- operator approval required before activation: yes/no and why
- target-touching/scanner/module execution status

Blocking issues:
- ...

Non-blocking recommendations:
- ...

Final Decision Block:
Decision:
Tier:
Milestone:
Hermes authority:
Reviewers consulted:
Validation performed:
Blocking findings:
Non-blocking recommendations:
Safety boundary:
OSS Recon Gate:
User approval required:
Next action:
```
