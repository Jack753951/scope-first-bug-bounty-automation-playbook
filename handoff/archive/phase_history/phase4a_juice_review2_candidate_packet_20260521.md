> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4A Juice Shop 第二輪攻擊/報告 Review — Candidate Packet

Target: `http://<lab-ip>:3000`
Scope: local intentionally vulnerable OWASP Juice Shop host-only lab
Mode: bounded Phase 4A calibration；candidate-only；manual verification required
Evidence root: `scans/phase4a_juice_20260521_083738/`
Reviewer output: 第二輪結果轉換為 candidate packet、gap list、verification plan、lab-only report readiness verdict

## Safety / authorization boundary

- 本輪只適用於本機 host-only lab，不可外推為真實 bug bounty 目標結論。
- 所有項目都維持 `candidate` / `observation` / `hardening`，不升級成 confirmed finding。
- 不要求 destructive steps；不要求 brute force、credential guessing、recursive download、SQL dump、external callback/OAST、高流量 fuzzing、ZAP active scan 或 exploit chaining。
- 若未來要測 aggressive upper-bound，只能放到 isolated snapshot future slice：獨立快照、可回復 victim、健康檢查、timeout/kill switch、audit log、redaction、operator explicit approval。

## Input evidence digest

- Headers audit: score `2/9`。存在 `X-Content-Type-Options: nosniff` 與 `X-Frame-Options: SAMEORIGIN`；缺少 HSTS、CSP、Referrer-Policy、Permissions-Policy、COOP、COEP；未觀察到 Set-Cookie。
  - Evidence: `headers_audit/report.md`, `headers_audit/detail.md`, `headers_audit/scores.csv`
- CORS audit: tested 1 URL，misconfig hits `0`；沒有反射 attacker origin + credentials 的證據。
  - Evidence: `cors_audit/report.md`
- Robots / fixed path probe: `/robots.txt` public，內容 `Disallow: /ftp`。
  - Evidence: `local_lab_web_observation_probe.json`
- `/ftp/`: HTTP 200，title `listing directory /ftp/`，body class `directory_listing_candidate`，只收集目錄 listing metadata，未下載檔案內容。
  - Visible metadata includes names such as `acquisitions.md`, `announcement_encrypted.md`, `coupons_2013.md.bak`, `incident-support.kdbx`, `package-lock.json.bak`, `package.json.bak`, `suspicious_errors.yml`.
  - Evidence: `local_lab_web_observation_probe.json`
- Security.txt: `/security.txt` 與 `/.well-known/security.txt` 皆 HTTP 200，內容為公開聯絡/致謝 metadata。
  - Evidence: `local_lab_web_observation_probe.json`
- SPA fallback: `/sitemap.xml`, `/manifest.json`, `/favicon.ico`, `/#/jobs`, canary path 回傳與 root 相同 HTML/body hash，屬 SPA fallback / false-positive trap。
  - Evidence: `local_lab_web_observation_probe.json`
- Nikto: 本輪只確認 tool availability 與 pre/post health；bounded Nikto 未產出可用 findings（因 update/check-before-scan 或未完成有效掃描而無 finding evidence）。
  - Evidence: `02_active_checks_run.txt`, `03_bounded_nikto.txt`

## Candidate packet

### CAND-001 — Public `/ftp/` directory listing metadata exposure

- Status: `candidate_needs_manual_verification`
- Report material quality: **好報告素材（本輪最佳 candidate）**，但還不是可提交 finding。
- Evidence summary:
  - `robots.txt` explicitly hints `Disallow: /ftp`.
  - `/ftp/` returns HTTP 200 with title `listing directory /ftp/`.
  - Listing metadata exposes file names, sizes/timestamps-like text, and backup/sensitive-looking filenames.
  - No recursive download and no file-body review were performed.
- Why it may matter:
  - Directory listing may disclose internal/business filenames, backup artifacts, dependency manifests, encrypted archives, or operational hints.
  - In real programs this needs proof of sensitive content or meaningful exposure; filename metadata alone may be insufficient.
- False-positive / caveat:
  - Juice Shop intentionally exposes training content; lab-only result cannot imply real-world impact.
  - Metadata-only evidence is enough for candidate triage, not enough for confirmed severity.
- Minimal non-destructive manual verification needed:
  - Reconfirm route is actual directory listing, not SPA fallback.
  - Capture headers/title/body-class/hash and listing metadata only.
  - If operator explicitly approves a narrower manual review, sample one clearly non-sensitive text/manifest item only; do not recurse or download loot-like files by default.
