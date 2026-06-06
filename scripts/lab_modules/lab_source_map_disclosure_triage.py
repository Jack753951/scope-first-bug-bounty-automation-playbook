#!/usr/bin/env python3
from web_exposure_common import main

CONFIG = {
    "bundle_id": "lab_source_map_disclosure_triage",
    "description": "Bounded local-lab JavaScript source map disclosure triage.",
    "owasp_mapping": [
        "A05:2021 Security Misconfiguration",
        "A06:2021 Vulnerable and Outdated Components (client-side dependency clues)",
        "2025 migration track: client artifact / information exposure leads",
    ],
    "cve_mapping": [],
    "probe_paths": [
        "/main.js.map",
        "/runtime.js.map",
        "/vendor.js.map",
        "/polyfills.js.map",
    ],
    "keywords": ["version", "sources", "sourcescontent", "webpack", "mappings", "file"],
    "candidate_signal": "source_map_disclosure_candidate",
    "oss_recon_decision": {
        "decision": "wrap/reference mature tools",
        "mature_tools": [
            {"name": "Retire.js", "repo": "RetireJS/retire.js", "license": "Apache-2.0", "use": "client-side dependency/CVE hint review after asset inventory"},
            {"name": "SecretFinder", "repo": "m4ll0k/SecretFinder", "license": "GPL-3.0", "use": "reference-only; avoid retaining secrets/raw bodies by default"},
            {"name": "trufflehog", "repo": "trufflesecurity/trufflehog", "license": "AGPL-3.0", "use": "offline redacted secret pattern review only, not raw loot retention"},
            {"name": "LinkFinder", "repo": "GerbenJavado/LinkFinder", "license": "MIT-like/verify before vendoring", "use": "reference-only endpoint extraction from JS assets"},
        ],
        "reason": "First check whether source maps are exposed; deeper dependency/secret tooling requires redaction and offline artifact hygiene.",
    },
}

if __name__ == "__main__":
    raise SystemExit(main(CONFIG))
