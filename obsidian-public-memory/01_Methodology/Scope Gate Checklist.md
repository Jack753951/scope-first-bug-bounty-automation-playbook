> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Scope Gate Checklist

Before any target-touching action, verify:

- [ ] Target belongs to local lab / CTF / owned asset / written client authorization / explicit bug bounty scope
- [ ] Global `config/scope.txt` allows the target
- [ ] Program scope/rules allow the target, if `--program` is used
- [ ] Technique is allowed
- [ ] Automation is allowed for selected mode
- [ ] Rate limits are respected
- [ ] Testing window is valid
- [ ] No out-of-scope assets are included
- [ ] Dry-run is used where appropriate

Scanner output is triage-only until manually verified with evidence, impact, remediation, and retest notes.
