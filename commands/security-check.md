---
description: Review an agent workflow for untrusted-input boundaries, handoff safety, credential leakage, and approval controls
argument-hint: "[repository or workflow path]"
---

Load the `secure-agent-boundaries` skill and review the supplied repository or
workflow. Prioritize exploitable weaknesses in this order:

1. Untrusted document content reaching privileged tools without executable
   validation.
2. Secret material written into manifests, URLs, logs, prompts, or artifacts.
3. Unsafe or nonfunctional cross-agent handoff parsing and routing.
4. Regulated actions or recommendations without explicit human approval.

Report findings first, with severity and file references. If changes are
requested, implement tests before or with the fix.

