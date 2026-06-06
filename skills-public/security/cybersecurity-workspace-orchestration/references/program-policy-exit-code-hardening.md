> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Program-policy exit-code hardening reference

Use this when working in the cybersec lab on `recon.sh`, program-scope gates, policy-boundary wrappers, or dry-run regression tests.

## Durable lesson

Program-policy boundary/config errors must not look like successful no-work dry runs. Keep ordinary deny/no-work semantics separate from malformed or invalid policy/config semantics.

Recommended convention from the P3.8 hardening slice:

- exit `0`: valid allow dry-run, and valid policy deny/no-work outcomes such as an authorized host that is outside the selected program scope;
- exit `3`: program-policy boundary/config error class, including malformed program scope surfaced through `VALIDATOR_DENY`, policy artifact validation failures, invalid policy timeout, missing boundary helpers, or policy Python selection failures;
- exit `1`: generic pipeline/runtime failure that is not specifically a policy-boundary/config error.

## Implementation pattern

1. Do a direction/review pass first if changing runtime semantics under the security gate.
2. Keep helper contracts stable unless the direction review explicitly authorizes helper/schema changes.
3. Add a narrow boundary-error counter in the caller/runtime wrapper, not a broad scanner or runner integration.
4. Classify boundary errors by both status and reason codes, because existing wrappers may surface malformed policy as `verdict=deny` with codes such as `VALIDATOR_DENY` rather than `status=error`.
5. Preserve valid deny/no-work exit `0`; this prevents CI from treating expected policy denials as tool failures.
6. Give policy-boundary/config errors an explicit non-zero exit, so CI/preflight/operator automation can distinguish malformed setup from a clean no-work dry run.
7. Run both focused tests and adjacent suites. Updating only the new test can miss older tests that intentionally asserted exit `0` for fail-closed boundary errors.

## Regression tests to include

- malformed program scope returns exit `3` and does not leak policy PASS or scanner dry-run markers;
- valid out-of-program-scope policy deny returns exit `0` and includes a non-error deny code such as `NOT_IN_PROGRAM_SCOPE`;
- policy artifact validation failures return exit `3`;
- invalid program policy timeout returns exit `3`;
- allow-path dry-run remains exit `0`;
- no scanner/module execution markers appear in deny/error paths.

## Verification pattern

Run at least:

```bash
python -m unittest scripts/test_recon_program_cli.py scripts/test_recon_program_policy_dry_run.py
python -m unittest discover -s scripts -p 'test_*.py'
git diff --check
HACKLAB=<user-home> ./bin/hermes review
```

Treat CRLF warnings as non-blocking only if `git diff --check` exits successfully.

## Safety boundaries

Do not smuggle in scanner/module execution, callbacks/OAST, fuzzing, brute force, exploit attempts, scope-file edits, program-scope fixture edits, report submission, credentials/OAuth, scheduler/deployment/billing/production changes, or module-runner coupling while performing exit-code hardening.
