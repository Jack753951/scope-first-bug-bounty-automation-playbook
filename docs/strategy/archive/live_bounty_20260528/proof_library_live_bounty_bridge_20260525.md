> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Proof Library → Live Bounty Bridge — 2026-05-25

Status: active bridge / Phase 5A decision aid
Source: Hermes synthesis after <program-redacted> Taiwan single-account live-target dry run
Date: 2026-05-25
Repo truth: `handoff/proof_library_index_20260523.md`, `programs/<program-slug>/notes/coupang_tw_pre_second_phone_single_account_auth_boundary_20260525.md`, `programs/<program-slug>/notes/coupang_tw_single_account_surface_map_20260525.md`, `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`

## Reviewer identity

- Reviewer route/tool: Hermes local repo synthesis
- Visible runtime model: `gpt-5.5`
- Provider / CLI version if visible: `openai-codex` provider; exact backend deployment not exposed
- Review focus: live bounty readiness, proof-pattern reuse, authorization/scope decision support
- Limitation: synthesis only; no additional live target requests or scans performed while writing this bridge

## Purpose

This bridge converts the local-lab proof library into live-bounty decision rules.

Use it before live target-touching work to answer:

1. Which local proof pattern is relevant?
2. What live prerequisites are mandatory before the pattern can be tested?
3. What is allowed with one owned account only?
4. What remains blocked until Account B / program guidance / safer scope exists?
5. What evidence would upgrade a surface observation into candidate or report-ready status?

This file does not authorize public targets, scans, fuzzing, exploit automation, payment/KYC/order/upload/seller/admin testing, or report submission. It is a routing and evidence-quality aid.

## Global live-bounty defaults

Default until a specific program says otherwise:

- Manual / browser-assisted / low-speed only.
- One live target lane at a time.
- Owned or program-authorized accounts only.
- No credentials, OTP, cookies, tokens, phone numbers, emails, addresses, or third-party data in artifacts.
- Candidate language until report-readiness review passes.
- Stop on CAPTCHA, rate limit, account warning, anti-abuse prompt, unexpected third-party data, policy uncertainty, or sensitive flow boundary.

Blocked by default:

- Broad scanner/fuzzer/bruteforce/dirbusting/nuclei/sqlmap/port scan.
- OAST/callback/public listener/tunnel/pivot.
- Payment, checkout, cash, KYC/AML, refunds/returns requiring real orders, upload/video-upload, seller/admin/internal flows.
- Customer-support messages, recovery flows, coupon redemption, or other state-changing actions unless a narrow approved plan exists.
- Automatic vulnerability report submission.

## Decision labels

Use these labels consistently:

- `surface_only`: normal UI/asset observation; no security claim.
- `needs_second_account`: object ownership / IDOR / BOLA cannot be proven with one account.
- `blocked_state_change`: next click/request would mutate state or contact support.
- `blocked_sensitive_flow`: next flow touches recovery, payment, KYC, upload, seller/admin, or sensitive user data.
- `gate_fixed_dry_run_verified`: local authorization gate accepts exact in-scope dry-run targets and rejects out-of-scope targets; still not permission for live scanner-like automation by itself.
- `gate_fail_closed_needs_fix`: local authorization gate denies safely but is not usable for automation readiness.
- `candidate`: safe evidence suggests a possible issue but controls are incomplete.
- `report_ready`: scoped, allowed, reproducible, redacted, meaningful impact, positive/negative controls complete, and Hermes synthesis approves report packet.

## Local proof pattern bridge

