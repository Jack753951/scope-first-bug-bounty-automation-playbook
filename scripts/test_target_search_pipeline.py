#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NORMALIZER_PATH = ROOT / "scripts" / "normalize_platform_policy.py"
BUILDER_PATH = ROOT / "scripts" / "build_target_candidates.py"
SCOPE_PACKET_PATH = ROOT / "scripts" / "build_scope_approval_packet.py"
PS1_PATH = ROOT / "scripts" / "kali-target-search.ps1"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


SAMPLE_VISIBLE_TEXT = """
<program-slug> Bug Bounty Program
Bounty Range $500 - $5,000
In scope
https://cloud.<program-redacted>.com SaaS Konnect dashboard and API
*.<program-redacted>.com only where explicitly listed
github.com/<program-slug>/<program-slug> Gateway source code
Out of scope
Denial of service and automated scanning
Social engineering, phishing, spam
OAuth apps, API tokens, webhooks, SCIM, SAML, organizations, invites, roles, audit logs
Login Sign up CAPTCHA verification code
"""


class NormalizePlatformPolicyTests(unittest.TestCase):
    def test_extracts_scope_rules_gates_and_candidate_classes_without_live_claims(self) -> None:
        mod = _load(NORMALIZER_PATH, "normalize_platform_policy_for_tests")

        result = mod.normalize_policy_text(
            SAMPLE_VISIBLE_TEXT,
            program="<program-slug>",
            platform="<bug-bounty-platform>",
            source_url="https://<bug-bounty-platform>.com/<program-slug>/policy_scopes",
        )

        self.assertEqual(result["schema_version"], "platform_policy_normalization/0.1")
        self.assertEqual(result["program_slug"], "<program-slug>")
        self.assertIn("https://cloud.<program-redacted>.com", {row["asset"] for row in result["in_scope_assets"]})
        self.assertTrue(any("Denial of service" in rule for rule in result["out_of_scope_rules"]))
        self.assertIn("captcha", result["auth_gates"])
        self.assertIn("verification code", result["auth_gates"])
        self.assertIn("oauth_oidc", result["candidate_classes"])
        self.assertIn("org_role_invite_authz", result["candidate_classes"])
        self.assertIn("scanner_fuzzer_dast_or_large_scale_discovery", result["stop_before"])
        self.assertIn("candidate", json.dumps(result).lower())
        self.assertNotIn("verified", json.dumps(result).lower())
        self.assertNotIn("reportable", json.dumps(result).lower())

    def test_cli_writes_json_output(self) -> None:
        mod = _load(NORMALIZER_PATH, "normalize_platform_policy_cli_for_tests")
        with tempfile.TemporaryDirectory() as td:
            text_path = Path(td) / "visible.txt"
            out_path = Path(td) / "policy.json"
            text_path.write_text(SAMPLE_VISIBLE_TEXT, encoding="utf-8")

            exit_code = mod.main([
                "--input", str(text_path),
                "--output", str(out_path),
                "--program", "<program-slug>",
                "--platform", "<bug-bounty-platform>",
                "--source-url", "https://<bug-bounty-platform>.com/<program-slug>/policy_scopes",
            ])

            self.assertEqual(exit_code, 0)
            payload = json.loads(out_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["source_url"], "https://<bug-bounty-platform>.com/<program-slug>/policy_scopes")


class BuildTargetCandidatesTests(unittest.TestCase):
    def test_builds_scored_pending_intake_candidate_without_scope_authorization(self) -> None:
        normalizer = _load(NORMALIZER_PATH, "normalize_platform_policy_for_candidate_tests")
        builder = _load(BUILDER_PATH, "build_target_candidates_for_tests")
        policy = normalizer.normalize_policy_text(
            SAMPLE_VISIBLE_TEXT,
            program="<program-slug>",
            platform="<bug-bounty-platform>",
            source_url="https://<bug-bounty-platform>.com/<program-slug>/policy_scopes",
        )
        public_doc = {
            "source": "public docs",
            "url": "https://docs.<program-redacted>.com/konnect/",
            "text": "Konnect supports organizations teams roles invites API tokens webhooks SAML SCIM audit logs GraphQL API.",
        }
        disclosed_report = {
            "source": "disclosed report",
            "url": "https://<bug-bounty-platform>.com/reports/example",
            "text": "IDOR in organization invite role allowed access-control bypass.",
        }

        payload = builder.build_pending_intake_payload(
            policies=[policy],
            public_docs=[public_doc],
            disclosed_reports=[disclosed_report],
            existing=None,
            replace_generated=True,
        )

        self.assertEqual(payload["schema_version"], "1.0")
        self.assertIn("no target testing is authorized", payload["boundary"].lower())
        generated = [c for c in payload["candidates"] if c.get("source_tool") == "build_target_candidates.py"]
        self.assertEqual(len(generated), 1)
        candidate = generated[0]
        self.assertEqual(candidate["slug"], "<program-slug>")
        self.assertEqual(candidate["status"], "candidate_passive_intake")
        self.assertGreaterEqual(candidate["score"]["total_0_23"], 12)
        self.assertIn("auth-role-separation", candidate["bundle_fit"])
        self.assertIn("api-token-or-webhook-boundary", candidate["bundle_fit"])
        self.assertIn("any live target testing beyond passive policy/public-doc reading", candidate["blocked_before"])
        self.assertNotIn("verified", json.dumps(candidate).lower())
        self.assertNotIn("reportable", json.dumps(candidate).lower())

    def test_cli_merges_generated_candidate_into_pending_intake(self) -> None:
        normalizer = _load(NORMALIZER_PATH, "normalize_platform_policy_for_cli_candidate_tests")
        builder = _load(BUILDER_PATH, "build_target_candidates_cli_for_tests")
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            policy_path = td_path / "policy.json"
            docs_path = td_path / "docs.json"
            existing_path = td_path / "pending.json"
            out_path = td_path / "out.json"
            policy_path.write_text(json.dumps(normalizer.normalize_policy_text(SAMPLE_VISIBLE_TEXT, program="<program-slug>", platform="<bug-bounty-platform>")), encoding="utf-8")
            docs_path.write_text(json.dumps([{"url": "https://docs.<program-redacted>.com", "text": "roles invites api tokens webhooks"}]), encoding="utf-8")
            existing_path.write_text(json.dumps({"schema_version": "1.0", "updated_at": "2026-05-29", "boundary": "existing", "candidates": [{"slug": "keep_me", "status": "reference"}]}), encoding="utf-8")

            exit_code = builder.main([
                "--policy", str(policy_path),
                "--public-docs", str(docs_path),
                "--existing", str(existing_path),
                "--output", str(out_path),
            ])

            self.assertEqual(exit_code, 0)
            payload = json.loads(out_path.read_text(encoding="utf-8"))
            slugs = [c["slug"] for c in payload["candidates"]]
            self.assertIn("keep_me", slugs)
            self.assertIn("<program-slug>", slugs)


