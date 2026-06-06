> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Security external-tool adapter rungs

Use this pattern when a cybersecurity lab session uses a valuable third-party recon/scanner script or tool and the user wants the project capability to grow over time rather than remain a one-off command.

## Trigger

Apply when any of these happen:

- A mature external tool such as httpx, katana, nuclei, ffuf, ZAP, dalfox, Nikto, or a custom triage script produces useful lab output.
- A one-off shell helper was needed to run a bounded local-lab check.
- The user asks whether the project retained the new capability, or emphasizes modularization / extensibility.
- A tool output format should feed candidate/evidence/report workflows.

## Principle

A useful script should become a tested adapter/runner module, not just a handoff note.

Separate the two halves:

1. Execution runner: prepares bounded, scope-gated, health-checked local-lab commands or scripts.
2. Offline importer: converts reviewed tool output into normalized observations/candidates without trusting tool output as a finding.

## RED tests first

Before implementation, add focused tests for:

- Plan-only by default; executable script generation requires an explicit approval flag such as `--execute-lab-approved`.
- Public targets and unknown tools are rejected fail-closed.
- Rate/depth/timeout limits are bounded.
- Pre-health and post-health steps are present for target-touching runners.
- Raw response bodies, callbacks/OAST, loot/dump/os-shell/persistence, and report submission are absent.
- Offline importer does not perform network I/O or subprocess execution.
- Malformed JSONL/output fails closed without partial unsafe observations.
- Imported observations never emit `confirmed`, `verified`, `reportable`, or `accepted` status values.

## Minimal module shape

Recommended project files:

```text
scripts/run_<tool_or_family>_lab.py          # bounded local-lab plan/script generator
scripts/import_<tool_or_family>_observations.py
scripts/test_<tool_or_family>_lab_runner.py
scripts/test_<tool_or_family>_observation_importer.py
tests/fixtures/external_tools/<tool>_sample.jsonl
handoff/<slice>_oss_recon_<date>.md
handoff/<slice>_result_<date>.md
```

Prefer family-level modules when tools share a contract, e.g. one `run_external_tool_lab.py` for bounded httpx/katana planning and one `import_external_tool_observations.py` for their JSONL outputs.

## Adapter-output importer rung

When a bounded lab adapter already writes safe JSONL observations, add a separate offline importer before candidate/review/report workflows consume it:

1. RED test for the missing importer CLI first, using a committed fixture under a family-specific directory such as `tests/fixtures/<adapter_family>/observations_sample.jsonl`.
2. Restrict accepted input paths to the adapter family's fixture/handoff contract, not arbitrary scan directories or unrelated external-tool fixtures. Reject unexpected paths fail-closed.
3. Normalize adapter records into a versioned envelope such as `schema_version`, `summary`, `observations`, `candidate_seeds`, and `safety`.
4. Preserve provenance fields needed for review (`run_id`, `source_module`, `observed_at`, normalized URL/path/status/content-type/source fixture), but do not retain raw bodies.
5. Convert only low-risk lead patterns into manual-review seeds. Examples: `/ftp/` directory listing candidate or `/api-docs/` Swagger/API-docs candidate. Every seed must stay `needs_manual_review` and must never become confirmed evidence.
6. Add negative tests for malformed JSONL, wrong schema/version, unrelated fixture directories, subprocess/network usage, and status vocabulary containing `confirmed`, `verified`, `reportable`, or `accepted`.
7. Smoke-run the importer after GREEN and assert candidate counts plus absence of promotional status values in the rendered JSON output.

Recommended shape for a manifest/runtime adapter follow-up:

```text
scripts/import_<adapter_family>_observations.py
scripts/test_<adapter_family>_observation_importer.py
tests/fixtures/<adapter_family>/observations_sample.jsonl
tests/fixtures/<adapter_family>/malformed_observations.jsonl
```

The importer is a bridge to candidate-review packets, not a verification engine. The next rung should consume `candidate_seeds[]` into a review fixture/input while preserving `manual review only`, `not confirmed`, and `not reportable` semantics.

## Candidate-review bridge rung

