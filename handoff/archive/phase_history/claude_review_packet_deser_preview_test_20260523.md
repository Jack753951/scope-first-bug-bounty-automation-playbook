> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Claude Code review packet — deserialization preview/review process test

Read-only review request. Do not use tools. Do not propose new safety gates. This is a tactical/project-value review only.

## Intended process under test

```text
OSS/source reconnaissance -> Hermes tactical preview -> Kali bounded-script execution -> artifact/evidence pullback -> Claude Code read-only review -> Hermes synthesis
```

## Lane

Dedicated `modern_vuln_api` unsafe deserialization bounded-marker rerun.

## Source/recon summary

- Target file: `labs/modern_vuln_api/modern_vuln_api.py`.
- Endpoint: `POST /deserialize` calls `pickle.loads(base64.b64decode(payload_b64))`.
- Bounded sink: `record_deser_marker(marker)` appends `{"type":"bounded_pickle_gadget", "marker": marker}` to in-memory `DESER_EVENTS`.
- Stronger sink: `record_deser_impact(marker, callback_url)` exists but Hermes preview rejected it for this process test because marker-only is enough.
- Recon note: `setting/local/oss_refs/deserialization_preview_test_20260523/README.md`.

## Hermes preview summary

Artifact: `handoff/modern_api_deserialization_preview_20260523.md`.

Preview decision:

- Execute the smallest useful proof path.
- Start target on victim `<lab-ip>:18081`.
- From attacker `<lab-ip>`, send health, invalid/control payload, positive bounded marker payload, `/deser-log`, post-health.
- No callback, no shell, no file write, no persistence, no credential access.
- Purpose: test preview/review workflow and split deserialization into a dedicated wave.

## Pre-execution checks

- VirtualBox showed both `<attacker-vm>` and `<victim-vm>` running.
- Both VMs showed host-only NIC1 and NAT/NIC2 closed.
- SSH reachable on attacker and victim.
- `python3` and `curl` available on attacker and victim.

## Execution result

The combined bounded execution command was blocked by execution layer:

```text
BLOCKED: User denied. Do NOT retry.
```

Hermes did not retry, encode, disguise, split, or move the same trigger into another command.

## Available evidence

- Preview artifact exists.
- Blocker handoff exists: `handoff/modern_api_deserialization_preview_test_blocked_20260523.md`.
- Source/recon note exists.
- No new runtime positive/control deserialization artifacts were produced.
- Historical prior deserialization bundle exists, but it should not be used to claim this dedicated rerun succeeded.

## Review questions

Return concise fields:

```text
Reviewer route/tool:
Visible model/runtime:
Review focus:
Evidence inspected:
Claim supported? yes/no/partial
Recommended status: verified-impact | valuable-candidate | attempted-not-verified | blocked/deferred | reference-only
Missing evidence:
False-positive controls:
Tactical next step:
Hermes final decision recommendation:
```

Focus on project value and evidence classification. Do not add a safety process or approval gate.
