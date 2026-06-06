> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Modern API Lab Wave 2

Status: completed / disposable target extended and tested
Date: 2026-05-22
Route/tool: Windows Hermes control plane -> SSH/SCP -> `<attacker-vm>` -> Chromium/curl/Python -> local target `http://127.0.0.1:18080`
Target source: `labs/modern_vuln_api/modern_vuln_api.py`
Runner: `labs/modern_vuln_api/modern_api_wave2_test.sh`
Artifacts: `<artifact-output-dir>/modern_api_wave2_20260522T022303Z/`

## Why this wave was run

Wave 1 verified IDOR, upload retrieval, and isolated SSRF. Wave 2 extended the same disposable target to cover remaining high-value modern lab gaps:

- reliable browser-runtime XSS proof;
- bounded XXE safe marker proof;
- bounded unsafe deserialization gadget proof.

## Results

### Browser runtime XSS

Bundle:

`modules/bundles/verified_lab_flow_modern_api_xss_runtime_proof.md`

Evidence:

```text
runtime_marker=yes
DOM contains: <body data-xss="XSS_RUNTIME_MARKER">
```

### Bounded XXE marker

Bundle:

`modules/bundles/verified_lab_flow_modern_api_xxe_safe_marker.md`

Evidence:

```text
POST /xxe -> 200
marker_found=yes
marker=XXE_SAFE_MARKER_HERMES_LOCAL_LAB
```

### Bounded deserialization gadget

Bundle:

`modules/bundles/verified_lab_flow_modern_api_deserialization_bounded_gadget.md`

Evidence:

```text
deserialize -> 200
log_status=200
marker_found=yes
DESER_SAFE_MARKER_HERMES_LOCAL_LAB
```

## Health

```text
pre_health: 200
post_health: 200
```

## Boundaries

- No public targets.
- No credential theft XSS payload.
- No external callback.
- XXE reads only a safe marker file.
- Deserialization payload invokes only a bounded in-process marker function, no shell.

## Cleanup

The target is disposable and can be stopped on Kali with:

```bash
~/hermes-labs/modern_vuln_api/stop_modern_vuln_api.sh 18080
```

## Next target additions

- Install Docker/Compose on Kali and add crAPI/WebGoat/Vulhub selected targets.
- Add a persistent report generator that converts verified bundles into evidence-driven lab reports.
- Use acquired GitHub tools (Arjun/Dalfox/XSStrike/jwt_tool) only after source review and bounded wrappers.
