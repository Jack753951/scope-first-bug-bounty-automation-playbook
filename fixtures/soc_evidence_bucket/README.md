> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# SOC Evidence-Bucket Synthetic Fixture (P3.11)

This directory contains a synthetic, redacted, offline, non-promotional
fixture that converts the TryGovMe / SOC simulator evidence-bucket lesson
captured in `handoff/trygovme_soc_sim_lessons_20260520.md` into a durable
project artifact suitable for future offline reviewer-alignment work.

## Posture (binding)

- The fixture is **synthetic**, **redacted**, **offline**, and **non-promotional**.
- It is **not a real finding**. It is **not a real IOC list**. It is **not target-touching**.
- It is **not a contract**: no other code in this repository may import, depend on,
  or treat as authoritative the field names, gap-code vocabulary, status vocabulary,
  or `evidence_confidence` vocabulary defined here. They live only inside this
  fixture and its sibling test `scripts/test_soc_evidence_bucket_fixture.py`.
- No real lab credentials, captured logs, simulator hashes, simulator URLs,
  simulator screenshots, real domains, real public IPs, real account names,
  or any real bug-bounty platform data may be substituted into this fixture.
  Only RFC reserved IP ranges and example/reserved domains are allowed.
- The slice is parallel **in spirit** to the data-only reviewer prompt catalog
  at `templates/report_readiness_reviewer_prompts.json`, but it is **not wired
  to it** and must not be wired to any runtime consumer, schema, module runner,
  scope helper, recon runtime, report generator, or platform adapter without a
  fresh T3+ direction review (see `handoff/cowork_soc_evidence_bucket_direction_review.md`).

## Allowed synthetic value ranges

- IPv4: `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24` (RFC 5737 documentation ranges).
- IPv6: `2001:db8::/32` (RFC 3849 documentation range).
- Domains and hosts: names ending in `.example`, `.invalid`, `.test`, or
  `.localhost`, plus the literals `example.tld`, `example.invalid`,
  `example.test`, `example.example`, and `localhost` (RFC 2606 / RFC 6761).
- User accounts: synthetic names such as `synthetic.user01`, `synthetic.svc.share`.
- File hashes: synthetic SHA-256 strings (64 lowercase hex characters) whose
  first four characters are `0000` or `dead`. This convention exists so that a
  reviewer cannot accidentally paste a real hash into the fixture: any real
  malware hash will not start with `0000` or `dead`, and the sibling test
  asserts the convention.

## Top-level shape

The fixture is a single JSON object with the following keys:

- `case_id` — synthetic identifier; not a real case number.
- `description` — synthetic, non-promotional description of the timeline.
- `stages` — ordered list of evidence-bucket-aligned stages.
- `notes` — synthetic operator/reviewer notes about the fixture's scope.

## Stage shape

Each stage carries the following in-fixture field set:

- `stage_index` (integer; ordering only)
- `stage_label` (short human description)
- `timestamps` — object with `event_observed` and `event_role`
- `assets` — object with `source_asset`, `execution_asset`, `target_asset`,
  `affected_asset`, `destination_asset`
- `user_account`
- `process_image`
- `command_line`
- `host_ioc` (list of reserved/example hostnames)
- `network_ioc` (list of reserved-range IPv4 or IPv6 addresses)
- `file_hashes` (list of synthetic SHA-256 strings using the `0000`/`dead` convention)
- `source_uri` (scheme-less; reserved/example hostnames only; may be empty string)
- `destination_path`
- `attack_tactic`
- `attack_technique`
- `attack_subtechnique`
- `evidence_confidence` ∈ {`low`, `medium`, `high`}
- `description`
- `gap_codes` (subset of the in-fixture gap-code vocabulary)
- `status` (subset of the in-fixture non-promotional status vocabulary)
- `next_pivot_query` (human-readable hunt prompt; not an executable query)

## In-fixture gap-code vocabulary

These codes live only inside this fixture and its sibling test:

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

## In-fixture non-promotional status vocabulary

These statuses also live only inside this fixture and its sibling test. They
are deliberately non-promotional so that a fixture stage cannot read as a
ready-to-submit finding:

- `needs_more_evidence`
- `needs_mapping_review`
- `needs_asset_reconciliation`
- `needs_second_pass_hunt`
- `not_report_ready`

## Negative-test contract

The sibling test `scripts/test_soc_evidence_bucket_fixture.py` asserts:

- Top-level required keys are present.
- Every stage carries every required field.
- Every `gap_codes[]` value is in the allowed vocabulary above.
- Every `status` value is in the allowed non-promotional vocabulary above.
- Every `evidence_confidence` value is in `{low, medium, high}`.
- Every `network_ioc` IP is in a reserved range. If a non-reserved IP such as
  `8.8.8.8` or `1.1.1.1` is introduced into the fixture, this assertion must
  fail closed. That is the synthetic-range negative-test contract.
- Every host_ioc / asset hostname / source_uri host is in the allowed
  example/reserved namespace.
- Every file hash is a 64-character hex string whose first four characters are
  `0000` or `dead`.
- The fixture contains no promotional or live key such as `confirmed_finding`,
  `submit_ready`, `report_ready`, `live_target`, `production`, `real_target`,
  or `real_credential`.
- The fixture text contains no forbidden live/action strings such as scanner
  names, Python network-module names, or any URL scheme.

## What this fixture is **not** for

- Not a runtime input to any module, runner, scanner, recon stage, report
  generator, scope helper, or external platform.
- Not a schema. No promotion to `modules/_schema/`, no `*/0.1-trial` document,
  no module manifest field, no run-manifest field.
- Not a SIEM payload. No Elastic / Kibana / Splunk / log-aggregation
  integration may consume this fixture.
- Not a finding template. No HTML / Markdown / submission rendering may
  reference this fixture as a starting payload.
- Not a lab credential store. No real account, hash, ticket, cookie, token, or
  loot-class artifact may be substituted into this fixture.

## Re-trigger conditions for a fresh direction review

A fresh T3+ direction review is required before any of the following can be
considered:

- Promoting any field name above into a runtime contract, schema, module
  manifest, or report-readiness gate.
- Importing the gap-code or status vocabulary from any code outside this
  directory and its sibling test.
- Wiring the fixture into any existing candidate-workflow consumer
  (`scripts/build_candidate_review_packet.py`, `scripts/review_candidate_packet_gaps.py`,
  `scripts/build_candidate_verification_plan.py`, `scripts/build_report_readiness_gate.py`,
  `scripts/build_candidate_workflow_fixture.py`, or any future consumer).
- Adding a reviewer-prompt JSON catalog parallel to
  `templates/report_readiness_reviewer_prompts.json` that loads or references
  the SOC gap-code vocabulary.
- Substituting any real lab, simulator, or bug-bounty platform data.
