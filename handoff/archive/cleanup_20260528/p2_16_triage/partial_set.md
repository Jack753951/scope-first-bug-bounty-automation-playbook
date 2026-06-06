> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# partial_set

## security_headers_baseline.x_frame_options.missing

Header: X-Frame-Options. Severity hint: low. References: OWASP Secure Headers Project, OWASP ASVS V14.4, CWE-693.

Remediation draft: Add the X-Frame-Options header where legacy frame-control coverage is still required. Confirm the application does not rely on embedding behavior that would conflict with the selected baseline before reporting this candidate.

## security_headers_baseline.referrer_policy.missing

Header: Referrer-Policy. Severity hint: low. References: OWASP Secure Headers Project, OWASP ASVS V14.4, CWE-693.

Remediation draft: Add the Referrer-Policy header using the application-approved privacy baseline. Confirm analytics, federated login, and cross-origin workflows remain functional before reporting this candidate.
