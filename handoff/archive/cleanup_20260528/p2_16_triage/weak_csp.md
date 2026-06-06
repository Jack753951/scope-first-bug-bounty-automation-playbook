> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# weak_csp

## security_headers_baseline.csp.unsafe_inline

Header: Content-Security-Policy. Severity hint: medium. References: OWASP Secure Headers Project, OWASP ASVS V14.4, CWE-693.

Remediation draft: Tighten the Content-Security-Policy header to remove the weak directive where the application design permits it. Review script loading patterns, migrate inline behavior to safer mechanisms, and manually verify browser enforcement before promoting this candidate.
