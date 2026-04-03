"""API テスト用: メール HMAC ユーザー名・暗号化メール。"""

from datetime import datetime, timezone
from uuid import UUID

from django.contrib.auth import get_user_model

from showcase.domain.email import Email
from showcase.infrastructure.pii_crypto import email_login_username, encrypt_pii
from showcase.models import OwnerProfile


def login_username(email: str) -> str:
    return email_login_username(Email.parse(email))


def create_user(email: str, password: str):
    return get_user_model().objects.create_user(
        username=login_username(email),
        email="",
        password=password,
    )


def create_owner_profile(
    *,
    user,
    owner_id: UUID,
    nickname: str,
    account_email: str,
    created_at=None,
    profile_image_key=None,
):
    if created_at is None:
        created_at = datetime.now(timezone.utc)
    return OwnerProfile.objects.create(
        id=owner_id,
        user=user,
        nickname=nickname,
        pii_email_ciphertext=encrypt_pii(Email.parse(account_email).value),
        profile_image_key=profile_image_key,
        created_at=created_at,
    )
