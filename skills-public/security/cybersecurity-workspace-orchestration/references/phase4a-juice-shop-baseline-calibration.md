> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Phase 4A Juice Shop Baseline Calibration

Use this reference when the operator has a two-Kali VirtualBox lab and wants Hermes to begin controlled Phase 4A calibration against a local OWASP Juice Shop target.

## Durable pattern

Roles:

- Windows/Hermes: control plane, VirtualBox settings, repo/handoff artifacts.
- Red-team Kali: tool runner for authorized lab checks.
- Victim Kali: intentionally vulnerable apps only, e.g. Juice Shop/DVWA/WebGoat.

Recommended first target shape:

```text
Target class: local intentionally vulnerable app
App: OWASP Juice Shop
Victim URL: http://<victim-host-only-ip>:3000
Allowed actions: reachability, HTTP headers, light fingerprinting, single known-port service detection
Forbidden by default: brute force, heavy fuzzing, exploit chaining, callbacks/OAST, credential/loot collection, public targets, report submission, automatic confirmed findings
```

## VM safety state before baseline checks

For the victim VM after setup/image pulls and snapshot:

```text
nic1 = hostonly
nic2 = null / NAT off
shared folder = removed or at least unmounted; transient mappings may require guest unmount + power cycle
clipboard = operator choice; bidirectional is acceptable for controlled lab convenience if file transfer is off
drag-and-drop = disabled
clipboard file transfer = off
```

For the red-team Kali:

```text
host-only IP assigned, e.g. <lab-ip>/24
NAT may remain on for tooling/control unless entering stricter isolation
SSH reachable from Windows/Hermes if wrappers are configured
```

If Host-only DHCP is disabled and the red-team Kali has no `192.168.56.x`, set it manually inside the red-team VM:

```bash
sudo ip addr add <lab-ip>/24 dev eth0
sudo ip link set eth0 up
```

## Juice Shop binding pitfall

`127.0.0.1:3000` is per-machine localhost. If the victim script says `Juice Shop local URL: http://127.0.0.1:3000`, red-team Kali must still use the victim host-only IP, not its own localhost:

```text
Red-team URL: http://<lab-ip>:3000
```

Check the victim Docker binding:

```bash
sudo docker ps
sudo ss -ltnp | grep ':3000'
```

If the container is bound only to `127.0.0.1:3000`, restart it on all interfaces:

```bash
sudo docker ps -q --filter ancestor=bkimminich/juice-shop | xargs -r sudo docker rm -f
sudo docker run -d --name juice-shop-lab -p 0.0.0.0:3000:3000 bkimminich/juice-shop
```

Patch local helper scripts only if needed:

```bash
cp ~/phase4a-lab/run-juice-shop.sh ~/phase4a-lab/run-juice-shop.sh.bak
sed -i 's/127\.0\.0\.1:3000:3000/0.0.0.0:3000:3000/g' ~/phase4a-lab/run-juice-shop.sh
sed -i 's/-p 3000:3000/-p 0.0.0.0:3000:3000/g' ~/phase4a-lab/run-juice-shop.sh
```

## First low-risk baseline

Run from the red-team Kali, not the victim:

```bash
TARGET=http://<lab-ip>:3000
HOST=<lab-ip>
curl -sS -I "$TARGET"
whatweb "$TARGET"
nmap -sV -Pn -p 3000 "$HOST"
```

Expected signs:

- `curl`: `HTTP/1.1 200 OK`.
- `whatweb`: title `OWASP Juice Shop`.
- `nmap`: `3000/tcp open`; service may be misclassified (for example `ppp?`) despite HTTP response. Treat that as scanner-noise calibration, not a finding.

When using the repo's Windows-to-Kali bridge, override the red-team Kali host if the default config still points to the victim:

```bash
powershell.exe -NoProfile -ExecutionPolicy Bypass -File './scripts/kali-run.ps1' \
  -HostName '<lab-ip>' \
  -Command 'TARGET=http://<lab-ip>:3000; curl -sS -I "$TARGET"; whatweb "$TARGET"; nmap -sV -Pn -p 3000 <lab-ip>'
```

## Proxychains/Burp guidance

Do not add proxychains by default for this baseline. Direct host-only routing is simpler and reduces ambiguity:

```text
red-team Kali -> victim host-only IP -> Juice Shop
```

Use browser/Burp proxy settings only when the task is specifically to calibrate manual web testing through Burp. Prefer tool-specific proxy flags over proxychains for HTTP tools. Avoid wrapping nmap in proxychains for this local web baseline.

## Evidence and closeout

For the first Phase 4A slice, save a candidate-only handoff file with:

- authorization/scope statement;
- VM isolation summary;
- exact target URL and attacker/victim IPs;
- commands run;
- curl headers;
- whatweb output;
- single-port nmap output;
- false-positive/noise notes;
- explicit statement that no confirmed vulnerabilities or report submissions were produced.

A suitable path is:

```text
handoff/phase4a_juice_shop_calibration_run_<YYYYMMDD>.md
```

Next safe step is a narrow lab-scope/rules artifact plus candidate-only evidence packet. Do not escalate to Nikto/Nuclei/ffuf/gobuster/sqlmap/bruteforce/fuzz/exploit PoCs without a separate lab-only approval and review tier decision.
