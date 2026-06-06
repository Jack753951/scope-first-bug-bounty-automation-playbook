> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Docker-backed WebGoat lab route

Session-derived reference for Cybersec Lab Phase 4B local-learning work.

## Stable role split

Use two Kali VMs when Docker-backed vulnerable targets are available:

- Windows Hermes host: control plane, orchestration, repo/handoff updates, VirtualBox control.
- `<lab-vm>`: attacker/tester plane for target-touching tools, browser/runtime checks, curl/nmap/ffuf/nikto/sqlmap-class work, artifact collection.
- `<lab-vm>`: Docker target host for vulnerable apps such as Juice Shop and WebGoat/WebWolf.

This is preferable to installing Docker on the attacker VM when the victim VM already hosts containers.

## Expected host-only topology

- `<lab-vm>`: host-only IP commonly `<lab-ip>`.
- `<lab-vm>`: host-only IP commonly `<lab-ip>`.
- Target services are reached from aggressive via victim host-only IP, for example:
  - `http://<lab-ip>:3000/` Juice Shop
  - `http://<lab-ip>:8080/WebGoat/login`
  - `http://<lab-ip>:9090/WebWolf/login`

Verify actual IPs each session; do not hard-code if the VM has changed.

## NAT discipline

For local lab target-touching execution, both VMs should return to host-only/no-Internet state after downloads or image pulls.

Verification pattern:

1. VirtualBox NIC2 is `null` or cable disconnected.
2. Inside each VM, `eth1` is down or absent.
3. `ip route` has only host-only/docker routes, no default route via NAT.
4. DNS or HTTP test to an Internet hostname fails.
5. Aggressive-to-victim target URLs still return expected HTTP statuses.

Do not rely only on VirtualBox guest properties; they may retain stale NAT IP values after NIC2 is disabled. Prefer in-guest `ip addr` / `ip route` / connectivity checks.

## Docker binding caveat

Docker containers may bind to the victim host-only IP rather than `127.0.0.1`. A service can be healthy from the attacker VM at `http://<lab-ip>:<port>` while `curl http://127.0.0.1:<port>` inside victim fails. Treat the attacker-to-victim route as authoritative for this lab architecture.

## WebGoat baseline before lesson proofs

Before attempting authenticated lesson proofs:

- Confirm WebGoat login/registration return 200.
- Confirm WebWolf login returns 200.
- Confirm known ports with a bounded scan of 8080/9090 only.
- Capture DOM/title markers with a browser/runtime check when available.
- Record artifacts and pre/post health.

Baseline readiness is a `valuable target-readiness` bundle, not a vulnerability proof.

## Required WebGoat capability lanes

The operator explicitly wants local-lab capability building for:

- Access Control / IDOR-style lessons
- JWT / token lessons
- Reflected XSS lessons
- Path traversal safe-marker lessons

These can be higher-risk if misused, but should not be avoided in the authorized local lab. Execute one lesson per run with bounded payloads, throwaway users/tokens, no credential theft, no external callbacks, no destructive writes, no real secret reads, no shells/persistence, pre/post health, and artifacted request/response/session/DOM evidence.
