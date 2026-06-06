> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4B OWASP bounded Wave — Benign reflection/redirect triage rerun

Status: completed / local-lab fast lane / candidate-only
Date: 2026-05-21
Run id: `phase4b_wave2_benign_rerun_20260521T070726Z`
Route/tool: Hermes local tools + Kali bridge (`scripts/kali-run.ps1`, `scripts/kali-pull.ps1`)
Visible runtime model: gpt-5.5 via Hermes/OpenAI Codex route; exact lower-level deployment details not exposed
Usage artifact path: none; direct Hermes tool execution only

## Selected OWASP class

Selected next bounded OWASP wave: preliminary A05-style injection/reflection/redirect triage using inert canaries.

Reason: original `open_redirect.sh` and `xss_finder.sh` are too broad for the fast lane, but the existing `wave2_benign_params.py` adapter can safely test a tiny fixed set of query/reflection and redirect behaviors on the local靶機 without executable payloads, redirect following, scanners, callbacks, brute force, or credentialed flows.

## Lab boundary

Target class: local intentionally vulnerable lab / private host-only VM.

Concrete target:

```text
http://<lab-ip>:3000/
```

This run did not touch public or real bug-bounty targets. It did not run broad scanners, brute force, OAST/callbacks, credentialed flows, exploit chains, recursive crawlers, file downloads, redirect following, or report submission.

## Adapter used

```text
scripts/lab_modules/wave2_benign_params.py
scripts/test_wave2_benign_params.py
setting/local/wave2_benign_params_rerun.sh
```

Adapter behavior:

- plan-only by default;
- `--lab-approved` required before writing executable script;
- private/local-lab target allowlist;
- fixed GET-only paths;
- inert text canary: `PHASE4B_REFLECT_CANARY`;
- inert redirect canary: `https://phase4b-canary.invalid/`;
- `--max-redirs 0`, no redirect following;
- raw bodies temporary only, redacted snippets in observations;
- output candidate-only JSONL;
- no executable JavaScript payloads, scanners, crawlers, callbacks, credential flows, or finding promotion vocabulary.

## Lab run result

Remote output directory:

```text
/home/kali/codex-output/phase4b_wave2_benign_rerun_20260521T070726Z
```

Pulled local artifact directory:

```text
<artifact-output-dir>/phase4b_wave2_benign_rerun_20260521T070726Z/
```

Health:

```text
pre_health=200
post_health=200
requests_sent=5
```

Summary:

```text
observations=5
1 x ('level2.benign_reflection_candidate', '200', 'application/json; charset=utf-8')
1 x ('level2.benign_reflection_candidate', '200', 'text/html; charset=UTF-8')
3 x ('level2.open_redirect_candidate', '406', 'text/html; charset=utf-8')
```

Notable observations:

```text
GET /rest/products/search?q=PHASE4B_REFLECT_CANARY -> 200 body_canary=False loc_canary=False ext_redirect=False loc=None title=None
GET /search?q=PHASE4B_REFLECT_CANARY -> 200 body_canary=False loc_canary=False ext_redirect=False loc=None title='OWASP Juice Shop'
GET /redirect?to=https%3A%2F%2Fphase4b-canary.invalid%2F -> 406 body_canary=False loc_canary=False ext_redirect=False loc=None title='Error: Unrecognized target URL for redirect: https://phase4b-canary.invalid/'
GET /redirect?to=/ -> 406 body_canary=False loc_canary=False ext_redirect=False loc=None title='Error: Unrecognized target URL for redirect: /'
GET /redirect?to=/#/score-board -> 406 body_canary=False loc_canary=False ext_redirect=False loc=None title='Error: Unrecognized target URL for redirect: /'
```

## Candidate assessment

No reflection/XSS candidate was found for these inert canaries.

No open-redirect candidate was found for these fixed redirect canaries because every redirect probe returned 406 and no `Location` header.

Useful calibration:

- `/search?q=...` is a SPA fallback false-positive control, not reflection evidence.
- `/rest/products/search?q=...` returned JSON success/empty data without reflecting the canary.
- `/redirect?to=...` rejects the tested canaries; error-body echo is tracked separately and is not counted as redirect/reflection evidence.

## Validation commands

```text
python scripts/test_wave2_benign_params.py
bash -n setting/local/wave2_benign_params_rerun.sh
Kali bridge run via scripts/kali-run.ps1
Kali artifact pull via scripts/kali-pull.ps1 with MSYS2_ARG_CONV_EXCL='*'
```

Observed validation:

```text
4 tests OK
bash -n OK
pre/post health 200
observations.jsonl produced
```

## Modularization decision

The successful/no-candidate calibration is retained as:

1. bounded runner/adapter: `scripts/lab_modules/wave2_benign_params.py`;
2. operator-facing bundle: `modules/bundles/benign_reflection_redirect_triage.md`;
3. generated runnable helper: `setting/local/wave2_benign_params_rerun.sh`;
4. pulled lab artifact result: `<artifact-output-dir>/phase4b_wave2_benign_rerun_20260521T070726Z/`.

Bridge/importer deferral: candidate-review fixture generation is intentionally deferred. This rerun produced no candidate that should become a finding fixture; future importer logic should only seed manual-review candidates if a canary reflection or external redirect candidate is actually observed.