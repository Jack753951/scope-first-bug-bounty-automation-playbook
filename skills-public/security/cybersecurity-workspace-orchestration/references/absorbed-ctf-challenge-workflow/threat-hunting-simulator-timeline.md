> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Threat hunting simulator timeline/reporting pattern

Use this reference for TryHackMe-style SOC/threat-hunting simulators where the task is to validate a hypothesis from SIEM logs and fill an attack-chain timeline form.

## Key lesson

Do not over-split every telemetry event into separate MITRE stages before understanding the platform's expected evidence categories. Many simulators grade by whether specific IOC classes appear in specific stages, not just by whether the narrative is technically plausible.

A common supply-chain/log-analysis shape:

1. Initial access / package event
   - Tactic: Initial Access
   - Technique: Supply Chain Compromise
   - IOCs: package name/version, install command, package manager path

2. Execution / script interpreter
   - Tactic: Execution
   - Technique: Command and Scripting Interpreter
   - IOCs: full PowerShell/cmd command, encoded-command marker, decoded script content
   - Description must state what the decoded command did, not only that it existed.

3. Persistence / registry or autorun change
   - Tactic: Persistence
   - Technique: prefer the exact registry/autorun option provided by the platform; if unavailable, inspect options before guessing a parent technique
   - IOCs: registry path, registry value name, payload path

4. Payload staging or follow-on activity
   - Include only when supported by logs. If the platform asks for later stages, verify file creation, process execution, network activity, or internal access rather than repeating earlier inferred payload intent.

5. Business impact / scope expansion
   - Use company context to prioritize affected users/assets and follow-up hunts, but do not create a MITRE stage from business impact unless the form allows non-attacker-activity notes.

## Practical workflow

1. Broad-search every explicit hint/IOC first:
   - package names
   - domains/URLs
   - executable names
   - registry value names
   - host/user names

2. Build a raw chronological evidence table before selecting MITRE values:
   - time
   - host
   - user
   - event code/source
   - image/process
   - parent process
   - command line
   - file path / registry path / DNS / destination

3. Identify the platform's expected IOC buckets from feedback screens.
   - If it says `PowerShell Command` and `Decoded Command` were missed in Stage 2, consolidate encoded PowerShell and decoded payload into Stage 2.
   - If it says `Registry Path` and `Registry Value Name` were missed in Stage 3, Stage 3 should be the registry persistence/system-change event.

4. If a tactic/technique is marked wrong despite being MITRE-plausible:
   - do not keep defending the generic MITRE mapping;
   - inspect the platform's technique dropdown or feedback categories;
   - choose the option that matches the grading bucket and evidence class.

5. When feedback says `investigation incomplete` or `trail went cold`, search for the missing follow-on result:
   - file created for the payload
   - payload process execution
   - outbound connection from payload
   - authentication/SMB/RDP/internal access to named infrastructure
   - same IOC on other hosts

## Report quality checklist

Each stage description should include:

- what was observed, not just inferred;
- why the event matters in the chain;
- key evidence/IOC values;
- follow-up result if available, e.g. decoded command, resulting registry change, file creation, or later execution;
- business asset context only after the technical event is clear.

Avoid:

- creating separate stages for every sub-event if the platform expects consolidated evidence buckets;
- using the current system time instead of the SIEM event time;
- leaving optional-looking stages empty or generic when the simulator expects findings and implications;
- putting decoded commands or registry value names in the narrative only while omitting them from the IOC list.