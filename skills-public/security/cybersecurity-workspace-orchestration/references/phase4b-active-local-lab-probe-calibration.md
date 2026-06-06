> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Active Local-Lab Probe Calibration

Use this when the operator has an intentionally vulnerable local lab / host-only victim VM and explicitly asks to make more use of the target rather than staying in offline planning.

## Core lesson

Do not over-correct toward docs-only/offline work once a local lab has been built and authorized. The lab exists to calibrate the automation pipeline. After the user approves target-touching local-lab work, actively use the victim within bounded controls and turn the results into reusable module/adapter capability.

Interpret requests like "use the target machine" or "test it" as approval for bounded local-lab interaction only when the target is already documented as local/intentionally vulnerable and in scope. This is not approval for public targets, bug bounty programs, brute force, callbacks/OAST, exploit chains, persistence, stealth, loot, or destructive testing.

## Safe execution pattern

1. Restate the target boundary briefly:
   - target URL/IP and VM names;
   - local lab / intentionally vulnerable app;
   - no public/client/bug-bounty target.
2. Run through the configured Kali bridge rather than testing from the Windows control plane when the project has a red-team Kali VM.
3. Use a fixed request list, not crawling or URL collection.
4. Include pre-health and post-health checks.
5. Set request cap, timeout, and redirect-follow behavior explicitly.
6. Emit JSONL observation records with:
   - schema/version;
   - target URL;
   - method/path;
   - status/content-type/content-length/hash;
   - short redacted snippets only when needed;
   - `candidate_only=true`, `manual_verification_required=true`, `promotes_finding=false`.
7. Pull artifacts back into the repo-local output directory.
8. Write a handoff result with:
   - route/tool;
   - visible runtime/model if relevant;
   - run id;
   - local/remote artifact paths;
   - pre/post health;
   - observed candidates;
   - false-positive notes;
   - next adapter/module step.
9. Update active strategy / accepted changes / Obsidian project index if the result changes the next lane.

## Good first probe shape

For Juice Shop-style web labs, a useful first active calibration can remain non-destructive:

- `GET /` baseline;
- `GET /robots.txt`;
- `GET /.well-known/security.txt`;
- `GET /ftp/` for directory-listing/content-class calibration;
- `GET /api-docs/` for API-docs metadata;
- one benign API search canary;
- one SPA route canary to demonstrate fallback false positives;
- one open-redirect negative-control canary with redirects disabled.

Prefer GET-only bounded probes with body-size controls for reusable adapters. HEAD against Express/SPA apps may produce timeout/HTTP-method artifacts; treat those as harness behavior, not findings.

## Output-side review cues

- `200 text/html` with the normal app title often indicates SPA fallback, not a discovered resource or reflected XSS.
- A negative redirect canary returning a rejection status with no `Location` header is useful evidence that the adapter can record `no_candidate` safely.
- A directory listing or API docs route in a local lab is a candidate/report-flow calibration artifact, not an automatically confirmed bug bounty finding.
- Any timeout suffix or partial transfer should be recorded as harness behavior and should drive adapter hardening, not vulnerability promotion.

## Next productization step

After a successful Hermes-orchestrated lab probe, convert it into a reusable bounded adapter/run-card:

- fixed local/private target allowlist;
- GET-only by default;
- request cap and timeout;
- pre/post health;
- JSONL output;
- redaction and short snippets;
- candidate-only vocabulary;
- tests for no public-target flags, no crawler, no subprocess scanner, no callback/OAST, no finding promotion.
