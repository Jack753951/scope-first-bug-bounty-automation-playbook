> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# INDEX — Project Canon (force-read, anti-drift)

Status: **binding**. Authority: see `SAFETY.md` § Authority order.

## Role

Authorized bug-bounty platform. Hermes (GPT-5.5) primary autonomous driver; Claude/Codex on-demand consults; operator clears human gates. Hard stops live in `SAFETY.md`.

## Canonical directory map

| Path | Owner | Mutate by |
|---|---|---|
| `SAFETY.md` | Operator | Operator |
| `INDEX.md` (this) | Operator | Operator (Hermes may propose; edit only with explicit approval) |
| `.hermes.md` | Operator | Operator (Hermes may propose) |
| `CLAUDE.md` | Operator | Operator |
| `README.md`, `PROJECT_CHARTER.md` | Operator | Operator |
| `bugbounty_report_template.md` | Operator + Hermes | Template edits with redaction/safety review |
| `bin/` | Operator | Codex (with operator review) |
| `config/scope.txt` | **Operator only** | **Operator only**, never agent |
| `config/recon.conf`, other `config/` | Codex + Operator | Codex/operator; no scope broadening without operator |
| `hermes/policies/` | Operator | Operator (Hermes may propose) |
| `hermes/loops/` | Operator + Hermes | Hermes may edit cadence; structure operator-owned |
| `hermes/state/` | Hermes | Hermes runtime/log state; transient pointers may be ignored |
| `hermes/digests/` | Hermes | Hermes writes daily |
| `hermes/calls/` | Hermes | Hermes append-only call records |
| `hermes/proposals/` | Hermes | Hermes writes; operator decides |
| `handoff/current_navigation.md` | Hermes + Operator | Hermes routine; operator for KILL list |
| `handoff/live_bounty_lane_queue.json` | Hermes | Hermes |
| `handoff/pending_intake.json` | Hermes | Hermes |
| `handoff/operator_inbox_<date>.md` | Hermes | Hermes daily (dated OK) |
| `handoff/accepted_changes.md` | All | **Append only, never truncate** |
| `handoff/live_bounty_*` (state/runner/seeds) | Hermes + runtime | Per file purpose |
| `programs/<slug>/scope.json` | Operator | Operator-approved only |
| `programs/<slug>/lane_state.json` | Hermes | Hermes for passive transitions |
| `programs/<slug>/notes/` | Hermes + Claude | Hermes/Claude |
| `programs/<slug>/findings/` | Hermes + Claude | with redaction rules |
| `intelligence/cve_briefs/` | Hermes | Hermes |
| `intelligence/program_briefs/` | Hermes | Hermes |
| `cves/` | Hermes | Public vuln-intel candidates/caches; raw feeds mostly ignored |
| `scripts/` (+ INDEX, SCRIPT_INVENTORY) | Operator + Codex | Codex review for code changes |
| `platform/` | Operator + Codex | Codex |
| `schemas/`, `fixtures/`, `tests/`, `tools/` | Operator + Codex | Validation/test/tooling changes; keep runnable checks |
| `modules/` | Hermes + Claude | Reusable bundles/check modules; evidence-safe summaries only |
| `labs/` | Hermes + Claude | Local/disposable lab proofs and inventories |
| `skills/` | Hermes + Operator | Repo-local project skills/reference; profile skills live outside repo |
| `wordlists/`, `templates/` | Hermes + Operator | Reusable inputs/templates; no secrets or live target data |
| `notes/`, `docs/`, `reports/` | Per file | Per file; prefer active truth over dated variants |
| `public_exports/`, `pictures/` | Hermes + Operator | Sanitized/shareable outputs only; no secrets/loot/customer data |
| `targets/` | Runtime + Hermes | Target/lab metadata only; live authorization still requires scope files |
| `setting/` | Local runtime | Machine-local config; secrets/keys ignored |
| `<artifact-output-dir>/`, `logs/`, `loot/`, `scans/`, `tmp/` | Runtime | Runtime/evidence/cache; mostly gitignored; sanitize before promoting |
| `.claude/`, `.playwright-mcp/`, `.pytest_cache/`, `__pycache__/`, `.n/` | Local runtime | Ignored local/cache state; do not commit |
| `archive/` | Operator | Frozen historical/reference after archive |

