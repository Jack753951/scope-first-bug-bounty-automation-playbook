> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

---
name: multi-project-memory-routing
description: Use when coordinating Hermes memory, repo handoff files, Obsidian notes, skills, and session_search across multiple projects. Provides process and judgment criteria, not a project database.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [memory, obsidian, handoff, multi-project, governance]
    related_skills: [obsidian, hermes-agent]
---

# Multi-Project Memory Routing

> **Note (2026-05-28):** Hermes orchestration retired in this project. Active driver = Claude Code single-agent. The "Hermes durable memory" layer in this skill is now Claude Code's auto-memory at `~/.claude/projects/<project>/memory/`; the routing principle ("compact cross-project signposts only, project facts stay in repo handoff or Obsidian") still holds.

## Added project reference

- `references/youtube-agent-learning-review-memory-bridge.md` — YouTube/content automation pattern for making Hermes private memory, repo handoff, and Obsidian-style long-term goals visible to Claude Code/Codex reviewers via explicit bridge files, while keeping multi-agent review learning-only rather than a new safety gate.

## Overview

Use this skill to decide where durable knowledge belongs when one Hermes profile is used across multiple projects. The skill is a process and judgment framework, not a storage location and not a project database.

Core principle:

```text
Hermes memory = compact cross-project signposts.
Repo handoff = project engineering truth.
Obsidian = long-term strategy, research, decisions, experiments, and review synthesis.
Skills = reusable procedures and judgment criteria, not project databases.
session_search = recall leads that must be verified.

If the user explicitly says to "remember", "善用", or otherwise rely on this memory-flow skill, treat that as a trigger to load this skill before deciding where information belongs. Still store only the durable preference/signpost in Hermes memory; project facts stay in repo handoff or Obsidian.
```

Do not copy project state into this skill. Project-specific data stays in each repo handoff or project Obsidian namespace.

## When to Use

Use this skill when:

- The user asks whether Hermes memory is shared across projects.
- Multiple repos need to coexist under the same Hermes profile.
- A project wants to align with another project's memory flow.
- You are deciding whether to save something to Hermes memory, Obsidian, a repo handoff file, or a skill.
- The user explicitly says that memory saves must be routed/classified first; classify before any `memory` tool call.
- You are auditing memory drift, handoff drift, goal drift, or project-structure drift.
- You are creating a durable process from repeated experience and need to avoid turning global memory into a project database.

Do not use this skill to store:

- Project progress logs.
- PR numbers, issue numbers, commit SHAs, or dated run artifacts.
- Secrets, credentials, OAuth tokens, cookies, scan output, target details, or private client data.
- Full project strategies or review reports.

## Authority Order

When memory layers disagree, use this order:

1. Current explicit user instruction.
2. Live project files, config, validation output, and current repo state.
3. Repo handoff files for accepted engineering state.
4. Active Obsidian project notes for long-term strategy, decisions, research, experiments, and review conclusions.
5. Hermes durable memory for compact preferences, safety rules, and pointers.
6. session_search only as recall; verify against files before treating it as current truth.

## Layer Responsibilities

### Hermes Durable Memory

Purpose: small profile-level memory that can safely affect multiple sessions and projects.

Use for:

- User-wide preferences: language, command style, review depth, visual QA preference.
- Cross-project safety/routing principles that remain true for weeks or months.
- Short index facts pointing to the correct project memory location.

Avoid:

- Daily progress, phase completion logs, PR/issue/commit IDs, one-off validation status.
- Full strategies, complete reviews, detailed implementation history.
- Anything likely to be stale within a week.
- Imperative instructions like "always run X" unless truly universal and user-approved.
- Secrets, credentials, tokens, cookies, private target details, sensitive runtime output.

Write memories as declarative facts, not commands. Prefer:

```text
Project Y uses repo handoff as engineering truth and Obsidian for strategy notes.
```

Avoid:

```text
Always update Project Y before doing anything else.
```

### Repo Handoff Files

Purpose: project-local engineering truth and audit trail.

Use for:

- Accepted implementation changes.
- Validation outcomes.
- Worker outputs that affect the repository.
- Blocked follow-ups and safety gates.
- Current engineering constraints a future worker must inspect.

Repo handoff answers:

- What changed?
- What was verified?
- What is accepted, blocked, or unsafe?
- What must a future implementation worker know?

### Obsidian Project Notes

Purpose: durable, searchable, linked project-domain memory outside one repo diff.

Use for:

