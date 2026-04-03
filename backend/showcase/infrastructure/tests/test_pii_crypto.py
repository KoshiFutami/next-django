import pytest

from showcase.domain.email import Email
from showcase.infrastructure.pii_crypto import (
    decrypt_pii,
    email_login_username,
    encrypt_pii,
)


@pytest.mark.django_db
def test_encrypt_decrypt_roundtrip():
    c = encrypt_pii("hello@example.com")
    assert decrypt_pii(c) == "hello@example.com"


@pytest.mark.django_db
def test_email_login_username_is_deterministic():
    e = Email.parse("A@B.CO")
    assert email_login_username(e) == email_login_username(Email.parse("a@b.co"))
