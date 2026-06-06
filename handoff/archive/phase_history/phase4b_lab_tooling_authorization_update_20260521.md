> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4B lab tooling authorization update

Status: active operator preference / local-lab only
Date: 2026-05-21

## Operator clarification

The operator clarified that the project should not categorically ban useful tooling against the authorized disposable local靶機. Tools such as broad scanners, fuzzers, Burp/session workflows, TLS scanners, and external OSS wrappers may be used when they improve lab coverage.

The operator also reaffirmed that aggressive and destructive scripts are authorized for the disposable lab when recovery is available. If a useful tool must be downloaded or updated, the accepted workflow is to temporarily enable NAT/network access, download/install the tool, record source/version/license, then disable NAT and return to host-only lab operation before target-touching execution.

## Scope of this authorization

This authorization applies only to the authorized local/disposable lab environment, currently tracked as:

- Attacker VM: `<attacker-vm>` / `<lab-ip>`
- Victim VM: `<victim-vm>` / `<lab-ip>`
- Local lab target observed: `http://<lab-ip>:3000/`
- Recovery/snapshot references: see `handoff/destructive_lab_auto_recovery_runbook_20260521.md` and `handoff/owasp_2017_2021_2025_single_vuln_modularization_tracker_20260521.md`

It does not authorize public/third-party/bug-bounty targets unless a separate program scope/rules gate explicitly permits the target and technique.

## Updated operating principle

Do not ban tools by category for the local lab. Gate them by:

1. target authorization and host-only/scope lock;
2. recovery verification before aggressive/destructive target-touching execution;
3. tool source/version/license recording for downloads;
4. NAT only for install/update, then disabled before lab execution when feasible;
5. request/impact caps where the tool supports them;
6. artifact hygiene: no raw secrets, loot, tokens, or unnecessary body retention;
7. candidate-only output until manual verification/report-readiness gate.

## Tool classes now explicitly allowed in the local lab gate

- Broad scanners, when pointed only at the lab target and outputs are triaged as candidate-only.
- Fuzzers, when bounded or run against a disposable/recoverable target.
- Burp/session workflows, when accounts/sessions are lab-only and no real credentials are used.
- TLS scanners, when the target exposes TLS or the wave explicitly needs transport analysis.
- OSS tools/templates/wrappers, including temporary NAT installation when required.
- Destructive/aggressive scripts, when snapshot/recovery has been verified and the effect stays inside the disposable lab.

## Still forbidden / still requires separate gate

- Public or real bug-bounty target activation without program scope/rules approval.
- Malware, stealth persistence, unauthorized access workflows, credential theft, real exfiltration, or uncontrolled propagation.
- Retention or transmission of secrets/loot/tokens/raw sensitive bodies.
- Destructive actions outside the disposable lab.
- Automatic confirmed-finding/reportable/submission promotion from scanner output.

## Practical effect on next waves

Future OWASP single-vulnerability modules should prefer mature tooling when useful. The decision options remain `adopt`, `wrap`, `adapt`, `reference-only`, or `write-custom`, but `too broad` is no longer a sufficient reason by itself to reject a tool for the disposable local lab. Instead, build a wrapper/run card with recovery and artifact controls.

For the next three-module wave, a good direction is to include at least one mature tool wrapper instead of another purely custom fixed-route adapter, assuming install/source/version can be recorded and the lab target remains recoverable.
