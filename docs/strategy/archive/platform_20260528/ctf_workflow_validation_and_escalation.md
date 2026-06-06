> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# CTF Workflow Validation and Escalation Criteria

Date: 2026-05-18
Status: Workflow direction / project backlog seed

## Purpose

Use CTF challenges as controlled drills for the cybersec lab's long-term platform goals:

- improve blind triage and weakness-class recognition
- validate Kali-first external interaction
- exercise output-side review decisions
- decide when single-agent solving is enough versus when to escalate
- extract reusable verifier/script patterns for the authorized bug-bounty platform

CTF solving is not only for flags. The intended artifact is a better workflow: scope gate, triage, tool choice, verification, second-review decision, and durable lesson capture.

## Operating Model

```text
Windows host = control plane / repo / Obsidian / orchestration
Kali VM      = external interaction / nc/curl/wget/security tools / target-touching probes
```

For CTF tasks:

1. Confirm CTF/training scope.
2. If the task touches an external host/service, use Kali.
3. Keep downloaded/generated challenge artifacts under ignored local paths.
4. Treat intermediate outputs as candidates until verified.
5. Record durable techniques in Obsidian; keep repo docs focused on workflow contracts and reusable tooling.

## Challenge Lessons So Far

### Some Assembly Required 4

Workflow value:

- Demonstrated a false-positive risk: UI/checker success can be misleading.
- Embedded NUL and C-string semantics can produce a valid prefix but incomplete flag.

Project rule:

- If candidate output has abnormal format, missing terminator, embedded NUL, or checker ambiguity, require second review or deterministic verification.

### Java Script Kiddie

Workflow value:

- Client-side reconstruction can be solved by reading transformation logic rather than guessing.
- File-format invariants and checksums are strong validators.

Project rule:

- For image/archive/document reconstruction, use magic bytes, parser validation, CRC/checksum, and independent decoding before accepting candidates.

### vault-door-8

Workflow value:

- Source reverse tasks should focus on final equality checks, transformation functions, and invertibility.
- Bit permutations/swap networks are usually reversible and can be verified by re-applying the original transform.

Project rule:

- For source-reverse tasks, accept a candidate only after original-checker or equivalent transform verification.

### Clouds

Workflow value:

- This was the strongest workflow drill: custom crypto + chosen-plaintext oracle + active nc service + probabilistic attack.
- A direct Z3/bit-vector approach timed out, which correctly signaled the need for structural cryptanalysis.
- Public writeups were useful for methodology, but old flags did not match the live instance and were rejected.
- Final output was accepted only after recovering keys and re-encrypting oracle plaintext/ciphertext pairs.

Project rule:

- If a task has custom crypto/protocol logic plus an oracle and generic tooling fails, escalate to structure/literature review instead of brute forcing longer.
- Treat external writeups/templates as method hints, not evidence.

## Escalation Criteria

Escalate from single-agent quick solving into research, subagent review, Claude/Cowork review, or Codex implementation when one or more are true:

```text
- custom crypto, protocol, serialization, auth, or access-control design
- active oracle/stateful service/per-instance secret
- generic solver/tool timeout or ambiguous result
- public PoC/writeup/template exists but may not match current instance
- candidate came only from UI success, scanner output, or external source
- output format is abnormal or has multiple candidates
- exploitability/impact claim would be made
- new reusable script/schema/module/reporting boundary is needed
```

Recommended routes:

```text
custom crypto + oracle + solver timeout
  -> crypto structure review / literature search / independent agent review

scanner high/critical or exploitability claim
  -> Hermes safety gate + Claude/Cowork triage + minimal verifier design

verification script needed
  -> Codex implementation with metadata, dry-run, scope checks, and tests

new platform contract/schema/module/report output
  -> OSS Recon Gate + review tiering policy
```

## Output-Side Review Checklist

Before treating any answer/finding as accepted:

```text
[ ] Is scope/authorization clear?
[ ] Is this output a hint, candidate, or verified result?
[ ] Is there an independent invariant/checksum/parser/oracle validation?
[ ] Does the result have expected format and terminator/wrapper rules?
[ ] Could the checker/UI/scanner have accepted a false positive?
[ ] Did any tool time out or fail in a way that changes confidence?
[ ] If using external writeups/PoCs, was the active instance verified?
[ ] Does this require a second agent/reviewer before reporting/submission?
```

## Backlog Seed

These are candidates for project implementation, not completed features:

1. `ctf_prepare_challenge.py`
   - create ignored local artifact directory
   - store challenge metadata
   - generate solve notes and output-side checklist
   - mark whether Kali fetch is required

2. `ctf_review_decision.py`
   - take structured solver output
   - classify as `hint`, `candidate`, `verified`, or `needs_second_review`
   - apply rules such as abnormal flag format, multiple candidates, tool timeout, external-source-only

3. `verifier_metadata.yaml` template
   - `category`
   - `requires_scope`
   - `destructive`
   - `oracle_required`
   - `second_review_triggers`
   - `evidence_outputs`

4. Helper templates
   - file-format reconstruction verifier
   - source-transform inversion verifier
   - active-service oracle capture harness
   - custom-crypto escalation checklist

## Guardrails

- Do not place live secrets, tokens, loot, or sensitive target outputs into committed files.
- Keep CTF raw artifacts and generated attack scripts under ignored local paths unless intentionally promoted after review.
- Scanner or solver output is triage/candidate until verified.
- If a CTF technique maps to real-world exploitation, preserve safety gates before implementing automation.
