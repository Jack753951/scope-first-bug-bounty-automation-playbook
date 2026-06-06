#!/usr/bin/env python3
from web_exposure_common import main

CONFIG = {
    "bundle_id": "lab_integrity_metadata_triage",
    "description": "Bounded local-lab software/data integrity metadata triage for security policy and client integrity clues.",
    "owasp_mapping": [
        "A08:2021 Software and Data Integrity Failures",
        "A05:2021 Security Misconfiguration",
        "2025 migration track: integrity / supply-chain metadata leads",
    ],
    "cve_mapping": [],
    "probe_paths": [
        "/.well-known/security.txt",
        "/security.txt",
        "/robots.txt",
        "/manifest.json",
        "/ngsw.json",
        "/service-worker.js",
        "/sw.js",
        "/integrity.json",
        "/.well-known/change-password",
    ],
    "keywords": ["security", "policy", "integrity", "sha", "script-src", "serviceworker", "ngsw", "contact", "disallow"],
    "candidate_signal": "integrity_metadata_candidate",
    "oss_recon_decision": {
        "decision": "reference browser/security-header and supply-chain tools; start with fixed metadata probes",
        "mature_tools": [
            {"name": "OWASP ZAP", "repo": "zaproxy/zaproxy", "license": "Apache-2.0", "use": "passive security-header and integrity-policy review"},
            {"name": "Mozilla Observatory", "repo": "mozilla/http-observatory", "license": "MPL-2.0", "use": "reference scoring model only; avoid public SaaS submission of lab/internal targets"},
            {"name": "retire.js", "repo": "RetireJS/retire.js", "license": "Apache-2.0", "use": "client dependency integrity/CVE hints after artifact hygiene"},
            {"name": "SRI Hash Generator/checkers", "repo": "various", "license": "varies", "use": "manual Subresource Integrity review; not automated proof"},
        ],
        "reason": "Integrity issues often require policy/context review; this bundle gathers only low-risk public metadata and flags manual checks.",
    },
}

if __name__ == "__main__":
    raise SystemExit(main(CONFIG))
