"""Validation helpers for the explicit Pasadu web-search fallback.

This module does not perform web requests. It validates the contract that the
root orchestrator must satisfy after using its web-search capability.
"""

from __future__ import annotations

from datetime import date
from urllib.parse import urlparse


WEB_FALLBACK_DISCLAIMER = (
    "คำตอบนี้ใช้ข้อมูลจาก web search ไม่ได้ใช้ฐานข้อมูลของ repository "
    "ข้อมูลมีโอกาสคลาดเคลื่อน โปรดตรวจสอบกับแหล่งทางการอีกครั้ง"
)
WEB_SOURCE_LABEL = "web source"
REPOSITORY_SOURCE_LABEL = "Repository source"
WEB_SOURCE_FIELDS = (
    "site_or_agency",
    "url",
    "accessed_at",
    "authority_name",
    "provision",
    "source_type",
)


def _non_empty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _valid_access_date(value: object) -> bool:
    if value is None or value == "":
        return True
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def validate_web_sources(sources: object) -> dict[str, object]:
    """Validate the structured metadata required for each web source."""

    errors: list[str] = []
    if not isinstance(sources, list) or not sources:
        return {"ok": False, "errors": ["at least one web source is required"]}

    for index, source in enumerate(sources, start=1):
        prefix = f"web source {index}"
        if not isinstance(source, dict):
            errors.append(f"{prefix} must be an object")
            continue
        missing = [field for field in WEB_SOURCE_FIELDS if field not in source]
        errors.extend(f"{prefix} missing {field}" for field in missing)
        if source.get("source_type") != WEB_SOURCE_LABEL:
            errors.append(f"{prefix} must be labelled '{WEB_SOURCE_LABEL}'")
        if not _non_empty(source.get("site_or_agency")):
            errors.append(f"{prefix} needs a site or owning agency")
        if not _valid_url(source.get("url")):
            errors.append(f"{prefix} needs a direct http(s) URL")
        if not _non_empty(source.get("authority_name")):
            errors.append(f"{prefix} needs a verified authority name")
        if not _non_empty(source.get("provision")):
            errors.append(f"{prefix} needs a verified provision or document number")
        if source.get("verified") is not True:
            errors.append(f"{prefix} must set verified=true")
        if not _valid_access_date(source.get("accessed_at")):
            errors.append(f"{prefix} accessed_at must be YYYY-MM-DD when provided")

    return {"ok": not errors, "errors": errors}


def validate_web_fallback_answer(
    answer: str,
    sources: object,
    *,
    repository_partial: bool = False,
) -> dict[str, object]:
    """Validate disclaimer, source labels, and visible metadata in an answer."""

    errors: list[str] = []
    if not isinstance(answer, str) or not answer.startswith(WEB_FALLBACK_DISCLAIMER):
        errors.append("the exact web fallback disclaimer must be the first content")

    source_result = validate_web_sources(sources)
    errors.extend(str(error) for error in source_result["errors"])

    if WEB_SOURCE_LABEL not in answer:
        errors.append("the answer must label the external material as 'web source'")
    if repository_partial and REPOSITORY_SOURCE_LABEL not in answer:
        errors.append("partial repository evidence must be under 'Repository source'")

    if isinstance(sources, list):
        for index, source in enumerate(sources, start=1):
            if not isinstance(source, dict):
                continue
            for field in ("site_or_agency", "url", "authority_name", "provision"):
                value = source.get(field)
                if _non_empty(value) and str(value) not in answer:
                    errors.append(f"web source {index} {field} is not shown in the answer")

    return {"ok": not errors, "errors": errors}


__all__ = [
    "REPOSITORY_SOURCE_LABEL",
    "WEB_FALLBACK_DISCLAIMER",
    "WEB_SOURCE_LABEL",
    "validate_web_fallback_answer",
    "validate_web_sources",
]
