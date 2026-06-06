> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Hermes-Owned Live Bug Bounty Loop

Session-derived guidance for authorized live-target bug bounty work where the operator wants Hermes to own the workflow end-to-end while the operator handles only human/secret gates.

## Core correction

Do not turn live-target work into a user-driven checklist where the operator must decide what to test, how to classify it, or which bundle to build next. Hermes should own the assessment loop:

```text
scope/rules intake
-> reconnaissance plan
-> tactical preview
-> choose existing bundle OR acquire/adapt tools/scripts into a new bundle
-> bounded execution plan
-> evidence summary
-> agent review routing
-> Hermes synthesis
-> next preview seed
-> repeat
-> report packet when report-ready
-> consolidate new/improved bundles
```

The operator should only be asked for gates Hermes should not handle:

- login/password handling;
- CAPTCHA / OTP / phone / email verification;
- sensitive browser/session handoff decisions;
- legal/scope clarifications only the operator can provide;
- final report-submission approval.

## Practical browser/session constraint

If Hermes cannot access the operator's already logged-in browser and credentials/tokens must not be shared, do not abandon ownership of the workflow. Instead:

1. Hermes gives exact, minimal operator-run observation steps.
2. Operator reports redacted paths, feature names, and yes/no observations only.
3. Hermes performs the analysis, surface-map normalization, preview, bundle choice/creation, review routing, and next-lane synthesis.
4. Durable artifacts must state the limitation and preserve no cookies/tokens/OTP/passwords.

This is still Hermes-owned: the operator is acting as a safe local sensor, not as the analyst.

## Single-account constraint

When a live target allows only one account because of phone-number or identity constraints:

- Defer two-account cross-account IDOR/object-ownership verification.
- Run a single-account surface-map lane first.
- Record owned object types and normal ID provenance.
- Separate read-only, self-owned write, and sensitive/high-risk flows.
- Produce a `needs_second_account` list for checks requiring negative control.
- Do not use unowned accounts, bought numbers, SMS receiving platforms, or opaque-ID guessing to compensate.

Single-account lane outputs:

```text
profile/member/my-page/cart/review/settings paths
owned object types
visible IDs and where they came from
read vs write operations
sensitive flows to avoid
bundle candidates
second-account dependency list
next preview seed
```

## Role split reminder

Default role split for this project remains:

```text
Hermes: previewer, coordinator, bundle router, final synthesis.
Claude Code / Cowork: nontrivial post-evidence review or implementation-heavy bundle work.
Operator: human-only auth gates and final submission decision.
```

If a future session says "agent preview" without naming an agent, Hermes owns it by default. Use Claude Code/Cowork for review or specialist preview only when it adds value.

## Pitfalls

1. **Handing the workflow back to the operator.** Asking the operator to browse is acceptable only as a credential-safe observation mechanism; Hermes must still decide what observations matter and what next step follows.
2. **Forcing IDOR with one account.** Without a second owned account, classify cross-account checks as `needs_second_account` rather than guessing IDs or using non-owned data.
3. **Overcorrecting into no testing.** Live-target safety should shape bounded surface mapping and bundle design, not freeze tactical exploration.
4. **Persisting secrets through convenience.** Never ask for or store password, OTP, cookie, CSRF token, phone number, full address, or raw sensitive profile data just to make automation easier.