- Strategy and roadmap rationale.
- Research and reference synthesis.
- Decision records.
- Experiment hypotheses, results, and adoption decisions.
- Periodic review synthesis and project-health conclusions.
- Methodology notes that improve future reasoning.
- Technical notes, vulnerability notes, sanitized lab lessons, and long-term strategy that are too project-specific or detailed for global Hermes memory.

Project-domain memory requirements:

- Keep global Hermes memory project-detail-light; store only compact cross-project preferences/signposts there.
- Write project technical/vulnerability/strategy notes into the matching Obsidian project namespace, not a shared/global bucket.
- Maintain a project index such as `00_Index/Home.md`, `00_Index/Active Projects.md`, or `00_Index/Memory Map.md` so notes remain discoverable.
- When creating or materially updating a durable Obsidian note, update the relevant project index when the note changes navigation or active strategy.
- Prefer sanitized vulnerability notes and methodology; do not copy raw exploit chains, loot, secrets, private scope, or sensitive target evidence into Obsidian.

Recommended metadata for durable notes:

```markdown
Status: active | superseded | rejected | experiment | reference
Source: User | Hermes | Claude | Codex | Mixed
Date: YYYY-MM-DD
Repo truth: path/to/handoff-or-code-file, if applicable
```

Each project should maintain an index note that points to current active guidance only. Old notes should be marked `superseded`, `rejected`, or `reference` rather than silently deleted.

### Skills

Purpose: reusable procedures and judgment criteria.

Use skills for workflows that should transfer across projects:

- A repeatable debugging process.
- A memory-routing decision tree.
- A review checklist.
- A validation recipe.
- A safe orchestration pattern.

Do not put raw project data in skills. Skills should describe how to decide and act, not store what happened in a specific project.

### session_search

Purpose: recall and discovery.

Use for:

- Finding earlier conversations when the user says "last time" or "remember when".
- Recovering leads for where a decision may have been written.

Never treat session_search as authority by itself. Verify recovered claims against repo files, active Obsidian notes, or live system state before acting.

## Decision Tree: Where Should This Go?

Ask these questions in order:

1. Is it a secret, credential, private token, cookie, client-sensitive data, or unsafe target detail?
   - Store nowhere. Record only non-sensitive safety rules if useful.

2. Is it a reusable workflow or judgment rule applicable across projects?
   - Put it in a skill or update an existing skill.

3. Is it a stable user preference or cross-project routing/safety rule?
   - Put a compact declarative entry in Hermes durable memory.

4. Is it accepted engineering state, validation output, or worker coordination for one repo?
   - Put it in that repo's handoff files.

5. Is it long-term project strategy, rationale, research, decision context, experiment result, or review synthesis?
   - Put it in that project's Obsidian namespace.

6. Is it temporary progress, a one-off run result, or a short-lived TODO?
   - Keep it in the current session or repo-local task tracking only if needed. Do not promote to durable memory.

7. Did the user say an existing global memory item should be deleted, but it is actually project-specific context that may remain useful?
   - Treat the correction as a layer/routing fix: rehome the useful fact to the project's Obsidian namespace or repo handoff first, then remove or compact the Hermes global memory entry. See `references/project-specific-memory-rehoming.md`.

## Cross-Project Alignment Procedure

When aligning two projects:

1. Read each repo's local context file such as `.hermes.md`, `AGENTS.md`, or equivalent.
2. Read each repo's memory/handoff policy if present.
3. Compare process and authority order, not raw project data.
4. Before proposing a new skill, list/search existing skills and prefer updating this umbrella or another class-level skill over creating a duplicate narrow skill.
5. Extract common principles into a shared note or skill.
6. Keep project-specific overrides in each repo unless the override is a reusable class-level rule.
7. Add Obsidian links only to indexes or policy notes, not to sensitive raw data.
8. Save only a compact pointer in Hermes durable memory if the alignment should affect future sessions. If the user explicitly says to use memory-routing discipline for future saves, update this skill or the relevant class-level skill with the workflow preference, then route project-specific environment details to repo handoff/Obsidian rather than global memory.
9. Validate that periodic reviews include memory drift and handoff drift checks.

See `references/cross-project-memory-alignment-example.md` for a concise example of aligning a media automation project and a cybersecurity lab without turning this skill into a project database.

See `references/upstream-subproject-main-architecture-alignment.md` for the pattern to use when an upstream/helper repo must serve a main project's architecture: inspect the main channel/config/engine/profile registries first, mirror real channel names, fail closed for unknown channels, and keep production activation gates untouched.

