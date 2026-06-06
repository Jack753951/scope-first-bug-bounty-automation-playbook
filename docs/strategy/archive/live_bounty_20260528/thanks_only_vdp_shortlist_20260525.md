> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Thanks-only / VDP first complete-flow shortlist

Status: passive shortlist only / no target touched
Date: 2026-05-25
Source: Hermes passive <bug-bounty-platform> program-directory lookup via `https://<bug-bounty-platform>.com/programs/search?...`
Boundary: no target request, no scope expansion, no account creation, no scan/fuzz/exploit, no report submission.

## Purpose

The operator wants a simpler live-bounty practice lane where the main goal is to walk the complete process once, not maximize payout. Prefer public VDP / thanks-only / response programs where expectations are lower, payment pressure is absent, and the project can practice:

1. exact policy/scope intake;
2. `programs/<slug>/scope.json` creation;
3. explicit `config/scope.txt` confirmation;
4. dry-run authorization gate pass/fail;
5. low-speed normal UI / owned-account surface map;
6. candidate/no-finding/report-readiness classification;
7. report packet or no-finding closeout;
8. post-proof consolidation.

This file is not authorization to test any target. Before any target-touching step, read the selected program page, extract exact scope/rules, create `programs/<slug>/scope.json`, confirm global scope entries with the operator, and run the dry-run gate.

## Selection criteria

Prefer:

- <bug-bounty-platform> submission state open;
- VDP / response / no listed bounty minimum in directory metadata;
- single-account-friendly web app or account surface;
- explicit program rules and safe harbor / disclosure policy;
- explicit researcher header or research login path if available;
- no need for payment, booking, KYC, seller, admin, upload, mobile MITM, OAST, or high-volume scanning.

Avoid for first full-flow practice:

- finance/banking/health/government/critical-infra unless the operator explicitly wants that program;
- hardware/IoT/product-firmware-only targets;
- broad infrastructure/CDN/cloud provider scope;
- targets requiring paid booking/order/payment to create evidence;
- programs whose policy mainly points outside <bug-bounty-platform> and may not support an in-platform report flow.

## Passive candidates

### 1. `<program-slug>` — <program-redacted> (VDP)

<bug-bounty-platform>: `https://<bug-bounty-platform>.com/<program-slug>`
Directory metadata observed: submission open, VDP/response style, no listed bounty minimum, triage active, low resolved count.
Why promising:

- Policy snippet explicitly mentions dedicated research signup/login paths:
  - `https://login.<program-redacted>.com/research/signup`
  - `https://login.<program-redacted>.com/research/login`
- This is useful for a complete process because the program appears to anticipate researcher accounts.
- Good fit for single-account surface mapping: signup/login/session/profile/workspace-like account state.

Risks / blockers:

- Must read full program page before action; likely requires specific header or session-layer rules.
- SaaS automation/workflow products may have state-changing automation features; first lane must avoid creating integrations, external callbacks, secrets, or workflow execution.

Suggested first lane:

- `single_account_auth_boundary_surface_map`
- Normal research signup/login only, if allowed.
- Map login/logout/session/profile/workspace empty state.
- Do not create external integrations, credentials, webhooks, workflows, or automation runs.

Recommended status: best first candidate if policy confirms free researcher signup and simple web scope.

### 2. `lovable-vdp` — Lovable VDP

<bug-bounty-platform>: `https://<bug-bounty-platform>.com/lovable-vdp`
Directory metadata observed: submission open, VDP/response style, no listed bounty minimum, triage active.
Why promising:

- Policy snippet explicitly says: avoid automated scanning, DAST, fuzzing APIs/endpoints; only interact with accounts you own or have permission for.
- That aligns well with the project’s manual, low-speed, owned-account-only posture.
- Likely has a modern web app/account surface suitable for simple single-account flow.

Risks / blockers:

- AI/app-builder surfaces may involve generated apps, uploads, prompts, or third-party integrations. Treat all generated-public-app, invite, publish, integration, webhook, and secrets flows as blocked until policy reviewed.
- First lane should not test cross-tenant/project access without Account B or explicit test-account guidance.

Suggested first lane:

- `single_account_auth_member_boundary_and_empty_project_surface`
- Signup/login/profile/account settings only.
- No public app publishing, third-party integrations, or generated-app sharing.

Recommended status: good second candidate if <program-redacted> signup is blocked.

### 3. `getyourguide_vdp` — GetYourGuide VDP

<bug-bounty-platform>: `https://<bug-bounty-platform>.com/getyourguide_vdp`
Directory metadata observed: submission open, VDP/response style, no listed bounty minimum, quick first response.
Why promising:

- Consumer web surface likely has login/profile/account settings and search/browse pages.
- Good for practicing report packet discipline and blocked payment/booking classification.

Risks / blockers:

- Travel/booking flows create payment/order/state-changing risk. For first full-flow practice, do not book, reserve, refund, coupon, wallet, payment, partner/supplier, or support flows.
- Single-account IDOR/BOLA will likely be blocked until an owned booking/object exists or program provides test guidance.

Suggested first lane:

