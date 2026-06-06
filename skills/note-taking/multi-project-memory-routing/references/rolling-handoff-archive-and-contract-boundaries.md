> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Rolling Handoff Archive and Contract-Boundary Adoption

Use this when borrowing process fixes from one project into another where both projects use rolling handoff files or generated review packets.

## Pattern

1. Identify rolling convenience outputs that wrappers overwrite, such as:
   - latest worker result,
   - latest review summary,
   - latest orchestration/pipeline report.
2. Before wrapper overwrite, copy any existing non-empty output to a local archive path such as `handoff/archive/rolling/` with timestamp + reason + original filename.
3. Add the archive path to `.gitignore` when it is only a local safety backup.
4. Keep durable decisions in named artifacts and accepted-change logs; archived rolling files are backup evidence, not the source of truth.
5. Add a small static regression test or smoke test that checks archive-before-overwrite placement for the wrapper.
6. Update project workflow docs so future agents know rolling files are convenience pointers.

## Contract-boundary distinction

When adopting a source project's strict boundary-contract idea, translate by artifact type:

- Machine-readable contracts: use explicit schema/version, closed fields, strict validation, and fail-closed unknown-field handling.
- Human governance Markdown: do not force machine schemas; instead include freshness/authority metadata and reviewer identity/decision blocks.
- Periodic review packets: treat as frozen governance snapshots, not activation contracts. If they conflict with live code or accepted handoff, verify and use current project authority.

## Do not transfer blindly

Do not copy source-project domain vocabulary such as cybersecurity target/scope/scanner/exploit fields into unrelated projects. Translate only the reusable governance property: archive-before-overwrite, durable-vs-convenience separation, and strict contracts only where machines parse them.

## Verification

- Wrapper smoke test passes.
- Archive path is ignored if local-only.
- No production/activation side effects occurred.
- Docs state where durable decisions belong.