class BuildScopeApprovalPacketTests(unittest.TestCase):
    def test_classifies_exact_scope_wildcards_source_and_blocked_entries_without_authorizing_live_action(self) -> None:
        normalizer = _load(NORMALIZER_PATH, "normalize_platform_policy_for_scope_packet_tests")
        packet_mod = _load(SCOPE_PACKET_PATH, "build_scope_approval_packet_for_tests")
        policy = normalizer.normalize_policy_text(
            SAMPLE_VISIBLE_TEXT + "\n*.edge.gateways.<program-redacted>.com customer data plane out of scope\n",
            program="<program-slug>",
            platform="<bug-bounty-platform>",
            source_url="https://<bug-bounty-platform>.com/<program-slug>/policy_scopes",
        )
        with tempfile.TemporaryDirectory() as td:
            scope_path = Path(td) / "scope.txt"
            scope_path.write_text("cloud.<program-redacted>.com\n", encoding="utf-8")

            packet = packet_mod.build_scope_approval_packet(policy, global_scope_path=scope_path)

        self.assertEqual(packet["schema_version"], "scope_approval_packet/0.1")
        self.assertIn("does not authorize live target testing", packet["boundary"])
        self.assertEqual(
            {row["scope_entry"] for row in packet["already_in_global_scope"]},
            {"cloud.<program-redacted>.com"},
        )
        self.assertIn("*.<program-redacted>.com", {row["scope_entry"] for row in packet["wildcard_requires_exact_host_narrowing"]})
        self.assertIn("github.com/<program-slug>/<program-slug>", {row["scope_entry"] for row in packet["source_or_local_only"]})
        self.assertIn("*.edge.gateways.<program-redacted>.com", {row["scope_entry"] for row in packet["blocked_or_out_of_scope"]})
        self.assertNotIn("*.<program-redacted>.com", packet["suggested_config_scope_entries"])
        self.assertIn("operator approval before editing config/scope.txt", packet["operator_gates"])
        self.assertNotIn("verified", json.dumps(packet).lower())
        self.assertNotIn("reportable", json.dumps(packet).lower())

    def test_cli_writes_markdown_and_json_packet(self) -> None:
        normalizer = _load(NORMALIZER_PATH, "normalize_platform_policy_for_scope_packet_cli_tests")
        packet_mod = _load(SCOPE_PACKET_PATH, "build_scope_approval_packet_cli_for_tests")
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            policy_path = td_path / "policy.json"
            scope_path = td_path / "scope.txt"
            md_path = td_path / "packet.md"
            json_path = td_path / "packet.json"
            policy = normalizer.normalize_policy_text(
                "In scope\nhttps://app.example.test roles api\nhttps://api.example.test direct url\n",
                program="example",
                platform="<bug-bounty-platform>",
            )
            policy_path.write_text(json.dumps(policy), encoding="utf-8")
            scope_path.write_text("app.example.test\n", encoding="utf-8")

            exit_code = packet_mod.main([
                "--policy", str(policy_path),
                "--global-scope", str(scope_path),
                "--output", str(md_path),
                "--json-output", str(json_path),
            ])

            self.assertEqual(exit_code, 0)
            markdown = md_path.read_text(encoding="utf-8")
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertIn("Scope Approval Packet", markdown)
            self.assertIn("api.example.test", markdown)
            self.assertEqual(payload["suggested_config_scope_entries"], ["api.example.test"])


class KaliTargetSearchWrapperTests(unittest.TestCase):
    def test_wrapper_documents_required_browser_pipeline_and_sanitized_output_directory(self) -> None:
        text = PS1_PATH.read_text(encoding="utf-8")
        self.assertIn("kali-browser-ops.ps1", text)
        self.assertIn("-Action", text)
        for action in ["open", "cdp-visible-text", "screenshot", "downloads"]:
            self.assertIn(action, text)
        self.assertIn("<artifact-output-dir>\\browser_state", text)
        self.assertIn("sanitize", text.lower())
        self.assertIn("manifest.json", text)


if __name__ == "__main__":
    unittest.main()
