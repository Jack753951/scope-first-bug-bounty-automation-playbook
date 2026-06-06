> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Level 1 Security Headers Baseline

`level1.security_headers_baseline` is an offline workflow-validation module. It exists to prove the committed fixture -> deterministic check -> committed candidate finding fixture -> human triage draft path without adding a runtime emission surface.

## Runtime Boundary

- No network, DNS, socket, TLS, subprocess, thread, async, or callback behavior.
- No live target input flags. The CLI accepts only `--fixture`, `--run-id`, and `--policy-decision-sha256`.
- No runtime writes. The CLI prints a single JSON array to stdout and writes nothing to `runs/`, `evidence/`, `loot/`, or `reports/`.
- No schema bumps and no runner, recon, CI, hook, scheduler, deployment, or profile wiring.
- `module.json` declares `emits_findings=false` and `emits_evidence=false`; runtime finding/evidence emission is deferred to a separately reviewed phase.

## Closed Fixture Shape

Fixtures are JSON objects with exactly these keys:

```json
{
  "fixture_version": "security_headers_baseline_input/1",
  "target": {
    "type": "domain",
    "value": "lab.local"
  },
  "status_code": 200,
  "headers": [
    {
      "name": "Content-Security-Policy",
      "value": "default-src 'self'"
    }
  ]
}
```

Rules:

- `fixture_version` must be exactly `security_headers_baseline_input/1`.
- `target.type` is only `url` or `domain`.
- Committed fixture targets use reserved or lab placeholders such as `lab.local`, `*.example.test`, `invalid.`, or URLs under those placeholder names.
- `status_code` is an integer from 100 through 599. Header rules apply uniformly across status codes in v1.
- `headers` is a list of closed `{name,value}` entries. Header names must match the RFC token-safe character set used by the tests. Header values are accepted only as fixture data and are not rendered into finding text.

## Header Coverage v1

The v1 coverage is exactly:

- `Content-Security-Policy`: missing; weak inline directive present.
- `X-Frame-Options`: missing; value outside the approved baseline.
- `X-Content-Type-Options`: missing; value outside the approved baseline.
- `Strict-Transport-Security`: missing; duration baseline not met; subdomain baseline not applied.
- `Referrer-Policy`: missing; value outside the fixed allowlist.

Header names are matched case-insensitively. Value comparisons are intentionally verbatim in v1 so fixture drift is visible in tests.

## Finding Shape

`evaluate(fixture, *, run_id, policy_decision_sha256)` returns `finding/1.0`-shaped candidate dictionaries:

- `status` is always `candidate`.
- `triage.scanner_output_only` and `triage.manual_verification_required` are always `true`.
- `source.module_id` is `level1.security_headers_baseline`.
- `source.run_id` and `source.policy_decision_sha256` must be supplied by the caller and are never synthesized.
- `evidence` is an empty array in v1.
- Finding text does not include `target.value` or raw header values.

The finding `id` is the stable rule ID, for example `security_headers_baseline.csp.missing`.

## Severity Hints

Severity is a static per-rule hint from the inline table in `check.py`. There is no numeric scoring, aggregate grade, or computed severity. Any future scoring model requires its own T3 review.

## References

- OWASP Secure Headers Project: `https://owasp.org/www-project-secure-headers/`
- OWASP ASVS V14.4 HTTP Security Headers requirements: `https://owasp.org/www-project-application-security-verification-standard/`
