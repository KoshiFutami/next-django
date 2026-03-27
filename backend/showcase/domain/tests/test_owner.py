import pytest

from showcase.domain.email import Email
from showcase.domain.exceptions import DomainValidationError
from showcase.domain.owner import Owner
from showcase.domain.owner_id import OwnerId
from showcase.domain.profile_image_key import ProfileImageKey


def test_email_parse_normalizes_and_accepts_valid():
    e = Email.parse("  Hello@Example.COM ")
    assert e.value == "hello@example.com"


@pytest.mark.parametrize(
    "raw",
    ["", " ", "a@", "@b", "no-at"],
)
def test_email_rejects_invalid(raw: str):
    with pytest.raises(DomainValidationError):
        Email.parse(raw)


def test_owner_register_success():
    owner = Owner.register(
        email=Email.parse("owner@example.com"),
        nickname="  太郎  ",
    )
    assert isinstance(owner.id, OwnerId)
    assert owner.nickname == "太郎"
    assert owner.email.value == "owner@example.com"
    assert owner.profile_image_key is None


@pytest.mark.parametrize("nickname", ["", "   "])
def test_owner_register_rejects_empty_nickname(nickname: str):
    with pytest.raises(DomainValidationError, match="nickname_empty"):
        Owner.register(email=Email.parse("a@b.co"), nickname=nickname)


def test_owner_register_rejects_long_nickname():
    with pytest.raises(DomainValidationError, match="nickname_too_long"):
        Owner.register(email=Email.parse("a@b.co"), nickname="x" * 65)


def test_owner_register_with_profile_image():
    key = ProfileImageKey.parse("uploads/owners/abc.webp")
    owner = Owner.register(
        email=Email.parse("owner@example.com"),
        nickname="太郎",
        profile_image_key=key,
    )
    assert owner.profile_image_key == key
