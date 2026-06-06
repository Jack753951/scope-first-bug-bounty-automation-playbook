> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Upload-Free Media/Channel Rungs

Use this reference when a repo generates visible media/content artifacts but public upload, scheduling, OAuth, credentials, or active-channel activation must remain gated.

## Pattern

1. **Creative review before the next rung**
   - Save a review packet/result in the repo handoff area.
   - Use explicit verdicts: `CANARY`, `REVISE`, `REJECT`.
   - Treat `CANARY` as permission to build the next offline artifact only, never publication permission.

2. **Narrow the rung**
   - Advance the strongest candidate only when review says so; do not expand all concepts at once.
   - Define one deterministic artifact: contact sheet, HTML storyboard, local MP4 fixture, script pack, etc.
   - Keep outputs under handoff/review directories unless the repo has a designated fixture path.

3. **TDD the artifact contract**
   - Write tests first for: mode, selected candidate, duration/counts, required visual/story evidence, output files, report content, and forbidden imports/side effects.
   - Observe a RED failure for the missing module/behavior before implementing.
   - Implement the smallest isolated generator needed to satisfy the contract.

4. **Safety guardrails in tests and manifest**
   - Assert upload/OAuth/scheduler/runtime-data flags are false.
   - Assert active channel/config remains absent when the feature is disabled-only.
   - Assert disabled/proposal config remains present.
   - Assert no imports of upload/runtime modules such as `youtube_api`, `agent`, `pipeline`, `database`, or scheduler entrypoints unless the specific approved rung requires them.
   - Do not read or print token/client-secret paths or contents.

5. **Visual QA before reporting success**
   - Open the generated artifact locally when browser tools are available.
   - Check safety labels (`NO UPLOAD`, mode, duration), loaded assets, required story beats/evidence, readability, and obvious clipping/broken images.
   - Capture PASS/REVISE notes in handoff records.

6. **Record handoff and project notes**
   - Update the repo handoff files that future agents/subagents will read.
   - If the project uses Obsidian/project notes, save the durable decision and next gate there.
   - Keep records about safety state explicit: no upload/publication, no scheduler change, no OAuth/token access, no active-channel activation, no runtime data writes.

## Useful validation bundle

Adapt to the repo, but a good final bundle is:

```bash
python -m pytest <new-test> <related-focused-tests> -q
python -m py_compile <new-module> <new-test> <related-modules>
python <new-generator>
python - <<'PY'
import json
from pathlib import Path
for path in [<manifest-or-json-paths>]:
    json.loads(Path(path).read_text(encoding='utf-8'))
print('json parse PASS')
PY
git diff --check
```

Also run the repo's own validation wrapper if present. On Windows projects launched from Git Bash, call PowerShell wrappers through `powershell.exe -NoProfile -ExecutionPolicy Bypass -File './script.ps1'`.

## Pitfalls

- Do not let a creative `CANARY` review become implied upload approval.
- Do not broaden from one winning concept to all concepts in the same rung unless explicitly requested.
- Do not skip browser/visual inspection for generated media artifacts; transcript/JSON-only checks miss layout and asset failures.
- Do not encode transient setup/tool failures as durable skill rules; record the retry or validation pattern, not the momentary failure.
