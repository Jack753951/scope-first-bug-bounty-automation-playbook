#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'USAGE'
Usage: scripts/post-proof-consolidation.sh --type <type> --artifact <path> [--dry-run]

Semi-automated post-proof consolidation checklist. It does not edit files by itself;
it prints the exact project indexes and validation gates Hermes must update after a
new proof, bundle, live surface map, report packet, or gate/tooling fix.

Valid types:
  local_lab_verified_proof
  local_lab_candidate
  attempted_not_verified
  live_surface_map
  live_candidate
  report_packet
  tooling_gate_fix
  bridge_or_decision_aid
  reference_only
USAGE
}

valid_type() {
    case "$1" in
        local_lab_verified_proof|local_lab_candidate|attempted_not_verified|live_surface_map|live_candidate|report_packet|tooling_gate_fix|bridge_or_decision_aid|reference_only)
            return 0
            ;;
        *) return 1 ;;
    esac
}

TYPE=""
ARTIFACT=""
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --type)
            [[ $# -ge 2 ]] || { echo "ERROR: --type requires a value" >&2; usage >&2; exit 2; }
            TYPE="$2"
            shift 2
            ;;
        --artifact)
            [[ $# -ge 2 ]] || { echo "ERROR: --artifact requires a path" >&2; usage >&2; exit 2; }
            ARTIFACT="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "ERROR: unknown argument: $1" >&2
            usage >&2
            exit 2
            ;;
    esac
done

[[ -n "$TYPE" ]] || { echo "ERROR: --type is required" >&2; usage >&2; exit 2; }
[[ -n "$ARTIFACT" ]] || { echo "ERROR: --artifact is required" >&2; usage >&2; exit 2; }
if ! valid_type "$TYPE"; then
    echo "ERROR: invalid type '$TYPE'; valid types are:" >&2
    usage >&2
    exit 2
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ARTIFACT_PATH="$ROOT/$ARTIFACT"
[[ -e "$ARTIFACT_PATH" ]] || { echo "ERROR: artifact not found: $ARTIFACT" >&2; exit 1; }

cat <<EOF
# Post-Proof Consolidation Checklist

Mode: $([[ "$DRY_RUN" == true ]] && echo dry-run || echo checklist)
Type: $TYPE
Artifact: $ARTIFACT

Required classification:
- Status: verified / candidate / attempted_not_verified / surface_only / needs_second_account / blocked / reference_only
- Report-readiness: report_ready / not_report_ready / guidance_only
- Safety boundary: local-only / authorized-live-manual / automation-blocked / sensitive-flow-blocked
- Artifact root: point to the durable handoff or <artifact-output-dir> path

Required updates:
- handoff/accepted_changes.md
- handoff/current_navigation.md
- handoff/live_bounty_lane_queue.json when lane routing/status changes
- handoff/pending_intake.json when candidate intake status changes
- programs/<slug>/notes/ or programs/<slug>/findings/ for durable program-local evidence summaries
- Obsidian Cybersec Lab namespace when strategy/rationale changes
EOF

case "$TYPE" in
    local_lab_verified_proof|local_lab_candidate|attempted_not_verified)
        cat <<'EOF'
- handoff/proof_library_index_20260523.md
- modules/bundles/ or module-specific bundle index when the method is reusable
EOF
        ;;
    live_surface_map|live_candidate|report_packet|bridge_or_decision_aid)
        cat <<'EOF'
- programs/<slug>/notes/ or programs/<slug>/findings/ should hold durable evidence summaries for active lanes
- archive/ paths are reference-only unless the operator explicitly restores a lane
EOF
        ;;
    tooling_gate_fix)
        cat <<'EOF'
- handoff/live_bounty_lane_queue.json / handoff/pending_intake.json if the gate affects live-bounty routing
- tests/ focused regression for fail-closed/pass-allowed behavior
EOF
        ;;
esac

cat <<'EOF'

Required metadata for reusable proof/bundle:
- Use when:
- Do not use when:
- Minimum evidence:
- Positive control:
- Negative control:
- Required accounts / roles:
- State-changing risk:
- Safe local runner:
- Artifact root:
- Live bounty prerequisites:
- Blocked live states:

Required validation commands:
- ./bin/hermes review
- git diff --check
- focused tests for changed scripts/tools

Required wrap-up fields:
- Benefit:
- Changes:
- Validation:
- Next safe action:

Hard boundaries:
- Do not auto-promote candidate/surface-only observations to verified/reportable.
- Do not authorize live targets, scans, cross-account testing, external callbacks, uploads, or report submission from this checklist.
- Do not store secrets, cookies, tokens, OTPs, phone numbers, emails, addresses, or raw loot.
EOF
