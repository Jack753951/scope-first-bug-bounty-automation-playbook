> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# all_headers_absent

## security_headers_baseline.csp.missing

Header: Content-Security-Policy. Severity hint: medium. References: OWASP Secure Headers Project, OWASP ASVS V14.4, CWE-693.

Remediation draft: Add the Content-Security-Policy header using an application-approved policy. Review script, style, frame, and asset loading behavior before rollout, then manually verify the deployed response before reporting this candidate.

## security_headers_baseline.x_frame_options.missing

Header: X-Frame-Options. Severity hint: low. References: OWASP Secure Headers Project, OWASP ASVS V14.4, CWE-693.

Remediation draft: Add the X-Frame-Options header where legacy frame-control coverage is still required. Confirm the application does not rely on embedding behavior that would conflict with the selected baseline before reporting this candidate.

## security_headers_baseline.x_content_type_options.missing

Header: X-Content-Type-Options. Severity hint: low. References: OWASP Secure Headers Project, OWASP ASVS V14.4, CWE-693.

Remediation draft: Add the X-Content-Type-Options header to reduce browser content interpretation risk. Validate representative static and dynamic responses after deployment before promoting this candidate.

## security_headers_baseline.hsts.missing

Header: Strict-Transport-Security. Severity hint: medium. References: OWASP Secure Headers Project, OWASP ASVS V14.4, CWE-693.

Remediation draft: Add the Strict-Transport-Security header after confirming the service and dependent subdomains are ready for the transport baseline. Roll out carefully and manually verify response behavior before treating this as report-ready.

## security_headers_baseline.referrer_policy.missing

Header: Referrer-Policy. Severity hint: low. References: OWASP Secure Headers Project, OWASP ASVS V14.4, CWE-693.

Remediation draft: Add the Referrer-Policy header using the application-approved privacy baseline. Confirm analytics, federated login, and cross-origin workflows remain functional before reporting this candidate.
