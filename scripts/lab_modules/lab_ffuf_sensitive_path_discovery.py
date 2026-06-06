#!/usr/bin/env python3
from tool_wrapper_common import main_for_spec

SPEC = {
    "slug": "lab_ffuf_sensitive_path_discovery",
    "owasp_classes": ["A05:2021 Security Misconfiguration"],
    "release_mapping": {
        "2017": ["A6:2017 Security Misconfiguration"],
        "2021": ["A05:2021 Security Misconfiguration"],
        "2025_migration_track": ["misconfiguration / exposed administrative or diagnostic path discovery"],
    },
    "risk_lane": "active-tool-wrapper / bounded fuzzer",
    "tool": {
        "name": "ffuf",
        "source": "Kali package / ProjectDiscovery-style web fuzzer alternative in local tool VM",
        "license_note": "record distro package metadata during full tool inventory refresh",
    },
    "oss_recon_decision": {
        "decision": "wrap",
        "candidates_considered": ["ffuf", "gobuster", "wfuzz", "OWASP ZAP spider"],
        "reason": "ffuf is installed on the Kali attacker VM and provides useful bounded path-discovery coverage when constrained to a tiny lab wordlist, rate cap, and candidate-only parser.",
    },
    "wordlist": [
        "admin",
        "administration",
        "rest/admin/application-configuration",
        "ftp",
        "backup",
        "debug",
        "metrics",
        "server-status",
        ".git/HEAD",
        "swagger.json",
        "api-docs",
        "robots.txt",
    ],
    "candidate_signals": ["HTTP 200/30x/401/403 discovered sensitive/admin/metadata path from bounded ffuf wordlist"],
    "control_signals": ["No parsed ffuf discoveries or only expected SPA/static routes"],
    "missing_evidence_to_confirm": [
        "manual intent/publicness check for discovered path",
        "authenticated versus unauthenticated comparison where relevant",
        "redacted evidence and impact review",
    ],
    "parser_signals": {
        "candidate": "ffuf_sensitive_path_candidate",
        "control": "ffuf_no_discovery_control",
    },
}

if __name__ == "__main__":
    raise SystemExit(main_for_spec(SPEC))
