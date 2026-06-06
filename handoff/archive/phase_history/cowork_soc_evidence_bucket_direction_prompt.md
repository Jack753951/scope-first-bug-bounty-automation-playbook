> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cowork Direction Review Prompt — SOC Evidence-Bucket Fixture / Reviewer Alignment

Date: 2026-05-20
Prepared by: Hermes
Recommended review tier: T3 design-only if it touches candidate workflow contracts; T2 only if reviewer recommends docs/fixtures/tests that remain completely local and non-contractual.
Milestone: Post-P3.10 project workflow calibration
Source lessons:
- `handoff/trygovme_soc_sim_lessons_20260520.md`
- `notes/daily/2026-05-20.md`
- `handoff/active_strategy_queue.md`

## Context

The TryGovMe / TryHackMe SOC Simulator exercise showed that a plausible attack-chain narrative can still fail reviewer/platform grading when stage evidence buckets are incomplete or misaligned.

The useful project lesson is not the simulator answer itself. The durable lesson is that the authorized bug-bounty platform needs stronger reviewer-aligned evidence completeness checks before report drafting or finding promotion.

Relevant current project state:

- P3.10 minimal dry-run explicit recon-policy-artifact direct-read bridge is complete and committed.
- The workspace is clean after closeout.
- CTF/SOC labs are calibration only and should feed backlog/project improvements when useful.
- Current candidate workflow already has non-promotional trial consumers for candidate review packets, gap reports, verification plans, and report-readiness gates.
- No current slice should add live SIEM integration, target interaction, scanner/module execution, report submission, or schema promotion without fresh review.

## Direction question

What is the safest and most useful next slice to convert the SOC simulator lesson into project capability?

Please choose one of these options, or propose a smaller safer variant:

1. `PROCEED_FIXTURE_ONLY`
   - Add synthetic/redacted offline fixtures representing a multi-stage incident timeline and expected evidence buckets.
   - Add tests/docs only.
   - No new consumer, schema, runner, report gate, scanner, SIEM, or platform adapter.

2. `PROCEED_REVIEWER_GAP_CATALOG_ONLY`
   - Add a static JSON/Markdown catalog of evidence-bucket gap codes and reviewer questions, similar in spirit to existing report-readiness reviewer prompt catalog work.
   - No executable consumer.

3. `PROCEED_TRIAL_CONSUMER_DESIGN_ONLY`
   - Write a no-code implementation plan for a future offline/stdout-only trial consumer that normalizes reviewer feedback into non-promotional gap categories.
   - No implementation yet.

4. `DEFER_AND_RETURN_TO_MAINLINE`
   - Defer SOC evidence-bucket work and return to a broader bug-bounty platform mainline slice.

5. `BLOCK`
   - Explain blocker(s), especially if this would overfit CTF/SOC simulator behavior or risk promoting lab artifacts into real findings.

## Boundary locks

The accepted next slice must not introduce:

- live SIEM or Elasticsearch/Kibana integration
- target-touching behavior
- scanner/module execution
- recon runtime changes
- report drafting or report submission
- schema promotion under `modules/_schema/` unless explicitly reviewed
- platform adapters
- credentials, cookies, OAuth, tokens, or lab secrets
- loot handling
- scheduler/CI activation
- exploit, brute force, callback/OAST, proxy, pivot, tunnel, or destructive behavior
- real TryHackMe screenshots/log exports committed if they contain lab credentials or sensitive data

Synthetic/redacted examples only.

## Required OSS Recon Gate notes

If recommending any contract, schema, evidence representation, or review artifact, compare the proposed shape conceptually against relevant mature formats without copying unsafe defaults:

- MITRE ATT&CK for tactic/technique/sub-technique mapping
- Sigma / Elastic detection rule evidence fields for event context
- STIX/OpenCTI for indicator and relationship concepts
- SARIF for result location/message/gap style
- DefectDojo/<bug-bounty-platform>/Bugcrowd only for report/reviewer workflow concepts, not for submission automation

Record adopt/adapt/ignore decisions.

## Evidence-bucket concepts to preserve

The review should decide whether and how to model these as fixture fields, gap codes, reviewer prompts, or future trial-consumer output:

- host IOC
- network IOC
- file hash
- timestamp
- user/account
- process image
- command line
- source URL/domain/IP
- destination path
- source asset
- execution asset
- target asset
- affected asset
- ATT&CK tactic
- ATT&CK technique/sub-technique
- evidence confidence
- reviewer gap category
- next pivot query
- follow-on implication in human description

Suggested non-promotional gap vocabulary:

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
- `NEEDS_SECOND_PASS_HUNT`

Potential non-promotional states:

- `needs_more_evidence`
- `needs_mapping_review`
- `needs_asset_reconciliation`
- `needs_second_pass_hunt`
- `not_report_ready`

## Review deliverable requested

Write the review to:

`handoff/cowork_soc_evidence_bucket_direction_review.md`

Include:

1. Final verdict from the options above.
2. Recommended review tier and why.
3. OSS Recon Gate adopt/adapt/ignore notes if applicable.
4. Exact allowed implementation boundary.
5. Exact forbidden surfaces.
6. Recommended files to create/modify if proceeding.
7. Tests or validation that must pass.
8. Whether P2.24 helper extraction or any existing candidate workflow contract is implicated.
9. Multi-Party Review Decision final block:
   - Hermes authority level
   - operator approval required? yes/no
   - blocking issues
   - non-blocking recommendations

## Hermes synthesis expectation

Hermes should not implement code from this prompt directly. After Cowork review, Hermes should synthesize the verdict and either:

- prepare a smaller offline fixture/catalog implementation task, or
- record deferral and return to mainline.
