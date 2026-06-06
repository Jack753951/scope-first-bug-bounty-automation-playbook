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
VALIDATOR_PATH = ROOT / "scripts" / "validate_preview_manifest.py"

spec = importlib.util.spec_from_file_location("validate_preview_manifest", VALIDATOR_PATH)
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


class PreviewManifestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.preview_dir = self.root / "runs" / RUN_ID / "preview"
        self.preview_dir.mkdir(parents=True)
        self.manifest = self.write_valid_bundle()

    def tearDown(self):
        self.tmp.cleanup()

    def write_valid_bundle(self):
        run = {
            "schema_version": "run/1.0",
            "run_id": RUN_ID,
            "created_at_utc": utc(-60),
        }
        inputs = []
        results = []
        consistency = {
            "schema_version": "module_io_bundle_consistency/1.0",
            "document_type": "module_io_bundle",
            "verdict": "allow",
            "errors": [],
            "warnings": [],
            "error_codes": [],
            "warning_codes": [],
            "error_details": [],
        }
        artifacts = []
        for name, payload in {
            "run.json": run,
            "module_inputs.json": inputs,
            "module_results.json": results,
            "bundle_consistency.json": consistency,
        }.items():
            data = json_bytes(payload)
            (self.preview_dir / name).write_bytes(data)
            artifacts.append({
                "name": name,
                "relative_path": f"runs/{RUN_ID}/preview/{name}",
                "sha256": sha256(data).hexdigest(),
                "size_bytes": len(data),
                "content_type": "application/json",
            })
        bundle_record = next(item for item in artifacts if item["name"] == "bundle_consistency.json")
        manifest = {
            "schema_version": "preview_manifest/1.0",
            "run_id": RUN_ID,
            "created_at_utc": utc(),
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
            "artifacts": artifacts,
        }
        self.write_manifest(manifest)
        return manifest

    def write_manifest(self, manifest):
        (self.preview_dir / "preview_manifest.json").write_bytes(json_bytes(manifest))

    def validate(self):
        return validator.validate_preview_bundle(self.preview_dir)

    def assertDeniedWith(self, code):
        result = self.validate()
        self.assertEqual(result.verdict, "deny", result.as_dict())
        self.assertIn(code, result.as_dict()["error_codes"])

    def test_valid_fixture_passes(self):
        result = self.validate()
        self.assertEqual(result.verdict, "allow", result.as_dict())
        self.assertEqual(result.as_dict()["errors"], [])

    def test_committed_golden_fixture_passes(self):
        fixture = ROOT / "tests" / "fixtures" / "preview_manifest" / "1.0" / "valid_minimal" / "runs" / RUN_ID / "preview"
        self.assertTrue(fixture.is_dir(), fixture)
        result = validator.validate_preview_bundle(fixture)
        self.assertEqual(result.verdict, "allow", result.as_dict())

    def test_missing_required_field_denied(self):
        manifest = deepcopy(self.manifest)
        del manifest["producer"]
        self.write_manifest(manifest)
        self.assertDeniedWith("PREVIEW_MANIFEST_REQUIRED_MISSING")

    def test_unknown_top_level_and_nested_fields_denied(self):
        manifest = deepcopy(self.manifest)
        manifest["unexpected"] = True
        self.write_manifest(manifest)
        self.assertDeniedWith("PREVIEW_MANIFEST_UNKNOWN_FIELD")

        manifest = deepcopy(self.manifest)
        manifest["producer"]["extra"] = True
        self.write_manifest(manifest)
        self.assertDeniedWith("PREVIEW_MANIFEST_UNKNOWN_FIELD")

    def test_bad_schema_version_denied(self):
        for value in ("preview_manifest/1.0.0", "preview_manifest/1.1", "preview_manifest/2.0"):
            with self.subTest(value=value):
                manifest = deepcopy(self.manifest)
                manifest["schema_version"] = value
                self.write_manifest(manifest)
                self.assertDeniedWith("PREVIEW_MANIFEST_SCHEMA_VERSION_INVALID")

    def test_unsafe_run_id_denied(self):
        for value in ("../escape", "bad run", "", "aa..bb", "C:drive"):
            with self.subTest(value=value):
                manifest = deepcopy(self.manifest)
                manifest["run_id"] = value
                self.write_manifest(manifest)
                self.assertDeniedWith("PREVIEW_MANIFEST_RUN_ID_INVALID")

    def test_missing_extra_or_self_artifact_denied(self):
        manifest = deepcopy(self.manifest)
        manifest["artifacts"] = [item for item in manifest["artifacts"] if item["name"] != "run.json"]
        self.write_manifest(manifest)
        self.assertDeniedWith("PREVIEW_MANIFEST_ARTIFACT_MISSING")

        manifest = deepcopy(self.manifest)
        extra = deepcopy(manifest["artifacts"][0])
        extra["name"] = "extra.json"
        extra["relative_path"] = f"runs/{RUN_ID}/preview/extra.json"
        manifest["artifacts"].append(extra)
        self.write_manifest(manifest)
        self.assertDeniedWith("PREVIEW_MANIFEST_ARTIFACT_NAME_INVALID")

        manifest = deepcopy(self.manifest)
        manifest["artifacts"][0]["name"] = "preview_manifest.json"
        manifest["artifacts"][0]["relative_path"] = f"runs/{RUN_ID}/preview/preview_manifest.json"
        self.write_manifest(manifest)
        self.assertDeniedWith("PREVIEW_MANIFEST_SELF_LISTED")

    def test_unsafe_relative_paths_denied(self):
        bad_paths = [
            "../run.json",
            f"/runs/{RUN_ID}/preview/run.json",
            f"runs\\{RUN_ID}\\preview\\run.json",
            "C:/runs/run.json",
            f"runs//{RUN_ID}/preview/run.json",
            f"runs/{RUN_ID}/./preview/run.json",
        ]
        for value in bad_paths:
            with self.subTest(value=value):
                manifest = deepcopy(self.manifest)
                manifest["artifacts"][0]["relative_path"] = value
                self.write_manifest(manifest)
                self.assertDeniedWith("PREVIEW_MANIFEST_PATH_INVALID")

    def test_symlink_artifact_denied_when_supported(self):
        real = self.preview_dir / "real_run.json"
        real.write_bytes((self.preview_dir / "run.json").read_bytes())
        (self.preview_dir / "run.json").unlink()
        try:
            (self.preview_dir / "run.json").symlink_to(real)
        except OSError as exc:
            self.skipTest(f"symlink creation unavailable: {exc}")
        self.assertDeniedWith("PREVIEW_MANIFEST_SYMLINK_DENIED")

    def test_hash_and_size_mismatch_denied(self):
        (self.preview_dir / "run.json").write_text('{"tampered":true}\n', encoding="utf-8")
        self.assertDeniedWith("PREVIEW_MANIFEST_HASH_MISMATCH")

        self.manifest = self.write_valid_bundle()
        manifest = deepcopy(self.manifest)
        manifest["artifacts"][0]["size_bytes"] += 1
        self.write_manifest(manifest)
        self.assertDeniedWith("PREVIEW_MANIFEST_SIZE_MISMATCH")

    def test_bundle_consistency_status_or_digest_mismatch_denied(self):
        bad = {
            "schema_version": "module_io_bundle_consistency/1.0",
            "status": "bad",
            "verdict": "allow",
        }
        data = json_bytes(bad)
        (self.preview_dir / "bundle_consistency.json").write_bytes(data)
        manifest = deepcopy(self.manifest)
        record = next(item for item in manifest["artifacts"] if item["name"] == "bundle_consistency.json")
        record["sha256"] = sha256(data).hexdigest()
        record["size_bytes"] = len(data)
        manifest["bundle_consistency"]["sha256"] = record["sha256"]
        self.write_manifest(manifest)
        self.assertDeniedWith("PREVIEW_MANIFEST_BUNDLE_STATUS_INVALID")

        self.manifest = self.write_valid_bundle()
        manifest = deepcopy(self.manifest)
        manifest["bundle_consistency"]["sha256"] = "0" * 64
        self.write_manifest(manifest)
        self.assertDeniedWith("PREVIEW_MANIFEST_BUNDLE_HASH_MISMATCH")

    def test_timestamp_future_or_before_run_start_denied(self):
        manifest = deepcopy(self.manifest)
        manifest["created_at_utc"] = utc(3600)
        self.write_manifest(manifest)
        self.assertDeniedWith("PREVIEW_MANIFEST_TIMESTAMP_FUTURE")

        self.manifest = self.write_valid_bundle()
        manifest = deepcopy(self.manifest)
        manifest["created_at_utc"] = datetime.now(timezone.utc).isoformat()
        self.write_manifest(manifest)
        self.assertDeniedWith("PREVIEW_MANIFEST_TIMESTAMP_INVALID")

        self.manifest = self.write_valid_bundle()
        run = json.loads((self.preview_dir / "run.json").read_text(encoding="utf-8"))
        run["created_at_utc"] = utc(60)
        data = json_bytes(run)
        (self.preview_dir / "run.json").write_bytes(data)
        manifest = deepcopy(self.manifest)
        manifest["artifacts"][0]["sha256"] = sha256(data).hexdigest()
        manifest["artifacts"][0]["size_bytes"] = len(data)
        manifest["created_at_utc"] = utc()
        self.write_manifest(manifest)
        self.assertDeniedWith("PREVIEW_MANIFEST_TIMESTAMP_ORDER_INVALID")

    def test_malformed_duplicate_key_trailing_data_and_non_utf8_denied(self):
        (self.preview_dir / "preview_manifest.json").write_text("{", encoding="utf-8")
        self.assertDeniedWith("PREVIEW_MANIFEST_JSON_INVALID")

        (self.preview_dir / "preview_manifest.json").write_text(
            '{"schema_version":"preview_manifest/1.0","schema_version":"preview_manifest/1.0"}',
            encoding="utf-8",
        )
        self.assertDeniedWith("PREVIEW_MANIFEST_DUPLICATE_KEY")

        (self.preview_dir / "preview_manifest.json").write_text('{"schema_version":"preview_manifest/1.0"} x', encoding="utf-8")
        self.assertDeniedWith("PREVIEW_MANIFEST_JSON_INVALID")

        (self.preview_dir / "preview_manifest.json").write_bytes(b"\xff\xfe\x00")
        self.assertDeniedWith("PREVIEW_MANIFEST_JSON_INVALID")

    def test_cli_success_and_failure_json_shape(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code, payload = validator.main([str(self.preview_dir), "--json"])
        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["verdict"], "allow")
        self.assertEqual(json.loads(stdout.getvalue())["schema_version"], "preview_manifest_validation/1.0")

        manifest = deepcopy(self.manifest)
        manifest["schema_version"] = "bad"
        self.write_manifest(manifest)
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            code, payload = validator.main([str(self.preview_dir)])
        self.assertNotEqual(code, 0)
        printed = json.loads(stdout.getvalue())
        self.assertEqual(payload["verdict"], "deny")
        self.assertEqual(printed["verdict"], "deny")
        self.assertIn("error_codes", printed)

    def test_validation_leaves_bundle_contents_and_mtimes_unchanged(self):
        before = {
            path.name: (path.read_bytes(), path.stat().st_mtime_ns)
            for path in self.preview_dir.iterdir()
            if path.is_file() and not path.is_symlink()
        }
        result = self.validate()
        self.assertEqual(result.verdict, "allow", result.as_dict())
        after = {
            path.name: (path.read_bytes(), path.stat().st_mtime_ns)
            for path in self.preview_dir.iterdir()
            if path.is_file() and not path.is_symlink()
        }
        self.assertEqual(after, before)

    def test_validator_static_imports_do_not_include_network_or_process_modules(self):
        tree = ast.parse(VALIDATOR_PATH.read_text(encoding="utf-8"))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        self.assertFalse({"socket", "urllib", "http", "subprocess"} & imported)


if __name__ == "__main__":
    unittest.main()
