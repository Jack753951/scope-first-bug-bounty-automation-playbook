> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <program-redacted> VDP Phase 5A dry-run packet

Status: policy_intake_complete / target_touching_blocked_pending_operator_confirmation
Date: 2026-05-25
Program: `<program-slug>` — <program-redacted> (VDP)
Program URL: `https://<bug-bounty-platform>.com/<program-slug>`
Source read: <bug-bounty-platform> program JSON endpoint `https://<bug-bounty-platform>.com/<program-slug>?type=team`
Boundary: policy/metadata read only. No request was made to `login.<program-redacted>.com` or any <program-redacted> target asset. No account creation, no scan, no fuzz, no exploit, no report submission.

## 1. Authorization source

Public <bug-bounty-platform> VDP policy page, submission state observed as open in the public program metadata.

Directory/program metadata observed:

```text
name: <program-redacted> (VDP)
handle: <program-slug>
submission_state: open
resolved_report_count: 2
triage_active: true
offers_bounties: not observed as enabled in fetched program detail
```

This is sufficient for policy intake only. Target-touching still requires exact scope confirmation and project scope-gate setup.

## 2. Key policy facts observed

The policy asks researchers to use these paths for new account signup/login:

```text
https://login.<program-redacted>.com/research/signup
https://login.<program-redacted>.com/research/login
```

The policy says researchers must use either:

```text
<researcher-alias-email>
```

or add this HTTP header when testing:

```text
X-<bug-bounty-platform>-Research: [H1 username]
```

The policy says:

- Do not disclose the vulnerability outside of the VDP.
- Do not violate any laws.
- Do not disrupt services, including DoS/DDoS.
- Do not access, modify, or destroy accounts/data that do not belong to you.
- Users can sign up for a free account through the website.
- Researchers using gmail or non-<bug-bounty-platform> alias without the required header may be subject to account deletion and possible program exclusion.
- Reports should include detailed reproducible steps.
- Submit one vulnerability per report unless chaining is needed for impact.
- Duplicates are triaged for the first fully reproducible report.
- Only interact with accounts you own or with explicit permission.

Policy impact guidance emphasizes real-world impact, including:

- privilege escalation;
- sensitive information disclosure;
- ability to affect resources not owned by the tenant/team.

The policy explicitly notes <program-redacted> Tenant Owners have full control over resources within their own tenant. For the run-script feature, it asks researchers to assess whether team/tenant isolation can be compromised or escaped before submitting.

## 3. Out-of-scope / blocked items

Explicitly out of scope from policy:

```text
HTTPS / TLS security headers suggestions
Direct testing of 3rd parties
SPF / DMARC / DKIM / DNSSEC suggestions
Banner/version disclosure
Social engineering / phishing / spam
```

Explicitly forbidden or blocked for this first lane:

```text
DoS/DDoS or service disruption
Access/modify/destroy non-owned account/data
Public disclosure outside VDP
Scanner/fuzzer/DAST
Rate-limit testing
External callbacks/OAST/webhooks
Third-party integrations
Workflow execution
Run-script feature testing
Secrets/API key creation or storage
Cross-tenant/team access attempts without owned-account controls
Tenant/team invitations or other-user interaction
Public sharing/publishing
```

The last group is a project safety restriction for first-lane practice, even where the policy may allow later bounded tests.

## 4. Scope artifact

Created draft scope file:

```text
programs/<program-slug>/scope.json
```

Selected assets pending operator confirmation:

```text
https://login.<program-redacted>.com/research/signup
https://login.<program-redacted>.com/research/login
login.<program-redacted>.com
```

Reference-only policy/documentation URLs from the policy:

```text
https://www.<program-redacted>.com/docs/quickstart/
https://www.<program-redacted>.com/api/welcome/
https://www.<program-redacted>.com/docs/actions/tools/run-script/
https://www.<program-redacted>.com/blog/python-<program-redacted>-how-to-guide/
https://www.<program-redacted>.com/security/
```

These reference URLs are not selected test targets for the first lane.

## 5. Config/scope gate status

Current status:

```text
added_to_config_scope
operator_confirmed_scope_gate_on_2026-05-25
dry_run_gate_passed_for_login_tines_com
out_of_scope_control_failed_closed_for_example_org
```

Minimal entry added to `config/scope.txt` after operator confirmation:

```text
login.<program-redacted>.com
```

Optional stricter future improvement: if the repo gate gains path-level URL entries, add the two exact research URLs instead of host-level only.

## 6. Dry-run gate plan

After operator confirmed adding `login.<program-redacted>.com` to `config/scope.txt`, Hermes ran:

```bash
HACKLAB="$PWD" ./recon.sh --dry-run --program <program-slug> --policy-mode dry-run https://login.<program-redacted>.com/research/login
HACKLAB="$PWD" ./recon.sh --dry-run --program <program-slug> --policy-mode dry-run https://example.org/
```

Observed result:

```text
https://login.<program-redacted>.com/research/login: safe_target PASS context=initial_target reason=in scope; dry-run complete; no network scanner stages executed.
https://example.org/: safe_target FAIL context=initial_target reason=not in scope; exit 1.
```

