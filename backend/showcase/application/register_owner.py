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
        for key in ("email", "password", "nickname"):
            if key not in raw or raw[key] is None:
                raise ValueError(f"{key} is required")
        password = raw["password"]
        if not isinstance(password, str):
            raise ValueError("password must be a string")
        nickname = raw["nickname"]
        if not isinstance(nickname, str):
            raise ValueError("nickname must be a string")

        try:
            validate_password(password)
        except DjangoValidationError as exc:
            raise ValueError(" ".join(exc.messages)) from exc

        email = Email.parse(str(raw["email"]))
        if self._repo.is_email_registered(email):
            raise EmailAlreadyRegisteredError

        profile_image_key = _optional_profile_image_key(raw)
        reg_kwargs: dict = {
            "email": email,
            "nickname": nickname,
            "profile_image_key": profile_image_key,
        }
        if "full_name" in raw:
            reg_kwargs["full_name"] = (
                "" if raw["full_name"] is None else str(raw["full_name"])
            )
        if "handle" in raw:
            h = raw["handle"]
            reg_kwargs["handle"] = None if h is None else str(h)
        owner = Owner.register(**reg_kwargs)
        if owner.handle and self._repo.is_handle_taken(owner.handle):
            raise HandleAlreadyRegisteredError
        self._repo.register_with_password(owner, password)
        return owner
