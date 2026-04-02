from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from uuid import UUID, uuid4

from showcase.domain.exceptions import DomainValidationError
from showcase.domain.owner_id import OwnerId
from showcase.domain.profile_image_key import ProfileImageKey
from showcase.domain.life_stage import LifeStage


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

    def life_stage(self, as_of: date) -> LifeStage:
        if as_of < self.birth_date:
            return LifeStage.NOT_YET_BORN
        if as_of < self.birth_date + timedelta(days=30):
            return LifeStage.NEWBORN
        if as_of < self.birth_date + timedelta(days=365):
            return LifeStage.YOUNG
        return LifeStage.ADULT


    @classmethod
    def register(cls, *, name: str, birth_date: date, weight: float, color: str, gender: str, owner_id: OwnerId, breed_code: int, profile_image_key: ProfileImageKey | None = None) -> "Dog":
        if not name:
            raise DomainValidationError("name_empty")
        if len(name) > 128:
            raise DomainValidationError("name_too_long")
        if birth_date > date.today():
            raise DomainValidationError("birth_date_empty")
        if weight <= 0:
            raise DomainValidationError("weight_negative")
        if len(color) > 64:
            raise DomainValidationError("color_too_long")
        if len(gender) > 32:
            raise DomainValidationError("gender_too_long")
        if not owner_id:
            raise DomainValidationError("owner_id_empty")
        if breed_code <= 0:
            raise DomainValidationError("breed_code_negative")
        if profile_image_key and len(profile_image_key.value) > 512:
            raise DomainValidationError("profile_image_key_too_long")
        
        return cls(
            id=uuid4(),
            name=name,
            birth_date=birth_date,
            weight=weight,
            color=color,
            gender=gender,
            owner_id=owner_id,
            breed_code=breed_code,
            profile_image_key=profile_image_key,
            created_at=_utc_now(),
        )