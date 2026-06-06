> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Phase 4A Victim Lab Control + Bounded Report Flow

Session pattern: the operator wanted Hermes to control a separate `<lab-vm>` VM and run a complete OWASP Juice Shop bug-bounty rehearsal with multi-party reviews.

## Durable workflow lessons

### Victim VM control boundary

- VirtualBox control is not the same as guest control. First verify VM presence/running state, NIC modes, Guest Additions properties, SSH reachability, and whether sudo is passwordless before claiming full automation.
- A host-only VM may show only Docker bridge IPs via Guest Additions. If Host-only DHCP is disabled and the guest interface is up without an IP, assign a static lab IP manually first.
- Avoid IP conflicts with the red-team Kali. In this session the attacker used `<lab-ip>`, so the victim was pinned to `<lab-ip>/24`.
- Windows host ICMP may be blocked; `ping <lab-ip>` failing from the victim does not imply lab network failure if TCP/HTTP checks to the victim succeed.

### Safe static-IP setup pattern

Use NetworkManager on the victim for persistent host-only IP, with no default route:

```bash
nmcli connection show
sudo nmcli connection modify "eth0" \
  connection.interface-name "eth0" \
  ipv4.method manual \
  ipv4.addresses "<lab-ip>/24" \
  ipv4.gateway '' \
  ipv4.dns '' \
  ipv4.never-default yes \
  ipv6.method disabled \
  connection.autoconnect yes
sudo nmcli connection up "eth0"
```

Verify:

```bash
ip -br addr show eth0
nmcli -f ipv4.method,ipv4.addresses,ipv4.gateway,ipv4.never-default connection show eth0
```

Expected: `ipv4.method=manual`, `<lab-ip>/24`, no gateway, `ipv4.never-default=yes`.

Pitfall: when writing a remote shell script from the host, quote heredocs so variables such as `$CONN`, `$IFACE`, and `$IP` are not expanded on the host into empty strings before reaching the guest. If a generated script shows `nmcli connection modify ""`, rewrite/re-upload it from a local file or with a single-quoted heredoc.

### Reusable victim service control helper

A useful local helper shape under `setting/local/`:

- SSH to `kali@<victim-ip>` with batch mode.
- `status`: hostname, `ip -br addr`, `docker ps`, and host-side HTTP check.
- `start`: fail closed if the victim interface does not already have the expected host-only IP; then `docker rm -f <name>` and `docker run -d --name <name> -p <victim-ip>:3000:3000 bkimminich/juice-shop`.
- `stop`, `restart`, `logs`.
- Do not pipe guessed passwords into sudo. If sudo is required, write a helper and ask the operator to run it in the VM.

Juice Shop may take several seconds after Docker reports the container as running; retry health after a short wait before declaring failure.

### Bounded end-to-end report flow

For a complete local-lab bug-bounty rehearsal, keep this rhythm:

```text
pre-health
-> baseline recon: curl / whatweb / single-port nmap
-> multi-party review: safety reviewer + attack strategy reviewer
-> selected bounded scripts
-> active checks with pre/post health
-> second multi-party review: safety/result + attack/report
-> candidate packet / gap list / verification plan
-> LAB ONLY pentest report draft
```

Good bounded script set for Juice Shop:

- security headers audit
- minimal CORS audit with crafted benign Origins
- fixed-path metadata checks (`/robots.txt`, `security.txt`, `/.well-known/security.txt`, `/ftp/`, known SPA routes)
- SPA fallback/body-hash classifier to avoid treating every 200 as an exposed file
- `/ftp/` metadata-only verifier: status, title, content-type, hash, visible filenames/sizes only; no recursive download and no file bodies by default
- bounded external scanner import only if it can be constrained and output stays observation-only

### Lab-only plugin prototype pattern

When a new active script is useful but not ready for the production runner, package it as a lab-only prototype under `setting/local/` with a small manifest. Include fields for:

- private/local target gate
- fixed paths only
- max requests / timeout
- no recursion
- no file-body downloads
- no credentials
- no external callbacks
- no destructive actions
- candidate-only output
- manual verification required

Do not wire this prototype into the main runner until it receives a separate reviewed execution-adapter slice.

### Reportability lessons

- `/ftp/` directory listing in Juice Shop is a good lab candidate, but metadata-only evidence is not a confirmed real bug-bounty finding. Manual sensitivity/impact review is required before stronger claims.
- Missing headers are hardening/informational unless chained to a verified impact such as XSS, clickjacking of a sensitive action, cookie weakness, or relevant HTTPS downgrade context.
- `Access-Control-Allow-Origin: *` without credentialed readable behavior is not a CORS vulnerability by itself.
- `security.txt` is expected public metadata.
- SPA fallback 200 responses are common false-positive traps; compare title/body hash with root and a random canary path before creating a candidate.
- A scanner/tool attempt that fails before producing usable observations must be recorded as a limitation, not as finding evidence.

### Aggressive upper-bound testing

Even with local-lab authorization, do not mix destructive/high-volume testing into the normal report rehearsal. Create a separate isolated-snapshot slice first:

- snapshot/recovery point
- host-only isolation and no unnecessary shared folders/clipboard/drag-drop
- explicit operator approval for the aggressive slice
- pre/post health checks
- per-step timeout, request caps, and kill/recovery control
- audit log and redaction
- candidate-only result conversion
- multi-party review before plugin promotion
