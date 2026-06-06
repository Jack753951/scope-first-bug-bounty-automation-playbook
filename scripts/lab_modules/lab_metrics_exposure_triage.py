#!/usr/bin/env python3
from web_exposure_common import main

CONFIG = {
    "bundle_id": "lab_metrics_exposure_triage",
    "description": "Bounded local-lab metrics / Prometheus exposure triage.",
    "owasp_mapping": [
        "A05:2021 Security Misconfiguration",
        "A09:2021 Security Logging and Monitoring Failures (contextual telemetry exposure)",
        "2025 migration track: exposed observability / misconfiguration leads",
    ],
    "cve_mapping": [],
    "probe_paths": [
        "/metrics",
        "/prometheus",
        "/stats/prometheus",
        "/actuator/prometheus",
        "/actuator/metrics",
    ],
    "keywords": ["# help", "# type", "prometheus", "process_", "nodejs_", "http_", "metrics"],
    "candidate_signal": "metrics_exposure_candidate",
    "oss_recon_decision": {
        "decision": "wrap/reference mature tools",
        "mature_tools": [
            {"name": "promtool", "repo": "prometheus/prometheus", "license": "Apache-2.0", "use": "offline syntax/format sanity for Prometheus text metrics"},
            {"name": "nuclei", "repo": "projectdiscovery/nuclei", "license": "MIT", "use": "allowlisted exposed metrics templates after scope gate"},
            {"name": "ffuf", "repo": "ffuf/ffuf", "license": "MIT", "use": "bounded metrics path discovery"},
            {"name": "OWASP ZAP", "repo": "zaproxy/zaproxy", "license": "Apache-2.0", "use": "passive metadata review"},
        ],
        "reason": "Metrics endpoints are usually safe to probe with GET, but impact depends on contents; keep candidate-only and redact raw bodies.",
    },
}

if __name__ == "__main__":
    raise SystemExit(main(CONFIG))
