#!/usr/bin/env python3
"""Phase 4A lab workflow runner (trial).

Turns the manually validated Phase 4A lab process into a deterministic,
deny-by-default workflow artifact:

scope gate -> baseline recon plan -> model-review prompt -> selected script plan
-> candidate packet -> gap report -> verification plan -> report-readiness gate
-> report draft plan.

This runner is deliberately plan-only in v0.1. It performs no target I/O, no
network calls, no subprocess launches, and no exploit execution. Lab execution
must remain a separate explicit operator-approved step until a later reviewed
slice adds an execution adapter.
"""

from __future__ import annotations

import importlib.util
import ipaddress
import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

SCHEMA_VERSION = "phase4a_lab_workflow/0.1-trial"
SOURCE_SCHEMA_VERSIONS = [
    "candidate_review_packet/0.1-trial",
    "candidate_review_gap_report/0.1-trial",
    "candidate_verification_plan/0.1-trial",
    "report_readiness_gate/0.1-trial",
]
STAGE_ORDER = [
    "scope_gate",
    "baseline_recon",
    "model_review_script_selection",
    "active_script_plan",
    "candidate_review_packet",
    "candidate_review_gap_report",
    "candidate_verification_plan",
    "report_readiness_gate",
    "lab_report_draft_plan",
]
INTENSITIES = {"baseline", "active", "max-lab"}


class WorkflowError:
    def __init__(self, code: str, path: str, message: str) -> None:
        self.code = code
        self.path = path
        self.message = message

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "path": self.path, "message": self.message}


def _compact_emit(payload: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    sys.stdout.write("\n")


def _empty_summary(input_count: int = 0) -> dict[str, int]:
    return {
        "input_count": input_count,
        "script_step_count": 0,
        "candidate_count": 0,
        "gap_finding_count": 0,
        "verification_plan_count": 0,
        "gate_result_count": 0,
        "blocked_count": 0,
        "needs_manual_review_count": 0,
    }


def _error_payload(errors: list[WorkflowError], input_count: int = 0) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "error",
        "run_mode": "plan_only",
        "source_schema_versions": SOURCE_SCHEMA_VERSIONS,
        "stage_order": STAGE_ORDER,
        "target": {},
        "summary": _empty_summary(input_count),
        "artifacts": {},
        "errors": [error.as_dict() for error in errors],
    }


def _load_script_module(filename: str, module_name: str) -> Any:
    target = Path(__file__).resolve().parent / filename
    existing = sys.modules.get(module_name)
    if existing is not None:
        return existing
    spec = importlib.util.spec_from_file_location(module_name, target)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"{filename} could not be located")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(module_name, None)
        raise
    return module


def _builder() -> Any:
    return _load_script_module("build_candidate_review_packet.py", "_phase4a_candidate_packet_builder")


def _gap_consumer() -> Any:
    return _load_script_module("review_candidate_packet_gaps.py", "_phase4a_gap_consumer")


def _planner() -> Any:
    return _load_script_module("build_candidate_verification_plan.py", "_phase4a_verification_planner")


def _gate() -> Any:
    return _load_script_module("build_report_readiness_gate.py", "_phase4a_report_readiness_gate")


def _is_local_lab_host(hostname: str) -> bool:
    lowered = hostname.lower().strip("[]")
    if lowered in {"localhost"} or lowered.endswith(".local") or lowered.endswith(".test"):
        return True
    try:
        ip = ipaddress.ip_address(lowered)
    except ValueError:
        return False
    return bool(ip.is_loopback or ip.is_private or ip.is_link_local)


