> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Latest RCE detector lane correction

Use this reference when the user asks for a latest-vulnerability lane and specifically expects fresh remote-control / RCE-style CVEs.

## Lesson

Do not over-optimize the latest-vuln lane for bounty-safe data leaks or access-control issues when the user asked for latest RCE / remote control signal. Preserve safety boundaries, but search and rank RCE candidates explicitly.

Correct split:

```text
latest RCE search -> candidate ranking -> local/lab detector EXECUTE -> live PASSIVE-ONLY -> exploit PARK unless explicitly authorized
```

## Candidate evaluation criteria

Prefer candidates that are:

- recent, ideally within the last 1-2 months;
- web/SaaS/CMS/framework products likely to appear in bug bounty scope;
- detectable by passive fingerprint, public asset, version, package, or exposure evidence;
- reproducible in local/owned lab with vulnerable/fixed versions;
- reportable from version/exposure/reachability evidence if program policy allows known-CVE reports.

Downrank or park candidates that require:

- live RCE triggering;
- callback/OAST/external payload hosting;
- writing files, running commands, or manipulating serialized payloads;
- admin/workflow privileges that may touch secrets/API keys/customer data;
- host/cloud/container/database control on third-party systems;
- social engineering or local-client compromise.

## Output shape

For each candidate, record:

```text
CVE/GHSA:
Product:
Published date:
Affected versions:
Why it is high-signal:
Why it may be bad for first-bounty live work:
Safe proof boundary:
Decision: EXECUTE lab detector / PASSIVE-ONLY live / PARK live exploit / KILL
```

## Pitfall from session

The user corrected a too-conservative selection: a Strapi data-leak lane was useful but not the right primary answer to "latest remote-control CVE". The corrected primary lane became a 2026-05 RCE detector approach, with live actions limited to passive/version/exposure checks and local lab validation for proof.

## Safety rule

Known-CVE RCE work is valuable as platform signal, but live exploitation is not default. Unless a program explicitly allows the technique and the operator approves it, do not trigger RCE on live targets.
