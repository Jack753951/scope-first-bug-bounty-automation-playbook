> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Phase 4B Lab Fast Lane + GET-only Adapter Pattern

Use when the operator has an intentionally vulnerable, host-only lab target and explicitly wants the lab used for calibration instead of offline-only planning.

## Trigger

- Target is a local/intentionally vulnerable app, e.g. Juice Shop on a host-only VM.
- Operator says the target VM exists for testing and the current safety gates feel too heavy.
- Work is Tier 1/Tier 2 metadata or benign-parameter probing, not exploitation, credential flows, callbacks, brute force, or destructive testing.

## Workflow correction

Do not keep applying full real bug-bounty / public-target review overhead to every host-only lab check. Establish a "lab fast lane" once the lab boundary is verified, then run bounded low-risk probes actively and review the output afterward.

Still preserve hard stops:

- no public or real bug-bounty target
- no credentials, brute force, callbacks/OAST, pivoting, DoS, destructive action, or loot collection
- no broad scanner/crawler by default
- no automatic confirmed/verified/reportable finding promotion

## Lab fast-lane controls

For Tier 1/Tier 2 local-lab checks, require:

- fixed private/local target URL and VM identity
- fixed request/path list
- small request cap (for example 40-100)
- timeout cap (for example <=5s unless a specific verifier justifies more)
- pre/post health checks
- redacted JSONL observation output
- temporary raw body handling only; keep hashes/snippets/headers, not bulk loot
- candidate-only wording and manual-verification-required flags
- artifact manifest and handoff result

## Adapter productization pattern

After a successful manual/orchestrated run, turn it into a reusable adapter rather than leaving it as a one-off script:

1. Write tests first for boundary behavior:
   - rejects public targets
   - rejects unsafe request caps/timeouts/rates
   - requires explicit lab approval before writing an executable script
   - generated script contains no scanner/crawler/promotion vocabulary
   - plan includes health gates and only GET/fixed paths for GET-only adapters
2. Implement a module under `scripts/lab_modules/` with a stable CLI.
3. Generate a remote bash script for Kali execution when needed.
4. Execute through the existing bridge, pull artifacts, and read back `health.txt`, `summary.txt`, and `observations.jsonl`.
5. Record result in `handoff/`, append `accepted_changes.md`, and mirror the key result into Obsidian/project index if the project uses it.

## GET-only metadata adapter shape

A good first fast-lane adapter uses only fixed GET requests such as:

- `/`
- `/robots.txt`
- `/.well-known/security.txt`
- `/ftp/`
- `/api-docs/`
- benign search/API canary
- redirect canary with no redirect following

Do not use HEAD automatically if the target/app has shown HEAD timeout or ambiguity. GET-only with max body size, hashing, short redacted snippets, and post-run cleanup may be more reliable.

## Wave2 benign-parameter adapter shape

After the GET-only metadata adapter is stable, convert old open-redirect/reflection helper scripts into a separate benign-parameter adapter instead of running the original scripts directly.

Recommended constraints:

- fixed local/private target only
- GET-only fixed URLs
- inert text canary only, e.g. `PHASE4B_REFLECT_CANARY`
- inert redirect canaries only, e.g. `https://phase4b-canary.invalid/`
- no redirect following (`--max-redirs 0`)
- no JavaScript/XSS payloads, `gau`, `kxss`, `dalfox`, `sqlmap`, crawler, scanner, callback/OAST, brute force, credential flow, or finding promotion
- JSONL candidate-only output with pre/post health and temporary raw bodies only
- executable script generation requires explicit lab approval

TDD should prove the adapter rejects public targets/unsafe limits, requires lab approval before script writing, includes health gates, and contains no scanner/payload/promotion terms.

## Interpretation notes

- `/ftp/` directory-listing metadata is a good lab finding-rehearsal candidate, but still needs bounded filename/content-class verification before confirmed wording.
- `/api-docs/` / Swagger UI is attack-surface metadata unless impact is demonstrated.
- SPA fallback pages are false-positive traps: `200 text/html` with the app title does not prove reflection, file exposure, or route existence.
- For reflection checks, count only inert canary presence in the intended response body for the reflection module. If a redirect endpoint echoes the canary in an error body/title, record it separately as `canary_echoed_in_error_body`; do not treat it as XSS/reflection or open-redirect evidence.
- Redirect canaries that return 406/no `Location` are useful negative controls. No `Location` header means no redirect candidate for that canary.

## Windows/Git-Bash remote path pitfall

When generating a remote Kali script from Git-Bash/MSYS on Windows, Unix paths such as `/home/kali/...` can be rewritten to `C:/Program Files/Git/home/kali/...`. Use an MSYS path-conversion exclusion (for example `MSYS2_ARG_CONV_EXCL='*'`) or construct/write the remote path in a way that avoids MSYS rewriting. Verify the generated script's first lines before copying it to Kali.
