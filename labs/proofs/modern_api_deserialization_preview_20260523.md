> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Modern API deserialization bounded-marker — Hermes tactical preview

Status: preview complete / tactical lens only / not a safety gate
Date: 2026-05-23
Lane: Dedicated unsafe deserialization bounded-marker rerun
Target: `labs/modern_vuln_api/modern_vuln_api.py` `/deserialize`

## Preview owner/tool

Hermes / GPT-5.5 via Hermes Agent.

## Visible model/runtime if available

Main session model visible in CLI context: `gpt-5.5` via `openai-codex` provider.

## Tactical focus

Test the newly fixed process once with the smallest useful local-lab wave:

```text
OSS/source reconnaissance -> Hermes tactical preview -> Kali bounded execution -> artifact pullback -> Claude Code read-only review -> Hermes synthesis
```

This preview is not an approval layer and does not add a safety gate. It chooses the proof path with the best project value for a quick process validation.

## Chosen proof path

Use the already source-controlled `modern_vuln_api.py` unsafe pickle endpoint and run a dedicated one-vulnerability marker-only proof:

- start the target on `<victim-vm>` at `<lab-ip>:18081`;
- from `<attacker-vm>` send baseline health, invalid/control deserialization payload, and positive bounded pickle payload;
- positive payload calls `record_deser_marker("DESER_PREVIEW_TEST_20260523")` only;
- verify `/deser-log` contains the marker;
- preserve request/response/log artifacts;
- stop the temporary target process.

## Accepted suggestions

- Keep this as a marker-only proof for process validation instead of using the stronger `record_deser_impact()` marker-file/callback sink.
- Use a dedicated artifact root so Claude Code can review a compact evidence packet without walking the whole repo.
- Classify result conservatively: this can validate the preview/review workflow and dedicated deserialization rerun shape, but should not become a new public-target/report claim.

## Rejected suggestions

- Do not add new schema/importer/report machinery for this test.
- Do not add extra reviewers beyond Claude Code review.
- Do not use callback, shell, command execution, public OAST, sensitive file read, credential access, or persistence.
- Do not turn preview/review into an approval workflow.

## Missing preconditions

- Confirm attacker/victim VMs are currently reachable on host-only network.
- Confirm SSH is reachable on attacker/victim.
- Confirm Python/curl are available on VMs.
- Copy or run source-controlled target code on victim.

## Execution plan

1. Create artifact root `<artifact-output-dir>/modern_api_deser_preview_test_20260523T<time>Z/`.
2. Copy `labs/modern_vuln_api/modern_vuln_api.py` to victim `/tmp/hermes_deser_preview/`.
3. Start the target with `python3 modern_vuln_api.py --host 0.0.0.0 --port 18081`.
4. From attacker, run capped curl checks: `/health`, invalid/control `/deserialize`, positive `/deserialize`, `/deser-log`, post-health.
5. Pull artifacts into the repo.
6. Stop victim target process.
7. Build compact review packet and ask Claude Code for read-only project-value/evidence review.

## Project value

This is valuable because it validates the new process on the current top lane without adding bureaucracy. If successful, the project gets a dedicated deserialization runner/evidence packet pattern separate from the older broad `modern_api_wave2` family, and proves that Hermes-preview + Claude-Code-review can improve tactical quality without becoming another safety gate.
