from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from showcase.application.refresh_access_token import RefreshTokenInvalidError


class RefreshAccessMismatchError(Exception):
    """body の refresh が access のユーザーと一致しない。"""


class LogoutOwnerUseCase:
    def execute(self, access_user_id: int, raw: dict) -> None:
        if "refresh" not in raw or raw["refresh"] is None:
            raise ValueError("refresh is required")
        refresh_str = raw["refresh"]
        if not isinstance(refresh_str, str) or not refresh_str.strip():
            raise ValueError("refresh must be a non-empty string")

        try:
            refresh = RefreshToken(refresh_str)
        except TokenError as exc:
            raise RefreshTokenInvalidError from exc

        if int(refresh["user_id"]) != int(access_user_id):
            raise RefreshAccessMismatchError

        refresh.blacklist()
