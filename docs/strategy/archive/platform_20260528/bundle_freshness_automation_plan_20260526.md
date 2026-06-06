> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Bundle Freshness Automation Plan — 2026-05-26

Status: proposed / no target touched
Boundary: metadata-only automation unless a later operator-approved plan explicitly authorizes local lab bootstrap or live target-touching work.

## Finding

The current bundle library is not automatically tracking the newest vulnerabilities end-to-end.

Evidence checked on 2026-05-26:

- `handoff/bundle_inventory_20260522.md` lists 42 bundle docs as of 2026-05-22: 16 verified/proved, 17 draft-active triage, 4 active/learning, 5 candidate/backlog.
- Filesystem now has 47 bundle docs under `modules/bundles/*.md` excluding README.
- A quick CVE/GHSA reference scan across bundle docs found 0 direct `CVE-*` / `GHSA-*` references.
- Bundle timestamps cluster around 2026-05-21 to 2026-05-23; latest parsed bundle timestamp observed: `20260523T124050Z`.
- `tools/vuln_intel_refresh.py` exists and can intake CISA KEV, NVD recent, and GitHub Advisories into `handoff/vuln_intel/`, but the latest stored run found was `vuln_intel_candidates_20260523T130000Z`.
- `cve_watch.py` exists for a narrower web infra watchlist: nginx, apache, tomcat, openssl, haproxy, envoy, traefik.
- `DAILY_SOP.md` references a scheduled `daily-cve-bugbounty-brief`, but `hermes cronjob list` did not show that job currently active. Current active cybersec scheduled job is the every-2-days third-party strategy review.
- `recon_pipeline.py --chain` only wires to `nginx_rift_scanner.py`; it is not a general CVE-to-bundle executor.

## Desired automation loop

Do not auto-create exploit bundles directly from news. Use a staged, fail-closed freshness loop:

1. Intake
   - Sources: CISA KEV, NVD recent published+modified, GitHub Security Advisories, vendor advisories, high-signal RSS/blog feeds, Exploit-DB metadata, nuclei template metadata if installed.
   - Output: normalized JSONL candidates under `handoff/vuln_intel/`.
   - No target touching.

2. Normalize and classify
   - Extract: CVE/GHSA, product, version range, vulnerability class, CWE, pre-auth/auth required, default-config likelihood, exploit maturity, patch/advisory references, safe proof posture.
   - Route to one of:
     - `covered_by_existing_bundle`
     - `needs_bundle_update`
     - `new_local_bootstrap_candidate`
     - `needs_authorized_live_target`
     - `reference_only`
     - `reject_low_signal`

3. Coverage diff
   - Build an index from `modules/bundles/*.md` containing capability class, proof preconditions, safe proof markers, target type, maturity, references, last verified date.
   - Compare candidate classes/products against bundle coverage.
   - Emit `handoff/bundle_freshness_delta_<stamp>.md` with top gaps and recommended next one bundle only.

4. Human/agent review gate
   - For each high-priority gap, require a mini review packet:
     - Is it legally safe?
     - Can it be reproduced locally without target touching?
     - Is it better represented as a generic class bundle, product-specific version detector, or reference-only note?
     - What is the minimal non-destructive proof?

5. Bundle update generation
   - Only after review, create or patch one of:
     - `modules/bundles/valuable_candidate_<class>_<product>.md`
     - `modules/bundles/verified_lab_flow_<target>_<class>.md`
     - `handoff/vuln_intel/reference_only_<cve>.md`
   - New bundle must include source links, safe proof boundary, target prerequisites, forbidden actions, and verification status.

6. Validation
   - Run metadata lint.
   - Run local-only tests if scripts changed.
   - Run `hermes review` if project scripts/scope gates changed.

7. Schedule
   - Daily brief: narrow high-yield infra CVE watchlist.
   - 2–3x/week bundle freshness diff: broader CISA/NVD/GHSA/vendor/RSS coverage.
   - Weekly consolidation: choose one local/bootstrap or live-scope candidate, not ten.

## Immediate engineering gaps

1. `vuln_intel_to_bundle_index.py`
   - Reads `handoff/vuln_intel/*.json` + `modules/bundles/*.md`.
   - Emits coverage/delta markdown and JSON.

2. Bundle metadata convention
   - Add optional fields to bundle docs:
     - `vuln_classes:`
     - `cwe:`
     - `cve_refs:`
     - `product_refs:`
     - `last_verified:`
     - `safe_proof_posture:`
     - `live_target_policy:`

3. Scheduled job
   - A Hermes cron job should run the intake + coverage diff and deliver only the delta, not raw feeds.
   - It should not run scanners, PoCs, recon, noVNC, or signup flows.

## Safety stance

Automatic freshness is allowed for metadata, classification, coverage diff, and draft planning.
Automatic live exploitation, scanner/fuzzer/DAST execution, credential handling, report submission, or scope expansion remains blocked by the project security gate.