When an adapter/importer family emits useful `candidate_seeds[]`, promote the wave into the existing offline candidate-review vocabulary before adding broader scanning or more aggressive modules. This is the reusable pattern for "each wave should leave behind valuable project modules," not just a one-off lab note.

1. RED test a missing bridge CLI/module first. The test should start from the adapter family's committed fixture (for example `tests/fixtures/<adapter_family>/observations_sample.jsonl`) and assert the bridge emits a versioned envelope plus an in-memory candidate-review packet.
2. Keep the bridge offline and non-writing by default: JSON stdout only, no target interaction, no network I/O, no subprocess execution, no report drafting/submission, and no default output-file writes.
3. Reject live-target flags such as `--target`, `--url`, `--host`, `--scope`, and `--live` with structured JSON and non-zero exit before parsing normal arguments.
4. Convert only `needs_manual_review` seeds into `finding/1.0` fixtures with `status: candidate`, empty `evidence`, `triage.scanner_output_only: true`, and `triage.manual_verification_required: true`.
5. Validate generated finding fixtures with the existing finding validator before packet projection; fail closed with no partial packet if generated fixtures do not validate.
6. Project fixtures through the existing candidate-review packet builder vocabulary in memory when possible instead of creating a competing packet schema. Preserve `candidate_review_packet/0.1-trial` semantics until a separate schema-promotion review authorizes changes.
7. Assert the bridge output contains no `confirmed`, `verified`, `reportable`, or `accepted` status values anywhere, and that packet `report_readiness` remains `not_ready` unless separate human evidence/review has been added.
8. Smoke-run the bridge after GREEN and record candidate seed count, fixture count, packet finding count, status vocabulary, validation commands, and safety boundary in the project handoff/accepted changes.

Recommended shape:

```text
scripts/build_<adapter_family>_candidate_review_fixture.py
scripts/test_<adapter_family>_candidate_review_bridge.py
```

Pitfall: do not feed scanner observations directly into the candidate packet builder as evidence. The bridge may create review fixtures, but it must not turn scanner output into proof. Evidence stays empty or references only separately redacted/manual captures authorized by a later review gate.

## Wave-by-wave retained-capability checklist

For every future lab wave, preserve the useful capability in this order before moving to the next wave:

1. **Wave direction / risk tier** — state the goal, technique class, target boundary, review tier, and whether target-touching execution is allowed. If target-touching or aggressive, require a run card and explicit operator approval.
2. **Module/manifests or adapter plan** — capture the wave as reusable module manifests or a bounded adapter plan rather than a one-off command.
3. **Bounded lab adapter/runner** — keep execution plan-only by default; require explicit lab approval for scripts; reject public/live targets; enforce request caps, timeouts, rate limits, fixed paths/origins, pre/post health, and JSONL output.
4. **Offline importer** — normalize only reviewed fixture/handoff output into observations and `candidate_seeds[]`; no network, subprocess, raw bodies, target touching, or finding/report promotion.
5. **Candidate-review bridge** — convert only manual-review seeds into `finding/1.0` candidate fixtures and existing candidate-review packet vocabulary; keep evidence empty unless separately redacted/manual evidence exists.
6. **Offline review chain** — run gap report, verification plan, and report-readiness gate before considering manual verification/report drafting.
7. **Documentation / accepted changes** — record route/tool, visible model/runtime when relevant, validation commands, safety boundary, output counts, and non-promotional vocabulary.

A wave is not "retained" until adapter/runner, importer, bridge or explicit bridge-deferral rationale, tests, fixtures, README entry, accepted-change entry, and validation evidence exist. Skipping this step turns valuable lab learning back into disposable scan output.

## Safe execution rung

Only after offline importer tests pass:

1. Confirm target is local lab / authorized scope.
2. Capture tool version and exact command.
3. Use low bounded settings first, e.g. metadata-only httpx, katana depth 1, small rate limit, short timeout.
4. Disable raw bodies and external callbacks.
5. Run from the red-team/tooling VM, not from the victim service plane.
6. Record pre/post health and artifact manifest.
7. Copy only safe/redacted artifacts into repo fixtures or handoff.
8. Import into normalized observations and keep outputs non-promotional.

