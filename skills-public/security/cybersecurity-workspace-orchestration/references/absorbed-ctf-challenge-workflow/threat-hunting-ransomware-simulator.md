> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Threat-hunting / SIEM ransomware simulator pattern

Use for TryHackMe/TryGovMe-style SOC simulators where the prompt gives a ransomware alert, company/user/host mapping, and IOCs such as suspicious domains, installer names, credential tools, and encrypted-file extensions.

## Investigation sequence

1. Label scope as authorized training / read-only SIEM analysis.
2. Start with a broad IOC query across the full incident day, not only the alert time:
   - suspicious domain/IP
   - installer names/extensions
   - payload filenames
   - credential-tool names
   - ransomware extension
3. Build a chronological evidence table before filling the simulator timeline.
4. Use company host mapping to convert hostnames to people/roles, but do not invent impact without log evidence.
5. Do not stop at the first encrypted host. If the prompt says "two machines" or "another developer", pivot on the ransomware extension and ransomware process name across all hosts to identify the second system.

## Ransomware chain stage shape

A robust stage model is usually:

1. Initial access / user execution
   - browser download of suspicious installer/archive/script
   - downloaded path and Zone.Identifier if present
   - user + host mapping
2. Installer or script execution
   - msiexec, PowerShell, cmd, wscript/cscript, or package-manager lifecycle process
   - remote script URL and command line
3. Decoded payload behavior
   - PowerShell 4104 / script-block logging
   - decoy install versus malicious download
   - payload file paths and source URLs/IPs
4. Persistence / service / system change
   - `sc.exe create`, scheduled task, Run key, service start, or dropped binary
   - service name, binary path, account, start mode
5. Proxy execution / payload launch
   - rundll32/regsvr32/mshta or service payload execution
   - DLL export/function if visible
6. Credential access and lateral movement
   - Mimikatz/credential dumping, pass-the-hash, WinRM/wsmprovhost, alternate user context
   - explicitly separate observed credential tool use from confirmed lateral movement if the pivot is not fully proven
7. Impact and scope
   - ransomware binary/process, encrypted file extension, ransom note, affected hosts/users
   - second host search if the prompt says multiple machines

## MITRE mapping hints

- Browser download + user-run installer: `Initial Access` or `Execution` depending on the simulator's taxonomy; if it rejects Initial Access, try `User Execution`.
- `powershell.exe iex(iwr ...)`: `Execution` -> `Command and Scripting Interpreter: PowerShell`.
- `sc.exe create ... start=auto obj=LocalSystem`: `Persistence` -> `Create or Modify System Process: Windows Service`.
- `rundll32.exe payload.dll,Start`: `Defense Evasion` or `Execution` -> `System Binary Proxy Execution: Rundll32`.
- Mimikatz/sekurlsa: `Credential Access` -> `OS Credential Dumping`.
- Pass-the-hash: `Lateral Movement` -> `Use Alternate Authentication Material: Pass the Hash`.
- `.777zzz` or similar mass encrypted extensions: `Impact` -> `Data Encrypted for Impact`.

## Simulator-form pitfalls

- Do not combine all late activity into one vague "credential theft and ransomware" stage if the form supports more stages; split credential access, lateral movement/remote session, and encryption impact.
- If you must use only five stages, make the final stage `Impact / Data Encrypted for Impact` and include credential-abuse evidence in the description/IOCs.
- When the prompt states SIEM went dark, hunt for log tampering/service stop events, but do not assert they occurred unless logs show them.
- If tool/browser APIs become unstable while querying Kibana, keep the raw facts already extracted and ask the user for the specific Discover result screenshot rather than making up the missing second-host scope.
