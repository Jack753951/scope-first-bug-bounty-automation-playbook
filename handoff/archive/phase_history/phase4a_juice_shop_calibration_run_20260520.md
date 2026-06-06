> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4A Juice Shop Calibration Run — 2026-05-20

Status: in progress / first low-risk baseline completed
Prepared by: Hermes
Scope class: local intentionally vulnerable app controlled by operator
Target: OWASP Juice Shop on victim Kali
Target URL: http://<lab-ip>:3000
Attacker VM: kali-linux-2026.1-virtualbox-amd64 / <lab-ip>
Victim VM: <victim-vm> / <lab-ip>

## Authorization and safety boundary

This run is limited to the local VirtualBox host-only lab. The target is an intentionally vulnerable local app selected by the operator for Phase 4A calibration.

Allowed in this first slice:

- reachability check;
- HTTP header capture;
- light web fingerprinting;
- single-port service detection on the already-known Juice Shop port 3000;
- candidate-only observations.

Not authorized in this slice:

- brute force;
- heavy fuzzing;
- exploit chaining;
- callbacks/OAST;
- credential theft or loot collection;
- destructive tests;
- public target testing;
- report submission;
- automatic confirmed findings.

## VM isolation state observed from VirtualBox

Victim `<victim-vm>`:

```text
VMState=running
nic1=hostonly
nic2=null
clipboard=bidirectional
clipboard_file_transfers=off
draganddrop=disabled
shared folder mapping: none observed in machine-readable output
snapshot=setup-complete-with-tools
```

Red-team Kali `kali-linux-2026.1-virtualbox-amd64`:

```text
VMState=running
nic1=hostonly
nic2=nat
clipboard=bidirectional
clipboard_file_transfers=off
draganddrop=bidirectional
snapshot=security-runtime-20260518-140349
```

## Red-team Kali baseline command

Executed from Windows/Hermes through `scripts/kali-run.ps1` against red-team Kali `<lab-ip>`:

```bash
TARGET=http://<lab-ip>:3000
HOST=<lab-ip>
curl -sS -I "$TARGET"
whatweb "$TARGET"
nmap -sV -Pn -p 3000 "$HOST"
```

Raw red-team output was saved on red-team Kali under:

```text
/home/kali/phase4a-calibration/juice-shop-20260520T101058Z/baseline.txt
```

Note: the wrapper output had a harmless quoting issue around one `tr` line used only for formatting the red-team IP summary; the actual curl/whatweb/nmap checks completed.

## Baseline observations

### HTTP headers

```text
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Feature-Policy: payment 'self'
X-Recruiting: /#/jobs
Content-Type: text/html; charset=UTF-8
Content-Length: 9903
```

### WhatWeb

```text
http://<lab-ip>:3000 [200 OK] Country[RESERVED][ZZ], HTML5, IP[<lab-ip>], Script[module], Title[OWASP Juice Shop], UncommonHeaders[access-control-allow-origin,x-content-type-options,feature-policy,x-recruiting], X-Frame-Options[SAMEORIGIN]
```

### Nmap single-port service detection

```text
3000/tcp open  ppp?
MAC Address: 08:00:27:ED:5B:F6 (Oracle VirtualBox virtual NIC)
```

Nmap did not classify the HTTP service cleanly and emitted an unrecognized-service fingerprint. This is not a vulnerability finding; it is a calibration observation that scanner output can be noisy/misleading and should be reviewed before becoming any candidate finding.

## Candidate-only observations

1. Target is reachable from the red-team Kali over host-only networking.
2. The app identifies as OWASP Juice Shop via page title/fingerprint.
3. Header capture contains potentially interesting training-lab headers (`X-Recruiting`, permissive CORS header), but these are not confirmed vulnerabilities.
4. Nmap service detection is noisy on port 3000 and should not be trusted as a product/version finding.

## Report-readiness notes

This run is not report-ready and should not produce confirmed findings. It only proves the lab link and baseline evidence capture.

Before Phase 4B lab-to-report trial, the workflow needs:

- a lab scope artifact separate from real bug-bounty program scope;
- a cleaner command wrapper that writes local evidence packets with timestamps and target metadata;
- candidate-finding schema mapping for low-risk observations;
- false-positive review notes for scanner output;
- manual verification checklist items before any severity/impact language.

## Next safe calibration step

Recommended next slice:

1. Record a narrow lab scope/rules artifact for Juice Shop.
2. Add a small `phase4a` evidence collection wrapper that runs only approved low-risk checks against the exact URL.
3. Produce a candidate-only review packet from the baseline observations.
4. Keep Nikto/Nuclei/fuzzing/brute-force/exploit PoCs out until a separate explicit lab-only review approves them.
