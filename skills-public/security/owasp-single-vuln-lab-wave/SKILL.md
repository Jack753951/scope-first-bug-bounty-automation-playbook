> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

---
name: owasp-single-vuln-lab-wave
description: Use when running one OWASP Top 10 vulnerability class at a time against an authorized disposable lab target and preserving the result as a reusable bounded module, importer, bridge, and handoff record.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [security, owasp, lab, bounded-adapter, destructive-lab]
    related_skills: [test-driven-development, systematic-debugging, first-bounty-bundle-sprint]
---

# OWASP Single-Vulnerability Lab Wave

## Overview

Use this workflow to test exactly one OWASP Top 10 vulnerability class at a time against an explicitly authorized lab/靶機, then retain the useful capability as a reusable module instead of a one-off command.

The default mode for unknown or public/client targets is bounded and candidate-only. For this project’s current learning stage, the operator has paused over-broad internal safety/tier/profile controls for the explicitly authorized disposable local靶機: do not block lab learning on missing heavy review/profile/contract artifacts, and do not categorically ban useful tools such as broad scanners, fuzzers, Burp/session workflows, TLS scanners, external tool wrappers, exploit-shaped scripts, or aggressive/destructive scripts when the work remains on the authorized learning lab. Keep external/legal red lines and candidate-only output semantics. Destructive means target-service disruption, data reset, or lab-state corruption inside the disposable VM/container only. It does not include malware, stealth persistence, credential theft, unauthorized public targets, or uncontrolled propagation.

Exploration breadth principle: do not shrink the authorized local-lab project to only the easiest or already-proven lanes. Try every useful proof possibility that can be tested with bounded scope, source/provenance, pre/post health, artifact capture, recovery/cleanup, and honest status labeling. Preserve useful attempts as `verified-impact`, `valuable-candidate`, `attempted-not-verified`, `blocked/deferred`, or `reference-only`; if a primary path is blocked/unsuitable, switch route via operator-run script, source-level proof, equivalent local target, adjacent safe-marker lane, mature OSS wrapper, or local target expansion rather than abandoning the class prematurely.

Phase 4B module-shaping convention: start from `script/tool -> bundle -> module`. A bundle is the operator-facing tactical workflow in `modules/bundles/` and is the default local-learning unit; a formal module is the platform-facing `modules/checks/**/module.json` capability used only after the bundle is stable or when runner/policy/report/authorized-assessment integration is needed. See `references/bundle-first-module-promotion.md`.

## When to Use

Use when:

- The operator asks to test OWASP Top 10 categories one-by-one on a local靶機.
- A single vulnerability class should become a repeatable module/bundle.
- A successful lab command must be promoted into adapter/importer/bridge documentation.
- The target is disposable and recovery can be verified before aggressive tests.

Do not use when:

- Target authorization is missing or ambiguous.
- The target is public/client/bug-bounty without current scope/rules approval.
- The target is an authorized live bug bounty/client service where local-lab scanner/exploit/destructive defaults would be unsafe; use `authorized-bug-bounty-assessment` instead for scope package, account handling, low-speed manual testing, evidence redaction, and report-readiness gates.
- Snapshot/container restore cannot be verified for destructive/aggressive lab waves that may damage state or availability.
- The requested behavior is stealth, persistence, malware, credential theft, real exfiltration, uncontrolled DoS/propagation, or bypassing legitimate controls outside the disposable lab.

## Bug-Bounty Applicability Target

These modules are intended to become reusable bug-bounty finding support modules, but lab success is not enough. A module becomes bug-bounty-ready only after it has:

- a one-vulnerability scope with explicit OWASP release mapping;
- program scope/rules checks and technique allow/deny gates;
- safe defaults for public/third-party targets: plan-only first, low rate, bounded requests, no destructive behavior, no credentials/brute force/callbacks unless the program explicitly allows them;
- evidence hygiene: redaction, no raw secrets/loot retention, reproducible commands, pre/post health where relevant;
- an offline importer and candidate-review bridge that emit `needs_manual_review`, not confirmed/reportable statuses;
- a manual verification path and report-readiness gate before anything is called a finding.

Therefore lab modules may produce bug-bounty **candidates/leads** after scope approval, but they must not directly auto-create confirmed findings or submissions. When moving from a lab bundle to a live bounty target, switch to `first-bounty-bundle-sprint` and use its Lab-to-Live Transfer Gate: preserve aggressive lab-derived thinking and proof primitives, then convert execution to program-allowed, scoped, low-noise steps. Scanner/fuzzer/callback/OAST/exploit-flow lanes should be retained when the live program explicitly permits them and bounded with caps/controls; when forbidden or ambiguous, use a surrogate proof or park the hypothesis instead of firing the lab version directly.

## Operator-Facing Bundle Layer

For this project, do not let the lab-wave process default to more governance, schemas, or review paperwork. Phase 4B should be bundle-first and script-first unless the operator explicitly asks to stabilize a platform contract or activate a real authorized target.

Treat lightweight bundles as the practical operator-facing module layer. Each bundle should answer:

1. when to use it;
2. which scripts/tools it runs;
3. required inputs;
4. output/artifact locations;
5. how to separate candidate signals from false positives, controls, and missing evidence.

Use the three-lane framing before choosing gates:

- `local-learning-lab`: disposable local靶機; scanners/fuzzers/aggressive/destructive tests may be used when recoverable; output remains candidate-only.
- `authorized-assessment`: real owned/client/bug-bounty target; strict scope/rules/rate/evidence gates; no destructive/bruteforce/callback/credential-sensitive behavior unless explicitly allowed.
- `offline-research`: CVE/advisory/parser/fixture/schema/report/knowledge-base work only; no target-touching behavior.

For Phase 4B learning work, prefer this promotion path: `scripts/SCRIPT_INVENTORY.md` -> `modules/bundles/<bundle>.md` -> local artifacts -> `possible_vulnerabilities` summary. Only promote to manifest/profile/schema/runner/importer/bridge when stabilizing a platform module or preparing for real authorized assessment.

