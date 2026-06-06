#!/usr/bin/env python3
from single_vuln_module_common import main_for_spec

SPEC = {
    "slug": "lab_exceptional_condition_metadata",
    "owasp_classes": ["A10:2025 Mishandling of Exceptional Conditions"],
    "release_mapping": ["2021 related context: Security Misconfiguration", "2021 related context: Security Logging and Monitoring Failures"],
    "risk_lane": "benign malformed/unknown route metadata",
    "oss_recon_decision": {
        "tools_checked": ["OWASP ZAP", "ffuf", "nuclei templates"],
        "decision": "write-custom",
        "reason": "Broad scanners/fuzzers exist, but this module uses only fixed benign routes with no crawler/fuzzer behavior and no destructive payloads."
    },
    "probes": [
        {"path": "/rest/products/search?q=%25", "purpose": "benign malformed percent query control", "signal": "stable_error_handling_control"},
        {"path": "/rest/products/search?q=%F0%9F%92%A9", "purpose": "benign unicode query control", "signal": "stable_error_handling_control"},
        {"path": "/rest/does-not-exist", "purpose": "unknown REST route error behavior", "signal": "server_error_candidate"}
    ],
    "candidate_signals": ["server_error_candidate"],
    "control_signals": ["stable_error_handling_control"],
    "missing_evidence_to_confirm": ["stable reproduction", "sensitive stack/framework detail check", "impact beyond cosmetic 500 response"]
}

if __name__ == "__main__":
    raise SystemExit(main_for_spec(SPEC))
