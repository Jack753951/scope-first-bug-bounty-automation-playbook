> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# OWASP 2025 Migration and Automation Modularization Review

Status: active
Source: Hermes
Date: 2026-05-21
Repo truth: `<user-home>`

## Summary

The Cybersec Lab long-term goal explicitly includes automation: collect and synthesize OWASP Top 10 coverage, test scripts in a controlled local lab when approved, and modularize successful checks so future authorized bug-bounty workflows can call them behind scope/policy/review gates.

Current phase remains Phase 4B: OWASP Top 10 modular local-lab check library and lab-to-review workflow.

## 2025 migration decision

- Runtime/module taxonomy remains OWASP Top 10 2021 until a separate implementation slice updates catalog aliases.
- OWASP 2025 categories are now reviewed for migration planning.
- Most 2025 categories can reuse 2021 module/checklist behavior with aliases.
- A03:2025 Software Supply Chain Failures needs checklist-only planning first.
- A10:2025 Mishandling of Exceptional Conditions needs checklist-only planning first because runtime testing may drift toward DoS/crash/fuzz behavior.
- Wave 2 benign parameter probes remain deferred until bounded adapter, tests, review, and explicit operator approval exist.

## Attack/victim details preservation

Global Hermes memory compaction did not delete operational engineering details. They are intentionally repo-local, mainly in:

- `handoff/kali_tool_lab_default.md`
- `handoff/phase4a_isolated_aggressive_lab_gate_status_20260521.md`
- `handoff/accepted_changes.md`
- `scripts/kali-run.ps1`, `scripts/kali-check-tools.ps1`, `scripts/kali-install-key.ps1`, `scripts/kali-pull.ps1`

Future agents should read those repo-local files before touching Kali, victim VM, Juice Shop, or any lab target workflow.

## Next safe slice

`phase4b_owasp_2025_alias_catalog_and_script_matrix`

Boundary: offline catalog/script-classification update only; no target interaction, scanner execution, Kali bridge run, schema/runtime/report promotion, or real bug-bounty activation.
