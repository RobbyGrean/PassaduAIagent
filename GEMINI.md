# Pasadu adapter for Gemini CLI

For substantive Thai government procurement questions, follow `AGENTS.md` and the standalone skill at `skills/pasadu/SKILL.md`.

- Run `python -B skills/pasadu/scripts/pasadu/evidence_packet.py "<question>" --limit 3` for new issues.
- Keep retrieval and all analysis in the current conversation; no custom subagent is required.
- Use web search only under the repository-first fallback conditions.
- Verify repository citations with `python -B skills/pasadu/scripts/pasadu/cite_check.py`.
- Preserve the exact web-fallback disclaimer and source-separation contract in `AGENTS.md`.
