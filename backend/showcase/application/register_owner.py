from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from showcase.domain.email import Email
from showcase.domain.exceptions import (
    EmailAlreadyRegisteredError,
    HandleAlreadyRegisteredError,
)
from showcase.domain.owner import Owner
from showcase.domain.profile_image_key import ProfileImageKey
from showcase.domain.repositories import OwnerRepository


def _optional_profile_image_key(raw: dict) -> ProfileImageKey | None:
    if "profile_image_key" not in raw:
        return None
    val = raw["profile_image_key"]
    if val is None or val == "":
        return None
    return ProfileImageKey.parse(str(val))


class RegisterOwnerUseCase:
    def __init__(self, owner_repository: OwnerRepository):
        self._repo = owner_repository

    def execute(self, raw: dict) -> Owner:
        for key in ("email", "password", "nickname", "full_name", "handle"):
            if key not in raw or raw[key] is None:
                raise ValueError(f"{key} is required")
        password = raw["password"]
        if not isinstance(password, str):
            raise ValueError("password must be a string")
        nickname = raw["nickname"]
        if not isinstance(nickname, str):
            raise ValueError("nickname must be a string")
        full_name = raw["full_name"]
        if not isinstance(full_name, str):
            raise ValueError("full_name must be a string")
        handle = raw["handle"]
        if not isinstance(handle, str):
            raise ValueError("handle must be a string")

        try:
            validate_password(password)
        except DjangoValidationError as exc:
            raise ValueError(" ".join(exc.messages)) from exc

        email = Email.parse(str(raw["email"]))
        if self._repo.is_email_registered(email):
            raise EmailAlreadyRegisteredError

        profile_image_key = _optional_profile_image_key(raw)
        owner = Owner.register(
            email=email,
            nickname=nickname,
            full_name=full_name,
            handle=handle,
            profile_image_key=profile_image_key,
        )
        if self._repo.is_handle_taken(owner.handle):
            raise HandleAlreadyRegisteredError
        self._repo.register_with_password(owner, password)
        return owner