Hermes' role in this class of work is secretary/intelligence/reviewer/synthesis support: organize handoffs, check scope/candidate language, summarize primary-source intelligence, and record lessons. Do not let Hermes expand architecture/process by default when a command-library page, bundle, or bounded adapter would solve the learning need.

See `references/phase4b-bundle-service-scanner-direction.md` for the session-derived bundle/service-scanner direction, including Apache, Tomcat, OpenSSL/TLS, HAProxy, Envoy, and Traefik baseline bundle candidates.

For service-baseline scanner implementation/runtime pitfalls, use `references/service-baseline-scanner-runtime-lessons.md`: quote generated service paths, execute the rendered runner (not only generator tests), suppress SPA/router fallback with root-body hashes, and avoid treating plaintext/OpenSSL no-certificate output as TLS candidates.

For API docs, metrics/observability, and JavaScript source-map exposure bundles, use `references/web-exposure-bundle-wave.md`: start with fixed GET-only local-lab probes, record mature OSS references, suppress SPA/router fallback with root-body hashes, keep raw bodies/secrets out of durable artifacts, and require manual verification before report/finding language.

For operator rest/sleep periods where Hermes should continue autonomously, use `references/rest-period-autonomous-lab-wave.md`: create a one-shot self-contained cron job, deliver back to the origin conversation, make maximum safe progress on remaining OWASP/CVE-usable local-lab waves, and avoid promising exhaustive CVE completion.

For operator requests to learn the full triggering process, use `references/verified-exploit-flow-bundles.md`: upgrade from metadata/candidate triage to a verified local-lab exploit-flow bundle only after reproducing the trigger, capturing evidence, and recording recovery/reset steps.

For target-touching verified-flow work, use `references/kali-verified-exploit-flow-route.md`: Windows/Hermes is the control plane, but scanners, browser/runtime checks, and exploit-flow attempts should default to `<lab-vm>`; do not call tools blocked just because they are missing from the Windows host.

For external intelligence intake and bundle retention rules, use `references/external-intel-and-valuable-bundle-retention.md`: CISA KEV, NVD, Exploit-DB, GitHub PoCs/tooling, HTB/training labs, OWASP, and CWE can seed lab bundles. Retain useful bundles as `verified-impact`, `valuable-candidate`, `attempted-not-verified`, `blocked/deferred`, or `reference-only`; full target control/file read/RCE is not required for retention when the workflow has reusable value.

For closeout-stage local labs and live-target-dependent candidates, use `references/ability-gap-and-live-target-routing.md`: stop adding similar lab waves once proof primitives are stable, add only explicit ability-gap proofs such as auth/session role separation, and route valuable candidates as `local_bootstrap_ready`, `local_simulation_possible_but_not_faithful`, `needs_authorized_live_target`, or `reference_only`. Local-first is not local-lab-only; if a lane needs a legal live target, ask the operator for scope/rules instead of filtering it out.

For Phase 5 vulnerability-intelligence intake, use `references/phase5-vuln-intel-intake.md`: create scope-package and report-readiness templates plus a one-shot metadata-only advisory refresh before any scheduler or target-touching automation. Classify candidates as local bootstrap review, high-impact local/live review, needs authorized live target, or reference-only, then pick at most one lane.

For the next step after vuln-intel candidate output, use `references/phase5-local-bootstrap-candidate-planning.md`: choose one `local_bootstrap_review` lane, write a bounded plan and target-catalog entry before any target launch, and add special socket/credential boundaries for Docker-management, CI/CD, secrets, cloud, identity, or other infrastructure-management products.

For intel-driven testing where the current靶機 cannot demonstrate a modern proof type, use `references/intel-driven-lab-target-expansion.md`: first extract useful bundles from the current authorized target, then add/modify a local vulnerable target when needed for IDOR/API, upload retrieval/execution-boundary, SSRF callback, XXE, or deserialization surfaces. New targets remain local/recoverable/scope-documented, and target-touching validation stays on `<lab-vm>`.

For acquiring modern exploit/tool sources and turning gaps into clean local proofs, use `references/script-acquisition-and-disposable-targets.md`: download selected Exploit-DB/GitHub/wordlist/tool material into git-ignored local acquisition dirs with provenance, treat raw PoCs as reference-only until reviewed, and add small disposable local targets when the current靶機 lacks the proof surface.

For source-driven parameter discovery and follow-on proof chains, use `references/source-driven-parameter-to-proof-chain.md`: preserve the CISA/NVD/Exploit-DB/GitHub/HTB source lineage, try mature tools safely from the attacker VM, but if dependency/setup state blocks execution in the isolated lab, port the safe core idea into a bounded local runner and then continue from one discovered surface into a single-vulnerability proof with baseline/positive/negative controls.

For Docker-backed vulnerable targets such as WebGoat/WebWolf, use `references/docker-backed-webgoat-lab-route.md`: keep Windows Hermes as control plane, `<lab-vm>` as tester, and `<lab-vm>` as Docker target host; verify NAT is closed from inside both VMs, do not trust stale VirtualBox guest-property NAT IPs, and treat WebGoat Access Control/IDOR, JWT/token, reflected XSS, and path traversal safe-marker lessons as required local-lab capability lanes with bounded evidence rules.

For continuation sessions after a pause/reboot/saved-state restore, use `references/lab-continuation-vm-route-safety.md`: remap actual VirtualBox VM names to attacker/victim roles, verify routes from inside the guest, close any revived NAT/default route before target-touching work, isolate project SSH from broken global SSH config with the project wrapper or empty `ssh -F` config, confirm the live service before picking the wave, and stop rather than retry if an exploit-shaped state-changing proof is denied by the safety layer/user.

For authenticated WebGoat lesson proof waves, use `references/webgoat-authenticated-lesson-proofs.md`: register short throwaway users, use lesson-compatible password rules, enumerate `/service/lessonmenu.mvc`, fetch direct lesson content URLs, preserve session/request artifacts, and promote verified lessons such as IDOR into bounded local-lab bundles.

