#!/usr/bin/env python3
"""Tests for scripts/lint_ctf_verifier_metadata.py.

P2.18 trial-only linter coverage. The expected behaviors come from
``handoff/cowork_p2_18_direction_review.md`` test cases 1-16.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "lint_ctf_verifier_metadata.py"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "ctf_verifier_metadata"

spec = importlib.util.spec_from_file_location("lint_ctf_verifier_metadata", SCRIPT)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# Also load ctf_review_decision and ctf_prepare_challenge for parity tests.
_REVIEW_SCRIPT = REPO_ROOT / "scripts" / "ctf_review_decision.py"
_review_spec = importlib.util.spec_from_file_location("ctf_review_decision", _REVIEW_SCRIPT)
assert _review_spec and _review_spec.loader
ctf_review_decision = importlib.util.module_from_spec(_review_spec)
_review_spec.loader.exec_module(ctf_review_decision)

_PREP_SCRIPT = REPO_ROOT / "scripts" / "ctf_prepare_challenge.py"
_prep_spec = importlib.util.spec_from_file_location("ctf_prepare_challenge", _PREP_SCRIPT)
assert _prep_spec and _prep_spec.loader
ctf_prepare_challenge = importlib.util.module_from_spec(_prep_spec)
_prep_spec.loader.exec_module(ctf_prepare_challenge)


VALID_SOURCE = """\
id: example-verifier
category: reverse
mode: offline
requires_scope: true
destructive: false
uses_external_service: false
oracle_required: false
kali_required: false
second_review_triggers:
  - abnormal_format
evidence_outputs:
  - raw_artifact
