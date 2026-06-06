> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# H1 Fresh Target Triage — 2026-05-28

Status: active first-bounty candidate triage
Boundary so far: <bug-bounty-platform>/Intigriti policy and scope metadata only. No target testing, scanning, fuzzing, exploit, OAST/callback, account mutation, report submission, or non-owned data access.

## noVNC / browser route

Hermes confirmed the existing Kali/noVNC browser route works without operator action:

- noVNC reachable at `127.0.0.1:6080`.
- Kali Firefox is controllable through SSH + `xdotool`.
- H1 Opportunity Discovery is logged in and visible.
- Intigriti preview pages are accessible, but logged-in Intigriti policy requires account login/2FA and no local env-backed Intigriti credentials were found.

Temporary local helpers used for this pass:

- `tmp/invoke-kali-command.ps1`
- `tmp/fetch-kali-file-base64.ps1`

These are operational helpers only; do not treat as platform features unless promoted deliberately.

## Intigriti candidates

### <program-redacted> Public Bug Bounty — KILL for first-bounty lane

Public preview text captured through Kali Firefox:

- Program: `<program-redacted> Public Bug Bounty`.
- Status indicators visible: `Public`, `Suspended`, `Software`.
- Bounty range visible: Tier 2 `$100 - $5,500`.
- Program specifics: two-factor authentication required.
- Requires Intigriti login/sign-up to submit/apply.

Decision:

```text
KILL for first-bounty execution because program status is Suspended.
```

Notes:

- <program-redacted> remains useful as an API/search/permission research reference, but not as active first-bounty target while suspended.

### <program-redacted>.be Dedicated Bug Bounty Program — PARK / operator-login gate

Public preview text captured through Kali Firefox:

- Program: `<program-redacted>.be Dedicated Bug Bounty Program`.
- Status indicators visible: `Application`, `Open`, `Business & Professional Services`.
- Description says <program-redacted>.be moved to a new deployment called `W-One` and asks Intigriti community to test after internal pentest.
- Bounty ranges visible:
  - Tier 1 and Tier 2 both show low to exceptional ranges from `€25-€50` up to `€2,500-€5,000`.
- Requires Intigriti login/sign-up to submit/apply.

Decision:

```text
PARK until logged-in Intigriti policy is available.
```

Blocker:

- No local env-backed Intigriti credentials found.
- Full policy/scope/apply details require Intigriti login and likely 2FA.

## <bug-bounty-platform> candidates

### Private opportunity — <program-slug> — OPERATOR GATE before claim

Observed on H1 Opportunity Discovery:

- Section: `Available private opportunities (up to 1 per 30 days)`.
- Program visible: `<program-slug>`.
- Type: Bug Bounty Program.
- Tags visible: `Domain 7`, `AndroidPlayStore 1`, `IosAppStore 1`.
- Standard: Gold Standard.
- Reward visible: `$50 - $1k`.
- Metrics visible: `22` reports, `21` hackers/collaboration metric, `88%` response indicator.
- Button visible: `Claim your spot`.

Decision:

```text
PARK / OPERATOR GATE before claim.
```

Reason:

- Claiming may consume the scarce `up to 1 per 30 days` private opportunity slot.
- Do not click `Claim your spot` without operator approval.

### <program-redacted> Taiwan — strongest autonomous candidate from this pass

H1 policy page captured through logged-in Firefox.

Program facts:

- Program: `<program-redacted> Taiwan`.
- URL: `https://www.tw.<program-redacted>.com`.
- Program type: Bug Bounty Program.
- Launched: May 2026.
- Response efficiency: 97%.
- Highlights: Fast Payment, Gold Standard Safe Harbor, Top Response Efficiency, Managed by <bug-bounty-platform>, Collaboration Enabled, Includes Retesting.
- Average time to first response: 13 hours.
- Average time to triage: 1 day, 13 hours.
- Average time to bounty: 4 days, 22 hours.
- Average time from submission to bounty: 6 days, 11 hours.
- Average time to resolution: 3 weeks, 1 day.
- Last policy update visible: May 5, 2026.
- Rewards:
  - Critical: `$4,000 - $6,000`.
  - High: `$1,500 - $3,000`.
  - Medium: `$400 - $600`.
  - Low: `$50 - $200`.
  - Accepted Risk or Informational: `$0`.

Scope facts:

- H1 Scope CSV downloaded through Firefox and parsed locally.
- CSV path: `tmp/scopes_for_coupang_tw_at_2026-05-28_06_26_44_UTC.csv`.
- 47 scope rows.
- 45 URL assets in latest H1 CSV.
- Current repo `config/scope.txt` has only 10 <program-redacted> URL hosts; live execution must stay inside that subset unless operator updates whitelist.
- All parsed rows show:
  - `eligible_for_bounty=true`.
  - `eligible_for_submission=true`.
  - `max_severity=critical`.
- Asset types include URL, Apple Store app ID, and Google Play app ID.

High-interest scoped assets for first-bounty hypotheses:

