"""メール・犬名などの個人情報をアプリ層で暗号化する（Fernet）。"""

from __future__ import annotations

import base64
import hashlib
import hmac
from functools import lru_cache

from cryptography.fernet import Fernet
from django.conf import settings

from showcase.domain.email import Email


@lru_cache(maxsize=1)
def _fernet() -> Fernet:
    raw = (getattr(settings, "SHOWCASE_PII_FERNET_KEY", None) or "").strip()
    if raw:
        return Fernet(raw.encode("ascii"))
    digest = hashlib.sha256(
        (settings.SECRET_KEY + "showcase-pii-fernet-v1").encode()
    ).digest()
    key = base64.urlsafe_b64encode(digest)
    return Fernet(key)


def email_login_username(email: Email) -> str:
    """ログイン・重複チェック用。平文メールから決定的に導く擬似ユーザー名（HMAC-SHA256 hex）。"""
    secret = (settings.SECRET_KEY + "showcase-pii-email-hmac-v1").encode()
    return hmac.new(secret, email.value.encode("utf-8"), hashlib.sha256).hexdigest()


def encrypt_pii(plain: str) -> str:
    return _fernet().encrypt(plain.encode("utf-8")).decode("ascii")


def decrypt_pii(cipher: str) -> str:
    return _fernet().decrypt(cipher.encode("ascii")).decode("utf-8")
