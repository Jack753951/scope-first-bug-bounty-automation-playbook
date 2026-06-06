> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Broad operator authorization -> bounded live-bounty test matrix

Use when the operator says something like: "只要確認 scope 合法就做所有授權的可能測試" / "once scope is legal, do all authorized tests."

Do not interpret this as permission for every technical capability. Convert it into a matrix of tests that are simultaneously:

1. explicitly or reasonably allowed by the program policy;
2. inside exact selected scope and mirrored into the repo scope gate;
3. compatible with the current project safety profile / lane;
4. executable with owned/authorized accounts and no secret/PII retention;
5. paired with stop conditions and candidate/no-finding/report-ready labels.

## Required sequence

1. Confirm exact program asset(s) and add only the minimal selected host/path-equivalent supported by the repo gate to `config/scope.txt`.
2. Run an in-scope dry-run and an out-of-scope negative control, e.g. selected host should pass and `https://example.org/` should fail closed.
3. If the dry-run passes only the initial target gate but later scanner-style stages drop a full URL as host-only context, treat that as acceptable only for a manual/browser first lane. Do not treat it as scanner automation readiness.
4. Update `programs/<slug>/scope.json`, `handoff/<slug>_phase5a_dry_run_packet_<date>.md`, navigation, active queue, and accepted changes.
5. Build a first-flow test matrix before opening the target in noVNC/browser.
6. Pause on policy-specific identity requirements (email alias, researcher header, proxy setup) before account creation/login.

## Matrix shape

| ID | Test | Method | Evidence | Stop/status |
|---|---|---|---|---|
| T1 | Signup/login reachability | Manual noVNC browser | Redacted page labels/screenshots | Stop on CAPTCHA, bot block, account warning |
| T2 | Researcher identity compliance | Alias or exact policy header | Record strategy only, not email/header secret values | Block if neither identity route is ready |
| T3 | Session boundary basics | Normal UI login/logout/session observation | Authenticated vs unauthenticated state notes | No brute force/repeated login abuse |
| T4 | Owned profile/account map | Normal UI navigation | Path inventory and empty-state table | No non-owned data or sensitive-field retention |
| T5 | Workspace/tenant empty-state map | Normal UI only | Object family inventory | No workflow execution, run-script, integrations, webhooks, API keys/secrets |
| T6 | Closeout | Handoff only | `surface_only` / `candidate` / `no_finding` | No report submit without report-readiness gate and operator approval |

## Explicitly separate later-plan items

Put these in a separate "later only" table unless policy and operator give a narrow plan:

- scanner/fuzzer/DAST;
- DoS/rate-limit testing;
- OAST/callbacks/webhooks;
- integrations or third-party app connections;
- workflow execution / run-script features;
- API-key or secret creation/storage;
- cross-tenant or Account B tests;
- non-owned data access;
- report submission.

## Researcher header pitfall

Do not assume the header name. Copy the program's exact wording into the scope packet. For the <program-redacted> VDP case, the observed policy wording used:

```text
X-HackerOne-Research: [H1 username]
```

not `X-HackerOne-Researcher`. If using browser-only with a HackerOne email alias, prefer the alias route for the first flow to avoid proxy/header setup complexity.