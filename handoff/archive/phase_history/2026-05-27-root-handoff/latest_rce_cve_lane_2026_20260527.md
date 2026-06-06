> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Latest RCE CVE lane correction — 2026-05

Date: 2026-05-27

## User correction

User challenged the lane choice: latest-vuln work should include latest remote-control / RCE CVEs, not only safer data-leak/access-control style CVEs.

## Correction accepted

The prior choice of Strapi relational filtering/data leak as the primary latest-vuln lane was too conservative for the requested "latest CVE" lane. It is useful for bounty-safe proofing, but it is not the best answer to "latest remote control / RCE CVE".

New policy for this lane:

- Keep first-bounty safety boundaries for live work.
- Search latest RCE/remote-code-execution candidates explicitly.
- Split every candidate into:
  - lab EXECUTE: owned/local proof or detector validation only;
  - live PASSIVE/BOUNDED: version, exposure, reachability, owned control only;
  - live PARK/KILL: no exploit, callback, destructive action, non-owned data, or host control.

## 2026-05 candidate ranking

### Primary detector lane: <specific-cve-id> — WordPress Avada Builder / Fusion Builder unauthenticated RCE

Why primary:

- Published 2026-05-21.
- WordPress + Avada/Fusion Builder is likely common on public web and bounty scopes.
- RCE severity is high-signal.
- Live-safe detector can be non-invasive: identify WordPress + Avada/Fusion Builder presence and affected version only.

Safe boundary:

- Live: passive fingerprint / public asset and version evidence only.
- Lab: local WordPress instance with vulnerable/fixed plugin versions to validate detector.
- Do not send exploit/AJAX/function-chain trigger requests to live targets.

Decision: EXECUTE for lab detector; PASSIVE-ONLY for live triage.

### Secondary: <specific-cve-id> / <specific-ghsa-id> — Strapi RCE condition

Why secondary:

- Published 2026-05-14.
- Strapi is relevant to web/API bounty surfaces.
- Version boundaries are clear.

Limitations:

- Requires authenticated admin / specific database or config conditions.
- Not suitable for live RCE triggering.

Decision: EXECUTE for version/exposure detector; PARK live exploit.

### Secondary: <specific-cve-id> / <specific-ghsa-id> — n8n workflow automation RCE chain

Why secondary:

- Published 2026-05-04.
- n8n appears on SaaS/automation/AI/ops surfaces.
- Version/exposure detector is safe.

Limitations:

- Requires authenticated workflow privileges and may touch secrets/workflows.

Decision: EXECUTE for version/exposure detector; PARK live exploit.

### Secondary: <specific-cve-id> — Apache OFBiz RCE

Why secondary:

- Enterprise web/ERP surface; high impact.
- Patch version is clear.

Limitations:

- Version detection may be noisy.
- OFBiz RCEs are often weaponized; live probing is high-risk.

Decision: PASSIVE detector only; PARK live exploit.

### Secondary: <specific-cve-id> — Magento 2 Mirasvit Full Page Cache Warmer RCE

Why secondary:

- Magento/Adobe Commerce is common in bounty/ecommerce scopes.
- Plugin-specific unauthenticated RCE is high signal.

Limitations:

- Plugin-specific and passive detection may need multiple weak signals.
- PHP object injection/gadget-chain style proof is not acceptable on live targets.

Decision: EXECUTE lab detector; PASSIVE-ONLY live triage.

## KILL/PARK classes

KILL/PARK for first-bounty live work:

- Supply-chain malware packages.
- Cloud/host/admin platform RCE that directly controls Docker/K8s/DB/host.
- Enterprise appliance/browser/storage/DNS RCE requiring special deployment.
- Workflow/AI automation RCE where proof may touch secrets/API keys/workflows.
- Client-side/Electron/TUI compromise requiring social engineering or local-user action.
- Library sandbox escapes unless target reachability can be proven without executing code.
- Callback/OAST/remote-loader RCE unless the program explicitly authorizes it.

## Current decision

Replace the latest-vuln lane from Strapi data leak to:

Primary: <specific-cve-id> Avada Builder passive/lab detector.

Keep Strapi/n8n/OFBiz/Magento as secondary 2026-05 RCE detector candidates.

Next action:

Build a script-first detector harness that only performs passive/version/exposure checks and a local lab validation path. Do not run live exploit attempts.
