"""Build an Office add-in manifest without disclosing configuration secrets."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlencode


FORBIDDEN_SECRET_KEYS = frozenset(
    {"azure_api_key", "gateway_token", "google_client_secret", "otlp_headers"}
)
ALLOWED_KEYS = frozenset(
    {
        "allow_1p",
        "auto_connect",
        "aws_region",
        "aws_role_arn",
        "azure_resource_name",
        "bootstrap_url",
        "disabled_features",
        "entra_scope",
        "entra_sso",
        "gateway_api_format",
        "gateway_auth_header",
        "gateway_url",
        "gcp_project_id",
        "gcp_region",
        "graph_client_id",
        "mcp_servers",
        "otlp_endpoint",
    }
)


@dataclass(frozen=True)
class ManifestBuildResult:
    output: Path
    configured_keys: tuple[str, ...]

    def log_message(self) -> str:
        keys = ", ".join(self.configured_keys)
        return f"Wrote {self.output} (configured keys: {keys}; secrets are not accepted in manifests)"


def _append_query(url: str, params: dict[str, str]) -> str:
    separator = "&" if "?" in url else "?"
    return f"{url}{separator}{urlencode(params)}"


def build_manifest(template_xml: str, output: Path, params: dict[str, str]) -> ManifestBuildResult:
    """Append startup config to taskpane URLs and write an XML manifest.

    Secrets are rejected rather than written into deployment XML or logs. Use a
    separately authenticated bootstrap endpoint for credential delivery.
    """

    if not params:
        raise ValueError("at least one configuration key is required")
    if any(not key or not value for key, value in params.items()):
        raise ValueError("configuration keys and values must be non-empty")
    forbidden = sorted(set(params) & FORBIDDEN_SECRET_KEYS)
    if forbidden:
        raise ValueError(
            f"secrets may not be embedded in a manifest: {', '.join(forbidden)}; "
            "deliver them through an authenticated bootstrap endpoint"
        )
    unknown = sorted(set(params) - ALLOWED_KEYS)
    if unknown:
        raise ValueError(f"unsupported manifest keys: {', '.join(unknown)}")

    markers = ('<SourceLocation DefaultValue="', 'id="Taskpane.Url" DefaultValue="')
    xml = template_xml
    found = False
    for marker in markers:
        start = 0
        while True:
            marker_at = xml.find(marker, start)
            if marker_at < 0:
                break
            value_start = marker_at + len(marker)
            value_end = xml.find('"', value_start)
            if value_end < 0:
                raise ValueError("malformed manifest URL attribute")
            original = xml[value_start:value_end].replace("&amp;", "&")
            replaced = _append_query(original, params).replace("&", "&amp;")
            xml = xml[:value_start] + replaced + xml[value_end:]
            start = value_start + len(replaced)
            found = True
    if not found:
        raise ValueError("manifest does not contain a supported taskpane URL slot")

    output.write_text(xml, encoding="utf-8")
    configured = tuple(sorted(params))
    return ManifestBuildResult(output=output, configured_keys=configured)

