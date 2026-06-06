> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Freshness-First Vulnerability × Target Lanes

Session signal: the operator clarified that the highest-value first-bounty zones are latest vulnerabilities and latest targets, and wants stronger attacker thinking while preserving authorized, bounded execution.

Use this reference when driving a first-bounty sprint or target-source intake.

## Core rule

Prioritize the intersection:

```text
fresh vulnerability × fresh/under-tested/scoped bounty target -> first-bounty candidate
```

If no clean intersection exists yet, keep two compact parallel lanes:

- `fresh_vuln_lane`: new CVE/advisory/PoC/patch diff -> local proof or passive detector -> scoped target match -> evidence/report only if policy allows.
- `fresh_target_lane`: new/updated/invited/scope-expanded program -> access-control/business-logic bundle -> owned-control proof -> report candidate.

Both lanes must serve the first-bounty metric. Do not let latest-vuln work become detector sprawl, and do not let latest-target work become signup/login drift.

## Good fresh-vuln candidates

Prefer vulnerabilities with:

- current-year, ideally last 1-2 months;
- common bounty-scope deployment or source-available product;
- web/API/auth/access-control/tenant/business-logic relevance;
- safe local proof or passive/owned-control live transfer;
- no need to read secrets, customer data, arbitrary files, or prove destructive RCE live.

Useful public sources:

- CISA KEV;
- NVD recent/modified CVEs;
- GitHub Security Advisories;
- vendor advisories / patch diffs;
- GitHub PoC trend only as triage, not as execution authorization;
- nuclei template updates only after scope/policy review.

Decision vocabulary:

- `EXECUTE_LOCAL_RESEARCH`: source/local lab proof is useful now.
- `PASSIVE_ONLY`: only passive matching or source review; no live exploit.
- `LOCAL_LAB_REFERENCE`: use as bundle inspiration, not target action.
- `RESEARCH_ONLY`: watch/understand; not enough bounty transfer yet.

## Good fresh-target candidates

Prefer targets with:

- newly launched, newly updated, private/invited, campaign, bounty/scope-changed, or newly added asset;
- paid bounty rather than VDP when first bounty is the primary metric;
- self-serve signup and low operator friction;
- team/workspace/org/role model;
- owned object/resource creation;
- API docs, SDK, public source, direct URLs, or clear object IDs;
- program policy that accepts access-control/business-logic findings.

Kill/park quickly when:

- phone/KYC/payment/sales-demo gates appear before a strong report title;
- the program is VDP/no-reward and the current goal is paid first bounty;
- scope or allowed techniques are unclear;
- only static/marketing pages are in scope;
- no owned object, negative control, or likely bundle exists after a short review.

## Intersection scoring prompt

For each candidate, fill only this compact record before target-touching work:

```text
lane: fresh_vuln / fresh_target / intersection
why_now:
program/platform:
bounty_or_vdp:
scope/policy status:
asset/surface:
bug_class:
proof_bundle:
operator_cost:
owned_controls:
evidence_path:
stop_before:
decision: EXECUTE / PASSIVE_ONLY / PARK / KILL
```

## Example high-value intersections

- New AI/devtool advisory + program exposing AI workflow/devtool/API surface.
- New/updated SaaS search/API program + metadata leak or API/UI permission mismatch bundle.
- New dedicated HR/business workflow bounty + owned account/profile/application object model.
- Patch diff for auth/tenant bug + source-available bounty target with similar flow.

## Pitfalls

- Do not treat a detector hit or technology fingerprint as a vulnerability.
- Do not live-test RCE/path traversal/SQLi/SSRF/OAST from a fresh advisory unless program scope and rules explicitly permit the exact technique and the proof is bounded.
- Do not spend a full session on signup friction; record the gate and pivot.
- Do not let “latest” justify poor target fit; fresh but unreportable is still PARK/KILL.
- Do not write a long strategy note when a compact lane record and execute/park/kill decision is enough.
