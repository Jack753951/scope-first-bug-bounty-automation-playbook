> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 5A Report-Readiness Checklist

Status: active checklist
Date: 2026-05-23
Purpose: convert local-lab proof packets or authorized live-target evidence into submit/not-submit decisions.

## Quick verdict

```text
Candidate:
Target/scope:
Vulnerability class:
Current status: candidate / verified-local / verified-authorized-live / not-submit
Recommended action: submit / do not submit / gather one more control / ask operator
```

## Required checks

| Check | Pass/Fail/Unknown | Notes |
| --- | --- | --- |
| In-scope asset/action | | |
| Test method allowed by rules | | |
| Uses test accounts/data only | | |
| No prohibited automation/rate behavior | | |
| No forbidden payload class | | |
| No sensitive data retained | | |
| Reproducible with bounded steps | | |
| Positive evidence present | | |
| Negative controls present | | |
| Impact crosses real security boundary | | |
| Not only self-impact/self-XSS/low-value behavior | | |
| Duplicate/known-issue checked where possible | | |
| Evidence redacted/minimized | | |
| Remediation guidance possible | | |

## Impact framing

Answer in plain language:

```text
Who can exploit it?
What privilege/account/tenant boundary is crossed?
What can be read/changed/triggered?
What is the realistic business/user risk?
What conditions or limitations reduce impact?
What did we avoid doing for safety?
```

## Evidence minimum by class

### Access control / IDOR / role separation

```text
Account A role and allowed baseline
Account B/admin/owner baseline if relevant
Unauthorized access/action by lower-privilege or wrong-tenant actor
Separate negative/secure control
Object/tenant ownership proof with redacted IDs
No real user data retained
```

### XSS

```text
Safe marker payload
Browser/runtime proof when claiming execution
Origin/path/session context
Negative/control artifact
No cookie theft, keylogging, account takeover, or victim deception
```

### File read / traversal / XXE

```text
Allowed/safe marker or synthetic test file
Wrong-path/no-entity control
No real secret files or sensitive records
Clear server-side behavior proof
Scope explicitly allows this class if live target
```

### SSRF/callback

```text
Scope explicitly allows callback/OAST/tunnel
DNS-only or lowest-impact callback where possible
Unique marker and timestamp
Callback source/context label
No metadata/internal scanning unless explicitly allowed
```

### RCE / command injection / deserialization

```text
Only if explicitly allowed
Benign marker command/function only
No shell persistence, no reverse shell, no secret read, no lateral movement
Pre/post health and cleanup
Human confirmation gate recommended
```

## Submit template

```text
Title:
Summary:
Affected asset:
Scope reference:
Severity rationale:
Steps to reproduce:
Expected result:
Actual result:
Impact:
Evidence:
Limitations/safety notes:
Suggested remediation:
```

## Not-submit reasons

Common valid reasons:

```text
out of scope
program excludes class
insufficient impact
self-only effect
needs prohibited action
not reproducible
only scanner/banner/version clue
duplicate/known accepted risk
insufficient authorization/account setup
unsafe evidence would be required
```

Record not-submit decisions; they are useful negative evidence.
