> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Learning-stage local-lab safety-control pause

Use this reference when a cybersecurity learning workspace has an explicitly authorized, disposable/recoverable local lab and the operator corrects the workflow away from over-broad safety/process gates.

## Session lesson

The operator may want to pause the project's **internal** safety/tier/profile/review machinery during a learning stage because it has become too wide and blocks normal lab learning. This is not the same as removing external/legal/abuse boundaries.

Preferred interpretation:

```text
Pause over-broad internal process controls for the learning lab.
Keep external authorization and non-abuse red lines.
Act script-first in the local lab.
```

## How to act

For an explicitly authorized disposable local lab / intentionally vulnerable app:

- Do not category-ban mature offensive/security tools such as ffuf, Nikto, nmap, nuclei, ZAP, gobuster, wfuzz, Burp workflows, TLS scanners, fuzzers, or exploit-shaped/destructive lab scripts.
- Do not require a fresh risk tier, profile, heavy review, contract, schema, or OSS gate before each learning-lab execution.
- Prefer the loop:

```text
choose existing script/tool
run against local lab
cap obvious runaway behavior
gather local artifacts
check health/recover if needed
summarize candidate-only lessons
modularize useful combinations
repeat
```

- If the primary Kali/shared-folder path is temporarily unusable but the authorized local target is reachable from the host, continue from the host rather than stopping solely because the preferred execution surface failed. Record the execution surface and reason.

## Non-paused boundaries

These are not merely project-process controls and should remain binding:

- no public/unknown target interaction without explicit authorization/scope;
- no malware;
- no stealth persistence;
- no real credential theft;
- no real exfiltration of secrets/tokens/PII/proprietary data;
- no unauthorized pivoting/relay infrastructure;
- no evasion of legitimate controls;
- no automatic report submission;
- no automatic promotion from tool/scanner output to confirmed findings.

## Output semantics

Aggressive learning-lab execution can be allowed while conclusions stay conservative:

```text
tool output -> observation
observation -> possible vulnerability / candidate
candidate -> manual review needed
manual verification + evidence + impact -> report-ready only after separate decision
```

## Recording pattern

When applying this pause, create or update local project artifacts such as:

- `handoff/<phase>_learning_stage_safety_pause_<date>.md`
- `handoff/active_strategy_queue.md`
- `scripts/SCRIPT_INVENTORY.md`
- `modules/bundles/<bundle>.md`
- candidate-only `possible_vulnerabilities.md`

Do not store raw targets, loot, credentials, secrets, or transient scan artifacts in global memory.