See `references/phase-boundary-routing.md` for a concise example of routing a user-stated project phase boundary into repo handoff instead of global memory or skill state.

See `references/active-strategy-queue-closeout.md` for the closeout pattern when a project has many review artifacts: close the phase in repo handoff, complete pending review synthesis, then create a compact active strategy queue before starting another lane.

See `references/memory-compaction-notification.md` for a concise pattern for notifying a project before compacting global Hermes memory so future workers do not mistake shorter memory for changed project direction.

See `references/near-capacity-memory-routing.md` for the near-capacity pattern: compact/replace an overlapping existing memory entry into a denser declarative signpost instead of forcing a new session-log-shaped memory.

See `references/mandatory-pre-save-routing.md` for the mandatory pre-save routing pattern: when the user asks that all memory saves pass through routing, classify the fact before any `memory` call and report where it was stored or intentionally not stored.

See `references/session-memory-skill-hygiene-review.md` for the post-session hygiene pattern: split durable user preferences from reusable workflow lessons, compact memory when near capacity, and update class-level skills or references rather than creating one-off session skills.

See `references/project-profile-isolation-routing.md` for the profile-isolation pattern: create large-project profiles to isolate durable memory/context, but stage migration so existing cron/Gateway production ownership is not moved or duplicated without an explicit checklist.

See `references/periodic-review-freshness-convention.md` for the review-packet freshness pattern: every periodic/deep review packet should state its frozen date, latest live handoff inspected, post-packet changes included/excluded, and authority rule when stale packets conflict with active handoff or live code.

See `references/high-ri<api-key-redacted>.md` for the pattern to use when a project asks to move from internal/readiness work into live scheduling, upload, publication, OAuth, destination, privacy, or other production-affecting activation.

See `references/exact-artifact-scheduled-canary-routing.md` for the pattern to use when a media/automation project schedules or uploads one exact already-reviewed artifact as a narrow canary: verify exact artifact QA, destination/auth/channel identity, privacy/schedule semantics, platform read-back, and record only repo-local artifact details.

See `references/ri<api-key-redacted>.md` for the pattern to use when a media/automation project is over-gated: keep upload/publication/OAuth/scheduler gates strict, but make local-only learning fast and move positive Claude/visionreview candidates toward exact-artifact canaries for live data.

See `references/cross-project-process-adoption-matrix.md` for the pattern to use when borrowing review, periodic-review, tiering, decision-gate, or milestone-batching improvements from one project into another without copying project-specific risks or state.

See `references/periodic-review-template-adoption.md` for the implementation pattern when cross-project review-process improvements should be encoded into a target project's periodic review packet generator and fallback templates.

See `references/rolling-handoff-archive-and-contract-boundaries.md` for the pattern to use when borrowing process fixes about overwritten rolling handoff files, local archive backups, and the difference between strict machine-readable contracts and flexible governance Markdown.

See `references/project-memory-governance-adoption.md` for the pattern to use when converting a useful memory/review workflow from another project into project-local governance files such as memory routing, active strategy queue, periodic freshness templates, and project context pointers.

See `references/workflow-process-change-governance-routing.md` for the pattern to use when the user corrects a project workflow/process rule that future agents must follow: classify the correction, update class-level skill only for reusable routing, write project-local governance/handoff, and also record long-term rationale in the project's Obsidian namespace when it affects future reasoning or review behavior.

See `references/source-project-architecture-extraction-for-new-product.md` for the pattern to use when a user starts or reshapes a new product by referencing existing projects: inspect source authority layers, extract process patterns rather than domain nouns, translate them into the target domain, create target-local charter/architecture/handoff artifacts, and save only a compact global memory signpost.

See `references/product-strategy-and-business-cycle-routing.md` for the follow-on pattern when architecture extraction turns into long-term goal, subscription strategy, phase roadmap, or business-cycle modeling: label assumptions, keep detailed strategy in repo/Obsidian, update the active queue, and preserve activation gates.

See `references/worker-max-turn-recovery-routing.md` for the pattern to use when a worker wrapper exits with max-turn/partial-output status but may have produced useful repo artifacts: inspect partial outputs, promote useful content into named handoff artifacts, verify locally, and keep run-specific details out of global memory.

See `references/worker-context-boundary-routing.md` for the pattern to use when explaining or designing what Claude Code, Codex, Cowork, or other external workers know: distinguish prompt-included context from files merely available on disk, add explicit required context reads for project navigation/strategy notes, and avoid copying detailed project state into global memory.

