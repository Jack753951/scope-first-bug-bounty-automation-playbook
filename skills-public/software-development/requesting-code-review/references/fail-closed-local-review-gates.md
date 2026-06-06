> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Fail-Closed Local Review Gates

Use this pattern when a repo has a local review/check command that writes a report (for example `handoff/latest_check.md`) and the user asks whether engineering hardening is really enforced.

## Durable lesson

A review command that prints `BAD`, `FAILED`, or `ACTIVE` but exits 0 is an advisory report, not an enforcing gate. For engineering hardening, core invariant failures must set a failure accumulator and return non-zero after writing the report.

## Good pattern

1. Keep report generation intact so the operator still gets a readable artifact.
2. Add a `review_fail=0` accumulator at the start of the review function.
3. For each core invariant, set `review_fail=1` when the invariant fails:
   - invalid JSON or schema fixtures
   - Python/syntax compile failure
   - shell `bash -n` failure
   - active lock file when the gate requires quiescence
   - missing/unrunnable verifier needed by the gate
   - unparseable required worker/reviewer artifact
4. At the end, print the full report, then `return 1` if `review_fail != 0`.
5. Preserve legitimate `SKIP` semantics for routes that have not run yet. A missing optional reviewer artifact can be SKIP; a missing verifier that is required to trust present artifacts should fail.
6. If the preferred validator is unavailable, use a deterministic fallback when possible (for example `python -m json.tool` when `jq` is unavailable). Do not silently skip a core check.

## Regression test pattern

Create a fixture-based shell test that runs the real review command against temporary mini-roots:

- clean minimal root -> passes
- invalid JSON -> fails and report contains the specific bad file
- broken Python -> fails and report contains compile failure
- broken shell -> fails and report contains the bad script
- active lock -> fails and report contains lock active
- missing required verifier -> fails and report names the missing verifier

Use temporary roots outside the production repo content, but be careful not to exclude the temporary root itself with broad `find ! -path '*/tmp/*'` filters. Prefer excluding only the repo-local runtime directories, e.g. `$ROOT/tmp/*` and `$ROOT/handoff/tmp/*`, so temp fixtures under `/tmp/...` are still tested.

## Dirty-tree reporting

In large long-lived workspaces, report the slice-specific files changed and explicitly say that unrelated dirty-tree noise remains. Passing focused validation does not mean the whole repo is a clean release checkpoint.
