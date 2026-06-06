> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Rest-period autonomous OWASP/CVE lab waves

Use this reference when the operator asks Hermes to keep working while they rest/sleep on the authorized disposable lab.

## Core interpretation

A rest-period request is not permission to touch public targets or claim that all CVEs can be exhaustively tested. Treat it as permission to make maximum safe progress on the remaining OWASP rows and CVE-adjacent practical checks against the already authorized local lab.

Phrase the goal as:

```text
continue remaining OWASP Top 10 / CVE-usable local-lab waves and record candidates
```

not:

```text
finish all CVEs
```

CVE coverage is open-ended; use CVE tooling and component/version clues as candidate support, not as a guarantee of complete coverage.

## Scheduling pattern

If the work should continue after the current chat turn, create a one-shot cron job with a self-contained prompt. The job should:

1. run from the project workdir;
2. load `owasp-single-vuln-lab-wave`, `test-driven-development`, and `obsidian`;
3. restrict tools to file/terminal/web when possible;
4. deliver back to the origin conversation unless the operator asked for local-only logging;
5. explicitly restate the authorized target/scope and forbidden behaviors;
6. require final validation and a concise Traditional Chinese report.

Avoid scheduling recursive cron jobs from within the cron prompt.

## Prompt ingredients

Include these constraints in the scheduled prompt:

- target-touching work is limited to the authorized disposable local lab and `config/scope.txt` private/local scope;
- no public/real bug bounty/client target activation;
- no malware, stealth persistence, credential theft, uncontrolled DoS, callback/OAST/pivoting, or exfiltration;
- aggressive/destructive lab work requires verified snapshot/restore and post-restore health, otherwise downgrade to metadata/checklist-only;
- outputs remain candidate-only/needs-manual-review;
- no confirmed/reportable/accepted finding language;
- read the tracker, active queue, script inventory, existing bundles, and latest work record before selecting waves;
- prefer 3-5 bounded waves rather than an unbounded promise;
- update bundle docs, script inventory, handoffs, accepted changes, active queue, and Obsidian;
- run focused tests, `py_compile`, `bash -n`, `HACKLAB=$(pwd) ./bin/hermes review`, and include `git status`.

## Good rest-period wave candidates

Prefer rows that can progress safely without interactive operator decisions:

- authentication surface/checklist without brute force;
- vulnerable/outdated component metadata from local dependency/version clues and offline/mature tools;
- software/data integrity metadata;
- logging/monitoring evidence checklist;
- manual verification mini-bundles for already observed `/api-docs` and `/metrics`;
- XXE/deserialization as metadata/checklist-only unless recovery and target fixtures are verified.

Keep SSRF/OAST/callback workflows plan-only unless an isolated callback lab already exists in scope and the prompt explicitly authorizes it.

## Reporting back

The final report should be short and direct in Traditional Chinese:

- what was attempted;
- what completed;
- artifact paths;
- candidate/control summary;
- validation status;
- what remains deferred or plan-only;
- explicit uncertainty where coverage is incomplete.
