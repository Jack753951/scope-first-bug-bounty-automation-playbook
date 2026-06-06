> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# OSS / Source Recon Guidance

Status: active simplified guidance
Owner: Hermes / Claude-Cowork / Codex
Safety posture: design/source learning only; no target-touching

## Purpose

Use mature open-source projects, official docs, public writeups, schemas, and training-lab source to improve this project before writing custom machinery. This is a capability-growth shortcut, not a gate ceremony.

## Default Rule

Before building a new reusable script, module, runner, schema, report/evidence format, or proof bundle, quickly check relevant mature sources when doing so is cheap and useful. Record only the decisions that affect implementation.

Do not block local/offline progress just because a perfect comparison was not done. If the work is small and reversible, implement with validation and leave a note for later source comparison if needed.

## What To Capture

Use a compact form:

```text
Source checked:
Useful pattern:
Decision: adopt / adapt / ignore / reference-only / custom
Why:
Safety note:
Implementation impact:
```

## Good Sources

Examples:

- OWASP WSTG/ASVS/Cheat Sheets and PortSwigger Web Security Academy;
- PayloadsAllTheThings, WebGoat, Juice Shop, DVWA, and intentionally vulnerable labs;
- Nuclei/ZAP/Semgrep/SARIF/OSV/CycloneDX conventions for metadata and fixtures;
- ProjectDiscovery tools, Amass, SpiderFoot, Recon-ng, DefectDojo, OpenVEX/CSAF when they clarify contracts.

## Hard Safety Boundary

This guidance does not authorize:

- running third-party scanners/templates against live targets;
- copying unsafe target-touching defaults;
- importing unreviewed code directly into runner paths;
- treating scanner/advisory output as confirmed findings;
- weakening scope, program-policy, dry-run, redaction, or evidence gates.

Prefer offline import/normalize/validate first. Live execution still requires exact scope, program rules, and operator approval when it crosses a hard stop.
