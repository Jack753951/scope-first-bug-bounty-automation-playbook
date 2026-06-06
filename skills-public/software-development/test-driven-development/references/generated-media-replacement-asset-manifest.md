> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Generated-media replacement asset manifest TDD

Use when an internal generated-media template is structurally accepted but blocked from production because placeholders or reference-only examples must be replaced by original/licensed assets.

## Trigger

- The user approves moving from an upload-free/internal structural template toward production-safe sourcing.
- Reference examples are downloaded/competitor/public and remain `YELLOW_INTERNAL_REFERENCE_ONLY`.
- The next risk is accidental promotion of unlicensed characters, SFX, BGM, props, backgrounds, or UI elements into active assets.

## TDD shape

Before creating or promoting any asset folder, write tests/manifest checks that prove:

1. The replacement manifest exists and is parseable.
2. Every required category has an ID, priority, category, required variants, license requirements, approval status, and `production_ready=false` by default.
3. The manifest has global license requirements for commercial YouTube use, editing/compositing, repeated automated renders, attribution, subscription dependency, AI/automation restrictions, and audio Content ID/whitelist handling.
4. Candidate assets remain in quarantine/reference-library folders until source URL, license path/text, allowed-use summary, sha256, and review packet are recorded.
5. `upload_authorized=false`, `channel_activation=false`, and no active channel config or publishing path is created by the manifest step.
6. Reference-only examples are not copied into the approved or active asset folder.

## Recommended category order

1. P0 SFX pack: ping, pop, whoosh, error/fail, impact, bonk/hit, bass hit, safe record-scratch alternative, vote/click. Require clear YouTube commercial/edit/mix/repeated-render rights and Content ID/whitelist notes.
2. P0 character/sticker pack: non-IP, watermark-free cast/expression set readable on Shorts. Require transparent PNG/SVG or editable source when possible.
3. P1 props/UI pack: phone, chat bubble/message card, timestamp/clock, receipt/bill/document, vote/poll card.
4. P2 background pack: crop-safe home/office/classroom/neutral stage.
5. P3 optional BGM: only after SFX/characters; stricter Content ID review.

## Handoff artifact pattern

Write:

- `replacement_asset_manifest_vN.json` with default `production_ready=false` for all requirements.
- `replacement_asset_buying_checklist_vN.md` for the user: plain-language purchase order, license questions, avoid list, and where to drop candidates.
- `candidate_licensed_asset_submission_template.md` with fields for source/vendor URL, license URL/PDF, commercial use, editing, repeated automated renders, attribution, subscription dependency, audio Content ID, IP/watermark risks, and hashes.
- A compact decision/handoff note summarizing the sourcing gate and next user action.

## Verification

Run a local JSON/safety check that confirms:

- required category IDs exist;
- all requirement entries stay `production_ready=false`;
- manifest-level `upload_authorized=false` and `channel_activation=false`;
- no active channel config was created;
- candidate files, if present, remain quarantined and unpromoted.

## Pitfalls

- A user saying they will buy/find assets is not approval to upload, schedule, enable a channel, or copy files into active production paths.
- Bought assets are not production-safe until the written license/source/hash/allowed-use record exists.
- Audio/BGM needs stronger Content ID handling than visual props or stickers.
- Do not hard-code a specific marketplace/vendor into the skill; licenses change.
