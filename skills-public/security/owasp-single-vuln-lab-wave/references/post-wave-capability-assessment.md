> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Post-wave capability assessment pattern

Use this when the operator asks to continue testing and then explain what the project can do now.

## Trigger

- The operator says some form of: `continue testing`, `after this test tell me what the project can do`, or asks for a capability summary after a local-lab proof wave.
- A wave has produced artifacts, route checks, validation output, or reviewer feedback.

## Pattern

1. Keep the test local-lab scoped unless the operator explicitly authorized a real/public target.
2. Verify the route before/after target-touching work:
   - attacker/victim identity;
   - host-only/NAT posture;
   - pre/post target health;
   - artifact pullback location.
3. Run only a capability-relevant proof wave, not a broad new lane, unless the active queue says otherwise.
4. Review evidence before claiming success:
   - positive marker or impact evidence;
   - negative/control evidence;
   - origin/path/session/source labels where relevant;
   - explicit false-positive boundary;
   - report-readiness status.
5. Record the result in repo handoff and project Obsidian when it changes project capability or navigation.
6. In the final response, include a compact capability map, not just a run log.

## Final response shape

Use concise Traditional Chinese by default for this operator:

```text
本次測試結論：
- route/tool
- target/scope
- artifact paths
- validation result
- reviewer identity/model/runtime if a review was used

專案現在能做到什麼：
1. infrastructure / route capability
2. proof classes actually verified
3. evidence quality and false-positive controls
4. reusable bundle/proof-library state
5. remaining limits before public/bug-bounty readiness

Dissent / boundary：
- what this does NOT prove
- what still blocks public-target/report-ready use

新增/更新了什麼：
- handoff
- bundles/scripts/artifacts
- Obsidian/project navigation
```

## Classification discipline

Prefer capability wording tied to evidence:

- `local-lab proof-capable`
- `verified local-lab runtime proof`
- `reusable methodology`
- `report-readiness rehearsal`
- `candidate needs manual review`

Avoid overclaiming:

- Do not say `bug bounty ready` merely because local proof waves succeeded.
- Do not imply public-target authorization from local-lab capability.
- Do not claim credential theft, cross-user impact, persistence, RCE, callback, file-read, or reportable finding unless those exact evidence elements are present.

## Example capability synthesis

A strong local-lab XSS rerun can support:

- stable attacker route and host-only posture;
- authenticated browser-runtime proof with DOM marker;
- positive/control separation;
- artifacted evidence packet inputs;
- reusable XSS proof methodology.

It does not by itself support:

- public-target readiness;
- production impact;
- credential/token exfiltration;
- persistent/cross-user XSS;
- automatic finding/report submission.
