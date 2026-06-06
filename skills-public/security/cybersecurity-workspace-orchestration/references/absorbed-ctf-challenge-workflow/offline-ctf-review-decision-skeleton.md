> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Offline CTF artifact + review-decision skeleton

Use this as a reusable implementation pattern when turning CTF drills into safe workflow tooling.

## Components

1. `ctf_prepare_challenge.py`
   - creates a local ignored workspace such as `setting/local/ctf/<slug>/`
   - writes `challenge.json` with operator-supplied slug/category/source/Kali-required flag
   - writes `solve_notes.md` containing an output-side review checklist
   - refuses overwrite by default; supports explicit `--force`
   - derives nothing from a URL/host and performs no network action

2. `ctf_review_decision.py`
   - reads solver-result JSON from stdin/file
   - emits deterministic sorted JSON
   - classifies status as `hint`, `candidate`, `verified`, or `needs_second_review`
   - keeps `confidence` as a separate `low|medium|high` axis
   - includes `triggers`, `reasons`, `ignored_fields`, and an `input_hash`

3. `ctf_verifier_metadata.yaml`
   - template only, not a schema/registry contract
   - document `mode`, `requires_scope`, `destructive`, `oracle_required`, second-review triggers, and evidence outputs
   - do not add severity/CVSS/exploitability axes in the first skeleton

## Required conservative triggers

- `abnormal_format`: candidate does not match expected wrapper/format, including no-wrapper cases when the expected regex says otherwise
- `multiple_candidates`: more than one plausible answer
- `solver_timeout`: SMT/solver/tool timed out or gave partial/underconstrained output
- `external_source_only`: candidate came only from public writeup/source
- `ui_or_checker_only`: only UI/checker success, no independent invariant/replay

Any trigger should produce `needs_second_review` and cap confidence at `low`.

## Boundary tests

Add tests proving:

- normal verified output becomes `verified`
- each trigger separately causes `needs_second_review`
- deterministic repeated input produces byte-identical output
- preparer refuses to overwrite without `--force`
- target/scope override fields are ignored and never grant verification

## Worker routing

This skeleton is a good candidate for Claude Code Pro/OAuth implementation because it is offline/local coding with tests. Keep Hermes as verifier and record the route in handoff logs. If Claude Code exits at max turns, inspect landed files and complete focused missing tests locally rather than rerunning a broad prompt.
