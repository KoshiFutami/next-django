"""飼い主（Owner）集約ルート（お手本）。永続化はリポジトリに委譲する。"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from showcase.domain.email import Email
from showcase.domain.exceptions import DomainValidationError
from showcase.domain.handle import parse_handle
from showcase.domain.owner_id import OwnerId
from showcase.domain.profile_image_key import ProfileImageKey


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _validate_full_name(full_name: str) -> str:
    name = (full_name or "").strip()
    if not name:
        raise DomainValidationError("full_name_empty")
    if len(name) > 128:
        raise DomainValidationError("full_name_too_long")
    return name


@dataclass(slots=True)
class Owner:
    """登録済みの飼い主（利用者）を表す。"""

    id: OwnerId
    email: Email
    nickname: str
    full_name: str
    handle: str
    profile_image_key: ProfileImageKey | None = None
    created_at: datetime = field(default_factory=_utc_now)

    @classmethod
    def register(
        cls,
        *,
        email: Email,
        nickname: str,
        full_name: str,
        handle: str,
        profile_image_key: ProfileImageKey | None = None,
    ) -> "Owner":
        """新規登録のファクトリ。不変条件はここに集約する。"""
        nick = (nickname or "").strip()
        if not nick:
            raise DomainValidationError("nickname_empty")
        if len(nick) > 64:
            raise DomainValidationError("nickname_too_long")
        fn = _validate_full_name(full_name)
        handle_norm = parse_handle(handle)
        return cls(
            id=OwnerId.generate(),
            email=email,
            nickname=nick,
            full_name=fn,
            handle=handle_norm,
            profile_image_key=profile_image_key,
            created_at=_utc_now(),
        )

    def merge_patch(self, patch: dict[str, Any]) -> "Owner":
        """許可キーのみ上書きした新インスタンス。値はアプリケーション層で型済み。"""
        nickname = patch["nickname"] if "nickname" in patch else self.nickname
        if "full_name" in patch:
            raw_fn = patch["full_name"]
            full_name = str(raw_fn) if raw_fn is not None else ""
        else:
            full_name = self.full_name
        handle_in_patch = "handle" in patch
        profile_image_key = (
            patch["profile_image_key"]
            if "profile_image_key" in patch
            else self.profile_image_key
        )
        nick = (nickname or "").strip()
        if not nick:
            raise DomainValidationError("nickname_empty")
        if len(nick) > 64:
            raise DomainValidationError("nickname_too_long")
        fn = _validate_full_name(full_name)
        handle_norm: str
        if handle_in_patch:
            h = patch["handle"]
            if h is None or (isinstance(h, str) and not str(h).strip()):
                raise DomainValidationError("handle_empty")
            handle_norm = parse_handle(str(h))
        else:
            handle_norm = self.handle
        if profile_image_key and len(profile_image_key.value) > 512:
            raise DomainValidationError("profile_image_key_too_long")
        return Owner(
            id=self.id,
            email=self.email,
            nickname=nick,
            full_name=fn,
            handle=handle_norm,
            profile_image_key=profile_image_key,
            created_at=self.created_at,
        )
