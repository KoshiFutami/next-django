"""認証。JWT 化時はここを差し替える。"""

from uuid import UUID

from django.conf import settings

from showcase.domain.owner_id import OwnerId


def get_current_owner_id(_request) -> OwnerId:
    raw = getattr(settings, "SHOWCASE_STUB_OWNER_ID", None)
    if raw is None or raw == "":
        raise RuntimeError("SHOWCASE_STUB_OWNER_ID is not set")
    return OwnerId(value=UUID(str(raw)))
