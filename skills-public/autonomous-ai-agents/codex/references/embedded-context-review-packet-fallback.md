> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Embedded Context Review Packet Fallback

Use this reference when delegating read-only direction/review work to Codex and the reviewer must attest to a fixed context set.

## Pattern

If direct repository reads are unavailable or the worker cannot honestly attest to reading required files, do not accept a provisional review as complete. Build a compact embedded context packet and retry the review with instructions to rely on that packet instead of local tools.

The key lesson is the retry pattern, not the setup-specific error.

## Steps

1. Write a review packet that lists:
   - review goal;
   - safety boundary;
   - required context files;
   - expected response shape;
   - explicit no-edit/no-target-contact instruction.
2. Run Codex in read-only or otherwise safe mode.
3. If Codex reports it cannot read required files, preserve that receipt as a failed/provisional attempt.
4. Build an embedded packet:

```text
# Original Review Packet
...

# Embedded Context Bundle
For each required file:
## FILE: <path>
<contents or MISSING marker>
```

5. Retry Codex using stdin with the embedded packet and require the attestation to say “embedded context supplied by Hermes” rather than pretending local reads occurred.
6. Save:
   - final review;
   - event/stdout log;
   - embedded packet path if it contains no secrets;
   - synthesis artifact if multiple reviewers were used.
7. Hermes remains verifier and should summarize any limitation in the final response.

## Guardrails

- Do not embed secrets, tokens, OTPs, cookies, private scope details that should not persist, or raw target-sensitive evidence.
- Do not convert a setup/tool read failure into a durable claim that Codex cannot read files. Treat it as an execution-state problem and use the embedded packet as a controlled fallback.
- Do not accept a review that required context reads but lacks an honest attestation.
