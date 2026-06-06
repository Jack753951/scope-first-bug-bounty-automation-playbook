> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Target Source Intake Platforms

Use this reference when the operator asks where to find new first-bounty targets or has just registered on new bounty platforms.

## First-bounty platform priority

Primary sequence for this Cybersec Lab first-bounty workflow:

1. HackerOne — keep as the main source when the account/workflow already exists.
2. Bugcrowd — register early; strong second source for public bounty programs and VRT-guided severity expectations.
3. Intigriti — register early; good source for SaaS/B2B web/API targets, often with less H1-style crowding.
4. YesWeHack — useful backup/diversity source; register after the first three if operator bandwidth allows.
5. HackenProof / Immunefi — observe only unless explicitly pivoting to web3/crypto.
6. Synack — longer-term onboarding, not a near-term first-bounty dependency.
7. Open Bug Bounty / disclose.io / FireBounty / ProjectDiscovery Chaos — discovery/reference sources; not automatically paid bounty authorization.

## First-bounty source rules

Prefer programs with:

- paid bounty, not VDP-only, unless the goal is practice/no-finding closeout;
- self-serve signup and free plan/trial;
- clear web/API scope and permission to test owned accounts/data;
- team/org/workspace/role/invite lifecycle;
- owned objects such as project/task/file/inbox/resource;
- API docs or direct URL surface;
- access-control, stale-access, IDOR, metadata leak, or UI/API mismatch bundle fit;
- low operator cost unless signal is already strong.

Park or kill programs with:

- reward disabled / bounty suspended;
- phone/KYC/payment/sales-demo gate before any strong signal;
- unclear scope or no permission for the candidate technique;
- marketing-only surface;
- high-friction mobile-only setup;
- VDP-only when the active metric is first paid bounty.

## Intake artifact pattern

For a new platform registration or first sweep, create/update a compact repo-local intake file such as:

`handoff/current/target_source_intake_<date>.md`

Include:

- registered platform status;
- first-bounty scoring template;
- 5 candidate programs from each new source;
- score /23 using the first-bounty target gate;
- decision: EXECUTE / PASSIVE_ONLY / PARK / KILL;
- operator gates and stop-before rule.

Do not store platform passwords, OTPs, recovery codes, phone values, tokens, cookies, or verification links in the intake file.

## Practical next step after registration

After the operator registers Bugcrowd and Intigriti, do not immediately test targets. First collect and score 5 candidate programs from each platform, then choose the top 1-3 candidates for policy/scope intake and bundle precondition review.
