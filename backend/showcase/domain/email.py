"""メールアドレスを値オブジェクトとして表す（お手本）。"""

from dataclasses import dataclass

from showcase.domain.exceptions import DomainValidationError


@dataclass(frozen=True, slots=True)
class Email:
    """空白を除き、最低限の形式だけを保証する例。"""

    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise DomainValidationError("email_empty")
        if (
            "@" not in self.value
            or self.value.startswith("@")
            or self.value.endswith("@")
        ):
            raise DomainValidationError("email_invalid_format")

    @classmethod
    def parse(cls, raw: str) -> "Email":
        normalized = (raw or "").strip().lower()
        return cls(value=normalized)
