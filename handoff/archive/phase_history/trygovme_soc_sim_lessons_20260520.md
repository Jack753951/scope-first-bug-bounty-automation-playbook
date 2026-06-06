> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# TryGovMe SOC Simulator Lessons — Evidence-Bucket Alignment

Date: 2026-05-20
Status: planning / workflow optimization
Source: operator-provided TryHackMe SOC Simulator feedback screenshots and summary breakdown
Boundary: documentation and future offline tooling backlog only; no live scans, no target interaction, no scope/config changes, no report submission, no credentials/loot handling.

## Why this lesson matters

The simulator run showed that a plausible adversary narrative is not enough. A report can correctly describe the broad chain while still scoring poorly if the stage evidence buckets do not match the reviewer/platform expectations.

Observed outcome:

- Hypothesis conclusion was correctly proven.
- Overall report narrative was directionally valid.
- Technique/tactic identification was very low because many stages used broad or mismatched ATT&CK mappings.
- IOC coverage was very low because the expected host/network indicators were distributed into different stage buckets than the initial timeline.
- Asset coverage was mixed because some stages required the execution host while others required the targeted/affected asset.

Durable lesson:

> Threat hunting deliverables should be evidence-complete, reviewer-aligned, and stage-bucket-aware, not merely story-complete.

## Concrete lessons from the run

### 1. Treat platform feedback as an evidence map

The breakdown screens exposed the expected IOC bucket per stage. Future simulator or reviewer feedback should be parsed as a structured signal:

- stage number
- host-based IOCs expected/missed
- network-based IOCs expected/missed
- asset correctness
- user correctness
- tactic correctness
- technique correctness
- description feedback themes

This is more useful than a simple pass/fail score. It can drive a second-pass hunt without starting over.

### 2. Build the raw evidence table before final stage labels

The initial 20-stage timeline overfit a reasonable story:

`trojanized MSI -> PowerShell -> persistence -> Mimikatz -> lateral movement -> ransomware`

The feedback showed missing or misplaced activities:

- Invoke-NanoDump / `pwrex.ps1` / `trash.evtx`
- SharpHound / BloodHound discovery earlier in the chain
- SharpChrome / browser credential theft
- AD Recovery group activity
- `itadmin`, `anna.jones`, password-change evidence
- Domain Admins / Domain Administrators group activity
- SharpKatz DCSync
- second Mimikatz / `sekurlsa::pth`
- two ransomware staging/encryption buckets
- file hashes tied to `bomb.exe` / `.777zzz`

Future workflow should delay final stage numbering until broad IOC pivots are complete.

### 3. Avoid parent ATT&CK mappings when a sub-technique is available

The simulator penalized broad parent techniques such as:

- `T1059` instead of PowerShell-specific evidence
- `T1003` instead of LSASS Memory or DCSync where applicable
- `T1543` instead of Windows Service where applicable
- `T1218` instead of Rundll32 where applicable

Future report-readiness review should flag generic parent mappings when the evidence contains a clear sub-technique.

### 4. Descriptions need finding + implication + follow-on result

Several descriptions were judged incomplete even when the observed event was correct. A stage description should include:

- what happened
- what evidence proves it
- source URL/domain/IP when download/network-related
- destination path when file-related
- process/command line when execution-related
- user and host/asset context
- follow-on result or implication

Example pattern:

`PowerShell downloaded X from Y to Z, then executed/created/modified W, which shows attacker-controlled payload transfer/persistence/credential access rather than benign installer behavior.`

### 5. Asset semantics change by stage

For some stages, the correct asset is the execution host. For others, it is the target/affected asset, such as a domain controller targeted by DCSync or the host encrypted by ransomware. Future timeline tools should store both fields instead of forcing one ambiguous `asset` value:

- `execution_asset`
- `target_asset`
- `affected_asset`
- `source_asset`
- `destination_asset`

### 6. CTF/SOC simulator lessons should feed the bug-bounty platform, not replace it

This exercise is useful because it maps directly to the authorized bug-bounty platform workflow:

