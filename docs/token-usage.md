# Pasadu token usage

This note explains how the retrieval scripts affect context size when Pasadu is used from Codex or another agent runtime.

## What does not enter the LLM context

`data/index/chunks.json` is loaded by Python in `retrieve.py`, but the whole file is not printed or sent to the model during normal use.

The normal flow is:

1. `route_query.py` chooses the primary source and fallback source.
2. `retrieve.py` loads `chunks.json` in process memory.
3. `retrieve.py` filters and scores chunks.
4. Only the selected results are printed or returned.

So the expensive part is not the size of `chunks.json` on disk. The expensive part is whatever text the caller prints and passes into the LLM context.

## Default context mode

`answer_context.py` now uses compact rules by default. It preserves the same routing and retrieval workflow, but it does not inject the full `pasadu.md` into every generated context block.

Pasadu uses compact mode silently by default:

- `compact` is the default and is recommended for normal questions.
- `full rules` is available when the user wants the full `pasadu.md` rules included.

Do not ask the user to choose a mode or announce the mode for a direct legal question. Use full rules only when explicitly requested for an audit.

Default:

```powershell
python skills/pasadu/scripts/pasadu/answer_context.py "คำถามด้านพัสดุ"
```

This includes:

- compact operating rules
- route metadata
- the user question
- retrieved references only
- output guardrail

## Full rules mode

Use `--full-rules` only when a caller explicitly needs the full `pasadu.md` rules in the context:

```powershell
python skills/pasadu/scripts/pasadu/answer_context.py "คำถามด้านพัสดุ" --full-rules
```

This is more expensive because it includes the full `pasadu.md` text plus retrieved references.

## Recommended Codex usage

For token-efficient Codex chat:

1. Use `evidence_packet.py` as the default single-pass retrieval entry point.
2. Reuse the prior verified packet for a same-issue follow-up.
3. Use `answer_context.py` default mode only when a ready-made answer context is useful.
4. Avoid reading `data/index/chunks.json` directly into chat.
5. Keep `--limit` small unless the question truly needs broader retrieval.
