> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Unverified Current-Intel Quarantine Routing

Use this pattern when a project generates a current-facts brief from degraded sources, fallback web search, partial automation, or sources that were not verified against primary references.

## Trigger

- A CVE/advisory/threat-intel/current-facts brief exists but primary-source verification is incomplete.
- A generated artifact contains action-oriented wording that could be mistaken for an approved operational step.
- The content is useful as a lead, but not safe to treat as authoritative project truth.

## Routing

1. Do not promote the brief into global Hermes memory.
2. Do not place it in the main accepted project evidence/report path.
3. Move it into a repo-local quarantine or unverified area, for example:
   - `cves/unverified/<date>_<topic>_unverified.md`
   - `cves/unverified/<date>_<topic>_unverified.json`
4. Add a visible warning at the top that the artifact is unverified and must not be executed or reported from directly.
5. Downgrade action language:
   - Prefer `Unverified follow-up (do not execute from this draft)` over `First action` or similar operational wording.
6. Record a short accepted-change / handoff note that the artifact was quarantined and why.
7. Keep exact claims, source snippets, URLs, run artifacts, and dates in repo-local files only.
8. If a reusable lesson exists, capture the routing pattern in this skill rather than copying the brief contents into memory.

## Verification

- The original loose/root artifact is removed or replaced by a pointer to the quarantined copy.
- The quarantined artifact is clearly labeled unverified.
- No credential, target, loot, or client-sensitive material is copied into global memory or skill text.
- Any later use starts with fresh primary-source verification before report drafting, scanner decisions, exploit testing, or client communication.
