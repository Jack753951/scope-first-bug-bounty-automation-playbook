> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Authorized Live-Target Dry-Run Template

Status: active template / no target authorized by this file
Purpose: move a research lab from local-proof platform to controlled
authorized-assessment readiness without automatic public/live target touching.

## Boundary

This template does not authorize testing. It only defines what must be
collected before an agent, tool, or human operator touches a live/real target.

Default until completed and approved:

```text
blocked-awaiting-scope
```

Hard blocks unless explicitly allowed by the scope package:

```text
public/live target probing
broad scanning
credential theft
real exfiltration
persistence / stealth / malware / evasion
DoS / stress / rate-limit testing
state-changing destructive tests
external callback / OAST / tunnel
payment / abuse flows
real user data collection
report submission
```

## 1. Scope package

Fill this before target-touching work.

```text
Target/program name:
Authorization/program URL:
Operator-provided authorization evidence location:
Target URLs / apps / APIs:
Product / version if known:
In-scope assets:
Out-of-scope assets:
Allowed vulnerability classes:
Forbidden vulnerability classes/actions:
Rate limits:
Testing time window:
Notification/contact rules:
Allowed automation level:
Allowed external callback / OAST / tunnel:
Allowed state-changing actions:
Destructive test permission:
Test account availability:
Test data availability:
Evidence redaction rules:
Report submission channel:
Duplicate / known-issue guidance:
```

If any line is unknown and materially affects safety, ask the operator before
proceeding.

## 2. Target map

Keep this compact. The goal is navigation, not exhaustive crawling.

```text
Primary app/API:
Authentication model:
Account roles available:
Organization/tenant model:
High-value flows:
Known integrations/webhooks/import/export:
File upload/download surfaces:
Admin/team/invite/billing surfaces:
Mobile/API/GraphQL surfaces:
Client-side artifacts:
Docs/API references:
```

## 3. Role/account matrix

Use throwaway accounts only.

| Account | Role | Tenant/org | Purpose | Allowed by scope? | Notes |
| --- | --- | --- | --- | --- | --- |
| A | normal/user | org-1 | baseline actor | TBD | |
| B | normal/user | org-1/org-2 | cross-user/tenant control | TBD | |
| C | admin/owner | org-1 | privileged baseline | TBD | |

## 4. Candidate lane selection

Choose one lane at a time.

| Candidate | Class | Why valuable | Scope status | Risk | Proof plan | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| | access control / IDOR / auth / upload / XSS / SSRF / other | | in-scope / unknown / blocked | low/med/high | | test / defer / reject |

Preferred first live-target lanes:

```text
access control / IDOR
auth/session role separation
file exposure / metadata leakage
safe XSS marker if allowed
upload retrieval/validation if allowed
```

High-risk lanes require explicit extra approval:

```text
SSRF with callback / OAST
path traversal file read
RCE / command injection
deserialization
payment / business-abuse flows
anything destructive or state-changing outside throwaway data
```

## 5. Proof plan

For the selected single lane:

```text
Hypothesis:
Security boundary:
Attacker preconditions:
Accounts/roles used:
Exact endpoints/actions:
Positive proof:
Negative controls:
Safe marker/data:
Expected impact if confirmed:
Rate/request budget:
Rollback/cleanup plan:
Stop conditions:
```

Stop immediately if behavior crosses the approved scope or requires an
unapproved action.

## 6. Evidence packet

Use minimum necessary evidence. Redact by default.

```text
Title:
Classification:
Affected asset:
Scope reference:
Timestamp / timezone:
Accounts / roles:
Requests / responses summary:
Screenshots / DOM / logs:
Positive evidence:
Negative controls:
Impact statement:
Limitations:
Redactions applied:
Submit / not-submit decision:
```

Do not store tokens, passwords, API keys, private user data, or raw sensitive
records. Use `[REDACTED]` when unavoidable in summaries.

## 7. Report-readiness gate

A candidate is report-ready only if all are true:

```text
scope explicitly allows this test
impact affects a meaningful security boundary
steps are reproducible with bounded requests
evidence uses test accounts/data or redacted minimal data
negative controls rule out false positive
program policy does not exclude this issue
no prohibited actions were used
limitations are stated honestly
```

If not report-ready, write `not_submit_reason` and keep the learning artifact.

## 8. Output files for a dry-run

Use a dated folder or handoff prefix:

```text
<artifact-dir>/<target-alias>_scope_interpretation_YYYYMMDD.md
<artifact-dir>/<target-alias>_target_map_YYYYMMDD.md
<artifact-dir>/<target-alias>_candidate_lanes_YYYYMMDD.md
<artifact-dir>/<target-alias>_evidence_packet_YYYYMMDD.md
<artifact-dir>/<target-alias>_report_decision_YYYYMMDD.md
```

Raw/redacted evidence should stay in an explicit artifact folder, not global
memory.
