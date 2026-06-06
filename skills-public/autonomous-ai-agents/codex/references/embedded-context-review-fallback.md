> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Codex Direction Review with Embedded Context Fallback

Use this reference when Codex is acting as a read-only reviewer for a safety-sensitive repo and must attest to specific context files.

## Pattern

1. Start with a normal read-only Codex review prompt that lists required context files and asks for attestation.
2. If Codex cannot read local files because of sandbox/PTY/Windows execution friction, do not accept the review as complete and do not harden the transient error into a durable rule.
3. Build an embedded context packet from Hermes-controlled file reads:
   - original review prompt;
   - explicit note that local tool reads failed and Hermes is injecting synchronized context;
   - contents of each required context file;
   - `[MISSING]` marker for missing files;
   - optional truncation markers when a file is too large.
4. Rerun Codex with the embedded packet and tell it not to use local tools; it should attest to reading the embedded context rather than claiming direct file reads.
5. Save both receipts:
   - the first failed/provisional review, if useful for audit;
   - the final embedded-context review;
   - the embedded packet path;
   - the event log / output-last-message path.
6. In the synthesis, state the provenance difference clearly: e.g. Claude Code direct-read completed; Codex embedded-context review completed after local-read friction.

## Why this matters

For Cybersec Lab direction reviews, context synchronization and attestation are policy-required. A reviewer that could not read the required files must not be treated as an approving reviewer. The embedded packet fallback preserves review diversity while keeping the receipt honest.

## What not to record

Do not create a persistent rule saying Codex cannot read files or that Windows sandbox is broken. Capture only the retry pattern: when a required-attestation reviewer cannot directly read context, inject a bounded synchronized context packet and label the receipt provenance.
