> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Controlled Lab Semi-Automated Calibration

Use this pattern when an authorized bug-bounty/security-testing platform is ready to move beyond offline/dry-run workflows but should not yet touch real bug-bounty targets.

## Placement

Insert this as a dedicated Phase 4A-style milestone after offline/dry-run MVP closeout and before any real authorized bug-bounty private beta.

Recommended sequence:

1. Offline/dry-run MVP closeout.
2. Controlled lab semi-automated calibration.
3. Lab-to-report workflow trial.
4. One-program authorized bug-bounty private-beta planning.
5. Real authorized bug-bounty controlled execution.

Do not fold lab live activation into the offline phase. A lab is safer than a public target, but it still introduces live-ish behavior: real HTTP services, real tool output, real candidate findings, and real human verification decisions.

## Authorized target classes

Only proceed after explicit operator selection and scope documentation for one of:

- local lab controlled by the operator;
- intentionally vulnerable local app;
- CTF/training platform instance with explicit scope;
- user-owned asset explicitly designated for lab testing.

Examples to consider later: OWASP Juice Shop, DVWA, WebGoat, PortSwigger Web Security Academy labs, HackTheBox/TryHackMe machines with explicit lab scope.

## Required operating mode

Keep it semi-automated, not autonomous:

1. Operator selects the lab target and exact scope.
2. Record a narrow lab scope/rules artifact separate from real program scope.
3. Treat activation as T4 by default; escalate to T5 if credentials, persistence, callbacks, destructive behavior, external services, production assets, scheduler/CI, proxy/pivot/transport, or secrets are involved.
4. Run only inside the approved lab scope.
5. Automation emits candidate findings only.
6. Agent/Hermes review checks false positives, evidence shape, redaction, and report-readiness gaps.
7. Human operator decides whether to continue, verify manually, discard, or refine scripts.
8. Nothing is submitted externally and nothing is marked confirmed by automation alone.

## Calibration goals

Measure workflow quality, not vulnerability count:

- scope gates deny out-of-lab/public targets;
- rate limits, timeouts, kill switch, audit logs, and stop conditions are understandable;
- scanner/module output can be triaged without excessive noise;
- candidate findings carry enough evidence for impact reasoning;
- evidence redaction blocks cookies, tokens, secrets, loot, sensitive payloads, and proprietary data;
- report-readiness gates block immature findings;
- manual verification checklist gaps become backlog items;
- scripts expose structured output, stable errors, retry/timeout behavior, and audit provenance.

## Exit criteria

Close the phase only when there is:

- at least one end-to-end candidate-only lab workflow packet;
- proof that out-of-lab targets are denied;
- an audit trail of what ran, when, and under which lab scope;
- a false-positive/noise assessment;
- manual verification checklist updates;
- report-readiness observations;
- script/workflow fixes identified before real-program planning;
- confirmation that no real bug-bounty target, production target, credentials, loot, or submission path was touched.

## Pitfalls

- Do not call this a real bug-bounty beta; it is a calibration bridge.
- Do not optimize for number of findings; optimize for safe workflow evidence.
- Do not let lab success skip real-program scope/rules review.
- Do not allow scheduler/CI, callbacks/OAST, proxy/pivot/tunnel, exploit chaining, brute force, fuzzing, credential handling, loot collection, automatic confirmation, or report submission unless a later explicit reviewed lab-only boundary authorizes a narrow case.
