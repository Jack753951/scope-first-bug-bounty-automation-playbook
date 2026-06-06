> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Active Testing / Module Risk-Tier Policy Pattern

Use when a cybersecurity automation project needs to distinguish valid bug-bounty pentesting methods from premature or unsafe automation.

## Core lesson

Do not describe active/payload-capable scripts as generically "excluded" or "banned" when the long-term product goal is authorized bug-bounty automation. The better policy language is:

- pentesting techniques are supported only through explicit authorization, scope/program rules, risk tiers, execution modes, candidate-only outputs, and review/operator gates;
- unauthorized, unscoped, unreviewed, or automatically-confirming attack automation is prohibited;
- active testing is deferred until the platform has the gates that make it safe.

## Recommended execution modes

- `offline`: local fixtures/schemas/handoff only; no target interaction, network clients, scanner/module execution, callbacks, or target tooling.
- `dry-run`: plans and validates policy/artifact contracts without touching a target. Never treat dry-run as live authorization.
- `planned`: produces a live plan for an authorized target/technique but does not execute target-touching behavior.
- `live`: sends requests or interacts with an authorized target; requires global scope, program rules, technique allow, rate/window controls, audit logging, and the applicable review/operator approval.

## Recommended module risk tiers

- Tier 0: offline docs/fixtures/contracts/validators. T0-T3 review depending on contract impact.
- Tier 1: passive/low-risk observation such as headers, TLS/cert metadata, CSP/CORS, robots/security.txt. Live use still requires scope and program gates.
- Tier 2: non-destructive triage probes such as bounded benign template checks, low-volume parameter reflection, and non-invasive scanner templates. Candidate-only output.
- Tier 3: vulnerability verification workflows such as XSS, SQLi, SSRF, IDOR, file upload, auth/session/reset flows, and CVE-specific exploit-shaped checks. Live use requires narrow approval and manual/agent verification before confirmation.
- Tier 4: high-risk/intrusive/callback-capable testing such as fuzzing, brute force, OAST/callback, aggressive PoCs, state-changing tests, proxy/pivot/tunnel/relay/reverse-listener behavior. Requires explicit narrow operator approval, program-rule allow, testing window, stop conditions, and audit logging.
- Tier 5: prohibited/out-of-platform behavior such as credential theft, malware, stealth persistence, destructive actions, secret/PII/loot exfiltration, evasion, unauthorized access, unauthorized pivoting, bypassing gates/rate limits, or automatic confirmed-finding promotion.

## Candidate-only output rule

Automation may emit candidate/triage states such as:

- `candidate`
- `needs_verification`
- `blocked`
- `not_ready`
- `reviewer_decision_required`
- `not_executed`

Automation must not emit confirmed/exploited/report-ready vulnerability claims without human or agent-assisted verification, evidence review, impact analysis, remediation guidance, and retest notes.

## Example-fixture clarification pattern

When examples include `automation_permitted: true` to test allow paths, add a local README or equivalent clarification:

- `_examples/` is examples/offline regression fixtures only and never a real program slug namespace.
- `automation_permitted: true` under `_examples/` is test-only and never live authorization.
- fixtures should use reserved/documentation-safe hosts/IPs and no secrets, customers, bounty-only details, credentials, OAuth, tokens, or private authorization records.
- real programs belong under `programs/<program-slug>/scope.json` and still require global scope, program rules, technique allow, rate/window controls, audit logging, and required review/operator approval.

## Safe sequencing

Before live activation, prefer:

1. clarify examples/fixtures and test-only automation flags;
2. define risk-tier policy in docs;
3. only later add risk-tier fields/validators to module manifests under T3/T4 review;
4. build recon-to-runner bridges dry-run-only first;
5. use lab-only controlled live activation before real bug-bounty private beta.
