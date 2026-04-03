import json
from datetime import datetime, timezone
from uuid import UUID, uuid4

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.test.utils import override_settings

from showcase.models import OwnerProfile as OwnerProfileRow

STUB_OWNER_ID = UUID("00000000-0000-0000-0000-000000000001")


def _stub_owner():
    User = get_user_model()
    u = User.objects.create_user(
        username="me@example.com", email="me@example.com", password="x"
    )
    OwnerProfileRow.objects.create(
        id=STUB_OWNER_ID,
        user=u,
        nickname="スタブ",
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
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
