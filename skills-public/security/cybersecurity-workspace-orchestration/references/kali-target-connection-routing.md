> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Kali Target-Connection Routing

Use this reference when the operator wants Windows Hermes to remain the central coordinator while Kali VM acts as the target-touching tool lab.

## Durable pattern

- Windows/host Hermes remains the control plane: memory, skills, Obsidian, planning, handoff arbitration, and final reporting.
- Kali VM is the execution plane for authorized target connections, CTF/lab interaction, Linux-native security tools, and worker validation.
- For target-touching work, prefer Kali-originating commands over Windows-host browser/curl when practical. This reduces Windows host exposure, avoids mixing host browser cookies/fingerprints with lab traffic, and keeps security tools isolated.
- Kali VM is not anonymity. NAT/VPN/provider routing may still expose the same network egress. Do not present Kali as hiding identity; describe it as host-isolation and tool-isolation.

## Scope gate remains mandatory

Before any active scan, exploit, brute force, callback, proxy-routed request, or other target-touching automation, confirm one of:

- CTF/training platform
- local intentionally vulnerable lab
- user-owned asset
- written client authorization
- explicit bug bounty scope/rules permitting the technique

A proxy does not expand authorization.

## Preferred SSH-wrapper shape from Windows/Git-Bash Hermes

Use the project wrapper when available:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File './scripts/kali-run.ps1' -Command 'cd ~/projects/cybersec && ./bin/hermes review'
```

Notes:

- The wrapper may start in a remote output directory such as `~/codex-output`; explicitly `cd ~/projects/cybersec` for repo work.
- Non-interactive SSH shells may not have the project `bin/` on PATH; prefer `./bin/hermes` inside the repo.
- Check `.agent.lock` before starting `./bin/hermes cowork`, `./bin/hermes codex`, or `./bin/hermes pipeline`.
- Use read-only checks freely; avoid parallel worker runs when a lock indicates a worker is active.

## When to use Kali

Use Kali for:

- CTF/training/lab HTTP requests and verification.
- Linux-native tools: `nmap`, `ffuf`, `feroxbuster`, `gobuster`, `whatweb`, `sqlmap`, `john`, `hashcat`, `tshark`, `tcpdump`, `impacket`, `proxychains4`.
- Bash/recon/scope script validation where Windows Git-Bash is not representative.
- Offline/dry-run validation of cybersec platform contracts and fail-closed scope behavior.
- Running Claude/Codex workers inside the lab repo when Linux-side context matters.

Use Windows/host Hermes for:

- memory, skills, Obsidian notes, strategic planning, and final synthesis;
- repo file inspection that does not require target contact;
- browser visual QA only when Kali/remote tooling is not practical, and after stating the reason.

## Proxychains posture

Kali is a good place for proxychains/proxychains4 when the purpose is authorized lab routing, Burp/ZAP interception, or controlled SOCKS pivoting.

Allowed examples after scope confirmation:

- Route CLI HTTP tools through local Burp/ZAP for inspection.
- Use a CTF/lab SOCKS tunnel or SSH dynamic forward for pivot exercises.
- Validate a user-owned/internal lab through a documented proxy chain.

Do not use proxychains for:

- unauthorized scanning or exploitation;
- evasion/stealth/anonymization claims;
- rate-limit/source-IP bypass;
- bug bounty targets where program rules disallow proxies, Tor, distributed scanning, or anonymizing infrastructure.

Bug bounty proxy use requires checking the program rules first. Local Burp interception is often acceptable; anonymizing or distributed proxies often are not.

## Communication rule

When switching from Windows to Kali for a target connection, state the routing choice briefly: "I will run the target-touching request from Kali via the SSH wrapper." If Kali is unavailable and Windows must be used, state why before connecting.
