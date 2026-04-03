from datetime import date
from uuid import UUID

from showcase.domain.dog import Dog
from showcase.domain.owner_id import OwnerId
from showcase.domain.profile_image_key import ProfileImageKey
from showcase.domain.repositories import DogRepository

_ALLOWED_PATCH_KEYS = frozenset(
    {
        "name",
        "birth_date",
        "weight",
        "color",
        "gender",
        "breed_code",
        "profile_image_key",
    }
)


def _normalize_patch(raw: dict) -> dict:
    patch: dict = {}
    for key in _ALLOWED_PATCH_KEYS:
        if key not in raw:
            continue
        val = raw[key]
        if key == "birth_date":
            if val is None:
                raise ValueError("birth_date must not be null")
            if isinstance(val, date):
                patch[key] = val
            else:
                patch[key] = date.fromisoformat(str(val))
        elif key == "weight":
            patch[key] = float(val)
        elif key == "breed_code":
            patch[key] = int(val)
        elif key == "profile_image_key":
            if val is None or val == "":
                patch[key] = None
            else:
                patch[key] = ProfileImageKey.parse(str(val))
        elif key in ("name", "color", "gender"):
            if val is None:
                raise ValueError(f"{key} must not be null")
            patch[key] = str(val)
    return patch


class UpdateMyDogUseCase:
    def __init__(self, dog_repository: DogRepository):
        self.dog_repository = dog_repository

    def execute(self, owner_id: OwnerId, dog_id: UUID, raw_patch: dict) -> Dog | None:
        dog = self.dog_repository.get_by_id_for_owner(owner_id, dog_id)
        if dog is None:
            return None
        normalized = _normalize_patch(raw_patch)
        updated = dog.merge_patch(normalized)
        self.dog_repository.save(updated)
        return updated