"""


def _codes(result: dict) -> list[str]:
    return [err["code"] for err in result["errors"]]


def _make_text(overrides: dict[str, str] | None = None, *, drop: tuple[str, ...] = ()) -> str:
    base = {
        "id": "example-verifier",
        "category": "reverse",
        "mode": "offline",
        "requires_scope": "true",
        "destructive": "false",
        "uses_external_service": "false",
        "oracle_required": "false",
        "kali_required": "false",
    }
    if overrides:
        base.update(overrides)
    for key in drop:
        base.pop(key, None)
    lines = [f"{k}: {v}" for k, v in base.items()]
    lines.append("second_review_triggers:")
    lines.append("  - abnormal_format")
    lines.append("evidence_outputs:")
    lines.append("  - raw_artifact")
    return "\n".join(lines) + "\n"


class HappyPathTests(unittest.TestCase):
    """Test 1: both committed fixtures lint clean."""

    def test_source_transform_inversion_passes(self) -> None:
        path = FIXTURES / "source_transform_inversion.yaml"
        result = mod.lint_file(path)
        self.assertEqual(result["status"], "ok", msg=result)
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["warnings"], [])

    def test_parser_validation_checksum_passes(self) -> None:
        path = FIXTURES / "parser_validation_checksum.yaml"
        result = mod.lint_file(path)
        self.assertEqual(result["status"], "ok", msg=result)
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["warnings"], [])

    def test_oracle_replay_kali_passes(self) -> None:
        """Test 3: optional active-service descriptor accepted with kali_required: true."""

        path = FIXTURES / "oracle_replay_kali.yaml"
        result = mod.lint_file(path)
        self.assertEqual(result["status"], "ok", msg=result)


class DestructiveTests(unittest.TestCase):
    """Test 2: destructive: true denied."""

    def test_destructive_true_denied(self) -> None:
        text = _make_text({"destructive": "true"})
        result = mod.lint_text(text)
        self.assertEqual(result["status"], "fail")
        self.assertIn("DESTRUCTIVE_NOT_ALLOWED", _codes(result))


class ActiveServiceKaliTests(unittest.TestCase):
    """Tests 4 & 5: active-service rules."""

    def test_active_service_without_kali_denied(self) -> None:
        text = _make_text(
            {
                "mode": "active-service",
                "uses_external_service": "true",
                "oracle_required": "true",
                "kali_required": "false",
            }
        )
        result = mod.lint_text(text)
        self.assertEqual(result["status"], "fail")
        self.assertIn("ACTIVE_SERVICE_REQUIRES_KALI", _codes(result))

    def test_active_service_missing_kali_field_denied(self) -> None:
        text = _make_text(
            {
                "mode": "active-service",
                "uses_external_service": "true",
                "oracle_required": "true",
            },
            drop=("kali_required",),
        )
        result = mod.lint_text(text)
        self.assertEqual(result["status"], "fail")
        self.assertIn("ACTIVE_SERVICE_REQUIRES_KALI", _codes(result))

    def test_uses_external_service_alone_requires_kali(self) -> None:
        text = _make_text({"uses_external_service": "true"})
        result = mod.lint_text(text)
        self.assertEqual(result["status"], "fail")
        self.assertIn("ACTIVE_SERVICE_REQUIRES_KALI", _codes(result))

    def test_uses_external_service_requires_scope_true(self) -> None:
        text = _make_text({"uses_external_service": "true", "kali_required": "true", "requires_scope": "false"})
        result = mod.lint_text(text)
        self.assertEqual(result["status"], "fail")
        self.assertIn("ACTIVE_SERVICE_REQUIRES_SCOPE", _codes(result))

    def test_oracle_required_alone_requires_kali(self) -> None:
        text = _make_text({"oracle_required": "true"})
        result = mod.lint_text(text)
        self.assertEqual(result["status"], "fail")
        self.assertIn("ACTIVE_SERVICE_REQUIRES_KALI", _codes(result))

    def test_oracle_required_requires_scope_true(self) -> None:
        text = _make_text({"oracle_required": "true", "kali_required": "true", "requires_scope": "false"})
        result = mod.lint_text(text)
        self.assertEqual(result["status"], "fail")
        self.assertIn("ACTIVE_SERVICE_REQUIRES_SCOPE", _codes(result))

    def test_active_service_requires_scope_true(self) -> None:
        text = _make_text(
            {
                "mode": "active-service",
                "requires_scope": "false",
                "uses_external_service": "true",
                "oracle_required": "true",
                "kali_required": "true",
            }
        )
        result = mod.lint_text(text)
        self.assertEqual(result["status"], "fail")
        self.assertIn("ACTIVE_SERVICE_REQUIRES_SCOPE", _codes(result))

    def test_active_service_host_execution_denied(self) -> None:
        text = _make_text(
            {
                "mode": "active-service",
                "uses_external_service": "true",
                "oracle_required": "true",
                "kali_required": "true",
            }
        )
        text = text + "command: /usr/bin/echo\n"
        result = mod.lint_text(text)
        self.assertEqual(result["status"], "fail")
        self.assertIn("HOST_EXECUTION_NOT_ALLOWED", _codes(result))

    def test_active_service_callback_url_denied(self) -> None:
        text = _make_text(
            {
                "mode": "active-service",
                "uses_external_service": "true",
                "oracle_required": "true",
                "kali_required": "true",
            }
        )
        text = text + "callback_url: example\n"
        result = mod.lint_text(text)
        self.assertIn("HOST_EXECUTION_NOT_ALLOWED", _codes(result))


class TriggerVocabularyTests(unittest.TestCase):
    """Test 6: unknown second_review_triggers value denied."""

    def test_unknown_trigger_denied(self) -> None:
        text = (
            "id: example-verifier\n"
            "category: reverse\n"
            "mode: offline\n"
            "requires_scope: true\n"
            "destructive: false\n"
            "uses_external_service: false\n"
            "oracle_required: false\n"
            "kali_required: false\n"
            "second_review_triggers:\n"
            "  - never_review\n"
            "evidence_outputs:\n"
            "  - raw_artifact\n"
        )
        result = mod.lint_text(text)
        self.assertEqual(result["status"], "fail")
        self.assertIn("UNKNOWN_TRIGGER", _codes(result))

    def test_allowed_triggers_match_review_decision(self) -> None:
        """The linter's ALLOWED_TRIGGERS must match the runtime decision helper."""

        self.assertEqual(
            tuple(sorted(mod.ALLOWED_TRIGGERS)),
            tuple(sorted(ctf_review_decision.ALLOWED_TRIGGERS)),
        )