See `references/review-to-launch-estimate-routing.md` for the pattern to use when a review/implementation slice closes and the user asks for today's goal, next workflow, or launch timeline: tier readiness, keep estimates in repo handoff, and recommend the next safe non-activation slice.

See `references/status-question-readonly-routing.md` for the pattern to use when the user asks for the long-term goal, current phase, or where the project stands: answer from project authority layers without advancing implementation, generation, upload, scheduling, or publication.

See `references/compaction-latest-message-reanchor-routing.md` for the pattern to use when a context-compaction block or handoff summary appears before a new live request: re-anchor on the latest user message, treat the summary as background only, and do not answer stale tasks from the compacted history.

See `references/automation-goal-status-correction-routing.md` for the pattern to use when the user corrects a status/goal summary because it underplayed automation, productionization, launch, or another durable goal dimension: update project-local navigation, preserve activation gates, and do not treat the correction as runtime approval.

See `references/ri<api-key-redacted>.md` for the pattern to use when the user agrees that heavy safety/review gates are slowing learning: re-tier local-only experiments for faster batch learning while preserving hard gates for upload, publication, OAuth, scheduler, destinations, default privacy, deletion, and other high-risk actions.

See `references/parking-content-direction-routing.md` for the pattern to use when the user shelves, pauses, or says to set aside a content direction or project lane: record the boundary in repo handoff/active queue as note-only project state, not global memory or skill state, and do not treat it as approval to advance another lane.

See `references/paused-upload-gate-vs-learning-loop-routing.md` for the pattern to use when the user corrects a project status because a paused upload/scheduled-publication gate was incorrectly treated as pausing the whole local-only learning/data loop: preserve the distinction, verify scheduler state when relevant, and restore only the narrow safe loop unless exact activation is approved.

See `references/single-scheduler-production-ownership-routing.md` for the pattern to use when a production-affecting automation loop could be owned by multiple schedulers or gates: verify all owners, make one cadence owner authoritative, pause/disable duplicates, and record exact job/task state repo-locally.

See `references/content-lane-decision-routing.md` for the pattern to use when the user says to remember a creative/channel direction and continue work: split compact durable preference from project-local lane decision, update repo handoff/queues, continue only inside the authorized lane, and keep activation gates closed.

See `references/content-review-purpose-correction-routing.md` for the pattern to use when the user corrects the success criterion for creative/vision review, such as centering human fun, interest, attention retention, payoff clarity, or other audience-facing outcomes: update repo handoff and project strategy notes, save only compact global signposts, and do not treat the correction as runtime activation approval.

See `references/project-specific-memory-rehoming.md` for the pattern to use when the user says a global memory entry should be deleted or belongs in project memory: distinguish destruction from removal-from-global-memory, rehome still-useful project facts to Obsidian/repo handoff, then remove or compact the global entry.

See `references/inactive-project-global-memory-removal.md` for the pattern to use when the user says a project is paused/inactive/not currently enabled and asks to remove its global-memory signpost: remove only the global signpost, do not mutate repo/Obsidian/runtime state, and avoid treating temporary inactivity as a permanent ban.

See `references/global-memory-index-project-namespace-first.md` for the pattern to use when the user wants project memory broadly moved out of Hermes durable memory: preserve project readability in Obsidian/repo handoff first, add compatibility notes for future agents, then compact global memory into namespace pointers and cross-project preferences only.

See `references/shared-handoff-append-only-and-cron-reporting.md` for the pattern to use when multiple agents or cron jobs write shared handoff Markdown: keep durable accepted-change logs append/prepend-only, re-read before patching, move long outputs into named artifacts, and keep pending activation gates visible in scheduled reports.

See `references/checkpoint-waiting-readiness-snapshot.md` for the pattern to use when the user asks to continue but the next meaningful project checkpoints are not mature yet: perform read-only prechecks, write a named repo-local readiness snapshot, update the active queue, and avoid premature generation/upload/scheduler actions.

See `references/mature-checkpoint-observation-retry-routing.md` for the follow-on pattern when a time-gated observation matures but the first readout hits a local helper/import/token-refresh caveat: classify the anomaly, patch/rerun only read-only observation if safe, preserve the superseded artifact, and avoid promoting helper bugs into project strategy.

See `references/unverified-current-intel-quarantine-routing.md` for the pattern to use when current-facts/CVE/advisory/threat-intel drafts are useful leads but not primary-source verified: quarantine them repo-locally, downgrade action wording, and require fresh verification before use.

