> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Offline Recon-to-Runner Bridge Coverage

Use when a cybersecurity workspace has an existing dry-run recon policy artifact and an existing dry-run module-runner preview path, and the next step is to prove interoperability without creating runtime coupling.

## Trigger

- A T3 direction review approves a tests/fixtures/docs-only recon-to-runner bridge slice.
- The implementation must demonstrate that a `policy_boundary/1.0` allow artifact from `recon.sh --dry-run` can be consumed by `scripts/module_runner.py --mode dry-run`.
- Runtime bridge, artifact auto-copying, new CLI flags, scanner/module execution, findings/evidence flow, reports, and live/lab activation remain unauthorized.

## Safe pattern

1. Keep all writes inside a per-test `tempfile.TemporaryDirectory` HACKLAB.
2. Install committed synthetic program scope into the temp HACKLAB only; do not modify real `config/scope.txt` or real program scopes.
3. Invoke recon only as dry-run, for example:
   `recon.sh --dry-run --program sample-lab --policy-mode dry-run <synthetic-target>`
4. Locate one emitted allow `policy_boundary_*.json` under temp scan evidence.
5. Copy that artifact inside the test harness only to temp `runs/<run_id>/policy/decision.json`.
6. Invoke the existing runner preview path:
   `scripts/module_runner.py --policy-artifact <copied-path> --run-id <run_id> --target <same-target> --target-type <type> --mode dry-run --discover-root <temp-HACKLAB> --json`
7. Assert preview-only allow semantics and fail-closed negative cases.
8. Record explicitly that runtime bridge/auto-copy remains deferred.

## Recommended assertions

- Positive recon artifact -> runner `allow` verdict.
- Planned run manifest stays `run/1.0`, `status=planned`, `dry_run=true`, `target_touching=false`.
- Optional module I/O preview produces `not_executed`, `dry_run=true`, `target_touching=false`, empty findings/evidence.
- Policy artifact SHA-256 and relative path match the copied temp `runs/<run_id>/policy/decision.json`.
- Target mismatch denies.
- Artifact path outside `runs/<run_id>/policy/` denies.
- Helper non-zero return code denies.
- Boundary audit event mismatch denies.
- Planned-vs-dry-run mode mismatch denies.
- `recon.sh --help` and runner `--help` do not expose bridge-specific flags.
- Combined output has no scanner execution leakage and no module execution leakage markers.
- Real repo `config/scope.txt` is SHA fenced.
- Real repo `runs/`, `loot/`, `scans/`, `evidence/`, and `reports/` are snapshot fenced.

## Validation commands

Run focused and adjacent tests plus project review:

```bash
python -m unittest scripts.test_recon_runner_bridge_dry_run
python -m unittest scripts.test_recon_program_policy_dry_run scripts.test_module_runner
python -m unittest discover scripts
git diff --check
USER=${USER:-Owner} HACKLAB=<user-home> ./bin/hermes review
```

Also run a staged/added-line secret scan before committing because handoff run metadata and review artifacts may be created.

## Worker timeout / incomplete RED evidence caveat

If a delegated worker times out after creating tests or artifacts, do not treat its output as complete. Inspect the workspace, rerun focused and full validation directly, write a named result file that records:

- worker route/tool and visible model/runtime;
- timeout or incomplete wrapper status;
- whether RED evidence is incomplete;
- exact GREEN validation commands/results;
- forbidden files confirmed untouched;
- why the caveat is process-only rather than a runtime blocker.

For tests-only slices with no production/runtime changes, incomplete RED evidence can be accepted as a documented process caveat after Hermes direct verification. Before any future runtime bridge discussion, prefer a lightweight independent implementation/safety review.

## Pitfalls

- Do not add bridge CLI flags to recon or runner during the test-only slice.
- Do not change `recon.sh`, `module_runner.py`, policy helpers, validators, module schemas/profiles, or committed scope/config just to make the bridge test pass.
- Do not copy artifacts into real repo `runs/`; use temp HACKLAB paths only.
- Do not interpret a passing bridge test as authorization for runtime coupling, scanner execution, module execution, candidate finding emission, reporting, lab/live activation, scheduler, credentials, deployment, or production changes.
