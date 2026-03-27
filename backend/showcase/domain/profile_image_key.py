"""プロフィール画像のストレージキー（パスはインフラ側のルールに従う）。"""

from dataclasses import dataclass

from showcase.domain.exceptions import DomainValidationError


@dataclass(frozen=True, slots=True)
class ProfileImageKey:
    """例: uploads/dogs/{uuid}.webp — 実体のファイルは infrastructure が扱う。"""

    value: str

    def __post_init__(self) -> None:
        v = self.value
        if not v or not v.strip():
            raise DomainValidationError("profile_image_key_empty")
        if ".." in v or v.startswith("/"):
            raise DomainValidationError("profile_image_key_invalid")
        if len(v) > 512:
            raise DomainValidationError("profile_image_key_too_long")

    @classmethod
    def parse(cls, raw: str) -> "ProfileImageKey":
        return cls(value=(raw or "").strip())
