"""Runtime boundaries between untrusted readers and privileged workflow steps."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Callable

from .validation import validate


@dataclass(frozen=True)
class ValidatedReaderResult:
    """Result whose schema was enforced before entering trusted processing."""

    source: str
    data: dict[str, Any]


class UntrustedReaderBoundary:
    """Validate a reader response before allowing it into a privileged workflow."""

    def __init__(self, schema: dict[str, Any]) -> None:
        self.schema = schema

    def accept(self, source: str, raw_output: str) -> ValidatedReaderResult:
        decoded = json.loads(raw_output)
        validate(decoded, self.schema)
        return ValidatedReaderResult(source=source, data=decoded)

    def forward(
        self,
        source: str,
        raw_output: str,
        trusted_step: Callable[[ValidatedReaderResult], Any],
    ) -> Any:
        """Invoke a trusted step only after validation succeeds."""

        result = self.accept(source, raw_output)
        return trusted_step(result)

