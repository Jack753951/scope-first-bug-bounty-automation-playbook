> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Program Policy Artifact Validation Hardening

Use this reference when runtime recon/execution code consumes an offline policy decision helper or boundary-wrapper artifact.

## Durable lesson

Do not treat `status=allow` on stdout plus an existing artifact file as sufficient authorization. The runtime must validate that the artifact is the exact, fresh decision for the current request, that the artifact itself is inside the trusted artifact directory, and that the boundary output/artifact provenance matches the current policy source files. A forged artifact that merely mirrors the requested target/stage/technique/mode can still replay an allow unless decision provenance and source hashes are cross-checked.

## Required checks before consuming an allow artifact

1. Resolve the artifact path strictly (`resolve(strict=True)` or equivalent).
2. Resolve the configured artifact directory and require the artifact path to be within it.
3. Reject symlink/path traversal escapes and artifacts from stale/alternate directories.
4. Validate a versioned schema marker, e.g. `schema_version == policy_boundary/1.0`.
5. Require `boundary.status == allow` (or the boundary-layer equivalent), not only top-level/stdout allow text.
6. Require a canonical allow boundary event such as `boundary.audit_event == PROGRAM_POLICY_ALLOW`, and cross-check it against the flat boundary-wrapper output.
7. Require the flat boundary output to include canonical provenance fields and validate both shape and truth:
   - `POLICY_BOUNDARY_AUDIT_EVENT == PROGRAM_POLICY_ALLOW`
   - `POLICY_BOUNDARY_PROGRAM_HASH` is canonical lowercase SHA-256 and equals the current `PROGRAM_SCOPE_FILE` hash.
   - `POLICY_BOUNDARY_GLOBAL_HASH` is canonical lowercase SHA-256 and equals the current global scope file hash.
   - `POLICY_BOUNDARY_DECIDED_AT_UTC` has a UTC timestamp shape and matches the artifact decision timestamp.
8. Cross-check request identity fields against the current invocation:
   - `request.target`
   - `request.stage`
   - `request.technique`
   - `request.mode`
   - program/global scope identifiers when available
9. Require an embedded `decision` object and cross-check it against both the current request and the boundary-wrapper output:
   - `decision.verdict == allow`
   - `decision.target`, `decision.technique`, and `decision.mode` match the current invocation.
   - `decision.audit_event`, `decision.program_file_sha256`, `decision.global_scope_sha256`, and `decision.decided_at_utc` match the boundary output.
10. Fail closed on parse, path, schema, status, request mismatch, provenance mismatch, or source-hash mismatch with a distinct audit/error code such as `PROGRAM_POLICY_BOUNDARY_ERROR` / `ARTIFACT_VALIDATION_FAILED`.
11. Keep scanner/probe/fuzzer/nuclei stages from seeing candidate targets when validation fails.

## Timeout parsing for security-sensitive boundary helpers

When a shell wrapper accepts a timeout env var such as `PROGRAM_POLICY_TIMEOUT_SECS`, avoid permissive arithmetic parsing:

- Accept only canonical decimal integer strings with no leading zero padding except the single digit `0` if explicitly allowed.
- For an allowed range like `1..60`, reject `0`, `61`, `099`, `000`, huge integers, negatives, whitespace, and non-integers before arithmetic.
- In bash, combine a regex gate with explicit base-10 parsing (`10#$raw`) only after the regex proves the value is safe/canonical.

Example pattern:

```bash
raw_timeout=${PROGRAM_POLICY_TIMEOUT_SECS:-10}
if [[ ! "$raw_timeout" =~ ^[1-9][0-9]*$ ]]; then
  fail_closed "invalid timeout"
fi
parsed_timeout=$((10#$raw_timeout))
if (( parsed_timeout < 1 || parsed_timeout > 60 )); then
  fail_closed "invalid timeout"
fi
```

## Regression tests to include

- Artifact path outside the configured artifact directory is rejected.
- Symlink/path traversal artifact escapes are rejected.
- Artifact `request.target` mismatch is rejected.
- Artifact `request.stage` mismatch is rejected.
- Artifact `request.technique` mismatch is rejected.
- Artifact `request.mode` mismatch is rejected.
- Missing/unknown `schema_version` or non-allow boundary status is rejected.
- Missing embedded `decision` object is rejected.
- `decision.target` / `decision.technique` / `decision.mode` mismatches are rejected.
- `boundary.audit_event` mismatch is rejected.
- Boundary output source hashes that do not match the current program/global scope files are rejected.
- Artifact `decision.*` provenance (`audit_event`, program/global hashes, decided timestamp) mismatching the boundary output is rejected.
- Timeout rejects `0`, `61`, `099`, `000`, giant integers, and non-integers.
- A rejection proves fail-closed behavior before any target-touching stage executes.

## Review expectation

Independent review should look specifically for shell numeric parsing pitfalls, stale artifact replay, alternate artifact directories, symlink escapes, request mismatch replay, forged/missing decision objects, boundary output that is internally consistent but not tied to the current source files, and whether error codes/audit logs make failures diagnosable without leaking secrets.
