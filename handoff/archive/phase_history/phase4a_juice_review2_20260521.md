> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4A Juice Shop Run — 第二輪安全/結果 Review

Target: http://<lab-ip>:3000
Scope: local intentionally vulnerable host-only lab
Run mode: bounded Phase 4A calibration, candidate-only
Reviewer: Hermes second-pass result/safety review
Date: 2026-05-21

## 結論

可以撰寫「lab-only pentest report」草稿，但只能以本機授權實驗室演練/校準報告呈現；不得宣稱任何項目為 confirmed real bug bounty finding，也不得暗示可直接提交真實 bug bounty。

本輪 active results 的證據完整度足以支持：

- 範圍與可用性：pre/post health 均為 HTTP 200，目標是 host-only local lab。
- 觀察分類：headers/CORS/fixed-path metadata/SPA fallback/`/ftp/` metadata-only 都有輸出。
- 報告限制：目前多數是 observation 或 candidate_needs_manual_verification；缺少真實影響鏈、手動驗證、敏感資料最小化取證、修復/重測證據。

## 分類

### Candidate findings（候選，需人工驗證；不可升級為已確認）

1. `/ftp/` directory listing candidate
   - Evidence: `/ftp/` HTTP 200，title 為 `listing directory /ftp/`，body_class=`directory_listing_candidate`，link_metadata 顯示多個檔名/大小/時間戳 metadata。
   - Safety boundary: 未下載檔案內容；只保留目錄頁 metadata/body sample。
   - Review classification: 合理候選發現，可進 lab-only report 的 Findings/Candidates 區段。
   - Verification needed: 低風險手動確認目錄索引是否可由未登入使用者存取；只允許 HEAD/Range 或單一明確允許的小樣本 metadata 驗證，不做 recursive download、不抓取敏感檔、不解密/破解、不大量枚舉。
   - Report wording: 應寫成「publicly accessible directory listing candidate in local Juice Shop lab」，而非已確認的真實 bounty 漏洞。

2. Missing security headers baseline weakness
   - Evidence: headers audit score 2/9；HSTS/CSP/Referrer-Policy/Permissions-Policy/COOP/COEP 缺失；XCTO/XFO present；HEAD 未見 Set-Cookie。
   - Review classification: 可作為 lab-only hardening candidate / baseline weakness，但單獨不應視為有效 bug bounty finding。
   - Verification needed: 若要提升嚴重性，必須鏈結可驗證影響，例如 XSS + no CSP、敏感 action clickjacking、cookie/session attribute 問題。現有資料沒有這些鏈。
   - Report wording: Low/Informational hardening gap；避免獨立高嚴重度敘述。

### Informational observations（資訊性觀察）

1. CORS baseline observation
   - Evidence: tested 1 URL with crafted origins；0 misconfig hits；baseline ACAO `*`，未觀察到 wildcard+credentials 或 reflected attacker origin + credentials。
   - Classification: informational / clean for tested path。
   - Limitation: 只測 1 URL；不能宣稱整站 CORS 安全，只能說本次受限測試未發現可利用 misconfiguration。

2. `robots.txt` present with `Disallow: /ftp`
   - Evidence: `/robots.txt` HTTP 200，body `User-agent: *\nDisallow: /ftp`。
   - Classification: informational hint；不是漏洞本身。
   - Use: 可作為為何檢查 `/ftp/` 的 discovery chain，但不可將 robots disclosure 單獨當 finding。

3. `security.txt` and `/.well-known/security.txt`
   - Evidence: HTTP 200，public Juice Shop contact / acknowledgements / preferred languages。
   - Classification: informational；在 Juice Shop lab 屬預期公開資訊。

4. X-Recruiting header `/#/jobs`
   - Evidence: baseline headers show `X-Recruiting: /#/jobs`。
   - Classification: informational easter-egg/recruiting hint；本次沒有敏感資料或 exploit impact。

5. Health and availability
   - Evidence: active checks and Nikto attempt pre/post health HTTP 200。
   - Classification: operational assurance；支持本次 bounded checks 沒有造成可見可用性影響。

### False positives / de-escalated items（誤報或降級）

1. SPA fallback 200 responses
   - Evidence: `/sitemap.xml`、`/manifest.json`、`/favicon.ico` 等 HTTP 200 但 body hash matches root/canary，title `OWASP Juice Shop`。
   - Classification: false positive trap / de-escalated observation。
   - Rationale: 200 不代表真實 sitemap/manifest/favicon 內容存在；應視為 SPA fallback，而不是 exposed file。

