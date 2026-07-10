from __future__ import annotations

import argparse
import re
from pathlib import Path

from common import (
    CLAUSE_NUMBER_PATTERN,
    INDEX_ROOT,
    LAW_FILES,
    compact_whitespace,
    read_text,
    repo_relative,
    write_json,
)


SECTION_RE = re.compile(rf"^###\s+(มาตรา|ข้อ)\s+({CLAUSE_NUMBER_PATTERN})\b(.*)$")
HEADING_RE = re.compile(r"^(#{1,2})\s+(.+)$")


def doc_type_for(path: Path) -> str:
    return "act" if path.name == "prb60.md" else "regulation"


def parse_metadata(lines: list[str]) -> dict[str, str]:
    metadata: dict[str, str] = {}
    in_metadata = False
    for line in lines:
        if line.strip() == "## Metadata":
            in_metadata = True
            continue
        if in_metadata and line.startswith("#") and line.strip() != "## Metadata":
            break
        if in_metadata and line.startswith("- ") and ":" in line:
            key, value = line[2:].split(":", 1)
            metadata[key.strip()] = value.strip()
    return metadata


def build_chunks_for_file(path: Path) -> tuple[dict[str, object], list[dict[str, object]]]:
    text = read_text(path)
    lines = text.splitlines()
    metadata = parse_metadata(lines)
    source = repo_relative(path)
    doc_type = doc_type_for(path)
    chunks: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    current_lines: list[str] = []
    heading_path: list[str] = []

    def flush() -> None:
        nonlocal current, current_lines
        if current is None:
            return
        body = "\n".join(current_lines).strip()
        current["text"] = body
        current["search_text"] = compact_whitespace(
            " ".join(
                [
                    str(current.get("title", "")),
                    " ".join(current.get("heading_path", [])),
                    body,
                ]
            )
        )
        chunks.append(current)
        current = None
        current_lines = []

    for line_no, line in enumerate(lines, start=1):
        section_match = SECTION_RE.match(line.strip())
        heading_match = HEADING_RE.match(line.strip())

        if section_match:
            flush()
            clause_type, clause_no, title_tail = section_match.groups()
            current = {
                "id": f"{path.stem}-{clause_type}-{clause_no}",
                "source": source,
                "doc_type": doc_type,
                "clause_type": clause_type,
                "clause_no": clause_no,
                "title": compact_whitespace(f"{clause_type} {clause_no} {title_tail}"),
                "heading_path": heading_path[:],
                "start_line": line_no,
            }
            if title_tail.strip():
                current_lines.append(title_tail.strip())
            continue

        if heading_match and not section_match:
            level, title = heading_match.groups()
            if level == "#":
                heading_path = [title.strip()]
            elif level == "##":
                heading_path = heading_path[:1] + [title.strip()]

        if current is not None:
            current_lines.append(line)

    flush()
    document = {
        "source": source,
        "doc_type": doc_type,
        "metadata": metadata,
        "chunk_count": len(chunks),
    }
    return document, chunks


def build_index() -> dict[str, object]:
    documents = []
    chunks = []
    for path in LAW_FILES.values():
        document, file_chunks = build_chunks_for_file(path)
        documents.append(document)
        chunks.extend(file_chunks)

    topic_routes = {
        "พรบ": ["reference/law/prb60.md"],
        "พ.ร.บ": ["reference/law/prb60.md"],
        "พระราชบัญญัติ": ["reference/law/prb60.md"],
        "มาตรา": ["reference/law/prb60.md"],
        "อุทธรณ์": ["reference/law/prb60.md"],
        "ร้องเรียน": ["reference/law/prb60.md"],
        "บทกำหนดโทษ": ["reference/law/prb60.md"],
        "ระเบียบ": ["reference/law/rbb60.md"],
        "ข้อ": ["reference/law/rbb60.md"],
        "ระเบียบฉบับที่ 3": ["reference/law/rbb60-3.md"],
        "ข้อ 190": ["reference/law/rbb60-3.md"],
        "ข้อ 191": ["reference/law/rbb60-3.md"],
        "คะแนนความเสียหาย": ["reference/law/rbb60-3.md"],
        "คะแนนความเสียหายสะสม": ["reference/law/rbb60-3.md"],
        "การระงับการยื่นข้อเสนอ": ["reference/law/rbb60-3.md"],
        "การระงับการทำสัญญา": ["reference/law/rbb60-3.md"],
        "การประเมินผลการปฏิบัติงานของผู้ประกอบการ": ["reference/law/rbb60-3.md"],
        "อันตรายสาหัส": ["reference/law/rbb60-3.md"],
        "ทรัพย์สินเสียหาย": ["reference/law/rbb60-3.md"],
        "วิธีเฉพาะเจาะจง": ["reference/law/rbb60.md"],
        "วิธีคัดเลือก": ["reference/law/rbb60.md"],
        "e-bidding": ["reference/law/rbb60.md"],
        "e-market": ["reference/law/rbb60.md"],
        "สัญญา": ["reference/law/prb60.md", "reference/law/rbb60.md"],
        "หลักประกัน": ["reference/law/rbb60.md"],
        "ตรวจรับ": ["reference/law/prb60.md", "reference/law/rbb60.md"],
        "บริหารสัญญา": ["reference/law/prb60.md", "reference/law/rbb60.md"],
        "บริหารพัสดุ": ["reference/law/prb60.md", "reference/law/rbb60.md"],
    }
    keyword_routes = topic_routes.copy()

    write_json(INDEX_ROOT / "documents.json", documents)
    write_json(INDEX_ROOT / "chunks.json", chunks)
    write_json(INDEX_ROOT / "topic_routes.json", topic_routes)
    write_json(INDEX_ROOT / "keyword_routes.json", keyword_routes)
    return {"documents": documents, "chunks": chunks}


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Pasadu section-aware JSON indexes.")
    parser.parse_args()
    index = build_index()
    print(f"Indexed {len(index['documents'])} documents and {len(index['chunks'])} chunks.")


if __name__ == "__main__":
    main()
