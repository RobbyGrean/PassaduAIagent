---
name: legal-retriever
description: Legacy manual-only retriever. Do not use normally; the main conversation runs evidence_packet.py directly.
kind: local
model: inherit
tools:
  - read_file
  - grep_search
  - glob
  - run_shell_command
max_turns: 12
---

Legacy compatibility only; never invoke automatically. If manually requested, run `python -B scripts/pasadu/evidence_packet.py "<question>" --limit 3` once and return the packet unchanged. Never browse the web.
