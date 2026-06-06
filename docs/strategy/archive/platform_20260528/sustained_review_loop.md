> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Sustained Hermes / Cowork / Codex Review Loop

Purpose: keep cybersecurity lab changes safe, reviewable, and traceable.

## Default Loop

1. Hermes classifies the request and checks authorization/scope.
2. Cowork/Claude handles strategy, threat modeling, report language, and independent review.
3. For new platform contracts, schemas, module capabilities, runner boundaries, reporting workflows, evidence/finding lifecycles, or tool integrations, Cowork/Claude performs the OSS Recon Gate in `docs/policy/oss_recon_gate.md`: compare 2-5 relevant open-source projects/formats, decide what to adopt/adapt/ignore, and preserve the long-term systematized/modular/update-friendly authorized-testing architecture.
4. Codex handles concrete code/script/template edits and validation automation, constrained by the accepted direction review and OSS Recon Gate notes.
5. Cowork/Claude independently reviews Codex's result for non-trivial engineering, security-gate, scope, recon, module/plugin, evidence/finding, or reporting-integrity changes. This review must not be limited to blocking defects: it should also assess whether the change advances the operator's long-term goals (extensibility, updateability, modularity, safe automation, agent-assisted analysis), whether OSS-inspired conventions were used safely, and provide third-party recommendations.
6. Hermes verifies locally, arbitrates route-back items, and updates handoff records.

## Handoff Files

- `handoff/cowork_proposal.md` — strategy/spec before implementation.
- `handoff/codex_task.md` — constrained implementation prompt for Codex.
- `handoff/codex_review.md` — implementation summary, validation, risks, route-back notes.
- `handoff/accepted_changes.md` — append-only accepted history.
- `handoff/cowork_<phase>_review.md` — independent Claude/Cowork review after Codex for high-impact changes.
- `docs/policy/oss_recon_gate.md` — required OSS comparison process and prompt add-ons for new contracts, schemas, module/runner boundaries, result/report workflows, and external-tool integrations.
- `handoff/latest_check.md` — latest Hermes local static review.

## When Claude Review Is Required

Run independent Claude/Cowork review after Codex when changes touch:

- authorization or scope enforcement
- `safe_target`, `config/scope.txt`, or future `programs/<slug>/scope.json`
- recon automation, scanners, fuzzing, nuclei, notification behavior
- report integrity, evidence handling, or finding templates
- worker orchestration, locks, audit logs, or safety gates

Skip only for trivial documentation-only edits or explicit operator instruction.

## Review Prompt Add-On

For future Claude/Cowork review tasks, include this requirement:

```text
Do not limit the review to blocking defects. In addition to ACCEPT/ROUTE-BACK, provide third-party recommendations about architecture, extensibility, maintainability, updateability, modularity, safety gates, agent-assisted analysis, testing, and future roadmap alignment. Separate findings into:
1. Blocking issues that must route back to Codex before acceptance.
2. Non-blocking improvements worth doing soon.
3. Strategic recommendations for future phases.
4. Architecture fit: how well the change supports the operator's long-term goal of a modular, update-friendly, systematized authorized testing platform.
5. OSS Recon Gate: when the task introduces a contract/schema/module/runner/reporting/tool-integration boundary, compare 2-5 relevant open-source projects or formats, identify adopt/adapt/ignore decisions, and list unsafe patterns that must not be copied.
```

## Minimum Verification Before Done

- `bash -n` for changed shell scripts.
- Python compile where Python files exist.
- Project local review wrapper where available.
- Safe dry-run tests only unless explicit authorized scope is present.
- `.agent.lock` clear.
- Handoff files reflect final state.