For WebGoat JWT/token proof waves, use `references/webgoat-jwt-token-proofs.md`: avoid shell `USER` variable collisions by using `WG_USER`, fetch lesson HTML/JS and endpoint maps, start with the low-risk `/WebGoat/JWT/decode` assignment, keep signing/weak-key/refresh/JKU/KID lanes as candidate-only until individually verified, and close out with project-benefit plus new/changed sections.

For WebGoat/browser-runtime XSS proof waves, use `references/webgoat-browser-runtime-xss-safe-marker.md`: prove DOM/runtime marker execution in the correct origin/path/session context, preserve positive and control browser artifacts, use safe DOM marker payloads only, and if a WebGoat endpoint returns JSON, explicitly label any same-origin DOM-sink rendering as local proof-pattern calibration rather than public-target report evidence.

For WebGoat path traversal and Zip Slip proof waves, use `references/webgoat-path-traversal-zipslip-proofs.md`: derive payloads from WebGoat upstream source plus OSS references such as PayloadsAllTheThings/Snyk, prove bounded marker-only file write or throwaway profile-image overwrite, keep direct file-read variants attempted-not-verified unless actual marker content is read, and close with pre/post health plus recovery status.

For path traversal file-read continuation when the current training endpoint rejects traversal before marker content is read, use `references/path-traversal-file-read-local-target-expansion.md`: preserve the rejected attempt honestly, then add or use an equivalent source-controlled disposable local target with lab-owned public/control/marker files, public-file and missing-file controls, one bounded `../` positive read, cleanup, and a narrow `verified_file_read_safe_marker_lab_only` classification.

For one-vulnerability max-impact local-lab drills, use `references/max-impact-local-lab-proofs.md`: prefer verified command execution identity, lab-only marker file write/readback, isolated callback/control only when listener reachability is proven, and explicit recovery/cleanup evidence. Distinguish verified impact from attempted-but-blocked impact; do not claim callback/control without listener evidence.

For proof-library cleanup and one-vulnerability evidence-packet consolidation after several verified/candidate waves, use `references/proof-library-and-evidence-packet-closeout.md`: group proof patterns by evidence type, create/update a short handoff index, packetize one strong verified proof with report-readiness, then advance the active queue so completed packetization does not remain the top next lane.

For tactical agent-preview and post-evidence Claude Code review lenses, use `references/agent-preview-and-review-gates.md`: Hermes writes preview after OSS/source reconnaissance and before Kali bounded-script execution; Claude Code performs read-only project-value/evidence review after artifact pullback and before `verified-impact` / bundle / evidence-packet promotion. Keep both lightweight and tactical; do not turn them into a new safety process or governance-first approval gate.

For execution-layer safety blockers and adjacent safe-marker continuation, use `references/execution-layer-blockers-and-safe-marker-lanes.md`: if an authorized local-lab trigger is blocked with `BLOCKED` / `Do NOT retry`, do not disguise or retry the same trigger. Preserve the blocked/deferred artifact. Operator preference for repeated/similar blockers: default to creating a Kali-side operator-run script/run-card for the user to execute manually, following the successful SSRF operator pattern, rather than trying Hermes-side variants. The script should include precheck-only mode, exact local-lab scope, diagnostics, artifact path, cleanup/post-health, and a human confirmation gate before one sensitive trigger. Hermes can then review/pull back artifacts and label the result honestly. Other valid continuations remain source-level proof, equivalent local靶機/lane, or adjacent safe-marker proof such as XXE/path-traversal/deserialization bounded markers. See `references/operator-run-exploit-trigger-scripts.md`.

For post-wave navigation cleanup after several verified/candidate proof waves, use `references/proof-library-navigation-cleanup.md`: add a short proof-pattern index grouped by evidence class, update current navigation/active queue/inventory/accepted changes/Obsidian, and reprioritize next lanes away from already-completed proofs toward evidence packet consolidation, dedicated reruns, or second-surface safe-marker generalization.

For operator requests to continue testing and then explain current project capability, use `references/post-wave-capability-assessment.md`: after route/posture checks, proof execution, artifact pullback, and evidence review, summarize what the project can actually do now, what evidence supports it, and what remains only local-lab/reusable-methodology rather than public-target/report-ready.

## Verified exploit-flow mode

When the operator explicitly asks to understand how to trigger vulnerabilities on the authorized disposable lab, do not stop at scanner leads or metadata-only candidate notes. Treat candidate triage as the discovery phase, then attempt a scoped local-lab reproduction using whatever mature tools, payload replay, browser/session workflow, or aggressive/destructive lab-only scripts are needed and recoverable. The bundle is considered `verified-impact` only when it records: discovery path, exact trigger request/command/payload, observable success evidence, false-positive exclusions, lab impact, cleanup/recovery, post-health, and artifacts. If the trigger cannot be reproduced, do not discard the work by default: label it `valuable-candidate` when the workflow, tooling, precondition analysis, or false-positive handling is reusable; label it `attempted-not-verified`, `blocked/deferred`, or `reference-only` when appropriate. Do not imply verification without runtime/impact proof.

## Per-Wave Lifecycle

1. **Select one OWASP class**
   - State the release mapping: 2017, 2021, or 2025 migration track.
   - Pick exactly one class and one concrete lab endpoint/behavior.
   - Mark the risk lane: metadata, benign, active, aggressive, or destructive-lab.

2. **Authorization and recovery gate**
   - Confirm the target is local/private/scope-approved.
   - For aggressive/destructive waves, verify restore first:
     - VM snapshot exists or container reset command is known.
     - Pre-test health command works.
     - Recovery command has been dry-run or is known safe.
     - Post-restore health command works.
   - If recovery is not verified, downgrade to non-destructive bounded probing.

