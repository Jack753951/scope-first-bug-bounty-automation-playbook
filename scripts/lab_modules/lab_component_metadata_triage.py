#!/usr/bin/env python3
from web_exposure_common import main

CONFIG = {
    "bundle_id": "lab_component_metadata_triage",
    "description": "Bounded local-lab vulnerable/outdated component metadata triage using static package/version clues.",
    "owasp_mapping": [
        "A06:2021 Vulnerable and Outdated Components",
        "A08:2021 Software and Data Integrity Failures (dependency provenance clues)",
        "2025 migration track: software supply-chain / component exposure leads",
    ],
    "cve_mapping": ["CVE candidates are not claimed from version strings alone; require primary-source/manual verification."],
    "probe_paths": [
        "/package.json",
        "/package-lock.json",
        "/npm-shrinkwrap.json",
        "/yarn.lock",
        "/bower.json",
        "/composer.json",
        "/assets/package.json",
        "/rest/admin/application-version",
    ],
    "keywords": ["dependencies", "devdependencies", "version", "package", "lockfileversion", "juice-shop", "angular", "express", "npm"],
    "candidate_signal": "component_metadata_exposure_candidate",
    "oss_recon_decision": {
        "decision": "wrap/reference mature dependency tools after artifact hygiene",
        "mature_tools": [
            {"name": "Retire.js", "repo": "RetireJS/retire.js", "license": "Apache-2.0", "use": "client-side JavaScript dependency/version CVE hinting on approved local artifacts"},
            {"name": "npm audit", "repo": "npm/cli", "license": "Artistic-2.0", "use": "offline/local package metadata review when manifest is legitimately available"},
            {"name": "OWASP Dependency-Check", "repo": "jeremylong/DependencyCheck", "license": "Apache-2.0", "use": "offline dependency/CVE correlation, not proof of exploitability"},
            {"name": "osv-scanner", "repo": "google/osv-scanner", "license": "Apache-2.0", "use": "offline advisory correlation for explicit package manifests"},
        ],
        "reason": "Version/package clues are candidate metadata only; mature tools help correlate advisories but do not prove reachability or impact.",
    },
}

if __name__ == "__main__":
    raise SystemExit(main(CONFIG))
