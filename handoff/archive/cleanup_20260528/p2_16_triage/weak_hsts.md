> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# weak_hsts

## security_headers_baseline.hsts.max_age_too_low

Header: Strict-Transport-Security. Severity hint: medium. References: OWASP Secure Headers Project, OWASP ASVS V14.4, CWE-693.

Remediation draft: Update the Strict-Transport-Security header to meet the approved duration baseline after confirming the service is consistently available over secure transport. Validate representative responses after deployment before treating this candidate as report-ready.

## security_headers_baseline.hsts.include_subdomains_missing

Header: Strict-Transport-Security. Severity hint: medium. References: OWASP Secure Headers Project, OWASP ASVS V14.4, CWE-693.

Remediation draft: Update the Strict-Transport-Security header to apply the approved subdomain baseline only after confirming dependent subdomains are compatible. Roll out with operational approval and manually verify response behavior before reporting.
