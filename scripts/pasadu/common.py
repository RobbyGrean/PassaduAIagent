from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
REFERENCE_ROOT = REPO_ROOT / "reference"
INDEX_ROOT = REPO_ROOT / "data" / "index"

REFERENCE_FILES = {
    "prb60": REFERENCE_ROOT / "law" / "prb60.md",
    "rbb60": REFERENCE_ROOT / "law" / "rbb60.md",
    "rbb60-3": REFERENCE_ROOT / "law" / "rbb60-3.md",
    "mr-specific-2560": REFERENCE_ROOT / "law" / "ministerial-regulations" / "mr-specific-2560.md",
    "mr-appeal-exclusions-2568": REFERENCE_ROOT / "law" / "ministerial-regulations" / "mr-appeal-exclusions-2568.md",
    "circular-w367-2567": REFERENCE_ROOT / "circulars" / "circular-w367-2567.md",
    "circular-w214-2563": REFERENCE_ROOT / "circulars" / "circular-w214-2563.md",
}

# Internal paths are useful to the retrieval/index layer, but they are not
# suitable citations for people using Pasadu. Keep the mapping here so every
# user-facing formatter uses the same authoritative document name.
SOURCE_DISPLAY_NAMES = {
    "reference/law/prb60.md":
        "พระราชบัญญัติการจัดซื้อจัดจ้างและการบริหารพัสดุภาครัฐ พ.ศ. 2560",
    "reference/law/rbb60.md":
        "ระเบียบกระทรวงการคลังว่าด้วยการจัดซื้อจัดจ้างและการบริหารพัสดุภาครัฐ พ.ศ. 2560",
    "reference/law/rbb60-3.md":
        "ระเบียบกระทรวงการคลังว่าด้วยการจัดซื้อจัดจ้างและการบริหารพัสดุภาครัฐ (ฉบับที่ 3) พ.ศ. 2569",
    "reference/law/ministerial-regulations/mr-specific-2560.md":
        "กฎกระทรวงกำหนดวงเงินการจัดซื้อจัดจ้างพัสดุโดยวิธีเฉพาะเจาะจง วงเงินการจัดซื้อจัดจ้างที่ไม่ทำข้อตกลงเป็นหนังสือ และวงเงินการจัดซื้อจัดจ้างในการแต่งตั้งผู้ตรวจรับพัสดุ พ.ศ. 2560",
    "reference/law/ministerial-regulations/mr-appeal-exclusions-2568.md":
        "กฎกระทรวงกำหนดเรื่องการจัดซื้อจัดจ้างกับหน่วยงานของรัฐที่ใช้สิทธิอุทธรณ์ไม่ได้ พ.ศ. 2568",
    "reference/circulars/circular-w367-2567.md":
        "หนังสือเวียน ว 367 ลงวันที่ 25 มิถุนายน 2567",
    "reference/circulars/circular-w214-2563.md":
        "หนังสือเวียน ว 214 ลงวันที่ 18 พฤษภาคม 2563",
}

THAI_DIGITS = str.maketrans("๐๑๒๓๔๕๖๗๘๙", "0123456789")
CLAUSE_NUMBER_PATTERN = r"[0-9๐-๙]+(?:/[0-9๐-๙]+)?"
REFERENCE_SECTION_NUMBER_PATTERN = r"[0-9๐-๙]+(?:(?:/|\.)[0-9๐-๙]+)*"
QUESTION_PREFIXES = ("/pasadu", "/passadu", "ในระเบียบ", "ตามระเบียบ")
QUESTION_TAIL_MARKERS = (
    "อยู่ข้อไหน",
    "เขียนว่าอะไร",
    "กล่าวว่าอะไร",
    "กล่าวถึงอะไร",
    "คืออะไร",
    "ได้เท่าไหร่",
    "ได้ไม่เกินเท่าไหร่",
    "ต้องทำอย่างไร",
    "ทำอย่างไร",
    "หรือไม่",
    "ไหม",
    "ถ้า",
)
GENERIC_DOMAIN_SUFFIXES = ("พัสดุ", "วัสดุ")


def normalize_digits(text: str) -> str:
    return text.translate(THAI_DIGITS)


def normalize_search_text(text: str) -> str:
    normalized = unicodedata.normalize("NFD", normalize_digits(text.lower()))
    return normalized.replace("ำ", "ํา")


def character_ngrams(text: str, size: int = 4) -> set[str]:
    compact = re.sub(r"[^a-z0-9ก-๙]+", "", normalize_search_text(text))
    return {
        compact[index : index + size]
        for index in range(max(0, len(compact) - size + 1))
    }


def compact_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def repo_relative(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def display_source(source: str) -> str:
    """Return the human-readable authority name for an internal source path."""
    return SOURCE_DISPLAY_NAMES.get(source, source)


def format_citation(source: str, clause_type: str, clause_no: object) -> str:
    """Format a citation for users without exposing repository filenames."""
    return f"{display_source(source)} {clause_type} {clause_no}"


def tokenize(text: str) -> list[str]:
    normalized = normalize_search_text(text)
    return re.findall(r"[a-z0-9]+|[ก-๙]+", normalized)


def focus_phrases(query: str) -> list[str]:
    """Extract Thai subject phrases without requiring a Thai word segmenter."""
    normalized = normalize_search_text(query)
    for prefix in QUESTION_PREFIXES:
        normalized = normalized.replace(prefix, " ")

    phrases: list[str] = []
    for token in tokenize(normalized):
        phrase = token
        for marker in QUESTION_TAIL_MARKERS:
            marker_at = phrase.find(marker)
            if marker_at >= 0:
                phrase = phrase[:marker_at]
        if len(phrase) >= 4 and phrase not in phrases:
            phrases.append(phrase)
        for suffix in GENERIC_DOMAIN_SUFFIXES:
            if phrase.endswith(suffix):
                shorter = phrase[: -len(suffix)]
                if len(shorter) >= 4 and shorter not in phrases:
                    phrases.append(shorter)
    return phrases
