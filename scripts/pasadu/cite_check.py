from __future__ import annotations

import argparse
import json
import re

from common import INDEX_ROOT, normalize_digits, read_json, read_text


CITATION_RE = re.compile(
    r"(reference/law/(?:prb60|rbb60)\.md)\s+(มาตรา|ข้อ)\s*([0-9๐-๙]+)"
)


def load_valid_citations() -> set[tuple[str, str, str]]:
    chunks = read_json(INDEX_ROOT / "chunks.json")
    assert isinstance(chunks, list)
    return {
        (
            str(chunk["source"]),
            str(chunk["clause_type"]),
            normalize_digits(str(chunk["clause_no"])),
        )
        for chunk in chunks
    }


def check_citations(answer: str) -> dict[str, object]:
    valid = load_valid_citations()
    found = [
        (source, clause_type, normalize_digits(number))
        for source, clause_type, number in CITATION_RE.findall(answer)
    ]
    invalid = [citation for citation in found if citation not in valid]
    return {
        "ok": bool(found) and not invalid,
        "found": [
            {"source": source, "clause_type": clause_type, "clause_no": number}
            for source, clause_type, number in found
        ],
        "invalid": [
            {"source": source, "clause_type": clause_type, "clause_no": number}
            for source, clause_type, number in invalid
        ],
        "message": "citation valid" if found and not invalid else "missing or invalid citation",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Check Pasadu answer citations against the local index.")
    parser.add_argument("--text", help="Answer text to check")
    parser.add_argument("--file", help="UTF-8 text file containing an answer")
    args = parser.parse_args()

    if not (INDEX_ROOT / "chunks.json").exists():
        raise SystemExit("Index not found. Run: python scripts/pasadu/build_index.py")
    if not args.text and not args.file:
        raise SystemExit("Use --text or --file")

    answer = args.text if args.text is not None else read_text(args.file)
    print(json.dumps(check_citations(answer), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
