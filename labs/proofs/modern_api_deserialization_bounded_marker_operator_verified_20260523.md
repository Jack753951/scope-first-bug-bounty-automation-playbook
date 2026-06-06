> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Modern API deserialization bounded-marker operator run — verified

Status: verified_bounded_marker_lab_only
Date: 2026-05-23
Route/tool: Operator manual run inside `<attacker-vm>` -> Docker target on `<victim-vm>`
Visible model/runtime: Hermes verification via `gpt-5.5 / openai-codex`; operator-run script executed manually outside Hermes trigger path
Artifact root: `<artifact-output-dir>/modern_api_deser_operator_20260523T093300Z/`
Run ID: `modern_api_deser_operator_20260523T093300Z`

## Scope

- Attacker VM: `<attacker-vm>` / `<lab-ip>`.
- Victim VM: `<victim-vm>` / `<lab-ip>`.
- Target: local Docker-published `modern_vuln_api` on `http://<lab-ip>:18082`.
- Script: `scripts/labs/operator_deser_bounded_marker_run.sh`.
- Run-card: `handoff/deser_operator_run_card_20260523.md`.

## Why this exists

The dedicated deserialization rerun was previously blocked through Hermes by the execution layer with `BLOCKED: User denied. Do NOT retry.` Hermes did not retry, encode, disguise, split, or move the same trigger. The operator manually ran the prepared Kali-side script, which has a human confirmation gate before the single positive trigger.

## Evidence summary

From `summary.md` and `run.log`:

```text
pre_health: 200
invalid_control_status: 400
deserialize_marker_status: 200
deser_log_pre_status: 200
deser_log_post_status: 200
post_health: 200
marker_found: yes
VERDICT=verified_bounded_marker_lab_only
```

Marker:

```text
DESER_OPERATOR_modern_api_deser_operator_20260523T093300Z
```

Positive response excerpt from `http/deserialize_marker_response.json`:

```json
{
  "deserialized_type": "dict",
  "result": "{'recorded': True, 'marker': 'DESER_OPERATOR_modern_api_deser_operator_20260523T093300Z'}",
  "events": [
    {
      "marker": "DESER_OPERATOR_modern_api_deser_operator_20260523T093300Z",
      "type": "bounded_pickle_gadget"
    }
  ]
}
```

Log evidence from `http/deser_log_post.json` contains the same marker and `type: bounded_pickle_gadget`.

Invalid/control response from `http/deserialize_invalid_control.json`:

```json
{
  "error": "Error('Incorrect padding')",
  "events": []
}
```

## Cleanup and posture

- `cleanup/target_cleanup.txt` contains `modern-api-deser-18082`, confirming the victim container was removed by cleanup.
- `cleanup/attacker_internet.txt`: `internet_closed`.
- `cleanup/victim_internet.txt`: `internet_closed`.
- Follow-up read-only checks:
  - attacker Internet: `attacker_internet_closed`.
  - victim Internet: `victim_internet_closed`.
  - victim `docker ps -a | grep modern-api-deser-18082`: no matching container.

## Classification

This is a verified local-lab unsafe-deserialization bounded marker proof. It demonstrates that attacker-controlled serialized data can invoke a server-side callable in the lab target.

It is not a public-target finding and not a report-ready bug bounty issue by itself. Report-readiness classification: `reusable_methodology / local proof pattern`.

## Boundary

Local authorized lab only. Exactly one bounded positive pickle marker trigger. No shell, arbitrary command, persistence, callback, credential access, public target, exfiltration, or automatic finding/report promotion.

## Updated records

- `modules/bundles/verified_lab_flow_modern_api_deserialization_bounded_gadget.md`
- `handoff/vulnerability_test_inventory_20260523.md`
- `handoff/proof_library_index_20260523.md`
- `handoff/current_navigation.md`
- `handoff/active_strategy_queue.md`
- `handoff/accepted_changes.md`
- `notes/obsidian_projects/Cybersec Lab.md`
