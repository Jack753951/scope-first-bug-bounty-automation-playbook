> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# NAT Docker Attempt and Source Wrapper Wave 1 2026-05-22

Status: Docker blocked by sudo-password handling policy; NAT closed; source-reviewed wrapper wave completed
Repo handoff: `<user-home>`
Artifacts: `<user-home>`

## Key points

- Opened NAT on `<lab-vm>` under operator authorization.
- Reboot exposed a boot blocker: missing VirtualBox shared folder `hacking`; fixed by re-adding host path `<user-home>`.
- Kali recovered with `eth0=<lab-ip>`, `eth1=NAT`, and Internet OK.
- Docker install could not proceed because sudo required a password and piping a guessed/default password was blocked by local safety policy.
- NAT was closed afterward and Internet verified closed.

## Continued testing

Added and ran `labs/modern_vuln_api/source_reviewed_wrapper_wave1.sh`.

This wrapper used Exploit-DB / PayloadsAllTheThings / Arjun / Dalfox / XSStrike patterns but did not execute raw exploit scripts.

Results:

- XSS runtime marker: yes
- Bounded XXE marker: yes
- Upload marker retrieval: yes
- IDOR object markers: yes
- Pre/post health: 200/200

## Manual prerequisite for Docker-backed targets

Run inside Kali when ready:

```bash
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y docker.io docker-compose-plugin docker-compose
sudo systemctl enable --now docker
sudo usermod -aG docker kali
```