See `references/cybersec-vulnerability-material-coverage-routing.md` for the pattern to use when the cybersec/hacking workspace asks how much of a vulnerability corpus has been tested: split family-touch coverage from individual material-entry coverage, keep ratios repo-local, and avoid treating broad local-lab coverage as public-target readiness.

See `references/cybersec-lab-navigation-cleanup-routing.md` for the pattern to use when cybersec lab capability and artifacts are growing but navigation is becoming hard to follow: create a compact current-navigation cleanup before new vuln lanes, keep public-target gates explicit, and route strategy/rationale to repo handoff plus Obsidian.

See `references/artifact-index-before-hardening-routing.md` for the pattern to use when a repo has many handoff/worker/evidence/schema/debug artifacts and needs a compact classification index before the next engineering-hardening slice: distinguish active substrate from garbage, wire the index into navigation, quarantine unverified current-intel, and validate before declaring readiness for the next engineering-hardening slice.

See `references/handoff-directory-policy-cleanup.md` for the pattern to use when `handoff/` has become a catch-all for rolling IPC, navigation, policies, target notes, lab proofs, worker receipts, and phase history: inventory, write a migration plan/manifest, archive long navigation snapshots, move artifacts into class-level directories, compact indexes, update active lane/path pointers, patch wrappers that still write receipts into `handoff/`, and validate without treating cleanup as target-testing authorization.

See `references/cybersec-phase-status-routing.md` for the pattern to use when the user asks the cybersec/hacking workspace's long-term goal, current phase, retest status, or what a review/feasibility decision means operationally: answer read-only from project-local navigation/handoff artifacts, separate feasibility from verified proof, and keep live-target authorization gates explicit.

See `references/cybersec-live-target-precontact-gate-routing.md` for the pattern to use when scope/readiness checks are complete but the next cybersecurity step crosses into live target contact or signup/auth gates: split scope authorization from autonomous target-touching permission, write a repo-local pre-contact checkpoint, and require only non-sensitive operator status replies before resuming low-risk mapping.

## Cross-Project Process Adoption

When the user asks to reference another project and keep only what helps the current project:

1. Compare process patterns and authority boundaries, not raw project content.
2. Translate domain-specific risks into the target project's equivalent activation risks.
3. Prefer a short project-local adoption note plus active queue / accepted changes update over a broad policy rewrite.
4. Preserve reviewer identity/model labeling and final decision blocks for non-trivial reviews.
5. Use milestone batching and periodic freshness metadata when the source project improved review hygiene.
6. If a periodic/deep-review packet generator exists, encode adopted blocks directly into generated snapshots, prompts, and blank reviewer-output templates.
7. Keep fallback generators/templates aligned with the primary generator so a degraded runtime does not silently drop review safeguards.
8. Update this skill or another class-level skill only with the reusable procedure; keep source/target project facts in their repo handoff or Obsidian notes.
9. When adopting rolling-file workflow fixes, archive existing non-empty rolling outputs before wrapper overwrite, but keep durable decisions in named artifacts / accepted-change logs rather than treating local archives as authoritative.
10. When adopting strict boundary-contract fixes, apply closed-field/fail-closed validation only to machine-readable contracts; keep human review Markdown flexible with freshness, authority, reviewer identity, and decision metadata.

## Memory Compaction / Preference Notification Pattern

Use this pattern when Hermes durable memory is near capacity or a user-wide preference is added that may affect an existing project.

1. Do not treat memory compaction as a project-state change.
2. Before or alongside compaction, write a short notice into the affected repo's memory/handoff policy, if one exists.
3. If there is a shared Obsidian alignment note for that project, add the same compact notice there.
4. Record only the stable preference or compact pointer in Hermes memory; keep detailed project state in repo handoff or Obsidian.
5. If the preference changes operational behavior across projects, state its project-local interpretation explicitly.
6. For deletion preferences specifically, distinguish ordinary recoverable files, sensitive material requiring user confirmation, and clearly rebuildable caches/artifacts.
7. When memory is near full, first look for an overlapping existing entry to compact/replace with a denser declarative signpost; do not append a session narrative just because the new fact is useful.
8. If no safe compaction target exists, route the detail to project handoff or Obsidian and either save a very short pointer or explicitly skip global memory.
9. Verify the docs/policy edit according to the project norm, but do not run unrelated tests or mutate runtime data just to record a memory-routing notice.

## Recommended Obsidian Namespace Pattern

Prefer one vault with clear namespaces unless the user explicitly wants hard isolation:

```text
Shared/
Projects/YouTubeAgent/
Projects/Cybersec Lab/
Projects/InvestmentAutomation/
```