class UnknownTopLevelFieldTests(unittest.TestCase):
    """Test 7: unknown top-level fields denied."""

    def test_benign_unknown_description_denied(self) -> None:
        text = _make_text() + "description: this should not be here\n"
        result = mod.lint_text(text)
        self.assertEqual(result["status"], "fail")
        self.assertIn("UNKNOWN_FIELD", _codes(result))

    def test_severity_leak_denied(self) -> None:
        text = _make_text() + "severity: high\n"
        result = mod.lint_text(text)
        self.assertEqual(result["status"], "fail")
        # severity is also in the forbidden vocabulary
        self.assertTrue(
            "FORBIDDEN_FIELD" in _codes(result) or "UNKNOWN_FIELD" in _codes(result),
            msg=_codes(result),
        )

    def test_target_url_leak_denied(self) -> None:
        text = _make_text() + "target_url: http://example.invalid\n"
        result = mod.lint_text(text)
        self.assertEqual(result["status"], "fail")
        self.assertTrue(
            "FORBIDDEN_FIELD" in _codes(result) or "UNKNOWN_FIELD" in _codes(result),
            msg=_codes(result),
        )


class BooleanTypeTests(unittest.TestCase):
    """Test 8: boolean-as-string denied."""

    def test_destructive_as_string_denied(self) -> None:
        text = _make_text({"destructive": '"false"'})
        result = mod.lint_text(text)
        self.assertEqual(result["status"], "fail")
        self.assertIn("BOOL_TYPE_MISMATCH", _codes(result))

    def test_each_boolean_field_must_be_bool(self) -> None:
        bool_fields = (
            "requires_scope",
            "destructive",
            "uses_external_service",
            "oracle_required",
            "kali_required",
        )
        for field in bool_fields:
            with self.subTest(field=field):
                text = _make_text({field: '"false"'})
                result = mod.lint_text(text)
                self.assertEqual(result["status"], "fail")
                self.assertIn("BOOL_TYPE_MISMATCH", _codes(result))


class ModeAndCategoryTests(unittest.TestCase):
    """Tests 9 & 10: mode / category vocabulary."""

    def test_invalid_mode_denied(self) -> None:
        text = _make_text({"mode": "live"})
        result = mod.lint_text(text)
        self.assertEqual(result["status"], "fail")
        self.assertIn("UNKNOWN_MODE", _codes(result))

    def test_invalid_category_denied(self) -> None:
        text = _make_text({"category": "unknown_class"})
        result = mod.lint_text(text)
        self.assertEqual(result["status"], "fail")
        self.assertIn("UNKNOWN_CATEGORY", _codes(result))

    def test_allowed_categories_match_prepare_challenge(self) -> None:
        self.assertEqual(
            tuple(sorted(mod.ALLOWED_CATEGORIES)),
            tuple(sorted(ctf_prepare_challenge.ALLOWED_CATEGORIES)),
        )

    def test_all_allowed_modes(self) -> None:
        for mode_value in mod.ALLOWED_MODES:
            with self.subTest(mode=mode_value):
                overrides = {"mode": mode_value}
                if mode_value == "active-service":
                    overrides["uses_external_service"] = "true"
                    overrides["kali_required"] = "true"
                text = _make_text(overrides)
                result = mod.lint_text(text)
                self.assertEqual(result["status"], "ok", msg=result)


