> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Incident Response (IR) Reference

Read when the user says any of: "I think we got hacked," "we have a breach," "we found a web shell / ransomware / suspicious process," "what do I do first," or asks how to handle a live security incident.

## Table of contents
1. The 6 IR phases (NIST 800-61 / SANS PICERL)
2. First-hour triage flow
3. Containment patterns by incident type
4. Forensic artefact collection — Linux & Windows
5. Communication patterns (who to tell, when)
6. Evidence handling & chain of custody
7. When to call law enforcement / CERT
8. Common scenarios with response playbook pointers
9. Tools

---

## 1. The 6 IR phases (PICERL / NIST)

| # | Phase | Goal | Don't |
|---|-------|------|------|
| 1 | **Preparation** | Have IR plan, contact tree, runbooks, forensic kit, retainer with DFIR firm if applicable | Wait until the incident to figure out who's on call |
| 2 | **Identification** | Confirm whether this is a real incident; classify severity | Page everyone over a false positive |
| 3 | **Containment** | Stop the bleeding without destroying evidence | Power-off without a memory image (loses RAM evidence) |
| 4 | **Eradication** | Remove root cause: patch, rotate, rebuild | "Just delete the malware and bring it back up" — backdoor likely persists |
| 5 | **Recovery** | Restore service from known-good state, monitor closely | Bring infected backups back |
| 6 | **Lessons Learned** | Post-mortem within 2 weeks, no blame | Skip this — most orgs do, and re-encounter the same incident |

## 2. First-hour triage flow

Use this when the user says "I think we have an incident":

```
┌─────────────────────────────────────────────────────────┐
│ Q1: Is there an active threat (active C2, exfil, etc.)? │
│   YES → containment FIRST, forensics SECOND             │
│   NO  → forensics first, then contain                   │
├─────────────────────────────────────────────────────────┤
│ Q2: Scope?                                              │
│   Single host  → isolate at switch, image RAM + disk    │
│   Multiple hosts / domain → assume DA compromise,       │
│                              treat as Tier-0 incident   │
├─────────────────────────────────────────────────────────┤
│ Q3: Sensitive data potentially exposed?                 │
│   YES → notify legal + privacy team within 24h          │
│         (regulatory clocks: GDPR 72h, HIPAA, etc.)      │
└─────────────────────────────────────────────────────────┘
```

Document everything in UTC timestamps from minute one.

## 3. Containment patterns by incident type

