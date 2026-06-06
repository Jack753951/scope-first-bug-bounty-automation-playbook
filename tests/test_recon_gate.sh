#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_ROOT="$ROOT/tmp/test_recon_gate"
mkdir -p "$TMP_ROOT"

run_capture() {
    local name="$1"
    shift
    set +e
    "$@" >"$TMP_ROOT/${name}.out" 2>&1
    local status=$?
    set -e
    printf '%s' "$status" >"$TMP_ROOT/${name}.status"
    return 0
}

status_of() { cat "$TMP_ROOT/$1.status"; }
output_of() { cat "$TMP_ROOT/$1.out"; }

assert_status() {
    local name="$1" expected="$2" actual
    actual="$(status_of "$name")"
    if [[ "$actual" != "$expected" ]]; then
        echo "FAIL $name: expected status $expected got $actual" >&2
        output_of "$name" >&2
        exit 1
    fi
}

assert_output_contains() {
    local name="$1" needle="$2"
    if ! grep -Fq -- "$needle" "$TMP_ROOT/$name.out"; then
        echo "FAIL $name: expected output to contain: $needle" >&2
        output_of "$name" >&2
        exit 1
    fi
}

assert_output_not_contains() {
    local name="$1" needle="$2"
    if grep -Fq -- "$needle" "$TMP_ROOT/$name.out"; then
        echo "FAIL $name: expected output not to contain: $needle" >&2
        output_of "$name" >&2
        exit 1
    fi
}

rm -f "$TMP_ROOT"/*.out "$TMP_ROOT"/*.status 2>/dev/null || true

# Regression 1: existing program slug directory with underscore must be accepted.
run_capture braze_program_in_scope env HACKLAB="$ROOT" "$ROOT/recon.sh" --dry-run --program <program-slug> --policy-mode dry-run https://bug-bounty-dashboard.k8s.tools-001.d-use-1.<program-redacted>-dev.com/
assert_status braze_program_in_scope 0
assert_output_contains braze_program_in_scope "safe_target PASS context=initial_target"
assert_output_contains braze_program_in_scope "Program scope:"
assert_output_not_contains braze_program_in_scope "--program requires a slug matching"

# Regression 2: localhost is a valid local-lab scope entry and must not poison unrelated in-scope validation.
run_capture global_scope_localhost_ok env HACKLAB="$ROOT" "$ROOT/recon.sh" --dry-run https://bug-bounty-dashboard.k8s.tools-001.d-use-1.<program-redacted>-dev.com/
assert_status global_scope_localhost_ok 0
assert_output_contains global_scope_localhost_ok "safe_target PASS context=initial_target"
assert_output_not_contains global_scope_localhost_ok "unparseable scope entry"

# Regression 3: fail-closed still rejects out-of-scope targets after the compatibility fixes.
run_capture global_scope_out_of_scope env HACKLAB="$ROOT" "$ROOT/recon.sh" --dry-run https://example.org/
assert_status global_scope_out_of_scope 1
assert_output_contains global_scope_out_of_scope "safe_target FAIL context=initial_target"
assert_output_contains global_scope_out_of_scope "not in scope"

# Hardening 4: malformed or non-lowercase program slugs fail before any target processing.
run_capture program_slug_uppercase env HACKLAB="$ROOT" "$ROOT/recon.sh" --dry-run --program <program-slug> --policy-mode dry-run https://bug-bounty-dashboard.k8s.tools-001.d-use-1.<program-redacted>-dev.com/
assert_status program_slug_uppercase 2
assert_output_contains program_slug_uppercase "--program requires a lowercase slug"
assert_output_not_contains program_slug_uppercase "safe_target PASS"

# Hardening 5: path-like program slugs fail closed and cannot resolve outside programs/<slug>/scope.json.
run_capture program_slug_path_like env HACKLAB="$ROOT" "$ROOT/recon.sh" --dry-run --program ../<program-slug> --policy-mode dry-run https://bug-bounty-dashboard.k8s.tools-001.d-use-1.<program-redacted>-dev.com/
assert_status program_slug_path_like 2
assert_output_contains program_slug_path_like "--program requires a lowercase slug"
assert_output_not_contains program_slug_path_like "safe_target PASS"

# Hardening 6: --skip-scope-check cannot be combined with program policy mode.
run_capture skip_scope_with_program env HACKLAB="$ROOT" SCOPE_OVERRIDE_TOKEN=abc SCOPE_OVERRIDE_CONFIRM=abc "$ROOT/recon.sh" --skip-scope-check --program <program-slug> --policy-mode dry-run https://bug-bounty-dashboard.k8s.tools-001.d-use-1.<program-redacted>-dev.com/
assert_status skip_scope_with_program 2
assert_output_contains skip_scope_with_program "--program is incompatible with --skip-scope-check"
assert_output_not_contains skip_scope_with_program "DRY:"

# Hardening 7: policy dry-run mode must also set --dry-run.
run_capture policy_dry_run_without_dry_run env HACKLAB="$ROOT" "$ROOT/recon.sh" --program <program-slug> --policy-mode dry-run https://bug-bounty-dashboard.k8s.tools-001.d-use-1.<program-redacted>-dev.com/
assert_status policy_dry_run_without_dry_run 2
assert_output_contains policy_dry_run_without_dry_run "--policy-mode dry-run requires --dry-run"
assert_output_not_contains policy_dry_run_without_dry_run "safe_target PASS"

# Hardening 8: --policy-mode without --program is rejected.
run_capture policy_mode_without_program env HACKLAB="$ROOT" "$ROOT/recon.sh" --dry-run --policy-mode dry-run https://bug-bounty-dashboard.k8s.tools-001.d-use-1.<program-redacted>-dev.com/
assert_status policy_mode_without_program 2
assert_output_contains policy_mode_without_program "--policy-mode requires --program"
assert_output_not_contains policy_mode_without_program "safe_target PASS"

echo "PASS test_recon_gate"
