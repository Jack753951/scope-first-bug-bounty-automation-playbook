#!/usr/bin/env python3
from tool_wrapper_common import main_for_spec

SPEC = {
    "slug": "lab_nmap_http_fingerprint",
    "owasp_classes": ["A05:2021 Security Misconfiguration"],
    "release_mapping": {
        "2017": ["A6:2017 Security Misconfiguration"],
        "2021": ["A05:2021 Security Misconfiguration"],
        "2025_migration_track": ["misconfiguration / HTTP header and service fingerprinting"],
    },
    "risk_lane": "active-tool-wrapper / service fingerprint",
    "tool": {
        "name": "nmap",
        "source": "Kali package / mature network mapper with HTTP NSE scripts",
        "license_note": "record distro package metadata during full tool inventory refresh",
    },
    "oss_recon_decision": {
        "decision": "wrap",
        "candidates_considered": ["nmap http-title/http-headers NSE", "httpx", "OWASP ZAP passive scan"],
        "reason": "nmap is installed on the Kali attacker VM and can provide bounded single-port HTTP fingerprint/header leads without crawling or credential use.",
    },
    "candidate_signals": ["HTTP script output reveals framework/server/header details worth manual misconfiguration review"],
    "control_signals": ["Service reachable/fingerprinted without actionable header/framework lead"],
    "missing_evidence_to_confirm": [
        "manual review of whether disclosed header/framework details are sensitive",
        "version/outdatedness confirmation from primary sources",
        "redacted evidence packet and report-readiness gate",
    ],
    "parser_signals": {
        "candidate": "nmap_http_fingerprint_candidate",
        "control": "nmap_http_fingerprint_control",
    },
}

if __name__ == "__main__":
    raise SystemExit(main_for_spec(SPEC))
