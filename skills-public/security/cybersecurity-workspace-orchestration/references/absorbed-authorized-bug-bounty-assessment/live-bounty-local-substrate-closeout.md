> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Live-bounty local substrate closeout pattern

Use this reference when an authorized bug bounty lane has accumulated local-only automation support (schemas, queue/state, status helpers, redaction checks, runners, grounding packets) and the user asks whether the engineering work is effectively finished.

## Pattern

1. Treat local orchestration helpers as decision/support artifacts, not authorization to touch a target.
2. Seal the substrate once it has:
   - machine-readable lane state and evidence schemas;
   - a queue/status validator;
   - redaction checks for evidence promotion;
   - local-only runner decisions with stable exit codes;
   - local-only reference/preview grounding;
   - focused regression tests;
   - an independent review or equivalent safety-focused check;
   - handoff/navigation/Obsidian/accepted_changes updates.
3. Create a closeout artifact that states:
   - sealed scope;
   - exact boundaries: no target request, browser automation, signup/login, scanner/fuzzer/DAST, callback, exploit, workflow execution, credential handling, or report submission;
   - current machine queue result;
   - next operator gate;
   - reopen criteria;
   - debug-only vs retained status artifacts.
4. Update navigation/active queue to say no further engineering slice is active by default. This prevents schema/tooling drift.
5. Move attention back to the true lane gate (for example operator identity/login, second owned account, or scope confirmation).

## Exit-code convention from the session

A useful local-only runner convention:

```text
0  autonomous_local_action_available
10 blocked_operator_action
20 blocked_scope_or_policy
30 invalid_queue_or_state
```

Target-like arguments such as `--target`, `--url`, `--host`, `--scope`, and `--live` should fail closed as structured JSON before argparse can produce plain-text errors, including bare flags.

## Anti-drift rule

If the local substrate already has queue/status/runner/grounding/redaction/tests/review, do not keep adding tools by default. Reopen only when:

```text
operator explicitly asks for wrapper/promotion tooling
a focused regression fails
schema cannot represent a real authorized lane
redaction false-positive/false-negative blocks safe promotion
a stable CLI wrapper is needed after repeated manual use
```

Otherwise, resume live-lane work only after the real operator gate is cleared.
