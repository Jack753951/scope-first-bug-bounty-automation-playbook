> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Phase 4B Script-first Architecture Reset 2026-05-21

Status: active direction reset
Source: Operator correction + Hermes synthesis
Date: 2026-05-21
Repo truth: `<user-home>`

## Correction

The desired architecture is script-first and context-driven, not contract-first.

Desired loop:

```text
preview + recon results
→ choose modules based on context
→ if no module fits, use script library
→ choose and execute a script combination for the situation
→ results + review
→ modularize the context-specific script combination
→ preview + recon results
→ repeat
→ penetration test report
```

## Meaning

- Scripts should be visible and primary.
- Module bundles should be reusable script combinations triggered by context.
- Heavy manifest/profile/validator/review contracts stay as guardrails, not the main workflow.
- Phase 4B should stop growing generic safety scaffolding before making the script library usable.

## New repo anchors

- `scripts/SCRIPT_INVENTORY.md` — operator-facing script map.
- `modules/bundles/README.md` — lightweight module-bundle shape.
- `modules/bundles/lab_directory_listing_triage.md` — first bundle draft around `/ftp/`.
- `handoff/phase4b_script_first_architecture_reset_20260521.md` — accepted direction reset.

## Next action

Build `lab_directory_listing_triage` for the current strongest candidate:

```text
/ftp/ directory listing
```

Expected next script:

```text
scripts/lab_modules/ftp_filename_content_class_verifier.py
```

The goal is to classify filenames/content-types/sizes and produce review/report input, not bulk download files or collect secrets.
