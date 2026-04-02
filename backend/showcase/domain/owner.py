"""飼い主（Owner）集約ルート（お手本）。永続化はリポジトリに委譲する。"""

from dataclasses import dataclass, field
from datetime import datetime, timezone

from showcase.domain.email import Email
from showcase.domain.exceptions import DomainValidationError
from showcase.domain.owner_id import OwnerId
from showcase.domain.profile_image_key import ProfileImageKey


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(slots=True)
class Owner:
    """登録済みの飼い主（利用者）を表す。"""

    id: OwnerId
    email: Email
    nickname: str
    profile_image_key: ProfileImageKey | None = None
    created_at: datetime = field(default_factory=_utc_now)

    @classmethod
    def register(
        cls,
        *,
        email: Email,
        nickname: str,
        profile_image_key: ProfileImageKey | None = None,
    ) -> "Owner":
        """新規登録のファクトリ。不変条件はここに集約する。"""
        nick = (nickname or "").strip()
        if not nick:
            raise DomainValidationError("nickname_empty")
        if len(nick) > 64:
            raise DomainValidationError("nickname_too_long")
        return cls(
            id=OwnerId.generate(),
            email=email,
            nickname=nick,
            profile_image_key=profile_image_key,
            created_at=_utc_now(),
        )