class ForbiddenFieldTests(unittest.TestCase):
    """Test 11: each forbidden field, individually, denied."""

    def test_every_forbidden_field_denied(self) -> None:
        # Iterate the linter's vocabulary itself to keep the test in sync.
        for field in sorted(mod.FORBIDDEN_FIELDS):
            with self.subTest(field=field):
                text = _make_text() + f"{field}: nope\n"
                result = mod.lint_text(text)
                self.assertEqual(result["status"], "fail")
                codes = _codes(result)
                self.assertTrue(
                    "FORBIDDEN_FIELD" in codes or "HOST_EXECUTION_NOT_ALLOWED" in codes,
                    msg=(field, codes),
                )

    def test_forbidden_fields_is_documented_superset_of_override_field_names(self) -> None:
        """Trial linter's vocabulary must be a (possibly-larger) superset."""

        override = set(ctf_review_decision.OVERRIDE_FIELD_NAMES)
        # ``status`` is consumed by the review decision document itself and is
        # a known intentional gap: it is not a verifier descriptor field. The
        # trial linter does not need to redeclare it. Any other gap should
        # surface here so it can be documented.
        intentional_gap = {"status"}
        missing = override - set(mod.FORBIDDEN_FIELDS) - intentional_gap
        self.assertEqual(
            missing,
            set(),
            msg=(
                f"ctf_review_decision.OVERRIDE_FIELD_NAMES has fields not in "
                f"the trial linter vocabulary: {sorted(missing)}"
            ),
        )


class DeterminismTests(unittest.TestCase):
    """Tests 12 & 13: deterministic and idempotent output."""

    def test_repeated_lint_byte_identical(self) -> None:
        path = FIXTURES / "source_transform_inversion.yaml"
        first = mod._render(mod.lint_paths([str(path)]))
        second = mod._render(mod.lint_paths([str(path)]))
        self.assertEqual(first, second)

    def test_multi_file_run_matches_separate_runs(self) -> None:
        paths = [
            FIXTURES / "source_transform_inversion.yaml",
            FIXTURES / "parser_validation_checksum.yaml",
        ]
        joint = mod.lint_paths([str(p) for p in paths])
        separate_results = []
        for p in paths:
            separate = mod.lint_paths([str(p)])
            separate_results.extend(separate["results"])
        separate_results.sort(key=lambda r: r["file"])
        self.assertEqual(joint["results"], separate_results)


class MissingRequiredFieldTests(unittest.TestCase):
    """Test 14: missing required keys denied."""

    def test_each_required_field_missing(self) -> None:
        required = (
            "id",
            "category",
            "mode",
            "requires_scope",
            "destructive",
            "uses_external_service",
            "oracle_required",
            "second_review_triggers",
            "evidence_outputs",
        )
        for field in required:
            with self.subTest(field=field):
                if field in ("second_review_triggers", "evidence_outputs"):
                    base_text = _make_text()
                    if field == "second_review_triggers":
                        text = base_text.replace(
                            "second_review_triggers:\n  - abnormal_format\n", ""
                        )
                    else:
                        text = base_text.replace(
                            "evidence_outputs:\n  - raw_artifact\n", ""
                        )
                else:
                    text = _make_text(drop=(field,))
                result = mod.lint_text(text)
                self.assertEqual(result["status"], "fail", msg=(field, result))
                self.assertIn("MISSING_REQUIRED_FIELD", _codes(result))


