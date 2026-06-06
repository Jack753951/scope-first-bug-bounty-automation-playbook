> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Live bounty autonomous workflow policy

Status: active project policy
Date: 2026-05-25
Owner: Hermes as project coordinator / safety gate / workflow owner
Scope: authorized bug bounty / VDP work in this repo
Boundary: does not authorize out-of-scope targets, scanners/fuzzers/DAST, exploit chains, callbacks, payment/upload/run-script/integration/cross-tenant testing, non-owned data access, or report submission without the specific gates below.

## Operator preference captured

The operator wants the cybersec lab to become more autonomous than a half-automatic assistant workflow. Hermes should act like the project owner: make safe decisions, execute authorized non-sensitive steps, and call the operator only when human input is truly needed or when a target/lane reaches a natural checkpoint.

## Default checkpoint model

Do not stop at every minor action if the next action is:

- within the exact program scope/rules;
- inside an already approved lane;
- low-speed/manual/browser-assisted or otherwise explicitly allowed;
- owned-account only;
- non-sensitive;
- reversible or read-only;
- already covered by the lane's stop conditions.

Checkpoint only when one of these occurs:

```text
lane_complete_or_exhausted
target_complete_or_parked
operator_action_required: auth / OTP / CAPTCHA / email / phone / local browser / payment / legal ambiguity
scope_or_policy_ambiguity
unexpected third-party data or sensitive data exposure
candidate could become report_ready
stronger technique needed: scanner / fuzzer / DAST / callback / upload / payment / run-script / integration / cross-tenant / non-owned data
report submission decision
```

When checkpointing, Hermes must state:

```text
why stopped:
what was completed:
current status label:
operator decision needed:
next autonomous action after decision:
```

## Autonomy levels

### A0 — Passive / documentation only

Hermes may do without asking:

- read public program policy and metadata;
- compare program rules;
- shortlist programs;
- read public docs, OWASP, PortSwigger, disclosed reports, OSS test cases;
- create scope drafts and handoff packets;
- update navigation/accepted_changes/Obsidian;
- run repo-local validation.

### A1 — Scope-gated dry-run only

Hermes may do after program policy facts exist and the operator has indicated the target/lane direction:

- add minimal exact host entries to `config/scope.txt` when the operator has clearly approved the program/lane;
- run `recon.sh --dry-run --program <slug> --policy-mode dry-run` in-scope/out-of-scope pairs;
- update scope artifacts and authorization-gate status.

A1 never means live scanning permission.

### A2 — Manual live target touch, owned-account, first lane

Hermes may proceed without per-click confirmation once:

- `programs/<slug>/scope.json` exists;
- exact target is in `config/scope.txt`;
- dry-run gate has passed in-scope and failed out-of-scope;
- identity/header/account strategy is ready;
- operator has completed any required auth/CAPTCHA/OTP/email locally;
- lane plan and stop conditions exist.

Allowed A2 examples:

- open official research signup/login path in Kali/noVNC;
- normal UI surface mapping;
- login/logout/session-state observation;
- owned profile/account/workspace empty-state mapping;
- path/object-family inventory from owned UI;
- redacted notes/screenshots.

### A3 — Bounded proof within owned resources

Requires a specific lane preview/review and may proceed only if explicitly within rules:

- harmless self-owned marker data;
- Account A/B checks where both accounts/tenants are operator-owned or program-provided;
- low-volume API checks against explicit endpoints with request budget;
- positive/negative controls with no non-owned data.

### A4 — High-risk or sensitive lanes

Always checkpoint before execution:

```text
scanner/fuzzer/DAST
DoS/rate-limit testing
callbacks/OAST/webhooks/tunnels
uploads or file-processing tests
payment/checkout/KYC/cash/refund
workflow execution
run-script execution
third-party integrations
API keys/secrets
cross-tenant tests without explicit owned-account controls
mobile MITM/rooted devices
admin/seller/partner surfaces without legitimate account context
report submission
```

## Preview/review grounding requirement

For nontrivial bug bounty preview/review, Hermes should use relevant public methodology and examples before executing or classifying:

- OWASP WSTG / ASVS controls;
- PortSwigger Web Security Academy labs;
- public <bug-bounty-platform> disclosed reports where relevant;
- GitHub Security Lab or vendor writeups;
- mature OSS project docs/test cases matching the feature shape;
- ZAP/Burp docs for safe proxy/header setup;
- Nuclei template metadata only as reference for expected evidence, not as permission to run scans.

The handoff should record the useful references when they influenced the plan or review.

## Application to current <program-redacted> VDP lane

Current status:

```text
program: <program-slug>
scope gate: login.<program-redacted>.com added, dry-run pass; example.org fail closed
current autonomy level: A2 pending identity strategy / operator-local auth
```

Hermes may proceed autonomously through the <program-redacted> first-lane surface map after the operator either:

```text
A. uses <bug-bounty-platform> email alias for browser-only flow, or
B. sets up X-<bug-bounty-platform>-Research header via proxy before target-touching.
```

During <program-redacted> A2 execution, Hermes should not stop for every page. Stop only for the checkpoint conditions above or once the lane is complete/exhausted.