- candidate findings need evidence buckets, not just summaries;
- reviewer feedback should become structured gap codes;
- report-readiness gates should check completeness before drafting;
- ATT&CK labels should be confidence-scored and sub-technique-aware;
- affected asset reconciliation should be evidence-driven.

## Proposed project optimizations

### New future slice: SOC evidence-bucket fixture set

Recommended tier: T2 or T3 depending on whether it remains fixtures/tests only.

Boundary:

- offline/local only
- synthetic/redacted data only
- no SIEM credentials or live TryHackMe data committed
- no network, scanner, module execution, report submission, or schema promotion

Deliverable idea:

- Add a synthetic fixture representing a multi-stage incident timeline with expected evidence buckets.
- Include host IOC, network IOC, hash, user, asset, timestamp, tactic, technique, and description-gap examples.
- Add tests that verify a candidate report can be evaluated for missing evidence buckets without claiming a confirmed real-world finding.

### New future slice: report-readiness evidence bucket gate

Recommended tier: T3 design review before implementation, because it may affect candidate workflow contracts.

Possible checks:

- missing source URL for download stages
- missing destination path for dropped-file stages
- missing process/command line for execution stages
- missing source/destination asset for lateral movement stages
- missing affected asset and extension/hash for impact stages
- parent ATT&CK technique used where sub-technique evidence exists
- stage description lacks implication/follow-on result

Output should stay non-promotional:

- `needs_more_evidence`
- `needs_mapping_review`
- `needs_asset_reconciliation`
- `needs_second_pass_hunt`
- `not_report_ready`

### New future slice: reviewer-feedback parser / gap normalizer

Recommended tier: T2 if implemented only as local fixture text parser; T3 if connected to candidate workflow.

Goal:

Convert human/simulator feedback into structured gap categories:

- `MISSING_HOST_IOC`
- `MISSING_NETWORK_IOC`
- `MISSING_HASH`
- `MISSING_SOURCE_URL`
- `MISSING_DESTINATION_PATH`
- `MISSING_COMMAND_LINE`
- `MISSING_FOLLOW_ON_IMPLICATION`
- `PARENT_TECHNIQUE_TOO_BROAD`
- `TACTIC_MISMATCH`
- `ASSET_ROLE_AMBIGUOUS`
- `TIMESTAMP_EVENT_ROLE_MISMATCH`

This would let Hermes/Cowork/Codex iterate from reviewer feedback without re-reading the entire case manually.

### New future slice: dual-asset semantics in candidate evidence

Recommended tier: T3/T4 design review before any schema or runner change.

Rationale:

The simulator highlighted that one `asset` field is insufficient for threat-hunting timelines. Later platform contracts may need separate fields for source, execution, target, and affected assets. This should remain deferred until schema promotion is intentionally reviewed.

## Immediate routing recommendation

Do not interrupt the current P3.10 closeout unless the operator explicitly chooses this lane.

Add this as a candidate planning lane after P3.10 hygiene:

1. P3.10 closeout / commit hygiene remains first.
2. SOC evidence-bucket fixture/reviewer-alignment slice becomes a strong next candidate if the operator wants to convert the TryHackMe lesson into the bug-bounty workflow.
3. Any schema/runner/report-readiness integration must go through fresh T3/T4 direction review.

## Reviewer prompt add-on for future related slices

When reviewing evidence-bucket or report-readiness work, ask:

- Does the change keep simulator/lab artifacts synthetic or redacted?
- Does it avoid promoting CTF/SOC simulator outputs into real findings?
- Does it separate execution asset, target asset, affected asset, and source/destination asset when relevant?
- Does it preserve non-promotional states and manual verification requirements?
- Does it flag broad ATT&CK parent mappings only as review gaps, not as automatic corrections?
- Does it avoid report drafting/submission and target-touching behavior?

## Final decision

Decision: RECORD_LESSON_AND_QUEUE_FUTURE_SLICE

This is a documentation/planning optimization only. The next implementation step, if selected, should be an offline synthetic fixture and reviewer-gap catalog, not live SIEM integration or report submission automation.
