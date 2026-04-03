"""認証。`Authorization: Bearer` があれば JWT から Owner を解決し、なければスタブ ID。"""

from uuid import UUID

from django.conf import settings
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

from showcase.domain.owner_id import OwnerId
from showcase.models import OwnerProfile as OwnerProfileRow


class OwnerAuthError(Exception):
    """Bearer が不正・期限切れ、または User に OwnerProfile が無い。"""


def _owner_id_from_bearer_token(token_str: str) -> OwnerId:
    try:
        token = AccessToken(token_str)
        user_id = token["user_id"]
    except TokenError as exc:
        raise OwnerAuthError("トークンが無効または期限切れです") from exc
    row = OwnerProfileRow.objects.filter(user_id=user_id).first()
    if row is None:
        raise OwnerAuthError("利用者プロフィールが見つかりません")
    return OwnerId(value=row.id)


def get_current_owner_id(request) -> OwnerId:
    auth_header = request.META.get("HTTP_AUTHORIZATION", "")
    parts = auth_header.split(None, 1)
    if len(parts) == 2 and parts[0].lower() == "bearer":
        token_str = parts[1].strip()
        if not token_str:
            raise OwnerAuthError("Bearer トークンが空です")
        return _owner_id_from_bearer_token(token_str)

    raw = getattr(settings, "SHOWCASE_STUB_OWNER_ID", None)
    if raw is None or raw == "":
        raise RuntimeError("SHOWCASE_STUB_OWNER_ID is not set")
    return OwnerId(value=UUID(str(raw)))