def validate_target_url(target_url: str) -> tuple[dict[str, str], list[WorkflowError]]:
    parsed = urlparse(target_url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return {}, [WorkflowError("TARGET_URL_INVALID", "target_url", "target URL must be http(s) with a host")]
    if not _is_local_lab_host(parsed.hostname):
        return {}, [WorkflowError("TARGET_NOT_LOCAL_LAB", "target_url", "target host must be localhost, private RFC1918/link-local, .local, or .test")]
    return {
        "url": target_url.rstrip("/"),
        "scheme": parsed.scheme,
        "host": parsed.hostname,
        "port": str(parsed.port or (443 if parsed.scheme == "https" else 80)),
        "scope_class": "local_lab_only",
    }, []


def build_baseline_recon_plan(target: dict[str, str]) -> dict[str, Any]:
    url = target["url"]
    return {
        "status": "planned",
        "execution_default": "plan_only",
        "steps": [
            {"id": "curl_head", "tool": "curl", "command": f"curl -sS -I {url}", "risk": "low"},
            {"id": "whatweb", "tool": "whatweb", "command": f"whatweb {url}", "risk": "low"},
            {"id": "nmap_single_port", "tool": "nmap", "command": f"nmap -sV -Pn -p {target['port']} {target['host']}", "risk": "low"},
        ],
    }


def build_model_review_prompt(target: dict[str, str], intensity: str) -> dict[str, Any]:
    return {
        "status": "planned",
        "reviewer_route": "model_review_required_before_next_script_batch",
        "prompt_sections": [
            "authorized scope summary",
            "baseline recon observations",
            "false-positive risks",
            "candidate next-script choices",
            "explicit deny list",
            "required reportability decision",
        ],
        "decision_outputs": [
            "selected_scripts",
            "rejected_scripts_with_reason",
            "manual_verification_needed",
            "candidate_vs_false_positive_assessment",
        ],
        "target_url": target["url"],
        "intensity": intensity,
    }


def _step(step_id: str, tool: str, command: str, risk: str, purpose: str) -> dict[str, str]:
    return {"id": step_id, "tool": tool, "command": command, "risk": risk, "purpose": purpose}


def build_active_script_plan(target: dict[str, str], intensity: str) -> dict[str, Any]:
    url = target["url"]
    steps = []
    if intensity in {"active", "max-lab"}:
        steps.extend(
            [
                _step("headers_audit", "headers_audit.sh", f"./scripts/headers_audit.sh --yes -o <out>/headers {url}", "low", "browser security header triage"),
                _step("cors_audit", "cors_audit.sh", f"./scripts/cors_audit.sh --yes -o <out>/cors {url}", "low", "credentialed CORS triage"),
                _step("nikto_bounded", "nikto", f"nikto -h {url} -nointeractive -maxtime 2m -Tuning xb -output <out>/nikto.txt", "moderate", "bounded web-server baseline; triage only"),
                _step("ftp_metadata_only", "custom_verifier", f"GET {url}/ftp/ and record status/title/filenames only", "low", "metadata-only directory listing verification; no recursive download"),
            ]
        )
    if intensity == "max-lab":
        steps.extend(
            [
                _step("xss_marker_triage", "xss_finder.sh/manual", f"single-reflection marker checks against one known Juice Shop search/fragment interaction on {url}; no payload sweep", "moderate", "bounded XSS signal check with inert marker only"),
                _step("sqli_error_triage", "sqli_triage.sh/manual", f"single-endpoint SQL error triage against lab login/search surface on {url}; no database extraction", "moderate", "bounded SQLi signal check; no dump or shell"),
            ]
        )
    return {
        "status": "planned",
        "execution_default": "plan_only",
        "intensity": intensity,
        "safety_limits": [
            "local lab only",
            "no brute force",
            "no external callback",
            "no database extraction",
            "no OS shell",
            "no recursive download",
            "no promotion above candidate without human review",
        ],
        "steps": steps,
    }


def _stage_failed(stage: str, payload: Any) -> bool:
    return not isinstance(payload, dict) or payload.get("status") != "ok"


def _stage_error(stage: str, payload: Any) -> WorkflowError:
    if isinstance(payload, dict) and isinstance(payload.get("errors"), list) and payload["errors"]:
        first = payload["errors"][0]
        if isinstance(first, dict):
            code = first.get("code", "UNKNOWN_STAGE_ERROR")
            message = first.get("message", "stage failed")
            path = first.get("path", stage)
            return WorkflowError("WORKFLOW_STAGE_FAILED", str(path), f"{stage}: {code}: {message}")
    return WorkflowError("WORKFLOW_STAGE_FAILED", stage, f"{stage} failed closed")


def build_report_draft_plan(target: dict[str, str], gate_payload: dict[str, Any]) -> str:
    summary = gate_payload.get("summary", {}) if isinstance(gate_payload, dict) else {}
    return "\n".join(
        [
            "# Phase 4A Lab Report Draft Plan",
            "",
            f"Target: {target['url']}",
            "Classification: LAB ONLY / not for bug-bounty submission",
            "",
            "## Required sections",
            "- Executive summary",
            "- Scope and rules of engagement",
            "- Methodology",
            "- Detailed candidate findings",
            "- False positives and excluded observations",
            "- Report-readiness gate result",
            "- Next manual verification actions",
            "",
            "## Gate summary",
            f"- Findings: {summary.get('finding_count', 0)}",
            f"- Needs manual review: {summary.get('needs_manual_review_count', 0)}",
            f"- Blocked: {summary.get('blocked_count', 0)}",
            "",
            "No item may be submitted externally until a human records a verified finding decision.",
            "",
        ]
    )


def _summary(input_count: int, script_plan: dict[str, Any], artifacts: dict[str, Any]) -> dict[str, int]:
    packet = artifacts["candidate_review_packet"]
    gap = artifacts["candidate_review_gap_report"]
    plan = artifacts["candidate_verification_plan"]
    gate = artifacts["report_readiness_gate"]
    return {
        "input_count": input_count,
        "script_step_count": len(script_plan["steps"]),
        "candidate_count": packet["summary"]["candidate_count"],
        "gap_finding_count": gap["summary"]["finding_count"],
        "verification_plan_count": plan["summary"]["finding_count"],
        "gate_result_count": gate["summary"]["finding_count"],
        "blocked_count": gate["summary"]["blocked_count"],
        "needs_manual_review_count": gate["summary"]["needs_manual_review_count"],
    }


def build_lab_workflow(repo_root: str | Path, target_url: str, inputs: list[str], intensity: str = "active") -> dict[str, Any]:
    target, errors = validate_target_url(target_url)
    if errors:
        return _error_payload(errors, len(inputs))
    if intensity not in INTENSITIES:
        return _error_payload([WorkflowError("INTENSITY_UNSUPPORTED", "intensity", "intensity must be baseline, active, or max-lab")], len(inputs))

    artifacts: dict[str, Any] = {}
    artifacts["scope_gate"] = {"status": "allow", "scope_class": "local_lab_only", "target": target}
    artifacts["baseline_recon"] = build_baseline_recon_plan(target)
    artifacts["model_review_script_selection"] = build_model_review_prompt(target, intensity)
    artifacts["active_script_plan"] = build_active_script_plan(target, intensity)

    packet = _builder().build_packet(repo_root, inputs)
    artifacts["candidate_review_packet"] = packet
    if _stage_failed("candidate_review_packet", packet):
        return _error_payload([_stage_error("candidate_review_packet", packet)], len(inputs))

    gap = _gap_consumer().review_packet(packet)
    artifacts["candidate_review_gap_report"] = gap
    if _stage_failed("candidate_review_gap_report", gap):
        return _error_payload([_stage_error("candidate_review_gap_report", gap)], len(inputs))

    plan = _planner().build_plan(gap)
    artifacts["candidate_verification_plan"] = plan
    if _stage_failed("candidate_verification_plan", plan):
        return _error_payload([_stage_error("candidate_verification_plan", plan)], len(inputs))

    gate = _gate().build_gate(plan)
    artifacts["report_readiness_gate"] = gate
    if _stage_failed("report_readiness_gate", gate):
        return _error_payload([_stage_error("report_readiness_gate", gate)], len(inputs))

    artifacts["lab_report_draft_plan"] = build_report_draft_plan(target, gate)
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "ok",
        "run_mode": "plan_only",
        "source_schema_versions": SOURCE_SCHEMA_VERSIONS,
        "stage_order": STAGE_ORDER,
        "target": target,
        "summary": _summary(len(inputs), artifacts["active_script_plan"], artifacts),
        "artifacts": artifacts,
        "errors": [],
    }


