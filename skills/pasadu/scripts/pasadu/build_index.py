from __future__ import annotations

import argparse
import re
from pathlib import Path

from common import (
    CLAUSE_NUMBER_PATTERN,
    INDEX_ROOT,
    REFERENCE_FILES,
    compact_whitespace,
    read_text,
    repo_relative,
    write_json,
)


LEGAL_SECTION_RE = re.compile(rf"^###\s+(มาตรา|ข้อ)\s+({CLAUSE_NUMBER_PATTERN})\b(.*)$")
NUMBERED_SECTION_RE = re.compile(r"^#{2,4}\s+(\d+(?:\.\d+)*\.?)\s*(.*)$")
HEADING_RE = re.compile(r"^(#{1,4})\s+(.+)$")


def doc_type_for(path: Path, metadata: dict[str, object]) -> str:
    if metadata.get("document_type"):
        return str(metadata["document_type"])
    return "act" if path.name == "prb60.md" else "regulation"


def parse_metadata(lines: list[str]) -> dict[str, object]:
    metadata: dict[str, object] = {}
    if lines and lines[0].strip() == "---":
        current_list: str | None = None
        for line in lines[1:]:
            if line.strip() == "---":
                break
            if line.startswith("  - ") and current_list:
                values = metadata.setdefault(current_list, [])
                assert isinstance(values, list)
                values.append(line[4:].strip().strip('"'))
                continue
            if line and not line.startswith(" ") and ":" in line:
                key, value = line.split(":", 1)
                current_list = key.strip() if not value.strip() else None
                metadata[key.strip()] = value.strip().strip('"') if value.strip() else []
        return metadata

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
    doc_type = doc_type_for(path, metadata)
    metadata_search = compact_whitespace(
        " ".join(
            str(value) if not isinstance(value, list) else " ".join(map(str, value))
            for value in metadata.values()
        )
    )
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
                    metadata_search,
                ]
            )
        )
        chunks.append(current)
        current = None
        current_lines = []

    for line_no, line in enumerate(lines, start=1):
        legal_match = LEGAL_SECTION_RE.match(line.strip())
        numbered_match = NUMBERED_SECTION_RE.match(line.strip())
        heading_match = HEADING_RE.match(line.strip())

        if legal_match or numbered_match:
            flush()
            if legal_match:
                clause_type, clause_no, title_tail = legal_match.groups()
            else:
                assert numbered_match is not None
                clause_no, title_tail = numbered_match.groups()
                clause_type = "หัวข้อ"
                clause_no = clause_no.rstrip(".")
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

        if heading_match and not legal_match and not numbered_match:
            level, title = heading_match.groups()
            depth = len(level)
            heading_path = heading_path[: depth - 1] + [title.strip()]

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
    for path in REFERENCE_FILES.values():
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
        "ว 214": ["reference/circulars/circular-w214-2563.md"],
        "คุณสมบัติผู้ยื่นเสนอราคา": ["reference/circulars/circular-w214-2563.md"],
        "กฎกระทรวงเจาะจง": ["reference/law/ministerial-regulations/mr-specific-2560.md"],
        "วงเงินเล็กน้อย": ["reference/law/ministerial-regulations/mr-specific-2560.md"],
        "ไม่ทำข้อตกลงเป็นหนังสือ": ["reference/law/ministerial-regulations/mr-specific-2560.md"],
        "กรรมการตรวจรับคนเดียว": ["reference/law/ministerial-regulations/mr-specific-2560.md"],
        "กฎกระทรวงอุทธรณ์": ["reference/law/ministerial-regulations/mr-appeal-exclusions-2568.md"],
        "ว 367": ["reference/circulars/circular-w367-2567.md"],
        "ไม่เข้าข่ายที่จะใช้สิทธิอุทธรณ์": ["reference/circulars/circular-w367-2567.md", "reference/law/prb60.md"],
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