## Source-of-truth

| Topic | File |
|---|---|
| Allowed/forbidden actions | `SAFETY.md` |
| File ownership + drift | `INDEX.md` (this) |
| Hermes role + cadence | `.hermes.md` |
| What Hermes can write | `hermes/policies/autonomous_actions.md` |
| When to call Claude/Codex | `hermes/policies/consult_{claude,codex}.md` |
| When Hermes must stop | `hermes/policies/stop_conditions.md` |
| Per loop's job | `hermes/loops/<loop>.md` |
| Current active route | `handoff/current_navigation.md` |
| Today's decisions | `handoff/operator_inbox_<latest>.md` |
| Active lanes | `handoff/live_bounty_lane_queue.json` |
| Per-program scope/state | `programs/<slug>/{scope,lane_state}.json` |
| Change log | `handoff/accepted_changes.md` (append only) |
| Hermes proposals | `hermes/proposals/<date>_<topic>.md` |

Other files reference these. They do not paraphrase.

## Forbidden patterns (drift signals)

1. **Dated strategy doc variants.** No `strategy_20260520.md` / `notes_v2.md` / `plan_final.md`. Only datable: `handoff/operator_inbox_<date>.md`, `hermes/digests/<date>.md`, `hermes/calls/<ts>_*.md`, `intelligence/cve_briefs/cve_brief_<date>.md`, `intelligence/program_briefs/<slug>_<date>.md`, `labs/proofs/*_<date>.md`, logs.
2. **Review-ping-pong artifacts.** No `cowork_proposal.md` / `codex_task.md` / `claude_code_result.md` at `handoff/` root. Use `hermes/calls/` (single-shot, logged).
3. **New top-level directories** without INDEX entry.
4. **New `.md`** outside listed locations without INDEX entry.
5. **Duplicate active-truth files.** One INDEX, one SAFETY, one .hermes, one current_navigation.
6. **Restating `SAFETY.md` rules.** Reference, don't paraphrase.
7. **Mega-commits.** Split by intent.
8. **`git reset --hard` / `git clean -fdx` / `rm -rf`** on lane state / scope / evidence / governance / logs / loot. Archive.
9. **Schema fictions.** If not enforced, remove.
10. **Verbose `learning.*` paragraphs in JSON.** Move to commit messages or notes.

## Drift detection (Hermes runs weekly)

- `git ls-files | grep -E '_v[0-9]+\.md$|_final\.md$|_old\.md$|_backup'` excluding `archive/`, `docs/**/archive/`, `handoff/archive/`, and `skills/.archive/` unless auditing historical debt.
- New `.md` under `handoff/` not matching the allowed list above.
- New top-level dir not in this index.
- `lane_state.json` with `learning.next_preview_seed` or `learning.reusable_capability`.
- Files >500 lines in `handoff/` or `programs/<slug>/`.

## Adding new files / dirs

1. Check this index.
2. If genuinely new: edit `INDEX.md` first (single commit).
3. Then add the file/dir (second commit).
4. If it fits an existing governed zone, put it there instead of creating a new top-level path.
5. If it is local/runtime/cache/secret-bearing, add an explicit `.gitignore` rule instead of tracking it.
6. If the new location cannot be justified in INDEX, the location is wrong.

## Authority order

Mirrors `SAFETY.md`. Operator instruction → live repo state → `SAFETY.md` → `INDEX.md` → `.hermes.md` → `hermes/policies/` → active-truth handoff → `docs/` → `archive/` (reference only).

## Boundary

This file does not authorize target action. `config/scope.txt` × `programs/<slug>/scope.json` × `SAFETY.md` decide.