2. CORS wildcard alone
   - Evidence: ACAO `*` baseline，但 audit 沒有 wildcard+credentials hit。
   - Classification: not a CORS vulnerability in this run；最多 informational。

3. Missing Set-Cookie attributes on HEAD
   - Evidence: no `Set-Cookie` observed on HEAD/root response。
   - Classification: not a cookie attribute finding；沒有 cookie 就不能判定 Secure/HttpOnly/SameSite 缺失。

4. Security headers as standalone bounty report
   - Evidence: missing multiple headers，但沒有 exploit chain。
   - Classification: lab hardening observation，不是可提交的 standalone real bounty finding。

### Blocked / incomplete items（受阻或未完成）

1. Bounded Nikto scan
   - Evidence: Nikto availability visible，pre/post health 200；context notes indicate red-team Kali attempt failed before scan because update check returned 403。
   - Classification: blocked/no scan evidence；不得引用 Nikto findings。
   - Next action: 若要重試，需禁用/避免 update check、固定單 host/port、timeout、candidate-only import、pre/post health；仍只限 local lab。

2. `/ftp/` content impact verification
   - Evidence: only metadata observed；no file bodies downloaded。
   - Classification: intentionally incomplete by safety design。
   - Next action: 需要 operator approval for a narrower manual verifier before reading any body content. Prefer metadata-only HEAD/Range and do not fetch sensitive-looking files such as `.kdbx`, `.bak`, compiled binaries, archives, or encrypted artifacts unless explicitly scoped for lab exercise.

3. Authenticated/user-context checks
   - Evidence: no credentials used。
   - Classification: not tested。
   - Next action: any authenticated flow requires separate approval, throwaway lab account, CSRF/state-change controls, and evidence redaction.

4. High-risk/aggressive testing
   - Evidence: brute force, sqlmap dump, callbacks, recursive mirroring, destructive actions, high-volume fuzzing were explicitly rejected/deferred。
   - Classification: blocked by safety gate。
   - Next action: only in isolated snapshot lab with T4/T5 activation review, health checks, kill/recovery controls, audit logs, and operator approval.

## Lab-only report readiness

Verdict: READY_WITH_LIMITATIONS for a lab-only pentest report draft.

Allowed report scope:

- Title/overview must say local OWASP Juice Shop lab calibration, not real bug bounty submission.
- Findings section may include:
  - `/ftp/` directory listing candidate requiring manual verification.
  - Missing security headers as Low/Informational hardening gap.
- Observations section may include CORS no-hit result, robots/security.txt metadata, SPA fallback false-positive traps, and health preservation.
- Limitations section must state no recursive download, no file body review, no credentials, no exploit chains, Nikto blocked, one tested CORS URL, and candidate-only semantics.

Not allowed:

- No confirmed vulnerability language.
- No real bug bounty severity claims.
- No claims that all CORS endpoints are safe.
- No claims that `/ftp/` contents expose sensitive data, because content bodies were not reviewed.
- No Nikto-derived finding.

## 下一步 verifier 建議與限制

1. Low-risk `/ftp/` metadata verifier
   - Confirm directory-listing page remains distinct from SPA fallback.
   - Capture HTTP status, content type, title, link count, and selected link names only.
   - Optional: one HEAD request per listed item for headers only; no GET body downloads.
   - Stop if unexpected redirects/auth prompts/large response/error spikes occur.

2. Header remediation verifier
   - Re-run headers audit after app/proxy config changes.
   - If trying to create a real finding chain, first produce separate evidence of exploitable XSS/clickjacking/session-cookie weakness; do not infer impact from headers alone.

3. CORS expansion verifier
   - If needed, test a small allowlisted set of API endpoints, with crafted Origin and credential/no-credential variants.
   - Still candidate-only; require a browser PoC only if reflected origin + credentials or sensitive cross-origin-readable data is observed.

4. Nikto retry gate
   - Retry only if the tool can run without external update dependency or with update disabled.
   - Enforce single target/port, timeout, rate controls, output import as observation-only, and pre/post health checks.

5. Report pipeline verifier
   - Build candidate packet -> gap/action report -> verification plan -> report-readiness gate -> lab-only report draft.
   - The final gate should fail closed on any wording that promotes candidate/observation to confirmed bounty finding.

## Final reviewer decision

PASS_WITH_LIMITATIONS.

The active results are suitable for local lab reporting calibration and next-step verifier planning. They are not sufficient for confirmed bug bounty claims. The safest next move is to draft a lab-only pentest report with explicit candidate/informational/false-positive/blocked labels, then run a narrow `/ftp/` metadata verifier and report-readiness wording gate before any deeper content review.
