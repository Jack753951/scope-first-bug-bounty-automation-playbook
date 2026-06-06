> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Realistic SaaS/API target-search tactics — 2026-05-29

Status: active note
Scope: local-lab methodology for translating realistic SaaS/API bug classes into bug-bounty candidate packets.

## Why this matters

For current bounty targets, the highest-value issues are usually not toy payloads. They are product-boundary failures that require owned accounts, object provenance, and controls:

- BOLA / IDOR object ownership;
- role/permission separation;
- file/path handling around upload/import/export/download;
- server-side fetch, webhook, importer, previewer, chatbot, or connector behavior;
- parser/deserialization/import processing;
- upload retrieval/public object exposure;
- runtime XSS only after browser proof.

## Local proof source

- Proof packet: `labs/proofs/realistic_saas_api_multi_class_kali_victim_20260529.md`
- Bundle: `modules/bundles/verified_lab_flow_realistic_saas_api_multi_class.md`
- Artifact root: `<artifact-output-dir>/realistic_saas_api_20260529T063059Z/`
- Target: `<victim-vm>` container `modern-realistic-api`, `http://<victim-vm>:18080`

## Candidate packet template for live lanes

For each route, preserve this shape:

```json
{
  "candidate_id": "<class>-<route>",
  "attacker_objective": "read/change another user, tenant, role, file, callback, or parser-controlled object",
  "path_hypothesis": "specific UI/API route and object/control relation",
  "owned_controls": ["Account A object", "Account B object", "negative control route"],
  "stop_before": ["non-owned data", "callbacks/OAST", "token/API-key creation", "scanner/fuzzer", "report submit"],
  "evidence_minimum": ["positive", "negative", "scope ref", "redacted request/response or screenshot"],
  "status": "candidate|blocked_preserve|bounded_executable"
}
```

## Tactical heuristics

1. BOLA first: look for predictable object IDs and API routes behind normal UI clicks. Never touch non-owned IDs on live targets; use two owned accounts/objects.
2. Role bugs need a negative control: a normal user reading admin data is stronger when another admin endpoint correctly returns 403.
3. File/path bugs should use synthetic markers and patched/negative controls locally before live consideration.
4. SSRF-like features are common in webhooks, URL importers, previewers, document fetchers, and AI/chatbot connectors; live callback/OAST needs explicit operator approval.
5. Parser/deserialization bugs often appear in import, backup, workflow, plugin, model, or document parsing paths; marker-only local proof first.
6. Upload retrieval bugs become valuable when direct URLs, missing auth, content-type confusion, or cross-tenant object access are present.
7. XSS sink evidence is not enough: runtime execution proof must avoid cookies/tokens/keylogging and use a safe DOM marker.

## Current caveat

OWASP crAPI is still the better off-the-shelf target to keep pursuing for realism. This run pulled several crAPI images to `<victim-vm>`, but compose startup did not complete cleanly. The verified tactic evidence therefore comes from the deterministic repo-owned modern API fixture.
