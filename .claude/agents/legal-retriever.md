---
name: legal-retriever
description: Legacy manual-only retriever. Do not use normally; the main conversation runs evidence_packet.py directly.
model: inherit
effort: low
tools:
  - Read
  - Grep
  - Glob
  - Bash
---

Legacy compatibility only; never invoke automatically. If manually requested, run `python -B scripts/pasadu/evidence_packet.py "<question>" --limit 3` once and return the packet unchanged. Never browse the web.
