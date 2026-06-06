#!/usr/bin/env python3
from single_vuln_module_common import main_for_spec

SPEC = {
    "slug": "lab_access_control_unauth_route_metadata",
    "owasp_classes": ["A01:2021 Broken Access Control"],
    "release_mapping": ["A05:2017 Broken Access Control", "2025 migration-track Broken Access Control"],
    "risk_lane": "active bounded metadata",
    "oss_recon_decision": {
        "tools_checked": ["OWASP ZAP", "Autorize", "AuthMatrix"],
        "decision": "write-custom",
        "reason": "Mature tools exist, but this wave intentionally avoids credentials/session replay/Burp workflows and broad scanning; fixed unauthenticated route metadata is safer for the local lab."
    },
    "probes": [
        {"path": "/rest/admin/application-configuration", "purpose": "unauthenticated admin/application configuration metadata", "signal": "unauthenticated_200_candidate"},
        {"path": "/api/Users", "purpose": "auth-gate control for user API", "signal": "auth_gate_control"},
        {"path": "/administration", "purpose": "SPA fallback false-positive control", "signal": "spa_fallback_control"}
    ],
    "candidate_signals": ["unauthenticated_200_candidate"],
    "control_signals": ["auth_gate_control", "spa_fallback_control"],
    "missing_evidence_to_confirm": ["intent/publicness check", "auth role comparison", "redacted sensitive-field review"]
}

if __name__ == "__main__":
    raise SystemExit(main_for_spec(SPEC))
