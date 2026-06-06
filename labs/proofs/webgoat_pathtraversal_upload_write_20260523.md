> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# WebGoat Path Traversal Upload File-Write Wave

Status: completed / verified local destructive-lab bounded file write
Date: 2026-05-23
Route/tool: Windows Hermes control plane -> `<attacker-vm>` -> Docker-backed WebGoat on `<victim-vm>`
Target: `http://<lab-ip>:8080/WebGoat`
Artifacts: `<artifact-output-dir>/webgoat_pathtraversal_upload_write_20260523T033108Z/`
Runner: `scripts/labs/webgoat_pathtraversal_upload_write_wave1.sh`
OSS/source references:
- WebGoat upstream `ProfileUpload.java`
- WebGoat upstream `ProfileUploadBase.java`
- PayloadsAllTheThings Directory Traversal reference saved under `setting/local/oss_refs/path_traversal_zipslip_20260523/`
- WebGoat lesson JS `/lesson_js/path_traversal.js`

## Scope and boundaries

- Authorized local WebGoat lab only.
- Operator explicitly allowed aggressive/destructive scripts against recoverable local靶機.
- This wave wrote only a marker image under WebGoat's PathTraversal lab directory.
- No public target, no system file overwrite, no shell, no persistence, no credential theft, no real exfiltration, no report/finding promotion.

## Result

Run id:

```text
webgoat_pathtraversal_upload_write_20260523T033108Z
```

Marker:

```text
WG_PATH_UPLOAD_webgoat_pathtraversal_upload_write_20260523T033108Z
```

Summary:

```text
pre_health: 200
login_status: 302
lesson_status: 200
js_status: 200
control_upload_status: 200
traversal_upload_status: 200
traversal_success: yes
profile_picture_status: 200
post_health: 200
```

Proof response:

```json
{
  "lessonCompleted" : true,
  "feedback" : "Congratulations. You have successfully completed the assignment.",
  "assignment" : "ProfileUpload",
  "attemptWasMade" : true
}
```

## Evidence files

- `summary.md`
- `observations.jsonl`
- `evidence/control_upload.json`
- `evidence/traversal_upload.json`
- `evidence/marker.jpg`
- `evidence/profile_picture_base64.txt`
- `http/PathTraversal.lesson.html`
- `http/path_traversal.js`

## Cleanup / recovery

- WebGoat post-health stayed 200.
- No snapshot restore was required.
- If cleanup is desired, restart/reset the WebGoat container or restore the victim VM snapshot.

## 對專案有什麼幫助

- 把 path traversal 從 directory listing / metadata 候選提升到可重跑的 bounded file-write impact proof。
- 訓練 upload filename / form field / canonical path bypass 的證據模式。
- 讓 destructive-lab 授權有實際範例：可打、可證明、可 post-health、可恢復。

## 新增/更新了什麼

- Added `scripts/labs/webgoat_pathtraversal_upload_write_wave1.sh`.
- Added artifacts under `<artifact-output-dir>/webgoat_pathtraversal_upload_write_20260523T033108Z/`.
- Added bundle `modules/bundles/verified_lab_flow_webgoat_pathtraversal_upload_write.md`.
