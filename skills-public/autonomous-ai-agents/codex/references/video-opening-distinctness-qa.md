> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Video Opening Distinctness QA

Use this reference when a Shorts/video automation project has technically valid renders but needs a lightweight, upload-free signal for whether the first few seconds are visually distinct enough for retention review.

## Pattern

Add or run a local-only probe that:

1. Reads an existing local MP4 only.
2. Extracts the first 4 seconds with ffmpeg at about 1 fps.
3. Scales frames to a small width, e.g. `scale=160:-1`.
4. Crops to the middle vertical band, e.g. `crop=iw:ih/2:0:ih/4`, so changing hook/subtitle text does not falsely hide a repeated background.
5. Compares adjacent PPM frames with stdlib mean absolute pixel difference.
6. Writes JSON only under `handoff/`.
7. Reports guardrails explicitly: no upload, publication, OAuth, scheduler, active channel config mutation, or writes outside handoff.

This should be framed as a reviewer signal, not a publication approval gate.

## Suggested CLI shape

Keep existing behavior as the default and add the probe as an additive mode:

```bash
python tools/oss_media_qa.py <mp4> --probe opening-distinctness --opening-seconds 4
```

If extending an existing scene/static QA tool, preserve the old default, e.g. `--probe scene-static`.

## Implementation guardrails

- Use `subprocess.run([...], shell=False)` / arg-list ffmpeg calls.
- Constrain output directories with an explicit resolver that only permits paths under `handoff/`.
- Use `tempfile.TemporaryDirectory(dir=out_root)` so temporary frame files also stay under handoff.
- Validate `opening_seconds > 0` and `sample_fps > 0` locally before invoking ffmpeg.
- Missing ffmpeg may be `SKIPPED_DEPENDENCY_MISSING` for optional QA; missing input should be `FAIL`.
- Do not import upload/auth/scheduler/database/channel-runtime modules into the probe module.

## Test checklist

Add focused tests for:

- PPM diff detects scene changes.
- Static frame sequences return `REVISE`.
- Missing input writes a fail report.
- Missing dependency writes a skip report if optional.
- Output outside `handoff/` is rejected.
- Invalid sampling params fail clearly before ffmpeg.
- Source-level forbidden imports/strings stay absent (`youtube_api`, `agent`, `pipeline`, `database`, `scheduler`, `config`, `client_secret`, `token.json`, `videos.insert`).

## Review packet usage

For each candidate video, include the generated JSON path in the handoff packet along with human visual QA. A pass means the first sampled seconds contain enough cropped-middle visual change for review; it does not override human judgement about whether the opening has a compelling second beat by ~1.5s.
