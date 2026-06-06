> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cybersec Lab Safety Contract

Status: active
Source: User + Hermes navigation cleanup
Date: 2026-05-23
Repo truth: `.hermes.md`, `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, `handoff/accepted_changes.md`

## Purpose

This file states the current safety boundary for the Cybersec Lab workbench. It is intentionally short and operational. It keeps local lab learning fast while preserving authorization, recoverability, and evidence hygiene.

## Binding route and scope

- Default attacker / target-touching route: `<attacker-vm>`.
- Deprecated route: old registered `<attacker-vm>`; forensic archive only.
- Default victim / vulnerable-target route: `<victim-vm>`.
- Default scope: local lab, owned/disposable targets, intentionally vulnerable apps, or explicitly authorized CTF/training environments.
- Public or real bug bounty targets are not authorized by this contract. They require explicit operator approval, program scope/rules, and technique gates.

## Network posture

- Default VM network posture is host-only.
- NAT is closed by default.
- Temporary NAT windows are allowed only for package installs, updates, or Docker/image pulls needed for the lab.
- After any NAT window, record that NAT was closed and verify Internet is unavailable from the lab route where practical.
- Do not add tunnels, relays, proxies, pivots, OAST/external callbacks, scheduler/CI target-touching jobs, or public listeners without explicit operator approval.

## Local-lab learning allowance

Within authorized disposable local lab targets, the project may use script-first, context-driven tooling, including scanners/fuzzers/Burp/session workflows/TLS tools/OSS tools/destructive recoverable-lab scripts, when the wave has:

- target and route clearly labeled;
- local-lab scope confirmed;
- pre-health and post-health checks when target-touching;
- artifact path identified;
- cleanup/recovery plan;
- candidate-only/report-readiness semantics;
- no real credential theft, real exfiltration, malware, stealth, persistence, uncontrolled propagation, or automatic submission.

## Proof quality rules

- One vulnerability behavior/class per proof wave by default.
- Prefer one-vuln max-impact proof over broad multi-class output.
- Scanner output is triage only; report-worthy findings require manual proof, impact reasoning, controls, remediation/retest notes, and report-readiness review.
- Strong proof examples:
  - true attacker-side callback with source/context and unique marker;
  - browser runtime execution in correct origin/session context;
  - safe-marker file read/path traversal/XXE proof;
  - authenticated/session replay with role boundary and controls;
  - bounded state-change evidence with cleanup.

## Evidence hygiene

Do not store or promote:

- raw secrets, credentials, tokens, cookies, private keys, hashes, loot;
- private target/scope details outside the authorized local project record;
- unnecessary raw response bodies when metadata/marker evidence is enough;
- exploit evidence dumps in Hermes global memory or broad Obsidian notes.

Artifact packets should store enough to rerun and explain the proof while minimizing sensitive material.

## Recovery rules

- Use clean snapshots/clones as the baseline for destructive or crash-prone testing.
- Do not treat a live, dirty VM state as durable truth.
- Record cleanup and whether snapshot restore was needed.
- If VirtualBox snapshot/disk state is unhealthy, stop and route to infrastructure recovery rather than continuing vulnerability work.

## Promotion rules

A local proof can be promoted to a reusable bundle only when it has:

- clear authorization boundary;
- repeatable route/tool commands;
- evidence packet or summary;
- cleanup/recovery notes;
- false-positive controls and limitations;
- candidate/report-readiness status that does not imply real-world confirmation.

Public target activation, report submission, automatic finding confirmation, scheduler/CI execution, scope/config changes, credential/OAuth use, and production settings remain blocked until explicitly approved.
