> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# CTF-to-platform workflow tooling notes — 2026-05-18

Use this reference when converting CTF solving lessons into the cybersec lab's authorized-testing platform workflow.

## User intent captured

The user wants CTF challenges to serve two purposes:

1. validate the agent workflow under controlled scope;
2. improve vulnerability/weakness-class recognition, not merely collect flags.

This means a future session should evaluate both the technical solution and the process lesson:

- Did blind triage correctly infer the class?
- Did Kali handle external services/tools?
- Was the output accepted only after deterministic or oracle-backed verification?
- Did ambiguity trigger second review or research escalation?
- Did the lesson become a reusable checklist, template, verifier, or note?

## Escalation criteria that emerged

Escalate from quick single-agent solving into research, second review, or multi-agent workflow when any of these appear:

- custom crypto/protocol/serialization/auth/access-control design;
- active oracle, stateful service, or per-instance secret;
- generic solver/tool timeout or ambiguous result;
- public PoC/writeup/template exists but may not match the live instance;
- candidate came only from UI success, scanner output, or external source;
- output format is abnormal or has multiple candidates;
- the next step requires new payload/attack design rather than passive interpretation;
- a conclusion would claim confirmed vulnerability/flag from indirect evidence.

Recommended routes:

```text
custom crypto + oracle + solver timeout
  -> crypto-structure review / literature search / independent agent review

scanner hit + exploitability claim
  -> Hermes safety gate + Claude/Cowork triage + minimal verifier design

verification script needed
  -> Codex implementation with metadata, dry-run, scope checks, and tests

new platform contract/schema/module/report output
  -> OSS Recon Gate + review tiering policy
```

## Output-side review checklist

Before accepting any flag/finding:

```text
[ ] Is scope/authorization clear?
[ ] Is this output a hint, candidate, or verified result?
[ ] Is there an independent invariant/checksum/parser/oracle validation?
[ ] Does the result match expected format and wrapper/terminator rules?
[ ] Could UI/checker/scanner output be a false positive?
[ ] Did a tool timeout/fail in a way that changes confidence?
[ ] If external writeups/PoCs were used, was the active instance verified?
[ ] Does this require second review before reporting/submission?
```

## Proposed reusable tooling slice

A safe next project slice is an offline/local CTF Artifact + Review Decision Skeleton.

Suggested files:

```text
scripts/ctf_prepare_challenge.py
scripts/ctf_review_decision.py
templates/ctf_verifier_metadata.yaml
tests/fixtures/ctf_review_decision/
```

Expected behavior:

- `ctf_prepare_challenge.py` creates `setting/local/ctf/<slug>/`, writes challenge metadata, and creates solve-note/checklist skeletons. It must not fetch external services by default.
- `ctf_review_decision.py` reads structured solver output and classifies it as `hint`, `candidate`, `verified`, or `needs_second_review`.
- The metadata template should initially remain non-binding unless reviewed into a versioned schema.
- Tests should cover normal flags, no-wrapper flags, UI-only candidates, multiple candidates, solver timeouts, and external-writeup-only answers.

Acceptance boundaries:

- offline/local by default;
- no live scans or target-touching automation;
- no scope/config/credential/loot/report/scheduler/deployment changes;
- if a future implementation touches schemas/contracts, run the OSS Recon Gate and review tiering policy first.

## Repository/Obsidian artifacts created in the validating session

These paths are session artifacts, not universal requirements, but they show the intended shape:

```text
handoff/ctf_workflow_validation_and_escalation.md
handoff/ctf_tooling_backlog.md
handoff/cowork_p2_17_direction_prompt.md
Cybersec Lab/01_Methodology/Scan-to-Verification Agent Review Pipeline.md
```

## Pitfalls

- Do not treat a public CTF writeup flag as valid for a live instance; use it as methodology only.
- Do not keep solving more challenges when the workflow lesson is already clear; turn the lesson into a checklist/backlog item.
- Do not commit raw challenge artifacts, attack transcripts, or secrets; keep them under ignored local paths unless explicitly promoted after review.