Use `Shared/` only for cross-project governance, templates, and non-sensitive shared process notes. Project-specific state belongs in the matching project namespace.

If using Obsidian Local REST API, remember it follows the vault currently open in Obsidian. Verify the active vault or use filesystem fallback before writing important notes.

## Obsidian API vs Filesystem Routing

Default to filesystem-first writes when the vault path is known and the task is ordinary note creation/editing. Direct Markdown writes are sufficient for most project-domain memory updates and work even when Obsidian is closed.

Use the Obsidian Local REST API when the task benefits from app-aware memory-library control:

- verifying which vault is currently open in Obsidian;
- reading the API-visible vault tree;
- maintaining project indexes and wikilinks/backlinks;
- creating or updating related-memory structures such as `Memory Map.md`;
- writing a note and immediately reading it back through the same API route;
- checking that API-relative project roots match the intended filesystem namespace.

If API credentials are configured but the local server refuses connection, treat it as setup/runtime state, not a durable tool failure. Ask the user to open Obsidian, enable the Local REST API plugin in the intended vault, and then retest. Continue with filesystem-first if direct vault writes are available and the task does not require app-aware API state.

## Sensitive-Project Additions

For cybersecurity, legal, finance, or client-sensitive projects, add stricter local rules:

- Do not store target details, scan output, exploit payloads, hashes, loot, cookies, credentials, private scope/rules, or client-sensitive data in Hermes memory.
- Keep authorization/scope gates in repo-local policy and handoff files.
- Treat current CVE/threat-intel claims as current facts requiring fresh primary-source lookup.
- Use Obsidian for methodology and decision rationale, not raw sensitive evidence.

## Review Identity / Model Labeling

When writing any review, third-party review, periodic review, artifact QA report, code review, or project-health packet for this user, include a short reviewer identity block near the top:

```markdown
## Reviewer identity

- Reviewer route/tool: Hermes subagent | Claude Code CLI | Codex CLI | local QA script | vision review | other
- Visible runtime model: `<model if exposed>` or `not exposed by tool`
- Provider / CLI version if visible: `<provider/version>`
- Review focus: creative | engineering | safety | subtitle/audio QA | visual QA | strategy | mixed
- Limitation: state if the exact underlying model or deployment details are not exposed
```

This is a cross-project user preference. Apply it in repo handoff and Obsidian review notes as well as chat summaries. Do not overclaim a model: if a wrapper only exposes the route or CLI version, write `model: not exposed by tool` and list the visible route/version instead.

## Periodic Review Checklist

During a periodic project-health review, check:

- [ ] The review packet includes reviewer route/tool, visible runtime model when exposed, provider/CLI version if visible, review focus, and limitations when exact model is not exposed.
- [ ] The review packet states its packet frozen date, latest handoff date inspected, and whether post-packet changes are included or excluded.
- [ ] When a frozen packet conflicts with active strategy queue, accepted changes, live code, or fresh validation, the live/project-local authority is explicitly used.
- [ ] Hermes durable memory contains only compact cross-project facts and pointers.
- [ ] Repo handoff reflects accepted engineering changes and validation status.
- [ ] Obsidian project index points to active strategy, decisions, experiments, and review process.
- [ ] Superseded Obsidian notes are clearly marked.
- [ ] session_search findings were verified against files before use.
- [ ] No secrets or credential material were copied into notes or handoff summaries.
- [ ] Project-specific rules are not leaking into unrelated projects through global memory.
- [ ] Reusable process improvements are captured as skills, not long memory blobs.
- [ ] Periodic review prompts include memory drift, handoff drift, goal drift, and structure drift.
- [ ] Broad review findings are synthesized into a compact active-priority/strategy queue before starting another implementation lane.

## Common Pitfalls

1. Turning Hermes memory into a project database.
   - Fix: store only compact pointers and stable preferences globally.

2. Turning a skill into a project log.
   - Fix: skills contain process and judgment criteria only; project facts belong in handoff or Obsidian.

3. Treating session_search as truth.
   - Fix: use it to locate leads, then verify with files.

4. Letting Obsidian become unstructured storage.
   - Fix: maintain project indexes and note status fields.

5. Copying one project's success metric into another.
   - Fix: keep project-specific goals in repo/Obsidian policy, not global memory.

6. Storing sensitive operational data because it feels useful later.
   - Fix: store the rule or methodology, not the raw sensitive data.

