> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Max-impact local-lab proofs and DVWA command-injection lessons

Session-derived guidance for authorized, recoverable local靶機 work where the operator wants one vulnerability to demonstrate the largest safe impact.

## Operator preference captured

For local/recoverable靶機, prefer one-vulnerability max-impact proofs over shallow metadata-only completion when safe and useful. High-value proof shapes include:

- server-side execution identity (`id`, `whoami`, service user);
- lab-only marker file write/readback under a disposable path such as `/tmp/hermes_*`;
- isolated host-only callback/control evidence when the listener path is explicitly reachable;
- cleanup/restore evidence after the run;
- explicit distinction between verified impact and attempted-but-not-verified impact.

Keep refusing or downgrading anything that would become public-target abuse, stealth persistence, credential theft, uncontrolled propagation, real exfiltration, or host/OS destruction outside the disposable lab/snapshot.

## DVWA command-injection pattern

A disposable `vulnerables/web-dvwa:latest` container can be used for command-injection max-impact training when existing WebGoat/Juice Shop lanes do not demonstrate OS execution. A successful wave proved:

- target: Docker-published DVWA on `<lab-vm>`;
- tester: `<lab-vm>`;
- vulnerability: DVWA low-security command injection;
- evidence: response contained `uid=33(www-data) gid=33(www-data)`, `www-data`, and a lab marker string read back from `/tmp/<marker>.txt`;
- cleanup: remove temporary impact container and verify normal lab services.

Reusable artifact locations from the session:

- runner: `scripts/labs/dvwa_command_injection_impact_wave1.sh`;
- bundle: `modules/bundles/verified_lab_flow_dvwa_command_injection_container_control.md`;
- handoff: `handoff/dvwa_command_injection_impact_wave1_20260522.md`.

## Callback/control pitfall

Do not claim callback/control just because a payload attempted it. In the session:

- command execution and marker write/readback were verified;
- outbound callback was not verified in the first run because high-port listeners on `<lab-vm>` and Windows host were unreachable from the target path;
- a later true attacker-side callback proof succeeded with a Docker-published listener and was standardized in the repo as `handoff/dvwa_attacker_callback_evidence_packet_standard_20260523.md`;
- future reruns should use the current attacker route `<lab-vm>`; older artifact labels that say `<lab-vm>` are historical metadata unless project handoff supersedes this;
- a PHP `file_get_contents()` callback can hang the web request if no timeout is set; always set a short timeout or separate callback attempt from the core command-execution evidence.

For future callback/control drills, first build/verify callback infrastructure, preferably:

1. Docker-published callback listener with known reachable host-only IP/port;
2. explicit operator-approved host-only firewall opening; or
3. dedicated callback lab container with pre/post health and cleanup.

Only promote callback/control to `verified-impact` after `requests.jsonl` or equivalent listener evidence shows the target reached the listener. If the runner can use either a local listener or an external/Docker listener, record which listener path is authoritative and pass/record an explicit external callback log path (for example `EXTERNAL_CALLBACK_LOG`) so summary counts and evidence artifacts cannot diverge.

## Port/firewall lesson

In this two-VM lab, host Python processes bound to arbitrary victim ports may be blocked even when listening on `0.0.0.0`; Docker-published ports on the victim were reachable. For target services or callback listeners that must be reached across VMs, prefer Docker-published ports or explicitly verified firewall rules. Capture this as route design, not as a durable claim that any tool is broken.

## Closeout requirement

For this user's lab tests, every closeout should include:

- `對專案有什麼幫助`: capability growth, evidence quality, automation/readiness improvement, blockers learned;
- `新增/更新了什麼`: scripts, bundles, handoffs, Obsidian notes, artifacts, blockers, reusable workflow changes.
