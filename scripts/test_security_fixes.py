#!/usr/bin/env python3
"""Regression checks for the security fixes carried by this fork."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ValidationError(Exception):
    pass


def _schema_validate(instance, schema):
    if not isinstance(instance, dict) or "event" not in instance:
        raise ValidationError("invalid payload")


def _load_orchestrate():
    old_anthropic = sys.modules.get("anthropic")
    old_jsonschema = sys.modules.get("jsonschema")
    sys.modules["anthropic"] = types.SimpleNamespace()
    sys.modules["jsonschema"] = types.SimpleNamespace(
        validate=_schema_validate,
        ValidationError=ValidationError,
    )
    try:
        spec = importlib.util.spec_from_file_location("orchestrate_under_test", ROOT / "scripts" / "orchestrate.py")
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        return module
    finally:
        if old_anthropic is None:
            sys.modules.pop("anthropic", None)
        else:
            sys.modules["anthropic"] = old_anthropic
        if old_jsonschema is None:
            sys.modules.pop("jsonschema", None)
        else:
            sys.modules["jsonschema"] = old_jsonschema


class HandoffRegressionTests(unittest.TestCase):
    def test_nested_payload_parses(self) -> None:
        module = _load_orchestrate()
        message = (
            '{"type":"handoff_request","target_agent":"month-end-closer",'
            '"payload":{"event":"Close May"}}'
        )
        self.assertEqual(module.extract_handoff(message)["payload"]["event"], "Close May")

    def test_non_allowlisted_target_is_ignored(self) -> None:
        module = _load_orchestrate()
        message = (
            '{"type":"handoff_request","target_agent":"external-exporter",'
            '"payload":{"event":"Export"}}'
        )
        self.assertIsNone(module.extract_handoff(message))


class ManifestLoggingRegressionTests(unittest.TestCase):
    def test_secret_value_is_redacted_from_process_output(self) -> None:
        node = "node.exe" if os.name == "nt" else "node"
        secret = "SENSITIVE_SENTINEL_TOKEN"
        xml = (
            'data:text/xml,%3COfficeApp%3E'
            '%3CSourceLocation%20DefaultValue=%22https%3A%2F%2Fpivot.claude.ai%2Ftaskpane%22%2F%3E'
            '%3Cbt%3AUrl%20id=%22Taskpane.Url%22%20DefaultValue=%22https%3A%2F%2Fpivot.claude.ai%2Ftaskpane%22%2F%3E'
            '%3C%2FOfficeApp%3E'
        )
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "manifest.xml"
            env = dict(os.environ, MANIFEST_URL=xml)
            result = subprocess.run(
                [
                    node,
                    str(ROOT / "claude-for-msft-365-install" / "scripts" / "build-manifest.mjs"),
                    "office",
                    str(output),
                    f"google_client_secret={secret}",
                ],
                capture_output=True,
                text=True,
                env=env,
                check=False,
            )
            combined = result.stdout + result.stderr
            self.assertEqual(result.returncode, 0, combined)
            self.assertNotIn(secret, combined)
            self.assertIn("google_client_secret=<redacted>", combined)
            self.assertTrue(output.exists())


class DeploymentBoundaryScopeTests(unittest.TestCase):
    def test_explicit_guard_list_matches_schema_bound_untrusted_workers(self) -> None:
        expected = {
            "earnings-reviewer",
            "gl-reconciler",
            "kyc-screener",
            "market-researcher",
            "meeting-prep-agent",
            "month-end-closer",
            "statement-auditor",
            "valuation-reviewer",
        }
        detected = set()
        cookbooks = ROOT / "managed-agent-cookbooks"
        for cookbook in cookbooks.iterdir():
            subagents = cookbook / "subagents"
            if not subagents.is_dir():
                continue
            for worker in subagents.glob("*.yaml"):
                text = worker.read_text(encoding="utf-8")
                if "\noutput_schema:" in text and "UNTRUSTED" in text.upper():
                    detected.add(cookbook.name)
                    break
        self.assertEqual(detected, expected)
        self.assertNotIn("pitch-agent", detected)
        self.assertNotIn("model-builder", detected)
        deploy_script = (ROOT / "scripts" / "deploy-managed-agent.sh").read_text(encoding="utf-8")
        for role in expected:
            self.assertIn(role, deploy_script)


class HarnessValidatorRegressionTests(unittest.TestCase):
    def test_validate_accepts_utf8_bom_json(self) -> None:
        old_jsonschema = sys.modules.get("jsonschema")
        sys.modules["jsonschema"] = types.SimpleNamespace()
        with tempfile.TemporaryDirectory() as directory:
            try:
                spec = importlib.util.spec_from_file_location("validate_under_test", ROOT / "scripts" / "validate.py")
                module = importlib.util.module_from_spec(spec)
                assert spec.loader is not None
                spec.loader.exec_module(module)

                instance = Path(directory) / "instance.json"
                instance.write_text('{"event":"Close May"}', encoding="utf-8-sig")
                self.assertEqual(module._load(instance), {"event": "Close May"})
            finally:
                if old_jsonschema is None:
                    sys.modules.pop("jsonschema", None)
                else:
                    sys.modules["jsonschema"] = old_jsonschema


if __name__ == "__main__":
    unittest.main(verbosity=2)