3. **OSS/tooling reconnaissance gate before writing new scripts or optimizing bundles**
   - Before creating a new adapter/custom script, or before materially improving a bundle, search for mature open-source projects, tools, templates, schemas, official docs, or training-lab upstream source that already cover the selected vulnerability behavior.
   - Compare: maintenance, license, safety defaults, target-touching behavior, output format, offline importability, fit for one-vuln max-impact proof, and whether the project can use `adopt`, `wrap`, `adapt`, `reference-only`, or `write-custom`.
   - Record the selected decision and references in the wave handoff/bundle before implementation. Treat `write-custom` as valid only after the OSS/tooling pass explains why the existing option is too broad, unsafe, unmaintained, hard to make deterministic, or poorly aligned with evidence-packet hygiene.
   - For SSRF/callback-style waves, also consult `references/ssrf-callback-local-lab-20260523.md` for the local host-only callback evidence pattern, Docker-published listener/target fallback, NAT-close verification, and blocked/deferred status discipline.
   - Compare at least: maintained status, license, safety defaults, target-touching behavior, output format, offline importability, and whether it can be wrapped safely for the local lab.
   - Decide and record one of: `adopt`, `wrap`, `adapt`, `reference-only`, or `write-custom`.
   - For the disposable local靶機, prefer using/wrapping mature tools when they improve coverage, including broad scanners, fuzzers, Burp/session workflows, TLS scanners, and tool-specific templates, as long as the run is scope-locked to the lab, impact-bounded where possible, recoverable, and candidate-only.
   - Write custom code only when OSS tools are unsafe for the lab gate, unmaintained, incompatible with artifact hygiene/candidate-only output, or less useful than a small fixed adapter for that wave.
   - If a useful tool or better local target surface is missing, the project convention is: Hermes may temporarily enable NAT/network access long enough to download/install/update the tool, pull a vulnerable image, or prepare a better recoverable local靶機 environment; record source/version/license/provenance, then disable NAT and return to host-only lab operation before target-touching execution unless a documented proof step explicitly requires a temporary install window.
   - Record the decision in the wave plan/handoff before implementation.

4. **Agent preview before runner/execution**
   - After OSS/source reconnaissance but before running a bounded script from Kali, do a short agent preview for tactical visibility and freedom.
   - Purpose: broaden attack-path thinking, compare mature tooling vs custom runner, identify missing controls/preconditions, and catch unsafe or low-value proof designs before execution. Preview must enumerate useful possibilities before prioritizing; it is not a narrowing filter and should not prematurely eliminate viable local-lab lanes.
   - Every preview must answer five tactical questions before execution:
     1. What is the maximum safe proof for this vulnerability behavior (callback, marker file write/readback, browser-runtime DOM marker, auth-boundary bypass, server-side identity, or controlled config/data exposure)?
     2. Can the current target prove that maximum safe proof? If not, do not force it; add/modify a recoverable local target or choose a better local lane.
     3. What is the minimum positive/control evidence required? Without a meaningful control, do not label the result `verified-impact`.
     4. If the primary trigger is blocked, what two alternate lanes still have learning value (operator-run exact trigger, source-level sink/gadget inventory, adjacent safe-marker lane, or equivalent disposable target)?
     5. Which proof-library capability does this wave add? If it only adds another log with no reusable evidence pattern, downgrade or choose a better lane.
   - Keep this lightweight for local-learning-lab: one focused preview is enough by default; use multiple reviewers only for high-risk/destructive/callback-heavy lanes or when the route is unclear.
   - Recommended reviewer roles:
     - `tactical preview`: likely proof path, payload/marker strategy, expected impact, false-positive controls, alternate local target if current靶機 is unsuitable.
     - `safety/evidence preview`: scope, recovery, request caps, artifact plan, no-secret/no-loot boundary, cleanup, report-readiness guard.
   - The preview must not authorize public targets or bypass safety blockers. It may recommend broader local-lab tools/scripts when recoverable and scope-locked.
   - Record the preview summary in the wave handoff or plan: route/tool, visible reviewer model/runtime when exposed, accepted/rejected suggestions, and final execution plan.

5. **RED tests first**
   - Add tests for plan-only default and explicit approval before writing runnable scripts.
   - Reject public targets fail-closed.
   - Enforce request caps/timeouts/rates/fixed paths.
   - Assert pre/post health and artifact manifest exist.
   - For destructive-lab waves, assert snapshot/restore metadata and recovery command are present in the plan.
   - Assert no output auto-promotes to confirmed/verified/reportable/accepted.
   - If using an OSS tool wrapper, test that unsafe defaults are disabled and outputs are normalized/redacted before import.

6. **Bounded adapter/runner**
   - Implement a runner under `scripts/lab_modules/`.
   - Default to plan JSON only.
   - Require explicit flags such as `--lab-approved` and, for destructive waves, `--destructive-lab-approved`.
   - Render a bash script only after approval; do not execute from the generator.
   - Record pre-health, run, post-health, summary, JSONL observations, artifact manifest.

7. **Safe lab execution**
   - Run target-touching scanners, browser/runtime checks, and exploit-flow attempts from the attacker/tool VM by default (for this project, `<lab-vm>`), not from the Windows Hermes control plane.
   - Before declaring a tool unavailable, verify it on Kali and verify the route actually reaches Kali.
   - Use fixed target, fixed path list, capped requests, short timeout, and bounded rate.
   - For destructive waves:
     - Capture pre-state.
     - Execute the destructive test.
     - If health fails or planned impact occurs, record it.
     - Run automatic recovery.
     - Verify restored health.
   - Pull back only safe artifacts; avoid raw bodies, secrets, dumps, and loot.