### Local-lab fast lane

When the user explicitly says the target is an intentionally vulnerable lab/靶機 and asks to reduce over-heavy safety review, do not add another broad policy-design detour. Use a minimal gate and act:

1. Verify the target is local/private or already whitelisted; reject public/real bug-bounty targets.
2. Pick one low-risk bounded wave, not a broad scan. Prefer fixed GET-only known paths, filename/header/status metadata, or inert parameter canaries.
3. Keep the run card small: fixed target, fixed path list, request cap, timeout/rate, pre/post health, JSONL observations, artifact manifest.
4. Still hard-stop on brute force, OAST/callbacks, credentialed flows without lab-only test accounts, destructive actions, loot retention, recursive download, exploit chains, and report/finding promotion.
5. After execution, immediately modularize the useful script combination or document the explicit importer/bridge deferral. Do not leave a successful lab command as only a local helper.

This fast lane changes review depth, not safety semantics: outputs remain candidate/observation-only until later manual verification and review gates.

## Manifest-to-runtime adapter rung

When a lab flow has already been captured as module manifests, do not stop at `module.json` catalog entries. Add a narrow runtime adapter rung that keeps planning separate from execution:

1. RED test first for the missing adapter path/API, expected module IDs, pre/post health steps, output shape, public-target rejection, unsafe limit rejection, and explicit approval before writing executable scripts.
2. Implement a plan-only default CLI that emits JSON and maps each planned step back to the class-level module IDs.
3. Require an explicit flag such as `--lab-approved` before writing a bash script or any executable artifact; script generation still must not run the target-touching commands itself.
4. Keep the first runtime adapter bounded to fixed known paths/origins, request caps, timeouts, rate limits, and JSONL observation output.
5. Render pre/post health and an artifact manifest into the script; validate the generated script with `bash -n` before considering the adapter callable.
6. Add a public-target fail-closed CLI check and assert it exits non-zero without writing a script.
7. Keep `module_runner.py` dry-run planning semantics distinct from the runtime adapter until a separately reviewed live-execution phase authorizes coupling.

Example shape for a Level 1 metadata bundle:

```text
scripts/lab_modules/<bundle>_metadata.py
scripts/test_<bundle>_metadata_lab_module.py
```

The adapter should output observation/candidate records only; it must not auto-promote confirmed/verified/reportable findings or submit reports.

### Directory-listing filename-class verifier rung

When a directory-listing observation is already the strongest lab candidate, the next retained-capability step can be a filename/content-class verifier instead of a heavier scanner:

1. RED test a missing `scripts/lab_modules/<context>_filename_content_class_verifier.py` adapter and public-target rejection first.
2. Keep execution plan-only by default and require `--lab-approved` before writing a runnable script.
3. Fetch only the listing page (for example a fixed `/ftp/` path) plus pre/post health. Do not download listed files, recurse, crawl, or persist raw response bodies.
4. Parse listing anchors into normalized `filename`, `path`, `content_class`, and `triage_hint` observations. Useful classes include backup/temp candidates, password-database candidates, sensitive-container candidates, text/markdown, package manifests, archives, and unknown/other.
5. Preserve the class as `needs_manual_review` or equivalent candidate vocabulary only; never infer sensitive file contents from the name alone and never promote to confirmed/reportable.
6. Save JSONL observations, summary, health, and artifact manifest; pull only those safe artifacts back from the tool VM.
7. Update the script inventory, bundle documentation, accepted changes, and active navigation. If there is not yet an importer/bridge, state the explicit deferral and make it the next candidate slice.

This rung is especially useful for OWASP Security Misconfiguration / directory listing work because it captures actionable triage value while avoiding file-content retention and exploit behavior.

### Benign reflection / redirect triage rung

When preview/recon suggests query reflection or redirect behavior but the lab phase should avoid executable XSS payloads and broad scanners, retain the capability as an inert-canary bounded adapter + bundle rather than running raw `open_redirect.sh` or `xss_finder.sh`.