| Local proof pattern | Verified local sources | Live bounty usable when | Blocked when | Minimum live evidence | <program-redacted> Taiwan current status |
|---|---|---|---|---|---|
| IDOR / object ownership / BOLA | `modules/bundles/verified_lab_flow_modern_api_idor_object_ownership.md`; `modules/bundles/verified_lab_flow_webgoat_idor_lesson_access_control.md`; `handoff/modern_api_auth_role_separation_wave1_20260523.md` | Two operator-owned or program-provided accounts exist; object IDs are obtained from normal UI/API provenance; program allows low-speed account-owned access-control testing; no third-party data is touched | Only one account exists; IDs are guessed; program rules forbid multi-account tests; flow touches payment/order/KYC/support/upload/seller/admin | Account A object provenance, Account A positive access, Account B negative control, optional secure-role/control endpoint, redacted request/response summary, no third-party data | `needs_second_account`; single account exposed empty order/inquiry/coupon-like states and no safe object ID |
| Auth/session/member boundary mapping | `modules/bundles/verified_lab_flow_modern_api_auth_role_separation.md`; WebGoat auth/session/JWT bundles | Normal UI allows account/session/profile/member pages; actions are read-only; no recovery or anti-abuse prompt appears | Login/signup bot detection, CAPTCHA/OTP/account warning; password reset/find-ID/recovery; session secrets would need to be copied | Auth-required vs unauth state, session/logout behavior, non-sensitive account label, screenshots/request summaries without cookies/tokens | Useful. `member.tw.<program-redacted>.com`, `id.tw.<program-redacted>.com`, and `my.tw.<program-redacted>.com` mapped to surface/empty states |
| Browser runtime XSS safe-marker | `modules/bundles/verified_lab_flow_webgoat_browser_runtime_xss_safe_marker.md`; `modules/bundles/verified_lab_flow_modern_api_xss_runtime_proof.md` | Owned profile/search/review/comment field supports harmless marker and program allows content testing; no active payload beyond benign marker; no third-party viewers | Requires creating public content/reviews/orders; could affect other users; CSP bypass/stealing cookies/exfiltration; upload or stored content not clearly allowed | Owned input provenance, benign marker render evidence, negative/control render, no token/cookie access, cleanup if state changed | Not suitable yet. No safe owned content field used; review/order creation blocked |
| File read / path traversal / XXE safe-marker | `modules/bundles/verified_lab_flow_modern_api_path_traversal_file_read.md`; `modules/bundles/verified_lab_flow_modern_api_xxe_safe_marker.md`; WebGoat file-write patterns | Program explicitly allows this class; target has a legal upload/import/file parameter lane; proof can use harmless owned marker only | Live target without explicit permission; attempts at `/etc/passwd`, cloud metadata, secrets, internal paths, or uploads; scanner/fuzzer required | Lab/owned marker provenance, positive marker read, wrong-path/no-entity negative control, no secret file access, redacted evidence | Blocked. <program-redacted> current safe lane has no file/import/upload permission and upload surfaces are deferred |
| SSRF / callback proof | `modules/bundles/verified_lab_flow_modern_api_ssrf_isolated_callback.md`; `handoff/modern_api_ssrf_true_attacker_callback_evidence_packet_20260523.md` | Program explicitly permits external callbacks/OAST or provides approved callback route; target has scoped URL-fetch feature; request budget and callback endpoint are approved | Default live bounty state; no callback permission; internal probing/metadata endpoints; public listener/tunnel not approved | Approved callback domain, one-shot trigger, listener log with marker/source, no internal scan/metadata, post-test cleanup | Blocked. No callback/OAST permission for <program-redacted> lane |
| Command injection / server-side execution | DVWA command-injection bundles; modern API bounded deserialization marker | Client/lab explicitly authorizes exploit validation and safe marker command; recoverable target or written permission exists | Public bounty normal shopping/account surface; would execute commands, read files, persist, or disrupt service | Written permission, exact one-shot marker command, pre/post health, no secrets/persistence, cleanup | Blocked for <program-redacted>. Not relevant to current manual account surface map |
| Upload / retrieval validation | `modules/bundles/verified_lab_flow_modern_api_upload_retrieval.md`; `modules/bundles/verified_lab_flow_file_upload_marker_pdf.md` | Program allows upload testing; content is benign inert marker; storage/public visibility rules are understood; cleanup exists | Active content, malware-like files, video/fileupload surfaces without explicit plan, public exposure to other users | Owned inert marker file, accepted/rejected controls, retrieval proof if allowed, cleanup, no active content | Deferred/blocked. <program-redacted> upload/video-upload targets were intentionally not touched |
| Exposure / metadata / headers / API docs | API docs / metrics / headers bundles | Asset is in scope; observation is passive/manual or tiny request budget; no brute force/crawl | Requires broad discovery, dir brute force, scanner output, or access to non-public/internal docs | Exact URL provenance, status/headers/body excerpt, impact explanation, no broad enumeration | Partially useful for root pages only. `id.tw.<program-redacted>.com` plain `hello` is `surface_only`, no issue by itself |
| Report-readiness evidence packet | SSRF, DVWA, WebGoat XSS evidence packets | Evidence is scoped, allowed, reproducible, redacted, has impact and controls | Missing controls, single-account-only IDOR, no impact, or program-policy uncertainty | Summary, asset, allowed technique, steps, expected/actual, impact, redacted evidence, remediation, limitations | Not report-ready. Current <program-redacted> result is no finding / readiness learning only |

