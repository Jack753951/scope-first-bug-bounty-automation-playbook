> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Phase 4A Juice Shop End-to-End Bug-Bounty Flow

Session pattern: local authorized OWASP Juice Shop lab used to exercise a complete but bounded bug-bounty-style workflow.

## Trigger

Use this reference when the user asks to test the full bug-bounty workflow on a local/intentionally vulnerable lab, especially after baseline recon has already proven reachability.

## Safety boundary

- Scope must be local lab / intentionally vulnerable app / CTF / written authorization.
- Keep all outputs `candidate` or lower until human verification.
- Do not run brute force, heavy fuzzing, sqlmap dumps, external callbacks/OAST, recursive downloads, credential theft, or exploit chaining by default.
- For Juice Shop `/ftp/`, do metadata-only enumeration first: status, headers, title/classification, filename/size metadata if visible. Do not recursively download files or inspect likely sensitive loot.

## Proven sequence

1. Confirm lab scope and VM isolation.
2. Baseline recon from the red-team Kali:
   - `curl -I http://<victim-hostonly-ip>:3000`
   - `whatweb http://<victim-hostonly-ip>:3000`
   - `nmap -sV -Pn -p 3000 <victim-hostonly-ip>`
3. Model review of baseline results:
   - classify scanner noise vs useful leads;
   - choose bounded next scripts;
   - explicitly reject aggressive next steps unless separately authorized.
4. Controlled active scripts:
   - security header audit;
   - CORS audit with crafted Origin but no credential abuse;
   - bounded Nikto baseline with runtime/timeout limits.
5. Second model review:
   - likely false positives;
   - candidate findings;
   - next low-risk verifier only.
6. Low-risk verification:
   - distinguish real route/content from SPA fallback;
   - verify suspicious file paths with status/content-type/title/body-class, not exploitation.
7. Candidate workflow:
   - write candidate-only packet;
   - run candidate gap report;
   - run candidate verification plan;
   - run report-readiness gate.
8. Draft a lab-only pentest report after gates run.

## Juice Shop observations from the calibration

- `/ftp/` returned a real directory listing and `robots.txt` disallowed `/ftp`; this is the best lab candidate but still needs manual review.
- Missing security headers are usually informational unless chained to concrete impact.
- `Access-Control-Allow-Origin: *` without credentialed readable cross-origin behavior is informational.
- Nikto may report `.htpasswd`, shell-history files, JSP CVEs, or JSON paths that are actually Juice Shop SPA fallback HTML. Verify content class before treating them as candidates.

## Flow implementation lesson

The workspace already had architectural support for post-scan agent review and report gates, but the end-to-end run was still Hermes-orchestrated rather than one-command productized. When this pattern recurs, record that distinction clearly:

- documented and partly implemented: post-scan review workflow, candidate packet/gap/verification/report gate consumers;
- manually validated: recon -> model review -> script selection -> active scripts -> model review -> candidate packet -> report gate -> report draft;
- missing platform slice: a reusable runner that persists run manifests, model-review artifacts, selected-script plans, candidates, gates, and lab-only report drafts.

## Report-writing requirement

When the user asks to test the full bug-bounty flow, include report drafting as a first-class step, not an afterthought. A lab-only report should include:

- executive summary;
- scope/rules of engagement;
- methodology and tooling;
- evidence locations;
- detailed findings;
- false positives/exclusions;
- report-readiness gate result;
- conclusion and next actions.

Never submit or present the lab report as a real bug-bounty report.