8. **Agent review before verified-impact/bundle promotion**
   - After execution and artifact pullback, but before labeling anything `verified-impact` or writing/promoting the bundle/evidence packet, run an agent review.
   - Purpose: challenge the proof claim, separate candidate/control/noise from impact evidence, identify missing artifacts, and decide whether the result is `verified-impact`, `valuable-candidate`, `attempted-not-verified`, `blocked/deferred`, or `reference-only`.
   - Default reviewer roles:
     - `evidence reviewer`: checks pre/post health, positive/control artifacts, marker provenance, source IP/session/origin labels, false-positive exclusions, and whether the claimed impact is exactly supported.
     - `tactical reviewer`: checks whether a stronger safe proof is reachable in the local lab, whether another tool/target surface would improve learning, and whether to continue, stop, or packetize.
   - For nontrivial/destructive/callback waves, prefer at least two reviewers or one reviewer plus Hermes synthesis. Record reviewer route/tool, visible model/runtime when exposed, summary, dissent, final Hermes decision, and any missing evidence.
   - Agent review is advisory, not an automatic finding gate. It must not promote public-target findings, bypass explicit safety denials, or demand governance-first work when a simple bundle/packet is enough.

9. **Offline importer**
   - Normalize observations into a versioned envelope.
   - No network/subprocess execution.
   - Convert only reviewed low-risk signals into `needs_manual_review` candidate seeds.
   - Do not emit confirmed/verified/reportable/accepted statuses.

10. **Candidate-review bridge and possible-vulnerability report**
   - Convert seeds into candidate review fixtures only.
   - Evidence remains empty unless separate manual/redacted evidence exists.
   - Report readiness stays `not_ready`.
   - Each lab run should also emit a short human-readable `possible vulnerabilities` summary with three sections:
     - `possible_manual_review_candidates`: signals worth reviewing next;
     - `non_findings_or_controls`: controls, false-positive suppressions, and metadata-only observations;
     - `missing_evidence_to_confirm`: exact evidence still needed before calling it a finding.
   - Use candidate language only: possible, candidate, lead, needs manual review. Do not use confirmed/verified/reportable unless the manual verification/report-readiness gate has passed.

11. **Proof-library and evidence-packet closeout when navigation grows**
   - After several verified/candidate waves, pause new target-touching work if navigation is becoming harder than execution.
   - Build or update a compact proof-library index grouped by evidence type, with bundle/handoff/artifact pointers and minimum evidence shapes.
   - Convert one strong verified proof into a one-vulnerability evidence packet with report-readiness, using `templates/one_vuln_evidence_packet_template.md` when available.
   - Update current navigation, active queue, inventory, accepted changes, and Obsidian so completed packetization is visible and the next lane advances.
   - See `references/proof-library-and-evidence-packet-closeout.md`.

12. **Modularize and record**
   - Add/update `modules/bundles/<bundle>.md`.
   - Update `scripts/SCRIPT_INVENTORY.md`.
   - Add a dated handoff result.
   - Append `handoff/accepted_changes.md`.
   - Update active navigation/Obsidian project index when relevant.
   - Record validation commands, route/tool, runtime/model when visible, artifact paths, and safety boundary.
   - After multiple verified/candidate waves or any stale next-lane status, add/update a proof-library index grouped by evidence pattern rather than chronology. See `references/proof-library-navigation-cleanup.md`.

13. **Lab/test wave closeout for this user**
   - Every completed test wave summary should include an explicit `對專案有什麼幫助` section: describe project benefit, capability/library growth, evidence quality improvement, automation/readiness impact, and false-positive/precondition learning.
   - Every completed test wave summary should include an explicit `新增/更新了什麼` section: list changed scripts, bundles, handoffs, Obsidian notes, artifacts, blockers, and reusable workflow updates.
   - Keep the existing route/tool, visible runtime/model, usage artifact path when available, artifact paths, boundaries, blockers, validation, and next-lane summary alongside these two sections.

## Release Matrix Discipline

For 2017, 2021, and 2025 migration tracks:

- Keep a matrix of OWASP release/category -> lab module/bundle -> adapter -> importer -> bridge -> test artifacts.
- Do not claim official 2025 category names unless verified from a primary OWASP source. If not verified, label it `2025 migration track`.
- One vulnerability class gets one module/bundle. Do not create omnibus bundles that actively test multiple unrelated OWASP classes in one runnable path.
- Cross-release equivalence is the exception: one module may cover the same capability mapped across 2017/2021/2025, but the module's primary scope must remain a single vulnerability behavior/capability and the mapping must be explicit.

## Destructive-Lab Rules

Allowed only inside an intentionally vulnerable/disposable local lab after recovery is verified:

- service crash/restart calibration;
- lab database reset or known challenge-state corruption;
- intentionally bad payloads that break only the lab target;
- controlled resource impact with strict caps;
- one-vulnerability max-impact proofs that demonstrate server-side execution identity, lab-only file write/readback, or isolated callback/control evidence, provided the payload is scope-locked, non-persistent by default, recoverable, and does not touch host/real data outside the disposable lab.

For max-impact local-lab work, do not stop at weak metadata when a verified impact proof is reasonably reachable. Aim for the largest safe proof from one vulnerability (for example command execution as the web user plus `/tmp` marker write/readback), then clearly label any attempted-but-blocked steps such as outbound callback. See `references/max-impact-local-lab-proofs.md`.

Still not allowed:

- public/third-party targets;
- malware, persistence, stealth, evasion, credential theft;
- real exfiltration or retention of secrets/PII/tokens;
- uncontrolled DoS or propagation;
- destructive actions outside the lab VM/container;
- automatic report submission or confirmed finding promotion.

## References

