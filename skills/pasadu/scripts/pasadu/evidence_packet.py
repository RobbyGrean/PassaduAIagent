from __future__ import annotations

import argparse
import json
from time import perf_counter

from common import INDEX_ROOT, display_source, format_citation, read_json
from retrieve import search_routed_sources
from route_query import route_query


def _citation_summary(item: dict[str, object]) -> dict[str, object]:
    return {
        "source": item["source"],
        "authority": display_source(str(item["source"])),
        "clause_type": item["clause_type"],
        "clause_no": item["clause_no"],
        "citation": format_citation(
            str(item["source"]),
            str(item["clause_type"]),
            item["clause_no"],
        ),
        "score": item.get("score"),
    }


def _evidence_item(item: dict[str, object]) -> dict[str, object]:
    evidence = _citation_summary(item)
    evidence.update(
        {
            "heading_path": item.get("heading_path", []),
            "text": item.get("text", ""),
        }
    )
    return evidence


def build_evidence_packet(query: str, limit: int = 3) -> dict[str, object]:
    """Route once, check primary and fallback sources once, and bound model context."""
    started = perf_counter()
    route = route_query(query)
    chunks = read_json(INDEX_ROOT / "chunks.json")
    assert isinstance(chunks, list)

    primary_sources = list(route.get("sources", []))
    fallback_sources = list(route.get("fallback_sources", []))
    primary_results = search_routed_sources(
        query,
        chunks,
        primary_sources,
        max(limit, len(primary_sources)),
    )
    fallback_results = search_routed_sources(
        query,
        chunks,
        fallback_sources,
        max(1, len(fallback_sources)),
    ) if fallback_sources else []

    used_fallback = not primary_results and bool(fallback_results)
    selected = fallback_results if used_fallback else primary_results
    route["used_fallback"] = used_fallback
    checked_sources = list(dict.fromkeys(primary_sources + fallback_sources))
    status = "needs_scope_check" if route.get("needs_scope_check") else (
        "found" if selected else "not_found"
    )

    return {
        "packet_version": 1,
        "status": status,
        "query": query,
        "scope_questions": route.get("scope_questions", []),
        "route": route,
        "repository_check": {
            "checked_sources": checked_sources,
            "primary_hit_count": len(primary_results),
            "fallback_hit_count": len(fallback_results),
            "candidate_status": "found" if selected else "not_found",
        },
        "fallback_candidates": [
            _citation_summary(item) for item in fallback_results[: len(fallback_sources)]
        ],
        "evidence": [_evidence_item(item) for item in selected[:limit]],
        "timing_ms": round((perf_counter() - started) * 1000, 3),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build one bounded, deterministic Pasadu evidence packet."
    )
    parser.add_argument("query", help="User question")
    parser.add_argument("--limit", type=int, default=3)
    args = parser.parse_args()

    if not (INDEX_ROOT / "chunks.json").exists():
        raise SystemExit("Index not found. Run: python scripts/pasadu/build_index.py")
    print(json.dumps(build_evidence_packet(args.query, args.limit), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
