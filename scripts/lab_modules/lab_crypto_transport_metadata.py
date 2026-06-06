#!/usr/bin/env python3
from single_vuln_module_common import main_for_spec

SPEC = {
    "slug": "lab_crypto_transport_metadata",
    "owasp_classes": ["A02:2021 Cryptographic Failures"],
    "release_mapping": ["A03:2017 Sensitive Data Exposure", "2025 migration-track Cryptographic Failures"],
    "risk_lane": "metadata only",
    "oss_recon_decision": {
        "tools_checked": ["testssl.sh", "SSLyze", "Mozilla HTTP Observatory"],
        "decision": "write-custom",
        "reason": "Mature TLS/HTTP observability tools exist, but the current lab target is plain HTTP; first module captures bounded transport/cookie metadata and defers TLS wrapper work."
    },
    "probes": [
        {"path": "/", "purpose": "transport and cookie metadata baseline", "signal": "crypto_transport_cookie_metadata"},
        {"path": "/rest/user/whoami", "purpose": "identity endpoint cookie/header metadata", "signal": "crypto_transport_cookie_metadata"},
        {"path": "/api/SecurityQuestions", "purpose": "security-question metadata context", "signal": "crypto_metadata_context"}
    ],
    "candidate_signals": [],
    "control_signals": ["crypto_transport_cookie_metadata", "crypto_metadata_context"],
    "missing_evidence_to_confirm": ["HTTPS/TLS scanner result if target supports TLS", "sensitive data proof", "cookie flag comparison with authenticated flow"]
}

if __name__ == "__main__":
    raise SystemExit(main_for_spec(SPEC))