## <program-redacted> Taiwan live-target dry run benefit

The 2026-05-25 <program-redacted> single-account test did not produce a vulnerability, but it materially improved the project in these ways:

1. It validated the live-target safety profile in a real <bug-bounty-platform> context: low-speed, browser-assisted, single lane, no scans, no state-changing actions, no sensitive artifact retention.
2. It proved the local proof library can prevent overclaiming: IDOR/BOLA was correctly classified as `needs_second_account`, not forced into a weak report.
3. It produced a target-specific empty-state map for the first live program: review/customer-service, id, member, my-account/order-list roots.
4. It identified future object families for Account A/B testing without touching them prematurely: orders, cancel/return/exchange/refund, coupons, inquiry records, profile/payment/address-like settings.
5. It discovered a repo authorization-gate readiness defect safely: `recon.sh --program <program-slug>` slug incompatibility and `localhost` scope-entry parsing failed closed before any automation; this was later fixed with focused regressions in `tests/test_recon_gate.sh`.
6. It created a reusable live-bounty bridge requirement: every local proof pattern now needs live prerequisites and blocked-state labels before use on real services.

## Current <program-redacted> target-state map

| Asset | Current observed state | Useful next question | Current label |
|---|---|---|---|
| `review.tw.<program-redacted>.com` | Customer-service style page with no recent inquiry records; contact action visible but not used | Does a legitimate owned review/inquiry object appear after normal non-test usage or Account B availability? | `surface_only`, `blocked_state_change`, `needs_second_account` |
| `id.tw.<program-redacted>.com` | Plain minimal `hello` root | Is this expected lightweight id-root behavior or merely a health/static root? No issue without impact. | `surface_only`, `no_finding` |
| `member.tw.<program-redacted>.com` | Redirects/lands on public <program-redacted> home with logged-in UI elements | Which member/auth paths remain read-only and non-sensitive? Avoid recovery/password flows. | `surface_only` |
| `my.tw.<program-redacted>.com` / `mc.tw.<program-redacted>.com` | My <program-redacted> order list empty; account-center navigation visible | After Account B exists, which owned object family can be tested with positive/negative controls and no payment/order creation? | `surface_only`, `needs_second_account` |

## Before Account B: allowed value-add work

Do:

1. Keep repo authorization-gate dry-runs healthy (`gate_fixed_dry_run_verified`).
2. Run `scripts/post-proof-consolidation.sh --type <type> --artifact <path> --dry-run` after new proof/bundle/live-surface artifacts, then update the listed indexes before wrap-up.
3. Prepare an A/B object-ownership matrix template without executing it.
4. Draft program-guidance request through official contact/ask route if available.
5. Refine bundle proof cards with live prerequisites.

Do not:

1. Create state just to manufacture IDs.
2. Touch support chat/contact, account recovery, coupon redemption, checkout/payment/KYC/upload/seller/admin.
3. Run recon/scanners/fuzzers against <program-redacted>.
4. Submit <bug-bounty-platform> report/guidance draft without operator approval.

## After Account B: first safe A/B matrix

Prerequisites:

- Account B is operator-owned or program-provided.
- No phone-verification bypass or rented/SMS relay number.
- Program rules allow low-speed account-owned object testing or guidance is obtained.
- Evidence remains redacted and account labels are Account A / Account B only.

Matrix shape:

