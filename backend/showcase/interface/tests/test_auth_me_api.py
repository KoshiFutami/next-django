import json
from uuid import UUID, uuid4

import pytest
from django.test import Client
from django.test.utils import override_settings

from showcase.infrastructure import pii_crypto
from showcase.interface.tests.pii_test_util import (
    create_owner_profile,
    create_user,
)
from showcase.models import OwnerProfile as OwnerProfileRow

STUB_OWNER_ID = UUID("00000000-0000-0000-0000-000000000001")


def _stub_owner():
    u = create_user("me@example.com", "x")
    create_owner_profile(
        user=u,
        owner_id=STUB_OWNER_ID,
        nickname="スタブ",
        account_email="me@example.com",
    )


@pytest.mark.django_db
@override_settings(SHOWCASE_STUB_OWNER_ID=str(STUB_OWNER_ID))
def test_auth_me_get_returns_profile():
    _stub_owner()
    client = Client()
    res = client.get("/api/auth/me/")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == str(STUB_OWNER_ID)
    assert data["email"] == "me@example.com"
    assert data["nickname"] == "スタブ"
    assert data["full_name"] == "テスト本名"
    assert data["handle"] == "h_00000000000000000000"
    assert data["profile_image_key"] is None
    assert "created_at" in data


@pytest.mark.django_db
@override_settings(SHOWCASE_STUB_OWNER_ID=str(uuid4()))
def test_auth_me_get_missing_owner_returns_404():
    client = Client()
    res = client.get("/api/auth/me/")
    assert res.status_code == 404
    assert res.json()["code"] == "not_found"


@pytest.mark.django_db
@override_settings(SHOWCASE_STUB_OWNER_ID=str(STUB_OWNER_ID))
def test_auth_me_patch_updates_nickname():
    _stub_owner()
    client = Client()
    res = client.patch(
        "/api/auth/me/",
        data=json.dumps({"nickname": "  新ニック  "}),
        content_type="application/json",
    )
    assert res.status_code == 200
    assert res.json()["nickname"] == "新ニック"
    row = OwnerProfileRow.objects.get(pk=STUB_OWNER_ID)
    assert row.nickname == "新ニック"


@pytest.mark.django_db
@override_settings(SHOWCASE_STUB_OWNER_ID=str(STUB_OWNER_ID))
def test_auth_me_patch_updates_full_name_and_handle():
    _stub_owner()
    client = Client()
    res = client.patch(
        "/api/auth/me/",
        data=json.dumps(
            {
                "full_name": "  山田 花子  ",
                "handle": "@hanako_y",
            }
        ),
        content_type="application/json",
    )
    assert res.status_code == 200
    data = res.json()
    assert data["full_name"] == "山田 花子"
    assert data["handle"] == "hanako_y"
    row = OwnerProfileRow.objects.get(pk=STUB_OWNER_ID)
    assert pii_crypto.decrypt_pii(row.full_name) == "山田 花子"
    assert row.handle == "hanako_y"


@pytest.mark.django_db
def test_auth_me_patch_duplicate_handle_returns_409():
    client = Client()
    for email, handle, nick in (
        ("h1@example.com", "taken_handle_9", "A"),
        ("h2@example.com", "other_handle_9", "B"),
    ):
        r = client.post(
            "/api/auth/register/",
            data=json.dumps(
                {
                    "email": email,
                    "password": "dup_handle_pass_9",
                    "nickname": nick,
                    "full_name": f"{nick}本名",
                    "handle": handle,
                }
            ),
            content_type="application/json",
        )
        assert r.status_code == 201
    login = client.post(
        "/api/auth/login/",
        data=json.dumps({"email": "h2@example.com", "password": "dup_handle_pass_9"}),
        content_type="application/json",
    )
    assert login.status_code == 200
    access = login.json()["access"]
    res = client.patch(
        "/api/auth/me/",
        data=json.dumps({"handle": "taken_handle_9"}),
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {access}",
    )
    assert res.status_code == 409
    assert res.json()["code"] == "handle_already_registered"


@pytest.mark.django_db
@override_settings(SHOWCASE_STUB_OWNER_ID=str(STUB_OWNER_ID))
def test_auth_me_patch_empty_nickname_returns_400():
    _stub_owner()
    client = Client()
    res = client.patch(
        "/api/auth/me/",
        data=json.dumps({"nickname": ""}),
        content_type="application/json",
    )
    assert res.status_code == 400
    assert res.json()["code"] == "bad_request"


@pytest.mark.django_db
@override_settings(SHOWCASE_STUB_OWNER_ID=str(STUB_OWNER_ID))
def test_auth_me_get_with_invalid_bearer_returns_401():
    _stub_owner()
    client = Client()
    res = client.get(
        "/api/auth/me/",
        HTTP_AUTHORIZATION="Bearer not-a-valid-jwt",
    )
    assert res.status_code == 401
    assert res.json()["code"] == "unauthorized"


@pytest.mark.django_db
@override_settings(SHOWCASE_STUB_OWNER_ID=str(STUB_OWNER_ID))
def test_auth_me_method_post_returns_405():
    _stub_owner()
    client = Client()
    res = client.post("/api/auth/me/")
    assert res.status_code == 405
    assert res.json()["code"] == "method_not_allowed"
