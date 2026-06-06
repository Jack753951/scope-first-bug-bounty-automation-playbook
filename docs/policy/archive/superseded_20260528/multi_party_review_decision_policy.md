> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Multi-Agent Advisory Policy

Status: active simplified policy
Owner: Hermes / Operator / Claude-Cowork / Codex
Safety posture: advisory collaboration; hard external/authorization gates remain operator-owned

## Purpose

This file replaces the old multi-party decision-gate ceremony. Multi-agent review should improve project growth, not slow it. Claude/Cowork/Codex provide tactical, architecture, safety, and evidence advice. Hermes owns synthesis and may continue when no concrete hard-stop blocker exists.

## Core Rule

Reviewer output is advisory unless it identifies a concrete blocker.

A `BLOCK`, `REQUEST_CHANGES`, or cautious reviewer tone is not enough. Hermes must translate it into a specific reason. If the reason is only better wording, optional refactor, extra caution, or future roadmap preference, record it and continue or defer.

## Concrete Blockers

Stop, fix, or ask the operator only for:

- missing/ambiguous authorization, scope, or program-rule allow;
- live target contact, scanner/fuzzer/DAST/exploit/callback/OAST/tunnel/proxy behavior outside the current approval;
- customer/non-owned data, secrets, credentials, cookies, tokens, OTPs, passwords, phone numbers, API keys, verification links, or loot;
- destructive, persistent, stealthy, evasive, brute-force, resource-exhaustive, or malware-like behavior;
- OAuth/integration/webhook/channel/mailbox/API-token/billing/payment/KYC/scheduler/deployment/publishing/report-submission activation without explicit operator approval;
- malformed machine-readable state consumed by runners;
- failing validation introduced by the slice;
- accidental deletion/overwrite of useful capability, evidence, or accepted handoff.

## When To Use External Review

Use Claude/Cowork/Codex when it clearly improves quality:

- complex architecture or contract design;
- new runner/module/report/evidence interfaces;
- non-obvious safety boundary changes;
- live-bounty candidate synthesis where multiple attacker paths should be preserved;
- report-readiness or final submission preparation;
- periodic project-health review.

Do not require external review for ordinary repo-local cleanup, local-lab proof iteration, bundle/index maintenance, validation helper work, or in-scope owned-account browser/manual work that remains within stop-before rules.

## Required Reviewer Shape When Review Is Used

Keep review artifacts compact and useful:

```text
Reviewer route/tool:
Visible model/runtime if exposed:
Context read:
Concrete blockers:
Advisory improvements:
Preserved useful hypotheses / dissent:
Validation checked:
Verdict:
```

Reviewers must not all fill the same generic approval table. Each review should contribute a distinct constraint, objection, or improvement.

## Hermes Acceptance

Before accepting non-trivial work, Hermes should confirm:

- hard stops are not crossed;
- focused validation passed or failures are explicitly deferred;
- useful reviewer dissent is preserved when review was used;
- accepted engineering/capability changes are recorded in `handoff/accepted_changes.md` when meaningful;
- active navigation/queue/index files are updated only when the current route changes.

## Operator Authority

The operator remains final authority for live activation, scope changes, secrets/credentials, external services, production/scheduler/deployment, report-ready promotion, and submission. This policy only removes unnecessary multi-agent ceremony.
