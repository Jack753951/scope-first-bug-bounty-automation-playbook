#!/usr/bin/env python3
from tool_wrapper_common import main_for_spec

SPEC = {
    "slug": "lab_nikto_server_misconfig",
    "owasp_classes": ["A05:2021 Security Misconfiguration"],
    "release_mapping": {
        "2017": ["A6:2017 Security Misconfiguration"],
        "2021": ["A05:2021 Security Misconfiguration"],
        "2025_migration_track": ["misconfiguration / server header and dangerous default file checks"],
    },
    "risk_lane": "active-tool-wrapper / scanner",
    "tool": {
        "name": "nikto",
        "source": "Kali package / mature web server scanner",
        "license_note": "record distro package metadata during full tool inventory refresh",
    },
    "oss_recon_decision": {
        "decision": "wrap",
        "candidates_considered": ["Nikto", "OWASP ZAP baseline", "nuclei http exposures templates"],
        "reason": "Nikto is installed on the Kali attacker VM and is useful for server/default-file misconfiguration leads when scoped to the disposable lab and parsed as candidate-only output.",
    },
    "candidate_signals": ["Nikto observation about server headers, unsafe default files, outdated components, or risky configuration"],
    "control_signals": ["Nikto completed with no parsed observations or only informational output"],
    "missing_evidence_to_confirm": [
        "manual validation of each Nikto message",
        "redacted reproduction for any reachable file/header issue",
        "impact analysis independent of scanner wording",
    ],
    "parser_signals": {
        "candidate": "nikto_server_misconfig_candidate",
        "control": "nikto_no_observation_control",
    },
}

if __name__ == "__main__":
    raise SystemExit(main_for_spec(SPEC))