7. Promoting an active phase boundary into a global rule.
   - Fix: when the user says to finish a project phase before starting another workstream, record the boundary in that repo's handoff/decision layer unless it is explicitly cross-project. Keep the reusable routing lesson in this skill, not the project state. See `references/phase-boundary-routing.md`.

10. Do not turn worker-wrapper failures into global memory or tool refusals.
   - Fix: route max-turn/error runs through project handoff recovery: inspect logs and archived rolling artifacts, preserve usage/result metadata in named repo artifacts, verify live repo state locally, and record only the reusable recovery pattern in a skill. See `references/worker-max-turn-recovery-routing.md`.

11. Treating a launch estimate as a single project-memory fact.
   - Fix: create a repo-local estimate with readiness tiers and activation gates, then summarize the next safe slice in chat. Keep exact dates, PRs, commits, and validation snapshots out of global memory. See `references/review-to-launch-estimate-routing.md`.

13. Treating a status/orientation question as approval to proceed.
   - Fix: when the user asks for the long-term goal, current phase, or where the project stands, first answer read-only from project authority layers. Label the next safe action as proposed/not executed unless the user explicitly says to continue. See `references/status-question-readonly-routing.md`.

13b. Answering stale compacted-history tasks instead of the latest live user message.
   - Fix: after a context-compaction block or recovered-session summary, explicitly re-anchor on the latest user message after the summary. Treat the compacted text as background only, especially if it mentions previous side-effect work or already-addressed questions. See `references/compaction-latest-message-reanchor-routing.md`.

13a. Treating a learning-speed correction as either safety removal or immediate runtime approval.
   - Fix: when the user says safety/review gates are slowing learning, re-tier the process: local-only experiments can move in lightweight batches, but upload/publication/scheduler/OAuth/destination/default-privacy/runtime-deletion gates remain strict and explicit. Update project-local strategy/navigation, not global memory, and do not generate/upload merely because the strategy was corrected. See `references/ri<api-key-redacted>.md`.

14. Treating a parked idea as either a global ban or a new active lane.
   - Fix: when the user shelves a content direction or project lane, record the boundary in the project-local handoff/routing index as note-only state, avoid global memory unless it is a stable cross-project preference, and do not advance another lane without explicit approval. See `references/parking-content-direction-routing.md`.

14a. Treating a paused upload gate as a paused learning/data loop.
   - Fix: if the user corrects this distinction, update project-local wording so upload/scheduled/publication gates stay paused while local-only drafts, read-only analytics, QA, and batch learning may continue if authorized. Verify actual scheduler/cron state before claiming the safe loop is running. See `references/paused-upload-gate-vs-learning-loop-routing.md`.

14b. Letting multiple schedulers own the same production cadence.
   - Fix: when OS scheduler, Hermes cron, app loop, upload gate, or scheduled-publication jobs can duplicate each other, verify all owners, choose exactly one active cadence owner unless explicitly approved otherwise, pause/disable duplicates, and record job/task state in repo handoff rather than global memory. See `references/single-scheduler-production-ownership-routing.md`.

14. Rewriting shared handoff Markdown after another worker or cron run.
   - Fix: for accepted-change logs and other durable collaboration surfaces, re-read immediately before patching, append/prepend short entries only, and place long outputs in named artifacts. Archive-before-overwrite is for known rolling convenience files, not a license to replace arbitrary shared handoff Markdown. See `references/shared-handoff-append-only-and-cron-reporting.md`.

15. Treating “remember this direction and continue” as either pure global memory or broad activation approval.
   - Fix: split the durable preference from the lane decision. Put exact creative/channel lane decisions, artifacts, validation, and blockers in repo handoff/queues; save at most a compact global signpost; continue only inside the explicitly authorized lane and keep activation gates closed. See `references/content-lane-decision-routing.md`.

15a. Treating a creative/vision review correction as chat-only or as mere technical QA.
   - Fix: when the user corrects the audience-facing success criterion for review, update project-local handoff/routing and strategy notes so future reviewers judge the intended outcome (e.g. human fun, interest, attention retention, payoff clarity) separately from technical readiness. Keep runtime activation gates explicit. See `references/content-review-purpose-correction-routing.md`.

16. Letting scheduled reports imply readiness beyond the gate actually passed.
   - Fix: cron/local-draft reports must keep downstream activation gates explicit, such as marking visual review as pending before private canary when render QA alone is insufficient. See `references/shared-handoff-append-only-and-cron-reporting.md`.

