> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Offline Module Discovery / Profile Selection

Use this pattern when adding module discovery before any real module execution exists.

## Contract

- Discovery is offline/data-only: read committed JSON manifests, do not import module code.
- Scan only repo-local `modules/checks/**/module.json` by default.
- Validate every discovered manifest with the strict module manifest validator before selection.
- Fail closed on malformed manifests, duplicate `module_id` values, unsupported profiles, or unsafe execution posture.
- The first conservative profile can be `audit-baseline`, selecting only modules whose manifest declares:
  - `execution.default_profile == "audit-baseline"`
  - `execution.supports_dry_run == true`
  - `execution.requires_network == false`
  - `execution.network_access == "none"`
  - `execution.target_touching == false`
  - target type compatible with the requested target type
- Pass selected manifests into the existing dry-run planning path, which should revalidate manifests and policy artifacts.

## CLI safety

- Keep discovery mode mutually exclusive with explicit manifest paths unless explicit paths receive the same repo-local containment/profile checks.
- If mixed modes are not needed, fail closed with a clear error such as: `cannot combine --discover-root with explicit --manifest paths`.

## TDD coverage

Add failing tests first for:

1. committed Level 1 fixture selected by `audit-baseline` discovery;
2. duplicate `module_id` denial;
3. malformed manifest denial;
4. path escape outside `modules/checks` denial;
5. target-touching/network-requiring manifest denial;
6. CLI discovery-to-plan happy path;
7. CLI mixed discovery + explicit manifest denial.

## Validation

- Focused runner/discovery tests.
- Full repository test suite where safe.
- Python compile and JSON parse.
- Project review/preflight wrapper.
- Independent Cowork/Claude review for non-trivial module platform changes.

## Safety boundary

Do not enable module execution, scanner execution, subprocess launch, network clients, target touching, callback behavior, finding/evidence emission, `config/scope.txt` changes, credentials/loot/report writes, scheduler/deployment/billing/production changes.