# Scope-First Bug Bounty Automation Playbook

A public, sanitized methodology for building an agent-assisted security research
workbench that turns local lab proofs and passive intelligence into bounded,
authorized bug-bounty evidence packets.

This repository is intentionally **methodology-only**:

- no private program names, scope files, credentials, screenshots, or findings;
- no exploit payload collections or target-touching automation;
- no raw scan output, loot, cookies, tokens, OTPs, or account data;
- no claim that any live target is authorized by these docs.

The source project that inspired this public edition is private. The content here
has been rewritten into reusable patterns: safety contracts, handoff structure,
multi-agent routing, memory governance, proof-quality gates, and dry-run
templates.

## What this helps with

1. Keep local lab learning fast without letting it leak into live targets.
2. Separate "think like an attacker" from "execute only bounded, authorized proof".
3. Make autonomous agents fail closed on scope, credentials, customer data, and
   report submission.
4. Preserve useful proof patterns as reusable capability bundles instead of
   ad-hoc notes.
5. Route project memory so future agents see the current truth without copying
   secrets into global memory or public repos.

## Repository map

```text
docs/
  01-safety-contract.md
  02-agent-operating-model.md
  03-memory-and-handoff-governance.md
  04-local-lab-proof-library.md
  05-authorized-live-target-dry-run.md
  06-evidence-redaction-and-report-readiness.md
  07-recon-and-intel-cadence.md
  08-public-export-safety.md
templates/
  lane_state.template.json
  evidence_packet.template.md
  operator_gate_card.template.md
scripts/
  public_safety_scan.py
```

## Core boundary

Local, disposable, owned lab targets may be used for fast proof learning.
Real programs, production systems, third-party accounts, callbacks, account
mutation, high-volume automation, and final submission require explicit scope,
policy, operator approval, and evidence-minimization controls.

If a document in this repo seems to authorize live testing by itself, read it as
`blocked-awaiting-scope`. It is a planning artifact, not permission.
