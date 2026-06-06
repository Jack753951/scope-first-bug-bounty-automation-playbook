> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Bug Bounty Workflow

## Default lifecycle

1. Intake program scope and rules
2. Validate scope offline
3. Generate policy decisions per target/technique/mode
4. Run safe recon only after authorization gates pass
5. Store structured evidence
6. Treat findings as candidates
7. Route candidates to agent/human review
8. Confirm manually before report
9. Draft report with impact, remediation, and retest steps
10. Preserve audit trail

## Principles

- Default deny
- No target-touching without scope
- No destructive defaults
- No secrets in repo or Obsidian
- No confirmed finding from scanner output alone
