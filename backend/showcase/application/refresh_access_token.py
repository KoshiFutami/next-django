from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


class RefreshTokenInvalidError(Exception):
    """リフレッシュトークンが無効・期限切れ・改ざんされている。"""


class RefreshAccessTokenUseCase:
    def execute(self, raw: dict) -> str:
        if "refresh" not in raw or raw["refresh"] is None:
            raise ValueError("refresh is required")
        token_str = raw["refresh"]
        if not isinstance(token_str, str) or not token_str.strip():
            raise ValueError("refresh must be a non-empty string")
        try:
            refresh = RefreshToken(token_str)
        except TokenError as exc:
            raise RefreshTokenInvalidError from exc
        return str(refresh.access_token)