- Current readiness: `not_report_ready` until manual content sensitivity/impact review and remediation wording exist.

### CAND-002 — Missing security headers baseline

- Status: `hardening_observation`
- Report material quality: **hardening/noise unless chained**。
- Evidence summary:
  - Headers score `2/9`.
  - Missing HSTS, CSP, Referrer-Policy, Permissions-Policy, COOP, COEP.
  - Present: `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`.
  - No Set-Cookie observed, so cookie attribute finding is not supported.
- Why it may matter:
  - CSP matters if paired with XSS or script injection evidence.
  - HSTS matters on HTTPS/on-path downgrade contexts, not this HTTP-only lab by itself.
  - Referrer/Permissions/COOP/COEP can be hardening recommendations.
- False-positive / caveat:
  - Most bug bounty programs reject standalone missing-header reports as informational.
  - Current evidence shows configuration hardening gap, not exploitable vulnerability.
- Current readiness: `not_report_ready_as_finding`; can be included in lab report as hardening appendix.

### CAND-003 — CORS posture

- Status: `closed_clean_observation`
- Report material quality: **not report material**。
- Evidence summary:
  - CORS audit found `0` misconfig hits.
  - ACAO `*` observed in headers, but no credentialed readable cross-origin behavior was shown.
- Why it may matter:
  - `Access-Control-Allow-Origin: *` can be informational on public resources.
- Current readiness: `do_not_report`; mention only as tested-and-clean methodology note.

### CAND-004 — `security.txt` public exposure

- Status: `benign_observation`
- Report material quality: **noise / expected public metadata**。
- Evidence summary:
  - `/security.txt` and `/.well-known/security.txt` return public contact/acknowledgement metadata.
- Current readiness: `do_not_report`; include only as route classification evidence if needed.

### CAND-005 — SPA fallback paths

- Status: `false_positive_trap`
- Report material quality: **noise; useful only to explain exclusions**。
- Evidence summary:
  - Several paths return HTTP 200 but same title/body hash as root page.
  - Canary path confirms SPA fallback behavior.
- Current readiness: `do_not_report`; useful for excluding scanner/Nikto-looking path hits.

### CAND-006 — Nikto bounded baseline

- Status: `no_finding_evidence`
- Report material quality: **no report material**。
- Evidence summary:
  - Pre/post health checks were OK.
  - Nikto availability/version seen, but no usable scan findings captured due update/check-before-scan / no effective output.
- Current readiness: `do_not_report`; record as tool-run limitation/gap only.

## Gap list

| Gap ID | Candidate | Gap | Effect on report readiness | Action class |
|---|---|---|---|---|
| GAP-001 | CAND-001 | `/ftp/` evidence is metadata-only; no manual sensitivity/impact determination | Blocks confirmed finding | Manual review, non-destructive |
| GAP-002 | CAND-001 | No remediation text tied to Juice Shop-like directory listing control | Blocks report draft | Draft remediation after verification |
| GAP-003 | CAND-001 | No retest criteria | Blocks report completeness | Add expected 403/404/no-index/no-listing retest |
| GAP-004 | CAND-001 | No severity decision; impact not proven | Blocks severity claim | Keep severity TBD/low until content impact verified |
| GAP-005 | CAND-002 | Missing headers are standalone hardening with no exploit chain | Blocks vulnerability report | Mark hardening appendix only |
| GAP-006 | CAND-003 | CORS audit clean; no misconfig evidence | Blocks any CORS finding | Close as tested-clean |
| GAP-007 | CAND-004 | security.txt is intended public standard metadata | Blocks finding | Close as benign |
| GAP-008 | CAND-005 | HTTP 200 path hits are SPA fallback | Blocks path exposure claims | Use content-class canary before reporting paths |
| GAP-009 | CAND-006 | Nikto produced no usable finding evidence | Blocks scanner-derived finding | Treat as limitation; rerun only if bounded/manual and useful |
| GAP-010 | Global | Lab-only intentionally vulnerable target | Blocks real bug bounty submission | Label lab-only; do not submit |

## Verification plan

### CHECK-001 — Scope and evidence integrity

- Applies to: all candidates
- Verify target remains `http://<lab-ip>:3000` in host-only lab.
- Confirm evidence paths are from `scans/phase4a_juice_20260521_083738/` and no credentials/loot are embedded in report output.
- Expected result: evidence remains lab-local and candidate-only.

