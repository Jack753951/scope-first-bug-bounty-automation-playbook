> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# verified_lab_flow_webgoat_jwt_decode_token_inspection

Status: verified-impact / local-lab only
Date: 2026-05-22
Route/tool: `<attacker-vm>` HTTP/curl -> Docker-backed WebGoat on `<victim-vm>`
Primary artifact: `<artifact-output-dir>/webgoat_jwt_wave3_20260522T045749Z/`
Handoff: `handoff/webgoat_jwt_wave3_20260522.md`

## Purpose

Bounded WebGoat JWT/token lesson flow for learning and retaining JWT inspection evidence without brute force, token forging, credential theft, or external callbacks.

This bundle currently verifies the low-risk JWT decode assignment and maps the remaining JWT lesson endpoints for future waves.

## When to use

Use when:

- WebGoat is running on the authorized Docker-backed local lab.
- A throwaway WebGoat user/session is acceptable.
- The goal is to verify JWT/token inspection workflow and collect next-lane endpoints.

Do not use when:

- The target is public/third-party or not explicitly authorized.
- The operator expects real target JWT exploitation.
- The goal requires brute forcing, dictionary cracking, external JWKS hosting, callback collection, or credential theft.

## Script

```bash
scripts/labs/webgoat_jwt_wave3.sh
```

Default target:

```bash
TARGET_HOST=<lab-ip>
WEBGOAT=http://<lab-ip>:8080/WebGoat
```

The script:

1. checks WebGoat login health;
2. registers/logs in a short throwaway user using `WG_USER`, not shell `USER`;
3. fetches JWT lesson page and lesson JS;
4. extracts JWT endpoints/actions;
5. submits bounded decode candidates (`WebGoat`, `Tom`, `user`, `Jerry`);
6. records verified decode success only when WebGoat returns `lessonCompleted=true`;
7. probes lesson-visible voting login endpoints for endpoint mapping only;
8. decodes JWT headers/payloads offline from local artifacts;
9. writes summary and JSONL observations.

## Verified evidence

Verified artifact:

```text
<artifact-output-dir>/webgoat_jwt_wave3_20260522T045749Z/jwt_probe/jwt_decode_user.json
```

Observed server response:

```json
{
  "lessonCompleted" : true,
  "feedback" : "Congratulations. You have successfully completed the assignment.",
  "assignment" : "JWTDecodeEndpoint",
  "attemptWasMade" : true
}
```

Observation line:

```json
{"type":"jwt_decode_verified","name":"user","value":"status=200 lessonCompleted=true"}
```

## Candidate-only endpoint map

`endpoint_extract.txt` captured these future lanes:

- `/WebGoat/JWT/decode`
- `/WebGoat/JWT/secret`
- `/WebGoat/JWT/votings`
- `/WebGoat/JWT/votings/login?user=Tom`
- `/WebGoat/JWT/refresh/checkout`
- `JWT/refresh/login`
- `JWT/refresh/newToken`
- `/WebGoat/JWT/jku/delete?...`
- `/WebGoat/JWT/kid/delete?...`
- `JWT/kid/follow/...`

These are not confirmed findings. They are local-lab next-lane seeds.

## Safety boundaries

- local authorized lab only
- no brute force/dictionary cracking
- no JWT forging in this wave
- no external callbacks/JWKS hosting
- no credential theft
- no destructive writes
- raw tokens remain local in git-ignored artifacts; durable docs use redacted/abbreviated values

## False-positive controls

- HTTP 200 alone is not treated as proof.
- Token issuance/login probes are endpoint mapping unless paired with `lessonCompleted=true` or separately verified impact.
- Full JWT signing/refresh/JKU/KID impact requires separate bounded proof.

## 對專案有什麼幫助

- Adds a reusable WebGoat JWT/token inspection bundle after the IDOR bundle.
- Gives future automation a stable artifact shape for JWT lesson page/JS/endpoint map/offline decoded-token records.
- Separates verified decode proof from candidate-only signing/refresh/JKU/KID leads.

## 新增/更新了什麼

- `scripts/labs/webgoat_jwt_wave3.sh`
- `handoff/webgoat_jwt_wave3_20260522.md`
- `<artifact-output-dir>/webgoat_jwt_wave3_20260522T045749Z/`
- this bundle document
