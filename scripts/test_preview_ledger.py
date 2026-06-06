import ast
import contextlib
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_preview_ledger.py"

spec = importlib.util.spec_from_file_location("validate_preview_ledger", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = validator
spec.loader.exec_module(validator)

RUN_ID = "20260516T020304Z_runner"


def utc(offset_seconds=0):
    value = datetime.now(timezone.utc).replace(microsecond=0) + timedelta(seconds=offset_seconds)
    return value.strftime("%Y-%m-%dT%H:%M:%SZ")


def json_bytes(payload):
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


class PreviewLedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.preview_dir = self.root / "runs" / RUN_ID / "preview"
        self.preview_dir.mkdir(parents=True)
        self.write_preview_bundle()
        self.ledger_path = self.root / "preview_ledger.json"
        self.ledger = self.write_valid_ledger()

    def tearDown(self):
        self.tmp.cleanup()

    def write_preview_bundle(self):
        artifacts = {
            "run.json": {
                "schema_version": "run/1.0",
                "run_id": RUN_ID,
                "created_at_utc": utc(-120),
            },
            "module_inputs.json": [],
            "module_results.json": [],
            "bundle_consistency.json": {
                "schema_version": "module_io_bundle_consistency/1.0",
                "document_type": "module_io_bundle",
                "verdict": "allow",
                "errors": [],
                "warnings": [],
                "error_codes": [],
                "warning_codes": [],
                "error_details": [],
            },
        }
        records = []
        for name, payload in artifacts.items():
            data = json_bytes(payload)
            (self.preview_dir / name).write_bytes(data)
            records.append({
                "name": name,
                "relative_path": f"runs/{RUN_ID}/preview/{name}",
                "sha256": sha256(data).hexdigest(),
                "size_bytes": len(data),
                "content_type": "application/json",
            })
        bundle_record = next(item for item in records if item["name"] == "bundle_consistency.json")
        manifest = {
            "schema_version": "preview_manifest/1.0",
            "run_id": RUN_ID,
            "created_at_utc": utc(-60),
            "producer": {
                "name": "module_runner",
                "version": "0.1.0",
            },
            "preview_mode": {
                "persist_preview_bundle": True,
                "include_module_io_preview": True,
                "dry_run": True,
            },
            "bundle_consistency": {
                "status": "ok",
                "verdict": "allow",
                "relative_path": f"runs/{RUN_ID}/preview/bundle_consistency.json",
                "sha256": bundle_record["sha256"],
            },
            "artifacts": records,
        }
        (self.preview_dir / "preview_manifest.json").write_bytes(json_bytes(manifest))

    def make_entry(self):
        manifest_data = (self.preview_dir / "preview_manifest.json").read_bytes()
        return {
            "run_id": RUN_ID,
            "preview_manifest_relative_path": f"runs/{RUN_ID}/preview/preview_manifest.json",
            "preview_manifest_sha256": sha256(manifest_data).hexdigest(),
            "preview_manifest_size_bytes": len(manifest_data),
            "schema_version_observed": "preview_manifest/1.0",
            "observed_at_utc": utc(-30),
        }

    def write_valid_ledger(self, entries=None):
        if entries is None:
            entries = [self.make_entry()]
        ledger = {
            "schema_version": "preview_ledger/1.0",
            "ledger_id": "ledger_20260518",
            "created_at_utc": utc(-10),
            "producer": {
                "name": "preview_ledger",
                "version": "0.1.0",
            },
            "entry_count": len(entries),
            "entries": entries,
        }
        self.write_ledger(ledger)
        return ledger

    def write_ledger(self, ledger):
        self.ledger_path.write_bytes(json_bytes(ledger))

    def validate(self):
        return validator.validate_preview_ledger(self.ledger_path, self.root)

    def assertDeniedWith(self, code):
        result = self.validate()
        self.assertEqual(result.verdict, "deny", result.as_dict())
        self.assertIn(code, result.as_dict()["error_codes"])

    def test_valid_fixture_passes(self):
        result = self.validate()
        self.assertEqual(result.verdict, "allow", result.as_dict())
        self.assertEqual(result.as_dict()["errors"], [])

    def test_committed_golden_fixture_passes(self):
        fixture = ROOT / "tests" / "fixtures" / "preview_ledger" / "1.0" / "valid_minimal"
        ledger = fixture / "preview_ledger.json"
        self.assertTrue(ledger.is_file(), ledger)
        result = validator.validate_preview_ledger(ledger, fixture)
        self.assertEqual(result.verdict, "allow", result.as_dict())

    def test_empty_entries_valid(self):
        ledger = deepcopy(self.ledger)
        ledger["entries"] = []
        ledger["entry_count"] = 0
        self.write_ledger(ledger)
        result = self.validate()
        self.assertEqual(result.verdict, "allow", result.as_dict())

    def test_missing_required_top_level_and_producer_fields_denied(self):
        for field in ("schema_version", "ledger_id", "created_at_utc", "producer", "entry_count", "entries"):
            with self.subTest(field=field):
                ledger = deepcopy(self.ledger)
                del ledger[field]
                self.write_ledger(ledger)
                self.assertDeniedWith("PREVIEW_LEDGER_REQUIRED_MISSING")

        for field in ("name", "version"):
            with self.subTest(field=field):
                ledger = deepcopy(self.ledger)
                del ledger["producer"][field]
                self.write_ledger(ledger)
                self.assertDeniedWith("PREVIEW_LEDGER_REQUIRED_MISSING")

    def test_unknown_fields_denied_at_all_object_levels(self):
        ledger = deepcopy(self.ledger)
        ledger["unexpected"] = True
        self.write_ledger(ledger)
        self.assertDeniedWith("PREVIEW_LEDGER_UNKNOWN_FIELD")

        ledger = deepcopy(self.ledger)
        ledger["producer"]["unexpected"] = True
        self.write_ledger(ledger)
        self.assertDeniedWith("PREVIEW_LEDGER_UNKNOWN_FIELD")

        ledger = deepcopy(self.ledger)
        ledger["entries"][0]["unexpected"] = True
        self.write_ledger(ledger)
        self.assertDeniedWith("PREVIEW_LEDGER_UNKNOWN_FIELD")

    def test_schema_version_drift_denied(self):
        for value in ("preview_ledger/1.0.0", "preview_ledger/1.1", "preview_ledger/2.0", 1):
            with self.subTest(value=value):
                ledger = deepcopy(self.ledger)
                ledger["schema_version"] = value
                self.write_ledger(ledger)
                self.assertDeniedWith("PREVIEW_LEDGER_SCHEMA_VERSION_INVALID")

    def test_entry_schema_version_observed_drift_denied(self):
        for value in ("preview_manifest/1.1", "preview_manifest/2.0", 1):
            with self.subTest(value=value):
                ledger = deepcopy(self.ledger)
                ledger["entries"][0]["schema_version_observed"] = value
                self.write_ledger(ledger)
                self.assertDeniedWith("PREVIEW_LEDGER_OBSERVED_SCHEMA_VERSION_INVALID")

        ledger = deepcopy(self.ledger)
        del ledger["entries"][0]["schema_version_observed"]
        self.write_ledger(ledger)
        self.assertDeniedWith("PREVIEW_LEDGER_REQUIRED_MISSING")

    def test_unsafe_ledger_id_and_run_id_denied(self):
        bad_values = ("../escape", "bad id", "", ".hidden", "aa..bb", "bad/path")
        for value in bad_values:
            with self.subTest(kind="ledger_id", value=value):
                ledger = deepcopy(self.ledger)
                ledger["ledger_id"] = value
                self.write_ledger(ledger)
                self.assertDeniedWith("PREVIEW_LEDGER_ID_INVALID")

        for value in bad_values:
            with self.subTest(kind="run_id", value=value):
                ledger = deepcopy(self.ledger)
                ledger["entries"][0]["run_id"] = value
                self.write_ledger(ledger)
                self.assertDeniedWith("PREVIEW_LEDGER_RUN_ID_INVALID")

    def test_unsafe_preview_manifest_relative_paths_denied(self):
        bad_paths = [
            f"runs/{RUN_ID}/../preview/preview_manifest.json",
            f"/runs/{RUN_ID}/preview/preview_manifest.json",
            f"runs\\{RUN_ID}\\preview\\preview_manifest.json",
            "C:/runs/run/preview/preview_manifest.json",
            f"runs//{RUN_ID}/preview/preview_manifest.json",
            f"runs/{RUN_ID}/./preview/preview_manifest.json",
            f"runs/other_run/preview/preview_manifest.json",
        ]
        for value in bad_paths:
            with self.subTest(value=value):
                ledger = deepcopy(self.ledger)
                ledger["entries"][0]["preview_manifest_relative_path"] = value
                self.write_ledger(ledger)
                self.assertDeniedWith("PREVIEW_LEDGER_PATH_INVALID")

    def test_duplicate_run_id_denied(self):
        entry = self.make_entry()
        self.write_valid_ledger(entries=[entry, deepcopy(entry)])
        result = self.validate()
        self.assertEqual(result.verdict, "deny", result.as_dict())
        self.assertIn("PREVIEW_LEDGER_DUPLICATE_RUN_ID", result.as_dict()["error_codes"])
        duplicate = next(error for error in result.as_dict()["errors"] if error["code"] == "PREVIEW_LEDGER_DUPLICATE_RUN_ID")
        self.assertIn("entries[0]", duplicate["expected"])
        self.assertIn("entries[1]", duplicate["observed"])

    def test_hash_size_and_missing_manifest_denied(self):
        ledger = deepcopy(self.ledger)
        ledger["entries"][0]["preview_manifest_sha256"] = "0" * 64
        self.write_ledger(ledger)
        self.assertDeniedWith("PREVIEW_LEDGER_HASH_MISMATCH")

        ledger = deepcopy(self.ledger)
        ledger["entries"][0]["preview_manifest_size_bytes"] += 1
        self.write_ledger(ledger)
        self.assertDeniedWith("PREVIEW_LEDGER_SIZE_MISMATCH")

        self.write_ledger(self.ledger)
        (self.preview_dir / "preview_manifest.json").unlink()
        self.assertDeniedWith("PREVIEW_LEDGER_PREVIEW_MANIFEST_MISSING")

    def test_symlinked_preview_manifest_denied_when_supported(self):
        real = self.preview_dir / "real_preview_manifest.json"
        real.write_bytes((self.preview_dir / "preview_manifest.json").read_bytes())
        (self.preview_dir / "preview_manifest.json").unlink()
        try:
            (self.preview_dir / "preview_manifest.json").symlink_to(real)
        except OSError as exc:
            self.skipTest(f"symlink creation unavailable: {exc}")
        self.assertDeniedWith("PREVIEW_LEDGER_SYMLINK_DENIED")

    def test_symlinked_preview_directory_denied_when_supported(self):
        real_preview = self.root / "real_preview"
        self.preview_dir.rename(real_preview)
        try:
            self.preview_dir.symlink_to(real_preview, target_is_directory=True)
        except OSError as exc:
            real_preview.rename(self.preview_dir)
            self.skipTest(f"symlink creation unavailable: {exc}")
        self.assertDeniedWith("PREVIEW_LEDGER_SYMLINK_DENIED")

    def test_symlinked_run_directory_denied_when_supported(self):
        run_dir = self.root / "runs" / RUN_ID
        real_run = self.root / "real_run"
        run_dir.rename(real_run)
        try:
            run_dir.symlink_to(real_run, target_is_directory=True)
        except OSError as exc:
            real_run.rename(run_dir)
            self.skipTest(f"symlink creation unavailable: {exc}")
        self.assertDeniedWith("PREVIEW_LEDGER_SYMLINK_DENIED")

    def test_symlinked_ledger_file_denied_when_supported(self):
        real = self.root / "real_preview_ledger.json"
        real.write_bytes(self.ledger_path.read_bytes())
        self.ledger_path.unlink()
        try:
            self.ledger_path.symlink_to(real)
        except OSError as exc:
            self.skipTest(f"symlink creation unavailable: {exc}")
        self.assertDeniedWith("PREVIEW_LEDGER_SYMLINK_DENIED")

    def test_timestamp_rules_denied(self):
        ledger = deepcopy(self.ledger)
        ledger["created_at_utc"] = utc(3600)
        self.write_ledger(ledger)
        self.assertDeniedWith("PREVIEW_LEDGER_TIMESTAMP_FUTURE")

        ledger = deepcopy(self.ledger)
        ledger["created_at_utc"] = datetime.now(timezone.utc).isoformat()
        self.write_ledger(ledger)
        self.assertDeniedWith("PREVIEW_LEDGER_TIMESTAMP_INVALID")

        ledger = deepcopy(self.ledger)
        ledger["entries"][0]["observed_at_utc"] = utc(3600)
        self.write_ledger(ledger)
        self.assertDeniedWith("PREVIEW_LEDGER_TIMESTAMP_FUTURE")

        ledger = deepcopy(self.ledger)
        ledger["created_at_utc"] = utc(-60)
        ledger["entries"][0]["observed_at_utc"] = utc(-30)
        self.write_ledger(ledger)
        self.assertDeniedWith("PREVIEW_LEDGER_TIMESTAMP_ORDER_INVALID")

    def test_entry_count_and_boolean_integer_rules_denied(self):
        ledger = deepcopy(self.ledger)
        ledger["entry_count"] = 2
        self.write_ledger(ledger)
        self.assertDeniedWith("PREVIEW_LEDGER_ENTRY_COUNT_MISMATCH")

        ledger = deepcopy(self.ledger)
        ledger["entry_count"] = True
        self.write_ledger(ledger)
        self.assertDeniedWith("PREVIEW_LEDGER_ENTRY_COUNT_INVALID")

        ledger = deepcopy(self.ledger)
        ledger["entries"][0]["preview_manifest_size_bytes"] = False
        self.write_ledger(ledger)
        self.assertDeniedWith("PREVIEW_LEDGER_SIZE_INVALID")

    def test_strict_json_parse_denials(self):
        self.ledger_path.write_text(
            '{"schema_version":"preview_ledger/1.0","schema_version":"preview_ledger/1.0"}',
            encoding="utf-8",
        )
        self.assertDeniedWith("PREVIEW_LEDGER_DUPLICATE_KEY")

        self.ledger_path.write_text('{"schema_version":"preview_ledger/1.0"} x', encoding="utf-8")
        self.assertDeniedWith("PREVIEW_LEDGER_JSON_INVALID")

        self.ledger_path.write_bytes(b"\xff\xfe\x00")
        self.assertDeniedWith("PREVIEW_LEDGER_JSON_INVALID")

    def test_notes_redaction_safety_denied(self):
        bad_notes = [
            "a" * 257,
            "path/to/file",
            "path\\to\\file",
            "contact@example.test",
            "http://example.test",
            "https://example.test",
            "host example.test",
            "ip 192.0.2.1",
        ]
        for note in bad_notes:
            with self.subTest(note=note[:20]):
                ledger = deepcopy(self.ledger)
                ledger["entries"][0]["notes"] = note
                self.write_ledger(ledger)
                self.assertDeniedWith("PREVIEW_LEDGER_NOTES_INVALID")

        ledger = deepcopy(self.ledger)
        ledger["entries"][0]["notes"] = "curated local preview bundle"
        self.write_ledger(ledger)
        self.assertEqual(self.validate().verdict, "allow")

    def test_validation_leaves_ledger_manifest_and_bundle_contents_unchanged(self):
        paths = [path for path in self.root.rglob("*") if path.is_file() and not path.is_symlink()]
        before = {path.relative_to(self.root).as_posix(): (path.read_bytes(), path.stat().st_mtime_ns) for path in paths}
        result = self.validate()
        self.assertEqual(result.verdict, "allow", result.as_dict())
        after = {
            path.relative_to(self.root).as_posix(): (path.read_bytes(), path.stat().st_mtime_ns)
            for path in paths
        }
        self.assertEqual(after, before)

    def test_static_imports_do_not_include_forbidden_modules(self):
        tree = ast.parse(VALIDATOR_PATH.read_text(encoding="utf-8"))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        self.assertFalse({"socket", "urllib", "http", "subprocess", "threading", "multiprocessing"} & imported)

    def test_cli_success_and_failure_json_shape(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code, payload = validator.main([str(self.ledger_path), "--repo-root", str(self.root), "--json"])
        self.assertEqual(code, 0, payload)
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(stdout.getvalue().count("\n"), 1)
        printed = json.loads(stdout.getvalue())
        self.assertEqual(printed["schema_version"], "preview_ledger_validation/1.0")
        self.assertEqual(printed["verdict"], "allow")

        ledger = deepcopy(self.ledger)
        ledger["schema_version"] = "bad"
        self.write_ledger(ledger)
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code, payload = validator.main([str(self.ledger_path), "--repo-root", str(self.root)])
        self.assertNotEqual(code, 0)
        printed = json.loads(stdout.getvalue())
        self.assertEqual(payload["verdict"], "deny")
        self.assertEqual(printed["verdict"], "deny")
        self.assertIn("error_codes", printed)


if __name__ == "__main__":
    unittest.main()