### Web shell on a public-facing server
1. Capture the live shell file + access logs (don't delete yet — evidence).
2. Block at WAF / firewall the inbound interaction patterns.
3. Disable the affected route / virtual host.
4. Audit ALL files modified in the same time window — there are usually more.
5. Rotate any credential the process had access to (DB creds, API keys).
6. Do NOT just delete the shell and bring the site back. Rebuild from clean source.

### Ransomware on endpoints
1. Isolate the host at the switch layer (don't reboot — encryption keys may be in RAM).
2. If feasible, dump RAM with `winpmem` / `lime` (Linux) — keys sometimes recoverable.
3. Check for lateral spread: SMB writes, scheduled tasks, RDP sessions in last 72h.
4. Notify executives, legal, insurance, and law enforcement (most insurance contracts require it).
5. Don't pay before consulting legal + a DFIR firm; many ransomware variants have public decryptors (nomoreransom.org).
6. Restore from backups verified to be from BEFORE the encryption timestamp.

### Compromised cloud account (AWS / Azure / GCP)
1. Rotate the exposed credentials FIRST — even before logging in, if the access key is the suspected vector.
2. Audit IAM activity logs (CloudTrail / Azure Activity / GCP Admin Audit) for the credential's actions.
3. Look for: persistence (new IAM users, access keys, login profiles), data exfil (S3 GetObject bursts, snapshot creates, object replication), spend (crypto mining EC2s).
4. Check for backdoor IAM roles with `AssumeRole` from external accounts.
5. Don't delete the compromised credential's audit trail — disable, don't delete.

### Active Directory compromise (DA / KRBTGT)
1. Assume KRBTGT compromised → all Kerberos tickets are forgeable.
2. Reset KRBTGT password TWICE with replication delay between (≥10h) — single reset leaves a window.
3. Reset all admin passwords; force re-login for all sessions.
4. Audit GPOs for new persistence (scheduled tasks, logon scripts).
5. BloodHound the environment fresh post-recovery — if attack paths existed before, they exist after.

### Insider data exfiltration
1. Don't tip off the insider before legal/HR aligns on next steps.
2. Capture proxy / DLP logs, USB events, email forwarding rules.
3. Preserve their workstation image + cloud account state.
4. Run by legal before any user-facing action.

## 4. Forensic artefact collection

### Linux — minimum viable triage

```bash
# RAM image (need root + matching kernel module)
sudo insmod lime-$(uname -r).ko "path=/mnt/external/mem.lime format=lime"

# Process tree, open sockets, loaded modules
ps auxef > /mnt/external/ps.txt
ss -tnp -tunap > /mnt/external/sockets.txt
lsmod > /mnt/external/lsmod.txt

# Persistence locations
ls -la /etc/cron* /var/spool/cron/crontabs/ /etc/systemd/system/
find / -newer /tmp/incident_start -type f 2>/dev/null > /mnt/external/recent.txt

# Logs
journalctl --since "7 days ago" > /mnt/external/journal.txt
tar czf /mnt/external/var_log.tgz /var/log/ 2>/dev/null

# Bash history for every user (don't forget root)
cat /root/.bash_history /home/*/.bash_history 2>/dev/null
```

Tool: **Velociraptor** for live forensics across many hosts.

### Windows — minimum viable triage

```powershell
# RAM via WinPMem
.\winpmem.exe E:\mem.raw

# KAPE — fast triage collection (forensicartifacts/KAPE)
.\kape.exe --tsource C: --tdest E:\triage --target !BasicCollection --tflush

# Quick wins:
Get-WinEvent -LogName Security -MaxEvents 5000 |
  Where-Object {$_.Id -in 4624,4625,4672,4688,4720,4732,1102}
Get-Service | Where-Object {$_.StartType -eq 'Automatic' -and $_.Status -ne 'Running'}
Get-ScheduledTask | Where-Object {$_.State -eq 'Ready'}
```

Tools: **KAPE** for triage, **Volatility 3** for memory analysis, **Eric Zimmerman tools** (PECmd, RECmd, MFTECmd) for artefact parsing.

### Network artefacts

- pcap from a SPAN port if available.
- Zeek logs (conn / http / dns / ssl) — high-signal, structured.
- Firewall logs around the incident window.
- Proxy logs for outbound destinations.

### Cloud artefacts

| Cloud | Logs |
|-------|------|
| AWS | CloudTrail (control plane), VPC Flow Logs (network), GuardDuty findings, S3 access logs, Config history |
| Azure | Activity Log, Sign-in Logs, Audit Logs (Entra), Defender for Cloud alerts, Sentinel |
| GCP | Cloud Audit Logs, VPC Flow Logs, Security Command Center findings |

Pull these into a SIEM or local Elasticsearch for correlation.

## 5. Communication patterns

| Audience | When | What |
|----------|------|------|
| IR commander | T+0 | Activate IR plan |
| Executive (CEO/CTO) | T+1h or earlier if critical | Severity, business impact, what we're doing |
| Legal counsel | T+1h | Regulatory exposure (GDPR/HIPAA/PCI), evidence handling |
| Privacy officer / DPO | T+1h if PII involved | Regulatory clock starts |
| Customers / users | When facts are confirmed, not before | Plain-language disclosure, what happened, what to do |
| Regulator | Per regulation (often 72h) | Formal notification |
| Law enforcement | Severe / criminal — see §7 | |
| Public press | Last, with PR / legal review | |
| Internal staff | Need-to-know during, broader after | Avoid speculation |

Templates: keep three — internal status, customer notification, regulator notification — drafted in advance.

## 6. Evidence handling & chain of custody

- Every artefact file: SHA256 hash on collection, recorded in evidence log.
- Each evidence item gets ID, who collected, when (UTC), how, where stored.
- Disk images: bit-for-bit (`dd` / `dc3dd` / `FTK Imager`). Verify hash before AND after each transfer.
- Keep originals read-only (write-blocker for physical drives, snapshot for VMs).
- Work from copies, not originals.
- Document analyst actions in the case notes — what you ran, what it returned.

If the incident may go to court or regulators: get an external DFIR firm involved early. They handle chain-of-custody to evidentiary standard.

## 7. When to call law enforcement / CERT

Call when:
- Ransomware (most insurance / regulatory frameworks require it).
- Suspected nation-state activity.
- Insider with criminal intent (theft, sabotage).
- Cross-border data theft.
- Targeting of critical infrastructure.

Channels:
- **US**: FBI IC3 (ic3.gov), CISA (cisa.gov/report), local FBI field office for serious cases.
- **UK**: NCSC (report.ncsc.gov.uk), Action Fraud.
- **EU**: National CERT (e.g. CERT-EU) + national data protection authority.
- **Taiwan**: 國家資通安全研究院 (NICS) / TWCERT/CC.
- **Japan**: JPCERT/CC.

Don't talk to media before law enforcement clears it.

## 8. Common scenarios — playbook pointers

| Scenario | Most likely tactic (ATT&CK) | Containment §3 case |
|----------|----------------------------|---------------------|
| Web shell on PHP / Java app | T1505.003 | Web shell |
| Encrypted files + ransom note | T1486 + T1490 | Ransomware |
| Sudden AWS bill spike | T1078.004 + T1496 (resource hijacking) | Cloud account |
| New domain admin you didn't create | T1098 + T1136.002 | AD compromise |
| Outbound traffic to known C2 | T1071 / T1572 | Single host |
| MFA-bypass login from unknown country | T1078 | Cloud account |
| Phishing landing page on your domain | T1583 (resource development) | Web shell-like |

## 9. Tools

| Purpose | Tool |
|---------|------|
| Triage collection (Windows) | KAPE, Velociraptor |
| Triage collection (Linux/Mac) | Velociraptor, UAC |
| Memory analysis | Volatility 3 |
| Disk analysis | Autopsy, X-Ways, FTK |
| Timeline / super-timeline | plaso (log2timeline), Timeline Explorer |
| Live response | Velociraptor, GRR Rapid Response |
| Hunting on logs | osquery + Fleet, Wazuh |
| YARA scanning | thor-lite (commercial), loki, yara-cli |
| Cloud IR | Prowler (audit), CloudCustodian, Stratus Red Team (emulation) |
| Comms / case mgmt | TheHive + Cortex, Splunk SOAR |

---

## What to refuse

- Helping the user **cover up** an incident (deleting logs, falsifying timestamps, withholding regulatory notifications).
- "I want to access X account — I think it's mine" — not your job. Account recovery is via the provider.
- "Help me reverse this ransomware key out of memory" → fine in principle, but if the user is rushing to avoid notification, redirect to legal first.
