# Secure Financial Agents

A security-first reference foundation for financial workflow agents. This
project rebuilds the runtime controls that matter before adding prompts,
connectors, or business-specific agent definitions.

## Install As A Plugin

Add this repository as a Claude plugin marketplace:

```text
https://github.com/namluu1998/secure-financial-agents
```

Then install **Secure Financial Agents** from the marketplace. It includes the
`secure-agent-boundaries` skill and the `/secure-financial-agents:security-check`
command for reviewing agent repositories and workflows.

## Security Guarantees

- Untrusted document-reader output is schema-validated in executable code
  before any trusted step receives it.
- Handoff requests are parsed as real nested JSON, schema-validated, and
  constrained to an allowlist of agent targets.
- Office manifest generation refuses credential-bearing keys. Secrets belong
  behind an authenticated bootstrap endpoint, not in deployment XML, URLs, or
  setup logs.

This project stages analysis and artifacts only. It does not execute trades,
approve onboarding, post ledger entries, or generate client-facing investment
recommendations without an application-specific review layer.

## Structure

```text
secure-financial-agents/
  .claude-plugin/             # marketplace and plugin manifests
  commands/                   # installed slash commands
  skills/                     # installed Claude security-review skill
  src/secure_financial_agents/
    validation.py    # dependency-free boundary schema validator
    pipeline.py      # mandatory untrusted reader -> trusted step gate
    handoff.py       # nested JSON handoff extraction and allowlist
    manifest.py      # secret-free add-in manifest builder
    cli.py           # command line interface
  examples/
    schemas/         # sample boundary schemas
  tests/             # regression tests for the identified vulnerabilities
```

## Run Locally

This repository uses Python standard library only at runtime.

PowerShell:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
python -m secure_financial_agents.cli validate-reader examples/schemas/gl_reader.schema.json examples/reader-output.json
python -m secure_financial_agents.cli extract-handoff examples/handoff-message.txt
python -m secure_financial_agents.cli build-manifest examples/office-manifest-template.xml out-manifest.xml bootstrap_url=https://config.example/bootstrap entra_sso=1
```

The last command logs configured key names only. The following is rejected:

```powershell
python -m secure_financial_agents.cli build-manifest examples/office-manifest-template.xml out.xml gateway_token=secret
```

## Boundary Pattern

Every agent that reads PDFs, emails, statements, KYC files, or other outside
content must be behind an explicit validation boundary:

```python
import json
from pathlib import Path

from secure_financial_agents.pipeline import UntrustedReaderBoundary

schema = json.loads(Path("examples/schemas/gl_reader.schema.json").read_text())
boundary = UntrustedReaderBoundary(schema)

def privileged_step(validated):
    return validated.data["breaks"]

result = boundary.forward("statement.pdf", raw_worker_json, privileged_step)
```

If parsing or validation fails, `privileged_step` is not called.

## Next Expansion Points

Add business workflows only after defining:

1. A schema for each untrusted input reader.
2. Tool permissions for each trusted processing step.
3. An approval boundary for regulated outputs.
4. Secret delivery through authenticated bootstrap or a secret manager.