```text
id.tw.<program-redacted>.com
member.tw.<program-redacted>.com
my.tw.<program-redacted>.com
myself.tw.<program-redacted>.com
cart.tw.<program-redacted>.com
checkout.tw.<program-redacted>.com
pay.tw.<program-redacted>.com
payment.tw.<program-redacted>.com
cash.tw.<program-redacted>.com
review.tw.<program-redacted>.com
fileupload.tw.<program-redacted>.com
fileupload-video.tw.<program-redacted>.com
partners.tw.<program-redacted>.com
ads-partners.tw.<program-redacted>.com
logs-partners.tw.<program-redacted>.com
rs-open-api.tw.<program-redacted>.com
developers.tw.coupangcorp.com
marketplace.tw.coupangcorp.com
helpseller.tw.coupangcorp.com
helpcenter-tw.coupangcorp.com
www.tw.<program-redacted>.com
tw.<program-redacted>.com
SUPERAPP (IOS)
SUPERAPP (AOS)
```

Visible scope exclusion facts:

- Anything else is out-of-scope, including infrastructure attacks.
- Core Ineligible Findings are out of scope.
- Infrastructure attacks/vulnerabilities are excluded.
- DoS attacks due to application vulnerabilities are excluded.
- Unlikely scenarios excluded:
  - attacks requiring jailbroken/rooted device;
  - attacks requiring Man-in-the-Middle or physical access to a user device.
- Social engineering excluded:
  - social engineering type vulnerabilities;
  - phishing attack using redirection.
- Other ineligible findings include:
  - CSRF with minor impact, e.g. logout;
  - improvements on password policies;
  - missing security headers;
  - internal IP or domain leakage;
  - error messages or version information;
  - issues requiring unlikely user interaction, e.g. self-XSS;
  - publicly known vulnerabilities.
- Already known issues / informational issues are excluded.

Visible Platform Standards deviation:

- IDORs with unpredictable IDs: reports without showing how those unpredictable IDs were obtained easily will not be considered valid.

Visible disclosure/program rules:

- Do not discuss the program or vulnerabilities, even resolved ones, outside the program without express consent.
- Follow <bug-bounty-platform> disclosure guidelines.
- Reports must be detailed and reproducible; non-reproducible reports are not eligible for reward.
- Submit one vulnerability per report unless chaining is needed to show impact.
- Duplicate reports: only first fully reproducible report is awarded.
- Multiple vulnerabilities caused by one underlying issue receive one bounty.
- Social engineering such as phishing/vishing/smishing is prohibited.
- Make a good-faith effort to avoid privacy violations, destruction of data, and interruption/degradation of service.
- Ask program team before submitting vulnerabilities on unscoped subdomains.
- Only interact with accounts you own or with explicit permission of the account holder.
- Publicly disclosed zero-days with official patch < 1 month are accepted case-by-case.
- Leaked credential reports are accepted only if verifiable and no prior response history; duplicate/previously addressed leaks are ineligible.
- Taiwan and Korea assets may share overlapping backend code; same fix across regions counts as one vulnerability report, first valid submission only.
- <program-redacted> reserves the right to determine researcher testing activity before awarding bounty.

Visible test plan:

- Users can sign up for a free account through the website when applicable.
- Use hacker email alias when testing: `<researcher-alias-email>`.
- Researchers should add HTTP header: `X-<bug-bounty-platform>-Researcher: [H1 username]`.

Preliminary target score:

```text
freshness: 3          # launched May 2026; scope rows updated Feb/Mar 2026; policy updated May 5
self_signup: 1        # free signup allowed when applicable, but exact account gates not yet tested
free_plan: 1          # likely user account possible, no purchase/payment path should be avoided
low_priv_control: 1   # unknown; consumer account likely, seller/partner roles may be higher friction
owned_object: 2       # carts/reviews/account objects likely possible, but not yet created
scope_clarity: 2      # H1 scope CSV clear, 47 eligible assets
operator_cost_low: 2  # H1 already logged in; target signup/OTP unknown
access_control_surface: 2 # account/cart/review/payment/member surfaces
api_or_direct_url_surface: 2 # many API/<program-name>/open-api hosts
Total: 16/23
```

Decision:

```text
EXECUTE_PREPARE_RUN_CARD, but do not touch target yet.
```

Best first bundles:

1. `auth-role-separation` around account/member/my/cart/review surfaces if low-priv/owned controls exist.
2. `object-ownership-idor` only if IDs are obtainable through owned flows and the report can show how IDs are obtained easily, due to IDOR deviation.
3. `api-ui-permission-mismatch` on cart/review/member/payment non-destructive owned objects.
4. `metadata-only-leak` around owned order/cart/review/account metadata only.
5. `upload-path-traversal-safe-marker` only on `fileupload*` if policy and owned upload object allow marker-only proof; otherwise PARK.

Hard stop before live execution:

- Do not touch target until run card is created and operator/safe gate confirms live target testing.
- Do not test payment, purchase, refunds, real orders, non-owned accounts, customer/seller data, rate limit, DoS, infrastructure, or social engineering.
- Do not submit report without final operator approval.

## Current recommendation

1. Do not claim <program-slug> yet; ask operator only if choosing to spend the private opportunity slot.
2. Park Intigriti <program-redacted> due suspended.
3. Park Intigriti <program-redacted> until Intigriti login/2FA policy gate is resolved.
4. Promote <program-redacted> Taiwan to the next run-card candidate because it is fresh, H1-authenticated, clear scope, reward-bearing, and already authorized in repo scope.
