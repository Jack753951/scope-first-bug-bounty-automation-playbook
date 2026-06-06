> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Bug bounty platform pivot cleanup

Use this reference when a cybersecurity workspace has drifted from a broad learning/expert-workbench charter into an automated bug bounty platform.

## Pivot signal

The user frames the current goal as an automated bug bounty platform, not general cybersecurity expertise. The repo should optimize for:

```text
fresh intel / target change -> detector or proof-bundle lane -> candidate -> evidence packet -> operator decision -> report submission
```

## Structural cleanup pattern

1. Preserve history, but remove root-level ambiguity.
   - Move original charters and expert-framework docs to `docs/charter/historical/`.
   - Add a short retired-structure note explaining why old shells were removed or downgraded.

2. Retire empty/manual-workflow root shells.
   - `command-library/` -> historical note or removal; operator should not manually pick commands as the core workflow.
   - `exploits/` -> retire; verification belongs in `modules/`, `labs/proofs/`, or target evidence packets.
   - `recon/` -> retire or migrate into `platform/recon/`.
   - random LLM scratch/noise directories like `etc/` -> delete after checking contents.

3. Downgrade learning/defense assets.
   - Root learning docs -> `notes/learning/`.
   - Defense baseline docs -> `notes/defense/`.
   - CTF notebooks -> `notes/learning/ctf/`.

4. Promote platform destinations.
   - `platform/detectors/`, `platform/recon/`, `platform/pipeline/`, `platform/bounty/`, `platform/intel/`, `platform/inbox/`, `platform/agents/`.
   - `docs/runbook/` for DAILY_SOP / Hermes workflow / Kali workflow.
   - `intelligence/cve_briefs/` for generated/adjudicated CVE brief archives.
   - `handoff/current/` only after worker scripts such as `bin/hermes` are updated and tested.

5. Rewrite active contracts in the same batch.
   - `PROJECT_CHARTER.md`: platform charter and north star.
   - `README.md`: first paragraph and repo map.
   - `AGENTS.md`: routing as detection / lane execution / evidence / review / submission / platform.
   - `.hermes.md`: project context, assets, routing, cadence.
   - `handoff/current_navigation.md` and `handoff/active_strategy_queue.md`: active platform identity and latest lanes.

## Pitfalls

- Do not move active rolling IPC (`handoff/cowork_task.md`, worker results, etc.) until script paths are updated and smoke-tested.
- Do not mix a structural cleanup commit with unrelated live-bounty lane state if the working tree is dirty; stage scoped paths only.
- If CVE briefs move under `intelligence/cve_briefs/`, update `.gitignore` exceptions so `cve_brief_*.md/json` archives are trackable there while root generated briefs can remain ignored.
- Keep historical expert-workbench material; do not erase the rationale. It can support future unfamiliar bug-class research, but it should not drive the platform workflow.

## Verification

- `python -m py_compile` for touched Python scripts.
- `git diff --check` for whitespace/path issues.
- `git check-ignore -v` for newly archived generated files that should be tracked.
- `git status --short` to confirm intended moves, deletions, and new platform skeleton only.