def write_artifacts(output_dir: str | Path, payload: dict[str, Any]) -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "workflow.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    artifacts = payload.get("artifacts", {})
    mapping = {
        "script_plan.json": artifacts.get("active_script_plan"),
        "candidate_review_packet.json": artifacts.get("candidate_review_packet"),
        "candidate_gap_report.json": artifacts.get("candidate_review_gap_report"),
        "candidate_verification_plan.json": artifacts.get("candidate_verification_plan"),
        "report_readiness_gate.json": artifacts.get("report_readiness_gate"),
    }
    for filename, data in mapping.items():
        if data is not None:
            (out / filename).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_plan = artifacts.get("lab_report_draft_plan")
    if isinstance(report_plan, str):
        (out / "lab_report_draft_plan.md").write_text(report_plan, encoding="utf-8")


def _parse_args(argv: list[str]) -> tuple[list[WorkflowError], dict[str, Any]]:
    opts: dict[str, Any] = {"inputs": [], "intensity": "active", "lab_mode": False, "output_dir": None, "repo_root": None, "target_url": None}
    errors: list[WorkflowError] = []
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg == "--lab-mode":
            opts["lab_mode"] = True
            index += 1
            continue
        if arg == "--json":
            index += 1
            continue
        if arg in {"--repo-root", "--target-url", "--input", "--intensity", "--output-dir"}:
            if index + 1 >= len(argv) or argv[index + 1].startswith("--"):
                errors.append(WorkflowError("ARGUMENT_VALUE_MISSING", f"argv[{index}]", f"{arg} requires a following value"))
                index += 1
                continue
            value = argv[index + 1]
            if arg == "--input":
                opts["inputs"].append(value)
            else:
                opts[arg[2:].replace("-", "_")] = value
            index += 2
            continue
        errors.append(WorkflowError("ARGUMENT_NOT_ALLOWED", f"argv[{index}]", "unsupported argument"))
        index += 1
    if not opts["lab_mode"]:
        errors.append(WorkflowError("LAB_MODE_REQUIRED", "argv", "--lab-mode is required for Phase 4A lab workflow generation"))
    if not opts["repo_root"]:
        errors.append(WorkflowError("REQUIRED_ARGUMENT_MISSING", "argv", "--repo-root is required"))
    if not opts["target_url"]:
        errors.append(WorkflowError("REQUIRED_ARGUMENT_MISSING", "argv", "--target-url is required"))
    if not opts["inputs"]:
        errors.append(WorkflowError("REQUIRED_ARGUMENT_MISSING", "argv", "at least one --input is required"))
    if opts["intensity"] not in INTENSITIES:
        errors.append(WorkflowError("INTENSITY_UNSUPPORTED", "intensity", "intensity must be baseline, active, or max-lab"))
    return errors, opts


def main(argv: list[str] | None = None) -> tuple[int, dict[str, Any]]:
    args = list(sys.argv[1:] if argv is None else argv)
    errors, opts = _parse_args(args)
    if errors:
        payload = _error_payload(errors, len(opts.get("inputs", [])))
        _compact_emit(payload)
        return 2, payload
    payload = build_lab_workflow(opts["repo_root"], opts["target_url"], opts["inputs"], opts["intensity"])
    if opts.get("output_dir") and payload.get("status") == "ok":
        write_artifacts(opts["output_dir"], payload)
    _compact_emit(payload)
    return (0 if payload["status"] == "ok" else 2), payload


if __name__ == "__main__":
    raise SystemExit(main()[0])
