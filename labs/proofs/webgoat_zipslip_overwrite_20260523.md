> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# WebGoat Zip Slip Profile Overwrite Wave

Status: completed / verified local destructive-lab bounded overwrite
Date: 2026-05-23
Route/tool: Windows Hermes control plane -> `<attacker-vm>` -> Docker-backed WebGoat on `<victim-vm>`
Target: `http://<lab-ip>:8080/WebGoat`
Artifacts: `<artifact-output-dir>/webgoat_zipslip_overwrite_20260523T033158Z/`
Runner: `scripts/labs/webgoat_zipslip_overwrite_wave1.sh`
OSS/source references:
- WebGoat PathTraversal lesson
- PayloadsAllTheThings Directory Traversal reference saved under `setting/local/oss_refs/path_traversal_zipslip_20260523/`
- WebGoat upstream path traversal source references saved under `setting/local/oss_refs/webgoat_pathtraversal_20260523/`

## Scope and boundaries

- Authorized local WebGoat lab only.
- Operator explicitly allowed aggressive/destructive scripts against recoverable local靶機.
- This wave overwrote only the throwaway user's WebGoat profile image through a zip entry path traversal.
- No system binary overwrite, no shell, no persistence, no public target, no credential theft, no real exfiltration, no report/finding promotion.

## Result

Run id:

```text
webgoat_zipslip_overwrite_20260523T033158Z
```

Marker:

```text
WG_ZIPSLIP_webgoat_zipslip_overwrite_20260523T033158Z
```

Zip entry used:

```text
../../../../../../../../home/webgoat/.webgoat-2025.3/PathTraversal/zs033158/zs033158.jpg
```

Summary:

```text
pre_health: 200
login_status: 302
lesson_status: 200
zip_upload_status: 200
zip_slip_success: yes
profile_picture_status: 200
post_health: 200
```

## Evidence files

- `summary.md`
- `observations.jsonl`
- `evidence/profile.zip`
- `evidence/zs033158.jpg`
- `evidence/zipslip_upload.json`
- `evidence/profile_picture_base64.txt`
- `http/PathTraversal.lesson.html`

## Cleanup / recovery

- WebGoat post-health stayed 200.
- No snapshot restore was required.
- If cleanup is desired, restart/reset the WebGoat container or restore the victim VM snapshot.

## 對專案有什麼幫助

- 建立 archive extraction / Zip Slip 的 bounded destructive-lab proof。
- 訓練 zip entry traversal、target path calculation、overwrite proof、post-health/recovery 記錄。
- 這個 pattern 對未來 bug bounty/pentest 很實用，因為 import/export/archive processing 很常見。

## 新增/更新了什麼

- Added `scripts/labs/webgoat_zipslip_overwrite_wave1.sh`.
- Added artifacts under `<artifact-output-dir>/webgoat_zipslip_overwrite_20260523T033158Z/`.
- Added bundle `modules/bundles/verified_lab_flow_webgoat_zipslip_profile_overwrite.md`.
