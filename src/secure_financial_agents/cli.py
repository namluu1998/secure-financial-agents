"""Command line entry points for the secure reference foundation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .handoff import extract_handoff
from .manifest import build_manifest
from .pipeline import UntrustedReaderBoundary


def _load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(prog="secure-financial-agents")
    commands = parser.add_subparsers(dest="command", required=True)

    validate_parser = commands.add_parser("validate-reader", help="validate untrusted worker JSON")
    validate_parser.add_argument("schema")
    validate_parser.add_argument("output")

    handoff_parser = commands.add_parser("extract-handoff", help="extract a validated handoff request")
    handoff_parser.add_argument("message")

    manifest_parser = commands.add_parser("build-manifest", help="generate a manifest with redacted logging")
    manifest_parser.add_argument("template")
    manifest_parser.add_argument("output")
    manifest_parser.add_argument("params", nargs="+", metavar="key=value")

    args = parser.parse_args()
    if args.command == "validate-reader":
        boundary = UntrustedReaderBoundary(_load_json(args.schema))
        boundary.accept(args.output, Path(args.output).read_text(encoding="utf-8"))
        print("OK: reader output validated before trusted processing")
        return 0
    if args.command == "extract-handoff":
        result = extract_handoff(Path(args.message).read_text(encoding="utf-8"))
        if result is None:
            print("No valid handoff found")
            return 1
        print(json.dumps(result, indent=2))
        return 0

    params: dict[str, str] = {}
    for pair in args.params:
        key, separator, value = pair.partition("=")
        if not separator:
            parser.error(f"expected key=value, got {pair!r}")
        params[key] = value
    result = build_manifest(
        Path(args.template).read_text(encoding="utf-8"),
        Path(args.output),
        params,
    )
    print(result.log_message())
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
