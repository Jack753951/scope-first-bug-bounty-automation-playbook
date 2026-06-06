> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Splunk threat-hunting lab workflow

Use when an authorized lab / CTF / training platform provides SIEM telemetry (for example Splunk) and the user is calibrating the cybersec bug-bounty / defense workflow with a hunt exercise.

## Scope posture

- Treat TryHackMe / HackTheBox / PortSwigger / intentionally vulnerable lab telemetry as authorized training scope, but still label it explicitly.
- Querying SIEM telemetry is read-only investigation. It is not approval to scan, exploit, callback, brute force, or touch external targets.
- Keep scanner-style claims as `candidate` until manually verified with evidence, impact, remediation, and retest notes.

## Minimal workflow

1. State the hunt hypothesis and scope.
   - Example: package-manager supply-chain compromise via postinstall payload.
   - Record platform, mode (`blind training`, `assisted solve`, etc.), and non-target-touching posture.
2. Start from supplied IOCs and exact strings.
   - Package names/versions, suspicious domains, payload filenames, persistence names, encoded-command markers.
3. Build the process tree.
   - Parent process, child process, command line, user/SID, host, EventCode.
   - For package-manager cases, explicitly pivot on `npm-cli.js`, `node.exe`, `postinstall`, package paths, and script artifacts.
4. Decode suspicious commands.
   - For PowerShell `-EncodedCommand`, decode as UTF-16LE and preserve the decoded payload in the report.
   - Extract destination path, URL, persistence command, and any embedded second-stage command.
5. Validate persistence and network pivots.
   - Registry Run keys, scheduled tasks, startup folders, service creation.
   - DNS / HTTP / process network events around the execution window.
6. Expand impacted scope.
   - Search all hosts for the same package, domain, payload filename, persistence value, encoded command pattern, and process lineage.
7. Separate confirmed from unconfirmed.
   - Confirmed: telemetry directly observed.
   - Unconfirmed: payload execution after download, exfiltration, credential access, lateral movement, etc.
8. Convert the hunt into platform learning.
   - Note which evidence fields a future automation platform should capture, but do not promote this lab's specific IOCs into global memory.

## Useful SPL patterns

Package / IOC sweep:

```spl
search "<package-or-ioc>"
| table _time ComputerName User Image CommandLine ParentImage ParentCommandLine EventCode TargetFilename TargetObject Details QueryName DestinationHostname DestinationIp DestinationPort Hashes
```

Encoded PowerShell triage:

```spl
search "EncodedCommand" "NoP" "Hidden"
| table _time ComputerName User Image CommandLine ParentImage ParentCommandLine EventCode
```

Host timeline:

```spl
search ComputerName=<host> earliest="MM/DD/YYYY:HH:MM:SS" latest="MM/DD/YYYY:HH:MM:SS"
| sort _time
| table _time EventCode Image CommandLine ParentImage ParentCommandLine TargetFilename TargetObject Details QueryName DestinationHostname DestinationIp DestinationPort Hashes
```

DNS pivot:

```spl
search EventCode=22 (QueryName="<domain>" OR QueryName="<related-domain>")
| stats count min(_time) as first max(_time) as last values(Image) as images by ComputerName QueryName
```

Package-manager install pivot:

```spl
search "npm-cli.js" (" install " OR " install")
| table _time ComputerName User Image CommandLine ParentImage ParentCommandLine
```

## Report skeleton

- Title
- Executive summary
- Scope / authorization / mode
- Hypothesis
- Key findings
- Timeline
- Attack chain mapped to evidence
- Affected entities
- IOCs
- Confirmed observations
- Unconfirmed / needs follow-up
- Containment recommendations
- Detection opportunities
- Automation/platform lessons

## Supply-chain package-manager pivots

For npm/Python/Ruby/etc. package-manager compromise hunts, prioritize:

- install command and package version
- package directory and lifecycle script artifacts (`postinstall`, `setup.py`, etc.)
- package-manager-descended process tree
- encoded or hidden script interpreters launched by package-manager children
- payload download URL/path
- persistence mechanism
- network DNS/HTTP events
- host/user scope expansion

## Pitfalls

- Do not present the flag/lab answer as the main deliverable when the user's stated goal is bug-bounty workflow improvement. Close with reusable hunting/reporting/platform lessons.
- Do not overclaim follow-on compromise from staging/persistence telemetry alone; label it `not yet confirmed` until execution/network/file evidence supports it.
- Do not store lab-specific IOCs, hostnames, timestamps, or package names in global memory. If useful, keep them in repo handoff, Obsidian lab notes, or this reference only as illustrative examples without treating them as current threat intel.
