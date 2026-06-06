#!/usr/bin/env python3
"""Build operator inbox markdown from lane states and pending intake.

Reads:
- handoff/live_bounty_lane_queue.json (active lanes)
- programs/<slug>/lane_state.json (per queue entry)
- handoff/pending_intake.json (optional, candidates not yet lanes)
- intelligence/cve_briefs/cve_brief_*.md (latest, optional reference)

Writes:
- handoff/operator_inbox_<YYYYMMDD>.md (or --out path)

Boundary: this script produces a decision summary. It does not authorize
live target action. Hard stops live in /SAFETY.md.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "handoff" / "live_bounty_lane_queue.json"
PENDING_INTAKE = ROOT / "handoff" / "pending_intake.json"
CVE_DIR = ROOT / "intelligence" / "cve_briefs"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def latest_cve_brief() -> Path | None:
    if not CVE_DIR.exists():
        return None
    briefs = sorted(CVE_DIR.glob("cve_brief_*.md"))
    return briefs[-1] if briefs else None


def extract_deadline(next_auto: str) -> str | None:
    for token in ("PARK_EXPIRES_AT:", "park_expires_at:"):
        if token in next_auto:
            after = next_auto.split(token, 1)[1].strip()
            return after.split()[0].rstrip(".,;") if after else None
    return None


def lane_decision(lane_state: dict) -> dict:
    slug = lane_state["program_slug"]
    state = lane_state.get("machine_state") or lane_state.get("state")
    status = lane_state.get("status")
    next_operator = lane_state.get("next_operator_action", "")
    deadline = extract_deadline(lane_state.get("next_autonomous_action", ""))
    return {
        "kind": "lane",
        "slug": slug,
        "title": f"`{slug}` / {lane_state['lane_title']}",
        "state": state,
        "status": status,
        "deadline": deadline,
        "situation": next_operator
        or f"Lane `{slug}` is in state `{state}` ({status}); no next operator action recorded.",
        "options": [
            {
                "label": "EXECUTE_OPERATOR_GATE",
                "default": True,
                "description": next_operator
                or "Complete documented operator gate, then ping driver to record resulting state.",
            },
            {
                "label": "WAIT",
                "default": False,
                "description": f"Leave parked. Deadline {deadline or 'n/a'}; on miss recommend KILL.",
            },
            {
                "label": "KILL",
                "default": False,
                "description": "Close lane. Driver updates operator_decision to KILL and rebuilds inbox.",
            },
        ],
    }


def pending_decision(entry: dict) -> dict:
    slug = entry.get("slug") or entry.get("candidate_id") or "candidate"
    program = entry.get("program") or entry.get("title") or slug
    score = entry.get("score", {}).get("total_0_23") if isinstance(entry.get("score"), dict) else None
    status = entry.get("status", "pending")
    title = f"`{slug}` / {program}"
    situation_bits = []
    if score is not None:
        situation_bits.append(f"Score: {score}/23.")
    if entry.get("recommended_next_step"):
        situation_bits.append(str(entry["recommended_next_step"]))
    elif entry.get("recommended_action"):
        situation_bits.append(str(entry["recommended_action"]))
    if entry.get("blocked_before"):
        situation_bits.append("Blocked before: " + "; ".join(str(x) for x in entry.get("blocked_before", [])[:3]))
    options = entry.get("options") or [
        {
            "label": "KEEP_PASSIVE_TRIAGE",
            "default": True,
            "description": "Keep as candidate; gather only passive/public information or build an approval packet.",
        },
        {
            "label": "PROMOTE_AFTER_OPERATOR_APPROVAL",
            "default": False,
            "description": "Promote only after exact scope and lane-boundary approval.",
        },
        {
            "label": "PARK",
            "default": False,
            "description": "Park if freshness/bundle/operator-cost signal is weaker than current top lane.",
        },
    ]
    return {
        "kind": "pending",
        "title": title,
        "source": entry.get("source", ""),
        "status": status,
        "situation": " ".join(situation_bits),
        "options": options,
    }


def render_decision(idx: int, d: dict) -> list[str]:
    lines = [f"### {idx}. {d['title']}", ""]
    if d.get("kind") == "lane":
        lines.append(f"- State: `{d['state']}` ({d['status']})")
        lines.append(f"- park_expires_at: `{d.get('deadline') or 'n/a'}`")
    if d.get("source"):
        lines.append(f"- Source: {d['source']}")
    lines.append("")
    if d.get("situation"):
        lines.append(d["situation"])
        lines.append("")
    lines.append("Options:")
    for opt in d.get("options", []):
        label = opt.get("label", "?")
        marker = " **(default)**" if opt.get("default") else ""
        desc = opt.get("description", "")
        lines.append(f"- `{label}`{marker} — {desc}")
    lines.append("")
    return lines


def build_inbox(queue: dict, pending: dict | None, max_decisions: int, today_iso: str) -> tuple[list[str], list[tuple[str, str]]]:
    decisions: list[dict] = []
    closed: list[tuple[str, str]] = []

    for entry in queue.get("lanes", []):
        state_file = ROOT / entry["state_file"]
        if not state_file.exists():
            continue
        lane_state = load_json(state_file)
        if lane_state.get("operator_decision") == "KILL":
            closed.append((entry["program_slug"], lane_state.get("next_autonomous_action", "")[:200]))
            continue
        decisions.append(lane_decision(lane_state))

    if pending is not None:
        for cand in pending.get("candidates", []):
            decisions.append(pending_decision(cand))

    decisions = decisions[:max_decisions]

    lines = [
        f"# Operator Inbox — {today_iso[:4]}-{today_iso[4:6]}-{today_iso[6:]}",
        "",
        f"Generated by `scripts/build_operator_inbox.py` at {datetime.now(timezone.utc).isoformat(timespec='seconds')}.",
        "",
        "Boundary: this inbox lists decisions only. Hard stops in `/SAFETY.md`.",
        "",
        f"## Today's decisions ({len(decisions)})",
        "",
    ]
    if not decisions:
        lines.append(
            "_No active decisions. Update lane state or `handoff/pending_intake.json` and rerun._"
        )
        lines.append("")
    else:
        for i, d in enumerate(decisions, 1):
            lines.extend(render_decision(i, d))

    lines += ["## Active lane snapshot", "", "| Lane | State | Status | Deadline |", "|---|---|---|---|"]
    for entry in queue.get("lanes", []):
        state_file = ROOT / entry["state_file"]
        if not state_file.exists():
            continue
        s = load_json(state_file)
        deadline = extract_deadline(s.get("next_autonomous_action", "")) or "—"
        lines.append(
            f"| `{s['program_slug']}` | `{s.get('machine_state', '?')}` | {s.get('status', '?')} | {deadline} |"
        )
    lines.append("")

    if closed:
        lines += ["## Recently closed (KILL)", ""]
        for slug, reason in closed:
            lines.append(f"- `{slug}` — {reason}")
        lines.append("")

    brief = latest_cve_brief()
    if brief is not None:
        rel = brief.relative_to(ROOT).as_posix()
        lines += ["## Latest CVE brief", "", f"See `{rel}`.", ""]

    lines.append("Boundary: see `/SAFETY.md`. No live action authorized by this inbox.")
    return lines, closed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build operator inbox markdown")
    parser.add_argument("--out", help="Output path")
    parser.add_argument("--date", help="Override date (YYYYMMDD)")
    parser.add_argument("--max-decisions", type=int, default=5)
    args = parser.parse_args(argv)

    if not QUEUE.exists():
        print(f"ERROR: queue file missing: {QUEUE}", file=sys.stderr)
        return 1

    today_iso = args.date or datetime.now(timezone.utc).strftime("%Y%m%d")
    out_path = Path(args.out) if args.out else (ROOT / "handoff" / f"operator_inbox_{today_iso}.md")

    queue = load_json(QUEUE)
    pending = load_json(PENDING_INTAKE) if PENDING_INTAKE.exists() else None
    lines, _ = build_inbox(queue, pending, args.max_decisions, today_iso)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out_path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