- `references/bundle-first-module-promotion.md` — operator-accepted distinction between scripts/tools, lightweight bundles, and formal modules; includes lane split, Hermes role boundary, and service-scanner bundle direction.
- `references/2026-05-21-lab-recovery-and-tracker.md` — dated project snapshot for the first OWASP single-vulnerability modularization setup: operator workflow correction, VirtualBox lab recovery commands, tracker/runbook paths, active bundles, and the capability-specific coverage pitfall.
- `references/mature-tool-wrapper-wave.md` — session-tested pattern for wrapping mature scanners/fuzzers/tooling (ffuf/Nikto/nmap class) in authorized recoverable local labs without category-banning them, including TDD shape, parser/suppression lessons, health/recovery handling, and verification checklist.
- `references/local-tool-acquisition-review-hygiene.md` — local acquisition pattern for mature tools/wordlists/templates: keep full downloads/runtime outputs git-ignored, commit manifests/bundles/result notes only, and exclude vendor/runtime dirs from project-owned static review gates.
- `references/service-baseline-scanner-runtime-lessons.md` — class-level runtime lessons for service baseline scanner bundles: generated bash quoting, rendered-runner execution, root-body fallback suppression, OpenSSL plaintext controls, candidate/control wording, and minimal artifacts.
- `references/web-exposure-bundle-wave.md` — pattern for API docs, metrics/observability, and source-map exposure bundles: fixed GET-only probes, mature OSS references, root-fallback false-positive suppression, artifact hygiene, and manual verification gates.
- `references/rest-period-autonomous-lab-wave.md` — pattern for operator rest/sleep requests: schedule a one-shot autonomous local-lab wave with self-contained scope/safety/candidate-only instructions, origin delivery, validation, and concise Traditional Chinese closeout.
- `references/phase4b-bundle-service-scanner-direction.md` — operator correction to keep Phase 4B bundle/script-first, use governance as guardrails, preserve three execution lanes, and seed Apache/Tomcat/OpenSSL/HAProxy/Envoy/Traefik baseline bundle backlog.
- `references/kali-verified-exploit-flow-route.md` — route correction for verified exploit-flow work: default target-touching tools to `<lab-vm>`, pull artifacts back to repo, and avoid treating Windows-host missing tools as blockers.
- `references/intel-driven-lab-target-expansion.md` — session-derived rule for intel-driven lab waves: retain valuable bundles without max impact, and add/modify local vulnerable targets when Juice Shop/current靶機 lacks proof surfaces such as IDOR, upload retrieval/execution, SSRF callback, XXE, or deserialization.
- `references/script-acquisition-and-disposable-targets.md` — acquire Exploit-DB/GitHub/tooling sources with provenance, keep raw PoCs reference-only until reviewed, and add small disposable local targets for clean IDOR/upload/SSRF/XXE/deserialization/XSS proofs when existing labs lack the surface.
- `references/source-driven-parameter-to-proof-chain.md` — source-driven parameter discovery and proof-chain pattern: preserve vulnerability-library lineage, safely try mature tools, port the core idea into a bounded local runner if setup/dependency state blocks execution, then continue into one-vulnerability proof with baseline/positive/negative controls.
- `references/webgoat-authenticated-lesson-proofs.md` — authenticated WebGoat/WebWolf lesson wave pattern: throwaway registration/session handling, lesson menu enumeration, direct lesson content paths, verified IDOR proof recipe, evidence conventions, and next-lane ordering for JWT/XSS/path traversal.
- `references/webgoat-jwt-token-proofs.md` — WebGoat JWT/token proof pattern: authenticated lesson fetch, endpoint/JS extraction, offline token decode artifacts, `/JWT/decode` verified proof shape, JWT next-lane candidates, `WG_USER` variable pitfall, and required project-benefit/new-changes closeout sections.
- `references/webgoat-browser-runtime-xss-safe-marker.md` — WebGoat/browser-runtime XSS proof pattern: safe DOM marker, origin/path/session labeling, positive/control browser artifacts, CDP helper workaround shape, and wording for JSON-output DOM-sink limitations.
- `references/webgoat-path-traversal-zipslip-proofs.md` — WebGoat path traversal/Zip Slip proof pattern: source-first OSS reference capture, bounded upload-file-write, archive-entry profile overwrite, attempted-not-verified direct-read handling, destructive-lab boundaries, and bundle improvement fields.
- `references/path-traversal-file-read-local-target-expansion.md` — continuation pattern when a direct-read training endpoint rejects traversal: preserve attempted-not-verified evidence, then use a source-controlled disposable target with lab-owned marker files, public/missing controls, bounded positive read, cleanup, review, and narrow lab-only classification.
- `references/max-impact-local-lab-proofs.md` — one-vulnerability max-impact local-lab pattern: command execution identity, lab marker file write/readback, callback/control verification requirements, Docker-published port route lesson, and DVWA command-injection evidence shape.
- `references/agent-preview-and-review-gates.md` — lightweight tactical agent preview/review gates: preview before Kali bounded-script execution; review before verified-impact/bundle/evidence-packet promotion.
- `references/proof-library-and-evidence-packet-closeout.md` — closeout pattern after several verified/candidate local-lab waves: build a proof-library index, group patterns by evidence type, packetize a strong proof, and advance active navigation.
- `references/execution-layer-blockers-and-safe-marker-lanes.md` — handling for authorized local-lab exploit triggers blocked by the execution layer: do not bypass/encode/retry; preserve blocked/deferred artifacts; continue via operator-run run-card, source-level proof, equivalent local target, or adjacent safe-marker lane such as XXE/path traversal/deserialization.
- `references/phase5-vuln-intel-intake.md` — Phase 5A metadata-only vulnerability-intelligence intake: scope package, report-readiness checklist, one-shot advisory refresh, candidate routing labels, and scheduler/live-target boundaries.
- `references/phase5-local-bootstrap-candidate-planning.md` — after vuln-intel intake, select one local-bootstrap candidate, write a plan/catalog entry before launching a target, and add explicit Docker socket/credential boundaries for infrastructure-management apps.
- `references/proof-library-navigation-cleanup.md` — post-wave navigation cleanup pattern: build a short proof-library index grouped by evidence class, update current navigation/active queue/inventory/accepted changes/Obsidian, and reprioritize next lanes after verified proofs.

## Tool acquisition hygiene

When the wave uses mature external tools, payload lists, templates, or wordlists, keep full downloads and raw runtime outputs under git-ignored local paths (for example `setting/local/...` and `kali-output/...`). Commit only project-owned acquisition manifests, wrapper/bundle docs, and candidate-only result summaries. If a local review wrapper recursively compiles/lints the repository, exclude those vendor/runtime acquisition dirs so third-party payload archives do not break project-owned gates. See `references/local-tool-acquisition-review-hygiene.md`.