| Object family | Account A positive | Account B negative | State change? | Allowed now? | Notes |
|---|---|---|---|---|---|
| Inquiry record | View own record if one exists | B cannot view A record | Creating inquiry is state-changing | No, unless normal existing owned record exists or guidance allows | Avoid contacting support just for testing |
| Order record | View own order if one exists | B cannot view A order | Order creation/payment is high-risk | No, unless normal existing owned record exists and rules allow | Do not create purchase solely for test |
| Coupon | View own coupon state | B cannot use/view A coupon | Redemption is state-changing | Observation only | Do not redeem |
| Profile/settings | View/edit own non-sensitive setting | B cannot view/edit A setting | Editing is state-changing | Read-only first | Avoid payment/address/phone/email sensitive fields |
| Cart | View own cart | B cannot view A cart | Cart mutation is state-changing | Only if normal existing benign cart state exists and no checkout | Avoid checkout |

## <program-redacted> VDP first complete-flow result

The 2026-05-25 <program-redacted> first owned-account lane completed the low-pressure VDP practice loop end-to-end:

1. Passive program/policy intake selected <program-redacted> and captured researcher identity requirements.
2. `login.<program-redacted>.com` was operator-confirmed into `config/scope.txt`; dry-run gate passed for the research login path and failed closed for `example.org`.
3. Operator completed <bug-bounty-platform>-alias signup/login locally in Kali/noVNC.
4. Hermes performed browser-only owned-account observation and closed the lane as `NO_FINDING_CLOSEOUT` / `no_finding` with evidence status `surface_only`.

Observed <program-redacted> surfaces, all normal UI and no-finding/surface-only:

| Surface | Result | Label |
|---|---|---|
| Stories dashboard/editor | One onboarding story and sample nodes visible; publish/run controls not used | `surface_only`, `blocked_state_change` |
| Credentials | Empty state; creation controls visible but not used | `surface_only`, `blocked_sensitive_flow` |
| Resources | Empty state; creation controls visible but not used | `surface_only`, `blocked_state_change` |
| Users/settings | One owned tenant owner context visible; invite controls not used; raw identity not retained | `surface_only`, `blocked_state_change` |
| API keys | Empty state; key creation not used | `surface_only`, `blocked_sensitive_flow` |
| Authentication settings | Session/recovery/SSO/provisioning controls visible; unlock/mutation not used | `surface_only`, `blocked_state_change` |
| Workbench | Chat/tool/template/MCP surface visible; no prompt, MCP, or tool execution | `surface_only`, `blocked_state_change` |

Current <program-redacted> status:

```text
lane_state: NO_FINDING_CLOSEOUT / no_finding
queue_status: no_finding
runner_decision: lane_closed_or_parked / exit 0
report_status: no report packet; no vulnerability observed
next_safe_action: none by default; any further <program-redacted> lane requires a new plan
```

This result is useful as workflow validation, not a finding: it proves the alias/login gate, noVNC route, redaction discipline, machine evidence closeout, and the anti-overclaim path for VDP no-finding work.

## Required gate checks before live automation

Current status: `gate_fixed_dry_run_verified` for the previously observed compatibility blockers; this is still only a dry-run readiness signal, not authorization to run live scanner-like automation.

Fixed in this slice:

1. Program slug compatibility: `recon.sh` now accepts lowercase underscore slugs such as `<program-slug>` while still rejecting path-like values.
2. Local-lab scope compatibility: `localhost` is intentionally accepted as a local scope/target token instead of poisoning unrelated scope validation.
3. Focused regression coverage in `tests/test_recon_gate.sh` verifies:
   - exact in-scope <program-redacted> program dry-run passes;
   - global-scope dry-run for `member.tw.<program-redacted>.com` passes despite `localhost` scope entry;
   - `example.org` remains rejected as out-of-scope.

Still required before any live scanner-like/scripted runner:

- Confirm the exact <bug-bounty-platform> program rules/scope still allow the target and technique.
- Keep `--dry-run` for automation readiness checks unless the operator explicitly approves a narrow live runner.
- Do not expand scope/config or run scanners based only on this dry-run fix.

## Future bundle improvement rule

When updating any `modules/bundles/*.md` used for live bounty planning, add or verify these fields:

```text
Live bounty prerequisites:
Blocked live states:
Minimum live evidence:
Account/role prerequisites:
State-changing risk:
Report-readiness threshold:
```

Candidate bundles that cannot answer these fields should stay local-lab/reference-only and must not be used directly for live target-touching work.