1. RED/GREEN test an adapter such as `scripts/lab_modules/<wave>_benign_params.py` for plan-only default, public-target rejection, unsafe-limit rejection, pre/post health, inert canaries, no redirect following, no executable payloads, and no finding-promotion vocabulary.
2. Use fixed GET-only paths first, e.g. API search, SPA search fallback controls, and a tiny set of redirect canaries. Keep `--max-redirs 0`; record `Location` separately without following it.
3. Treat SPA fallback 200 HTML and error-body echo as false-positive controls unless the inert canary is reflected in the intended sink or a redirect response includes an unsafe `Location`.
4. Persist only JSONL observations, health, summary, artifact manifest, and per-step headers; raw bodies must be temporary or redacted snippets only.
5. Record no-candidate calibration runs too. A no-candidate result can still become an active reusable bundle when it proves the selector/false-positive handling and adapter safety.
6. Create/update an operator-facing bundle such as `modules/bundles/benign_reflection_redirect_triage.md` with `Use when`, `Do not use when`, `Inputs`, `Scripts`, `Caps`, `Outputs`, `Review`, `Current local-lab result`, `Promotion rule`, and bridge-deferral sections.
7. Defer importer/bridge unless a future run observes actual candidate signals. Any bridge must keep seeds `needs_manual_review` and never convert inert-canary output into confirmed evidence.

## OSS / supply-chain gate

For random GitHub PoCs or exploit scripts, do not jump straight to execution. Require:

- Pinned commit/hash or release.
- Static review for outbound callbacks, credential/loot collection, destructive writes, persistence, shell/dropper behavior, and aggressive defaults.
- Local lab only and explicit operator approval.
- Timeout/kill/recovery gates and artifact redaction.

Prefer mature, schema-friendly tools first. Random exploit scripts belong behind a stricter review rung than http metadata/crawler tools.

## Tool-specific rungs captured from lab use

### httpx / katana

- Start with metadata-only `httpx` and depth-limited `katana` before scanners/fuzzers.
- Keep `katana` depth small (`1` first, `2` only with explicit rationale), add crawl scope, and disable raw/body retention.
- Import JSONL as `observation` records only; crawler-discovered URLs are leads, not proof.

### nuclei

- Do not start by running a full template pack. First modular rung should be a generated local informational template or an explicitly allowlisted template registry.
- Add tests that the runner includes `-omit-raw`; nuclei JSONL can otherwise retain request/response/body material that should not become committed fixtures.
- Avoid `-interactions-cache-size 0`; nuclei v3.8.0 can panic with `gcache: Cache size <= 0`. Use a small positive value such as `1` when disabling/avoiding interactions in a bounded lab plan, and keep OAST/callback behavior out of the template/command.
- Imported nuclei results should become `template_observation`/scanner-output records, never confirmed findings.

### ffuf

- First rung should use a generated tiny wordlist checked into/recorded by the runner, not `/usr/share/wordlists` or recursive discovery.
- Bound with low rate, short timeout, and max time (for example rate 2, timeout 5, maxtime 30 in local lab calibration).
- Treat hits as `content_discovery_hit` observations requiring manual review; interesting paths such as `/administration`, `/robots.txt`, `/security.txt`, `/api`, `/rest`, or `/ftp` are inventory/candidate leads, not automatic vulnerabilities.

### Windows Git-Bash to Kali path generation

When generating a bash script on Windows/Git-Bash that will run on Kali/Linux, guard absolute Linux paths from MSYS path conversion. Prefix the local generation command with `MSYS2_ARG_CONV_EXCL='*'` or otherwise verify the generated script did not rewrite `/home/kali/...` into `C:/Program Files/Git/home/kali/...`. Add a focused regression when this path class matters.

## Handoff and durable learning

After a successful useful run:

- Update accepted changes with the new reusable module and validation commands.
- Keep run-specific target paths, scan logs, and dated artifacts in repo handoff/fixtures, not global memory.
- If the pattern is reusable beyond the repo, update this skill/reference rather than creating a narrow one-session skill.

## Pitfall

Do not treat `setting/local/*.sh` helpers as sufficient retained capability. If the script has enduring value, promote the pattern into committed/tested `scripts/` modules with fixtures and safety tests.