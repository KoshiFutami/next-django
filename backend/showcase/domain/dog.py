from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from uuid import UUID

from showcase.domain.owner_id import OwnerId
from showcase.domain.profile_image_key import ProfileImageKey


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(slots=True)
class Dog:
    """犬の情報を表すクラス"""

    id: UUID
    name: str
    birth_date: date
    weight: float
    color: str
    gender: str
    owner_id: OwnerId
    breed_code: int
    profile_image_key: ProfileImageKey | None = None

    created_at: datetime = field(default_factory=_utc_now)