Note: dry-run later stage host-only filters dropped the full URL for scanner-style stages (`URL not allowed in host-only context`), which is acceptable for this manual first lane because scanner-like automation remains blocked. The initial authorization gate is usable for the selected host, and out-of-scope control fails closed.

This still proves only dry-run readiness, not permission for scanning/automation.

## 7. First-lane hypothesis

Lane:

```text
researcher-account auth/session/profile/workspace empty-state surface map
```

Execution style:

```text
manual Kali/noVNC browser
low-speed
one account only
normal UI only
no scanner/fuzzer/exploit
no workflow execution
no integrations/webhooks/callbacks
```

Expected useful result:

```text
no_finding or surface_only
```

Possible candidate only if clearly observed within owned account boundaries:

```text
unexpected auth/session inconsistency
sensitive owned-account disclosure
tenant/team isolation boundary signal
privilege/role inconsistency inside owned tenant
```

No cross-tenant/access-control finding can be claimed without owned Account B / second tenant / explicit test-account guidance and a separate plan.

## 8. Account/session handling decision

Operator handles:

- <bug-bounty-platform> username/alias choice;
- email verification;
- CAPTCHA/anti-abuse prompts;
- OTP if any;
- local login/session actions.

Hermes records only labels such as:

```text
Account A
<program-redacted> researcher account
owned tenant/team
```

Do not store:

```text
email address
password
OTP
cookies
tokens
API keys
secrets
PII
```

Header decision:

- Best: use <bug-bounty-platform> email alias for signup if operator has it available.
- If not using the alias: configure `X-<bug-bounty-platform>-Research: [H1 username]` via Burp/ZAP before target-touching requests.
- Browser-only work without alias/header is risky per policy because non-<bug-bounty-platform>-domain accounts without header may be deleted/excluded.

## 9. Stop conditions

Stop immediately on:

- policy ambiguity;
- CAPTCHA/bot detection/account warning;
- request for payment, phone, KYC, or unusual verification;
- any third-party data;
- accidental access to non-owned resources;
- workflow execution prompt;
- integration/webhook/API key/secret flow;
- rate limiting or service errors;
- need for Account B / second tenant;
- anything that looks like DoS, spam, phishing, or external callback behavior.

## 10. Current blockers

Before target-touching:

1. Operator confirms whether to proceed with <program-redacted> VDP.
2. Operator provides/chooses <bug-bounty-platform> handle or confirms alias/header strategy without storing secrets.
3. Operator confirms adding `login.<program-redacted>.com` to `config/scope.txt`.
4. Dry-run gate in-scope/out-of-scope pair passes.
5. If using header instead of alias, proxy/header setup must be ready before requests to <program-redacted> assets.

## 11. Report-readiness gate

No report packet should be generated unless all are true:

- exact asset/action is in scope;
- account/data is owned or authorized;
- evidence is reproducible and minimal;
- there is real-world impact beyond normal Tenant Owner control;
- no forbidden actions were used;
- no sensitive data is retained;
- positive and negative controls are meaningful;
- Hermes synthesis says `report_ready`;
- operator explicitly approves submission.

## 12. Authorized test matrix for first complete-flow practice

Interpretation of operator instruction: "do all authorized possible tests" means enumerate and execute all tests that are both (a) allowed by <program-redacted> policy and (b) safe under the project first-lane profile. It does not authorize scanners/fuzzers/DAST, DoS, callbacks, integrations, workflow execution, run-script testing, cross-tenant testing, non-owned data access, or report submission.

Authorized now after scope gate:

| ID | Test | Method | Evidence | Stop / status |
|---|---|---|---|---|
| T1 | Research signup/login reachability | Manual noVNC browser only | Page labels/screenshots with secrets redacted | Stop on CAPTCHA, account warning, bot block, unusual verification |
| T2 | Researcher identity compliance | Use H1 alias, or proxy header before requests | Record alias-vs-header strategy only, no email value | If neither alias nor header ready, blocked_operator_action |
| T3 | Session boundary basics | Login/logout/session expiry observation via normal UI | Redacted notes: authenticated vs unauthenticated states | No brute force, no repeated login abuse |
| T4 | Owned profile/account surface map | Normal UI navigation | Path inventory and empty-state table | No non-owned data, no sensitive fields retained |
| T5 | Workspace/tenant empty-state map | Normal UI only | Object families visible from owned empty tenant | No workflow execution, run-script, integrations, webhooks, API keys/secrets |
| T6 | Report/no-finding closeout | Handoff only | candidate/no_finding/surface_only classification | No report submit unless report-readiness gate passes and operator approves |

Potential later only with separate plan:

| Test | Additional prerequisite |
|---|---|
| Team/tenant isolation | owned Account B / second tenant or program guidance |
| API checks | explicit chosen endpoint, docs review, request budget, no secrets retained |
| Workflow/run-script boundary | separate high-risk review; likely not for first practice flow |
| Integration/webhook/OAST behavior | explicit program permission and operator approval |

## 13. Next safe action

Proceed to manual noVNC run only after operator confirms researcher identity strategy:

```text
A. <bug-bounty-platform> email alias, preferred for browser-only first flow
B. Non-alias email plus configured X-<bug-bounty-platform>-Research header through proxy
```

If A is selected, open noVNC and let operator perform signup/login/verification locally. Hermes will observe/summarize only redacted surface labels and stop on any gate condition.
