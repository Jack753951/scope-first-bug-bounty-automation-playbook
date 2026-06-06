> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Latest-Vulnerability Lane Freshness Pattern

Use this reference when running a parallel latest-vulnerability lab/detector lane alongside the live first-bounty funnel.

## Lesson

A well-known older vuln can be a good detector reference, regression target, or fallback, but it should not silently become the active `latest vulnerability` lane when the user's stated strategy is freshness-first.

For a freshness lane, default to vulnerabilities/advisories from the current year and preferably the last 1-2 months. If a candidate is older but still useful, label it explicitly as `reference_only` or `fallback`, not as the primary lane.

## Selection Rules

1. Define freshness before candidate selection:
   - preferred: current year, last 1-2 months;
   - acceptable: current year with strong active exploitation or unusually broad bounty surface;
   - fallback/reference: older than the freshness window.
2. Query current advisory sources before committing:
   - GitHub Security Advisories;
   - vendor advisories;
   - NVD/CVE where useful;
   - project release/security notes.
3. Score candidates for bounty transfer, not just technical severity:
   - common SaaS/web/API deployment in bounty scopes;
   - local synthetic proof possible;
   - passive fingerprint or owned-control live transfer possible;
   - no need for destructive RCE/file-read/customer-data proof;
   - clear affected/fixed version boundary.
4. Keep older high-quality detectors as `reference/fallback` artifacts if they are reusable, but do not let them consume the active freshness lane.

## Output Shape

Record the latest-vuln lane like this:

```text
Lane: latest-vuln
Freshness window: <current-year / last 1-2 months / explicit exception>
Primary candidate: <CVE/advisory>
Why current: <dates/advisory source>
Why bounty-relevant: <scope prevalence + safe proof route>
Local proof: <synthetic target/control>
Live transfer: <passive or owned-control only>
Reference/fallback detectors: <older candidates, if any>
Decision: EXECUTE / PARK / KILL
```

## Pitfall

Do not present a 2025-era detector as the active 2026/latest-vuln lane just because it is technically solid. Promote it only as a reusable detector/reference unless the user explicitly changes the lane from `latest` to `best available detector`.
