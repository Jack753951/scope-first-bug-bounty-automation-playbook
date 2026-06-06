> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Proposal — Agent-driven access-control hunt playbook (niche: SaaS/API authorization)

Date: 2026-05-29
Author: Claude (consultant)
Status: **PROPOSAL — operator review**. Methodology design for you to read/place; does not change `SAFETY.md` or any scope.

## Why this niche

Pick ONE niche and let agents run it deep. Recommended: **authorization / access-control bugs on multi-tenant SaaS/API products** — BOLA/IDOR, broken function-level authz, role & invite-lifecycle boundaries, tenant isolation, business-logic authz.

Reasons it fits *you specifically*:

1. **Your evidence already concentrates here.** Lab bundles (BOLA, role separation, IDOR object ownership) + your real live lanes (<program-redacted>, <program-redacted>) were all access-control / A-B role work. You are not starting cold.
2. **It needs owned-account A/B testing, NOT scanning/fuzzing.** So the entire pipeline runs **inside your current `SAFETY.md` with zero relaxation** — no DAST/OAST/fuzz, no aggressive automation. The fuzz-relaxation proposal is *not* required for this.
3. **Low automated-competition / low duplicate.** XSS and recon-spray are saturated by bots. Logic/authz bugs are manual and reasoning-driven — exactly where agent-assisted hypothesis volume beats lone manual hunters, and where AI-spam crowds don't compete well.
4. **Hallucination-resistant.** The verdict is deterministic: with two real owned accounts, does A reach B's object — yes or no. Agents can't fake that past human re-check.

## Division of labor (the core idea)

| Role | Does | Never does |
|---|---|---|
| **Agent(s)** | reading, enumeration, hypothesis generation, disclosed-report mining, bounded A/B execution on owned data, report drafting | submit; touch secrets/OTP/cookies; act outside scope; declare a finding "real" |
| **Operator (you)** | scope approval, owned-account provisioning + auth gates, final submission | the tedious reading/enumeration the agent should do |
| **Human-verify (you, by hand)** | manually reproduce every candidate in two real sessions before it counts | trust an agent-claimed finding unverified |

The scarce resource is **your judgment**. Spend it only on Stage 0 approval, Stage 5 verification, Stage 7 submission. Agents do everything in between.

## The pipeline

### Stage 0 — Target selection (agent-heavy → operator approves)
Agent scans H1/Bugcrowd for SaaS/API programs and scores each on, in priority order:
1. **Can I obtain 2+ owned accounts?** (self-signup, sandbox, or invite) — this is your recurring park-cause; make it the FIRST gate, not a late surprise.
2. Policy explicitly permits owned-account testing.
3. Product has multi-role / multi-tenant features (teams, orgs, invites, RBAC, API tokens).
4. Program pays for access-control bugs.

Output: ranked candidates, each with the account-acquisition question already answered.
Gate: **operator** picks one, approves into `config/scope.txt` + `programs/<slug>/scope.json`.

### Stage 1 — Surface & object-model mapping (agent-heavy, passive/owned)
Agent reads public API docs, OpenAPI/Swagger, JS bundles, frontend routes, product docs → builds an **object × role × expected-access matrix**: every object type (invoice, user, workspace, webhook, export, file…), the endpoints that read/write it, and which role *should* reach it.
Pure reading → fits guardrails. Output: the access matrix.

### Stage 2 — Hypothesis generation (agent-heavy)
Agent cross-references the access matrix with **mined disclosed-report patterns** → emits a ranked queue of falsifiable A/B hypotheses, each in the form:
> "Account A (low-priv) attempts `<verb> <endpoint>` on Account B's `<object>` → **expected: DENY**. Negative control: A's own equivalent object → ALLOW."

Output: hypothesis queue, each item testable with a defined positive/negative control.

### Stage 3 — Owned-account provisioning (OPERATOR gate)
Operator creates/authenticates 2+ owned accounts spanning roles/tenants (A low-priv, B target), clears OTP/CAPTCHA/KYC. Agent never sees secrets.
**Reframe vs. your past lanes:** because Stage 0 already filtered for "accounts obtainable," this gate should clear, not park. Batch it.

### Stage 4 — Bounded A/B execution (agent, owned-data only)
For each hypothesis the agent records **three points**:
- baseline: A on A's own object → expected ALLOW
- positive control: B on B's object → confirms object exists
- cross-access: A on B's object → the test

Strictly owned synthetic data, low rate, in-scope, reversible, logged. No scanning/fuzzing.
Output: result matrix; flag every cross-access that unexpectedly SUCCEEDED = candidate.

### Stage 5 — Human verification (NON-NEGOTIABLE — you, by hand)
Manually reproduce each candidate in two real browser sessions. Confirm it's a true authz break, not: same-tenant-by-design, a misread status code, or agent hallucination. Capture clean redacted evidence.
This is your anti-AI-slop reputation gate. **Nothing advances without it.**

### Stage 6 — Report drafting (agent draft → you verify every claim)
Agent drafts from verified evidence: repro steps, impact, CVSS justification, scope ref, cleanup notes — using your existing `bugbounty_report_template.md`. You check each sentence against reality.

### Stage 7 — Final submission (OPERATOR gate)
You review and submit. Agent never submits. (Matches current `SAFETY.md`.)

### Feedback loop (compounding edge)
Every outcome (accepted / duplicate / N/A / no-finding) feeds back into Stage 2's pattern library and ranking. Over weeks the agent's hypothesis quality compounds — this is how you *manufacture* the pattern-experience you lack vs. top hunters.

## The metric that matters

Track **"hypotheses pushed to Stage 5 (human-verify) per week."** Finding the first bug is a numbers game; this number is your throughput on the volume axis where agents give you the edge. Aim to grow it weekly, not to chase a perfect single target.

## What this deliberately does NOT do

- No `SAFETY.md` change required (runs entirely within current rules).
- No fuzz/DAST/OAST/scanner/high-volume automation.
- No agent submission, no agent-declared findings, no secret handling by agents.

## Mapping to your repo

- Stage 0 output → `handoff/pending_intake.json` + `live_bounty_lane_queue.json`
- Stage 1–2 artifacts → `programs/<slug>/notes/`
- Stage 4 results → `programs/<slug>/findings/` (redacted) + evidence dirs
- Reusable hypothesis templates → `modules/bundles/`
- Lane status → `programs/<slug>/lane_state.json`
- Pattern library / feedback → `intelligence/program_briefs/`

## Operator decision

- [ ] adopt as primary hunt loop
- [ ] adopt with edits (note below)
- [ ] not now

Notes:
