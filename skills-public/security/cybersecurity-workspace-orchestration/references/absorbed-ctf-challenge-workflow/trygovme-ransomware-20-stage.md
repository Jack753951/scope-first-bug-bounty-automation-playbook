> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# TryGovMe-style ransomware SIEM simulator: 20-stage timeline pattern

Use this as a reference when a SOC/threat-hunting simulator expects a long attack-chain timeline (around 20 stages) rather than 3-7 consolidated phases.

## When to use

- Prompt describes ransomware, multiple encrypted hosts, SIEM outage, suspicious installer/tooling IOCs, or employee/host mapping.
- The simulator has many timeline slots or the user says it expects ~20 stages.
- Logs are read-only ELK/Kibana/SIEM data from a training lab.

## Investigation order

1. Confirm training/lab scope and stay read-only in SIEM.
2. Query broad IOCs for the full incident day:
   - suspicious domain/IP
   - installer/archive names and extensions
   - PowerShell/script names
   - dropped EXE/DLL names
   - credential tools (`mimikatz`, `SharpKatz`, `sekurlsa`, `DCSync`)
   - remote execution markers (`Invoke-Command`, `wsmprovhost`, WinRM)
   - ransomware process and encrypted extension
3. Build a chronological evidence table before mapping tactics.
4. Pivot on encrypted extension and ransomware process across all hosts. Do not trust the prompt's role wording (for example, "another developer") over SIEM evidence; use host/user mappings from logs.
5. Split late activity if the form supports it: credential access, alternate credentials, account manipulation, AD discovery, remote staging, and impact should be separate stages.

## 20-stage shape

Use exact timestamps, users, assets, and IOCs from logs; this is the stage taxonomy to adapt:

1. Suspicious installer/archive downloaded by initial user.
2. Installer/archive executed by user (`msiexec`, archive utility, package manager, etc.).
3. Installer launches script interpreter (`powershell.exe iex/iwr`, `cmd`, `wscript`, etc.).
4. Malicious domain/IP resolution or first outbound contact.
5. Remote script retrieved/executed; cite script-block logs when available.
6. Legitimate/decoy software installed to mask compromise.
7. Malicious binary dropped from attacker infrastructure.
8. Persistence created (`sc.exe create`, Run key, scheduled task, service install).
9. Persistence executed or service started.
10. Malicious DLL/second payload dropped.
11. Proxy execution (`rundll32`, `regsvr32`, `mshta`, service host, etc.).
12. Credential tool downloaded or staged.
13. Credential tool executed (for example Mimikatz/SharpKatz).
14. Alternate credentials / pass-the-hash / spawned shell context observed.
15. Domain account manipulation attempt (`net user`, password reset, group add).
16. Domain account manipulation confirmed with framework/tool (`PowerView`, AD cmdlets, etc.).
17. Higher-value credential collection such as DCSync.
18. AD/domain reconnaissance (`SharpHound`/BloodHound, account/group/session discovery).
19. Ransomware staged remotely to another host (`Invoke-Command`, WinRM, SMB copy, scheduled task).
20. Ransomware executed and encrypted files; include all affected hosts/users and extension/ransom note.

## MITRE mapping reminders

- Script launch: `Execution` / `Command and Scripting Interpreter`.
- Ingress tool transfer: `Command and Control` or `Command and Control` / `Ingress Tool Transfer`, depending on simulator taxonomy.
- Windows service: `Persistence` / `Create or Modify System Process: Windows Service`.
- `rundll32`: `Defense Evasion` or `Execution` / `System Binary Proxy Execution: Rundll32`.
- Credential tool / DCSync: `Credential Access` / `OS Credential Dumping` or `DCSync` if available.
- Pass-the-hash: `Lateral Movement` / `Use Alternate Authentication Material: Pass the Hash`.
- Account password reset or group manipulation: `Persistence` or `Credential Access` / `Account Manipulation`.
- BloodHound/SharpHound: `Discovery` / account, group, domain trust, or permission discovery.
- Remote PowerShell / WinRM: `Lateral Movement` / `Windows Remote Management`.
- Encryption extension/ransomware: `Impact` / `Data Encrypted for Impact`.

## Kibana/ELK querying technique

When browser UI automation is awkward, Dev Tools can be queried from the logged-in browser context via Kibana's console proxy. Use POST to the proxy even when the Elasticsearch method is GET/POST, and include `kbn-xsrf: true`:

```javascript
fetch('/api/console/proxy?path=winlogbeat-*/_search&method=POST', {
  method: 'POST',
  headers: {'kbn-xsrf': 'true', 'content-type': 'application/json'},
  body: JSON.stringify({
    size: 50,
    sort: [{'@timestamp': 'asc'}],
    query: { query_string: { query: '"777zzz" OR "bomb.exe" OR "sekurlsa::pth"' } }
  })
}).then(r => r.json())
```

For aggregations, use `.keyword` fields (for example `host.hostname.keyword`, `user.name.keyword`, `process.executable.keyword`) because text fields cannot be aggregated without fielddata.

## Form-filling guidance

- Keep each description outcome-based: evidence + implication + follow-on result, not only "PowerShell observed". TryGovMe feedback often marks descriptions incomplete when they omit what the command caused next, such as a script downloading payloads, creating a service, dumping credentials, moving laterally, or encrypting files.
- Include all four evidence anchors in download/execution descriptions when available: source URL/domain/IP, destination path, executing process/command line, and host/user context. Missing download source, exact directory, or follow-on execution is a common grading failure.
- Prefer ATT&CK sub-techniques over parent technique IDs. Parent IDs such as `T1059`, `T1543`, `T1218`, and `T1003` may be marked wrong even when semantically close. Try likely child mappings first: `T1059.001` PowerShell, `T1543.003` Windows Service, `T1218.011` Rundll32, `T1003.001` LSASS Memory, `T1003.006` DCSync, `T1550.002` Pass the Hash, `T1021.006` WinRM, `T1569.002` Service Execution, `T1486` Data Encrypted for Impact.
- Treat timestamp as the grader's expected key event time, not necessarily the first related event. If a stage gets timestamp-only feedback wrong, try the timestamp for the decisive result: PowerShell spawn rather than MSI launch, payload execution rather than file download, or ransomware process start rather than the first bulk encrypted-file create.
## Feedback-driven refinement lessons

When a TryGovMe/SOC simulator summary exposes breakdowns for techniques, tactics, assets, or IOCs, treat that feedback as an evidence map rather than a simple grade.

- Reconstruct expected stage buckets from the breakdown: host-based IOCs, network-based IOCs, hashes, users, assets, timestamps, tactics, and techniques.
- Do not assume the first plausible 20-stage narrative is the grader's expected segmentation. If the feedback shows missing tools/IOCs, reorder stages around those buckets.
- Delay final stage numbering until broad pivots are complete for suspicious domains/IPs, payload names, credential tools, AD discovery tools, group names, ransomware names, hashes, and encrypted extensions.
- Prefer sub-techniques over broad parent ATT&CK IDs when evidence supports them. Parent choices such as generic `T1059`, `T1003`, `T1543`, or `T1218` are often marked wrong when the dropdown expects PowerShell, LSASS/DCSync, Windows Service, or Rundll32.
- Store separate asset roles in notes even if the form has one `asset` field: execution/source asset, destination/target asset, affected/encrypted asset, and domain-controller target. Some stage graders want the execution host; others want the target or affected asset.
- Descriptions should include finding + implication + follow-on result: source URL/IP, destination path, process/command line, user/host context, and why it proves adversary behavior.

2026-05-20 TryGovMe lesson: a directionally correct ransomware chain still scored poorly because expected IOC buckets included additional activities not captured in the initial timeline, such as NanoDump/pwrex/trash.evtx, SharpHound/BloodHound, SharpChrome/certutil/browser credential theft, AD Recovery/itadmin/Domain Admin group manipulation, SharpKatz DCSync, repeated Mimikatz `sekurlsa::pth`, two ransomware staging/encryption buckets, and file hashes tied to `bomb.exe`/`.777zzz`. For future runs, use summary breakdown screenshots to rebuild the stage taxonomy before revising individual fields.

## Form-filling guidance

- Keep each description outcome-based: evidence + implication, not only "PowerShell observed".
- If the simulator supports saving drafts, fill/verify the first few stages before submitting all 20.
- If feedback marks a plausible MITRE choice wrong, align to the simulator dropdown wording rather than arguing generic ATT&CK semantics.
- Avoid exposing real or lab credential values in reusable notes; use placeholders for hashes/passwords unless the simulator requires them in a one-time IOC field.
