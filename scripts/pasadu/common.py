from __future__ import annotations

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
REFERENCE_ROOT = REPO_ROOT / "reference"
INDEX_ROOT = REPO_ROOT / "data" / "index"

LAW_FILES = {
    "prb60": REFERENCE_ROOT / "law" / "prb60.md",
    "rbb60": REFERENCE_ROOT / "law" / "rbb60.md",
    "rbb60-3": REFERENCE_ROOT / "law" / "rbb60-3.md",
}

THAI_DIGITS = str.maketrans("๐๑๒๓๔๕๖๗๘๙", "0123456789")


def normalize_digits(text: str) -> str:
    return text.translate(THAI_DIGITS)


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


def tokenize(text: str) -> list[str]:
    normalized = normalize_digits(text.lower())
    return re.findall(r"[a-z0-9]+|[ก-๙]+", normalized)