## Common Pitfalls

1. **Assuming broad tools are banned on the disposable lab.** They are allowed when the operator has authorized the lab wave, recovery is verified, execution is scope-locked, and artifacts remain candidate-only. Public/third-party targets still default to strict bounded/scope-rule gates. When wrapping tools, preserve suppression metadata (for example ffuf SPA/default fallback suppression, service-baseline root-body fallback suppression, OpenSSL plaintext/no-certificate controls, exposure-bundle root-fallback controls, and Nikto informational-line filtering) so future review sees both candidates and why non-candidates were ignored.
2. **Filtering out valuable lanes only because they need live targets.** Local lab proof is the default first route, not a hard capability filter. If a candidate is valuable but cannot be faithfully reproduced locally, keep it as `needs_authorized_live_target` and ask the operator for the legal target/scope/rules package before any target-touching work. Do not drop the class silently, and do not let Hermes self-authorize live testing.
3. **Starting Phase 5 vulnerability intelligence with a scheduler or auto-bootstrap.** First run a one-shot metadata-only advisory refresh and inspect the output. The first Phase 5A deliverables are a legal scope package template, report-readiness checklist, candidate routing output, and current-navigation update. Only add weekly/cron automation after the one-shot output is compact and useful.
4. **Continuing to add similar lab waves after proof primitives are stable.** In closeout posture, only add new vulnerability tests that fill explicit ability gaps, such as auth/session role separation for role/account matrix evidence. Move recurring latest-vulnerability refresh/candidate intake to the next phase rather than expanding the local proof phase indefinitely.
5. **Treating service-path or exposure-path HTTP 200 as proof.** Apache/Tomcat/HAProxy/Envoy/Traefik default/status paths, API docs paths, metrics paths, and inferred `.js.map` paths can all return 200 on SPA/router fallbacks. Compare response-body hashes against the target root and downgrade identical catch-all responses to controls unless there is service- or exposure-specific header/body/location evidence.
5. **Over-mapping exposure leads to CVEs.** API docs, metrics, and source maps are usually A05/information-exposure leads; record CVE tooling such as Retire.js only as a later dependency/version hint unless a specific affected component/version is manually verified.
6. **Delivering only candidate metadata when the operator requested trigger mastery.** In local-learning-lab mode, if the operator asks for the complete vulnerability flow, continue from discovery into scoped reproduction: use the necessary lab-safe tools/payloads/session workflow, capture proof of trigger, recover/reset, and then write a `verified-impact` lab bundle when impact proof exists. If no trigger is found, still consider retaining a `valuable-candidate` bundle when the workflow is useful for modern security practice, false-positive handling, exploit precondition mapping, or later attack-chain work; otherwise mark `attempted-not-verified`, `blocked/deferred`, or `reference-only`.
5. **Skipping recovery validation.** Destructive/aggressive lab approval requires restore verification before the run.
6. **Keeping only local helper scripts.** A retained wave needs tests, adapter, bundle docs, handoff, and accepted changes.
7. **Mislabeling OWASP 2025.** Use `2025 migration track` unless official source verification is recorded.
9. **Misrouting target-touching lab work through Windows.** Windows/Hermes is the control plane; Kali is the default tool/attacker plane. If a worker inherits the Windows workdir and says `ffuf`, `nikto`, `nmap`, `sqlmap`, Chromium, or similar tools are unavailable, reroute through Kali before recording a blocker.
10. **Overlooking external intelligence as bundle intake.** CISA KEV, NVD, Exploit-DB/searchsploit, GitHub PoCs/tooling, HTB/training-lab patterns, OWASP, and CWE should feed the lab queue. Extract patterns and preconditions; do not blindly execute PoCs or claim product-specific CVEs unless the target component/version matches and behavior is reproduced.
11. **Letting tool setup state stop a source-driven lane.** If a GitHub/Exploit-DB/tool-source lane points to a useful technique but the isolated attacker VM lacks a dependency, record the setup debt and either open a deliberate temporary-NAT install window or port the safe core idea into a bounded local runner. Continue only with scoped inputs, low rate, controls, artifacts, and post-health; do not encode the transient setup state as a durable tool limitation.
12. **Overtrusting noisy parameter-probe indicators.** Status/length/hash deltas and SQL/error keywords are leads, not proof. Follow promising parameters with a one-vulnerability proof using baseline, normal, positive, and negative controls; watch for product text that naturally contains strings such as `SELECT` or `WHERE`.
13. **Re-probing an unsuitable靶機 instead of adding a local target.** If the current lab cannot cleanly prove IDOR, upload retrieval/execution-boundary, SSRF callback, XXE, deserialization, or another modern pattern, add or modify a local intentionally vulnerable target with documented scope, reset, and health checks. The operator permits temporary NAT/downloads and local VM/container/source changes for better recoverable靶機 coverage when source/provenance, close/verify, and recovery/post-health are recorded. Do not force unrelated CVEs onto Juice Shop just to keep using the same victim.
12. **Putting Docker on the wrong VM or testing localhost on the victim.** In the two-VM lab, the Docker target host may be `<lab-vm>` while `<lab-vm>` remains the tester. Do not treat Docker absence on the attacker VM as a blocker if victim already hosts containers. Verify services from attacker to victim host-only IP; Docker port bindings may not answer on victim `127.0.0.1`.
13. **Skipping continuation-state audit after VM resume.** Before continuing a prior lab wave, re-resolve VM names, verify attacker/victim IPs, inspect guest routes from inside the attacker, close any revived NAT/default route, confirm target services from attacker to victim, and use project-scoped SSH config/wrappers instead of global user SSH config. If a state-changing exploit proof is denied, do not retry around the denial; close out the completed low-risk work and request explicit approval for the next bounded lab proof.
13. **Avoiding high-risk classes entirely in the local learning lab.** The operator wants capability growth for Access Control/IDOR, JWT/token, reflected XSS, and path traversal safe-marker lessons. Keep them local, bounded, recoverable, and evidence-focused; do not skip them merely because they would be high-risk on public targets.
14. **Misreading WebGoat lesson routes.** Lesson-menu links are hash/client routes like `#lesson/IDOR.lesson`; direct lesson content is fetched as `/WebGoat/IDOR.lesson`. Do not probe `/WebGoat/lesson/IDOR.lesson` and conclude the lesson is missing from a 404.
15. **Treating WebGoat registration failure as target failure too early.** Auto-generated long usernames or special-character passwords can trigger registration form validation. Retry with short throwaway usernames and a simple lab password such as `webgoat`, then verify login/session cookies before moving on.
16. **Letting transient browser-driver setup block all WebGoat progress.** Browser runtime evidence is needed for XSS, but IDOR/JWT/path traversal HTTP/session proofs can proceed. Record the browser blocker as a setup issue, do not encode it as a durable tool limitation. For XSS itself, consider a narrow CDP helper that captures DOM marker/origin/path/control artifacts before giving up on runtime proof.
17. **Overstating max-impact or callback/control evidence.** For local靶機 max-impact work, command execution identity and marker-file write/readback can be verified independently from callback/control. If a callback listener is unreachable, record it as a blocker and keep the verified-impact claim limited to what the artifacts prove. Add short timeouts to callback attempts so egress blockers do not destroy the primary evidence.
18. **Assuming a listening victim host port is reachable across VMs.** In this lab, host processes on arbitrary victim ports may be blocked while Docker-published services are reachable. Verify attacker-to-victim reachability before a wave, and prefer Docker-published listener/target ports for cross-VM target or callback infrastructure.
19. **Calling reflected text a browser-runtime XSS proof.** For XSS waves, require runtime evidence in the browser context: DOM attribute/console marker, origin/path/session label, saved DOM/screenshot, and a negative control that does not set the marker. If the endpoint returns JSON and the helper renders an `output` field into a same-origin DOM sink, state that limitation explicitly and keep report-readiness at local-learning/reusable-methodology.
20. **Treating lesson completion as equivalent to impact proof.** Some training labs allow lesson completion through alternate answers or hash submission. For path traversal/file-read lanes, require actual marker read/write/overwrite evidence before `verified-impact`; otherwise label the runner `attempted-not-verified` even if the lesson says completed.
21. **Forcing an unsuitable direct-read endpoint instead of target expansion.** If a training endpoint rejects raw/encoded traversal before returning marker content, keep that as valuable control evidence and switch routes: source-level route review, equivalent disposable local target, or adjacent safe-marker lane. A clean local target expansion should use lab-owned public/control/marker files, not `/etc/passwd` or secrets, and should classify narrowly as `verified_file_read_safe_marker_lab_only` only after public control, missing-file control, positive marker content, post-health, cleanup, and review.
22. **Letting an execution-layer blocker stop the lab program or tempt bypass.** If a local authorized exploit trigger is denied with `BLOCKED` / `Do NOT retry`, do not encode, split, hide, or retry the same trigger via another client. Record the attempted step as `blocked/deferred`, preserve useful route/setup artifacts, and continue with an operator-run run-card, source-level proof, equivalent local靶機, or adjacent safe-marker lane. Setup success is not impact proof; label the claim to match the artifact.