### CHECK-002 — `/ftp/` route is real directory listing

- Applies to: CAND-001
- Minimal steps: single GET/HEAD-style route classification; record status, content-type, title, body hash, and listing marker.
- Do not recurse; do not bulk download; do not inspect loot-like files by default.
- Expected result: `title = listing directory /ftp/`, not root SPA hash.

### CHECK-003 — `/ftp/` metadata sensitivity triage

- Applies to: CAND-001
- Review visible names/sizes/timestamps for reportable exposure indicators: backups, dependency manifests, password-manager DB, encrypted documents, incident/support names.
- If extra proof is needed, require explicit operator approval for one narrow, non-sensitive sample; otherwise stay metadata-only.
- Expected result: either (a) enough metadata-impact language for lab report, or (b) remain informational.

### CHECK-004 — `/ftp/` remediation and retest definition

- Applies to: CAND-001
- Remediation draft: disable directory listing; remove public backups/sensitive artifacts; serve only intended static assets; enforce allowlist/authorization; ensure robots.txt is not relied upon as access control.
- Retest draft: `/ftp/` no longer lists directory; sensitive/backup artifacts inaccessible; robots.txt does not reveal hidden sensitive routes.

### CHECK-005 — Header hardening classification

- Applies to: CAND-002
- Confirm no Set-Cookie exists before making cookie attribute claims.
- Do not claim missing CSP/HSTS as vulnerability without an exploit chain.
- Expected result: lab report appendix/hardening note, not a bounty finding.

### CHECK-006 — CORS closure

- Applies to: CAND-003
- Confirm no reflected arbitrary Origin with `Access-Control-Allow-Credentials: true` and readable sensitive response evidence.
- Expected result: close as clean/no finding.

### CHECK-007 — SPA fallback exclusion

- Applies to: CAND-005 and future scanner/path hits
- Compare suspicious route body hash/title/content-type against root and canary path.
- Expected result: exclude SPA fallback 200s from findings.

### CHECK-008 — Nikto limitation handling

- Applies to: CAND-006
- Do not derive findings from the failed/empty Nikto run.
- If rerun is desired later, keep single host/port, short timeout, pre/post health, observation-only output; still manually classify content class.
- Expected result: no scanner-only finding.

## Lab-only report readiness verdict

Verdict: `NOT_READY_FOR_REAL_BUG_BOUNTY_SUBMISSION`; `PARTIAL_READY_FOR_LAB_ONLY_REPORT`.

- Ready as good lab report material:
  - CAND-001 `/ftp/` directory listing metadata exposure as a candidate finding, clearly labelled unverified/manual-review-required.
  - SPA fallback analysis as false-positive/exclusions section.
  - Headers audit as hardening appendix, not finding.
  - CORS clean result as methodology/negative finding note.
- Not ready / do not submit as real bounty:
  - Missing headers as standalone vulnerability.
  - CORS finding (clean).
  - security.txt exposure.
  - Scanner/Nikto-derived claims.
  - Any SPA fallback path treated as sensitive file exposure.
- Minimum to become lab-report-ready:
  1. Complete CHECK-002 to CHECK-004 for `/ftp/`.
  2. Add screenshot/text evidence snippets that do not include loot or secrets.
  3. Add impact wording constrained to metadata exposure unless file content is explicitly and safely verified.
  4. Add remediation and retest criteria.
  5. Preserve lab-only disclaimer and candidate status.

## Isolated snapshot future slice — aggressive upper-bound only

Only if the operator separately approves and the lab is snapshotted/isolated:

- Purpose: measure upper-bound risk and runner safety, not produce automatic confirmed findings.
- Requirements before any aggressive test:
  - Fresh victim VM/container snapshot and restore plan.
  - Host-only isolation confirmed; no external callbacks/OAST.
  - Pre/post health checks, timeout, kill switch, logs, redaction, and audit trail.
  - Explicit allowlist of target/port/path family and stop conditions.
- Candidate future tests to discuss only after controls exist: bounded crawler depth, limited active scanner profile, or controlled file-content sample review. No destructive or irreversible actions by default.

## Reviewer conclusion

第二輪結果中，`/ftp/` directory listing 是唯一值得推進成 report candidate 的素材；它仍需要人工驗證、影響判斷、修補/複測文字。Headers 是 hardening；CORS clean、security.txt、SPA fallback、Nikto empty/failed output 都不是 finding。整體可以進入 lab-only report draft 的候選階段，但不可當成真實 bug bounty submission。
