"""公開用ハンドル（@ の後ろ相当）。正規化・検証のみ。"""

import re

from showcase.domain.exceptions import DomainValidationError

_HANDLE_RE = re.compile(r"^[a-z0-9]([a-z0-9._]{1,28}[a-z0-9])?$")

_RESERVED = frozenset(
    {
        "admin",
        "api",
        "auth",
        "breeds",
        "dogs",
        "explore",
        "health",
        "help",
        "me",
        "null",
        "owner",
        "reels",
        "settings",
        "support",
        "system",
        "undefined",
        "www",
    }
)


def parse_optional_handle(raw: str | None) -> str | None:
    """先頭の @ を除き小文字化。空なら None。形式・予約語違反で DomainValidationError。"""
    if raw is None:
        return None
    s = (raw or "").strip()
    if not s:
        return None
    if s.startswith("@"):
        s = s[1:].strip()
    if not s:
        return None
    normalized = s.lower()
    if len(normalized) < 3 or len(normalized) > 30:
        raise DomainValidationError("handle_length_invalid")
    if not _HANDLE_RE.fullmatch(normalized):
        raise DomainValidationError("handle_format_invalid")
    if ".." in normalized:
        raise DomainValidationError("handle_format_invalid")
    if normalized in _RESERVED:
        raise DomainValidationError("handle_reserved")
    return normalized
