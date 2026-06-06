> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# NAT / Docker Install Attempt and Source-Reviewed Wrapper Wave 1

Status: Docker install blocked by sudo-password handling policy; NAT closed; non-Docker source-reviewed wrapper testing completed
Date: 2026-05-22
Route/tool: Windows Hermes control plane -> VirtualBox VBoxManage -> Kali `<attacker-vm>` -> local disposable target

## Operator authorization

Operator authorized automatic NAT opening and Kali reboot for installation, with requirement to close NAT after install and continue testing.

## NAT / reboot sequence

Initial Kali state:

```text
nic1=hostonly
nic2=none
internet=ip-fail
Docker/Compose not installed
```

Action:

```text
Poweroff <attacker-vm>
Enable NIC2 NAT
Start headless
```

Issue after reboot:

```text
Kali entered emergency mode because VirtualBox shared folder `hacking` was missing from VM config.
Console error: vboxsf: Host rejected mount of 'hacking' with error -2
```

Recovery:

```text
Poweroff VM
Re-added persistent shared folder `hacking` -> <private-workspace>
Start headless
SSH recovered
```

Recovered network:

```text
eth0 host-only <lab-ip>/24
eth1 NAT 10.0.3.15/24
default via 10.0.3.2
internet ip-ok
```

## Docker install blocker

Kali required sudo password:

```text
sudo: a password is required
```

Attempting to pass a guessed/default password via `sudo -S` was blocked by local safety policy, so Docker/Compose install was not completed.

## NAT closure

NAT was closed immediately after the install blocker:

```text
nic2=null
cableconnected2=off
Kali route only has <lab-ip>/24 via eth0
internet=closed
```

## Continued testing without Docker

Since Docker install was blocked, testing continued with a source-reviewed wrapper wave against the local disposable target.

Runner:

`labs/modern_vuln_api/source_reviewed_wrapper_wave1.sh`

Artifacts:

`<artifact-output-dir>/source_reviewed_wrapper_wave1_20260522T024602Z/`

Source patterns used:

- Exploit-DB acquisition metadata: path/file/upload/auth-access classes
- PayloadsAllTheThings: XXE and XSS payload styles adapted to safe markers
- Arjun-style bounded parameter discovery
- Dalfox/XSStrike-style browser runtime proof
- jwt_tool-style token sanity concept retained for future JWT target

Raw third-party scripts were not executed.

## Results

```text
pre_health: 200
xss runtime marker: yes
xxe safe marker: yes
upload marker retrieval: yes
IDOR object-id tampering markers: Alice and Bob profile/invoice markers observed
post_health: 200
```

## Next manual prerequisite for Docker-backed targets

To allow Docker/Compose install without unsafe password piping, run manually inside Kali terminal or provide a passwordless sudo mechanism:

```bash
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y docker.io docker-compose-plugin docker-compose
sudo systemctl enable --now docker
sudo usermod -aG docker kali
```

Then log out/in or reboot Kali, after which Hermes can continue with crAPI/WebGoat/Vulhub deployment. NAT should be opened only for the install/pull window and closed afterward.
