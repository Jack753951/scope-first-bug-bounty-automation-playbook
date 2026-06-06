> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# verified_lab_flow_juice_shop_search_sqli_boolean

Status: active / verified local-lab flow candidate
Lane: local-learning-lab
Source lineage: GitHub/Arjun-inspired parameter discovery -> bounded parameter probe -> one-vulnerability SQLi boolean differential proof
Latest handoff: `handoff/juice_q_sqli_bounded_wave_20260522.md`
Latest artifacts: `<artifact-output-dir>/juice_q_sqli_bounded_wave_20260522T110815Z/`

## When to use

Use this bundle when an authorized disposable Juice Shop-style target exposes a search endpoint like:

```text
/rest/products/search?q=...
```

and the goal is to test one vulnerability behavior only: SQL injection style boolean response differential on the `q` search parameter.

Do not use this bundle for public targets unless a separate authorized-assessment scope/rules gate is completed and the runner is adapted for safe public-target defaults.

## Scripts/tools

Primary reusable adapter:

```text
scripts/lab_modules/lab_juice_shop_search_sqli_boolean_probe.py
```

Focused tests:

```text
scripts/test_lab_juice_shop_search_sqli_boolean_probe.py
```

The adapter emits plan JSON by default and writes a runnable bash script only with `--lab-approved`.

## Example usage

Plan-only:

```bash
python scripts/lab_modules/lab_juice_shop_search_sqli_boolean_probe.py \
  --target http://<lab-ip>:3000/
```

Generate a local-lab runner:

```bash
python scripts/lab_modules/lab_juice_shop_search_sqli_boolean_probe.py \
  --target http://<lab-ip>:3000/ \
  --lab-approved \
  --out-script setting/local/verified_lab_flow_juice_shop_search_sqli_boolean_run.sh \
  --output-dir <artifact-output-dir>/<run_id>/
```

Target-touching execution should run from the Kali attacker VM route, not the Windows control plane.

## Probe set

The bounded runner sends these GET probes to `/rest/products/search?q=...`:

1. baseline empty: `q=`
2. normal control: `q=apple`
3. syntax probe/control: `q='`
4. boolean true: `q=')) OR 1=1--`
5. boolean false: `q=')) AND 1=2--`

## Candidate signal

Promising evidence is the true/false response differential:

- boolean true returns a much larger result set/body;
- boolean false collapses to the same/similar short empty/error-like body as the single-quote control;
- target health remains OK after the run.

Generic SQL keywords such as `SELECT` or `WHERE` in response text are explicitly treated as noisy controls because they can appear in product content. They are not proof by themselves.

## Outputs

A generated runner writes:

- `results.json`
- `classification.json`
- `observations.jsonl`
- `possible_vulnerabilities.md`
- `summary.txt`
- `artifact_manifest.txt`
- truncated `*.body.txt` response samples

All semantics remain `candidate-only` / `needs_manual_review`.

## False-positive / control handling

Do not promote based on:

- HTTP 200 alone;
- one response-size delta without positive and negative controls;
- generic SQL keywords in body text;
- product/version assumptions from external CVE/PoC sources.

## Missing evidence before report language

- Manual review of exact request/response pairs.
- Redacted evidence packet.
- Impact statement.
- Remediation and retest notes.
- Program scope/rules check before any non-lab use.
- Report-readiness gate before confirmed/reportable language.

## OWASP mapping

- OWASP 2021 A03 Injection
- OWASP 2017 A1 Injection
- 2025 migration track: injection / query manipulation behavior

## Project value

This bundle captures the project’s desired source-driven flow:

```text
vulnerability-source/tool library
-> bounded parameter discovery
-> one discovered surface
-> one-vulnerability proof with controls
-> reusable bundle/module candidate
```

It avoids raw exploit execution and records setup debt separately from useful capability: full Arjun execution needs dependency installation, but the bounded core idea is now retained as a reusable lab module.
