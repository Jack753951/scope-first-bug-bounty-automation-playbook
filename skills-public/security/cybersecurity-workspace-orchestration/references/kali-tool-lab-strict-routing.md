> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Kali Tool-Lab Strict Routing and Artifact Loop

This reference captures the corrected workflow for this user's cybersecurity workspace when doing target-touching lab work.

## Default split

- Windows Hermes is the control plane: repo edits, handoff/accepted_changes, Obsidian, synthesis, review, script authoring, and pulling artifacts.
- Kali `<lab-vm>` is the tool/attacker plane: curl/probing, ffuf, Nikto, nmap, sqlmap, nuclei, Chromium/headless browser validation, exploit-flow attempts, and aggressive local-lab testing.

Do not mark a tool or workflow blocked just because the synchronous worker inherited Windows/Git-Bash PATH/workdir. First route through the Kali bridge/wrapper and verify the Kali route/tool inventory.

## Strict execution loop

1. Confirm scope/authorization and target identity.
2. Use the project Kali wrapper/SSH bridge for target-touching commands.
3. Run a pre-health check from Kali.
4. Verify required Kali tools with `command -v` or version checks.
5. Execute bounded lab scripts/tools from Kali only.
6. Save artifacts under Kali output directories.
7. Pull artifacts back to the Windows repo with the project pull wrapper.
8. Update bundles/handoff/Obsidian/accepted_changes from Windows.
9. Run project review from the repo root.
10. Report route, artifacts, validation, and whether claims are verified-impact vs valuable-candidate/attempted/blocked.

## Exceptions

Windows may directly touch a target only for quick reachability or emergency fallback, and the exception should be stated clearly. Do not use Windows direct contact as the default for scanners, payloads, browser runtime proof, or exploit-flow evidence.

## Evidence discipline

- Record pre/post health.
- Avoid raw secrets/loot in durable artifacts.
- Pull back only safe evidence and metadata unless the operator explicitly approves a narrower manual review.
- If a flow does not achieve max impact, retain it when useful as `valuable-candidate`, `attempted-not-verified`, `blocked/deferred`, or `reference-only` rather than losing the learning.
