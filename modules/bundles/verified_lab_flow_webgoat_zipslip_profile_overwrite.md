> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Verified Lab Flow — WebGoat Zip Slip Profile Overwrite

Status: verified-impact / local-learning-lab only
Last verified: 2026-05-23
Handoff: `handoff/webgoat_zipslip_overwrite_20260523.md`
Artifacts: `<artifact-output-dir>/webgoat_zipslip_overwrite_20260523T033158Z/`
Runner: `scripts/labs/webgoat_zipslip_overwrite_wave1.sh`

## Use when

Use this to practice archive extraction path traversal / Zip Slip in the authorized local WebGoat lab.

## Rerun

```bash
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ./scripts/kali-run.ps1 -Command 'cd /mnt/hacking && bash scripts/labs/webgoat_zipslip_overwrite_wave1.sh'
```

Pull artifacts:

```bash
MSYS2_ARG_CONV_EXCL='*' powershell.exe -NoProfile -ExecutionPolicy Bypass -File ./scripts/kali-pull.ps1 -RemotePath '/home/kali/<artifact-output-dir>/<run_id>'
```

## Success criteria

- `zip_upload_status=200`
- `zip_slip_success=yes`
- `post_health=200`
- `evidence/zipslip_upload.json` contains `lessonCompleted: true`.

## Boundary

Local WebGoat only. Bounded throwaway profile-image overwrite only. No public targets, system binary overwrite, shell, persistence, credential theft, or report promotion.
