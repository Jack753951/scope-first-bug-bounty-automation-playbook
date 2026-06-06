> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# SSRF / callback-style local lab pattern — 2026-05-23

Use this reference when running one-vulnerability local-lab waves that need attacker-side callback evidence, especially SSRF, XXE, command-injection callbacks, or bounded deserialization callbacks.

## Durable workflow lessons

1. Start with OSS-first reconnaissance every time.
   - Check mature sources before writing or changing a runner/bundle: PayloadsAllTheThings, SSRFmap, nuclei templates, OWASP/CWE/NVD/CISA as relevant, training-lab upstream source, and existing project scripts.
   - Record the decision as `adopt`, `wrap`, `adapt`, `reference-only`, or `write-custom`.
   - Apply the same rule to bundle optimization, not only new scripts.

2. Prefer local host-only callback evidence over public OAST for default lab waves.
   - Public OAST/interactsh-style patterns may be useful references, but local authorized lab default should use a host-only attacker listener with a unique marker.
   - Evidence must include listener log, marker, source IP/context, target pre/post health, cleanup/recovery, and boundary notes.

3. If direct host listeners or target processes are unreliable, use a Docker-published listener/target instead of repeatedly reprobeing.
   - Pattern: attacker VM publishes a small callback listener container on host-only IP/port.
   - Pattern: victim VM publishes the disposable vulnerable target container on host-only IP/port.
   - Verify target-to-listener reachability with a benign `/ping?marker=RUN_ID` before attempting the vulnerability trigger.
   - Do not hard-code this as the only route; it is a robust fallback/standard route when plain host listeners are blocked, firewalled, or inconsistent.

4. Temporary NAT / local target expansion is allowed for this project when useful.
   - It may be used to pull images, install/update tools, or add/modify recoverable local vulnerable targets.
   - Always document source/provenance/version/license when applicable.
   - Close NAT afterward and verify Internet is closed on each VM touched.
   - Keep the work local and recoverable; no public/unknown targets, cloud metadata probing, public OAST by default, credential theft, exfiltration, persistence, or uncontrolled DoS.

5. Never overclaim a blocked/deferred wave.
   - If the final trigger is denied by the safety layer or otherwise not executed, record setup/prep as valuable but mark the proof `blocked/deferred`, not `verified-impact`.
   - Do not retry around explicit `Do NOT retry` style denials; switch lanes or prepare a narrower reviewed runner.

## Minimal evidence packet for callback waves

- OSS/source references saved path.
- Decision: adopt/wrap/adapt/reference-only/write-custom.
- Route: control plane, attacker VM/container, victim VM/container, host-only IPs/ports.
- NAT windows opened/closed, with final Internet-closed verification.
- Pre-health of target.
- Callback listener baseline.
- Trigger payload with unique marker, if permitted.
- Positive callback log and negative/control result, if executed.
- Post-health and cleanup result.
- Explicit status: `verified-impact`, `attempted-not-verified`, or `blocked/deferred`.

## Session-specific artifact examples

- Handoff: `<private-workspace>\handoff\modern_api_ssrf_attacker_callback_attempt_20260523.md`
- Artifacts: `<private-workspace>\<artifact-output-dir>\modern_api_ssrf_attacker_callback_20260523T035629Z\`
- OSS refs: `<private-workspace>\setting\local\oss_refs\ssrf_callback_20260523\`
