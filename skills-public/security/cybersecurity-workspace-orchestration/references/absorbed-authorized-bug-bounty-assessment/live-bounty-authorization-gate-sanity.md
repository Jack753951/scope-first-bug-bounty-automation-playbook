> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Live Bounty Authorization-Gate Sanity Checks

Use this reference when a live bug-bounty lane has a repository-level scope/policy gate (`config/scope.txt`, `programs/<slug>/scope.json`, `recon.sh`, bundle manifests, or similar). The goal is to prove the gate is usable before any scanner-like or automated runner touches a live target.

## Trigger

Run these checks before live automation when:

- a program scope JSON was newly created or renamed;
- `config/scope.txt` was edited;
- a script/bundle will rely on a scope guard such as `safe_target`;
- program slugs, schema validation, or scope-entry formats changed;
- a lane has been manual-only so far and is about to move to tooling.

## Sanity pattern

1. Identify the exact in-scope target and one clearly out-of-scope target.
2. Run the runner in dry-run/planned mode only.
3. Verify the in-scope target reaches an explicit allow/pass decision.
4. Verify the out-of-scope target reaches an explicit deny/fail decision.
5. Verify malformed or ambiguous scope entries fail closed with a clear reason.
6. Verify bypass/override flags cannot enable live network execution accidentally.
7. Record the command, verdict, and reason in the handoff before any live automation.

## What to record

Use concise, non-secret evidence:

```text
runner:
program_slug:
global_scope_file:
program_scope_file:
in_scope_test_target:
in_scope_dry_run_verdict:
out_of_scope_test_target:
out_of_scope_dry_run_verdict:
fail_closed_cases:
compatibility_notes:
status: gate_clean | gate_fail_closed_needs_fix | blocked_do_not_automate
```

## Interpretation

- `gate_clean`: in-scope passes, out-of-scope fails, override behavior is safe. Automation may still require program permission and a narrow plan.
- `gate_fail_closed_needs_fix`: the gate denies execution before it can prove legitimate in-scope behavior. This is safer than accidental allow, but do not rely on it for live automation until fixed.
- `blocked_do_not_automate`: the gate allows ambiguous/out-of-scope behavior, ignores scope, or bypasses dry-run. Stop and fix before touching the target.

## Common durable gotchas

- Slug convention drift: directory names, JSON `slug`, CLI validation, and docs must use the same slug grammar. If the project uses underscores in `programs/<slug>/`, the runner must allow them, or the directory should be renamed consistently.
- Scope-entry grammar drift: global scope files often contain local lab entries (`localhost`, `127.0.0.1`, CIDR, wildcard domains). The validator must either accept the intended grammar or the scope file must be normalized before live use.
- Fail-closed is not enough for automation readiness. A gate that blocks everything is safe but not operational; keep live testing manual until a legitimate in-scope dry-run can pass.
- Do not encode a transient missing-binary or machine setup error as a permanent rule. Capture the verification pattern and any durable config/schema convention instead.

## Handoff note template

```text
Authorization-gate sanity check:
- In-scope dry-run: <pass/fail + reason>
- Out-of-scope dry-run: <pass/fail + reason>
- Override behavior: <dry-run only / blocked / issue>
- Current status: <gate_clean | gate_fail_closed_needs_fix | blocked_do_not_automate>
- Decision: <manual-only until fixed | automation allowed under plan>
```
