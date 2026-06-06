> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Public-clean methodology repo publish pattern

Use this when a private workspace contains sensitive operational state, but the user asks to make a public GitHub repo from it.

## Durable lesson

Do not treat "copy the project and sanitize it" as a recursive copy task when the source is a cybersec, client, auth, or operations workspace. First perform a sensitivity inventory, then publish a hand-rewritten methodology layer that preserves the reusable workflow shape while dropping private nouns, raw handoff, program state, scope, evidence, logs, screenshots, account details, and target-specific history.

## Recommended sequence

1. Read the project authority layers and external memory/index layers relevant to publication.
   - Project safety/index/current-navigation files.
   - Active lane/queue state only to understand what must not be copied.
   - Existing `public_exports/` or public-clean staging docs if present.
   - External project notes/vault index when the user explicitly asks to include outside memory.
2. Run a text inventory over the private repo and external notes to quantify risk before copying.
   - Count text files read and bytes processed for the final report.
   - Search for private paths, VM names, private IPs, target/program names, platform aliases, secrets/token words, advisory IDs, and evidence/output paths.
   - Treat many hits as a signal to rewrite from scratch, not to weaken the scan.
3. Build a separate public-clean repository outside the private source tree.
   - Do not recursively copy raw `handoff/`, `programs/`, `config/`, `archive/`, screenshots, scans, loot, logs, browser state, or vault config.
   - Prefer class-level docs: safety contract, agent operating model, memory/handoff governance, local-lab proof library, live-target dry-run template, evidence redaction/report-readiness, recon/intel cadence, public-export safety.
   - Include reusable templates and a fail-closed safety scanner.
4. Scan locally before commit.
   - Run the repo's own scanner.
   - Also run an independent grep/search for private paths, old workspace names, private IPs, target names, H1 aliases, platform names, CVE/GHSA IDs, and token-like patterns.
   - Any hit outside the scanner's own regex definitions should be rewritten or allowlisted only with a clear reason.
5. Commit and publish with `gh repo create --public --source . --remote origin --push`.
   - If git identity is missing, set repo-local `user.name` from `gh api user --jq .login` and noreply email from user id/login; do not make a global config change unless asked.
6. Verify after publish.
   - `gh repo view OWNER/REPO --json nameWithOwner,isPrivate,visibility,url,defaultBranchRef,pushedAt` must show `isPrivate:false` and `visibility:PUBLIC`.
   - Fresh-clone the public repo into a temp directory and rerun the public safety scan.
   - Check the GitHub Actions run if a scan workflow was added.

## Report shape

In the final reply, include:

- public repo URL;
- local public-clean path;
- files/categories created;
- exact verification results: scan pass, public visibility, fresh-clone scan pass, workflow status if available;
- explicit note that raw private project files were not copied because sensitivity inventory showed private operational content.

## Pitfalls

- A source repo may already have a `public_exports/` folder; use it as guidance, but still create a fresh public-clean target and rescan.
- The public scanner can contain sensitive regex strings such as `CVE-20` or token patterns; independent search hits inside the scanner itself are acceptable if documented.
- GitHub CLI auth output masks tokens but can still contain token prefixes; do not copy it into public files.
- Publishing methodology is not the same as publishing evidence or findings. Keep live-target authorization and final submission gates explicit.
