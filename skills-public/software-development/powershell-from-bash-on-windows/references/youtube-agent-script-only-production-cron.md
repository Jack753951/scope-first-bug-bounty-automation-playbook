> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# YouTube Agent script-only Hermes production cron pattern

Use this when a Shorts automation repo already has approved daily production-loop cron jobs and you want to reduce agent overhead or avoid delivery-origin failures by converting them to Hermes `no_agent` script-only jobs.

## Durable pattern

1. Keep the real implementation in the project repo.
   - Example: `scripts/run_production_loop.py`.
   - Require an explicit `--channel`.
   - Validate first via the existing project wrapper, e.g. `run_agent.ps1 validate`.
   - Delegate production only to the existing entrypoint, e.g. `run_agent.ps1 loop --channel <channel>`.

2. Add fixed-channel repo wrappers for clarity and dry-run verification.
   - Example: `scripts/run_production_loop_redditstories.py` calls the shared wrapper with `--channel redditstories`.
   - Example: `scripts/run_production_loop_redditscary.py` calls the shared wrapper with `--channel redditscary`.

3. Add tiny Hermes-script entrypoints under `~/.hermes/scripts/`.
   - Hermes cron rejects absolute/home-relative script paths; `script=` must be a filename relative to `~/.hermes/scripts/`.
   - The Hermes script should import the repo implementation and call the fixed channel.
   - Keep this file tiny so project logic remains in repo handoff/versioned context.

4. Add a dry-run mode before updating cron.
   - CLI flag: `--dry-run`, and/or env var such as `YOUTUBE_AGENT_PRODUCTION_LOOP_DRY_RUN=1`.
   - Dry-run should run validation and print the exact would-run command.
   - Dry-run must explicitly not run loop/create/remake/upload.

5. Update existing cron jobs rather than creating duplicate production owners.
   - Set `no_agent=true`.
   - Set `script=<filename-under-hermes-scripts.py>`.
   - Preserve the schedule and workdir unless the user explicitly asked otherwise.
   - For CLI-origin jobs where no user-facing success message is needed, use `deliver=local` and make normal success silent. Non-empty stdout from a `no_agent` job is delivered verbatim; empty stdout is quiet.

6. Keep upload gates separate.
   - Do not resume best-candidate scheduled-upload gates just because production-loop cron changed.
   - Production loops and exact-artifact upload gates are separate ownership lanes.

## Verification bundle

Run and record:

```bash
python -m py_compile scripts/run_production_loop.py scripts/run_production_loop_<channel>.py
python scripts/run_production_loop_<channel>.py --dry-run
YOUTUBE_AGENT_PRODUCTION_LOOP_DRY_RUN=1 python <user-home>
powershell -NoProfile -ExecutionPolicy Bypass -File './run_agent.ps1' validate
hermes cron status
```

Then inspect `hermes cron list`:

- production jobs enabled;
- schedules unchanged;
- `no_agent=true`;
- expected `script=` filename set;
- upload-gate jobs still paused when that was the intended ownership model;
- `.agent.lock` clear;
- `DEFAULT_PRIVACY='private'`.

## Pitfalls

- `last_status` may still show an old delivery error until the next run. Distinguish historical status from current `script/no_agent/deliver` configuration.
- Do not treat a successful dry-run as a completed production loop; it proves scheduler mechanics and validation only.
- Do not print secrets from validation. Presence/shape checks are enough.
