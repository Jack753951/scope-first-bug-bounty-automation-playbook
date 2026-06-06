#!/usr/bin/env python3
from web_exposure_common import main

CONFIG = {
    "bundle_id": "lab_auth_surface_no_bruteforce",
    "description": "Bounded local-lab authentication surface triage without brute force or credential attempts.",
    "owasp_mapping": [
        "A07:2021 Identification and Authentication Failures",
        "A01:2021 Broken Access Control (auth-gate metadata only)",
        "2025 migration track: authentication surface / access-control leads",
    ],
    "cve_mapping": [],
    "probe_paths": [
        "/login",
        "/#/login",
        "/rest/user/login",
        "/rest/user/whoami",
        "/api/Users",
        "/api/SecurityQuestions",
        "/rest/admin/application-configuration",
    ],
    "keywords": ["login", "password", "authentication", "authorization", "jwt", "token", "security question", "email"],
    "candidate_signal": "auth_surface_metadata_candidate",
    "oss_recon_decision": {
        "decision": "reference mature tools but do not automate brute force",
        "mature_tools": [
            {"name": "OWASP ZAP", "repo": "zaproxy/zaproxy", "license": "Apache-2.0", "use": "passive auth-surface and session-handling observation after scope gate"},
            {"name": "Burp Suite Community", "repo": "portswigger/burp-suite", "license": "proprietary/freeware", "use": "manual proxy verification only; no Intruder/brute force by default"},
            {"name": "ffuf", "repo": "ffuf/ffuf", "license": "MIT", "use": "tiny fixed auth path discovery only, not username/password fuzzing"},
            {"name": "hydra", "repo": "vanhauser-thc/thc-hydra", "license": "AGPL-3.0", "use": "explicitly excluded for this bundle; no real brute force"},
        ],
        "reason": "Authentication checks are useful, but this bundle only records unauthenticated surface metadata and access-control controls; no passwords, credential stuffing, or lockout testing.",
    },
}

if __name__ == "__main__":
    raise SystemExit(main(CONFIG))
