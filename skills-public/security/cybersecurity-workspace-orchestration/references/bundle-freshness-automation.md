> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Bundle freshness automation for cybersec workspaces

Use this reference when the user asks whether a proof/bundle library is keeping up with current CVEs/GHSAs/vendor advisories, or when a no-finding live-bounty session suggests the learning loop is not improving target/lane selection.

## Durable lesson

A proof-library can be strong at class-level capability coverage while still failing to track current vulnerabilities. Treat these as separate health checks:

- **Class-level coverage:** reusable proof patterns for SQLi, IDOR/BOLA, SSRF, XXE, XSS, path traversal, upload, deserialization, command injection, auth/session boundaries, etc.
- **Freshness coverage:** current CVE/GHSA/vendor advisories are normalized, mapped to bundle classes/products, diffed against existing bundles, and routed to update/bootstrap/reference-only decisions.

Do not assume latest-vulnerability coverage just because many local bundles exist. Verify by checking bundle metadata/references and the latest vulnerability-intelligence artifacts.

## Recommended metadata-only loop

Keep the automation fail-closed and non-target-touching until a separate scope/authorization plan exists:

1. **Intake**
   - Sources: CISA KEV, NVD recent published+modified, GitHub Security Advisories, vendor advisories, high-signal RSS/blog feeds, Exploit-DB metadata, nuclei template metadata if locally available.
   - Output normalized JSON/JSONL under the repo handoff/vuln-intel area.
   - No recon, scanning, PoC, login, signup, noVNC, or target traffic.

2. **Normalize/classify**
   - Extract IDs, product, affected version range, CWE/class, pre-auth vs auth-required, default-config likelihood, exploit maturity, patch/advisory references, and safe proof posture.
   - Route each item to one of:
     - `covered_by_existing_bundle`
     - `needs_bundle_update`
     - `new_local_bootstrap_candidate`
     - `needs_authorized_live_target`
     - `reference_only`
     - `reject_low_signal`

3. **Coverage diff**
   - Build an index from `modules/bundles/*.md`: capability class, proof preconditions, safe proof markers, target/component type, maturity, references, last verified date.
   - Compare candidates against bundle coverage.
   - Emit a compact `bundle_freshness_delta_<stamp>.md` plus machine-readable JSON.

4. **Review gate**
   - For each high-priority gap, decide whether it should become a generic class bundle, product-specific passive detector, local lab/bootstrap task, live-scope candidate, or reference-only note.
   - Pick one highest-value gap at a time; do not fan out into many half-built bundles.

5. **Bundle update**
   - Create/patch bundle docs only after review.
   - Include source links, safe proof boundary, target prerequisites, forbidden actions, verification status, and whether live scope/operator controls are required.

6. **Validation and schedule**
   - Run metadata lint/tests when scripts or schemas change.
   - Suggested cadence: daily narrow CVE brief for high-yield infra, 2–3x/week broader freshness diff, weekly one-gap consolidation.

## Suggested bundle metadata fields

Use machine-readable frontmatter or consistently formatted fields when possible:

```yaml
vuln_classes:
  - ssrf
  - path-traversal
cwe:
  - CWE-918
cve_refs: []
ghsa_refs: []
product_refs:
  - nginx
  - tomcat
last_verified: YYYY-MM-DD
safe_proof_posture: marker-only
live_target_policy: requires-explicit-scope
maturity: verified-lab-flow
```

## Maturity levels

- `L0 reference_only`: intelligence only; not actionable as a bundle.
- `L1 mapped_to_existing_class`: maps to an existing generic proof class.
- `L2 local_bootstrap_candidate`: can likely be reproduced in disposable local lab.
- `L3 verified_lab_bundle`: local proof verified and reusable.
- `L4 live_candidate`: requires authorized live target, A/B controls, exact scope/rules.
- `L5 report_ready`: evidence, impact, scope, remediation, and retest path are ready for human submission.

## Safety boundary

Allowed automatically: metadata intake, classification, coverage diff, draft bundle proposal, and local-bootstrap planning.

Blocked without separate approval/scope package: live target scans, PoCs, recon, fuzzing/DAST, credential handling, account creation, report submission, or automatic expansion of `config/scope.txt`.
