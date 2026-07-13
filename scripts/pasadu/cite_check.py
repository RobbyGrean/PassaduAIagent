from __future__ import annotations

import argparse
import json
import re

from common import (
    INDEX_ROOT,
    REFERENCE_SECTION_NUMBER_PATTERN,
    SOURCE_DISPLAY_NAMES,
    normalize_digits,
    read_json,
    read_text,
)


CITATION_RE = re.compile(
    rf"(reference/(?:law(?:/ministerial-regulations)?|circulars)/[a-z0-9-]+\.md)"
    rf"\s+(มาตรา|ข้อ|หัวข้อ)\s*({REFERENCE_SECTION_NUMBER_PATTERN})"
)
HUMAN_SOURCE_RE = "|".join(
    re.escape(label)
    for label in sorted(SOURCE_DISPLAY_NAMES.values(), key=len, reverse=True)
)
HUMAN_CITATION_RE = re.compile(
    rf"({HUMAN_SOURCE_RE})\s+(มาตรา|ข้อ|หัวข้อ)\s*({REFERENCE_SECTION_NUMBER_PATTERN})"
)
DISPLAY_TO_SOURCE = {label: source for source, label in SOURCE_DISPLAY_NAMES.items()}


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
    path_citations = [
        (source, clause_type, normalize_digits(number))
        for source, clause_type, number in CITATION_RE.findall(answer)
    ]
    human_citations = [
        (DISPLAY_TO_SOURCE[label], clause_type, normalize_digits(number))
        for label, clause_type, number in HUMAN_CITATION_RE.findall(answer)
    ]
    found = path_citations + human_citations
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
