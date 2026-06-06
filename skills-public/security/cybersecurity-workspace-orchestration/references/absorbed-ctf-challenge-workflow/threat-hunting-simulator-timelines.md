> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Threat hunting simulator timelines

Use this reference for TryHackMe / SOC simulator tasks where the goal is to validate or disprove a hypothesis from SIEM logs and fill a staged attack-chain form.

## Common failure mode

Do not over-split every log event into a separate MITRE stage too early. Simulator graders often expect stages to represent core evidence classes, not every sub-action. If the feedback says the investigation is incomplete or the trail went cold, it usually means a key evidence category was omitted or placed in the wrong stage.

## Stable workflow

1. Read the business context first.
   - Map user -> host -> role.
   - Note important servers and subnets; they often become follow-up hunt pivots.

2. Broad-search all given IOCs and suspicious strings before filling the form.
   - Package names, domains, file names, registry value names, encoded command markers, hostnames, backup servers.
   - Sort by time and build an evidence-first chain.

3. Build a plain chain before MITRE mapping.
   - initial access / install
   - execution / script or command
   - decoded command / payload behavior
   - file, registry, or network changes
   - follow-on execution, lateral movement, or scope expansion

4. Fill simulator stages around the expected evidence categories.
   - Each stage should include: title, full adversary description, exact timestamp, tactic, technique, user, asset, and IOCs.
   - IOCs should be placed in the stage where the grader expects them, not only where they are most narratively convenient.

## Example evidence-category mapping

For a malicious npm supply-chain hunt:

- Stage 1: NPM package / initial access
  - Tactic: Initial Access
  - Technique: Supply Chain Compromise
  - IOC: package name and version, install command, node/npm process path

- Stage 2: PowerShell execution / decoded command
  - Tactic: Execution
  - Technique: Command and Scripting Interpreter
  - IOCs: full PowerShell command, `-NoP -W Hidden -EncodedCommand`, decoded script lines, download command, payload path

- Stage 3: Registry persistence / system change
  - Tactic: Persistence
  - Technique: choose the exact registry/run-key option if present; otherwise inspect the grader feedback before guessing
  - IOCs: registry path, registry value name, persisted command, payload path

Additional stages should be supported by actual log evidence, such as payload file creation, payload execution, outbound connection, backup server access, or additional affected hosts.

## Grader-feedback interpretation

If feedback lists missed IOCs with stage numbers, rewrite around those stage numbers. Example:

- `NPM Package — Stage 1` means package IOC must appear in Stage 1.
- `PowerShell Command — Stage 2` and `Decoded Command — Stage 2` means Stage 2 must include both raw and decoded command evidence.
- `Registry Path — Stage 3` and `Registry Value Name — Stage 3` means Stage 3 must be the registry persistence/system-change stage.

If a tactic/technique is red even though it seems MITRE-correct, do not argue with the taxonomy. The simulator may use a narrower expected stage model. Ask for the technique dropdown screenshot or use the closest registry/tool-transfer option indicated by the platform.

## Report quality checklist

Before submitting, verify each stage answers:

- What happened?
- Which host and user were involved?
- What exact evidence proves it?
- What did the decoded command or artifact do?
- What changed on the system?
- What should be hunted next?
- Why does it matter to the business context?

Avoid leaving late stages as generic C2/persistence labels without findings and implications. A full stage should state the result, not only the hypothesis.
