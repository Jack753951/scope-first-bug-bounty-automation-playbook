> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Front passive-only resume visibility checkpoint (2026-05-26)

Session lesson for authorized SaaS bug-bounty lanes that are already downgraded to passive UI/docs mapping only.

## Situation

- Lane boundary allowed only passive UI/docs inventory.
- noVNC tunnel and VM were reachable.
- Existing screenshots showed useful Front onboarding/setup-guide evidence, but the current visible Kali workspaces only showed the desktop and no visible Front browser window.
- A process-kill/restart command for Chromium was treated as destructive and denied by the operator/system guard.

## Durable workflow lesson

When a passive-only lane resumes and the browser is not visibly available:

1. Verify scope/lane state first.
2. Capture non-sensitive workspace screenshots to document the resume state.
3. Do not reset, kill, or restart existing browser/session processes without explicit operator approval.
4. If the UI is unavailable, switch to non-target-touching public docs/reference mapping and preserve hypotheses/bundles instead of forcing live interaction.
5. Record the blocked restore attempt as a boundary event, then stop or ask for a non-destructive restore path.

## Safe alternatives

- Ask the operator to bring the app/browser window back into view in noVNC.
- Request explicit approval for a non-destructive restore action such as opening a new browser window/profile.
- Continue docs-only mapping from public references.
- Preserve future proof bundles with operator gates rather than promoting proof readiness.

## Do not encode as a global negative claim

This was not evidence that noVNC, Chromium, browser tools, or the VM are generally broken. It was a passive-only boundary lesson: do not convert a visibility problem into a destructive session reset without approval.
