> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# External intelligence and valuable bundle retention

Session-derived update: 2026-05-22

## User correction captured

For the cybersec lab, do not retain only bundles that achieved maximum impact such as target control, file read, RCE, or privilege control. A bundle is worth keeping when it teaches a reusable modern security workflow, even if it did not fully exploit the target.

## Bundle outcome vocabulary

Use these statuses for local lab / authorized training work:

- `verified-impact`: reproduced on the authorized lab with concrete impact evidence, such as auth bypass, protected API read, bounded file read, accepted upload/state change, or runtime proof.
- `valuable-candidate`: no full exploitation yet, but the workflow is worth retaining because it captures useful tooling, payload design, false-positive handling, exploit preconditions, artifact strategy, or next-step decision logic.
- `attempted-not-verified`: tested with artifacts, but no runtime/impact proof yet.
- `blocked/deferred`: missing target component/version, matching input surface, callback lab, auth state, recovery condition, or tooling.
- `reference-only`: useful external intelligence that does not apply to the current lab target but should inform future fixtures, modules, or target selection.

Do not collapse everything that is not `verified-impact` into failure. Preserve learning value with the right status.

## External intelligence sources to include

Use modern vulnerability intelligence as an intake source for lab bundles:

- CISA KEV: known exploited vulnerabilities; best for prioritizing real-world patterns.
- NVD: CVE metadata, CWE/CVSS/descriptions, recent modified/published feeds.
- Exploit-DB / searchsploit: public exploit technique and platform/type hints; do not blindly execute PoCs.
- GitHub security tooling / PoC / vulnerable-lab repos: source of techniques, fixtures, and tool ideas; review code and provenance before use.
- HTB / PortSwigger / TryHackMe / training labs: pattern calibration and workflow practice; avoid public writeups unless explicitly in assisted mode.
- OWASP / CWE: taxonomy and defensive/reporting alignment.

## Intake workflow

1. Fetch or consult external intelligence on the Windows/Hermes control plane.
2. Extract pattern, preconditions, affected component/version, CWE/OWASP mapping, and likely proof type.
3. Decide applicability to the current lab:
   - matching product/version/component exists -> candidate for product-specific reproduction;
   - only weakness pattern matches -> pattern-inspired lab bundle;
   - no matching surface -> `reference-only` or `blocked/deferred`.
4. Any target-touching validation runs from `<lab-vm>`, not Windows.
5. Preserve safe artifacts and write the bundle with the outcome vocabulary above.

## Product-specific CVE rule

Do not claim a CVE exists on Juice Shop or another lab just because a KEV/NVD/Exploit-DB entry resembles the weakness class. Product-specific CVEs are pattern inspiration unless the target actually has the affected product/version/component and the vulnerable behavior is reproduced.

## Recommended index shape

Maintain an intelligence-to-bundle index with columns like:

- source: CISA KEV / NVD / Exploit-DB / GitHub / HTB / OWASP
- source ID or URL
- CVE/CWE/OWASP mapping
- weakness pattern
- affected component/version precondition
- local lab surface
- bundle path
- status: `verified-impact`, `valuable-candidate`, `attempted-not-verified`, `blocked/deferred`, or `reference-only`
- Kali artifact path
- missing evidence / next step
