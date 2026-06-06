> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Media profile label rungs for generated-media projects

Use this when adding asset/render/QA profile labels to a media automation pipeline without changing generation, rendering, upload, scheduling, or publication behavior.

## Goal

Expose human-review context such as `asset_profile`, `render_profile`, `qa_profile`, and `media_profile_schema_version` through metadata and QA reports while keeping labels non-authoritative. Labels must not become canary/publication approval, upload readiness, render behavior, asset selection, or QA PASS/FAIL logic unless a later reviewed plan explicitly authorizes that behavior.

## Recommended TDD rungs

### Phase A — closed data-only registry

Write RED tests before creating the registry:

- known active channels resolve to fixed profile labels and a schema version;
- unknown channels fail closed;
- unknown payload fields fail closed;
- activation/publication terms fail closed even when hidden inside otherwise allowed fields, for example `upload`, `publish`, `public`, `privacy`, `scheduler`, `oauth`, `token`, `destination`;
- validation returns a copy, not the original mutable object.

Minimal implementation shape:

- stdlib-only module such as `media_profiles.py`;
- `SCHEMA_VERSION = "media-profiles/1.0"`;
- `resolve_channel_profiles(channel_name) -> dict`;
- `validate_profile_payload(payload) -> dict`;
- active lanes only; avoid adding paused/internal experiments as active defaults.

### Phase B — optional output metadata passthrough

Write RED tests that the existing metadata builder preserves supplied profile labels and does not invent them when absent.

Minimal implementation:

- add only optional passthrough keys to the existing metadata helper, commonly:
  - `asset_profile`
  - `render_profile`
  - `qa_profile`
  - `media_profile_schema_version`
- do not wire registry lookup into generation/render/upload paths in this rung;
- do not mutate channel config or runtime state.

### Phase C — read-only QA report context

Write RED tests that the render/local QA result exposes labels from `metadata.json` and that printed output shows them for reviewers.

Assertions:

- labels are available on a non-authoritative field such as `QAResult.profile_labels`;
- missing labels remain `{}` and do not create failures;
- printed reports omit the profile section when labels are absent;
- `QAResult.ok` remains based only on `failures`.

Minimal implementation:

- add `profile_labels: dict = field(default_factory=dict)` to the QA result dataclass;
- copy only the allowed optional label keys from metadata;
- print labels as informational output after duration or metadata path;
- do not change PASS/FAIL calculation.

## Validation set

Run focused and adjacent tests, then project safety checks:

```powershell
.venv\Scripts\python.exe -m unittest tests.test_media_profiles tests.test_media_profile_metadata tests.test_render_qa_profile_labels -v
.venv\Scripts\python.exe -m unittest tests.test_channel_script_engines tests.test_safety_optimizations tests.test_render_fix_gate -v
.venv\Scripts\python.exe -m py_compile media_profiles.py pipeline.py render_qa.py config.py
powershell -NoProfile -ExecutionPolicy Bypass -File .\run_agent.ps1 validate
git diff --check
```

Expected safety statement:

- no generation/create/draft/loop/remake;
- no render behavior change;
- no QA PASS/FAIL change;
- no upload/publication/scheduler/OAuth/token/default-privacy/channel destination change;
- no channel JSON, DB, or runtime media mutation;
- labels remain review context only.

## Pitfalls

- Do not treat labels as machine approval. They are context until a later reviewed plan says otherwise.
- Do not make labels required in the first metadata/report rungs; doing so breaks old outputs.
- Do not put upload/privacy/scheduler/destination concepts inside profile payloads.
- Do not add inactive experimental lanes to active channel defaults.
- If a future rung wants labels to affect behavior, create a new plan and write RED tests for that specific authorization boundary first.
