# 06 — Evidence Redaction and Report Readiness

Status: public methodology

## Evidence minimization

Record enough to explain and reproduce the issue, but not enough to leak secrets,
customer data, tokens, cookies, private scope, or unnecessary raw responses.

Prefer:

- unique safe markers;
- status codes and key headers;
- short redacted snippets;
- screenshots with sensitive UI cropped or blurred;
- hashes of local marker files when useful;
- role/control tables;
- exact request counts and cleanup confirmation.

## Redaction checklist

- [ ] No API keys, passwords, tokens, cookies, OTPs, private keys, or session IDs.
- [ ] No customer/non-owned data.
- [ ] No private program scope/rules in public artifacts.
- [ ] No raw scan dumps unless explicitly sanitized.
- [ ] No local IPs, VM names, usernames, or host paths in public exports.
- [ ] No report-ready wording unless every gate passes.

## Report-ready gate

A candidate can become report-ready only when all are true:

```text
scope explicitly allows the test;
program policy does not exclude the issue;
impact crosses a meaningful security boundary;
proof used only authorized accounts/data/actions;
request volume was bounded and documented;
negative controls passed;
redactions are complete;
cleanup is complete or not required;
limitations are stated honestly;
human final-submit gate is cleared.
```

Otherwise keep `candidate` or `not_submit_reason`.
