> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Agent-operable capability substrate pattern

Use when a project is primarily for Hermes/agent operation rather than human-readable presentation, especially security research, lab orchestration, or bug bounty workflows.

## Core principle

Optimize artifacts for agent capability, coordination, validation, and recovery. Human readability is useful only when it helps agents or the operator make the next decision.

Do not reorganize a project just to make the repo/docs look polished for human readers. Prefer compact, machine-checkable state and contract artifacts that answer: what can Hermes safely do next, what is blocked, which agent ran, what evidence/state is current, and what learning should change future selection.

## Good artifact shape

Prefer:
- JSON/JSONL schemas with narrow consumers.
- CLI helpers with `seed`, `validate`, and `summarize` modes.
- Exit codes that distinguish local OK, operator/scope block, invalid state, and forbidden target-like arguments.
- Handoff files that are concise pointers to machine-readable state, not long narrative replacements.
- Review artifacts that record actual route/agent/role/verdict, not aspirational participation.
- Tests that prove forbidden live-target flags fail closed before argparse/network/browser/tool side effects.

Avoid:
- Broad governance frameworks before a concrete consumer exists.
- Big documentation reshuffles for human presentation.
- One-session one-skill sprawl.
- Treating readiness as authorization.
- Turning no-finding learning seeds into evidence promotion.

## Minimal triad for cybersec/lab workflows

A compact capability substrate before live target contact can include three local-only layers:

1. Role-conflict synthesis
   - Inputs: role artifacts from adversarial planner, boundary engineer, evidence critic, deterministic/safety reviewer.
   - Output: selected bounded lane, blocked-preserve, needs-local-simulation, needs-operator-control, evidence-too-weak/sensitive, no-selection.
   - Rule: if a selected candidate has `REQUEST_CHANGES`, `BLOCKED`, or `FAIL`, downgrade/park it rather than allowing execution.

2. Kali/noVNC readiness state
   - Tracks VM/profile/noVNC/shared-folder/browser/session/operator-gate readiness.
   - Must keep `target_touching_allowed=false` unless a separate explicit scope/operator gate authorizes contact.
   - Readiness answers "is the workbench ready?", not "may we touch the target?".

3. No-finding learning seed
   - Converts no-finding/surface-only/blocked outcomes into next target/lane-selection hints.
   - Reject candidate/report-ready evidence so learning cannot become proof promotion.
   - Useful classifications: `surface_only`, `needs_second_account`, `needs_paid_feature`, `needs_enterprise_feature`, `needs_existing_data`, `needs_admin_role`, `needs_integration`, `needs_callback_control`, `target_low_surface`, `policy_too_restrictive`, `auth_gate_blocked`, `evidence_too_weak`, `technique_mismatch`.

## Safety and validation rules

For local-only security workflow helpers:
- Reject target-like flags (`--target`, `--url`, `--host`, `--scope`, `--live`) in both bare and `--flag=value` forms before normal argparse dispatch, and return a structured fail-closed JSON with a stable exit code such as `30`.
- Do not import browser, network, scanner, VM-control, credential, or subprocess behavior into pure state helpers.
- Make JSONL one compact valid object per line; tests should parse each line independently.
- Use Codex/independent review when the helper will become a gate before live target contact; if the first review returns `REQUEST_CHANGES`, fix concrete blockers and rerun rather than summarizing it as success.
- Keep live target contact blocked until operator confirms exact program asset/scope facts and explicitly approves scope/config changes.

## Summary phrasing

When reporting this class of work, state:
- which routes actually ran (Hermes-local, delegate_task, Codex, Claude/Cowork, Claude Code Impl);
- which artifacts changed;
- which validation commands passed;
- what remains blocked;
- that engineering readiness is not target authorization.
