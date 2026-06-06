> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# YouTube Agent upload-free draft review pattern

Use this when continuing `youtubestrict/youtube_agent` phase work from a Git-Bash/MSYS terminal on Windows and the next step must stay local-only.

## Safe command shape

Run PowerShell wrappers from the repository root with POSIX-style script paths:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File './run_agent.ps1' draft --channel psychology --topic 'boundary pause relationship text' --draft-script-engine psychology_insight_v1 1
```

Safety properties to preserve:

- Use `draft`, not `create`, for experimental Psychology/Storytime phase work.
- Require explicit `--channel`; do not run draft overrides across all channels.
- Keep engine overrides in-memory/per-run only; do not edit `channels/psychology.json` just to test a draft.
- Do not fill YouTube destination IDs, touch OAuth/token/client-secret files, change `DEFAULT_PRIVACY`, or alter scheduler behavior.
- Treat generated videos under `data/<channel>/output/...` as user-owned runtime artifacts; do not delete them during review.

## TDD before local artifact generation

Before running a local draft with a new engine/override, add focused tests that prove:

1. The CLI override is fail-closed when ambiguous.
2. The explicit override reaches `config.current().script_engine` or the downstream in-memory object used by the renderer.
3. Persistent channel JSON remains unchanged.
4. Review metadata (for example `insight_cards`, provenance, or card contracts) survives into `metadata.json`.

Then run focused unittest, py_compile, `run_agent.ps1 validate`, and `git diff --check`.

## Internal visual QA packet

For an upload-free draft, record at least:

- final video path
- metadata path
- render-QA duration/verdict
- generated frame-strip/contact-sheet path if created
- visual QA verdict: black screen/broken image, hook readability, card/diagram visibility, subtitle clipping/overlap
- explicit safety statement: no upload/publication, no scheduler/OAuth/privacy/channel activation changes

A PASS can still be `internal review only` if card microtext is small, footage is generic, asset provenance is unresolved, or the channel is not production-activated.
