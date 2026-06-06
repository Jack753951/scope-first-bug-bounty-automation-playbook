#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_ROOT="$ROOT/tmp/test_post_proof_consolidation"
rm -rf "$TMP_ROOT"
mkdir -p "$TMP_ROOT"

SCRIPT="$ROOT/scripts/post-proof-consolidation.sh"

if [[ ! -x "$SCRIPT" ]]; then
    echo "FAIL: missing executable $SCRIPT" >&2
    exit 1
fi

set +e
"$SCRIPT" --type live_surface_map --artifact archive/cleanup_hermes_primary_20260528/programs/<program-slug>/notes/coupang_tw_pre_second_phone_single_account_auth_boundary_20260525.md --dry-run >"$TMP_ROOT/dry_run.out" 2>&1
status=$?
set -e
if [[ "$status" -ne 0 ]]; then
    echo "FAIL: dry-run should exit 0, got $status" >&2
    cat "$TMP_ROOT/dry_run.out" >&2
    exit 1
fi

for expected in \
    "handoff/accepted_changes.md" \
    "handoff/current_navigation.md" \
    "handoff/live_bounty_lane_queue.json" \
    "programs/<slug>/notes/ or programs/<slug>/findings/" \
    "Obsidian Cybersec Lab namespace" \
    "./bin/hermes review" \
    "git diff --check" \
    "Benefit:" \
    "Changes:" \
    "Validation:" \
    "Next safe action:"; do
    if ! grep -Fq -- "$expected" "$TMP_ROOT/dry_run.out"; then
        echo "FAIL: dry-run output missing checklist item: $expected" >&2
        cat "$TMP_ROOT/dry_run.out" >&2
        exit 1
    fi
done

set +e
"$SCRIPT" --type definitely_not_valid --artifact archive/cleanup_hermes_primary_20260528/programs/<program-slug>/notes/coupang_tw_pre_second_phone_single_account_auth_boundary_20260525.md --dry-run >"$TMP_ROOT/bad_type.out" 2>&1
bad_status=$?
set -e
if [[ "$bad_status" -eq 0 ]]; then
    echo "FAIL: invalid type should fail closed" >&2
    cat "$TMP_ROOT/bad_type.out" >&2
    exit 1
fi
if ! grep -Fq -- "valid types" "$TMP_ROOT/bad_type.out"; then
    echo "FAIL: invalid type should describe valid types" >&2
    cat "$TMP_ROOT/bad_type.out" >&2
    exit 1
fi

echo "PASS test_post_proof_consolidation"
