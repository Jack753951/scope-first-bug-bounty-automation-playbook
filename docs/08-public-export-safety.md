# 08 — Public Export Safety

Status: public methodology

## Pattern

1. Treat the private workspace as sensitive by default.
2. Create a separate public-clean export directory or repository.
3. Write/rewrite public content by hand; do not recursively copy private handoff.
4. Run a fail-closed scan for paths, tokens, target names, VM names, IPs, advisories,
   and secret words.
5. Review `git diff --cached` before push.
6. Publish only after the export scan is clean.

## Do not publish raw

- scope files and program lane state;
- screenshots, HAR files, browser state, cookies, or downloads;
- scan output, loot, private evidence bundles;
- local vault/workspace config;
- exact target names or account aliases;
- local VM names, host-only IPs, host paths;
- private worker call transcripts containing target context.

## Prefer public replacements

| Private noun | Public replacement |
| --- | --- |
| exact program or host | `<authorized-target>` |
| local VM name | `<attacker-vm>` / `<victim-vm>` |
| host-only IP | `<lab-ip>` |
| credential/token filename | `<provider-credential-file>` |
| scope file | `<authorized-scope-file>` |
| evidence folder | `<artifact-output-dir>` |
| specific advisory ID | `<specific-advisory-id>` or omit |
