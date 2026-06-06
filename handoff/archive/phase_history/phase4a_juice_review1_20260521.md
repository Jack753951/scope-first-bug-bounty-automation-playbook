> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4A Juice Shop Run — Multi-party Review 1

Target: http://<lab-ip>:3000
Scope: local intentionally vulnerable host-only lab
Run mode: bounded Phase 4A calibration, candidate-only
Reviewer route/tool: Hermes delegate_task subagents
Visible model/runtime: gpt-5.5 as reported by delegate_task

## Baseline inputs

- curl: HTTP 200 OK
- whatweb: OWASP Juice Shop, HTML5, Script[module]
- nmap: 3000/tcp open, HTTP responses, Oracle VirtualBox MAC
- Headers: ACAO `*`, XCTO `nosniff`, XFO `SAMEORIGIN`, Feature-Policy `payment 'self'`, X-Recruiting `/#/jobs`

## Safety reviewer verdict

ACCEPT bounded active checks only:

- security header audit
- benign CORS Origin audit
- fixed endpoint metadata checks
- SPA fallback/content-class verification
- `/ftp/` metadata-only check
- optional bounded Nikto-style baseline only with timeout, single host/port, candidate-only output
- pre/post health checks required

Reject/defer:

- brute force / credential guessing
- sqlmap dump / data extraction
- external callback/OAST/interactsh
- recursive download/mirroring
- destructive or irreversible state changes
- high-volume fuzzing / broad nuclei/ZAP active scan
- automatic confirmed findings

## Attack strategy reviewer verdict

Recommended order:

1. security_headers_baseline
2. cors_behavior_minimal
3. X-Recruiting / metadata classification
4. robots/static metadata fixed paths
5. `/ftp/` metadata-only verifier if indicated
6. SPA fallback content-class verifier
7. bounded Nikto observation import last, observation-only

## Hermes decision

Proceed with bounded active lab checks. Do not execute destructive/aggressive scripts in this run despite local authorization, because the execution-adapter safety controls for destructive testing are not yet implemented and previous bounded scans impacted availability. Treat destructive/max-lab as a separate isolated-snapshot slice.
