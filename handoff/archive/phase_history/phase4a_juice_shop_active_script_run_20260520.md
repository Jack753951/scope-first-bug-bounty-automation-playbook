> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4A Juice Shop Active Script Run — 2026-05-20

Status: completed / candidate-only lab calibration
Prepared by: Hermes
Reviewer route: Hermes orchestration + delegated model review step
Runtime/tools: red-team Kali via `scripts/kali-run.ps1`; scripts: `headers_audit.sh`, `cors_audit.sh`, `nikto`, custom low-risk path verifier
Model/runtime model: exact backend runtime not fully exposed by interface; delegated review returned model label `gpt-5.5`

## Scope and authorization

Target class: local intentionally vulnerable app controlled by operator.
Target: OWASP Juice Shop in local VirtualBox host-only lab.
URL: `http://<lab-ip>:3000`
Red-team Kali: `<lab-ip>`
Victim Kali: `<lab-ip>`

Allowed actions for this slice:

- header audit;
- CORS header audit with crafted Origin headers;
- controlled Nikto baseline with 2-minute max time;
- low-risk path verification using status/headers and 512-byte range peeks;
- candidate-only review.

Disallowed actions for this slice:

- brute force;
- heavy fuzzing;
- recursive download;
- OAST/callback;
- exploit chaining;
- credential theft or loot collection;
- DB dump or file read/write exploitation;
- public target interaction;
- confirmed vulnerability claims or report submission.

## Model review gate

A delegated model review inspected the baseline observations and recommended the next allowed scripts:

1. `headers_audit.sh` — low-risk security header inventory.
2. `cors_audit.sh` — bounded CORS verification because `Access-Control-Allow-Origin: *` appeared.
3. `nikto` — controlled lab-only baseline with time cap, no aggressive follow-up.
4. Low-risk path verification — reconcile Nikto claims with status/header/body-classification only.

The review explicitly warned that Nikto high-impact claims must be treated as unverified until manually checked and that no scanner output should become confirmed findings automatically.

## Executed commands

From Hermes/Windows to red-team Kali:

```bash
TARGET=http://<lab-ip>:3000
OUT="$HOME/phase4a-calibration/juice-shop-active-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$OUT"
cd /mnt/hacking
bash scripts/headers_audit.sh "$TARGET" --yes -o "$OUT/headers"
bash scripts/cors_audit.sh "$TARGET" --yes -o "$OUT/cors"
nikto -h "$TARGET" -nointeractive -Tuning 123457890 -maxtime 2m -output "$OUT/nikto.txt" -Format txt || true
```

Active-script output directory on red-team Kali:

```text
/home/kali/phase4a-calibration/juice-shop-active-20260520T102205Z
```

Low-risk path verification output directory:

```text
/home/kali/phase4a-calibration/juice-shop-verify-20260520T102634Z
```

## Results summary

### Headers audit

```text
Score: 2/9
Present: X-Content-Type-Options, X-Frame-Options/SAMEORIGIN
Missing: Strict-Transport-Security, Content-Security-Policy, Referrer-Policy, Permissions-Policy, COOP, COEP
No Set-Cookie on root path
```

Assessment: candidate / low-risk configuration weakness only. Not report-ready by itself.

### CORS audit

```text
URLs tested: 1
Misconfig hits: 0
```

Assessment: `Access-Control-Allow-Origin: *` is present, but no credentialed CORS misconfiguration was detected by the bounded script. Treat as informational unless later evidence shows credentials + sensitive readable data.

### Nikto controlled baseline

Nikto reported:

- `Access-Control-Allow-Origin: *`;
- uncommon `X-Recruiting: /#/jobs`;
- `robots.txt` with one entry;
- missing suggested headers;
- `/ftp/` and `/public/` interesting;
- many JSON paths as interesting;
- high-impact-looking claims for `/.htpasswd`, `/.bash_history`, `/.sh_history`;
- `JAMonAdmin.jsp` XSS CVE hint;
- contradictory `X-Content-Type-Options missing` claim.

Assessment: Nikto produced useful leads plus obvious noise. All high-impact-looking items remain unverified until the path verifier reconciles them.

### Low-risk path verifier

Key path verifier outcomes:

```text
/                 206 text/html; title OWASP Juice Shop; X-Content-Type-Options nosniff
/ftp/             200 text/html; title listing directory /ftp/; interesting-directory-or-route
/public/          206 text/html; title OWASP Juice Shop; SPA fallback
/robots.txt       200 text/plain; robots entry: Disallow: /ftp
JSON paths        206 text/html; title OWASP Juice Shop; SPA fallback
/.htpasswd        206 text/html; title OWASP Juice Shop; SPA fallback
/.bash_history    206 text/html; title OWASP Juice Shop; SPA fallback
/.sh_history      206 text/html; title OWASP Juice Shop; SPA fallback
/JAMonAdmin.jsp   206 text/html; title OWASP Juice Shop; SPA fallback
```

Assessment:

- `/.htpasswd`, `/.bash_history`, `/.sh_history`: likely Nikto false positives caused by SPA fallback / partial-content HTML, not retrieved secret files.
- `JAMonAdmin.jsp`: likely Nikto false positive; Node/Express Juice Shop SPA fallback, not a real JSP admin panel.
- JSON paths: likely SPA fallback, not exposed JSON data in this check.
- `X-Content-Type-Options`: present as `nosniff` in verifier; Nikto missing-header claim likely false or path-specific scanner issue.
- `/ftp/`: real interesting directory route; candidate for next manual metadata-only review.
- `robots.txt`: informational; points to `/ftp`.

## Candidate-only triage table

| Item | Status | Next action |
|---|---|---|
| Missing CSP/Referrer/Permissions/COOP/COEP/HSTS | Candidate / low info | Keep as header baseline; do not report standalone |
| ACAO `*` | Informational | No credentialed CORS finding yet |
| `/ftp/` directory | Candidate | Manual metadata-only review; do not recursively download |
| `/public/` | Likely SPA fallback | No issue yet |
| JSON paths | Likely SPA fallback false positives | No issue yet |
| `/.htpasswd` | Likely false positive | No secret file retrieved |
| `/.bash_history`, `/.sh_history` | Likely false positives | No shell history retrieved |
| `JAMonAdmin.jsp` | Likely false positive | No JSP service evidence |
| Nikto X-Content-Type-Options missing | Likely false positive | Verifier saw `nosniff` |
| `robots.txt` | Informational | Points to `/ftp` |
| `X-Recruiting` | Informational | App hint/easter egg |

## Current bug-bounty-style workflow result

This run successfully exercised the intended loop:

1. Recon/baseline collection.
2. Model review of recon results.
3. Model-selected next scripts under safety limits.
4. Active lab-only scripts executed on the exact target.
5. Second review reconciled scanner noise.
6. Candidate-only triage produced without confirmed findings.

No real bug-bounty target, public target, external callback, credential handling, loot, report submission, or destructive action was used.

## Recommended next step

Proceed to a narrow `/ftp/` manual metadata review and evidence-packet conversion:

- list only file names and sizes, no recursive download;
- fetch at most harmless metadata or first bytes of non-sensitive training files if needed;
- classify whether `/ftp/` is an intentional Juice Shop training route;
- convert `/ftp/` and missing-header observations into candidate review packets;
- run the existing report-readiness gate to confirm they remain not-ready or lab-only.

Do not start SQLi/XSS automation yet. If the operator wants offensive payload testing next, create a separate bounded approval slice for one endpoint and one payload family.