- `single_account_profile_and_auth_boundary_surface_map`
- Read-only account/profile/session mapping; no booking/payment/order creation.

Recommended status: viable, but only if we accept a likely no-finding surface-map outcome.

### 4. `hack_the_box` — Hack The Box VDP

<bug-bounty-platform>: `https://<bug-bounty-platform>.com/hack_the_box`
Directory metadata observed: submission open, VDP/response style, no listed bounty minimum, quick first response, triage active.
Why promising:

- Security-training platform; operator/project context is familiar with training/lab platforms.
- Could be psychologically simpler than commerce/finance.

Risks / blockers:

- Policy snippet says official VDP Terms PDF is legally binding and must be read in full before testing.
- HTB has intentionally vulnerable content/labs/challenges, which can confuse target scope. Must not test challenge machines/content unless explicitly in scope.

Suggested first lane:

- Only if policy clearly permits normal account/profile/session surface testing on the platform itself.
- Avoid machines/challenges/labs, other users, teams, billing, academy/business/admin surfaces.

Recommended status: viable after careful terms review, not the simplest first pick.

### 5. `bose_vdp` — Bose (VDP)

<bug-bounty-platform>: `https://<bug-bounty-platform>.com/bose_vdp`
Directory metadata observed: submission open, VDP/response style, no listed bounty minimum, quick first response, triage active.
Why promising:

- Policy snippet mentions detailed reports and researcher headers like `X-<bug-bounty-platform>-Research: [H1 username]`.
- Suitable for practicing exact-header/scope intake and dry-run gate.

Risks / blockers:

- Consumer accounts may involve hardware/device/app/cloud interactions; first lane should avoid device pairing, mobile MITM, firmware, Bluetooth, upload, warranty/order/payment, and support flows unless rules explicitly allow.

Suggested first lane:

- Read-only account/auth boundary surface if web account signup is available and in scope.

Recommended status: backup candidate.

## Not recommended as first complete-flow practice

- `fastly-vdp`: infra/CDN/edge platform; too much critical-infra and customer-impact risk for first simple flow.
- `redis-vdp`: priorities include Redis Cloud, RCE, API flaws, cross-tenant data access; valuable but too high-impact for first simple lane.
- `recreation_gov_vdp`: likely booking/reservation/payment/state-changing risk.
- finance/banking VDPs such as ABN AMRO, Fifth Third, LPL, MUFG, Fidelity, Oportun: avoid for first practice.
- government/high-sensitivity VDPs such as DoD, Department of State, City of Los Angeles: avoid for first practice unless the operator explicitly chooses them.

## Recommended first pick

Recommended: `<program-slug>`.

Reason: It appears to provide researcher-specific signup/login paths, which gives us the highest chance of completing the whole process legally and cleanly without fighting normal consumer signup/account gates. The first lane can be very small:

```text
program: <program-redacted> VDP
lane: researcher-account auth/session/profile/workspace empty-state surface map
request style: manual browser/noVNC, low-speed, one lane
blocked: integrations, workflows, webhooks, external callbacks, secrets, API fuzzing, DAST, multi-account, public sharing
expected outcome: no_finding or candidate-only; practice full flow
```

## Full-flow checklist for the selected program

1. Passive policy intake
   - Read full <bug-bounty-platform> program page.
   - Capture in-scope assets, out-of-scope assets, allowed classes, forbidden actions, rate limits, headers, account policy, reporting rules.

2. Scope artifacts
   - Create `programs/<program_slug>/scope.json`.
   - Ask operator before adding exact assets to `config/scope.txt`.

3. Dry-run authorization gate
   - In-scope exact target dry-run must pass.
   - `https://example.org/` or other clearly out-of-scope target must fail.
   - Record `gate_fixed_dry_run_verified` only for dry-run readiness, not automation permission.

4. Operator/account gate
   - Operator handles CAPTCHA/OTP/email/phone locally.
   - Hermes records Account A label only; no secrets/PII.

5. First lane preview
   - Use `docs/strategy/live_bounty/proof_library_live_bounty_bridge_20260525.md`.
   - Choose a single low-risk lane, preferably auth/session/profile empty-state surface.

6. Execution
   - Manual/noVNC, low-speed, normal UI only.
   - No scanner/fuzzer/exploit/DAST.
   - Stop on policy ambiguity, account warning, bot detection, unexpected third-party data, or state-changing prompt.

7. Evidence and review
   - Write `handoff/<program_slug>_single_account_surface_map_<date>.md`.
   - Classify `no_finding`, `surface_only`, `candidate`, `blocked`, or `needs_second_account`.
   - Generate report packet only if report-readiness gate passes.

8. Consolidation
   - Run `scripts/post-proof-consolidation.sh --type live_surface_map --artifact <handoff> --dry-run`.
   - Update accepted_changes/current_navigation/active_strategy_queue/Obsidian if status changed.

## Next safe action

Open/read the selected program policy only, no target asset navigation yet. If operator agrees with the recommendation, start with `<program-slug>` policy intake and produce `programs/<program-slug>/scope.json` plus a dry-run packet before any account creation or target-touching step.
