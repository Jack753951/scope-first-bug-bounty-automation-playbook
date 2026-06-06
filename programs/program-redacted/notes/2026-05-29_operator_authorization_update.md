> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Operator authorization update — bounded aggressive in-scope testing

Date: 2026-05-29

Operator clarified that in-scope testing is authorized with a stronger attacker posture: use the most likely high-value lane, aggressive scripts where useful, and retain only minimal safe evidence.

Execution constraints remain:
- In-scope sandbox assets only.
- Owned accounts/objects only.
- No internal/customer/non-owned data contact.
- No secrets/tokens/cookies/API keys/OTP/password/phone captured into artifacts.
- No destructive, resource-exhaustive, evasive, persistent, or final-submission action.
- Checkpoint before A4-class actions such as scanners/fuzzers/DAST/OAST/webhooks/OAuth/API-token/payment/KYC/integration flows.

Tactical correction:
- Prior behavior was too conservative after dashboard access.
- Continue with aggressive hypotheses, bounded execution.
- Primary lane remains Account B/team invite lifecycle + auth-role/API-UI mismatch checks.
