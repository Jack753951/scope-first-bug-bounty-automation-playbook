#!/usr/bin/env python3
from web_exposure_common import main

CONFIG = {
    "bundle_id": "lab_api_docs_exposure_triage",
    "description": "Bounded local-lab API documentation / OpenAPI exposure triage.",
    "owasp_mapping": [
        "A05:2021 Security Misconfiguration",
        "API9:2023 Improper Inventory Management",
        "2025 migration track: misconfiguration / exposed documentation leads",
    ],
    "cve_mapping": [],
    "probe_paths": [
        "/api-docs",
        "/api-docs/",
        "/swagger",
        "/swagger/",
        "/swagger-ui",
        "/swagger-ui/",
        "/swagger.json",
        "/openapi.json",
        "/api/swagger.json",
    ],
    "keywords": ["swagger", "openapi", "api-docs", "swagger-ui", "paths", "components"],
    "candidate_signal": "api_docs_exposure_candidate",
    "oss_recon_decision": {
        "decision": "wrap/reference mature tools",
        "mature_tools": [
            {"name": "OWASP ZAP", "repo": "zaproxy/zaproxy", "license": "Apache-2.0", "use": "OpenAPI import and passive API exposure review"},
            {"name": "nuclei", "repo": "projectdiscovery/nuclei", "license": "MIT", "use": "allowlisted exposure templates after scope gate"},
            {"name": "ffuf", "repo": "ffuf/ffuf", "license": "MIT", "use": "bounded API docs path discovery"},
            {"name": "dirsearch", "repo": "maurosoria/dirsearch", "license": "unknown from GitHub API", "use": "reference-only alternative path discovery"},
        ],
        "reason": "Use fixed low-impact docs paths first; mature tools can broaden coverage later under lab/scope gates.",
    },
}

if __name__ == "__main__":
    raise SystemExit(main(CONFIG))