class UnsafeYamlTests(unittest.TestCase):
    """Test 15: unsafe / object YAML rejected before any execution."""

    def test_python_object_tag_rejected(self) -> None:
        text = (
            'id: !!python/object/apply:os.system ["echo pwned"]\n'
            "category: reverse\n"
            "mode: offline\n"
            "requires_scope: true\n"
            "destructive: false\n"
            "uses_external_service: false\n"
            "oracle_required: false\n"
            "second_review_triggers:\n"
            "  - abnormal_format\n"
            "evidence_outputs:\n"
            "  - raw_artifact\n"
        )
        result = mod.lint_text(text)
        self.assertEqual(result["status"], "fail")
        self.assertIn("YAML_UNSAFE_SYNTAX", _codes(result))

    def test_anchor_rejected(self) -> None:
        text = _make_text() + "extra: &anchor value\n"
        result = mod.lint_text(text)
        self.assertEqual(result["status"], "fail")
        self.assertIn("YAML_UNSAFE_SYNTAX", _codes(result))

    def test_merge_key_rejected(self) -> None:
        text = _make_text() + "<<: othermap\n"
        result = mod.lint_text(text)
        self.assertEqual(result["status"], "fail")
        self.assertIn("YAML_UNSAFE_SYNTAX", _codes(result))

    def test_flow_mapping_rejected(self) -> None:
        text = "id: {a: 1}\n"
        result = mod.lint_text(text)
        self.assertEqual(result["status"], "fail")

    def test_flow_sequence_at_top_level_rejected(self) -> None:
        text = "[a, b, c]\n"
        result = mod.lint_text(text)
        self.assertEqual(result["status"], "fail")
        self.assertIn("YAML_UNSAFE_SYNTAX", _codes(result))


class SchemaPromotionNegativeTests(unittest.TestCase):
    """Test 16: no schema file is created and the trial banner is present."""

    def test_no_ctf_verifier_metadata_schema_file_exists(self) -> None:
        schema_dir = REPO_ROOT / "modules" / "_schema"
        if not schema_dir.exists():
            return
        offenders = [
            p.name
            for p in schema_dir.iterdir()
            if "ctf_verifier_metadata" in p.name.lower()
        ]
        self.assertEqual(
            offenders,
            [],
            msg=f"Schema promotion is deferred to P2.19+; found: {offenders}",
        )

    def test_linter_has_trial_only_banner(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("TRIAL ONLY", text)
        # Sanity: confirm the trial banner appears near the top of the file
        # (within the first 40 lines) so the reader sees it immediately.
        head = "\n".join(text.splitlines()[:40])
        self.assertIn("TRIAL ONLY", head)


class StaticSafetyTests(unittest.TestCase):
    """The linter must not import network/subprocess or runtime scanner paths."""

    def test_linter_does_not_import_unsafe_modules(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        forbidden_imports = (
            "import socket",
            "import http",
            "import urllib",
            "import requests",
            "import subprocess",
            "import asyncio",
            "import selectors",
            "from scripts.module_runner",
            "from scripts.program_policy_boundary",
            "from scripts.validate_module_io_bundle",
            "from scripts.validate_module_io_contract",
            "import scripts.module_runner",
            "import scripts.program_policy_boundary",
        )
        for needle in forbidden_imports:
            with self.subTest(needle=needle):
                self.assertNotIn(needle, text)


class CliTests(unittest.TestCase):
    """End-to-end CLI behavior: exit codes and JSON shape."""

    def test_cli_passes_on_valid_fixtures(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--input",
                str(FIXTURES / "source_transform_inversion.yaml"),
                "--input",
                str(FIXTURES / "parser_validation_checksum.yaml"),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            completed.returncode,
            0,
            msg=(completed.returncode, completed.stdout, completed.stderr),
        )
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["status"], "ok")

    def test_cli_fails_on_destructive_descriptor(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            bad = Path(td) / "bad.yaml"
            bad.write_text(_make_text({"destructive": "true"}), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), "--input", str(bad)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(completed.returncode, 0)
            payload = json.loads(completed.stdout)
            self.assertEqual(payload["status"], "fail")

    def test_cli_rejects_output_argument_and_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "report.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--input",
                    str(FIXTURES / "source_transform_inversion.yaml"),
                    "--output",
                    str(out),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertFalse(out.exists())
            self.assertIn("unrecognized arguments", completed.stderr)


if __name__ == "__main__":
    unittest.main()
