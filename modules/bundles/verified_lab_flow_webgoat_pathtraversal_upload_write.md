> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Verified Lab Flow — WebGoat Path Traversal Upload Write

Status: verified-impact / local-learning-lab only
Last verified: 2026-05-23
Handoff: `handoff/webgoat_pathtraversal_upload_write_20260523.md`
Artifacts: `<artifact-output-dir>/webgoat_pathtraversal_upload_write_20260523T033108Z/`
Runner: `scripts/labs/webgoat_pathtraversal_upload_write_wave1.sh`

## Use when

Use this to practice and verify upload-field path traversal leading to bounded file write in the authorized local WebGoat lab.

## Rerun

```bash
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ./scripts/kali-run.ps1 -Command 'cd /mnt/hacking && bash scripts/labs/webgoat_pathtraversal_upload_write_wave1.sh'
```

Pull artifacts:

```bash
MSYS2_ARG_CONV_EXCL='*' powershell.exe -NoProfile -ExecutionPolicy Bypass -File ./scripts/kali-pull.ps1 -RemotePath '/home/kali/<artifact-output-dir>/<run_id>'
```

## Success criteria

- `traversal_upload_status=200`
- `traversal_success=yes`
- `post_health=200`
- `evidence/traversal_upload.json` contains `lessonCompleted: true` and assignment `ProfileUpload`.

## Boundary

Local WebGoat only. Bounded marker image write only. No public targets, system-file overwrite, shell, persistence, credential theft, or report promotion.
