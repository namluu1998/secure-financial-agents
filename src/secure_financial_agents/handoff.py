"""Typed extraction of cross-agent handoff requests."""

from __future__ import annotations

import json
from typing import Any, Iterable

from .validation import SchemaValidationError, validate


DEFAULT_ALLOWED_TARGETS = frozenset(
    {
        "earnings-reviewer",
        "gl-reconciler",
        "kyc-screener",
        "market-researcher",
        "meeting-prep-agent",
        "model-builder",
        "month-end-closer",
        "pitch-agent",
        "statement-auditor",
        "valuation-reviewer",
    }
)

HANDOFF_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["type", "target_agent", "payload"],
    "properties": {
        "type": {"type": "string", "enum": ["handoff_request"]},
        "target_agent": {"type": "string", "maxLength": 64, "pattern": r"^[a-z0-9-]+$"},
        "payload": {
            "type": "object",
            "additionalProperties": False,
            "required": ["event"],
            "properties": {
                "event": {"type": "string", "maxLength": 2000},
                "context_ref": {
                    "type": "string",
                    "maxLength": 256,
                    "pattern": r"^[A-Za-z0-9 ._/:#-]+$",
                },
            },
        },
    },
}


def _json_objects(text: str) -> Iterable[dict[str, Any]]:
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char != "{":
            continue
        try:
            value, _ = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            yield value


def extract_handoff(
    text: str,
    allowed_targets: frozenset[str] = DEFAULT_ALLOWED_TARGETS,
) -> dict[str, Any] | None:
    """Return the first validated handoff JSON object found in model output."""

    for candidate in _json_objects(text):
        if candidate.get("type") != "handoff_request":
            continue
        try:
            validate(candidate, HANDOFF_SCHEMA)
        except SchemaValidationError:
            continue
        if candidate["target_agent"] not in allowed_targets:
            continue
        return candidate
    return None

