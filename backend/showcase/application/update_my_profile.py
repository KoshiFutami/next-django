from showcase.domain.exceptions import HandleAlreadyRegisteredError
from showcase.domain.owner import Owner
from showcase.domain.owner_id import OwnerId
from showcase.domain.profile_image_key import ProfileImageKey
from showcase.domain.repositories import OwnerRepository

_ALLOWED_PATCH_KEYS = frozenset(
    {"nickname", "profile_image_key", "full_name", "handle"}
)


def _normalize_patch(raw: dict) -> dict:
    patch: dict = {}
    for key in _ALLOWED_PATCH_KEYS:
        if key not in raw:
            continue
        val = raw[key]
        if key == "nickname":
            if val is None:
                raise ValueError("nickname must not be null")
            patch[key] = str(val)
        elif key == "profile_image_key":
            if val is None or val == "":
                patch[key] = None
            else:
                patch[key] = ProfileImageKey.parse(str(val))
        elif key == "full_name":
            patch[key] = "" if val is None else str(val)
        elif key == "handle":
            if val is None or val == "":
                patch[key] = None
            else:
                patch[key] = str(val)
    return patch


class UpdateMyProfileUseCase:
    def __init__(self, owner_repository: OwnerRepository):
        self.owner_repository = owner_repository

    def execute(self, owner_id: OwnerId, raw_patch: dict) -> Owner | None:
        owner = self.owner_repository.get_by_id(owner_id)
        if owner is None:
            return None
        normalized = _normalize_patch(raw_patch)
        if not normalized:
            return owner
        updated = owner.merge_patch(normalized)
        if updated.handle != owner.handle and updated.handle is not None:
            if self.owner_repository.is_handle_taken(
                updated.handle, exclude_owner_id=owner_id
            ):
                raise HandleAlreadyRegisteredError
        self.owner_repository.save(updated)
        return updated
