> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Modern API deserialization preview/review process test — blocked/deferred

Status: blocked/deferred / process test still valid
Date: 2026-05-23
Lane: dedicated unsafe deserialization bounded-marker rerun
Route intended: Windows Hermes -> SSH -> `<attacker-vm>` -> `<victim-vm>`

## Flow tested

```text
OSS/source reconnaissance -> Hermes tactical preview -> bounded execution attempt -> artifact/evidence pullback -> Claude Code review -> Hermes synthesis
```

## OSS/source reconnaissance

- Local source inspected: `labs/modern_vuln_api/modern_vuln_api.py`.
- Relevant endpoint: `POST /deserialize` uses `pickle.loads(base64.b64decode(payload_b64))`.
- Existing sink: `record_deser_marker()` records in-process marker events without shell, file write, persistence, callback, credential access, or external target.
- Existing stronger sink: `record_deser_impact()` writes lab-only marker/callback, but Hermes preview intentionally rejected it for this process test.
- Recon note: `setting/local/oss_refs/deserialization_preview_test_20260523/README.md`.

## Hermes tactical preview

Preview artifact: `handoff/modern_api_deserialization_preview_20260523.md`.

Decision: attempt the smallest marker-only proof path from attacker VM to victim VM, with no callback/shell/file/persistence.

## Route prechecks completed before block

- VirtualBox showed both `<attacker-vm>` and `<victim-vm>` running.
- Both VMs showed host-only NIC1 and NAT/NIC2 closed.
- SSH was reachable on attacker `<lab-ip>:22` and victim `<lab-ip>:22`.
- `python3` and `curl` were present on both VMs.

## Execution attempt result

The combined bounded execution command was blocked by the execution layer:

```text
BLOCKED: User denied. Do NOT retry.
```

Hermes did not retry, encode, disguise, split, or move the same pickle-trigger execution into another command. No `verified-impact` claim is made for this run.

## Evidence available for review

- Preview artifact: `handoff/modern_api_deserialization_preview_20260523.md`.
- Blocker record: this file.
- Source/recon note: `setting/local/oss_refs/deserialization_preview_test_20260523/README.md`.
- Prior broad-family evidence remains historical context only: `modules/bundles/verified_lab_flow_modern_api_deserialization_bounded_gadget.md` and `<artifact-output-dir>/modern_api_wave2_20260522T022303Z/`.

## Recommended classification before Claude Code review

`blocked/deferred` for the attempted dedicated rerun.

Project value is still positive as a process test because it verified that:

- Hermes preview ran before execution;
- the execution-layer blocker was not bypassed;
- the correct next step is review/synthesis, not retrying the trigger;
- the workflow can classify blocked/deferred without creating extra safety gate bureaucracy.

## Tactical next step options

1. If the operator wants to run it manually: create a Kali-side operator run-card with exact command, expected artifact, cleanup, and confirmation phrase.
2. If avoiding this trigger path: do a source-level unit/integration proof or choose adjacent safe-marker lane, but do not call it runtime deserialization impact unless the endpoint trigger is actually observed.
3. If testing only the preview/review process: send this blocked packet to Claude Code review and let Hermes synthesize `blocked/deferred`.
