> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Verified Lab Flow: Realistic SaaS/API multi-class target on <victim-vm>

Status: active / verified local-lab methodology
Date: 2026-05-29
Latest artifacts: `<artifact-output-dir>/realistic_saas_api_20260529T063059Z/`
Proof packet: `labs/proofs/realistic_saas_api_multi_class_kali_victim_20260529.md`
Target fixture: `labs/modern_vuln_api/modern_vuln_api.py`
Runtime target: `<victim-vm>` Docker container `modern-realistic-api` on `<victim-vm>:18080`

## When to use

Use this bundle when preparing real bug-bounty tactics for modern SaaS/API targets where the likely reportable classes are not single-form toy bugs but cross-boundary product issues:

- BOLA / IDOR object ownership;
- role separation and admin/read-only boundary exposure;
- path traversal in import/export/download/file-serving features;
- SSRF/server-side fetch primitives in webhook/importer/previewer/chatbot flows;
- XXE/parser file disclosure;
- unsafe deserialization/import code paths;
- upload retrieval and public object exposure;
- reflected XSS sink discovery that still needs browser-runtime proof.

Do not use this bundle to claim live impact. It is a local-lab methodology and evidence-shaping bundle.

## Setup

The completed run used the repo-owned fixture because it is deterministic and has owned synthetic markers.

```bash
# on <victim-vm>
docker rm -f modern-realistic-api 2>/dev/null || true
docker run -d --name modern-realistic-api \
  -p <victim-vm>:18080:18080 \
  -v /home/kali/realistic-targets/modern-vuln-api:/app:ro \
  python:3-alpine \
  python /app/modern_vuln_api.py --host 0.0.0.0 --port 18080
curl -fsS http://<victim-vm>:18080/health
```

The run first attempted to install OWASP crAPI as the closest off-the-shelf realistic API target. Several crAPI images were pulled, but full compose startup did not complete reliably. Treat crAPI as the next improvement target, not as the verified proof source for this packet.

## Evidence minimum

A run is useful only if it records both positives and controls:

- authenticated normal user baseline;
- owned-object positive control;
- cross-object positive where applicable;
- negative/secure control for role bugs;
- safe marker file for traversal/parser bugs;
- callback/OAST surrogate that does not contact public infrastructure;
- post-run health check;
- no secrets, cookies, tokens, OTPs, customer data, or live targets in artifacts.

## Current verified coverage

From `<artifact-output-dir>/realistic_saas_api_20260529T063059Z/summary.json`:

- `BOLA-001`: Alice reads Bob-owned synthetic invoice marker.
- `AUTHZ-001`: Alice reads admin audit marker while `/api/admin/settings` remains denied.
- `PATH-001`: traversal reaches lab-owned file marker.
- `SSRF-001`: target fetches loopback callback; attacker-host callback was blocked by lab network posture.
- `XXE-001`: parser expands known safe marker entity.
- `DESER-001`: bounded pickle gadget records synthetic marker without shell/secrets/persistence.
- `UPLOAD-001`: authenticated upload becomes unauthenticated direct retrieval.
- `XSS-001`: reflected script sink candidate; browser-runtime proof still required.

## Tactical use against live bounty programs

Convert this bundle into live work only after scope and ownership gates are explicit:

1. Map product objects: invoice, vehicle, project, ticket, file, workspace, org, role, invite, export, webhook.
2. Create Account A/B owned objects and preserve provenance.
3. Test one route family at a time with low request volume.
4. Require positive + negative controls before calling a candidate reportable.
5. Stop before callbacks/OAST, token generation, integrations, payment/KYC, customer data, report-ready promotion, or final submission unless explicitly approved.

## Stop-before rules

- No live target or public infrastructure by default.
- No scanner/fuzzer/DAST transfer from this local bundle.
- No credential/secret/cookie/token storage.
- No non-owned/customer data.
- No destructive writes or persistence.
- No OAST/callback/webhook/integration on live targets without a named operator gate.

## Cleanup

```bash
# on <victim-vm>
docker rm -f modern-realistic-api
```

If crAPI containers/images were partially pulled and disk cleanup is desired, inspect first with `docker compose -f ~/realistic-targets/crapi/docker-compose.yml ps` and `docker images`; do not remove unrelated lab images blindly.
