> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Deserialization Operator Run-Card — modern_vuln_api bounded marker

Status: operator-run / authorized local lab only / do not auto-execute from Hermes after safety-layer denial
Date: 2026-05-23
Purpose: complete the previously blocked dedicated unsafe-deserialization bounded-marker rerun manually, while preserving local-lab boundaries.

## Why this is operator-run

The dedicated deserialization proof was blocked by the execution layer with:

```text
BLOCKED: User denied. Do NOT retry.
```

Hermes did not retry, encode, disguise, split, or move the same pickle-trigger execution into another command. If the operator wants this local authorized proof completed, the clean route is: Hermes prepares a Kali-side run-card/script; the human operator runs it manually; Hermes can later pull artifacts and record the result.

## Scope / hard boundaries

Allowed:

- Local lab only.
- Attacker VM: `<attacker-vm>` / `<lab-ip>`.
- Victim VM: `<victim-vm>` / `<lab-ip>`.
- Target: local Docker-published `modern_vuln_api` only.
- Exactly one positive unsafe-deserialization marker trigger after confirmation.
- Positive payload calls only the lab source function `record_deser_marker(marker)`.

Not allowed in this run-card:

- No public/unknown target.
- No shell, arbitrary command, persistence, callback, credential access, token capture, or exfiltration.
- No loops, fuzzing, brute force, crawler behavior, or public OAST.
- No automatic report/finding promotion.

## Prepared script

Run this manually inside `<attacker-vm>`:

```bash
cd /mnt/hacking
bash scripts/labs/operator_deser_bounded_marker_run.sh
```

The script:

1. starts the victim-side `modern_vuln_api` target on port `18082`;
2. verifies victim local health and attacker-to-victim health;
3. sends one invalid/control deserialize request, expecting HTTP `400`;
4. pauses before the positive unsafe-deserialization trigger;
5. requires this exact confirmation phrase:

```text
RUN_DESER_MARKER_ON_LOCAL_LAB
```

6. sends exactly one bounded marker pickle trigger;
7. verifies `/deser-log` and post-health;
8. cleans the victim container by default;
9. writes artifacts under `/home/kali/<artifact-output-dir>/<RunId>/`.

## Precheck-only mode

To test setup without sending the positive pickle trigger:

```bash
cd /mnt/hacking
bash scripts/labs/operator_deser_bounded_marker_run.sh --precheck-only
```

Expected precheck verdict:

```text
verdict: setup_ready_no_pickle_trigger_sent
```

## Expected proof

Success requires all of these:

1. Pre-health on target is HTTP `200`.
2. Invalid/control `/deserialize` request returns HTTP `400`.
3. Positive `/deserialize` marker request returns HTTP `200`.
4. `/deser-log` or positive response contains the unique marker `DESER_OPERATOR_<RunId>`.
5. Post-health on target is HTTP `200`.
6. Cleanup removes the victim target container.
7. NAT/Internet remains closed or is re-closed and verified.

## Pull artifacts back to Windows

After completion, note the printed `RUN_ID`, then from Windows PowerShell:

```powershell
cd <private-workspace>
$env:MSYS2_ARG_CONV_EXCL='*'
.\scripts\kali-pull.ps1 -RemotePath "/home/kali/<artifact-output-dir>/<RunId>"
.\scripts\kali-pull.ps1 -HostName <lab-ip> -RemotePath "/home/kali/<artifact-output-dir>/<RunId>"
Remove-Item Env:\MSYS2_ARG_CONV_EXCL -ErrorAction SilentlyContinue
```

Replace `<RunId>` with the run ID printed by the script.

Artifact location should be:

```text
<private-workspace>\<artifact-output-dir>\<RunId>\
```

## After you run it

Send Hermes the `RunId` and/or paste `summary.md`. Hermes should then:

1. Verify pre/post health, invalid control, positive marker response, and `/deser-log`.
2. Classify as `verified_bounded_marker_lab_only` only if the marker is present and controls pass.
3. Update `handoff/modern_api_deserialization_preview_review_process_test_20260523.md` or create a verified follow-up handoff.
4. Update `modules/bundles/verified_lab_flow_modern_api_deserialization_bounded_gadget.md` if the evidence is standalone.
5. Update `handoff/accepted_changes.md`, `handoff/current_navigation.md`, and Obsidian.

## Verification checklist

- [ ] Pre-health is 200.
- [ ] Invalid/control deserialize request is 400.
- [ ] Exactly one positive bounded marker trigger was sent.
- [ ] Marker appears in positive response or `/deser-log`.
- [ ] Post-health is 200.
- [ ] Victim container removed.
- [ ] Attacker/victim Internet closed.
- [ ] Artifacts pulled to Windows.
