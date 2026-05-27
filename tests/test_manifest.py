import tempfile
import unittest
from pathlib import Path

from secure_financial_agents.manifest import build_manifest


TEMPLATE = '<OfficeApp><SourceLocation DefaultValue="https://app.example/taskpane?mode=org" /></OfficeApp>'


class ManifestTests(unittest.TestCase):
    def test_log_includes_keys_but_not_values(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = build_manifest(
                TEMPLATE,
                Path(directory) / "manifest.xml",
                {"bootstrap_url": "https://config.example/bootstrap", "entra_sso": "1"},
            )
            message = result.log_message()

        self.assertIn("bootstrap_url", message)
        self.assertNotIn("https://config.example/bootstrap", message)

    def test_rejects_secret_in_deployment_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "secrets may not be embedded"):
                build_manifest(
                    TEMPLATE,
                    Path(directory) / "manifest.xml",
                    {"gateway_token": "real-production-secret"},
                )

    def test_manifest_encodes_non_secret_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "manifest.xml"
            build_manifest(
                TEMPLATE,
                output,
                {"gateway_url": "https://gateway.example/v1", "gateway_api_format": "anthropic"},
            )
            xml = output.read_text()

        self.assertIn("gateway_url=https%3A%2F%2Fgateway.example%2Fv1", xml)
        self.assertIn("&amp;gateway_api_format=anthropic", xml)


if __name__ == "__main__":
    unittest.main()

