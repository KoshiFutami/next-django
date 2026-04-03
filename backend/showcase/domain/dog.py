from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from typing import Any
from uuid import UUID, uuid4

from showcase.domain.exceptions import DomainValidationError
from showcase.domain.life_stage import LifeStage
from showcase.domain.owner_id import OwnerId
from showcase.domain.profile_image_key import ProfileImageKey


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _validate_dog_attributes(
    name: str,
    birth_date: date,
    weight: float,
    color: str,
    gender: str,
    breed_code: int,
    profile_image_key: ProfileImageKey | None,
) -> None:
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
    if breed_code <= 0:
        raise DomainValidationError("breed_code_negative")
    if profile_image_key and len(profile_image_key.value) > 512:
        raise DomainValidationError("profile_image_key_too_long")


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
    def register(
        cls,
        *,
        name: str,
        birth_date: date,
        weight: float,
        color: str,
        gender: str,
        owner_id: OwnerId,
        breed_code: int,
        profile_image_key: ProfileImageKey | None = None,
    ) -> "Dog":
        if not owner_id:
            raise DomainValidationError("owner_id_empty")
        _validate_dog_attributes(
            name,
            birth_date,
            weight,
            color,
            gender,
            breed_code,
            profile_image_key,
        )

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

    def merge_patch(self, patch: dict[str, Any]) -> "Dog":
        """許可されたキーのみ上書きした新インスタンスを返す。値はアプリケーション層で型済み。"""
        name = patch["name"] if "name" in patch else self.name
        birth_date = patch["birth_date"] if "birth_date" in patch else self.birth_date
        weight = patch["weight"] if "weight" in patch else self.weight
        color = patch["color"] if "color" in patch else self.color
        gender = patch["gender"] if "gender" in patch else self.gender
        breed_code = patch["breed_code"] if "breed_code" in patch else self.breed_code
        profile_image_key = (
            patch["profile_image_key"]
            if "profile_image_key" in patch
            else self.profile_image_key
        )
        _validate_dog_attributes(
            name,
            birth_date,
            weight,
            color,
            gender,
            breed_code,
            profile_image_key,
        )
        return Dog(
            id=self.id,
            name=name,
            birth_date=birth_date,
            weight=weight,
            color=color,
            gender=gender,
            owner_id=self.owner_id,
            breed_code=breed_code,
            profile_image_key=profile_image_key,
            created_at=self.created_at,
        )
