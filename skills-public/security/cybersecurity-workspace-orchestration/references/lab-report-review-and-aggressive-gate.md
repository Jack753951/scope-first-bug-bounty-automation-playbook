> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Lab report review and isolated aggressive-gate workflow

Use this reference when a local/intentionally vulnerable lab exercise has reached candidate findings or a lab-only report, and the operator asks for third-party review, stronger evidence/report quality, or a transition toward aggressive/destructive testing.

## Report third-party review pattern

1. Keep the report explicitly `LAB ONLY` and `NOT FOR REAL BUG BOUNTY SUBMISSION` unless the target is an approved real program/client asset.
2. Route a narrow independent review to Claude/Cowork/Claude Code for report quality, evidence sufficiency, false-positive risk, impact language, remediation/retest wording, and whether any claim overstates automation output.
3. Save the review in task-specific handoff artifacts. When the worker exposes usage/model metadata, preserve the JSON result and summarize: route/tool, login/runtime route when known, model names as reported, turns/cost if present, and any limitation on verifying the exact runtime model. If only a wrapper/delegate model is visible, say the exact lower-level backend is not independently exposed rather than guessing.
4. Require the reviewer to issue an explicit verdict such as `ACCEPT`, `PASS_WITH_RECOMMENDATIONS`, `REVISE`, or `BLOCKED`, and separate blocking corrections from non-blocking future improvements.
5. Revise report language to avoid public-scope ambiguity: say `host-only lab exposure`, `local lab service`, or `unauthenticated local-lab access` rather than wording that sounds like public internet exposure. If the report uses `public`, define it narrowly as `reachable without authentication inside the host-only lab`, not internet-exposed.
6. Treat scanner output and lab artifact names as triage signals. For `/ftp/` or directory-listing style observations, record metadata first and avoid downloading/inspecting sensitive-looking files unless the operator approves a narrower manual step. Use cautious phrases such as `sensitive-looking filename metadata` and `password-manager-database-like artifacts if present and confirmed`; do not imply content leakage from filename-only evidence.
7. Retest steps that request representative artifact filenames or bodies should be conditional: `if separately authorized and still in scope`. Keep first-pass retest focused on disabling listing/access and confirming no sensitive filenames are exposed.
8. Keep hardening-only items such as missing headers in an appendix or hardening section unless there is verified exploitability and program-specific impact.
9. Add evidence integrity where useful: artifact paths, hashes, sizes, timestamps, source command, and scope/mode caveats.
10. Before accepting a lab report, run or request a lightweight secret/sensitive-token scan of the report text for private-key blocks, cloud keys, GitHub/Slack tokens, JWT-like strings, Cookie/Set-Cookie headers, password assignments, and api-key/secret/token assignments; record zero-count results or redactions in the closeout.

## Aggressive/destructive transition gate

Do not mix aggressive scripts into the standard report rehearsal. Split fuzzing, exploit PoCs, callbacks, destructive/state-changing checks, or high-availability-risk probes into a separate isolated-snapshot slice.

Before any aggressive execution:

- Confirm authorization is local lab / intentionally vulnerable app / CTF / owned asset / written client authorization / explicit bounty scope.
- Use a separate attacker VM clone where possible, not the main work VM.
- Verify victim and attacker are on host-only lab networking for attack mode; NAT/shared folders/clipboard/drag-and-drop/file-transfer convenience channels should be disabled unless the operator explicitly chooses a setup-control mode.
- Confirm clean snapshots exist for attacker and victim.
- Check disk capacity before cloning/snapshotting. If free space is too low for reliable VM clone/snapshot/recovery, mark execution `BLOCKED` rather than partially proceeding.
- Define request caps, timeouts, concurrency limits, kill switch, pre/post health checks, audit logging, and recovery steps.
- Require a fresh safety/implementation review for the first aggressive script or execution adapter.
- Keep outputs candidate-only and redact evidence before any report draft.

## Closeout wording

Status summaries should clearly distinguish:

- report status, e.g. `accepted as lab-only` versus `ready for real submission`;
- policy/plan status, e.g. `aggressive slice policy accepted`;
- execution status, e.g. `BLOCKED: disk/snapshot/clone gate not satisfied`;
- safest next action, e.g. `free disk, clone attacker VM, snapshot both VMs, then rerun preflight`.
