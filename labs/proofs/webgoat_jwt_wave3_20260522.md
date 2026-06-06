> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# WebGoat JWT Wave 3

Status: completed / verified low-risk JWT decode proof + token endpoint map
Date: 2026-05-22
Route/tool: Windows Hermes control plane -> SSH/SCP -> `<attacker-vm>` -> Docker-backed WebGoat on `<victim-vm>` (`<lab-ip>:8080`)
Model/runtime: current Hermes session; no Claude/Codex worker invoked; no usage artifact
Artifact run: `<artifact-output-dir>/webgoat_jwt_wave3_20260522T045749Z/`

## Scope and boundary

- Local authorized WebGoat lab only.
- Single capability lane: JWT/token lesson.
- No public targets.
- No brute force or dictionary cracking.
- No credential theft.
- No external callbacks.
- No destructive writes.
- Raw token values in durable docs are abbreviated/redacted; full raw runtime artifacts remain local under git-ignored `<artifact-output-dir>/`.

## Verified proof

Bounded verified proof used the WebGoat JWT decode assignment only.

Evidence:

- `<artifact-output-dir>/webgoat_jwt_wave3_20260522T045749Z/jwt_probe/jwt_decode_user.json`

Observed result:

```json
{
  "lessonCompleted" : true,
  "feedback" : "Congratulations. You have successfully completed the assignment.",
  "assignment" : "JWTDecodeEndpoint",
  "attemptWasMade" : true
}
```

Supporting observation:

```json
{"type":"jwt_decode_verified","name":"user","value":"status=200 lessonCompleted=true"}
```

## Additional useful token evidence

The run also fetched authenticated JWT lesson material and decoded lesson-provided JWT examples offline:

- `JWT.lesson`: 200 / 65445 bytes
- `lesson_js/jwt-voting.js`: 200 / 3150 bytes
- `lesson_js/jwt-weak-keys.js`: 200 / 92 bytes
- `lesson_js/jwt-refresh.js`: 200 / 1419 bytes
- `lesson_js/jwt-jku.js`: 200 / 174 bytes
- `lesson_js/jwt-kid.js`: 200 / 182 bytes
- `lesson_js/jwt-buy.js`: 200 / 1073 bytes
- `images/logs.txt`: 200 / 1155 bytes

Endpoint map artifact:

- `<artifact-output-dir>/webgoat_jwt_wave3_20260522T045749Z/endpoint_extract.txt`

Decoded-token artifact:

- `<artifact-output-dir>/webgoat_jwt_wave3_20260522T045749Z/jwt_probe/decoded_tokens.jsonl`

Token patterns captured for future lanes:

- HS256 token with `ROLE_ADMIN` / `ROLE_USER` claims in lesson content.
- HS512 voting tokens with `admin=false` and user claims.
- RS256 `jku` token pointing to a JWKS URL in lesson content.
- HS256 `kid=webgoat_key` token in lesson content.

These are useful next-lane seeds, but they are not promoted as exploit proofs in this wave.

## Script fixes discovered during this wave

- Initial script used shell built-in `USER`, causing accidental `kali` username behavior and authenticated JWT fetches returning 302.
- Fixed variable to `WG_USER` and reran cleanly.
- Added candidate decode attempts for `WebGoat`, `Tom`, `user`, and `Jerry`; only `user` produced `lessonCompleted=true`.

## Possible vulnerabilities / review candidates

### possible_manual_review_candidates

- JWT decode lesson proof is verified-impact for local lab learning and demonstrates token inspection/claim-reading workflow.
- JWT voting, weak key, refresh token, JKU, and KID endpoints are mapped and ready for separate bounded waves.
- Decoded lesson tokens show admin/role, `jku`, and `kid` claim patterns that map well to bug-bounty JWT review checklists.

### non_findings_or_controls

- This wave did not brute-force weak secrets.
- This wave did not forge JWTs.
- This wave did not call external JWKS/callback infrastructure.
- Voting/login token issuance was treated as endpoint mapping, not as a finding.

### missing_evidence_to_confirm

- A JWT signing/role-escalation proof would need a separate bounded wave with exact token mutation and server-accepted impact.
- Refresh-token manipulation would need a separate bounded wave with controlled access/refresh token pairing evidence.
- JKU/KID misuse would need a separate bounded wave and should avoid external callback unless explicitly approved for local lab infrastructure.

## 對專案有什麼幫助

- 補上 WebGoat JWT/token 能力線的第一個 verified proof，讓 Access Control/IDOR 之後的第二條必測能力線開始落地。
- 建立 authenticated JWT lesson artifact pattern：lesson page + JS + endpoint map + offline token decode + JSON observation。
- 把 JWT lesson 拆成後續可重複的子能力：decode、signing/role escalation、weak key、refresh token、JKU、KID。
- 發現並修正 shell `USER` 變數踩雷，避免未來 lab script 產生錯誤 throwaway user/session。
- 提供 bug bounty / pentest automation 的 JWT review seed，但保留 candidate-only/manual-review 語言。

## 新增/更新了什麼

- Added `scripts/labs/webgoat_jwt_wave3.sh`.
- Added this handoff record.
- Added `modules/bundles/verified_lab_flow_webgoat_jwt_decode_token_inspection.md`.
- Added Obsidian lab note for WebGoat JWT wave 3.
- Updated `handoff/accepted_changes.md`.
- Updated `handoff/active_strategy_queue.md`.
- Updated `scripts/SCRIPT_INVENTORY.md`.

## Next lane

Recommended next WebGoat JWT lane: weak-key/signing or refresh-token manipulation, before browser-dependent XSS runtime proof.
