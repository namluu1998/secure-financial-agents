"""Minimal dependency-free schema enforcement for untrusted agent output."""

from __future__ import annotations

import math
import re
from typing import Any


class SchemaValidationError(ValueError):
    """Raised when untrusted output does not satisfy its schema."""

    def __init__(self, path: str, message: str) -> None:
        super().__init__(f"{path}: {message}")
        self.path = path
        self.message = message


def _fail(path: str, message: str) -> None:
    raise SchemaValidationError(path, message)


def _check_type(value: Any, expected: str, path: str) -> None:
    matches = {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "boolean": isinstance(value, bool),
        "null": value is None,
    }
    if expected not in matches:
        _fail(path, f"unsupported schema type {expected!r}")
    if not matches[expected]:
        _fail(path, f"expected {expected}, got {type(value).__name__}")


def validate(value: Any, schema: dict[str, Any], path: str = "$") -> Any:
    """Validate `value` against the restricted schema dialect used at boundaries.

    Supported keywords are intentionally small and auditable: type, enum,
    required, additionalProperties, properties, items, maxItems, maxLength,
    minimum, maximum, and pattern.
    """

    expected = schema.get("type")
    if expected:
        _check_type(value, expected, path)

    if "enum" in schema and value not in schema["enum"]:
        _fail(path, f"value {value!r} is not allowed")

    if isinstance(value, dict):
        required = schema.get("required", [])
        for name in required:
            if name not in value:
                _fail(path, f"missing required property {name!r}")

        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            unexpected = set(value) - set(properties)
            if unexpected:
                _fail(path, f"unexpected properties: {', '.join(sorted(unexpected))}")
        for name, child in properties.items():
            if name in value:
                validate(value[name], child, f"{path}.{name}")

    if isinstance(value, list):
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            _fail(path, f"has {len(value)} items; maximum is {schema['maxItems']}")
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                validate(item, item_schema, f"{path}[{index}]")

    if isinstance(value, str):
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            _fail(path, f"has length {len(value)}; maximum is {schema['maxLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            _fail(path, "does not match the allowed character pattern")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if not math.isfinite(value):
            _fail(path, "must be finite")
        if "minimum" in schema and value < schema["minimum"]:
            _fail(path, f"is below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            _fail(path, f"is above maximum {schema['maximum']}")

    return value

