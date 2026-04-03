from dataclasses import dataclass

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from showcase.domain.email import Email
from showcase.domain.owner import Owner
from showcase.domain.repositories import OwnerRepository


class LoginFailedError(Exception):
    """メールまたはパスワードが一致しない（列挙を避けるため詳細は返さない）。"""


@dataclass(frozen=True, slots=True)
class LoginResult:
    owner: Owner
    access: str
    refresh: str


class LoginOwnerUseCase:
    def __init__(self, owner_repository: OwnerRepository):
        self._repo = owner_repository

    def execute(self, raw: dict) -> LoginResult:
        if "email" not in raw or raw["email"] is None:
            raise ValueError("email is required")
        if "password" not in raw or raw["password"] is None:
            raise ValueError("password is required")
        password = raw["password"]
        if not isinstance(password, str):
            raise ValueError("password must be a string")

        email = Email.parse(str(raw["email"]))
        user = authenticate(
            request=None,
            username=email.value,
            password=password,
        )
        if user is None:
            raise LoginFailedError
        owner = self._repo.get_by_email(email)
        if owner is None:
            raise LoginFailedError

        refresh = RefreshToken.for_user(user)
        return LoginResult(
            owner=owner,
            access=str(refresh.access_token),
            refresh=str(refresh),
        )
