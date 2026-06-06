> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Live bounty target shortlist and parallel Hermes routing

Use this when the operator is temporarily blocked on an account prerequisite such as a second phone-verified account, but wants productive HackerOne work to continue.

## Target selection before a second account exists

When a two-account IDOR/BOLA lane is blocked, do not stop all work. Re-route to lanes that benefit from a single owned account and produce reusable prep artifacts:

1. Prefer auth/member boundary surfaces first:
   - login/session/logout/account recovery pages;
   - auth-required vs unauthenticated redirects/401/403;
   - session expiry and account-state behavior;
   - member/profile identifiers visible through normal UI.
2. Prefer self-owned account surfaces second:
   - profile/member/my-page/settings/cart/review/customer-service empty states;
   - object-type inventory and object-ID provenance from normal UI/API flows;
   - request/endpoint inventory for future A/B testing.
3. Treat review/cart/customer-service surfaces as future A/B seeds unless the operator can create harmless owned objects without payment/order/KYC/upload risk.
4. Defer payment, checkout, cash, KYC/AML, upload/video-upload, seller/partner/admin-like surfaces until explicit program guidance and a narrow benign plan exist.

Deliverable shape:

```text
program_slug:
selected_single_account_lane:
why it does not need Account B:
object types / endpoint seeds discovered:
what remains needs_second_account:
blocked high-risk surfaces:
next A/B matrix once Account B exists:
```

## Second phone/account guidance

If the operator can legally obtain another phone/SIM under their own name, it is a much cleaner path than SMS rental, VoIP-for-bypass, borrowed numbers, support bypass, or third-party accounts. Still treat it only as making Account B legally owned; it does not authorize high-risk testing by itself.

Two accounts are usually sufficient for first-pass IDOR/BOLA proof. A third account has lower marginal value and should require a clear model such as group/team/family/referral/multi-role behavior or a need to rule out a two-account anomaly.

## Parallel Hermes in one live-bounty repo

Parallel Hermes sessions are useful for read-only work, but only one lane should touch a live target at a time.

Safe parallel work:
- read-only program policy/scope comparison;
- target shortlist drafting;
- report template or evidence-packet drafting;
- local proof-library or bundle preparation;
- independent evidence review from sanitized artifacts.

Avoid parallel live execution or concurrent shared-file writes:
- one coordinator should own `config/scope.txt`, `programs/<slug>/scope.json`, rolling handoffs, and final live execution decisions;
- do not use `--no-lock` to let multiple workers write shared handoff/scope files unless the operator explicitly accepts merge/safety risk;
- keep each program in named artifacts such as `handoff/<program_slug>_surface_map_<date>.md` and `handoff/<program_slug>_phase5a_dry_run_packet_<date>.md`.

Recommended policy:

```text
one target-touching Hermes lane at a time;
multiple read-only Hermes/worker lanes allowed;
main Hermes is the scope/config/handoff coordinator;
workers write only named artifacts unless assigned otherwise.
```
