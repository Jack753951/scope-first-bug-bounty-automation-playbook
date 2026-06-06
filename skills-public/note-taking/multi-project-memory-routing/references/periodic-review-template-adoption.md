> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Periodic Review Template Adoption Pattern

Use this when one project develops a better periodic/deep-review workflow and the user asks to adopt the useful parts into another project.

## Goal

Turn cross-project process improvements into project-local review templates without copying source-project state, risks, or domain-specific artifacts.

## Reusable adoption steps

1. Inspect the source project's review-policy files for process structure only: review tiers, freshness metadata, final decision blocks, reviewer identity/model labeling, milestone batching, and authority rules.
2. Translate the risk vocabulary into the target project domain. Example: a security project's activation gate may become a media project's upload/publish/schedule/OAuth/channel-destination gate.
3. Write a short project-local adoption note summarizing what was adopted, adapted, and rejected.
4. Update the target project's active queue / accepted changes, not global memory, with the current implementation status.
5. If the target project has a packet generator, implement the process in the generator rather than relying on reviewers to remember it manually.
6. Keep fallback builders aligned with the primary builder. For example, if Python packet generation adds freshness/tier/identity/decision blocks, PowerShell fallback should emit equivalent blocks.
7. Verify by generating a safe packet and reading the produced snapshot/prompt/template files.

## Recommended generated packet blocks

- `Freshness / Authority`: packet frozen date, latest safe handoff inspected, post-packet inclusion/exclusion, authority rule when stale packets conflict with live code or accepted handoff.
- Project-specific review tiers: for media projects, YT0-YT3 is useful, with upload/publish/schedule/OAuth/channel-destination/privacy activation as YT3.
- `Reviewer Identity`: route/tool, visible runtime model, provider/runtime limitation, review scope.
- `Final Decision Block`: PASS/PASS_WITH_CONDITIONS/REQUEST_CHANGES/DEFER/ESCALATE_TO_USER, tier, owner/authority, reviewers consulted, validation, blocking findings, non-blocking recommendations, safety boundary, user-approval requirement, next safe action.

## TDD guardrail

For code-backed packet generators, add tests first that fail when these blocks are missing from generated snapshots, prompts, and blank reviewer-output templates. Then implement the smallest generator/template change and smoke-run the packet builder.

## Pitfalls

- Do not copy source-project domain rules wholesale. Translate the reusable process, not the source project's state.
- Do not let fallback generators go stale; future agents may run them when the primary runtime is unavailable.
- Do not store generated packet artifacts in Hermes memory. Store only the reusable pattern in skills and the project-specific status in repo handoff.
- A generated packet is frozen review input, not live truth. It must state how conflicts with later handoff/live code are resolved.
