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
        full_name="山田太郎",
        handle="@owner_ok_h",
    )
    assert isinstance(owner.id, OwnerId)
    assert owner.nickname == "太郎"
    assert owner.email.value == "owner@example.com"
    assert owner.full_name == "山田太郎"
    assert owner.handle == "owner_ok_h"
    assert owner.profile_image_key is None


@pytest.mark.parametrize("full_name", ["", "   "])
def test_owner_register_rejects_empty_full_name(full_name: str):
    with pytest.raises(DomainValidationError, match="full_name_empty"):
        Owner.register(
            email=Email.parse("a@b.co"),
            nickname="x",
            full_name=full_name,
            handle="hx",
        )


def test_owner_register_rejects_long_full_name():
    with pytest.raises(DomainValidationError, match="full_name_too_long"):
        Owner.register(
            email=Email.parse("a@b.co"),
            nickname="x",
            full_name="あ" * 129,
            handle="hx",
        )


@pytest.mark.parametrize("nickname", ["", "   "])
def test_owner_register_rejects_empty_nickname(nickname: str):
    with pytest.raises(DomainValidationError, match="nickname_empty"):
        Owner.register(
            email=Email.parse("a@b.co"),
            nickname=nickname,
            full_name="名",
            handle="hx",
        )


def test_owner_register_rejects_long_nickname():
    with pytest.raises(DomainValidationError, match="nickname_too_long"):
        Owner.register(
            email=Email.parse("a@b.co"),
            nickname="x" * 65,
            full_name="名",
            handle="hx",
        )


def test_owner_register_with_profile_image():
    key = ProfileImageKey.parse("uploads/owners/abc.webp")
    owner = Owner.register(
        email=Email.parse("owner@example.com"),
        nickname="太郎",
        full_name="名",
        handle="img_owner_h",
        profile_image_key=key,
    )
    assert owner.profile_image_key == key


def test_owner_merge_patch_updates_nickname():
    owner = Owner.register(
        email=Email.parse("o@example.com"),
        nickname="旧名",
        full_name="本名",
        handle="patch_nick_h",
    )
    updated = owner.merge_patch({"nickname": "  新名  "})
    assert updated.nickname == "新名"
    assert updated.id == owner.id
    assert updated.email == owner.email
    assert updated.full_name == "本名"
    assert updated.handle == "patch_nick_h"


def test_owner_merge_patch_clears_profile_image():
    key = ProfileImageKey.parse("uploads/x.webp")
    owner = Owner.register(
        email=Email.parse("o@example.com"),
        nickname="太郎",
        full_name="名",
        handle="clr_img_h",
        profile_image_key=key,
    )
    updated = owner.merge_patch({"profile_image_key": None})
    assert updated.profile_image_key is None


@pytest.mark.parametrize("nickname", ["", "   "])
def test_owner_merge_patch_rejects_empty_nickname(nickname: str):
    owner = Owner.register(
        email=Email.parse("o@example.com"),
        nickname="太郎",
        full_name="名",
        handle="rej_nick_h",
    )
    with pytest.raises(DomainValidationError, match="nickname_empty"):
        owner.merge_patch({"nickname": nickname})


def test_owner_merge_patch_rejects_long_nickname():
    owner = Owner.register(
        email=Email.parse("o@example.com"),
        nickname="太郎",
        full_name="名",
        handle="rej_long_n_h",
    )
    with pytest.raises(DomainValidationError, match="nickname_too_long"):
        owner.merge_patch({"nickname": "x" * 65})


def test_owner_merge_patch_updates_full_name_and_handle():
    owner = Owner.register(
        email=Email.parse("o@example.com"),
        nickname="太郎",
        full_name="旧本名",
        handle="old_handle",
    )
    updated = owner.merge_patch(
        {"full_name": "新 名前", "handle": "@new_handle"},
    )
    assert updated.full_name == "新 名前"
    assert updated.handle == "new_handle"


@pytest.mark.parametrize("full_name", ["", "  ", None])
def test_owner_merge_patch_rejects_empty_full_name(full_name):
    owner = Owner.register(
        email=Email.parse("o@example.com"),
        nickname="太郎",
        full_name="元",
        handle="rej_fn_h",
    )
    with pytest.raises(DomainValidationError, match="full_name_empty"):
        owner.merge_patch({"full_name": full_name})


@pytest.mark.parametrize("h_raw", [None, "", "   "])
def test_owner_merge_patch_rejects_empty_handle(h_raw):
    owner = Owner.register(
        email=Email.parse("o@example.com"),
        nickname="太郎",
        full_name="名",
        handle="keep_handle",
    )
    with pytest.raises(DomainValidationError, match="handle_empty"):
        owner.merge_patch({"handle": h_raw})
