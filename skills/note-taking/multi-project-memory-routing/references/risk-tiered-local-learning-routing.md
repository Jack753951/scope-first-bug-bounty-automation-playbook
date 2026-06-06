> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Risk-Tiered Local Learning Routing

Use this pattern when a project with strong safety/review gates starts slowing content or product learning because publication-grade process is being applied to low-risk local experiments.

## Trigger

Examples:

- User says safety mechanisms are slowing learning.
- User agrees that local-only experiments should move faster while upload/publication gates stay strict.
- A status/strategy discussion reveals the project is optimizing for gate compliance more than content/product learning.

## Rule

Do not respond by removing safety. Re-tier safety by risk:

- Local-only learning: fast, lightweight, batch-oriented.
- Private / scheduled / public canary: strict exact-artifact gates.
- OAuth, scheduler, channel destination/config, default privacy, publication, runtime deletion: highest strictness and explicit approval only.

Treat the correction as a project-local strategy/navigation update, not as runtime approval.

## Procedure

1. Verify project authority layers before writing:
   - active strategy queue / roadmap handoff;
   - accepted changes or decision log;
   - Obsidian project strategy/index if the project uses Obsidian.
2. Update the compact active strategy layer with a short overlay:
   - heavy gates were slowing low-risk learning;
   - local-only experiments should use faster batches;
   - hard gates remain strict for irreversible/high-risk actions;
   - no generation/upload/scheduler/OAuth action is authorized by the note itself.
3. Record the decision in accepted changes or decision log.
4. Update the long-term strategy note / Obsidian project strategy so future status answers preserve the distinction.
5. Keep global Hermes memory project-detail-light; save at most a compact signpost only if the preference is cross-project.

## Recommended project wording

```text
Local-only learning may run faster once explicitly requested: prefer 3-5 local-only drafts per learning batch, lightweight QA only, compact table logging, and batch ranking/review after enough artifacts instead of long per-artifact handoff/review.

Candidate promotion rule: only the top candidate selected from a local batch enters exact-artifact private/scheduled/public gate with full validation, auth/destination checks, and explicit user approval.

Hard gates remain strict for upload, publication, scheduled/public canary, OAuth/token/client_secret, channel destination/config, DEFAULT_PRIVACY, Windows Task Scheduler, runtime deletion, and third-party/competitor asset reuse.
```

## Output wording pattern

```text
你說得對：目前問題不是安全方向錯，而是安全等級沒有依風險分層。
我已把專案導航修成：local-only learning 快；private/public/OAuth/scheduler 等高風險 gate 嚴格。
這不是生成、上傳或排程授權；下一步若你要繼續，建議開一輪 3-5 支 local-only batch。
```

## Pitfalls

1. Do not treat “speed up learning” as approval to publish, schedule, change OAuth, change destinations, or enable broad automation.
2. Do not keep applying private/public canary readiness criteria to every local-only artifact.
3. Do not create long per-artifact handoff files for every low-risk local draft if the accepted direction is batch learning; use compact tables and batch summaries.
4. Do not remove hard safety gates where mistakes are irreversible or account/channel-affecting.
5. Do not save dated artifacts, video IDs, or one-off phase state in global memory; route those to repo handoff.