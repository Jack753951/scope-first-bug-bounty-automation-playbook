> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# 2026-05-21 Lab Recovery and OWASP Tracker Notes

This reference captures session-specific details for the `owasp-single-vuln-lab-wave` workflow. Keep the SKILL.md class-level; use this file as the concrete project snapshot.

## User workflow correction

The operator explicitly wants a script-first, one-vulnerability-at-a-time OWASP module loop:

1. Pick one OWASP Top 10 class.
2. Write RED tests / adapter plan.
3. Run against the authorized local靶機.
4. If useful, modularize the flow into adapter/importer/bridge/bundle records.
5. Repeat until 2017, 2021, and 2025 migration-track rows are covered.

The operator also authorized aggressive/destructive scripts only inside the disposable local lab, with the rule: if the target breaks, record the breakage, restore from snapshot/container reset automatically, then verify health.

## Project files created in that session

- Tracker: `handoff/owasp_2017_2021_2025_single_vuln_modularization_tracker_20260521.md`
- Recovery runbook: `handoff/destructive_lab_auto_recovery_runbook_20260521.md`
- Accepted-change entry: `handoff/accepted_changes.md`
- Active navigation: `handoff/active_strategy_queue.md`
- Obsidian index: `Projects/Cybersec Lab/00_Index/Active Projects.md`

## Verified local lab snapshot at the time

- Target URL: `http://<lab-ip>:3000/`
- Attacker VM: `<attacker-vm>`, observed host-only IP `<lab-ip>`
- Victim VM: `<victim-vm>`, observed host-only IP `<lab-ip>`
- Victim snapshots observed:
  - `setup-complete-with-tools`
  - `pre-aggressive-current-running-recovery-20260521-093252`
- Attacker snapshot observed:
  - `clean-before-aggressive-tests-20260521-093233`
- Attacker route boundary observed: host-only `<lab-ip>/24`, no default route
- Health observed from attacker to victim: `HTTP/1.1 200 OK`

Treat these as a dated snapshot, not permanent truth. Re-check before a destructive wave.

## Recovery command template used in project notes

From Git-Bash on the Windows host:

```bash
VBOX='/c/Program Files/Oracle/VirtualBox/VBoxManage.exe'
"$VBOX" controlvm <victim-vm> poweroff || true
"$VBOX" snapshot <victim-vm> restore pre-aggressive-current-running-recovery-20260521-093252
"$VBOX" startvm <victim-vm> --type headless
```

Then verify from attacker VM through the existing Kali bridge:

```bash
MSYS2_ARG_CONV_EXCL='*' powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/kali-run.ps1 -Command 'curl -sS -I --max-time 10 http://<lab-ip>:3000/ | head -n 1'
```

Expected health line:

```text
HTTP/1.1 200 OK
```

## Existing active/partial bundles at this point

- `lab_directory_listing_triage`: active for `/ftp/` or directory-listing/security-misconfiguration candidate.
- `benign_reflection_redirect_triage`: active for query reflection/open-redirect candidate using inert canaries only.
- `wave1a_metadata.py` + importer + bridge: partial active baseline for metadata, `/api-docs/`, `/robots.txt`, CORS, known paths.

## Pitfall learned

Do not infer that a category is fully covered just because it maps to a 2021 category already touched by a partial module. Example: XXE or exceptional-condition handling may map loosely to security misconfiguration, but directory-listing metadata does not cover parser-risk or error-handling behavior. Mark coverage as capability-specific and require a dedicated single-vulnerability wave for each class.
