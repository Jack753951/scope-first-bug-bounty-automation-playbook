> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Security Fixture Review TDD Pattern

Use this for safety-sensitive cybersec pipelines where the next slice is fixture-only and must not introduce live target behavior.

## Pattern

1. Start with the approved direction review / OSS Recon Gate verdict and list the exact allowed file surface.
2. Write RED tests before adding fixtures:
   - required fixture directories/files must exist;
   - each fixture validates against the existing schema/validator;
   - fixture content is synthetic/redacted (for example `.example.test`, project-specific synthetic module IDs, redacted evidence refs, placeholder hashes);
   - workflow output is byte-identical across repeated runs;
   - downstream status vocabulary remains non-promotional (`blocked`, `needs_manual_review`, `not_ready`, etc.);
   - known edge cases survive independently, e.g. duplicate/near-duplicate candidates are not silently collapsed.
3. Run focused tests and confirm they fail for the expected missing-fixture or missing-behavior reason.
4. Add the smallest committed synthetic fixtures needed to make the tests pass. Prefer realistic shape over real target/source data.
5. Run direct validator snippets over every fixture, then run a deterministic end-to-end offline workflow diff if a pure chain exists.
6. Ask for independent implementation review. If it returns `REQUEST_CHANGES`, convert each blocker into a focused regression test before patching fixtures/code.
7. Update the project handoff/accepted-changes log only after the review blocker is fixed and local verification passes.

## Safety boundaries to assert

- No live scans, probes, fuzzing, exploit tooling, callbacks/OAST, proxy/pivot/tunnel work, or target interaction.
- No network clients, scanner imports, subprocess-driven scanner/runtime execution, or external-source ingest.
- No schema promotion, runtime/recon wiring, platform adapter, report drafting, or report submission.
- No scope files, loot, credentials, OAuth, scheduler, deployment, billing, or production setting changes.

## Pitfall

Aggregate vocabulary coverage can pass while an important fixture-specific invariant is wrong. Add targeted tests for review-discovered blockers, such as distinct `source.module_id` values for notional duplicate sources, and prove both records survive the packet/workflow builder.