## References

- `references/owasp-three-class-trial-20260521.md` — concrete pilot example for three OWASP classes, including OSS/tooling recon decisions, generated-runner testing pitfall, SPA fallback false-positive handling, and candidate bridge guidance.
- `references/2026-05-21-single-vuln-split-run.md` — corrective split pattern for turning a multi-class pilot into three one-vulnerability modules, including `possible_vulnerabilities.md`, MSYS remote-path handling, and generated heredoc pitfalls.

## Verification Checklist

- [ ] OSS/tooling reconnaissance completed before writing new scripts; adopt/wrap/adapt/reference-only/write-custom decision recorded.
- [ ] Agent preview completed after OSS/source reconnaissance and before Kali bounded-script execution; preview summary, accepted/rejected suggestions, route/tool, and reviewer identity/model labels recorded.
- [ ] Generated runnable scripts are tested directly (`bash -n` plus at least one lab execution or dry-run path); do not rely only on generator tests.
- [ ] On Windows/Git-Bash/MSYS when generating remote Linux paths, use `MSYS2_ARG_CONV_EXCL='*'` or equivalent path-conversion guard so `/home/kali/...` stays a Linux path.
- [ ] Generated bash with nested Python/heredocs preserves newline escaping; prefer raw string templates or explicit escaping, then verify the rendered runner itself.
- [ ] False-positive controls are explicit: SPA/root-body fallbacks, auth gates, metadata-only observations, plaintext/TLS-unavailable controls, and status-code-only signals are not promoted as findings.
- [ ] One OWASP class selected and release mapping recorded.
- [ ] Target is local/private/scope-approved.
- [ ] Recovery verified before destructive run, or wave downgraded.
- [ ] RED tests added before implementation.
- [ ] Adapter is plan-only by default and approval-gated.
- [ ] Public target rejection tested.
- [ ] Request caps/timeouts/rates/fixed paths tested.
- [ ] Pre/post health and artifact manifest generated.
- [ ] JSONL observations are candidate-only.
- [ ] Browser-runtime XSS evidence, when applicable, includes DOM/console marker, origin/path/session context, positive/control artifacts, and explicit limitation wording for any artificial DOM sink used for local calibration.
- [ ] Importer/bridge added or explicitly deferred.
- [ ] Agent review completed after artifact pullback and before `verified-impact` / bundle / evidence-packet promotion; review challenges proof claim, labels missing evidence, and records Hermes final decision.
- [ ] Bundle docs, script inventory, handoff, accepted changes updated.
- [ ] If an execution-layer safety blocker occurred, no bypass/retry was attempted; the step is labeled `blocked/deferred`, useful artifacts are preserved, and an operator-run/source-level/equivalent-target/adjacent-lane continuation is recorded.
- [ ] Focused tests and local review pass.
