#!/usr/bin/env python3
"""Local-only reference grounding generator for live-bounty lane previews.

This script reads the live-bounty lane queue, selects the highest-priority lane,
validates the referenced lane state, and writes a markdown grounding packet for
safe preview/review. It never touches targets, launches browsers, runs scanners,
or executes probes.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
LANE_SCHEMA_PATH = ROOT / "schemas" / "live_bounty_lane_state.schema.json"
TARGET_TOUCHING_OPTIONS = {"--target", "--url", "--host", "--scope", "--live"}
EXIT_OK = 0
EXIT_INVALID = 30


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def resolve_path(path_value: str) -> Path:
    if os.name == "nt" and path_value.startswith("/c/"):
        return Path("C:/" + path_value[3:])
    if os.name == "nt" and path_value.startswith("/tmp/"):
        return Path(os.environ.get("TEMP", "C:/tmp")) / path_value[len("/tmp/"):]
    path = Path(path_value)
    if not path.is_absolute():
        path = ROOT / path
    return path


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_.-]+", "_", value.strip())
    return cleaned.strip("._-") or "lane"


def validate_doc(doc: Any, schema: dict, label: str) -> list[str]:
    validator = Draft202012Validator(schema)
    errors: list[str] = []
    for error in sorted(validator.iter_errors(doc), key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in error.path) or "<root>"
        errors.append(f"{label}:{where}: {error.message}")
    return errors


def validate_queue(queue: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(queue, dict):
        return ["queue:<root>: must be object"]
    if queue.get("schema_version") != "1.0":
        errors.append("queue:schema_version must be 1.0")
    lanes = queue.get("lanes")
    if not isinstance(lanes, list) or not lanes:
        errors.append("queue:lanes must be a non-empty list")
        return errors
    seen_priorities: set[int] = set()
    for idx, lane in enumerate(lanes):
        if not isinstance(lane, dict):
            errors.append(f"queue:lanes/{idx}: must be object")
            continue
        for field in ["program_slug", "lane_id", "state_file", "priority", "status"]:
            if field not in lane:
                errors.append(f"queue:lanes/{idx}: missing {field}")
        priority = lane.get("priority")
        if priority is not None:
            if not isinstance(priority, int):
                errors.append(f"queue:lanes/{idx}/priority: must be integer")
            elif priority in seen_priorities:
                errors.append(f"queue:lanes/{idx}/priority: duplicate priority {priority}")
            else:
                seen_priorities.add(priority)
        state_file = lane.get("state_file")
        if isinstance(state_file, str):
            candidate = resolve_path(state_file)
            if not candidate.exists():
                errors.append(f"queue:lanes/{idx}/state_file does not exist: {state_file}")
        elif "state_file" in lane:
            errors.append(f"queue:lanes/{idx}/state_file: must be string")
    return errors


def select_lane(queue: dict) -> dict:
    return sorted(queue["lanes"], key=lambda lane: lane["priority"])[0]


def has_target_touching_args(argv: list[str]) -> bool:
    return any(arg in TARGET_TOUCHING_OPTIONS or any(arg.startswith(opt + "=") for opt in TARGET_TOUCHING_OPTIONS) for arg in argv)


def option_value(argv: list[str], option: str) -> str | None:
    for idx, arg in enumerate(argv):
        if arg == option and idx + 1 < len(argv) and not argv[idx + 1].startswith("--"):
            return argv[idx + 1]
        prefix = option + "="
        if arg.startswith(prefix):
            return arg[len(prefix):]
    return None


def bullet_list(items: list[str], fallback: str = "none recorded") -> str:
    if not items:
        return f"- {fallback}\n"
    return "".join(f"- {item}\n" for item in items)


def lane_focus(lane_id: str, lane_title: str) -> str:
    text = f"{lane_id} {lane_title}".lower()
    if any(key in text for key in ["auth", "session", "login", "profile", "workspace"]):
        return "auth_session_profile_workspace"
    if any(key in text for key in ["idor", "bola", "ownership", "object"]):
        return "access_control_object_ownership"
    return "generic_owned_account_surface"


def methodology_for_focus(focus: str) -> list[str]:
    common = [
        "OWASP WSTG — use as reference-only methodology for safe manual test design, not as permission to run tools.",
        "OWASP ASVS — map controls and expected behavior for authentication, session, authorization, and data protection.",
        "PortSwigger Web Security Academy — use relevant labs as safe reference-only examples of evidence and controls.",
        "Public disclosed reports and official docs — compare evidence shapes, but do not copy payloads or aggressive techniques.",
        "Reference-only scanner/template metadata — read class descriptions and expected evidence; do not run scanner templates by default.",
    ]
    if focus == "auth_session_profile_workspace":
        return common + [
            "OWASP WSTG-ATHN/WSTG-SESS categories: login/logout, session lifecycle, account-state boundaries, and credential handling expectations.",
            "ASVS V2/V3/V4 controls: authentication, session management, and access-control expectations for owned accounts.",
        ]
    if focus == "access_control_object_ownership":
        return common + [
            "OWASP WSTG-ATHZ categories: horizontal/vertical authorization checks with legitimate object provenance.",
            "ASVS V4 controls: object-level authorization and deny-by-default behavior for Account A/B checks.",
        ]
    return common + [
        "OWASP WSTG information gathering and business-logic guidance for low-risk, owned-account mapping.",
    ]


def positive_controls(focus: str, state: dict) -> list[str]:
    controls = [
        "Use only operator-owned / program-authorized account labels such as Account A and Account B.",
        "Record normal UI/API provenance for any object identifier before making a claim.",
        "Keep request budget small and capture sanitized method/path/status summaries only.",
    ]
    if focus == "auth_session_profile_workspace":
        controls += [
            "Authenticated Account A can view its own profile/workspace empty state after normal login.",
            "Logout/session-expiry behavior returns the account to unauthenticated or login-required state without exposing owned data.",
        ]
    elif focus == "access_control_object_ownership":
        controls += [
            "Account A can access an object that Account A created or legitimately owns.",
            "Account B can access only Account B-owned objects through normal provenance.",
        ]
    else:
        controls += ["Owned account can navigate documented low-risk surfaces without state-changing side effects."]
    return controls


def negative_controls(focus: str, state: dict) -> list[str]:
    controls = [
        "Do not access non-owned data, tenant data, third-party identities, secrets, tokens, or PII.",
        "Do not use guessed opaque IDs; mark the lane blocked if normal provenance is unavailable.",
        "Stop on CAPTCHA, OTP, account warning, rate-limit/bot block, policy ambiguity, or unexpected third-party data.",
    ]
    if focus == "auth_session_profile_workspace":
        controls += [
            "Unauthenticated requests should not reveal Account A profile/workspace data.",
            "Session changes should not be forced, fuzzed, or brute-tested beyond normal UI behavior.",
        ]
    elif focus == "access_control_object_ownership":
        controls += [
            "Account B must not access Account A-owned object IDs unless explicitly authorized by the feature model.",
            "If a second owned account is unavailable, classify as `needs_second_account` instead of `no_finding`.",
        ]
    return controls


def evidence_thresholds(focus: str) -> list[str]:
    return [
        "`no_finding`: allowed lane exhausted with meaningful negative controls and no evidence of unauthorized access or impact.",
        "`candidate`: owned-account evidence suggests a security boundary may fail, but impact/controls/reproducibility still need review.",
        "`needs_manual_review`: evidence is ambiguous, policy-sensitive, or could become report_ready after human review.",
        "`blocked_operator_action`: auth/CAPTCHA/OTP/email/phone/local browser or legal/account gate prevents continuation.",
        "`report_ready`: only after scope, owned-data boundary, positive/negative controls, impact, redaction, duplicate/policy review, and Hermes synthesis all pass; never auto-submit.",
    ]


def render_markdown(state: dict, queue_entry: dict, *, date_value: str) -> str:
    program = state.get("program_slug", "unknown_program")
    lane = state.get("lane_id", "unknown_lane")
    title = state.get("lane_title", lane)
    focus = lane_focus(lane, title)
    auth = state.get("authorization", {})
    boundary = state.get("lane_boundary", {})
    learning = state.get("learning", {})
    artifacts = state.get("artifacts", {})
    allowed = boundary.get("allowed_actions", [])
    blocked = boundary.get("blocked_actions", [])
    operator_gates = state.get("operator_gates", [])
    stop_conditions = state.get("stop_conditions", [])
    preview_refs = learning.get("preview_references", [])

    lines: list[str] = []
    lines.append(f"# Live bounty preview grounding: {program} / {lane}\n")
    lines.append(f"Date: {date_value}\n")
    lines.append("Boundary: local reference generation only\n")
    lines.append("No target request, browser automation, scanner, fuzzer, DAST, callback, exploit, workflow execution, or report submission is authorized by this file.\n")
    lines.append("Do not treat this grounding packet as permission to touch the target. It is a preview/reference checklist for later authorized owned-account work.\n")
    lines.append("\n## Lane snapshot\n\n")
    lines.append(f"- Program: `{program}`\n")
    lines.append(f"- Lane: `{lane}`\n")
    lines.append(f"- Title: {title}\n")
    lines.append(f"- Current lane state: `{state.get('state')}`\n")
    lines.append(f"- Current lane status: `{state.get('status')}`\n")
    lines.append(f"- Autonomy level: `{state.get('autonomy_level')}`\n")
    lines.append(f"- Queue priority: `{queue_entry.get('priority')}`\n")
    lines.append(f"- Program URL: `{auth.get('program_url')}`\n")
    lines.append(f"- Scope file: `{auth.get('scope_file')}`\n")
    lines.append(f"- Dry-run gate: `{auth.get('dry_run_gate')}`\n")
    lines.append(f"- Out-of-scope control: `{auth.get('out_of_scope_control')}`\n")
    lines.append("\n## Reference methodology\n\n")
    lines.append(bullet_list(methodology_for_focus(focus)))
    if preview_refs:
        lines.append("\n## Lane-provided preview references\n\n")
        lines.append(bullet_list(preview_refs))
    lines.append("\n## Positive controls\n\n")
    lines.append(bullet_list(positive_controls(focus, state)))
    lines.append("\n## Negative controls\n\n")
    lines.append(bullet_list(negative_controls(focus, state)))
    lines.append("\n## Allowed actions from lane state\n\n")
    lines.append(bullet_list(allowed))
    lines.append("\n## Blocked techniques\n\n")
    lines.append(bullet_list(blocked + [
        "broad scanning",
        "credential brute force or password spraying",
        "payment/KYC/upload/run-script/integration/cross-tenant tests without separate approval",
    ]))
    lines.append("\n## Stop conditions\n\n")
    lines.append(bullet_list(stop_conditions))
    lines.append("\n## Evidence thresholds\n\n")
    lines.append(bullet_list(evidence_thresholds(focus)))
    lines.append("\n## Next safe local action\n\n")
    lines.append(f"- Next autonomous action after required gates: `{state.get('next_autonomous_action')}`\n")
    lines.append(f"- Next operator gate: `{state.get('next_operator_action')}`\n")
    if operator_gates:
        lines.append("- Operator gates still recorded:\n")
        lines.append("".join(f"  - {gate}\n" for gate in operator_gates))
    lines.append("\n## Artifact routing\n\n")
    lines.append(bullet_list([f"{key}: {value}" for key, value in artifacts.items()]))
    lines.append("\n## Classification guardrails\n\n")
    lines.append("- Use `surface_only`, `blocked_operator_action`, `needs_second_account`, `candidate`, `needs_manual_review`, `no_finding`, or `report_ready` only with the evidence thresholds above.\n")
    lines.append("- Do not use unreviewed promotional labels that imply verified/reportable status before review.\n")
    lines.append("- Redact tokens, cookies, emails, phone numbers, OTPs, and non-owned data before evidence promotion.\n")
    return "".join(lines)


def build_result(*, decision: str, exit_code: int, errors: list[str], output_path: str | None = None,
                 queue_path: str | None = None, queue_entry: dict | None = None, state: dict | None = None) -> dict:
    result: dict[str, Any] = {
        "schema_version": "1.0",
        "runner": "live-bounty-preview-grounding",
        "runner_mode": "local_reference_generation_only",
        "target_touching": False,
        "decision": decision,
        "exit_code": exit_code,
        "errors": errors,
        "queue_path": queue_path,
        "output_path": output_path,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }
    if queue_entry is not None:
        result["queue_entry"] = queue_entry
    if state is not None:
        result.update({
            "program_slug": state.get("program_slug"),
            "lane_id": state.get("lane_id"),
            "lane_title": state.get("lane_title"),
            "status": state.get("status"),
            "state": state.get("state"),
            "next_autonomous_action": state.get("next_autonomous_action"),
            "next_operator_action": state.get("next_operator_action"),
        })
    return result


def emit(result: dict, status_out: str | None) -> None:
    text = json.dumps(result, indent=2, ensure_ascii=False)
    print(text)
    if status_out:
        out = Path(status_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(description="Generate local-only live-bounty preview grounding markdown")
    parser.add_argument("--queue", required=True, help="Path to handoff/live_bounty_lane_queue.json")
    parser.add_argument("--output-dir", default="handoff/references", help="Directory for grounding markdown")
    parser.add_argument("--date", help="YYYY-MM-DD for deterministic output naming")
    parser.add_argument("--status-out", help="Optional path to write status JSON")
    parser.add_argument("--target")
    parser.add_argument("--url")
    parser.add_argument("--host")
    parser.add_argument("--scope")
    parser.add_argument("--live", action="store_true")

    if has_target_touching_args(argv):
        status_out = option_value(argv, "--status-out")
        result = build_result(
            decision="invalid_queue_or_state",
            exit_code=EXIT_INVALID,
            errors=["target-touching arguments are not supported by this local-only reference generator"],
            queue_path=option_value(argv, "--queue"),
        )
        emit(result, status_out)
        return EXIT_INVALID

    args = parser.parse_args(argv)
    try:
        queue = load_json(args.queue)
        errors = validate_queue(queue)
        if errors:
            result = build_result(decision="invalid_queue_or_state", exit_code=EXIT_INVALID, errors=errors, queue_path=args.queue)
            emit(result, args.status_out)
            return EXIT_INVALID
        queue_entry = select_lane(queue)
        state_path = resolve_path(queue_entry["state_file"])
        state = load_json(state_path)
        schema = load_json(LANE_SCHEMA_PATH)
        Draft202012Validator.check_schema(schema)
        errors = validate_doc(state, schema, "lane_state")
        if queue_entry.get("program_slug") != state.get("program_slug"):
            errors.append("queue/state program_slug mismatch")
        if queue_entry.get("lane_id") != state.get("lane_id"):
            errors.append("queue/state lane_id mismatch")
        if queue_entry.get("status") != state.get("status"):
            errors.append("queue/state status mismatch")
        if errors:
            result = build_result(
                decision="invalid_queue_or_state",
                exit_code=EXIT_INVALID,
                errors=errors,
                queue_path=args.queue,
                queue_entry=queue_entry,
                state=state if isinstance(state, dict) else None,
            )
            emit(result, args.status_out)
            return EXIT_INVALID

        date_value = args.date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
        date_slug = date_value.replace("-", "")
        out_dir = Path(args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        file_name = f"{slugify(state['program_slug'])}_{slugify(state['lane_id'])}_grounding_{date_slug}.md"
        output_path = out_dir / file_name
        output_path.write_text(render_markdown(state, queue_entry, date_value=date_value), encoding="utf-8")
        result = build_result(
            decision="grounding_written",
            exit_code=EXIT_OK,
            errors=[],
            output_path=str(output_path),
            queue_path=args.queue,
            queue_entry=queue_entry,
            state=state,
        )
        emit(result, args.status_out)
        return EXIT_OK
    except Exception as exc:  # pragma: no cover - defensive CLI boundary
        result = build_result(
            decision="invalid_queue_or_state",
            exit_code=EXIT_INVALID,
            errors=[f"{type(exc).__name__}: {exc}"],
            queue_path=args.queue if "args" in locals() else None,
        )
        emit(result, getattr(args, "status_out", None) if "args" in locals() else None)
        return EXIT_INVALID


if __name__ == "__main__":
    raise SystemExit(main())