16a. Treating an exact-artifact canary as broad runtime permission.
   - Fix: schedule/upload only the explicitly selected reviewed artifact, verify destination/auth/privacy/schedule semantics and platform read-back, record IDs/timestamps in repo handoff only, and state that no generic generation loop, unrelated scheduler/OAuth/default-privacy/config change, deletion, or immediate publication was done. See `references/exact-artifact-scheduled-canary-routing.md`.

16. Treating a pre-checkpoint “continue” request as permission to start a new lane.
   - Fix: if the next accepted phase is time-gated observation and the checkpoint is not mature, do active read-only work instead: verify current time/gates/status, write a named repo-local readiness snapshot, update the active queue, and wait for the mature checkpoint. See `references/checkpoint-waiting-readiness-snapshot.md`.

17. Treating unverified current-intel drafts as project truth.
   - Fix: quarantine fallback CVE/advisory/threat-intel drafts in repo-local `unverified/` storage, add a warning, downgrade action wording, and require fresh primary-source verification before using them for reports, scans, or operational decisions. See `references/unverified-current-intel-quarantine-routing.md`.

18. Treating a local observation-helper failure as a project gate failure.
   - Fix: classify whether the anomaly came from the helper/cwd/import path, expected token refresh during read-only API access, or actual platform/channel/privacy status. If it is local and safely fixable, patch and rerun the same read-only observation, keep the first artifact as superseded, and update repo handoff without changing activation gates. See `references/mature-checkpoint-observation-retry-routing.md`.

19. Treating a global-memory removal request as pure deletion when it is really a routing correction.
   - Fix: if the content is project-specific but still useful, rehome it into the project's Obsidian namespace or repo handoff, then remove/compact the global memory entry. Report both the removal and the project-local destination. See `references/project-specific-memory-rehoming.md`.

20. Compacting global memory before future agents can still understand the project.
   - Fix: before removing detailed project facts from Hermes memory, add or update project-local Obsidian/repo handoff routing notes, including a compatibility note that shorter global memory is intentional and does not mean the project direction changed. Keep global memory as an index with namespace pointers, not as the project database. See `references/global-memory-index-project-namespace-first.md`.

21. Treating a workflow/process correction as chat-only.
   - Fix: if the correction changes how future agents should operate a specific project, update the project's repo governance/handoff and, when it affects long-term reasoning or review behavior, the project's Obsidian namespace too. Save only a compact global memory signpost if needed, and update skills only with the reusable class-level pattern. See `references/workflow-process-change-governance-routing.md`.

22. Treating a newly stable cybersec lab as permission to add more lanes or move public.
   - Fix: when infrastructure stabilizes but navigation is bloated, first create a compact repo-local current-navigation cleanup: default route, active targets, top 3 next vuln lanes, deprecated lanes, recovery/snapshot rules, artifact conventions, and Obsidian routing. Keep local proof-pattern gates explicit before public-target work. See `references/cybersec-lab-navigation-cleanup-routing.md`.

22a. Treating artifact cleanup as deletion-only or chat-only before hardening.
   - Fix: when a repo has many handoff/worker/evidence/schema/debug artifacts, first create or update a compact repo-local artifact index that classifies active substrate, references, superseded files, local-only/debug trash, operator-owned files, and unverified quarantine. Wire that index into current navigation/active queue and run focused validation before claiming readiness for the next engineering-hardening slice. See `references/artifact-index-before-hardening-routing.md`.

23. Treating external workers as if they inherit Hermes memory and full Obsidian context.
   - Fix: distinguish what the wrapper definitely embeds from what is merely readable on disk. Add explicit required context reads for current navigation, active strategy queue, project Obsidian note/index, and relevant handoff artifacts when a worker must preserve long-term goals. See `references/worker-context-boundary-routing.md`.

24. Treating scope authorization as permission for autonomous live-target contact.
   - Fix: split scope authorization from target-touching permission. For cybersec/bug-bounty work, write a repo-local pre-contact checkpoint, mark operator-only signup/auth/OTP/CAPTCHA/payment/policy gates explicitly, and ask the user for only non-sensitive status tokens before continuing. See `references/cybersec-live-target-precontact-gate-routing.md`.

## Verification After Applying This Skill

- [ ] The target project has a local memory/handoff policy or equivalent note.
- [ ] The project has an Obsidian namespace or an explicit reason not to use one.
- [ ] The global Hermes memory entry, if any, is short and declarative.
- [ ] Project-specific details stayed out of this skill and out of global memory.
- [ ] Any new durable note has status/source/date/repo-truth metadata.
- [ ] Any updated periodic review process checks memory and handoff drift.
